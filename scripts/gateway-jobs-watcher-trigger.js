// Trigger del job gateway-jobs-watcher (CORREGIDO 2026-09-15).
// Lee `r.aggregated`, no `r.output` (que no existe en exec de code-mode), y
// dispara ante CUALQUIER fallo del check: exit 1 (problemas encontrados) o
// exit 2 (no se pudo chequear). Un watcher que se calla cuando su check falla
// parece sano estando roto.
const r = await exec({
  command:
    'bash /Users/gonzoblasco/.openclaw/workspace/scripts/gateway-jobs-check.sh 2>&1; echo __EXIT__:$?',
});
const m = (r.aggregated || '').match(/__EXIT__:(\d+)/);
const out = (r.aggregated || '').replace(/__EXIT__:\d+/, '').trim();
const exitCode = m ? parseInt(m[1], 10) : (typeof r.exitCode === 'number' ? r.exitCode : -1);

if (exitCode === 1 || exitCode === 2) {
  return json({
    fire: true,
    message: out || ('gateway-jobs-check.sh fallo con exit ' + exitCode),
    state: { lastCheck: new Date().toISOString(), lastResult: 'problems' },
  });
}
return json({
  fire: false,
  state: { lastCheck: new Date().toISOString(), lastResult: exitCode === 0 ? 'ok' : 'error-' + exitCode },
});
