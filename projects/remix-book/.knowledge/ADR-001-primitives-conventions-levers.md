# ADR-001 — Mental Model: Primitives, Conventions, Levers

**Fecha:** 2026-08-05
**Contexto:** Capítulo 1 de "Full Stack Web Development with Remix"
**Fuente:** Andre Landgraf, basado en conceptos de Ryan Florence

## Decisión

Adoptar el mental model de **Primitives, Conventions, Levers** como framework de análisis para evaluar cualquier tecnología, no solo Remix.

## Detalle

### Primitives
Son las herramientas que el framework expone para que las uses en tu código: funciones, hooks, componentes, tipos. Deben ser fáciles de entender pero lo suficientemente composables para permitir lógica de negocio compleja. En Remix, los primitives son thin abstractions de web APIs estándar (Form component ≈ form element nativo, Request/Response siguen Web Fetch API).

**Qué buscar en cualquier tecnología:**
- ¿Los primitives son abstracciones delgadas o cajas negras?
- ¿Siguen estándares existentes o inventan los suyos propios?
- ¿Son composables o te obligan a un solo camino?

### Conventions
Son contratos entre el framework y tu aplicación: naming de archivos, estructura de carpetas, exports esperados. Reducen configuración y boilerplate a cambio de seguir reglas predecibles.

**Qué buscar:**
- ¿Las conventions son intuitivas o crípticas?
- ¿Se pueden sobrescribir cuando es necesario?
- ¿El framework documenta claramente el contrato?

### Levers
Son opciones que el framework te da para optimizar según tus prioridades. No hay una talla única — vos decidís qué tradeoffs hacer. Esto te da poder pero también responsabilidad.

**Qué buscar:**
- ¿El framework te deja elegir o decide por vos?
- ¿Los levers son explícitos o tenés que hacer workarounds?
- ¿Podés cambiar de opinión sin reescribir todo?

## Consecuencias

**Positivas:**
- Framework de análisis portable a cualquier tecnología (React, Vue, Svelte, Express, etc.)
- Ayuda a identificar rápidamente si un framework es opinionado en exceso o te da control
- Útil para escribir ADRs y documentación técnica: podés categorizar features

**Negativas:**
- No todos los frameworks se dejan mapear limpiamente a estas tres categorías
- Algunos features pueden caer en múltiples categorías (ambiguo)

## Notas

Este ADR se aplica al evaluar cualquier tecnología futura. Es un patrón de análisis, no una regla de implementación.
