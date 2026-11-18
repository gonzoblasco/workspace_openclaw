// Trigger del job gateway-channels-watchdog (E3.1, v2 2026-11-18).
//
// CAMBIO IMPORTANTE respecto de la v1:
// La v1 corria `gateway-channels-watch.sh` dentro del trigger. Ese script llama
// a `openclaw channels status --json`, que arranca un Node completo. Dentro del
// code-mode del trigger se encola detras de otros procesos: 1.8s a mano,
// 50-80s ahi, contra un presupuesto de ~30s. Resultado: timeout en rafaga, con
// corridas de 49 a 83 segundos, y el job muriendo justo cuando tenia que medir.
//
// La v2 solo LEE un archivo que otro proceso refresca. Leer un archivo no
// depende de la carga del gateway ni del sandbox.
//
// Si el cache esta viejo, eso TAMBIEN dispara: un watchdog que confia en un
// dato de hace horas y dice "todo bien" es peor que uno que avisa que no puede
// medir.

const CACHE = '/Users/gonzoblasco/.openclaw/gateway-channels-state.json';
const STALE_MS = 30 * 60 * 1000; // 30 min: el refresh corre cada 20

const r = await exec({ command: 'cat ' + CACHE + ' 2>&1; echo __EXIT__:$?' });

const raw = r.aggregated || '';
const m = raw.match(/__EXIT__:(\d+)/);
const body = raw.replace(/__EXIT__:\d+/, '').trim();
const readRc = m ? parseInt(m[1], 10) : -1;

const prev = (trigger && trigger.state) || {};

// Sin cache legible no se puede afirmar que los canales esten sanos.
if (readRc !== 0 || !body) {
  const key = 'sin-cache';
  if (prev.last === 'fired' && prev.key === key) {
    return json({ fire: false, state: { last: 'fired', key, lastCheck: new Date().toISOString() } });
  }
  return json({
    fire: true,
    message:
      'ALERTA de canales: NO SE PUEDE MEDIR.\n\n' +
      'No se pudo leer el cache de estado (' + CACHE + ', exit ' + readRc + ').\n' +
      'El refresh de canales no esta corriendo o murio.',
    state: { last: 'fired', key, lastCheck: new Date().toISOString() },
  });
}

let data;
try {
  data = JSON.parse(body);
} catch (e) {
  return json({
    fire: true,
    message: 'ALERTA de canales: el cache no es JSON valido.\n\n' + body.slice(0, 300),
    state: { last: 'fired', key: 'json-roto', lastCheck: new Date().toISOString() },
  });
}

const ts = Date.parse(data.ts || '');
const ageMs = Number.isFinite(ts) ? Date.now() - ts : Infinity;
const stale = ageMs > STALE_MS;

// Canal caido reportado por la medicion.
if (data.healthy === false) {
  const key = 'unhealthy';
  if (prev.last === 'fired' && prev.key === key) {
    return json({ fire: false, state: { last: 'fired', key, lastCheck: new Date().toISOString(), suppressed: (prev.suppressed || 0) + 1 } });
  }
  return json({
    fire: true,
    message:
      'ALERTA de canales: CANAL CAIDO (medido ' + data.ts + ')\n\n' +
      (data.detail || '(sin detalle)') +
      '\n\nDiagnostico sugerido: openclaw channels status',
    state: { last: 'fired', key, lastCheck: new Date().toISOString(), suppressed: 0 },
  });
}

// Sano pero el dato es viejo: se avisa, no se asume sano.
if (stale) {
  const key = 'stale';
  if (prev.last === 'fired' && prev.key === key) {
    return json({ fire: false, state: { last: 'fired', key, lastCheck: new Date().toISOString(), suppressed: (prev.suppressed || 0) + 1 } });
  }
  const mins = Number.isFinite(ageMs) ? Math.round(ageMs / 60000) : '?';
  return json({
    fire: true,
    message:
      'ALERTA de canales: DATO VIEJO.\n\n' +
      'El ultimo estado medido es de ' + data.ts + ' (' + mins + ' minutos).\n' +
      'El refresh de canales dejo de correr. No puedo afirmar que los canales esten sanos.',
    state: { last: 'fired', key, lastCheck: new Date().toISOString(), suppressed: 0 },
  });
}

return json({
  fire: false,
  state: { last: 'ok', key: 'ok', lastCheck: new Date().toISOString() },
});
