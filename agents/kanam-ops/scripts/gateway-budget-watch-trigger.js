// Trigger del job gateway-budget-watchdog (E3.2).
// Dispara ante exit 1 (umbral cruzado) o exit 2 (no se pudo medir).
//
// El check es read-only: avisa, no borra. Los .bak de migracion son respaldos
// reales; borrarlos es decision humana, no de un watchdog nocturno.
const r = await exec({
  command:
    'bash /Users/gonzoblasco/.openclaw/workspace/agents/kanam-ops/scripts/gateway-budget-watch.sh 2>&1; echo __EXIT__:$?',
});

const raw = r.aggregated || '';
const m = raw.match(/__EXIT__:(\d+)/);
const out = raw.replace(/__EXIT__:\d+/, '').trim();
const exitCode = m ? parseInt(m[1], 10) : (typeof r.exitCode === 'number' ? r.exitCode : -1);

// Dedupe: el disco que crecio no vuelve a achicarse solo. Alertar cada hora
// con el mismo numero entrena a ignorar la alerta. Se avisa cuando aparece
// el problema y se vuelve a avisar solo si el texto cambia (crecio mas).
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

const why = exitCode === 2 ? 'NO SE PUDO MEDIR' : 'PRESUPUESTO DE DISCO';
return json({
  fire: true,
  message:
    'ALERTA de presupuesto: ' + why + ' (exit ' + exitCode + ')\n\n' + (out || '(sin detalle)') +
    '\n\nEsto es informativo: ningun borrado es automatico. Revisar con Gonzo antes de tocar los .bak.',
  state: { last: 'fired', key, lastCheck: new Date().toISOString(), suppressed: 0 },
});
