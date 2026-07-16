---
name: "product-reset"
description: "Reset estratégico de un producto existente: diagnosticar estado actual, definir visión, planificar crecimiento, y ejecutar primera fase."
---

# product-reset

> Reset estratégico de un producto existente. Diagnosticar, visionar, planificar, ejecutar.

## Cuándo usarla

- El creador del producto no sabe qué hacer con él ("está ahí, cumple, pero podría ser más")
- El producto tiene tracción inicial (~1000 descargas, algunos usuarios) pero no dirección clara
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

**Preguntas para el creador:**
1. "¿Qué es este producto para vos hoy?" — proyecto personal, herramienta, experimento, portfolio
2. "¿Qué querés que sea?" — mantenimiento, crecimiento, vehículo para otra cosa
3. "¿Qué NO estás dispuesto a hacer?" — videos, marketing,社区, etc. (esto es crítico: un plan que ignora limitaciones reales va a fallar)

**Output:** Visión clara y realista. Si el creador quiere crecimiento pero no va a hacer marketing, hay que ajustar el plan.

### Fase 2 — Plan: de acá a allá

**Estructura del plan:**
- Fase 0: Fundación — que la experiencia de primera impresión sea impecable (fixes, lint, README, docs)
- Fase 1: Visibilidad — que exista en los lugares correctos (website, posts, listados)
- Fase 2: Adopción — que quien lo pruebe quiera quedarse (onboarding, templates, casos de uso)
- Fase 3: Comunidad — que aparezca el primer contributor externo (issues, discussions, release notes)
- Fase 4: Sostenibilidad — que crezca sin consumir al creador (CI/CD, automated releases, scope discipline)

**Reglas del plan:**
- Cada fase tiene un objetivo concreto y medible
- No saltar fases: no tiene sentido mostrar algo que está roto
- El creador elige el orden y qué incluir/excluir
- Si algo no se va a hacer (ej: video), se saca del plan sin discusión

**Output:** Roadmap con fases, cada una con checkbox items.

### Fase 3 — Ejecución: arrancar por Fase 0

**Siempre arrancar por Fase 0, que incluye:**

1. **Fix lo que está roto** — lint, build, tests, typecheck. Que pase todo en verde.
2. **README reescrito** — que venda metodología/valor, no features. Preguntar: "¿qué problema resuelve?" en vez de "qué incluye?"
3. **Docs actualizadas** — STATUS, ROADMAP, HANDOFF, CHANGELOG reflejando el nuevo plan
4. **Test de humo manual** — generar un proyecto, correrlo, que ande. Documentar el resultado.

**Regla de oro:** No pasar a Fase 1 hasta que Fase 0 esté completa y verificada.

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

## Ejemplo real

Ver sesión de create-stack-next (2026-07-16):
- Producto: CLI scaffolder con ~1000 descargas, sin dirección clara
- Diagnóstico: vende features, no metodología; sin comunidad; template API infravalorado
- Visión: crecimiento con comunidad
- Plan: 5 fases (Fundación → Visibilidad → Adopción → Comunidad → Sostenibilidad)
- Fase 0: fix Biome, formatear templates, README reescrito, docs actualizadas
- Video sacado del plan porque el creador no lo va a hacer
