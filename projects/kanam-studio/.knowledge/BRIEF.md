# BRIEF - Kanam Studio

**Fecha:** 2026-09-01 (visión corregida)
**Repo:** gonzoblasco/kanam-studio (privado)
**Stack:** Next.js 15 + React 19 + Biome + Vitest + Playwright + Zod + OpenSpec (create-stack)

## Visión (corregida 2026-09-01)

**Kanam Studio es un taller de construcción de mundos y planificación narrativa, no un juego de "elige tu propia aventura".**

El grafo es el **andamiaje interno** del autor: cada nodo = un momento de la historia, cada edge = una relación causal/temporal entre momentos. El propósito NO es que un lector juegue las ramas - es que el autor:

1. **Defina el mundo** (personajes, lugares, reglas, tramas) conversando con la IA, que mantiene consistencia (canon checker + world-building).
2. **Explore las ramificaciones** para entender las posibilidades narrativas (modo jugar, simulación de rutas).
3. **Derive el relato lineal final**: el orden exacto de los sucesos, la versión canónica que se escribe como prosa.

El "modo jugar" y las ramas son **herramientas de exploración, no el producto**. El producto es: **mundo consistente + línea de tiempo canónica + relato final**.

## Relación con kanam-story

Kanam Studio **NO es hermano separado de kanam-story - es su versión superada**: el mismo viaje con IA asistida durante todo el viaje, incluyendo world-building con IA. kanam-story = manuscrito lineal; kanam-studio = grafo de nodos con IA en cada paso. La salida de kanam-studio (relato final derivado) alimenta la escritura en prosa.

## Decisiones clave

- **Narrativa ramificada como andamiaje** (decisión de Gonzo 2026-08-31 16:55, visión refinada 2026-09-01): el grafo es el taller, no el producto final.
- **Modelo de datos:** JSON estructurado con Zod, no DSL (resuelto en ROADMAP).
- **Grafo:** React Flow (@xyflow/react 12) + dagre, no canvas propio (validado en spike).
- **Persistencia:** IndexedDB vía idb, documento por story denormalizado, escrituras atómicas.
- **Store:** Zustand con autosave debounce 800ms.
- **Estilos:** CSS Modules (v0.6.0), CSS variables para tema light/dark.
- **IA:** deepseek-v4-flash:cloud (default), streaming SSE, crítica constructiva (no servicial).

## Roadmap (7 slices)

1. ✅ Grafo editable (v0.1.0)
2. ✅ Modo jugar (v0.2.0)
3. ✅ IA co-autora de ramas (v0.3.0)
4. ✅ Canon checker automático (v0.4.0)
5. ⏳ **World-building con IA** (biblia viva superada, consistencia cruzada con canon checker) - CENTRAL para la visión
6. Export (Twine/Ink/JSON) + **derivación del relato lineal final**
7. Simulación de rutas

## Estado

- **Slices 1-4 COMPLETOS** (v0.1.0 → v0.4.0), v0.5.0 (tema), v0.6.0 (CSS Modules).
- **Próximo:** Slice 5 - World-building con IA (el corazón de la visión corregida).
