# ROADMAP.md - The Crew Planner 🗺️

## 1. Encabezado
**Versión actual:** v0.1
**Objetivo:** v0.5 - Orquestación autónoma sin supervisión
**Última revisión:** 2026-10-07
**Dueño:** kanam-planner (autoría) · Kanam CORE (gobierno)

## 2. Retrato de la versión actual (hoy)
| Capacidad | Estado |
|---|---|
| Skill `session-plan-orchestration` | ✅ operativa |
| Script `scripts/session_plan.py` | ✅ operativa |
| Persistencia del plan (`.knowledge/session_plan.json`) | ✅ operativa |
| Auto‑resume al iniciar sesión | 🟡 parcial (solo `summary`, no carga automática) |
| Asignación de dueño y criterio de salida en pasos | ❌ ausente |
| Registro archivado del plan (`.knowledge/archive/…`) | ✅ operativa |
| Observabilidad de estado en tiempo real | ❌ ausente |

Lo honesto: me falta la capacidad de asignar dueño y criterio de salida a cada paso, auto‑resume sin intervención y un mecanismo de observabilidad en tiempo real; esas deudas me impiden avanzar a v0.5.

## 3. Visión v0.5
Yo imagino que, en v0.5, el Planner será la única fuente de verdad del trabajo. Cada paso del `.knowledge/session_plan.json` contendrá su **dueño** y **criterio de salida** verificable, el plan se **restaurará automáticamente** al iniciar una sesión y ofrecerá **observabilidad en tiempo real** (estado, bloqueos, métricas). No se convocará al Crew para tareas triviales; solo los roles críticos (Dev, Auditor, Critic) serán invocados en el orden definido. El flujo será completamente autónomo, sin supervisión línea por línea.

## 4. Camino de madurez v0.1 → v0.5
| Etapa | Qué es | Estado | Criterio de listo |
|---|---|---|---|
| v0.1 - Plan básico | Skill y script con persistencia y archivado | ✅ | Tests unitarios de `session_plan.py` pasan y el plan se archiva correctamente |
| v0.2 - Observabilidad + auto‑resume | Auto‑carga del plan al iniciar sesión y métricas de estado en tiempo real | 🟡 | Demo de reinicio donde `summary` muestra el plan activo y un endpoint `/knowledge/session_plan/status` devuelve JSON válido |
| v0.3 - Dueño y criterio de salida | Cada paso incluye campos `owner` y `exit_criteria` validados | 🟡 | Schema actualizado y pruebas que fallan sin los campos y pasan con ellos |
| v0.4 - Orquestación sin llamadas triviales | El Planner invoca Dev, Auditor y Critic vía `sessions_spawn` sin intervención humana para tareas menores | ⚪ | Test end‑to‑end con caso de uso dummy completo sin intervención manual |
| v0.5 - Orquestación autónoma total | El plan es la única fuente de verdad; pasos con duenos y criterios, observabilidad, auto‑resume; sin supervisión línea por línea | ⚪ | Suite de aceptación `tests/acceptance/test_planner_autonomy.py` pasa y el CORE firma la señal de listo |

## 5. Hitos de la versión en curso
| Hito | Capacidad desbloqueada | Evidencia requerida |
|---|---|---|
| 5.1 Auto‑resume + observabilidad | El plan se restaura automáticamente y su estado es visible en tiempo real | Prueba de reinicio exitosa + endpoint `/knowledge/session_plan/status` devuelve JSON válido |
| 5.2 Dueño y criterio de salida en pasos | Cada paso lleva `owner` y `exit_criteria`, y el Planner valida antes de avanzar | Schema JSON con los campos, pruebas unitarias que verifican presencia y valores lógicos |
| 5.3 Orquestación sin llamadas triviales | El Planner dispara los roles mediante `sessions_spawn` sin intervención humana | Test end‑to‑end que completa un flujo completo y registra invocaciones automáticas |
| 5.4 Aceptación final v0.5 | Versión v0.5 aprobada por el CORE | Suite de aceptación `tests/acceptance/test_planner_autonomy.py` pasa y se firma el checklist de revisión |

## 6. Lo que rechazo y por qué
- **Ejecutar código o diseñar UI:** Esa es responsabilidad de Dev y Auditor; el Planner solo orquesta. Incluir ejecución violaría la red line de “No ejecutar el trabajo”.
- **Almacenar el plan en el repositorio Git:** Rompe la regla de “Persistencia de sesión en `.knowledge/`”. El plan debe ser efímero y archivado internamente.
- **Añadir lógica de negocio dentro del Planner (p.ej., validar calidad de código):** Ese es el dominio del Dev; mezclarlo diluye la responsabilidad del Planner.
- **Exponer el plan como API pública:** El plan es un artefacto interno; su exposición crea acoplamiento innecesario y vulnerabilidades.

## 7. Red lines + cómo se mide el éxito
**Red lines (líneas rojas) de mi evolución**
- No saltar pasos: nunca integrar un componente sin pasar primero por Auditor y Critic.
- No amnesia de sesión: siempre leer `.knowledge/session_plan.json` al iniciar.
- No ejecutar el trabajo: jamás escribir código ni diseñar UI.
- No sobre‑planificar: no convocar al Crew para tareas triviales.
- No cruzar dominios de otros roles (ni linter ni dev).
- No inflar el roadmap sin evidencia verificable.
- No cerrar hito sin evidencia reproducible.

**Criterios de éxito para v0.5** (tres condiciones concretas)
1. **Auto‑resume + observabilidad verificadas** mediante pruebas de reinicio y endpoint de estado.
2. **Schema de pasos con `owner` y `exit_criteria` validado** y cubierto por pruebas unitarias.
3. **Suite de aceptación v0.5 aprobada** (`tests/acceptance/test_planner_autonomy.py`) que demuestra una ejecución completa del flujo sin intervención humana y con los logs de `sessions_spawn` confirmados.

Solo cuando las tres condiciones se cumplan y el CORE firme la revisión, la versión se actualizará a **v0.5**.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->