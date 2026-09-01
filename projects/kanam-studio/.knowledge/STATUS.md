# STATUS - Kanam Studio

**Última actualización:** 2026-09-01 13:45 GMT-3

## Estado actual - ROADMAP COMPLETO ✅

Los 7 slices del roadmap están implementados (v0.1.0 → v0.9.0):

- **Slice 1** (v0.1.0): grafo editable (React Flow + dagre), modelo Zod, IndexedDB, inspector, variables, autosave, a11y.
- **Slice 2** (v0.2.0): engine de juego puro + StoryPlayer.
- **Slice 3** (v0.3.0): IA co-autora de ramas - chat con streaming SSE, manos sobre el grafo.
- **Slice 4** (v0.4.0): canon checker automático - 8 checks + panel Canon.
- **Slice 5** (v0.7.0): world-building con IA - biblia del mundo + chat + 3 checks de consistencia cruzada.
- **Slice 6** (v0.8.0): export + relato lineal - deriveTimeline, JSON versionable, Twine, Ink.
- **Slice 7** (v0.9.0): simulación de rutas - todas las rutas posibles con condiciones/efectos, cobertura, detección de ciclos.

**Extras:** v0.5.0 tema light/dark, v0.6.0 CSS Modules, IA crítica (no servicial), markdown en chat, modelo deepseek-v4-flash:cloud.

## Visión (corregida 2026-09-01)

Kanam Studio es un **taller de construcción de mundos y planificación narrativa**, no un juego de aventura. El grafo es el andamiaje interno; el producto es: **mundo consistente + línea de tiempo canónica + relato final**. El modo jugar y las ramas son herramientas de exploración.

## Verificación

- **169 unit + 10 E2E verdes**, lint, typecheck, build OK.
- Tags: v0.1.0 → v0.9.0 (9 releases).

## Próximos pasos posibles

- Validación en browser real del flujo completo (browser tool bloqueado por policy para localhost - Playwright directo es la vía).
- ADR de la decisión de arquitectura (IndexedDB vs JSON versionable para sync).
- Iteración sobre la visión: refinar el relato lineal con IA (que la IA proponga el camino canónico).
