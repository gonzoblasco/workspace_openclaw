// job-application.test.js – Tests para las funciones puras del skill
//
// POR QUÉ EXISTE (2026-10-23): validar que los utilities de `react-form.mjs`
// y la detección de ATS funcionan sin necesidad de lanzar un browser.
//
// POR QUÉ EXISTE LA PARTE DE DISCOVERY (2026-10-25): el radar de vacantes
// dejo de encontrar nada y la causa NO fue que no hubiera vacantes: fueron
// cinco bugs encadenados, cada uno invisible desde afuera (un radar mudo
// parece "no hay nada"). El mas caro: las fuentes se llamaban con los
// argumentos en el orden equivocado, asi que se buscaban las vacantes de
// "AR" en vez de la query.
//
// La leccion: un scraper sin tests es un scraper que se rompe callado. Estos
// tests son los que hacen que un cambio de markup o de parametro en un sitio
// SALGA en la suite, en vez de en el silencio. Por eso el parser de LinkedIn
// y el filtro de pais viven en lib/discovery.mjs (puros y testeados), y no
// inline en el script que hace la red.

const path = require('node:path');
// Helpers para cargar módulos ESM desde CommonJS test runner.
async function importMjs(rel) {
  // __dirname está disponible en CommonJS.
  const modPath = path.resolve(__dirname, '..', '..', rel);
  return await import(modPath);
}

let reactValue, verifyFields, detectAdapter;
let matchesCountry, isRemoteAnywhere, parseLinkedinCards, filterJobs, listOf;

(async () => {
  const { reactValue: rv, verifyFields: vf } = await importMjs('skills/job-application/scripts/lib/react-form.mjs');
  reactValue = rv;
  verifyFields = vf;
  const { detectAdapter: da } = await importMjs('skills/job-application/scripts/lib/ats.mjs');
  detectAdapter = da;
  const disc = await importMjs('skills/job-application/scripts/lib/discovery.mjs');
  matchesCountry = disc.matchesCountry;
  isRemoteAnywhere = disc.isRemoteAnywhere;
  parseLinkedinCards = disc.parseLinkedinCards;
  filterJobs = disc.filterJobs;
  listOf = disc.listOf;
})();

// Helper fake page/locator for verifyFields.
class FakeLocator {
  constructor(dom, react) {
    this._dom = dom;
    this._react = react;
  }
  async inputValue() {
    return this._dom;
  }
  async evaluate(fn) {
    // Simula un element con _valueTracker.
    const el = { _valueTracker: { getValue: () => this._react } };
    return fn(el);
  }
  async count() {
    return 1;
  }
  // Playwright tiene .first() y el codigo lo usa: el fake tiene que
  // imitarlo, o verifyFields reventaba en los tests.
  first() {
    return this;
  }
}

// Un locator SIN _valueTracker: los forms que no son React (Lever) no lo
// tienen. El gate tiene que distinguir "no verificable" de "divergente".
class FakeLocatorSinTracker {
  constructor(dom) {
    this._dom = dom;
  }
  async inputValue() {
    return this._dom;
  }
  async evaluate(fn) {
    return fn({}); // sin _valueTracker
  }
  async count() {
    return 1;
  }
  // Playwright tiene .first() y el codigo lo usa: el fake tiene que
  // imitarlo, o verifyFields reventaba en los tests.
  first() {
    return this;
  }
}

class FakePageSinTracker {
  constructor(map) {
    this.map = map;
  }
  locator(sel) {
    return new FakeLocatorSinTracker(this.map[sel] || '');
  }
}

class FakePage {
  constructor(map) {
    this.map = map; // selector -> {dom,react}
  }
  locator(sel) {
    const def = this.map[sel] || { dom: '', react: '' };
    return new FakeLocator(def.dom, def.react);
  }
}

function report(name, cond, detail) {
  if (cond) {
    console.log(`ok ${name}`);
  } else {
    console.log(`FAIL ${name}${detail ? ' -- ' + detail : ''}`);
    process.exitCode = 1;
  }
}

// Wait a tick for imports to finish.
setTimeout(() => {
  // ==== reactValue ==== //
  const elWith = { _valueTracker: { getValue: () => 'hello' } };
  report('reactValue returns tracker value', reactValue(elWith) === 'hello');
  const elWithout = {};
  report('reactValue returns null when no tracker', reactValue(elWithout) === null);

  // ==== verifyFields ==== //
  const fakePage = new FakePage({
    '#email': { dom: 'a@b.com', react: 'a@b.com' },
    '#phone': { dom: '123', react: '456' }, // diverge
  });
  verifyFields(fakePage, ['#email', '#phone']).then((div) => {
    report('verifyFields detects divergencias', div.length === 1 && div[0].selector === '#phone');
  }).catch((e) => {
    console.error('verifyFields error', e);
    process.exitCode = 1;
  });

  // ==== verifyFields: form NO-React (Lever) ==== //
  // BUG CORREGIDO 2026-10-25: los inputs de Lever no tienen
  // _valueTracker. El gate comparaba el DOM contra "" y reportaba
  // divergencia en TODOS los campos, con el formulario impecable: un falso
  // positivo que hacia parecer roto lo que funcionaba.
  const fakePageSinTracker = new FakePageSinTracker({
    '#name': 'Gonzalo Blasco',
    '#salary': '3200',
  });
  verifyFields(fakePageSinTracker, ['#name', '#salary']).then((div) => {
    report(
      'verifyFields: sin tracker NO reporta divergencia',
      div.length === 0,
      JSON.stringify(div)
    );
    report(
      'verifyFields: sin tracker queda como no verificable',
      (div.noVerificables || []).length === 2,
      JSON.stringify(div.noVerificables)
    );
  }).catch((e) => {
    console.error('verifyFields (sin tracker) error', e);
    process.exitCode = 1;
  });

  // ==== detectAdapter ==== //
  const leverUrl = 'https://jobs.lever.co/RyzLabs/34d126be-b8fa-4291-8bc4-924031455850/apply';
  const ashbyUrl = 'https://jobs.ashbyhq.com/mural/3493ea21-5b96-4383-964a-996249db3a14/application';
  const eightfoldUrl = 'https://mercadopago.eightfold.ai/careers/apply?pid=44891701';
  report('detectAdapter lever', detectAdapter(leverUrl) === 'lever');
  report('detectAdapter ashby', detectAdapter(ashbyUrl) === 'ashby');
  report('detectAdapter eightfold', detectAdapter(eightfoldUrl) === 'eightfold');
  report('detectAdapter unknown returns null', detectAdapter('https://example.com') === null);

  // ==== DISCOVERY: los bugs que rompieron el radar el 2026-10-25 ==== //

  // El caso testigo del bug de pais: "ar" como substring matcheaba
  // "Arkansas" (Bentonville, Arkansas, Estados Unidos pasaba el filtro de
  // Argentina). Tiene que matchear Argentina, y NO Arkansas.
  report(
    'matchesCountry: Argentina matchea por codigo AR',
    matchesCountry({ location: 'Buenos Aires, Argentina', country: 'Argentina' }, 'AR') === true
  );
  report(
    'matchesCountry: Arkansas NO matchea AR',
    matchesCountry({ location: 'Bentonville, Arkansas, Estados Unidos', country: 'Estados Unidos' }, 'AR') === false
  );
  report(
    'matchesCountry: codigo suelto AR matchea',
    matchesCountry({ location: 'AR', country: 'AR' }, 'AR') === true
  );
  report(
    'matchesCountry: sin ubicacion no se descarta',
    matchesCountry({ location: '', country: '' }, 'AR') === true
  );

  // Una vacante remota "Worldwide" es una oportunidad LATAM, no de otro
  // pais: no puede descartarse por no decir "AR".
  report(
    'isRemoteAnywhere: Worldwide cuenta',
    isRemoteAnywhere({ remote: true, location: 'Worldwide' }) === true
  );
  report(
    'isRemoteAnywhere: una vacante de un pais concreto no cuenta',
    isRemoteAnywhere({ remote: true, location: 'Bentonville, Arkansas, Estados Unidos' }) === false
  );
  report(
    'isRemoteAnywhere: no remota no cuenta',
    isRemoteAnywhere({ remote: false, location: 'Worldwide' }) === false
  );

  // El parser de LinkedIn: la clase del link cambio (base-card__full-link).
  // El fixture tiene el markup ACTUAL; si el sitio vuelve a cambiar, este
  // test falla y avisa.
  const LI_HTML = `
    <ul>
      <li>
        <div class="base-card relative base-search-card job-search-card">
          <a class="base-card__full-link absolute" href="https://ar.linkedin.com/jobs/view/frontend-dev-at-acme-111?x=1">
            <span class="sr-only">
              Frontend Developer React
            </span>
          </a>
          <h3 class="base-search-card__title">Frontend Developer React</h3>
          <h4 class="base-search-card__subtitle">Acme</h4>
          <span class="job-search-card__location">Buenos Aires, Provincia de Buenos Aires, Argentina</span>
        </div>
      </li>
    </ul>`;
  const cards = parseLinkedinCards(LI_HTML);
  report('parseLinkedinCards: encuentra la tarjeta', cards.length === 1);
  report(
    'parseLinkedinCards: extrae el titulo',
    cards[0]?.title === 'Frontend Developer React',
    cards[0]?.title
  );
  report(
    'parseLinkedinCards: extrae la ubicacion',
    /Argentina/.test(cards[0]?.location || ''),
    cards[0]?.location
  );
  report(
    'parseLinkedinCards: el pais sale de la ubicacion (no hardcodeado)',
    cards[0]?.country === 'Argentina',
    cards[0]?.country
  );
  report(
    'parseLinkedinCards: la URL se limpia de los query params',
    cards[0]?.url === 'https://ar.linkedin.com/jobs/view/frontend-dev-at-acme-111',
    cards[0]?.url
  );

  // El markup VIEJO no debe parsear: si el sitio volviera a esa forma, el
  // radar volveria a devolver cero. El test falla visible.
  report(
    'parseLinkedinCards: el markup viejo no devuelve tarjetas (reactivo)',
    parseLinkedinCards('<li><a class="result-card__full-card-link" href="https://x/1"></a></li>').length === 0
  );

  // El filtro: palabra entera, dedupe por URL, y remotas que no son de AR.
  const jobs = [
    { title: 'UX Expert - Software', url: 'https://a/1', location: 'Buenos Aires, Argentina', remote: false },
    { title: 'Withdrawal Local Auxiliar', url: 'https://a/2', location: 'Buenos Aires, Argentina', remote: false },
    { title: 'Frontend Engineer', url: 'https://a/3', location: 'Worldwide', remote: true },
    { title: 'Frontend Engineer', url: 'https://a/3?utm=x', location: 'Worldwide', remote: true },
  ];
  const ux = filterJobs(jobs, { query: 'UX', country: 'AR', remote: false, limit: 10 });
  report(
    'filterJobs: "UX" no matchea "Auxiliar"',
    ux.length === 1 && ux[0].title === 'UX Expert - Software',
    JSON.stringify(ux.map((j) => j.title))
  );
  const fe = filterJobs(jobs, { query: 'frontend', country: 'AR', remote: false, limit: 10 });
  report(
    'filterJobs: una remota Worldwide entra (oportunidad LATAM)',
    fe.length === 1 && fe[0].title === 'Frontend Engineer',
    JSON.stringify(fe.map((j) => j.title))
  );
  report(
    'filterJobs: dedupe por URL ignorando query params',
    fe.length === 1,
    `llegaron ${fe.length}`
  );
  const rem = filterJobs(jobs, { query: 'frontend', country: 'AR', remote: true, limit: 10 });
  report('filterJobs: el filtro --remote excluye las no remotas', rem.length === 1);

  // listOf: los flags repetidos o con coma.
  report('listOf: default cuando no hay valor', listOf(undefined, 'mural')[0] === 'mural');
  report('listOf: separa por coma', listOf('a,b', 'x').length === 2);
  report('listOf: limpia espacios', listOf(' a , b ', 'x')[0] === 'a');
}, 100);

