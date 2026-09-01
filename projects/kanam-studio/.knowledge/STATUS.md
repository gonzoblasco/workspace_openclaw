# STATUS - Kanam Studio

**Última actualización:** 2026-09-01 17:20 GMT-3

## Estado actual - ROADMAP COMPLETO + HITO 7 ✅

Los 7 slices del roadmap están implementados (v0.1.0 → v0.9.0) y el Hito 7
(prosa final) cierra el círculo de la visión: el grafo es el andamiaje, la
biblia el corazón, el camino canónico la decisión, y la prosa final la salida.

- **Slice 1** (v0.1.0): grafo editable (React Flow + dagre), modelo Zod, IndexedDB, inspector, variables, autosave, a11y.
- **Slice 2** (v0.2.0): engine de juego puro + StoryPlayer.
- **Slice 3** (v0.3.0): IA co-autora de ramas - chat con streaming SSE, manos sobre el grafo.
- **Slice 4** (v0.4.0): canon checker automático - 8 checks + panel Canon.
- **Slice 5** (v0.7.0): world-building con IA - biblia del mundo + chat + 3 checks de consistencia cruzada.
- **Slice 6** (v0.8.0): export + relato lineal - deriveTimeline, JSON versionable, Twine, Ink.
- **Slice 7** (v0.9.0): simulación de rutas - todas las rutas posibles con condiciones/efectos, cobertura, detección de ciclos.
- **Hito 5** (v0.13.0): camino canónico con IA - la IA propone el relato lineal óptimo (qué ramas incorporar, cuáles descartar, con justificación).
- **Hito 7** (v0.14.0): prosa final - la IA escribe el relato completo en prosa narrativa con voz configurable (persona/tiempo/tono), streaming SSE, descarga .md.

**Extras:** v0.5.0 tema light/dark, v0.6.0 CSS Modules, IA crítica (no servicial), markdown en chat, modelo deepseek-v4-flash:cloud.

## Visión (corregida 2026-09-01)

Kanam Studio es un **taller de construcción de mundos y planificación narrativa**, no un juego de aventura. El grafo es el andamiaje interno; el producto es: **mundo consistente + línea de tiempo canónica + relato final**. El modo jugar y las ramas son herramientas de exploración.

## Verificación

- **293 unit + 10 E2E verdes**, lint, typecheck, build OK.
- Prosa final validada contra Ollama real: la IA escribe prosa narrativa coherente con el camino y la biblia (streaming SSE completo, sin acciones).
- Tags: v0.1.0 → v0.9.0 (9 releases).

## Próximos pasos posibles

- Validación en browser real del flujo completo (browser tool bloqueado por policy para localhost - Playwright directo es la vía).
- ADR de la decisión de arquitectura (IndexedDB vs JSON versionable para sync).
- Iteración sobre la visión: refinar la prosa final (longitud objetivo, capítulos, revisión de la IA sobre su propia prosa).
