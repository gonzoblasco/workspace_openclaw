# STATUS - Kanam Studio

**Última actualización:** 2026-09-01 13:10 GMT-3

## Estado actual

- **Slice 1 COMPLETO** (v0.1.0): grafo editable (React Flow + dagre), modelo Zod, IndexedDB, inspector de nodo, panel de variables, autosave, a11y.
- **Slice 2 COMPLETO** (v0.2.0): engine de juego puro + StoryPlayer.
- **Slice 3 COMPLETO** (v0.3.0): IA co-autora de ramas - chat con streaming SSE, manos sobre el grafo, IDs `nuevo-*` resueltos a UUIDs.
- **Slice 4 COMPLETO** (v0.4.0): canon checker automático - 8 checks de consistencia + panel Canon.
- **Slice 5 COMPLETO** (v0.7.0): world-building con IA - biblia del mundo (personajes, lugares, reglas, tramas), chat dedicado con streaming, panel Mundo, 3 checks de consistencia cruzada.
- **Slice 6 COMPLETO** (v0.8.0): export + relato lineal - `deriveTimeline` (camino canónico + ramas), export JSON (versionable para sync vía git), Twine HTML, Ink, panel Exportar con vista previa.
- **v0.5.0:** toggle tema light/dark (ThemeProvider + localStorage + prefers-color-scheme + anti-FOUC).
- **v0.6.0:** migración de 105 estilos inline a CSS Modules.
- **Próximo:** Slice 7 - Simulación de rutas (último del roadmap).

## Visión (corregida 2026-09-01)

Kanam Studio es un **taller de construcción de mundos y planificación narrativa**, no un juego de aventura. El grafo es el andamiaje interno; el producto es: **mundo consistente + línea de tiempo canónica + relato final**. El modo jugar y las ramas son herramientas de exploración.

## Commits recientes

- `a1ce42f` + `664186b` feat(world): biblia del mundo con IA (Slice 5)
- `f052fa2` fix(world): matching por palabra en canon + updateEntity sin duplicados (review B)
- `ae3fb12` feat(export): relato lineal + export JSON/Twine/Ink (Slice 6)

## Notas

- **IA crítica:** prompt actualizado (no servicial, señala problemas con justificación). Markdown en el chat (react-markdown).
- **Modelo:** deepseek-v4-flash:cloud (default, ~9s vs 5+ min del local).
- **E2E con Playwright:** 10 tests. Browser tool de OpenClaw bloqueado por policy para localhost.
- **Tests:** 152 unit + 10 E2E verdes.
- Proyecto clonado en esta máquina el 2026-08-31 22:52 (estaba solo en GitHub).
