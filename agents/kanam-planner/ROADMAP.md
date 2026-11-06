# ROADMAP.md - The Crew Planner 🗺️

## 1. Encabezado
**Versión actual:** v0.3
**Objetivo:** v0.5 - Orquestación autónoma sin supervisión
**Última revisión:** 2026-11-06
**Dueño:** kanam-planner (autoría) · Kanam CORE (gobierno)

## 2. Retrato de la versión actual (hoy)
| Capacidad | Estado |
|---|---|
| Skill `session-plan-orchestration` | ✅ operativa |
| Script `scripts/session_plan.py` | ✅ operativa (wrapper local) |
| Persistencia del plan (`.knowledge/session_plan.json`) | ✅ operativa |
| Auto‑resume al iniciar sesión | 🟡 parcial (brief de programas + `summary`; no carga automática del plan de rol) |
| Asignación de dueño y criterio de salida en pasos | ✅ operativa (`program_plan.py` + `plan_lint.py`) |
| Registro archivado del plan (`.knowledge/archive/…`) | ✅ operativa |
| Observabilidad de estado en tiempo real | 🟡 parcial (`status --json`, `board`, `report`; sin endpoint HTTP) |
| Programas multi‑sesión | ✅ operativos (`program-orchestration`, `crew-dispatch`) |
| Delegación automática desde el CORE | ✅ operativa (`planner-delegation` + regla en `AGENTS.md`) |
| Review semanal | ✅ automation lunes/viernes |
| Dispatch directo del Planner | ⏳ Fase 2 (requiere `subagents.allowAgents`) |

Lo honesto: la Fase 0 y la Fase 1 están implementadas. Queda la autonomía de dispatch (Fase 2): que el Planner invoque Dev/Auditor/Critic sin pasar por el CORE. Esa deuda es deliberada: primero se mide la demanda y la calidad del plan; después se habilita el spawn directo.

## 3. Visión v0.5
Yo imagino que, en v0.5, el Planner será la única fuente de verdad del trabajo. Cada paso del programa (`program_plan.py`) contendrá su **dueño** y **criterio de salida** verificable, el plan se **restaurará automáticamente** al iniciar una sesión y ofrecerá **observabilidad en tiempo real** (estado, bloqueos, métricas). No se convocará al Crew para tareas triviales; solo los roles críticos (Dev, Auditor, Critic) serán invocados en el orden definido. El flujo será completamente autónomo, sin supervisión línea por línea.

## 4. Camino de madurez v0.1 → v0.5
| Etapa | Qué es | Estado | Criterio de listo |
|---|---|---|---|
| v0.1 - Plan básico | Skill y script con persistencia y archivado | ✅ | Tests unitarios de `session_plan.py` pasan y el plan se archiva correctamente |
| v0.2 - Observabilidad + auto‑resume | Auto‑carga del plan al iniciar sesión y métricas de estado en tiempo real | 🟡 | Demo de reinicio donde `summary` muestra el plan activo y `status --json` devuelve JSON válido (sin endpoint HTTP) |
| v0.3 - Dueño y criterio de salida | Cada paso incluye campos `owner` y `exit_criteria` validados | ✅ | Schema actualizado y `plan_lint.py` falla sin los campos y pasa con ellos |
| v0.4 - Orquestación sin llamadas triviales | El Planner invoca Dev, Auditor y Critic vía `sessions_spawn` sin intervención humana para tareas menores | 🟡 | El CORE ya delega programas al Planner y ejecuta sus contratos; falta el spawn directo del Planner |
| v0.5 - Orquestación autónoma total | El plan es la única fuente de verdad; pasos con duenos y criterios, observabilidad, auto‑resume; sin supervisión línea por línea | ⚪ | Suite de aceptación `tests/acceptance/test_planner_autonomy.py` pasa y el CORE firma la señal de listo |

## 5. Hitos de la versión en curso
| Hito | Capacidad desbloqueada | Evidencia requerida |
|---|---|---|
| 5.1 Auto‑resume + observabilidad | El brief de programas se imprime al iniciar y el estado es visible | `session-start.sh` imprime programas activos + `status --json` devuelve JSON válido (sin endpoint HTTP) |
| 5.2 Dueño y criterio de salida en pasos | Cada paso lleva `owner` y `exit_criteria`, y el Planner valida antes de avanzar | Schema JSON con los campos y `plan_lint.py` falla sin ellos |
| 5.3 Orquestación sin llamadas triviales | El CORE delega programas al Planner y ejecuta sus contratos; el Planner no spawnea en Fase 1 | Flujo CORE → Planner → contrato → CORE ejecuta, registrado en el programa |
| 5.4 Aceptación final v0.5 | Versión v0.5 aprobada por el CORE | Suite de aceptación `tests/acceptance/test_planner_autonomy.py` pasa y se firma el checklist de revisión |

## 6. Lo que rechazo y por qué
- **Ejecutar código o diseñar UI:** Esa es responsabilidad de Dev y Auditor; el Planner solo orquesta. Incluir ejecución violaría la red line de “No ejecutar el trabajo”.
- **Almacenar el plan en el repositorio Git:** Rompe la regla de “Persistencia de sesión en `.knowledge/`”. El plan debe ser efímero y archivado internamente.
- **Añadir lógica de negocio dentro del Planner (p.ej., validar calidad de código):** Ese es el dominio del Dev; mezclarlo diluye la responsabilidad del Planner.
- **Exponer el plan como API pública:** El plan es un artefacto interno; su exposición crea acoplamiento innecesario y vulnerabilidades.

## 7. Red lines + cómo se mide el éxito
**Red lines (líneas rojas) de mi evolución**
- No saltar pasos: nunca integrar un componente sin pasar primero por Auditor y Critic.
- No amnesia de sesión: siempre leer el plan de sesión y el brief de programas activos al iniciar.
- No ejecutar el trabajo: jamás escribir código ni diseñar UI.
- No spawnear en Fase 1: el Planner entrega contratos; el CORE ejecuta los `sessions_spawn`.
- No sobre‑planificar: no convocar al Crew para tareas triviales.
- No cruzar dominios de otros roles (ni linter ni dev).
- No inflar el roadmap sin evidencia verificable.
- No cerrar hito sin evidencia reproducible.

**Criterios de éxito para v0.5** (tres condiciones concretas)
1. **Auto‑resume + observabilidad verificadas** mediante `session-start.sh` y `status --json`.
2. **Schema de pasos con `owner` y `exit_criteria` validado** por `plan_lint.py`.
3. **Suite de aceptación v0.5 aprobada** (`tests/acceptance/test_planner_autonomy.py`) que demuestra una ejecución completa del flujo sin intervención humana y con los logs de `sessions_spawn` confirmados.

Solo cuando las tres condiciones se cumplan y el CORE firme la revisión, la versión se actualizará a **v0.5**.

**Programa activo:** [critic-v0.3](PROGRAMS/critic-v0.3.md) - Critic v0.3 "El Cable": T1 primer veredicto real, T3 absorcion, T4 extensiones, T5/v1.0 gate.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->