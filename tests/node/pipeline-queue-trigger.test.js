// Harness del trigger con la logica de stallCount.
// Forma REAL del exec: aggregated + exitCode.
const fs = require('node:fs');
const path = require('node:path');
const src = fs.readFileSync(
  path.join(__dirname, '..', '..', 'scripts', 'pipeline-queue-trigger.js'),
  'utf8',
);

let pass = 0;
let fail = 0;

async function run(name, { orphanOut, orphanRc, stateJson, stateRc, prevState, execCode = 0, missing = 0 }, expectFire) {
  const exec = async () => ({
    status: 'completed',
    exitCode: execCode,
    aggregated:
      'ORPH<<' + orphanOut + '>>|' + orphanRc + '\n' +
      'STATE<<' + stateJson + '>>|' + stateRc + '\n' +
      'MISSING<<' + missing + '>>\n',
    cwd: '/x',
  });
  const json = (o) => ({ __json: true, ...o });
  const trigger = { state: prevState };
  const fn = new Function('exec', 'json', 'trigger', 'return (async () => {' + src + '})()');
  const res = await fn(exec, json, trigger);

  const ok = res.fire === expectFire;
  if (ok) pass++; else fail++;
  console.log(`${ok ? 'PASS' : 'FAIL'} [${res.fire ? 'FIRE ' : 'quiet'}] ${name}${ok ? '' : ' (esperado fire=' + expectFire + ')'}`);
  if (res.message) console.log('        ' + res.message.split('\n').join('\n        '));
  console.log('        state: ' + JSON.stringify(res.state) + '\n');
  return res;
}

(async () => {
  const queued1 = JSON.stringify([{ n: 'U1', s: 'queued', a: 0 }]);
  const working = JSON.stringify([{ n: 'U1', s: 'running', a: 1 }, { n: 'U2', s: 'queued', a: 0 }]);
  const orphanState = JSON.stringify([{ n: 'U1', s: 'running', a: 1 }, { n: 'U2', s: 'queued', a: 0 }]);

  await run('1. idle: sin unidades', { orphanOut: '', orphanRc: 0, stateJson: '[]', stateRc: 0, prevState: null }, false);
  await run('2. cola detenida 1er check -> quiet (stallCount=1)', { orphanOut: '', orphanRc: 0, stateJson: queued1, stateRc: 0, prevState: null }, false);
  await run('3. cola detenida 2do check -> FIRE', { orphanOut: '', orphanRc: 0, stateJson: queued1, stateRc: 0, prevState: { key: 'U1', actionable: false, stallCount: 1 } }, true);
  await run('4. detenida 3er check -> quiet (dedupe)', { orphanOut: '', orphanRc: 0, stateJson: queued1, stateRc: 0, prevState: { key: 'U1', actionable: true, stallCount: 2 } }, false);
  await run('5. trabajando (queued + running) -> quiet, contador a 0', { orphanOut: '', orphanRc: 0, stateJson: working, stateRc: 0, prevState: { key: 'U1', actionable: false, stallCount: 1 } }, false);
  await run('6. huerfana -> FIRE inmediato (señal dura)', { orphanOut: 'U1', orphanRc: 0, stateJson: orphanState, stateRc: 0, prevState: null }, true);
  await run('7. huerfana repetida misma key -> quiet (dedupe)', { orphanOut: 'U1', orphanRc: 0, stateJson: orphanState, stateRc: 0, prevState: { key: 'U1,U2', actionable: true, stallCount: 0 } }, false);
  await run('8. post-tick: reencolada, key igual -> quiet (sin loop)', { orphanOut: '', orphanRc: 0, stateJson: JSON.stringify([{ n: 'U1', s: 'queued', a: 1 }]), stateRc: 0, prevState: { key: 'U1', actionable: true, stallCount: 2 } }, false);
  await run('9. estado corrupto (rc=2) -> FIRE con error, NO como unidad', { orphanOut: 'Estado corrupto: no es JSON valido. Abortando.', orphanRc: 2, stateJson: 'jq: error', stateRc: 5, prevState: null }, true);
  await run('10. corrupto repetido -> quiet', { orphanOut: 'Estado corrupto: x', orphanRc: 2, stateJson: 'jq: error', stateRc: 5, prevState: { key: '', actionable: true, last: 'broken', stallCount: 0 } }, false);
  await run('11. todo done -> quiet', { orphanOut: '', orphanRc: 0, stateJson: JSON.stringify([{ n: 'U1', s: 'done', a: 1 }]), stateRc: 0, prevState: null }, false);
  await run('12. exec falla (exitCode 1) -> FIRE con error', { orphanOut: '', orphanRc: 0, stateJson: '[]', stateRc: 0, prevState: null, execCode: 1 }, true);
  await run('13. JSON no-array -> roto, FIRE', { orphanOut: '', orphanRc: 0, stateJson: '{"fase":"x"}', stateRc: 0, prevState: null }, true);
  await run('14. failed presente, cola detenida 1er check -> quiet', { orphanOut: '', orphanRc: 0, stateJson: JSON.stringify([{ n: 'U1', s: 'failed', a: 3 }, { n: 'U2', s: 'queued', a: 0 }]), stateRc: 0, prevState: null }, false);
  await run('15. failed + detenida 2do check -> FIRE y lista failed', { orphanOut: '', orphanRc: 0, stateJson: JSON.stringify([{ n: 'U1', s: 'failed', a: 3 }, { n: 'U2', s: 'queued', a: 0 }]), stateRc: 0, prevState: { key: 'U1,U2', actionable: false, stallCount: 1 } }, true);

  // Regresion 2026-11-02: pipeline-state.json ausente (se limpia al cerrar la
  // fase) se leia como estado roto y el watcher gritaba en falso cada 15m.
  await run('16. archivo ausente -> quiet (cola vacia, NO error)', { orphanOut: '', orphanRc: 0, stateJson: '[]', stateRc: 0, prevState: null, missing: 1 }, false);
  await run('17. ausente y luego aparece cola detenida -> quiet 1er check', { orphanOut: '', orphanRc: 0, stateJson: queued1, stateRc: 0, prevState: { key: '', actionable: false, last: 'idle', stallCount: 0 }, missing: 0 }, false);
  await run('18. ausente con prev broken -> quiet (sale del modo roto)', { orphanOut: '', orphanRc: 0, stateJson: '[]', stateRc: 0, prevState: { key: '', actionable: true, last: 'broken', stallCount: 0 }, missing: 1 }, false);
  await run('19. presente pero ilegible -> FIRE (corrupcion real)', { orphanOut: '', orphanRc: 0, stateJson: 'jq: error: Could not open file', stateRc: 2, prevState: null, missing: 0 }, true);

  console.log(`\n=== ${pass} PASS / ${fail} FAIL (de ${pass + fail}) ===`);
  process.exit(fail === 0 ? 0 : 1);
})();
