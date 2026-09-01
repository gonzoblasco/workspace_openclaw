# STATUS - Kanam Studio

**Última actualización:** 2026-09-01 09:50 GMT-3

## Estado actual

- **Slice 1 COMPLETO** (v0.1.0): grafo editable (React Flow + dagre), modelo Zod, IndexedDB, inspector de nodo, panel de variables, autosave, a11y.
- **Slice 2 COMPLETO** (v0.2.0): engine de juego puro + StoryPlayer, 13 tests verdes.
- **Slice 3 COMPLETO** (v0.3.0): IA co-autora de ramas - chat con la IA (proxy a Ollama, JSON mode), manos sobre el grafo (acciones propuestas que el autor aprueba), IDs `nuevo-*` resueltos a UUIDs, a11y.
- **Slice 4 COMPLETO** (v0.4.0): canon checker automático - 8 checks de consistencia (sin start, múltiples starts, edges colgantes, nodos huérfanos, nodos sin salida, variables sin definir, variables sin usar, finales inalcanzables vía BFS). Panel Canon con severidad + navegación al nodo.
- **v0.5.0 (2026-09-01):** toggle de tema light/dark - ThemeProvider (localStorage + prefers-color-scheme), script anti-FOUC, ThemeToggle accesible (aria-pressed, sol/luna), migración completa de colores a CSS variables (9 componentes + React Flow). 59 unit + 7 E2E verdes.
- **UX fixes (2026-09-01):** historia con nodo start automático, botón "+ Inicio", nodos en cascada, hint de conexión por drag, controles React Flow oscuros en bottom-right (lejos del logo de Next).
- **Próximo:** Slice 5 - World-building con IA (biblia viva superada, consistencia cruzada con canon checker).

## Commits recientes

- `67cb71c` feat(editor): historia con nodo start automatico + cascada + hint de conexion
- `42c3c86` style: biome format en handleAddNode
- `0b64999` feat(theme): toggle light/dark con persistencia y prefers-color-scheme
- `ca29089` docs: changelog v0.5.0

## Notas

- **E2E con Playwright:** 7 tests (flujo completo, conexión por drag, persistencia, tema). Browser tool de OpenClaw bloqueado por policy para localhost - Playwright directo es la vía de validación.
- El modelo local qwen3.5:9b-mlx tarda ~120s en frío (timeout del proxy configurado a 120s).
- Proyecto clonado en esta máquina el 2026-08-31 22:52 (estaba solo en GitHub).
