// Trigger del watcher de FIN DE LA FASE CLOUD (2026-10-28).
//
// Por que una automatizacion y no un proceso encadenado (nohup &): un proceso
// colgado muere cuando el exec que lo lanzo termina. La automatizacion
// persiste en el gateway y este trigger corre cada 5 minutos.
//
// Cuando dispara, el payload arranca la fase local: 4 modelos locales
// (nova-2b, ornith-1.5:9b, gemma4:12b-mlx, qwen3.5:9b-mlx) x 3 harnesses x
// 1 TAREA (decision de Gonzo: los locales son GGUF en CPU y tardan 10-20 min
// por celda; con 3 tareas serian 6-8 horas).
const r = await exec({
  command:
    'bash /Users/gonzoblasco/.openclaw/workspace/scripts/watch-cloud-fin.sh 2>&1; echo __EXIT__:$?',
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
    message:
      payload.message || 'La fase cloud de la cata termino: hay que arrancar la fase local.',
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
