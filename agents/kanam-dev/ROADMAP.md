# ROADMAP.md - Kanam DEV 💻

**Versión actual:** v0.1
**Objetivo:** v0.5 - Autonomía operativa sin supervisión línea por línea
**Última revisión:** 2026-10-07
**Dueño:** kanam-dev (autoría) · Kanam CORE (gobierno)

---

## 2. Retrato verificado de la versión actual (v0.1)

| Capacidad | Estado |
|---|---|
| **Ciclo Hermes (hermes‑architect, hermes‑builder, hermes‑discovery, hermes‑openspec, hermes‑planner, hermes‑pr‑reviewer, hermes‑qa, hermes‑release, hermes‑reviewer)** | 🟡 parcial - la documentación y los `SKILL.md` existen, pero la mayor parte del código de orquestación no está implementada ni testeada. |
| **Desarrollo guiado por especificaciones (`spec‑driven‑development`, `openspec`, `openspec‑pattern`)** | ✅ operativo - skill presente, pruebas unitarias verdes y ejemplos de uso en la memoria. |
| **Desarrollo basado en pruebas (`test‑driven‑development`)** | ✅ operativo - pruebas unitarias integradas en el workspace y ejecución verificable en CI. |
| **Ingeniería de UI Frontend (`frontend‑ui‑engineering`, `design‑direction`)** | ✅ operativo - artefactos de UI, ejemplos de componentes y pruebas visuales presentes. |
| **Documentación y ADRs (`documentation‑and‑adrs`, `idea‑refine`)** | ✅ operativo - guías y plantillas actualizadas, generación de ADRs en los flujos de trabajo. |
| **CI/CD y automatización (`ci‑cd‑and‑automation`, `shipping‑and‑launch`)** | 🟡 parcial - los scripts de despliegue existen, pero falta integración completa con el repositorio y gating de PR. |
| **Optimización de performance (`performance‑optimization`, `performance‑benchmark`)** | 🟡 parcial - documentación de benchmarks, pero pocos resultados medidos y sin pipeline de performance integrado. |
| **Seguridad y hardening (`security‑and‑hardening`)** | 🟡 parcial - checklist disponible, pero no hay validaciones automáticas en CI. |
| **Observabilidad e instrumentación (`observability‑and‑instrumentation`)** | ❌ no existe - no hay código ni pruebas que proporcionen métricas en tiempo real. |
| **Gestión de dependencias (`dependency‑advisor`)** | 🟡 parcial - guía presente, pero falta un motor de resolución automática. |
| **Cross‑engine CSS measurement (`cross‑engine‑css‑measurement`)** | 🟡 parcial - prototipo experimental sin pruebas de integración. |

**Honestidad:** lo que me falta para avanzar de v0.1 a v0.5 son principalmente la orquestación completa del ciclo Hermes, la integración de CI/CD con gating automático y un registro permanente de evidencias que cierre el bucle de retroalimentación.

---

## 3. Visión v0.5 - Rol con autonomía completa

En v0.5 **Kanam DEV** será capaz de:

- Tomar un brief, generar el **OpenSpec** completo, diseñar la arquitectura y planificar las tareas sin intervención humana.
- Emitir **PRs pequeños** (un PR por cambio funcional) que describen exactamente lo que hacen y que pasan los tests con la razón correcta cuando fallan.
- Ejecutar su propio **pipeline de verificación** (hermes‑qa) que produce evidencia reproducible (logs, screenshots, resultados de pruebas) y decide automáticamente si el PR se puede **mergear**.
- Actualizar la documentación (ADRs, READMEs) de forma declarativa y vinculada al cambio, garantizando que la información nunca quede desactualizada.
- Mantener un **registro de evidencias** en la memoria del workspace que permite auditorías posteriores sin volver a ejecutar el pipeline.

En resumen, el rol no depende de que otro agente revise línea por línea; cada entrega está respaldada por pruebas y evidencia verificable.

---

## 4. Camino de madurez v0.1 → v0.5

| Etapa | Qué es | Estado | Criterio de listo (señal verificable) |
|---|---|---|---|
| **v0.1 - Presencia** | El rol existe, tiene `AGENTS.md`, `IDENTITY.md` y un catálogo de 38 skills documentadas. | ✅ completada | Todos los `SKILL.md` están presentes y listados en `skills/`. |
| **v0.2 - Operatividad de skills** | Cada skill posee pruebas automáticas y pasa CI verde. | 🟡 en curso | CI muestra **100 % de tests verdes** para todas las skills y el catálogo contiene enlaces a los artefactos de prueba. |
| **v0.3 - Ciclo Hermes integrado** | El flujo `openspec → hermes‑architect → hermes‑planner → hermes‑builder → hermes‑qa → hermes‑release` está totalmente conectado y ejecutable. | ⚪ pendiente | Un cambio de ejemplo pasa por todo el ciclo y genera un *release* sin intervención humana; se almacena evidencia en `memory/`. |
| **v0.4 - CI/CD con gating automático** | Un *GitHub Action* ejecuta el ciclo Hermes en cada PR y bloquea merges que fallan cualquier etapa. | ⚪ pendiente | Acción `roadmap‑pipeline.yml` se ejecuta en *green* y marca el PR como **approved** sólo cuando todas las métricas (tests, SHARP, evidencias) están aprobadas. |
| **v0.5 - Autonomía completa** | El rol entrega cambios desde el brief hasta el release con evidencia reproducible y sin supervisión línea por línea. | ⚪ pendiente | Demostración de *end‑to‑end* con al menos tres cambios diferentes que siguen todo el ciclo, se mergean automáticamente y se archivan sus evidencias en la memoria. |

---

## 5. Hitos de la versión en curso (v0.5) 

| Hito | Capacidad desbloqueada | Evidencia requerida para cerrar |
|---|---|---|
| **5.1 Catálogo de skills completo** | Visibilidad y descubrimiento de todas las 38 habilidades. | Archivo `skills‑catalog.tsv` actualizado y CI que muestra **todos los skills con tests verdes**. |
| **5.2 Pipeline Hermes operativo** | Orquestación automática de especificación, diseño, planificación, implementación y QA. | Un *workflow* de ejemplo (`demo‑change/`) que finaliza en `hermes‑release` con artefacto `release‑v1.0.tar.gz` y logs accesibles. |
| **5.3 Gating CI/CD** | PRs sólo pueden mergearse si pasan el pipeline completo. | GitHub Action `roadmap‑pipeline.yml` ejecutada en *green* y registro de `check‑run` que marca `approved`. |
| **5.4 Registro persistente de evidencias** | Historial consultable de pruebas y métricas para auditoría. | Base `memory/evidences.db` con al menos 10 entradas y un dashboard HTML que muestra métricas de *SHARP* y *performance*. |
| **5.5 Autogeneración de PRs** | El agente abre PRs a partir de un brief sin intervención. | PR creado por el agente (autor `kanam-dev[bot]`) que contiene el cambio completo y pasa los hitos 5.1‑5.4. |

---

## 6. Lo que rechazo y por qué

- **Convertirme en linter de estilo** - mi foco es *sustancia* (arquitectura, pruebas, documentación). Un linter pertenece al rol `kanam‑ops`.  
- **Generar documentación sin referencia a código** - la regla de *documentación con criterio* exige que cada ADR o README responda a una pregunta concreta de un implementador; la documentación genérica es ruido.  
- **Automatizar despliegues de producción sin revisión de QA** - el pipeline debe detenerse antes del despliegue si `hermes‑qa` falla; cualquier salto que evite esa barrera rompe la garantía de calidad.  
- **Usar código externo sin evaluación de riesgos** - cualquier dependencia nueva debe pasar por `hermes‑pr‑reviewer` y `security‑and‑hardening`; aceptar librerías sin revisión violaría la línea de defensa. 

---

## 7. Red lines + cómo se mide el éxito

**Red lines (líneas rojas):**
1. No escribir código de producción ni modificar la lógica de negocio; solo diseño y facilito la entrega.  
2. No cruzar el dominio de otros roles (no actuar como `kanam‑ops`, `kanam‑critic` o `kanam‑auditor`).  
3. No aprobar cambios sin evidencia reproducible (tests verdes, SHARP score, screenshots). 

**Criterios de éxito para v0.5 (tres condiciones concretas):**
1. **Evidencia reproducible** - cada cambio aprobado almacena logs, resultados de pruebas y artefactos en `memory/`; una auditoría aleatoria reproduce el mismo veredicto.  
2. **Gating automático en CI** - la acción `roadmap‑pipeline.yml` bloquea merges que no cumplan el *criterio de listo* del ciclo Hermes.  
3. **Entrega end‑to‑end sin intervención humana** - al menos tres briefs diferentes generan PRs, pasan por el ciclo completo y se mergean automáticamente.

---

<!-- project: github.com/gonzoblasco/workspace_openclaw -->