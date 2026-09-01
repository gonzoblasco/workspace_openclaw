# BRIEF - Kanam Studio

**Fecha:** 2026-08-31
**Repo:** gonzoblasco/kanam-studio (privado)
**Stack:** Next.js 15 + React 19 + Biome + Vitest + Playwright + Zod + OpenSpec (create-stack)

## Visión

Estudio de **ficción interactiva local-first** (BYOK → Ollama). El grafo es el centro: nodos = pasajes, edges = elecciones. Estado del mundo explícito (variables flag/counter). IA co-autora de ramas. Canon checker automático. Modo jugar. Export a Twine/Ink/JSON.

## Relación con kanam-story

Kanam Studio **NO es hermano separado de kanam-story - es su versión superada**: el mismo viaje con IA asistida durante todo el viaje, incluyendo world-building con IA. kanam-story = manuscrito lineal; kanam-studio = grafo de nodos con IA en cada paso.

## Decisiones clave

- **Narrativa ramificada** (decisión de Gonzo 2026-08-31 16:55): no world-building standalone, no engine headless.
- **Modelo de datos:** JSON estructurado con Zod, no DSL (resuelto en ROADMAP).
- **Grafo:** React Flow (@xyflow/react 12) + dagre, no canvas propio (validado en spike).
- **Persistencia:** IndexedDB vía idb, documento por story denormalizado, escrituras atómicas.
- **Store:** Zustand con autosave debounce 800ms.

## Roadmap (7 slices)

1. ✅ Grafo editable (v0.1.0)
2. ✅ Modo jugar (v0.2.0)
3. ⏳ IA co-autora de ramas (chat con manos, proxy a Ollama, contexto = ruta)
4. Canon checker automático
5. World-building con IA (biblia viva superada, consistencia cruzada con canon checker)
6. Export (Twine/Ink/JSON)
7. Simulación de rutas

## Estado

- **Slice 1 COMPLETO** (v0.1.0): grafo editable, modelo Zod, IndexedDB, inspector de nodo, variables, autosave, a11y (tema oscuro AA, skip link, foco visible).
- **Slice 2 COMPLETO** (v0.2.0): engine de juego puro (`src/lib/engine.ts`), StoryPlayer, 13 tests verdes.
- **Próximo:** Slice 3 - IA co-autora de ramas.
