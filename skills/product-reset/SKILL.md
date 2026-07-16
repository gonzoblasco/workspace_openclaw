---
name: "product-reset"
description: "Reset estratégico de un producto existente: diagnosticar estado actual, definir visión, planificar crecimiento, y ejecutar primera fase."
---

# product-reset

> Reset estratégico de un producto existente. Diagnosticar, visionar, planificar, ejecutar.

## Cuándo usarla

- El creador del producto no sabe qué hacer con él ("está ahí, cumple, pero podría ser más")
- El producto tiene tracción inicial pero no dirección clara
- Hay múltiples direcciones posibles y hay que elegir una
- El producto necesita pasar de "proyecto personal" a "herramienta con comunidad"

## No usar cuando

- El producto ya tiene roadmap claro y solo necesita ejecución (usar project-orchestrator)
- Es un producto nuevo sin nada construido (usar product-orchestrator desde Phase 0)
- El creador ya sabe exactamente qué quiere hacer (solo necesita ejecución)

## Fases

### Fase 0 — Intake: entender el producto

**Input:** El producto existe, tiene código, docs, usuarios (aunque sean pocos).

**Acciones:**
1. Leer toda la documentación del producto: BRIEF, EVALUATION, DEFINITION, ROADMAP, STATUS, HANDOFF, LEARNINGS, CHANGELOG, README
2. Leer el código fuente: package.json, estructura, tests, lint status
3. Ejecutar build, tests, lint, typecheck para saber el estado real
4. Identificar qué está funcionando y qué no

**Output:** Diagnóstico honesto del estado actual.

### Fase 1 — Diagnóstico: qué es vs qué podría ser

**Preguntas para el creador (hacerlas en orden, una por una):**

1. **"¿Qué es este producto para vos hoy?"**
   - Proyecto personal que ya cumple su función
   - Herramienta que querés que crezca
   - Vehículo para otra cosa (ej: que la gente adopte X tecnología)
   - Portfolio / experimento

2. **"¿Qué querés que sea?"**
   - Mantenimiento mínimo (solo lo necesario para que funcione)
   - Crecimiento con comunidad (que otros lo usen, compartan, contribuyan)
   - Algo intermedio

3. **"¿Qué NO estás dispuesto a hacer?"** (esto es crítico)
   - Videos, marketing en redes, posts en comunidades
   - Mantener un Discord / canal de comunidad
   - Hacer website
   - Responder issues de usuarios
   - **Cualquier cosa que el creador no vaya a hacer, sacarla del plan sin discusión. Un plan que ignora limitaciones reales va a fallar.**

**Output:** Visión clara y realista.

### Fase 2 — Plan: de acá a allá

**Estructura recomendada (5 fases):**

| Fase | Nombre | Objetivo |
|------|--------|----------|
| 0 | Fundación | Que la experiencia de primera impresión sea impecable |
| 1 | Visibilidad | Que exista en los lugares correctos |
| 2 | Adopción | Que quien lo pruebe quiera quedarse |
| 3 | Comunidad | Que aparezca el primer contributor externo |
| 4 | Sostenibilidad | Que crezca sin consumir al creador |

**Reglas del plan:**
- Cada fase tiene un objetivo concreto y medible
- No saltar fases: no tiene sentido mostrar algo que está roto
- El creador elige el orden y qué incluir/excluir de cada fase
- Si algo no se va a hacer, se saca del plan. Sin discusión, sin "deberías".

**Output:** Roadmap con fases, cada una con checkbox items.

### Fase 3 — Ejecución: arrancar por Fase 0

**Siempre arrancar por Fase 0. Siempre.** No importa si el creador quiere saltar a visibilidad — primero hay que asegurarse de que la experiencia base sea impecable.

**Checklist de Fase 0:**

1. **Fix lo que está roto**
   - Lint: que pase sin errores
   - Build: que compile
   - Tests: que pasen todos
   - Typecheck: que no haya errores de tipos
   - Si hay warnings, documentarlos pero no bloquear

2. **README reescrito**
   - Que venda valor/metodología, no features
   - Preguntar: "¿qué problema resuelve?" en vez de "qué incluye?"
   - Público objetivo claro: "¿para quién es?"
   - Tagline que describa el valor, no el mecanismo

3. **Docs actualizadas**
   - STATUS.md reflejando el nuevo plan
   - ROADMAP.md con las fases acordadas
   - HANDOFF.md con el estado post-reset
   - CHANGELOG.md con los cambios de la sesión

4. **Test de humo manual**
   - Usar el producto como lo usaría un usuario nuevo
   - Verificar que todo funcione
   - Documentar el resultado (qué pasó, qué no)
   - Si hay errores, fixearlos antes de seguir

**Regla de oro:** No pasar a Fase 1 hasta que Fase 0 esté completa y verificada con test de humo.

### Fase 4 — Cierre: documentar el reset

1. Actualizar HANDOFF.md del proyecto con el nuevo plan
2. Registrar en MEMORY.md / daily memory la sesión
3. Hacer commit + push de los cambios del workspace
4. Si el código cambió, commit + push al repo del proyecto

## Outputs esperados

- Diagnóstico del estado actual
- Visión del creador (mantenimiento / crecimiento / vehículo)
- Plan de fases con checkboxes
- Fase 0 ejecutada: lint ✅, build ✅, tests ✅, README nuevo, docs actualizadas
- HANDOFF.md actualizado

## Ejemplo real: create-stack-next (2026-07-16)

Esta skill se creó a partir de una sesión real con CSN. El patrón completo:

1. **Intake:** Leímos BRIEF, EVALUATION, DEFINITION, ROADMAP, STATUS, LEARNINGS, decisions.md, CHANGELOG, README, package.json, código fuente. Corrimos build, tests, lint, typecheck.

2. **Diagnóstico:** CSN es un CLI sólido (64 tests, build ✅) pero vende features cuando debería vender metodología. No tiene comunidad. El template API está infravalorado. El creador quería crecimiento.

3. **Plan:** 5 fases (Fundación → Visibilidad → Adopción → Comunidad → Sostenibilidad). Video demo sacado porque el creador no lo va a hacer.

4. **Ejecución Fase 0:**
   - Fix Biome 2.5+ (schema, `root: true`, `includes` restrictivo)
   - Templates formateados
   - Código muerto eliminado (`logStep`)
   - README reescrito: "Tu proyecto Next.js, listo para IA desde el día 1"
   - CHANGELOG, STATUS, ROADMAP, HANDOFF actualizados
   - Test de humo: lint ✅, typecheck ✅, tests ✅, build ✅

5. **Cierre:** HANDOFF actualizado, daily memory registrada, cambios commiteados.
