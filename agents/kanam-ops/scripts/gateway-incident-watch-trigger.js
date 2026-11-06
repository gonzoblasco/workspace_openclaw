// Trigger del job gateway-incident-postmortem (E3.4).
// Dispara cuando hay un reporte de estabilidad NUEVO desde la ultima revision.
//
// Por que "nuevo" y no "hay incidentes": el directorio es historico. Si se
// dispara por presencia, avisa para siempre por el mismo evento viejo y la
// alerta se vuelve ruido que se ignora.
const DIR = '/Users/gonzoblasco/.openclaw/logs/stability';

const r = await exec({
  command:
    'ls -1 ' + DIR + '/*.json 2>/dev/null | wc -l; ' +
    'ls -1t ' + DIR + '/*.json 2>/dev/null | head -1',
});

const raw = r.aggregated || '';
const lines = raw.split('\n').map((s) => s.trim()).filter(Boolean);
const count = parseInt(lines[0] || '0', 10);
const newest = lines[1] || '';

const prev = (trigger && trigger.state) || {};

// Primer arranque: se guarda la linea base sin avisar. Avisar por todo el
// historico en el primer tick entrena a ignorar la alerta para siempre.
if (typeof prev.count !== 'number') {
  return json({
    fire: false,
    state: { count, newest, lastCheck: new Date().toISOString(), baselined: true },
  });
}

if (count <= prev.count) {
  return json({
    fire: false,
    state: { count, newest: prev.newest, lastCheck: new Date().toISOString(), baselined: true },
  });
}

const nuevos = count - prev.count;
const pm = await exec({
  command:
    'bash /Users/gonzoblasco/.openclaw/workspace/agents/kanam-ops/scripts/gateway-postmortem.sh --since 1d 2>&1',
});

return json({
  fire: true,
  message:
    'INCIDENTE NUEVO del gateway: ' + nuevos + ' reporte(s). Ultimo: ' + newest + '\n\n' +
    (pm.aggregated || '(no se pudo generar el post-mortem)'),
  state: { count, newest, lastCheck: new Date().toISOString(), baselined: true },
});
