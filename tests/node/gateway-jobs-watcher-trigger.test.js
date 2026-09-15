// Harness del trigger corregido de gateway-jobs-watcher.
// Verifica que dispare ante exit 1 y exit 2, y quede quieto en exit 0.
const fs = require('node:fs');
const path = require('node:path');
const src = fs.readFileSync(
  path.join(__dirname, '..', '..', 'scripts', 'gateway-jobs-watcher-trigger.js'),
  'utf8',
);

let pass = 0;
let fail = 0;

async function run(label, aggregated, expectFire) {
  const exec = async () => ({ aggregated, exitCode: 0 });
  const json = (o) => ({ __json: true, ...o });
  const trigger = { state: null };
  const fn = new Function('exec', 'json', 'trigger', 'return (async () => {' + src + '})()');
  const res = await fn(exec, json, trigger);
  const ok = res.fire === expectFire;
  if (ok) pass++; else fail++;
  console.log(`${ok ? 'PASS' : 'FAIL'} [${res.fire ? 'FIRE ' : 'quiet'}] ${label}`);
  if (res.message) console.log('        msg: ' + res.message.slice(0, 120));
}

(async () => {
  await run('exit 0: todo sano -> quiet', 'OK: all gateway jobs healthy\n__EXIT__:0', false);
  await run('exit 1: problemas encontrados -> FIRE', 'PROBLEMS in gateway jobs (2)\n__EXIT__:1', true);
  await run('exit 2: no se pudo chequear -> FIRE (no quedar mudo)', 'ERROR: could not get automations\n__EXIT__:2', true);
  console.log(`\n=== ${pass} PASS / ${fail} FAIL ===`);
  process.exit(fail === 0 ? 0 : 1);
})();
