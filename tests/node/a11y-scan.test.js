// Tests del clasificador de scripts/a11y-scan.mjs.
//
// Por que existen: el gate mide accesibilidad real con axe-core, pero su JUICIO
// (que violacion bloquea) es una funcion pura. Probamos esa funcion sin browser
// ni red, y - lo que importa - probamos que PUEDE FALLAR. Un check que no puede
// fallar no verifica nada (leccion de check-contrast.py).
//
// El resto del pipeline (playwright + axe) se verifico a mano end-to-end: un
// test que levante un browser no corre en CI (no hay playwright instalado) y
// seria un verde por skip. El clasificador es lo unico que decide el exit code.
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { classify, summarize, IMPACT_ORDER } = require(
  path.join(__dirname, '..', '..', 'scripts', 'a11y-scan.mjs'),
);

let pass = 0;
let fail = 0;
function check(name, cond, detail) {
  if (cond) {
    pass++;
    console.log(`ok ${pass + fail} ${name}`);
  } else {
    fail++;
    console.log(`FAIL ${pass + fail} ${name}${detail ? ' -- ' + detail : ''}`);
  }
}

const v = (id, impact) => ({ id, impact, help: id, nodes: [{}] });

// --- el caso limpio no inventa violaciones ---

check('sin violaciones -> gate vacio', classify([], 'serious').gate.length === 0);

// --- el umbral decide, no el nombre ---

{
  const r = classify([v('a', 'critical'), v('b', 'serious'), v('c', 'moderate'), v('d', 'minor')], 'serious');
  check('serious+critical bloquean', r.gate.map((x) => x.id).join(',') === 'a,b');
  check('moderate/minor quedan informativas', r.info.map((x) => x.id).join(',') === 'c,d');
}

{
  const r = classify([v('a', 'critical'), v('b', 'serious'), v('c', 'moderate')], 'moderate');
  check('umbral moderate incluye moderate', r.gate.map((x) => x.id).join(',') === 'a,b,c');
}

// --- no se descarta en silencio lo desconocido ---

{
  const r = classify([v('x', undefined), v('y', null), v('z', 'bogus')], 'serious');
  check('impacto desconocido/nulo trata como peor caso (bloquea)', r.gate.length === 3, `gate=${r.gate.length}`);
}

// --- un umbral invalido no pasa como verde ---

{
  let threw = false;
  try {
    classify([], 'nope');
  } catch {
    threw = true;
  }
  check('umbral invalido lanza (no hay verde silencioso)', threw);
}

// --- summarize cuenta nodos ---

{
  const s = summarize([{ id: 'a', impact: 'serious', help: 'h', nodes: [{}, {}] }]);
  check('summarize cuenta nodos', s[0].nodes === 2 && s[0].id === 'a');
}

// --- el orden de severidad es el documentado ---

check('IMPACT_ORDER correcto', IMPACT_ORDER.join(',') === 'minor,moderate,serious,critical');

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
