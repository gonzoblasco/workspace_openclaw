---
name: "openspec-creator"
description: "Crear specs OpenSpec as-built o delta para features existentes, guiando al usuario paso a paso."
---

# openspec-creator

Crear specs OpenSpec (as-built o delta) en proyectos con OpenSpec inicializado. Guía al usuario paso a paso por el viaje completo: elegir qué spec'ear, leer el código (as-built) o definir lo que se quiere construir (delta), identificar requisitos, escribir escenarios WHEN/THEN, y commitear.

Cubre dos flujos:
- **As-built**: describir funcionalidad que YA EXISTE en el código
- **Delta**: describir funcionalidad que SE VA A CONSTRUIR (spec primero, código después)

## Cuándo usarla

- El usuario pide "creame una spec para X feature"
- El usuario pide "actualizá la spec de Y"
- El usuario quiere aprender a escribir specs y pide ser guiado
- Hay una feature sin spec y queremos documentarla antes de modificarla
- El usuario quiere planificar un cambio nuevo escribiendo la spec primero

## Flujo general

### Fase 0: Determinar el tipo de spec

Preguntar al usuario:
- **As-built**: la feature ya existe en código, vamos a documentarla
- **Delta**: la feature NO existe, vamos a planificarla antes de codear

Según la respuesta, seguir el flujo correspondiente.

---

## FLUJO AS-BUILT (documentar lo que ya existe)

### Fase 1: Elegir qué spec'ear

1. Si el usuario ya dijo qué feature, usar esa.
2. Si no, listar las Edge Functions, componentes, o módulos del proyecto que NO tienen spec en `openspec/specs/`.
3. Preguntar al usuario cuál quiere spec'ear. Dar contexto breve de cada opción.
4. Si el proyecto no tiene OpenSpec inicializado, abortar y sugerir `openspec init` primero.

### Fase 2: Leer el código

1. Leer el código de la feature elegida (Edge Function, componente, etc.).
2. Si la feature abarca múltiples archivos (ej: webhook + sync), leer todos los relevantes.
3. Identificar:
   - Endpoints/entry points
   - Flujos principales (happy path)
   - Casos borde (errores, falta de config, datos incompletos)
   - Integraciones externas (APIs, webhooks, servicios)
   - Configuraciones que afectan comportamiento (feature flags, settings)
4. Tomar notas mentales de los requisitos que emergen.

### Fase 3: Identificar requisitos

1. Agrupar la funcionalidad en bloques lógicos (Requisitos). Cada Requirement cubre un aspecto coherente.
2. Para cada Requirement, pensar en los escenarios que cubre:
   - Escenario feliz (todo funciona)
   - Escenario sin datos/config (fallback)
   - Escenario de error (timeout, 401, 429, parse failure)
   - Escenario de borde (datos parciales, legacy compat)
3. Nombrar cada Requirement con un título descriptivo.

### Fase 4: Escribir la spec

Estructura:

```markdown
# Spec: <Nombre>

## Purpose

<Una línea que explica para qué sirve esta feature>

## Requirements

### Requirement: <Nombre del requisito>
<El sistema SHALL + descripción de alto nivel>

#### Scenario: <Nombre del escenario>
- **WHEN** <condición que dispara el escenario>
- **THEN** <comportamiento esperado>
- **AND** <comportamiento adicional si aplica>
```

Reglas:
- Usar SHALL para requisitos (no "debe", no "should")
- Cada escenario es un WHEN/THEN atómico
- Usar AND para consecuencias adicionales del mismo escenario
- Escribir en español (a menos que el proyecto use inglés)
- Ser específico: nombrar Edge Functions, tablas, RPCs, settings por su nombre real
- No describir el "cómo" (implementación), solo el "qué" (comportamiento observable)

### Fase 5: Crear el archivo

1. Crear `openspec/specs/<slug>/spec.md`
2. Escribir la spec completa
3. Verificar que el archivo existe y tiene contenido

### Fase 6: Commitear

1. `git add openspec/specs/<slug>/spec.md`
2. `git commit -m "feat(openspec): spec as-built para <nombre>"`
3. Mostrar resumen al usuario de lo que se creó

---

## FLUJO DELTA (planificar lo que se va a construir)

### Fase 1: Definir qué se quiere construir

1. Preguntar al usuario qué quiere hacer. Explorar juntos:
   - ¿Qué problema resuelve?
   - ¿Quién lo va a usar?
   - ¿Cómo debería funcionar el flujo feliz?
2. Si el usuario no tiene claro, ayudarlo a definir el alcance mínimo.
3. Elegir un nombre corto para el cambio (slug).

### Fase 2: Identificar requisitos (sin código)

1. A diferencia del as-built, NO hay código que leer. Los requisitos se definen desde la necesidad.
2. Para cada Requirement, pensar en:
   - Escenario feliz (todo funciona como el usuario espera)
   - Escenario sin datos (qué pasa si no hay config, no hay API key, no hay registros)
   - Escenario de error (qué pasa si falla una API externa, si hay timeout, si el usuario no tiene permiso)
   - Escenario de borde (qué pasa si el usuario hace algo inesperado)
3. Preguntar al usuario: "¿Qué pasa si...?" para cubrir casos que no consideró.
4. Nombrar cada Requirement con un título descriptivo.

### Fase 3: Escribir el delta spec

Misma estructura que as-built, pero en `openspec/changes/<slug>/spec.md`:

```markdown
# Delta: <Nombre del cambio>

## Purpose

<Qué problema resuelve este cambio>

## Requirements

### Requirement: <Nombre del requisito>
<El sistema SHALL + descripción>

#### Scenario: <Nombre del escenario>
- **WHEN** <condición>
- **THEN** <comportamiento esperado>
- **AND** <consecuencia>
```

Reglas adicionales para delta specs:
- Usar futuro o presente genérico ("el sistema SHALL...")
- Incluir non-goals: qué NO va a hacer este cambio (para evitar scope creep)
- Si el cambio depende de otros cambios o configuraciones previas, documentarlo

### Fase 4: Revisar con el usuario

1. Leer la spec completa al usuario (o mostrarle el archivo).
2. Preguntar: "¿Esto cubre todo lo que querías? ¿Falta algo?"
3. Ajustar según feedback.

### Fase 5: Crear el archivo

1. Crear `openspec/changes/<slug>/spec.md`
2. Escribir el delta spec completo
3. Verificar que el archivo existe y tiene contenido

### Fase 6: Commitear

1. `git add openspec/changes/<slug>/spec.md`
2. `git commit -m "feat(openspec): delta spec para <nombre>"`
3. Mostrar resumen al usuario de lo que se creó

### Fase 7: Codear contra la spec (posterior)

Cuando el usuario quiera implementar:
1. Leer el delta spec como guía
2. Codear cada Requirement
3. Al terminar, archivar el delta: mover de `openspec/changes/<slug>/` a `openspec/changes/archive/<slug>/`
4. Si la feature es permanente, crear una spec as-built en `openspec/specs/` con el mismo contenido

---

## Formato de respuesta

Durante el proceso, ir mostrando al usuario qué se está haciendo en cada paso. Explicar el "por qué" de cada decisión (por qué este Requirement, por qué estos escenarios). Al final, dar un resumen de lo que aprendió.

## Notas

- Si el usuario no tiene claro qué feature spec'ear, dar opciones con breve descripción de cada una.
- Si el código es muy grande (>500 líneas), leer por partes y resumir.
- Las specs as-built describen funcionalidad EXISTENTE. No inventar features que no están implementadas.
- Si hay features parcialmente implementadas, documentar solo lo que funciona.
- Los delta specs describen funcionalidad A CONSTRUIR. Son el plano antes de la construcción.
- Un delta spec bien escrito es suficiente para que un agente IA (o cualquier dev) pueda implementar el cambio sin preguntar nada más.
- Después de implementar un delta, archivar el cambio y considerar si merece una spec as-built permanente.
