# PLANNER-INTEGRATION.md - Dónde cae el Planner y quién lo llama

**Fecha:** 2026-11-06
**Estado:** implementación Fase 1. El Planner deja de ser un agente que hay que abrir a mano y pasa a ser una estación de servicio del CORE.
**Decisión de arquitectura:** el CORE sigue siendo el orquestador accountable (ADR-083). El Planner es su servicio de planificación y estado de programas. No compite con el CORE ni emite veredictos.

---

## 1. La respuesta corta

- **Gonzo** habla con el **CORE**. No necesita abrir al Planner.
- **El CORE** llama al Planner **al inicio de un programa**, cuando cambia el alcance, en los gates y en el cierre.
- **El Planner** devuelve plan, brief y contratos. **No spawnea en Fase 1.**
- **El CORE** ejecuta los contratos con `sessions_spawn`, verifica el repo y actualiza estado/evidencia.
- **Dev/Ops/Mind/Studio/Auditor/Critic** no llaman al Planner: devuelven a CORE.

Eso responde a "creí que serías parte integrada": la integración faltante no era una puerta manual, era **una regla de llamada en el CORE**.

---

## 2. RACI

| Actividad | Gonzo | CORE | Planner | Dev/Ops/Mind/Studio | Auditor/Critic |
|---|---|---|---|---|---|
| Definir prioridad y alcance humano | **A** | R | C | I | I |
| Decidir si el objetivo es programa | I | **A/R** | C | I | I |
| Descomponer en pasos, dueños y criterios | I | C | **A/R** | I | I |
| Escribir contratos de ejecución | I | C | **A/R** | I | I |
| Ejecutar el paso | I | **A** | C | **R** | I |
| Verificar el repo | I | **A/R** | C | C | I |
| Emitir veredicto de superficie/sustancia | I | C | C | I | **A/R** |
| Actualizar estado y evidencia | I | **R** | **A** | C | I |
| Re-planear por cambio de alcance | I | C | **A/R** | I | I |
| Cerrar el programa | I | **A** | **R** | I | C |
| Review semanal | I | C | **A/R** | I | I |

**A** = accountable (decide), **R** = responsible (hace), **C** = consulted, **I** = informed.

---

## 3. Quién llama a quién

### Hoy (antes de esta integración)

| Desde | Hacia | Cuándo | Problema |
|---|---|---|---|
| Gonzo | CORE | Siempre | OK |
| CORE | Dev/Ops/Mind/Studio | Según tarea | OK, pero sin plan de programa |
| CORE | Auditor/Critic | Según tarea | OK, pero sin gates de programa |
| CORE | Planner | Casi nunca | Solo dos usos como subagente genérico |
| Planner | Nadie | Nunca | Sin canal ni cadencia |

### Debería ser (Fase 1)

| Desde | Hacia | Cuándo | Regla |
|---|---|---|---|
| Gonzo | CORE | Siempre | Puerta de entrada humana |
| Gonzo | Planner | Opcional | Solo para hablar de planificación; no es el flujo normal |
| CORE | Planner | Inicio de programa | Antes de ejecutar, una vez por programa |
| CORE | Planner | Cambio de alcance | Cuando el plan ya no representa la realidad |
| CORE | Planner | Gate/cierre | Para review y aprendizaje |
| CORE | Dev/Ops/Mind/Studio | Ejecución | Usa el contrato del Planner |
| CORE | Auditor/Critic | Gate | Usa el contrato del Planner |
| Planner | CORE | Siempre | Devuelve plan/brief/contratos; nunca le habla a Gonzo |
| Planner | Dev/Ops/... | **Fase 2** | Solo con `subagents.allowAgents` explícito |
| Dev/Ops/... | Planner | Nunca | Devuelven a CORE |

---

## 4. Dónde se inserta en cada workflow/pipeline

| Punto | Archivo | Hoy | Debería |
|---|---|---|---|
| **Intake** | `AGENTS.md` §3 | No menciona al Planner | Regla dura: programa → CORE llama al Planner antes de ejecutar |
| **Arranque de sesión** | `skills/session-lifecycle/scripts/session-start.sh` | Imprime el plan de sesión del CORE | Además imprime el brief de programas activos del Planner |
| **Complejidad** | `skills/complexity-driven-pipeline/SKILL.md` | Calcula T y decide A/B/C | Si el objetivo es programa, deriva al Planner antes de dividir unidades |
| **Delegación A/B/C** | `skills/agent-orchestration-pipeline/SKILL.md` | El CORE escribe prompts y spawnea | El Planner entrega contratos; el CORE adapta el prompt y spawnea |
| **Estado intra-paso** | `scripts/pipeline-track.sh` | Estado de unidades A/B | Se mantiene: es el estado *dentro* de un paso, no el programa |
| **Plan de sesión** | `scripts/session_plan.py` | Plan de la sesión actual | Se mantiene: es estado de la sesión, no del programa |
| **Cierre de sesión** | `skills/session-lifecycle/scripts/session-end.sh` | Cierra el plan de sesión | Si hubo programa, el CORE actualiza el paso/evidencia antes de cerrar |
| **Cadencia** | `automations` | No hay review del Planner | Lunes plan, viernes review; entrega brief a Gonzo |

### La diferencia clave: tres estados, no uno

| Estado | Dueño | Archivo | Qué responde |
|---|---|---|---|
| Plan de sesión | CORE | `.knowledge/session_plan.json` | "¿En qué estábamos en esta sesión?" |
| Programa | Planner | `agents/kanam-planner/.knowledge/programs/<slug>.json` | "¿Dónde está el objetivo a través de las sesiones?" |
| Pipeline A/B/C | CORE | `pipeline-state.json` | "¿En qué unidad está el paso actual?" |

No se duplican: se anidan. El programa contiene pasos; un paso puede tener un pipeline A/B/C; una sesión ejecuta uno o más pasos.

---

## 5. Secuencia

```text
Gonzo -> CORE: objetivo
CORE: complexity-scorer -> T
CORE: ¿es programa? (3+ pasos, 2+ roles, >1 sesión, fecha/bloqueo)
  |
  +-- no --> CORE ejecuta (T≤12) o pipeline A/B/C (T≥13)
  |
  +-- sí --> CORE -> Planner: spawn(plan)
             Planner -> CORE: programa.json + brief + contratos
             CORE: plan_lint.py + status --json
             loop pasos listos:
               CORE -> Rol: spawn(contrato)
               Rol -> CORE: evidencia
               CORE: verifica repo
               CORE: program_plan.py update (in-progress/completed)
             CORE -> Planner: gate/cierre/review
             Planner -> CORE: veredicto de plan + próximo
             CORE -> Gonzo: síntesis final
```

---

## 6. Reglas duras

1. **Una llamada por programa, no por paso.** Llamar al Planner por cada paso lo convierte en cuello de botella.
2. **El plan nace antes de ejecutar.** Un plan retroactivo es una justificación, no una decisión.
3. **Sin lint verde no se ejecuta.** `plan_lint.py` es el gate.
4. **Sin evidencia no hay `completed`.** El auto-reporte del subagente no es prueba.
5. **El CORE no agrega/borra/reordena pasos.** Si el alcance cambia, vuelve al Planner.
6. **El Planner no spawnea en Fase 1.** El CORE ejecuta. La autonomía de dispatch es Fase 2.
7. **El Planner no le habla a Gonzo.** Devuelve al CORE; el CORE sintetiza.
8. **No se duplica el estado.** Programa, plan de sesión y pipeline son capas, no copias.

---

## 7. Modos de falla

| Falla | Síntoma | Prevención |
|---|---|---|
| Planner llamado tarde | Plan que describe lo ya hecho | Regla de intake en `AGENTS.md` |
| Planner llamado por paso | 10 programas para una feature | Una llamada por programa |
| Planner usado de investigador | Brief sin pasos ni criterios | `planner-delegation` y lint |
| Plan sin dueño | Pasos huérfanos | `plan_lint.py` |
| Plan sin evidencia | `completed` falso | `--evidence` obligatorio |
| Gates salteados | Feature sin Auditor/Critic | `gates` + lint |
| Spawn duplicado | Dos agentes en el mismo paso | `crew_capacity.py` |
| Programa y sesión duplicados | Dos fuentes de verdad | Capas separadas + revisión |
| Planner sin canal | Nunca se usa | CORE delegation + weekly automation |

### Lección 2026-11-06 — Preflight

Un plan del Planner afirmó que Chromium corría con `--no-sandbox` sin leer `src/lib/scan.ts:69`; era falso. El CORE lo cazó. El review también señaló que faltaban quota y cap de concurrencia; eso era cierto en el snapshot que leyó, y el commit `289cb19` los agregó después. La regla es citar **commit + `archivo:línea`**: una afirmación de estado es válida solo para el snapshot que se leyó. Si no, es hipótesis, no plan.

---

## 8. Fases

### Fase 1 (esta implementación)

- Regla de intake en `AGENTS.md`.
- Skill `planner-delegation` en el CORE.
- Programas en JSON + `program_plan.py` + `plan_lint.py`.
- Contratos con `dispatch_contract.py`.
- Brief de programas en `session-start.sh`.
- Automations semanales.
- **El Planner no spawnea.** El CORE ejecuta.

### Fase 2 (si la métrica lo justifica)

- `subagents.allowAgents` en el Planner para dispatch directo.
- Tool nativa `plan` (plugin) para que cualquier agente consulte sin shell.
- Crew Board en dashboard.
- `verdict_ledger.py` y `plan_review` avanzado.

**Condición para Fase 2:** 3+ invocaciones por semana durante 3 semanas y 2 programas activos. Si no se cumple, no se agrega autonomía: se simplifica.

---

## 9. Métrica de éxito

| Métrica | Baseline | Target 30 días |
|---|---|---|
| Invocaciones del Planner por semana | ~0 | 3+ |
| Programas activos | 0 | 2 |
| Pasos con dueño + criterio | 0% | 100% |
| Gates salteados | sin medición | 0 |
| Brief semanal entregado | 0 | 4/4 |
| Bloqueos detectados antes de que los pregunte Gonzo | 0 | 2/mes |

**Criterio de retiro:** menos de 1 invocación por semana después de 30 días con Fase 1 → el rol se fusiona con el CORE o se retira.

---

## 10. Referencias

- `AGENTS.md` §3 — regla de intake.
- `skills/planner-delegation/SKILL.md` — cómo llama el CORE.
- `agents/kanam-planner/CAPABILITIES.md` — catálogo y definición de programa.
- `agents/kanam-planner/skills/program-orchestration/SKILL.md` — cómo piensa el Planner.
- `agents/kanam-planner/skills/crew-dispatch/SKILL.md` — contratos.
- `agents/kanam-planner/skills/plan-review/SKILL.md` — review semanal.
- `skills/complexity-driven-pipeline/SKILL.md` — scorer.
- `skills/agent-orchestration-pipeline/SKILL.md` — pipeline A/B/C.
- `skills/session-lifecycle/SKILL.md` — arranque y cierre.

---

_El Planner no reemplaza al CORE: le da el plano que el CORE hoy dibuja de memoria._
