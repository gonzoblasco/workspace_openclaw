// Trigger del watcher de FIN de la cata de harnesses (2026-10-28).
//
// Por que existe: el driver corre en background y su salida va a un log
// bufferizado, asi que el owner no ve progreso ni se entera del final sin
// preguntar. Este watcher mira el ESTADO (artefactos + suite.json), no el log.
//
// Dispara UNA vez por tanda: el script escribe el sello CATA-DONE al terminar,
// y el trigger solo dispara si el sello no existe todavia.
const r = await exec({
  command:
    'bash /Users/gonzoblasco/.openclaw/workspace/scripts/watch-cata-fin.sh 2>&1; echo __EXIT__:$?',
});
const out = (r.aggregated || '').replace(/__EXIT__:\d+/, '').trim();

let payload = {};
try {
  payload = JSON.parse(out);
} catch (e) {
  return json({
    fire: false,
    state: { lastCheck: new Date().toISOString(), lastResult: 'no-json' },
  });
}

if (payload.fire) {
  return json({
    fire: true,
    message: payload.message || 'La tanda de la cata de harnesses termino.',
    state: { lastCheck: new Date().toISOString(), lastResult: 'fired' },
  });
}

return json({
  fire: false,
  state: {
    lastCheck: new Date().toISOString(),
    lastResult: payload.reason || 'sin accion',
  },
});
