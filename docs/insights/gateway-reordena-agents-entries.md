# Hallazgo: el gateway reescribe `agents.entries` en orden alfabetico, sin actor de agente

**Fecha:** 2026-09-29
**Origen:** investigacion del registro de plugins `stale` (ADR-081)
**Estado:** observado y verificado; candidato a reporte upstream
**Superficie:** escritura de config del gateway (`logs/config-audit.jsonl`)

---

## Que se observo

El gateway **reescribe `~/.openclaw/openclaw.json` por su cuenta**, sin que ningun agente ni comando lo pida, y en esa reescritura **el orden de las claves de `agents.entries` pasa a ser alfabetico**.

En este setup el roster tenia `main` primero (orden elegido a proposito). Despues de una reescritura del gateway quedo:

```
kanam-dev, kanam-mind, kanam-ops, kanam-studio, main
```

Es decir: `main` (el `systemAgent`) **se mueve al final**, y el orden queda lexicografico.

## Evidencia

**1. Eventos `config.write` sin actor de agente.** `logs/config-audit.jsonl` registra seis escrituras consecutivas en ~3 minutos, todas `result: success`, `nextUid: 501` (el usuario), **sin campo de actor**:

```
2026-09-28T23:26:59Z  bytes 31453->31615  suspicious=[]
2026-09-28T23:27:46Z  bytes 31615->31614  suspicious=[]
2026-09-28T23:28:34Z  bytes 31614->31615  suspicious=[]
2026-09-28T23:29:12Z  bytes 31615->31614  suspicious=[]
2026-09-28T23:30:18Z  bytes 31614->31431  suspicious=['gateway-mode-removed']
2026-09-28T23:30:20Z  bytes 31431->31453  suspicious=[]
```

Ninguna coincide con una accion de agente: los `audit_events` de la DB de estado **se cortan a las 22:02**, y a las 23:01 ya estaba el orden cambiado. El unico `config.write` con marca sospechosa (`gateway-mode-removed`) es del 23:30:18.

**2. El orden cambia entre backups consecutivos.**

| Backup | Orden de `agents.entries` |
|---|---|
| 2026-09-28 17:00 | `main`, `kanam-dev`, `kanam-mind`, `kanam-ops`, `kanam-studio` |
| 2026-09-28 23:01 | `kanam-dev`, `kanam-mind`, `kanam-ops`, `kanam-studio`, `main` (**alfabetico**) |

**3. El efecto secundario es medible.** El indice persistido de plugins (`config_machine_state.plugins.installedIndex` → `index.workspaceDir`) pasa a apuntar al subtree del primer entry, y el registro queda `stale`:

```
state: stale | refreshReasons: ['source-changed'] | differences: 0
persisted: /Users/gonzoblasco/.openclaw/workspace/agents/kanam-dev
current  : /Users/gonzoblasco/.openclaw/workspace
```

## Por que importa

- **Cualquier decision que dependa del orden del roster es fragile.** Si una herramienta, un script o una persona ordena `agents.entries` con un criterio (por ejemplo "el owner del control-plane primero"), el gateway lo revierte en la proxima escritura. Lo verificado: **el orden no es una eleccion persistente**.
- **El reordenamiento tiene consecuencia funcional**, no solo cosmetica: el scope persistido del registro de plugins sigue al primer entry, y eso deja el registro `stale`.
- **No hay rastro de quien lo pidio.** Las escrituras no llevan actor de agente, lo que dificulta atribuir el cambio a una accion concreta.

## Que NO se afirma

- **No se afirma que el `stale` cause fallos de automatizacion.** Medido: con el orden roto y el registro `stale`, los tres jobs vigilados hicieron **0 errores en 31 corridas**. El flag y el fallo son independientes (retractacion completa en `docs/adr/ADR-081-scope-plugins-orden-entries.md`).
- **No se afirma la ruta exacta de codigo** que produce la reescritura. Solo el hecho, su evidencia y su efecto.

## Nota de metodo

Este hallazgo salio de perseguir un sintoma (registro `stale`) y encontrar, de paso, una causa distinta y mas general (el gateway normaliza el orden del roster). Vale registrarlo por separado del ADR-081, cuyo eje era el fallo de los triggers: **son dos cosas distintas**, y mezclarlas fue justamente el error que el ADR-081 tuvo que retractar.
