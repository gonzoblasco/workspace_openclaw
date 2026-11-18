# ADR-113: Biblioteca de scripts - propuesta rechazada en su forma actual

**Status:** Rejected (2026-11-18)
**Deciders:** Kanam (CORE), pendiente de Gonzo
**Origen:** auditoria de la skill `growing-doc-retention` y de la tabla de scripts de `docs/SETUP.md`

## Contexto
`docs/SETUP.md` documenta ~30 scripts; `scripts/` tiene 147 entradas (142 scripts). La tabla no está desfasada (cero filas apuntan a archivos inexistentes) pero está **incompleta y mezcla catálogo vivo con actas de defunción**. Tres de sus filas ya son deuda explícita (`init-project.sh`, `aggregate-sync.sh`, `initial-setup.sh`).

## Lo que se propuso y no se pudo sostener
Convertir la tabla en un bloque managed generado desde `memory.db`, con gate en el pre-commit.

## Por que se rechaza en su forma actual
1. **El patrón managed no soporta contenido arbitrario.** Los bloques no se definen en la DB: se definen hardcodeados en la lista `BLOCKS` de `scripts/managed-blocks.py` (líneas 118-174), y la DB solo provee *variables* que se interpolan en un `template` fijo. Guardar una tabla entera como valor de un setting (`scripts_inventory`) no produce ningún bloque: `apply` reporta "al día" y no escribe nada. Verificado 2026-11-18.
2. **El gate resultante era decorativo.** `scripts-inventory.py --check` delega en `managed-blocks.py apply` global; como la clave no está bindeada a ningún archivo, reporta drift permanente (exit 1) y abortaría *cualquier* commit con `docs/SETUP.md` staged, sin arreglar nada.

## Lo que sí quedó verificado y sirve
- **Inventario completo y medido:** 142 scripts, cada uno con su conteo de referencias reales (`tmp/scripts_inventory_raw.json`). Distribución: 9 con 0 referencias, 18 con 1, 52 con 2-4, 63 con 5+.
- **9 huérfanos con cero referencias:** `cata-fin-watcher-trigger.js`, `cata-local-state.py`, `cloud-fin-watcher-trigger.js`, `docker-cata-watcher-trigger.js`, `heartbeat-snapshot.sh`, `migrate-content.py`, `model-compare-qwen-gemma.sh`, `moltbook-ingest.py`, `record_entity.py`. **Todos los que no son infra son de la "Cata de Harnesses" (octubre 2026)**: un evento cerrado, no tooling vigente.
- **Confirmado por Gonzo (2026-11-18):** `moltbook-ingest.py` está vivo — es la rutina de revisión periódica de sitios para noticias y artículos, con dev.to agregado ese mismo día. `heartbeat-snapshot.sh` es infra (job `agentTurn`).
- **Candidato a revisión:** `record_entity.py` — sistema de entidades, sin uso, con propósito recuperable.

## Consecuencias
- La clasificación vive en `tmp/scripts_inventory_decision.json` (temporal) y no se promovió a gobernanza.
- Los artefactos intermedios (el script generador en `scripts/`, la clave `scripts_inventory` en `settings`, el gate del pre-commit) fueron **retirados** el mismo día.
- Si se retoma, la forma correcta no es un bloque managed con contenido libre: es un script que **escriba** la tabla entre marcadores propios, con `--check` que compare el archivo contra lo que generaría. Eso requiere un mecanismo nuevo, no el de ADR-055.
