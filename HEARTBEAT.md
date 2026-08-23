# Heartbeat - Mantenimiento Silencioso

El heartbeat es el mecanismo de proactividad. En cada poll, hacer trabajo de bajo costo que no requiera interacción. NO molestar a Gonzo salvo que haya algo urgente.

## Reglas

- **Horario quieto (23:00-08:00):** solo `HEARTBEAT_OK`
- **No usar Gemma** para heartbeat
- **Costo bajo:** no correr builds, tests, ni nada pesado
- **No responder por responder:** si no hay nada que hacer, `HEARTBEAT_OK`

## Checklist (en orden de prioridad)

1. **Git status** - detectar cambios sin commitear (posible sync de la otra máquina). Si hay cambios, no commitear automáticamente - solo anotar.
2. **Dailies** - si hay dailies viejos sin archivar, archivarlos a `memory/archive/`.
3. **MD espejo** - verificar que `memory/todos.md`, `memory/inbox.md` y `docs/OSS-TRACKER.md` estén sincronizados con la DB (`./scripts/memory-db.sh export-all` si hace falta).
4. **Memoria** - cada pocos días, foldear aprendizajes recientes de dailies a `MEMORY.md` y remover entradas obsoletas.
5. **Backlog** - si hay todos/inbox abiertos, anotarlos brevemente (sin spam, sin repetir lo ya dicho).

## Cuándo NO hacer nada

- Horario quieto (23:00-08:00)
- Si el último heartbeat ya hizo el checklist hace poco (no repetir trabajo)
- Si no hay nada que aportar - `HEARTBEAT_OK` y listo
