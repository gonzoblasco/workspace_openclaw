---
name: "planner-delegation"
description: "Como llama el CORE al Crew Planner: cuando un objetivo es un programa multi-sesion, que prompt usar, que entregable exigir y como verificar el plan antes de ejecutar. Usar antes de spawnear agentes para tareas con 3+ pasos, 2+ roles o mas de una sesion."
metadata:
  category: "Core"
  tags:
    - core
    - planner
    - delegation
    - programs
    - orchestration
user-invocable: false
---

# planner-delegation

Esta es la skill del **CORE** para llamar al Planner. No es una skill del Planner: es el contrato de quien lo convoca. El objetivo es que el Planner no sea un agente que hay que abrir a mano, sino una estación de servicio que el CORE usa cuando el trabajo lo justifica.

## Regla de oro

**El CORE llama al Planner una vez por programa, antes de ejecutar. No una vez por paso.**

## Cuándo llamarlo

Llamá al Planner si el objetivo cumple **al menos una** de estas condiciones:

- 3+ pasos secuenciales;
- 2+ roles (Dev, Ops, Mind, Studio, Auditor, Critic);
- más de una sesión;
- una fecha o un bloqueo externo (CI, tercero, deadline);
- complejidad T≥13 con trabajo cruzado entre roles.

## Cuándo NO llamarlo

- Tarea de una sesión y un rol (T≤12): la resuelve el CORE.
- Incidente en producción: primero se estabiliza; el Planner entra después, para el post-mortem.
- Pregunta, investigación o lectura: eso es MIND, no Planner.
- El trabajo ya empezó y solo querés un plan retroactivo: el plan nace antes, no después.
- Cada paso por separado: eso es burocracia y duplica estado.

## Regla de verificación

Antes de proponer pasos, el Planner lee el código y los docs relevantes. **Cada afirmación sobre el estado actual cita `archivo:línea` o se marca como supuesto.** Si no pudo verificar, agrega un paso 0 de verificación; no lo asume hecho. Un plan sobre supuestos no se ejecuta.

Esto vale para el Planner y para el CORE: cuando el CORE revisa el plan, verifica sus propias afirmaciones contra el repo, no contra la memoria.

## Procedimiento

### 1. Scorear

```bash
bash scripts/complexity-scorer.sh "<objetivo>"
```

Guardá el T-score. Si es T≥13 o el objetivo es programa, seguí. Si no, no inventes un programa.

### 2. Spawnear al Planner

```text
sessions_spawn({
  agentId: "kanam-planner",
  context: "isolated",
  task: "<prompt de la sección 3>"
})
```

El Planner corre en su workspace (`agents/kanam-planner`) y escribe el programa en
`agents/kanam-planner/.knowledge/programs/<slug>.json`.

### 3. Prompt mínimo

**No se improvisa el prompt.** Esta plantilla existe porque un prompt en prosa
produce un plan en prosa. Caso testigo (2026-11-06, ABYA YALA): el CORE pidió
*"devolvé el plan como texto estructurado"*, el Planner obedeció, y el
resultado fueron 0 archivos de programa, 0 llamadas a `program_plan.py` y rutas
inventadas. El Planner no falló solo: se le pidió el artefacto equivocado.

Antes de lanzarlo, el CORE **lee el código del proyecto** (no solo los docs) y
lo resume en `Contexto`: dónde viven las estadísticas, qué archivos existen y
cuáles no. Sin eso, el Planner planifica a ciegas y rellena con su plantilla.

```text
[Subagent Task] Programa: <titulo>

Objetivo: <objetivo en una frase>
Contexto: <links, decisiones, restricciones, estado actual>
Alcance: <que entra y que no>
Gates: <auditor, critic o ninguno>

Antes de proponer pasos, leé el código/docs relevantes. Cada afirmación sobre el estado
actual debe citar archivo:línea; si no, marcala como supuesto y agregá un paso de
verificación. No agregues un test que dependa de una implementación que no existe.

Entregable:
1. Crear o actualizar el programa en agents/kanam-planner/.knowledge/programs/<slug>.json.
2. Pasos atomicos con role, owner, exit_criteria, depends_on y gate cuando corresponda.
3. Correr python3 agents/kanam-planner/scripts/plan_lint.py <slug> hasta que de verde.
4. Devolver:
   - slug y path del programa;
   - brief de 10 lineas;
   - proximo paso accionable;
   - contratos de los pasos listos (dispatch_contract.py);
   - riesgos y decisiones que necesitan al CORE.

No ejecutes el trabajo. No spawnees agentes. No escribas codigo ni UI.
```

### 4. Verificar el entregable

No confíes en el auto-reporte. Corré:

```bash
python3 agents/kanam-planner/scripts/plan_lint.py <slug>
python3 agents/kanam-planner/scripts/program_plan.py status <slug> --json
```

Criterios:

- `lint` exit 0.
- Todos los pasos tienen `owner` y `exit_criteria`.
- El próximo paso existe y sus dependencias están completas.
- Los gates declarados tienen un paso de Auditor/Critic.
- Las afirmaciones de estado tienen fuente (`archivo:línea`) o están marcadas como supuesto con un paso de verificación.
- El brief se puede leer sin abrir el JSON.
- **Cada ruta citada existe en el repo, o lleva `NUEVO` al lado.** Verificarlo
  con `ls`/`test -e`, no de memoria. Un plan que menciona `src/data/x.json`
  cuando ese directorio no existe es un plan que va a romper a quien lo ejecute.

Si algo falla, devolvé el plan al Planner. **No ejecutes un plan inválido.**

### 5. Ejecutar el plan

Para cada paso listo:

```bash
python3 agents/kanam-planner/scripts/dispatch_contract.py <slug> <step> --format markdown
```

El contrato trae el prompt y el `agentId`/`model`. El CORE hace el `sessions_spawn`. Después de verificar el resultado:

```bash
python3 agents/kanam-planner/scripts/program_plan.py update <slug> <step> in-progress --session-ref "<session-key>"
python3 agents/kanam-planner/scripts/program_plan.py update <slug> <step> completed --evidence "<evidencia>"
```

**El CORE puede actualizar estado y evidencia. No puede agregar, borrar ni reordenar pasos: eso es del Planner.** Si el alcance cambia, se vuelve a llamar al Planner.

### 6. Gates y cierre

- **Gate Auditor/Critic:** el CORE spawnea al Auditor/Critic con el contrato; el veredicto se registra como evidencia del paso `review`.
- **Cambio de alcance o bloqueo estructural:** el CORE vuelve a llamar al Planner para re-planear, no parchea el plan a mano.
- **Cierre:** cuando todos los pasos están `completed` o `waived`, el CORE pide al Planner el review final y cierra con `program_plan.py close <slug>`.

## Quién llama a quién

| Desde | Hacia | Cuándo | Nota |
|---|---|---|---|
| Gonzo | CORE | Siempre | Puerta de entrada humana |
| Gonzo | Planner | Opcional | Solo si quiere hablar de planificación; no es el flujo normal |
| CORE | Planner | Inicio de programa, cambio de alcance, gate, cierre, weekly | Una vez por programa, no por paso |
| Planner | CORE | Devolución de plan, brief, contratos, riesgos | Nunca le habla a Gonzo directamente |
| CORE | Dev/Ops/Mind/Studio | Ejecución de pasos | Usa el contrato del Planner |
| CORE | Auditor/Critic | Gates | Usa el contrato del Planner |
| Planner | Dev/Ops/... | **Fase 2, no Fase 1** | Requiere `subagents.allowAgents` explícito |
| Dev/Ops/... | Planner | Nunca | Devuelven a CORE, no negocian el plan |

## Anti-patrones

- **Llamar al Planner después de empezar.** El plan se vuelve una justificación, no una decisión.
- **Llamarlo por cada paso.** Duplica estado y convierte al Planner en cuello de botella.
- **Usarlo de investigador o redactor.** Para eso están MIND y STUDIO.
- **Aceptar un plan sin lint.** Un plan sin dueño o criterio de salida no es un plan.
- **Dejar que el Planner spawnee sin allowlist.** En Fase 1 no spawnea; en Fase 2 se habilita con config explícita.
- **Actualizar el plan a mano sin pasar por el script.** Rompe la fuente única.

## Ejemplo bueno

> Objetivo: "Implementar el chat RAG de onwheels con citas verificables."
> T=16, 6 pasos, roles Dev + Critic + Auditor + CORE, dos sesiones.
> CORE llama al Planner → plan con 6 pasos, gates y contratos → CORE ejecuta → Planner revisa en el gate y en el cierre.

## Ejemplo malo

> Objetivo: "Arreglar el typo del botón."
> T=3, un archivo, un rol.
> Llamar al Planner sería burocracia. Lo hace el CORE.

## Referencias

- `agents/kanam-planner/CAPABILITIES.md` — definición de programa y catálogo.
- `agents/kanam-planner/skills/program-orchestration/SKILL.md` — cómo piensa el Planner.
- `agents/kanam-planner/skills/crew-dispatch/SKILL.md` — contratos de ejecución.
- `docs/PLANNER-INTEGRATION.md` — RACI y puntos de inserción en los pipelines.
- `skills/complexity-driven-pipeline/SKILL.md` — scorer y buckets.

---

_El CORE no abre al Planner: lo convoca. La diferencia es el contrato._
