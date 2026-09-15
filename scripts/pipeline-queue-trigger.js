// Trigger READ-ONLY del job "pipeline-queue-watcher".
// Detecta trabajo detenido en la cola durable del pipeline A/B.
// No muta nada: la recuperacion (tick) vive en el payload.
//
// Forma real del retorno de exec (verificada 2026-09-15 con un probe):
//   { status, exitCode, exitSignal, exitReason, durationMs, aggregated, noOutputTimedOut, cwd }
// OJO: NO existe `output`. El campo de texto es `aggregated`.
//
// Diseno de señales (por que no dispara con "queued y nada running"):
// la cola hoy NO es el driver de ejecucion (el pipeline A/B corre por
// sessions_spawn, y `running` solo se setea si alguien llama `claim`).
// Por eso un "stall" de un solo check es normal, no una falla. Solo se
// alerta si el MISMO conjunto de unidades lleva 2 checks consecutivos
// detenido. Las huerfanas y el estado ilegible si son señales duras.
const W = '/Users/gonzoblasco/.openclaw/workspace';

const cmd = [
  'cd ' + W,
  'o=$(bash scripts/pipeline-queue.sh orphans 2>&1); orc=$?',
  "s=$(jq -c '.units // [] | map({n:.name,s:.state,a:(.attempts//0)})' pipeline-state.json 2>&1); src=$?",
  "printf 'ORPH<<%s>>|%s\\nSTATE<<%s>>|%s\\n' \"$o\" \"$orc\" \"$s\" \"$src\"",
].join('; ');

const r = await exec({ command: cmd });
const out = String(r.aggregated || '');
const execRc = typeof r.exitCode === 'number' ? r.exitCode : -1;

function grab(tag) {
  const m = out.match(new RegExp(tag + '<<([\\s\\S]*?)>>\\|(\\d+)'));
  return m ? { text: m[1].trim(), rc: parseInt(m[2], 10) } : { text: '', rc: -1 };
}

const orph = grab('ORPH');
const st = grab('STATE');

let units = [];
let parseError = false;
try {
  const parsed = JSON.parse(st.text);
  if (Array.isArray(parsed)) {
    units = parsed;
  } else {
    // Un plan sin `units` array es estado roto, no una cola vacia:
    // tratarlo como vacio dejaria al watcher mudo ante un archivo malformado.
    parseError = true;
  }
} catch (e) {
  parseError = true;
}

// rc 2 en orphans = estado corrupto (require_valid_state aborta asi).
const stateBroken = parseError || orph.rc === 2 || st.rc !== 0 || execRc !== 0 ||
  /^Estado corrupto|^Error:/.test(orph.text);

const orphans = stateBroken
  ? []
  : orph.text
      ? orph.text.split('\n').map((s) => s.trim()).filter(Boolean)
      : [];

const queued = units.filter((u) => u.s === 'queued').map((u) => u.n);
const running = units.filter((u) => u.s === 'running').map((u) => u.n);
const failed = units.filter((u) => u.s === 'failed').map((u) => u.n);

// Dedupe por NOMBRES de unidades: estable frente al tick (running -> queued
// no cambia el conjunto), asi que la recuperacion automatica no re-dispara
// en loop. Vuelve a disparar al pasar de no-accionable a accionable.
const key = units.map((u) => u.n).sort().join(',');
const prev = (trigger && trigger.state) || {};
const now = new Date().toISOString();

const stalled = queued.length > 0 && running.length === 0;
const sameKey = prev.key === key;
const stallCount = stalled ? (sameKey ? (prev.stallCount || 0) + 1 : 1) : 0;
const persistentStall = stallCount >= 2;

const actionable = orphans.length > 0 || persistentStall;

if (stateBroken) {
  // Un watcher que se calla cuando su check falla parece sano estando roto.
  if (prev.last === 'broken' && sameKey) {
    return json({
      fire: false,
      state: { key, actionable: true, last: 'broken', lastCheck: now, stallCount },
    });
  }
  return json({
    fire: true,
    message:
      'ERROR: no se pudo leer el estado de la cola del pipeline.\n' +
      'orphans: ' + (orph.text || '(vacio)').slice(0, 300) + '\n' +
      'jq: ' + (st.text || '(vacio)').slice(0, 300) + '\n' +
      'exit codes: exec=' + execRc + ' orphans=' + orph.rc + ' jq=' + st.rc,
    state: { key, actionable: true, last: 'broken', lastCheck: now, stallCount },
  });
}

if (!actionable) {
  return json({
    fire: false,
    state: { key, actionable: false, last: 'idle', lastCheck: now, stallCount },
  });
}

if (prev.actionable === true && sameKey) {
  return json({
    fire: false,
    state: { key, actionable: true, last: 'dedup', lastCheck: now, stallCount },
  });
}

const lines = [];
if (orphans.length) lines.push('Unidades huerfanas (proceso muerto): ' + orphans.join(', '));
if (persistentStall) {
  lines.push(
    'Cola detenida ' + stallCount + ' checks seguidos: pendientes sin nada corriendo -> ' +
      queued.join(', '),
  );
}
lines.push('Estado: queued=' + queued.length + ' running=' + running.length + ' failed=' + failed.length);
if (failed.length) lines.push('En failed (terminal, no bloquea el resto): ' + failed.join(', '));

return json({
  fire: true,
  message: lines.join('\n'),
  state: { key, actionable: true, last: 'fired', lastCheck: now, stallCount },
});
