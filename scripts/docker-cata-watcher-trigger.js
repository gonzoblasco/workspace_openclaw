// Trigger del watcher de Docker para la cata de harnesses (2026-10-28).
//
// POR QUE EXISTE: la VM de Docker reserva 7,7 GB de los 24 GB del host como
// memoria WIRED. Con Docker abierto quedan 0,14 GB libres; con Docker cerrado,
// 8,32 GB. Los runners MLX de Ollama expiran solos a los 5 minutos: lo que NO
// expira nunca es la VM de Docker. Gonzo lo pidio explicitamente: "lo que
// debemos saber es que hay que cerrarlo luego, me lo recuerdas?".
//
// El trigger es CONDICIONAL y NO consume modelo en silencio: solo dispara si la
// cata YA TERMINO y Docker SIGUE ABIERTO. Si la cata sigue en curso, o si
// Docker ya esta cerrado, devuelve fire:false.
const r = await exec({
  command:
    'bash /Users/gonzoblasco/.openclaw/workspace/scripts/watch-docker-cata.sh 2>&1; echo __EXIT__:$?',
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
      payload.message ||
      'La cata de harnesses termino y Docker Desktop sigue abierto.',
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
