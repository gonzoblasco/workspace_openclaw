# STATUS - Kanam Studio

**Última actualización:** 2026-09-01 09:15 GMT-3

## Estado actual

- **Slice 1 COMPLETO** (v0.1.0): grafo editable (React Flow + dagre), modelo Zod, IndexedDB, inspector de nodo, panel de variables, autosave, a11y.
- **Slice 2 COMPLETO** (v0.2.0): engine de juego puro + StoryPlayer, 13 tests verdes.
- **Slice 3 COMPLETO** (v0.3.0): IA co-autora de ramas - chat con la IA (proxy a Ollama, JSON mode), manos sobre el grafo (acciones propuestas que el autor aprueba), IDs `nuevo-*` resueltos a UUIDs, a11y. 34 tests verdes.
- **Slice 4 COMPLETO** (v0.4.0): canon checker automático - 8 checks de consistencia (sin start, múltiples starts, edges colgantes, nodos huérfanos, nodos sin salida, variables sin definir, variables sin usar, finales inalcanzables vía BFS). Panel Canon con severidad + navegación al nodo. 52 tests verdes.
- **Próximo:** Slice 5 - World-building con IA (biblia viva superada, consistencia cruzada con canon checker).

## Commits (después de v0.3.0)

- `7e09301` fix(a11y): main centraba el editor y colapsaba el grafo a 0px
- `0d4b58e` feat(canon): canon checker automático con 8 checks (Slice 4)
- `29ece14` docs: changelog v0.4.0

## Pipeline (T=16, high)

- Agente A escribió el Slice 4 (canon.ts + CanonPanel + tests, 18 nuevos).
- Agente B revisó: **cero críticos, cero mayores** - solo análisis de edge cases confirmados como correctos (BFS con ciclos, orden de severidad, navegación a nodos existentes).
- Kanam verificó: 52/52 tests, lint, typecheck, build OK.
- Fix a11y reportado por Gonzo (grafo invisible): CSS global centraba el editor → stretch por defecto.

## Notas

- Bug del template create-stack: biome.json con `root: false` escaneaba el workspace entero (10453 errores). Fix: `root: true` (commit 353e7f1 en create-stack).
- El modelo local qwen3.5:9b-mlx tarda ~120s en frío (timeout del proxy configurado a 120s).
- Validación SIEMPRE en browser real (regla de validación UI). Browser tool bloqueado por policy para localhost - validación vía curl + tests.
- Proyecto clonado en esta máquina el 2026-08-31 22:52 (estaba solo en GitHub).
