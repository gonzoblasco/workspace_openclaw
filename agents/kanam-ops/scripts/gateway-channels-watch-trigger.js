// Trigger del job gateway-channels-watchdog (E3.1).
// Dispara ante exit 1 (canal caido) o exit 2 (no se pudo medir).
// El 2 incluido a proposito: un watchdog que se calla cuando su propio check
// falla parece sano estando roto. Es el bug que tuvo jobs-watcher el 2026-09-15.
//
// Forma real del retorno de exec: el campo de texto es `aggregated`, NO `output`.
const r = await exec({
  command:
    'bash /Users/gonzoblasco/.openclaw/workspace/agents/kanam-ops/scripts/gateway-channels-watch.sh 2>&1; echo __EXIT__:$?',
});

const raw = r.aggregated || '';
const m = raw.match(/__EXIT__:(\d+)/);
const out = raw.replace(/__EXIT__:\d+/, '').trim();
const exitCode = m ? parseInt(m[1], 10) : (typeof r.exitCode === 'number' ? r.exitCode : -1);

// Dedupe: no repetir la misma alerta mientras el estado no cambie. Un canal
// caido por horas no debe mandar un mensaje cada 5 minutos.
const prev = (trigger && trigger.state) || {};
const key = out || 'empty';

if (exitCode === 0) {
  return json({
    fire: false,
    state: { last: 'ok', key: 'ok', lastCheck: new Date().toISOString() },
  });
}

if (prev.last === 'fired' && prev.key === key) {
  return json({
    fire: false,
    state: { last: 'fired', key, lastCheck: new Date().toISOString(), suppressed: (prev.suppressed || 0) + 1 },
  });
}

const why = exitCode === 2 ? 'NO SE PUDO MEDIR' : 'CANAL CAIDO';
return json({
  fire: true,
  message:
    'ALERTA de canales: ' + why + ' (exit ' + exitCode + ')\n\n' + (out || '(sin detalle)') +
    '\n\nDiagnostico sugerido: openclaw channels status',
  state: { last: 'fired', key, lastCheck: new Date().toISOString(), suppressed: 0 },
});
