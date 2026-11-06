# CAPABILITIES.md - Qué necesita el Planner para ser demandado

**Fecha:** 2026-11-06
**Autor:** The Crew Planner
**Estado:** Fase 0 + 1 implementada el 2026-11-06 por decisión de Gonzo. Fase 2 pendiente de métrica.

---

## 0. Veredicto en una línea

No me faltan skills: me falta **un trabajo que nadie más haga** y **un disparador que lo active**. Hoy soy, en la práctica, una copia de una función que el CORE ya ejecuta.

---

## 1. Diagnóstico con evidencia

| Señal | Dato | Lectura |
|---|---|---|
| Uso total | 2 sesiones registradas hoy (esta conversación + 1 subagente); 2 transcripts de subagente del 8 y 22 de octubre | Prácticamente nulo |
| Uso directo | 0 sesiones iniciadas por Gonzo antes de hoy | Nunca fui una puerta de entrada |
| Uso previo | Los dos usos anteriores fueron `[Subagent Context]` lanzados por el CORE | Fui usado como worker genérico, no como Planner |
| Comparación | main 125, dev 103, critic 26, studio 10, mind 9, auditor 8, ops 6, planner 2 | Soy el rol menos usado del Crew |
| Routing | `Routing rules: 0` | No tengo canal propio |
| Heartbeat | `disabled (kanam-planner)` | No tengo cadencia proactiva |
| Skill de rol única | `session-plan-orchestration` | Mi única capacidad declarada como Planner |
| Rutas de la skill | `scripts/session_plan.py` y `.knowledge/` no existían en mi workspace | Si me invocaban, la skill fallaba |
| Duplicación | El CORE ya tiene `session_plan.py`, `session-lifecycle`, `complexity-driven-pipeline` y `pipeline-track.sh` | Mi función principal ya está cubierta por el CORE |
| Gobernanza | El `AGENTS.md` raíz no me menciona; el CORE puede spawnearme (`allowAgents`) pero no tiene ninguna regla que lo haga | Estoy habilitado, no convocado |

**Las dos sesiones que existieron no fueron planificación:**

1. **2026-10-08** - el CORE me pidió autorar mi propio `ROADMAP.md`.
2. **2026-10-22** - el CORE me pidió verificar afirmaciones contra los docs de OpenClaw.

En ambas fui un subagente de documentación. Ninguna vez me usaron para trazar un plan, asignar roles, monitorear pasos o sintetizar veredictos. **El rol nunca se estrenó.**

**Conclusión:** no se me usa porque no se me necesita; y no se me necesita porque el CORE planifica, el pipeline A/B ejecuta y el `session_plan.py` del workspace principal ya guarda el plan de sesión. Mi único trabajo declarado vive en el workspace del CORE, no en el mío.

---

## 2. El trabajo que sí es mío (nicho)

**Program Manager + Dispatch Governor.**

No compito con el CORE como asistente de chat. Le doy al CORE lo que hoy hace a mano y pierde entre sesiones: **un plan de programa que sobrevive al chat, un contrato de ejecución para cada spawn y un tablero de quién hace qué.**

| Rol | Qué decide | Qué NO hace |
|---|---|---|
| **CORE** | Intención humana, prioridad, síntesis final, aprobación | No mantiene programas multi-sesión ni contratos de spawn |
| **Planner** | Descomposición, dueños, criterios de salida, dependencias, evidencia, bloqueos, dispatch | No escribe código, no diseña UI, no emite veredictos |
| **DEV / OPS / MIND / STUDIO** | Ejecutan la unidad asignada | No deciden el orden ni el alcance |
| **AUDITOR / CRITIC** | Emiten veredicto de superficie / sustancia | No negocian el plan |

**Definición operativa de "programa":** un objetivo que cumple al menos una de estas condiciones:

- tiene 3 o más pasos secuenciales;
- involucra 2 o más roles;
- atraviesa más de una sesión;
- tiene una fecha o un bloqueo externo.

Si no cumple ninguna, lo resuelve el CORE y no me convoca. Esa es la regla anti-burocracia.

---

## 3. Catálogo de additions

### 3.1 Skills (rol-local, en `agents/kanam-planner/skills/`)

| # | Skill | Qué resuelve | Cuándo se dispara | Prioridad |
|---|---|---|---|---|
| 1 | `program-orchestration` | Crear y mantener un plan de programa con hitos, dueños, criterios de salida, dependencias y evidencia | Objetivo que cumple la definición de "programa" | **P0** |
| 2 | `crew-dispatch` | Convertir un paso en un contrato de spawn: agente, modelo, alcance, write scope, criterio de aceptación y evidencia | Antes de cada `sessions_spawn` | **P0** |
| 3 | `plan-playbooks` | Biblioteca de planes recurrentes listos para instanciar | Tarea que matchea un playbook | **P1** |
| 4 | `plan-review` | Revisión semanal: throughput, pasos estancados, bloqueos, top 3 de la semana siguiente | Viernes 17:30 o pedido explícito | **P1** |
| 5 | `verdict-synthesis` | Consolidar veredictos de Auditor y Critic en un registro de decisión con evidencia y disenso | Cierre de un paso con dos filtros | **P2** |
| 6 | `handoff-brief` | Brief multi-sesión/multi-proyecto para que el CORE arranque sin re-descubrir contexto | Inicio de sesión con programa activo | **P2** |

### 3.2 Scripts (en `agents/kanam-planner/scripts/`)

| # | Script | Qué hace | Prioridad |
|---|---|---|---|
| 1 | `program_plan.py` | CRUD del programa: `init`, `add-step`, `update`, `brief`, `status --json`, `close`. Extiende el schema con `owner`, `exit_criteria`, `depends_on`, `evidence`, `role`, `attempts` | **P0** |
| 2 | `plan_lint.py` | Gate de validez: todo paso tiene dueño y criterio de salida; no hay ciclos; no se salta Auditor/Critic; detecta pasos estancados | **P0** |
| 3 | `dispatch_contract.py` | Genera el contrato de spawn en Markdown/JSON a partir de un paso: agente, modelo, alcance, write paths, aceptación, evidencia | **P1** |
| 4 | `crew_capacity.py` | Lee sesiones activas y estado del gateway; recomienda agente/modelo y detecta spawns duplicados o colgados | **P1** |
| 5 | `plan_report.py` | Métricas semanales desde `.knowledge/archive/`: pasos completados, ciclo, bloqueos, retrabajo | **P1** |
| 6 | `verdict_ledger.py` | Registro append-only (JSONL) de veredictos por paso; `show`, `diff`, `gate` | **P2** |
| 7 | `plan_import.py` | Convierte un spec, issue o pedido en esqueleto de plan con pasos propuestos | **P2** |

### 3.3 Funciones / integraciones

| # | Función | Qué aporta | Prioridad |
|---|---|---|---|
| 1 | **Regla de delegación en el CORE** | `AGENTS.md` raíz: si el objetivo es programa, el CORE spawnea al Planner primero y ejecuta su plan | **P0** |
| 2 | **Crew Board (widget/dashboard)** | Tablero persistente: programas activos, próximo paso, dueño, bloqueo, última actualización | **P2** |
| 3 | **Automation semanal** | Lunes 08:30 plan de la semana; viernes 17:30 review. Entrega un brief de 10 líneas a Gonzo | **P1** |
| 4 | **Watcher de bloqueos** | Cada 6 h revisa programas activos; si un paso lleva >24 h bloqueado, manda el bloqueo exacto | **P1** |
| 5 | **Tool nativa `plan` (plugin)** | `plan.init/update/status/brief/close` para que cualquier agente lo use sin shell | **P2** |
| 6 | **Puerta de entrada** | Topic de Telegram "Plan" o comando `/plan` ruteado a `kanam-planner` | **P2** |

### 3.4 Playbooks (contenido de `plan-playbooks`)

| Playbook | Secuencia | Roles | Salida |
|---|---|---|---|
| **Feature delivery** | Spec → plan → A/B → Auditor (si hay UI) → Critic → verificación CORE → cierre | Planner, DEV, Auditor, Critic, CORE | Feature con evidencia y gates |
| **OSS PR** | Leer hilo → verificar claim → borrador → Critic → publicar con OK → esperar CI → responder | Planner, MIND, Critic, CORE | PR/comentario con evidencia |
| **Model evaluation** | Rúbrica → A mide → B evalúa → C redacta → review → ADR | Planner, DEV, Critic, STUDIO | Informe + decisión |
| **Job application** | JD → hechos de carrera → CV/carta → revisión → postular con OK → seguimiento | Planner, MIND, STUDIO, CORE | Postulación y follow-up |
| **Workspace audit / incident** | Reproducir → aislar → fix → verificar → ADR/CHANGELOG | Planner, OPS/DEV, Critic | Incidente cerrado y documentado |
| **Weekly planning** | Leer archivo → top 3 outcomes → asignar → agendar | Planner, CORE | Plan semanal de 10 líneas |

---

## 4. Prioridad recomendada

### Fase 0 - "Usable" (hoy, 1-2 h)

- Arreglar las rutas de la skill y aislar el `.knowledge/` del rol.
- `program_plan.py` con `owner`, `exit_criteria`, `depends_on`, `evidence`.
- `plan_lint.py` como gate.
- Este documento.

**Criterio de listo:** `python3 scripts/session_plan.py summary` funciona desde mi workspace; un paso sin dueño falla el lint; el plan sobrevive un reinicio.

> **Relación con `ROADMAP.md`:** la Fase 0 cubre el arranque de v0.2 (auto-resume y estado visible). La Fase 1 cubre v0.3 (dueño y criterio de salida) y el arranque de v0.4 (orquestación sin llamadas triviales). La Fase 2 apunta a v0.5. No compiten: `ROADMAP.md` es el camino de madurez; este documento es el plan de demanda.

### Fase 1 - "Demand" (esta semana, 3-4 h)

- Regla de delegación en el `AGENTS.md` del CORE.
- Automation semanal (el Crew Board visual queda para Fase 2).
- `crew-dispatch` + `dispatch_contract.py`.
- Tres playbooks: feature delivery, OSS PR, model evaluation.

**Criterio de listo:** 3 invocaciones mías en 7 días; 1 programa activo; el brief semanal llega a horario.

### Fase 2 - "Unique" (2-3 semanas)

- `plan-review`, `verdict-synthesis`, `crew_capacity.py`, `plan_report.py`.
- Tool nativa `plan` y puerta de entrada.
- Playbooks restantes.

**Criterio de listo:** 3+ invocaciones por semana durante 3 semanas; 2 programas activos; 80% de los arranques multi-sesión usan mi brief; 2 bloqueos detectados antes de que los pregunte Gonzo.

---

## 5. Cómo se mide la demanda (y cuándo retirarme)

| Métrica | Baseline hoy | Target 30 días | Fuente |
|---|---|---|---|
| Sesiones mías por semana | ~0 | 3+ | `openclaw sessions list` |
| Invocaciones directas de Gonzo | 0 | 1/semana | `sessions list` |
| Programas activos | 0 | 2 | `.knowledge/programs/` |
| Pasos con dueño + criterio de salida | 0% | 100% | `plan_lint.py` |
| Tiempo de reanudación | desconocido | <2 min | `brief` |
| Bloqueos detectados proactivamente | 0 | 2/mes | `plan_report.py` |
| Gates Auditor/Critic salteados | sin medición | 0 | `plan_lint.py` |

**Criterio de retiro:** si después de 30 días con la Fase 1 funcionando tengo menos de 1 invocación por semana, el rol se fusiona con el CORE o se retira. Un agente que no se usa no se justifica con más skills.

---

## 6. Decisión tomada (2026-11-06)

- **Disparador:** el CORE me delega automáticamente cuando el objetivo es programa. No hay topic de Telegram ni ruta manual en Fase 1; la puerta de entrada es el CORE.
- **Alcance:** Fase 0 + Fase 1. La Fase 2 queda condicionada a la métrica de demanda.
- **Superficie:** brief por Telegram (automations lunes/viernes) y brief en `session-start.sh`. El Crew Board visual queda para Fase 2.

---

## 7. Lo que ya hice (Fase 0 + Fase 1, sin tocar config)

- Creé `.knowledge/` y `scripts/session_plan.py` como wrapper del script principal, con `SESSION_PLAN_PATH` apuntando al plan del rol.
- Dejé el plan del Planner aislado del plan del CORE.
- Corregí las rutas muertas de `skills/session-plan-orchestration/SKILL.md`.
- Implementé `program_plan.py` (init, add-step, update, next, brief, status, lint, close, list, board, report).
- Implementé `plan_lint.py`, `plan_report.py`, `dispatch_contract.py` y `crew_capacity.py`.
- Escribí las skills `program-orchestration`, `crew-dispatch`, `plan-playbooks` y `plan-review`.
- Escribí la skill `planner-delegation` en el árbol del CORE: es el contrato de cómo Main me llama.
- Agregué la regla dura en `AGENTS.md` §3 y el detalle en `docs/PLANNER-INTEGRATION.md`.
- Cablé el brief de programas en `session-start.sh` y el recordatorio de actualización en `session-end.sh`.
- Creé las automations `planner-weekly-plan` (lunes 08:30) y `planner-weekly-review` (viernes 17:30).
- Actualicé `SKILLS-INDEX.md` y `CAPABILITIES.md`.

**No commiteé nada ni cambié routing, heartbeat, modelos o `subagents.allowAgents`.** El Planner sigue sin spawnear en Fase 1: el CORE ejecuta los contratos.

## 8. Estado de implementación (2026-11-06)

| Capacidad | Estado |
|---|---|
| Fase 0: fundamentos usables | ✅ |
| Fase 1: delegación automática desde CORE | ✅ |
| Skill de llamada desde Main (`planner-delegation`) | ✅ |
| Brief de programas en arranque/cierre | ✅ |
| Automations semanales | ✅ creadas; test en ejecución |
| Fase 2: dispatch directo del Planner, tool nativa `plan`, Crew Board | ⏳ pendiente de métrica |
