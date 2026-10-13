# ADR-093: El plan de sesión como objeto persistente (session-planning-hooks se cablea)

**Fecha:** 2026-10-06
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** sesión 2026-10-06 - Gonzo: *"El camino de madurez del sistema (Kanam OS, por etapas)" -> "arranquemos"*. Cierra el hueco declarado en `docs/NORTH.md`: la Etapa 2 tenía cinco gates que existían y nadie invocaba.
**Relacionado:** ADR-055 (bloques managed desde la DB), ADR-056 (guardas de gobernanza en el pre-commit), ADR-083 (frontera de roles + enforcement), ADR-092 (rotación del CHANGELOG)

---

## Contexto

La Etapa 2 de Kanam OS ("El Ritmo: ciclos de vida y gates") estaba clasificada como 🟡 **parcial**: cinco specs documentaban implementaciones vivas que **nada invocaba**. El commit `44d9bc779b` (2026-10-06) cableó `security-scan` al pre-commit y **clasificó honestamente** los otros cuatro:

| Gate | Estado tras `44d9bc779b` |
|---|---|
| `security-scan` | ✅ ADOPTADO (pre-commit, `--staged`) |
| `session-planning-hooks` | 🟡 **PARCIAL** - el `AGENTS.md` del planner lo referencia; **no hay hook** |
| `skill-evals` | 🧪 EXPERIMENTO no adoptado |
| `lifecycle-tracker` | 🧪 EXPERIMENTO no adoptado |
| `regression-control` | 🧪 EXPERIMENTO no adoptado |

De los cuatro pendientes, **`session-planning-hooks` es el único que resuelve un problema real y barato de cerrar.** Los otros tres (evals, lifecycle, regression) son burocracia sin dueño: su valor exige rúbrica SHARP medida y una cadencia que hoy nadie sostiene. El plan de sesión, en cambio, ataca una pérdida concreta y ya diagnosticada.

El problema es la **amnesia de sesión**: el `AGENTS.md` del planner dice, textualmente, *"Prohibida la amnesia de sesión: nunca empezar un turno sin leer el `.session_plan.json` actual"* - y **nada lo garantizaba**. La planificación vivía solo en el hilo del chat. Un reinicio del Gateway, un cambio de contexto o un cierre la borraban. El script `scripts/session_plan.py` existía pero:

1. Tenía el path **clavado** a `/Users/gonzoblasco/...` (no portable, no testeable);
2. Vivía en la **raíz** del workspace (`.session_plan.json`, un archivo suelto y tracked);
3. **Nadie lo invocaba** - ni arranque ni cierre.

## Decisión

**El plan de sesión pasa a ser un objeto persistente del sistema: `session_plan.py` lo escribe, el arranque lo lee, el cierre lo archiva.**

1. **Estado durable en `.knowledge/`.** El plan vive en `<workspace>/.knowledge/session_plan.json`, junto al resto del estado del workspace (`HANDOFF.md`, `SHARP.md`, `entities/`). El path se **deriva del script** (portable) y es sobrescribible con `SESSION_PLAN_PATH` para tests/aislamiento. Se retira el `.session_plan.json` de la raíz.

2. **Hook de arranque (`session-start.sh`).** Si hay un plan activo, imprime `session_plan.py summary` **antes** de scorear complejidad y buscar memoria: *"retomando: estábamos en el paso X"*. Elimina la necesidad de preguntar *"¿en qué estábamos?"*. Idempotente y silencioso si no hay plan.

3. **Hook de cierre (`session-end.sh`).** Llama a `session_plan.py close`: marca el plan `completed` y lo **archiva** en `.knowledge/archive/session_plan_<id>.json`. El cierre de sesión queda atado al plan, y el historial de intenciones sobrevive.

4. **`close` es defensivo e idempotente.** Sale 0 **siempre** (sin plan, ya cerrado, o cerrado dos veces): el `session-end.sh` corre bajo `set -e`, y un exit != 0 abortaría el cierre completo. Es una regla dura del diseño, cubierta por test.

5. **La deuda adyacente del mismo archivo se corrige de paso.** `session-start.sh` resolvía el HANDOFF en `projects/$PROJECT/.knowledge/` - la estructura **pre-ADR-075**, muerta desde 2026-09-26. Se alinea con `scripts/session-handoff.py` (workspace -> `.knowledge/` propio; proyecto -> `<workspace>/projects/<slug>/.knowledge/`, ADR-098).

### Qué NO se adopta (y por qué, escrito)

Los tres experimentos restantes **se quedan clasificados como experimentos no adoptados**. No es un descarte: es una decisión con criterio.

- **skill-evals / lifecycle-tracker:** exigen un `.eval.yaml` por skill sobre un runner que ejecuta la skill por CLI. Hoy **no hay skills con evals** (solo un fixture en `sandbox/`) y el runner es un stub. Adoptarlos sería crear un gate que no puede juzgar nada.
- **regression-control:** compara puntajes SHARP contra un baseline (`.knowledge/quality_baseline.json`) que **no existe** y que nadie mide. Sin rúbrica con puntaje observado, el gate es una caja vacía.

Se conservan sus specs con su estado real. Si el frente "ciclo de vida de skills" se retoma, ahí está el punto de partida.

## Consecuencias

- **Positivas:** la amnesia de sesión deja de depender de la disciplina. El plan sobrevive reinicios y es verificable (arranque lo lee, cierre lo archiva). El `AGENTS.md` del planner deja de prometer algo que nadie garantizaba.
- **Positivas (método):** el hueco se cierra con **la misma medicina que el resto del sistema**: script portable + hook + test + doc. Una regla sin enforcement se viola sola (ADR-083); esto es enforcement.
- **Coste:** dos líneas de hook en `session-start.sh`/`session-end.sh` y un test. Marginal.
- **Deuda declarada:** los tres experimentos siguen sin dueño y sin cadencia. **No se cablean hasta que exista lo que miden** (evals escritos, baseline SHARP medido). Queda anotado en `docs/NORTH.md`.
- **Riesgo de mal uso:** que el plan se convierta en burocracia (inicializar un plan por cada tarea trivial). El criterio es el mismo del `progress_card`: **solo trabajo sustancial con pasos secuenciales**. El scorer de complejidad (T-score) es la guía natural.

## Alternativas consideradas

1. **Adoptar los cinco gates de una.** Rechazada: tres no tienen qué medir. Adoptar un gate vacío es peor que no tenerlo - da falso verde.
2. **Dejar `session-planning-hooks` como experimento.** Rechazada: el problema (amnesia de sesión) es real, barato de cerrar, y el `AGENTS.md` del planner ya lo prometía.
3. **Guardar el plan en la DB (`memory.db`).** Rechazada por ahora: el plan es estado del **workspace** (como el HANDOFF), no memoria consultable. La DB es para lo que `memory_search` indexa; el plan es para el arranque. Coherente con ADR-065 (DB-first vs doc-only: cada dato donde se consume).
