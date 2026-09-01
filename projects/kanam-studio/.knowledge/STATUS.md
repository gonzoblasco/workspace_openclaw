# STATUS - Kanam Studio

**Última actualización:** 2026-08-31 23:35 GMT-3

## Estado actual

- **Slice 1 COMPLETO** (v0.1.0): grafo editable (React Flow + dagre), modelo Zod, IndexedDB, inspector de nodo, panel de variables, autosave, a11y.
- **Slice 2 COMPLETO** (v0.2.0): engine de juego puro + StoryPlayer, 13 tests verdes.
- **Slice 3 COMPLETO** (v0.3.0): IA co-autora de ramas - chat con la IA (proxy a Ollama, JSON mode), manos sobre el grafo (acciones propuestas que el autor aprueba), IDs `nuevo-*` resueltos a UUIDs, a11y. 34 tests verdes.
- **Próximo:** Slice 4 - Canon checker automático.

## Commits (después de v0.2.0)

- `5a8432f` feat(ai): IA co-autora de ramas con acciones sobre el grafo (Slice 3)
- `3a8565c` fix(ai): idempotencia de acciones y validacion de existencia (review B)
- `193e6e3` docs: changelog fixes review B para v0.3.0

## Pipeline (T=15, high)

- Agente A escribió el Slice 3 (commit 5a8432f).
- Agente B revisó: 4 hallazgos mayores (applyAll re-aplicaba acciones, createNode con id repetido colisionaba, createEdge sin validar existencia, updateNode/updateEdge con éxito silencioso) + menores (a11y aria-live, raw en errores, tamaño de payload).
- Kanam aplicó los fixes (commit 3a8565c) + 5 tests nuevos.
- Validación: endpoint real contra Ollama (qwen3.5:9b-mlx) responde reply + acciones válidas. 34/34 tests, lint, typecheck, build OK.

## Notas

- Bug del template create-stack: biome.json con `root: false` escaneaba el workspace entero (10453 errores). Fix: `root: true` (commit 353e7f1 en create-stack).
- El modelo local qwen3.5:9b-mlx tarda ~120s en frío (timeout del proxy configurado a 120s).
- Validación SIEMPRE en browser real (regla de validación UI). Browser tool bloqueado por policy para localhost - validación vía curl + tests.
- Proyecto clonado en esta máquina el 2026-08-31 22:52 (estaba solo en GitHub).
