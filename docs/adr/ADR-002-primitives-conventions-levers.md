# ADR-002 - Mental model: Primitives, Conventions, Levers para evaluar tecnologias

**Status:** Aceptado
**Origen:** remix-book ADR-001
**Fecha:** 2026-08-05

## Contexto

Al evaluar una tecnologia nueva (framework, libreria, herramienta), es facil caer en analisis superficiales: "tiene X features", "es popular", "lo usa Y empresa". Falta un framework de analisis estructurado que permita comparar tecnologias en terminos de su filosofia de diseno, no solo su feature set.

## Decision

Adoptar el mental model de **Primitives, Conventions, Levers** como framework de analisis para evaluar cualquier tecnologia.

### Primitives
Son las herramientas que la tecnologia expone para usar en codigo: funciones, hooks, componentes, tipos. Deben ser faciles de entender pero lo suficientemente composables para permitir logica de negocio compleja.

**Que buscar:**
- Los primitives son abstracciones delgadas o cajas negras?
- Siguen estandares existentes o inventan los suyos propios?
- Son composables o te obligan a un solo camino?

### Conventions
Son contratos entre la tecnologia y tu aplicacion: naming de archivos, estructura de carpetas, exports esperados. Reducen configuracion y boilerplate a cambio de seguir reglas predecibles.

**Que buscar:**
- Las conventions son intuitivas o cripticas?
- Se pueden sobrescribir cuando es necesario?
- La tecnologia documenta claramente el contrato?

### Levers
Son opciones que la tecnologia te da para optimizar segun tus prioridades. No hay una talla unica - vos decidis que tradeoffs hacer.

**Que buscar:**
- La tecnologia te deja elegir o decide por vos?
- Los levers son explicitos o tenes que hacer workarounds?
- Podes cambiar de opinion sin reescribir todo?

## Consecuencias

### Positivas
- Framework de analysis portable a cualquier tecnologia (React, Vue, Svelte, Express, etc.).
- Ayuda a identificar rapidamente si una tecnologia es opinionada en exceso o te da control.
- Util para escribir ADRs y documentacion tecnica: podes categorizar features.

### Negativas
- No todas las tecnologias se dejan mapear limpiamente a estas tres categorias.
- Algunos features pueden caer en multiples categorias (ambiguo).

## Notas

Este ADR se aplica al evaluar cualquier tecnologia futura. Es un patron de analisis, no una regla de implementacion.
