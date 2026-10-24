// job-application.test.js – Tests para las funciones puras del skill
//
// POR QUÉ EXISTE (2026-10-23): validar que los utilities de `react-form.mjs`
// y la detección de ATS funcionan sin necesidad de lanzar un browser.

const path = require('node:path');
// Helpers para cargar módulos ESM desde CommonJS test runner.
async function importMjs(rel) {
  // __dirname está disponible en CommonJS.
  const modPath = path.resolve(__dirname, '..', '..', rel);
  return await import(modPath);
}

let reactValue, verifyFields, detectAdapter;

(async () => {
  const { reactValue: rv, verifyFields: vf } = await importMjs('skills/job-application/scripts/lib/react-form.mjs');
  reactValue = rv;
  verifyFields = vf;
  const { detectAdapter: da } = await importMjs('skills/job-application/scripts/lib/ats.mjs');
  detectAdapter = da;
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

  // ==== detectAdapter ==== //
  const leverUrl = 'https://jobs.lever.co/RyzLabs/34d126be-b8fa-4291-8bc4-924031455850/apply';
  const ashbyUrl = 'https://jobs.ashbyhq.com/mural/3493ea21-5b96-4383-964a-996249db3a14/application';
  const eightfoldUrl = 'https://mercadopago.eightfold.ai/careers/apply?pid=44891701';
  report('detectAdapter lever', detectAdapter(leverUrl) === 'lever');
  report('detectAdapter ashby', detectAdapter(ashbyUrl) === 'ashby');
  report('detectAdapter eightfold', detectAdapter(eightfoldUrl) === 'eightfold');
  report('detectAdapter unknown returns null', detectAdapter('https://example.com') === null);
}, 100);

