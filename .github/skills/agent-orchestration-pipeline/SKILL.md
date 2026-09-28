---
name: "agent-orchestration-pipeline"
description: "Orquestar agentes A/B en cadena con cross-review multi-ronda, usando Claude Code (estandar, ADR-049) o Qwen Code (fallback) via Ollama, con modelo dinamico."
---

# Agent Orchestration Pipeline

Orquestar multiples agentes implementadores con revision cruzada multi-ronda, coordinados por un agente orquestador, para desarrollar unidades atomicas con gates de calidad en cada etapa.

> **ESTANDAR DE TRABAJO (ADR-049, 2026-09-15):** la forma de programar de ahora en mas es este pipeline con **Claude Code (embebido en Claude Desktop 3p, >= 2.x) como el motor de los agentes A/B**, apuntando al gateway Ollama con el modelo dinamico. **Qwen Code queda como fallback o segundo par de ojos, no como estandar.** Kanam (orquestador) redacta las tareas, encadena los outputs (pasa el codigo de A a B), verifica y reporta. El desarrollador no escribe prompts de agentes - solo da la meta.

## Motor: Claude Code via Ollama (estandar, ADR-049)

Los agentes implementadores son instancias de **Claude Code** lanzadas por el orquestador, apuntando al gateway Ollama y usando los modelos locales/cloud de Ollama. Esto da acceso a los modelos sin APIs externas de pago.

### Comando base (headless)
```bash
# Camino recomendado (verificado 2026-09-22): levanta el gateway y resuelve el enmascarado solo
ollama launch claude --model <tag> -- -p "<tarea>"

# Alternativa directa
ANTHROPIC_BASE_URL=http://127.0.0.1:11434 \  # o 11435 (gateway, para aliases)
ANTHROPIC_AUTH_TOKEN=<cualquier-valor> \
claude -p "<tarea>" --model <tag o alias> \
  --dangerously-skip-permissions
```
- **`claude` esta en el PATH (2026-09-22):** instalado global (`/opt/homebrew/bin/claude`, 2.1.280). El embebido de Claude Desktop 3p sigue como respaldo.
- **Aliases vs tags crudos:** los aliases (`claude-sonnet-5`) los resuelve el gateway `11435` (requiere Claude Desktop corriendo); contra el daemon `11434` fallan - ahi va el tag crudo (`deepseek-v4.1-flash:cloud`). `ollama launch claude` evita tener que elegir.
- **Config persistente:** `~/.claude/settings.json` acepta un bloque `env` con `ANTHROPIC_BASE_URL` + `ANTHROPIC_AUTH_TOKEN` + `CLAUDE_CODE_MAX_CONTEXT_TOKENS`; no hace falta exportar en el shell. Un install global NO hereda la config del 3p.
- `-p` = headless; `--dangerously-skip-permissions` = auto-aprueba tools (write, edit, shell) sin prompt.
- Modelo: cualquiera de `ollama list`, elegido por tarea (ADR-040).
- El prompt (`-p`) lo redacta el ORQUESTADOR (Kanam), no el desarrollador.

**Requisitos Claude Code:** >= 2.x (la 0.2.18 no maneja el bloque `{type:thinking}`), `~/.claude/settings.json` con `permissions.allow` (Edit, Write, Bash, Read), y tolerar los warnings `unrecognized_model` (ruido, no bloquean).

### Flujo en CADENA (no paralelo) - validado
A escribe → [orquestador pasa el output/codigo de A como contexto a B] → B revisa y corrige → [orquestador verifica] → A revisa el fix de B → ... hasta aprobar.

Ejemplo validado: A escribio `sumar()` (bug latente: concatena strings) → B reviso el codigo de A (pasado como contexto) y lo corrigio a `Number(a)+Number(b)` → orquestador verifico. Iterable indefinidamente.

### Aislamiento entre agentes
- Cada agente trabaja en su propia carpeta/directorio (no se pisan).
- El orquestador pasa el estado (archivo/codigo) de un agente a otro como contexto en el prompt.
- Dos instancias paralelas funcionan, PERO el flujo de trabajo estandar es EN CADENA (dependencia de orden: B necesita el output de A).

### Motor alternativo: Qwen Code via Ollama (fallback, no estandar)

Qwen Code queda como **fallback o segundo par de ojos** (ADR-049), no como estandar. Comando:
```bash
ollama launch qwen --model <modelo> -- -p "<tarea>" -y
```
OJO: SIGKILL en tareas largas (~3 min). Claude Code maneja mejor las sesiones largas y es el recomendado.

### Limitaciones
- **OpenCode:** no instalado por defecto. Requiere instalacion si se quiere usar.
- **Claude Code es el motor estandar** (ADR-049) por su mejor manejo de sesiones largas y ser el camino que ya usan los ciclos reales. Qwen Code queda como recurso para un segundo par de ojos con distinta implementacion de edicion.

### Verificacion del orquestador
El orquestador NO solo lanza y lee output: verifica el resultado real (leer archivos creados/editados, correr build/tests/lint) antes de pasar a la siguiente etapa.

---

## Cuando usar

- El trabajo es lo suficientemente grande para dividirse en unidades atomicas (features, slices, bugs) que puedan desarrollarse de forma paralela o secuencial.
- Se quiere calidad alta con revision independiente (no solo self-review del autor).
- Hay 2+ agentes implementadores disponibles (Qwen Code via Ollama) con un orquestador que coordina.
- Se prioriza la correccion de bugs por ojos frescos sobre la velocidad de un solo agente.

## Roles

### Orquestador (Kanam / agente principal)
- Planifica y divide el spec en unidades atomicas (U1, U2, ...) con criterios de aceptacion.
- **Redacta los prompts/tareas** para los agentes (el desarrollador no escribe prompts de agentes - solo da la meta).
- Asigna unidades a los agentes (paridad: A = impares, B = pares) y **encadena los outputs** (pasa el codigo de A a B como contexto).
- **Verifica el resultado real** de cada agente (leer archivos, correr build/tests/lint) antes de avanzar.
- Define las reglas del pipeline y el flujo de revision cruzada.
- Coordina el cierre (release, changelog, tag).
- Documenta el plan en un archivo dedicado (ej. `PLAN-FASE-X.md`) + STATUS + ROADMAP.
- NO desarrolla unidades de los agentes (salvo tareas de orquestacion como tests de infra, refactors, o cuando el orquestador asume una unidad directamente).

### Agentes implementadores (A, B, C, ...)
- **Son instancias de Claude Code lanzadas por el orquestador** apuntando al gateway Ollama (`claude -p "<tarea>" --model <modelo>` headless, ver ADR-049).
- Cada uno trabaja en su propia carpeta/directorio (aislamiento).
- Desarrollan su unidad asignada (commit atomico + push).
- REVISAN la unidad que el agente anterior acaba de completar (cross-review), antes de empezar la suya.
- Corrigen bugs de la unidad revisada si los encuentran (el orquestador les pasa el codigo como contexto).
- Dejan mensaje claro de que hicieron y que necesita revision.

## Reglas de oro

1. **Cada unidad = commit atomico + push.** Nada de commits monoliticos que mezclan features.
2. **Nadie avanza sin que el otro valide.** El pipeline es en cadena: cada agente revisa lo anterior antes de seguir.
3. **Revision cruzada multi-ronda.** Para calidad alta, el codigo puede pasar por varias rondas: orquestador implementa → A revisa/corrige → B re-revisa las correcciones de A → (opcional) rondas adicionales. Cada ronda tiene ojos frescos.
4. **Criterios de aceptacion explicitos por unidad.** El orquestador los define en el plan; el agente los verifica al cerrar.
5. **Verificacion obligatoria:** build + tests + lint verdes antes de commitear. El agente los corre y reporta.
6. **No romper invariantes del sistema** (modelo de aceptacion del chat, arquitectura, ADRs). Si una correccion los tocaria, el agente lo senala en vez de romperlos.
7. **Paridad A/B:** A desarrolla unidades impares, B pares. Cada uno revisa la del otro. (Configurable segun cantidad de agentes.)
8. **Docs al dia:** al cerrar cada unidad, actualizar PLAN/STATUS/ROADMAP y commitear los docs al workspace.

## Flujo (pipeline en cadena)

```
Orquestador: planificar + dividir en unidades + asignar paridad
   ↓
Agente A: desarrolla U1 + push
   ↓
Agente B: REVISA U1 + desarrolla U2 + push
   ↓
Agente A: REVISA U2 + desarrolla U3 + push
   ↓
Agente B: REVISA U3 + desarrolla U4 + push
   ↓
... (se alterna hasta la ultima unidad)
   ↓
Cierre: A y B revisan el conjunto + orquestador hace release
```

**Revision multi-ronda (para calidad maxima):**
```
Orquestador implementa (opcional) → Agente A revisa/corrige → Agente B re-revisa las correcciones de A → (rondas extra si se requiere) → aprobado
```

## Seleccion de modelo por tarea (model-router.sh)

El pipeline usa un router de modelo configurable por tipo de tarea + overrides sticky, portado del concepto ToggleLogic (ClawHub) SIN su licencia patentada. En vez de elegir el modelo manualmente cada vez, se consulta la ruta del tipo de tarea:

```bash
./scripts/model-router.sh model <tipo>   # code/review/long/cheap/writing/default
./scripts/model-router.sh set <tipo> <model>   # override sticky (persiste)
./scripts/model-router.sh reset <tipo>         # limpiar override
./scripts/model-router.sh default <model>      # cambiar default
./scripts/model-router.sh list                 # ver rutas + overrides
```

**Rutas por defecto (2026-08-30):** code → deepseek-v4-flash, review → deepseek-v4-flash, long → glm-5.3-flash, cheap → gemma4, writing → glm-5.3-flash, pipeline_ab → gpt-oss:120b-cloud / deepseek-v4.1-flash:cloud, default → deepseek-v4-flash.

**Division de modelos A/B (2026-09-28, pedido de Gonzo):** en `pipeline_ab`, el **Agente A (ejecutor) usa un modelo liviano** (`gpt-oss:120b-cloud`) y el **Agente B (evaluador y corrector) usa uno grande con context window amplia** (`deepseek-v4.1-flash:cloud`, 1M de contexto).

**Por que asimetrico:** A produce, B revisa. Darle a B el modelo mas grande y de mayor contexto le permite **expandirse y ver el contexto completo** - el codigo de A, el repo, las reglas - y asi corregir con fundamento en lugar de opinar sobre un fragmento. A no necesita esa profundidad: necesita velocidad y costo bajo para producir el primer borrador. La asimetria es intencional: **el revisor ve mas que el ejecutor**.

> Medido el 2026-09-28: un review hecho con el mismo modelo que ejecuto no fue un "otro ojo". Con A y B distintos, el review adversarial del gate de verificacion encontro 3 evasiones reales que la suite del propio autor no cubria.

**Uso en el pipeline:** al lanzar un agente, el orquestador consulta `model-router.sh model <tipo>` para decidir el `--model` (en vez de elegirlo ad hoc). Los overrides sticky permiten fijar " usá kimi para todo el codigo de esta fase" y persiste hasta reset.

**Nota:** el router es una sugerencia de modelo; el orquestador puede sobreescribir si la tarea lo justifica (es una decision de Kanam, no del router).

## Templates de prompt para agentes

### Estado durable del pipeline + crash recovery (pipeline-track.sh)

El pipeline usa un tracker de estado durable para sobrevivir a crashes (SIGKILL de Qwen), restarts y eviction de contexto. Portado del concepto Pipeline Architect (ClawHub).

```bash
# Inicializar el plan de la fase con unidades
./scripts/pipeline-track.sh init "Fase 3 - editor" U1 U2 U3 U4 U5 U6

# Marcar el estado de cada unidad
./scripts/pipeline-track.sh start U3    # agente empezo U3
./scripts/pipeline-track.sh review U2   # U2 en cross-review
./scripts/pipeline-track.sh done U1     # U1 completa
./scripts/pipeline-track.sh note U2 "B encontro bug en U1, corregido"

# Ver estado y que falta (tras crash/SIGKILL)
./scripts/pipeline-track.sh status
./scripts/pipeline-track.sh resume      # unidades no-done (para relanzar)
```

**Flujo de crash recovery:** si un agente muere (SIGKILL) a mitad de una unidad, el orquestador corre `pipeline-track.sh resume` para ver que quedo pendiente, verifica el trabajo parcial real (archivos/build/tests), y relanza el agente con un prompt corto para la unidad que quedo en `running` o `queued`. El estado vive en `pipeline-state.json` (o $PIPELINE_STATE_FILE), durable entre sesiones.

**Nota sobre el estado:** el tracker es una sugerencia del orquestador, no una autoridad - Kanam decide que relanzar basandose en el estado + la verificacion real del trabajo (no confiar solo en el estado JSON).

### Detector de riesgos en el cross-review

Antes de pasar el codigo de un agente al siguiente para revision, el orquestador puede correr el detector de riesgo de PRs para darle al revisor senales de que mirar con lupa:

```bash
./scripts/github-pr-risk.sh <owner/repo> <pr-number>
```

Salida (markdown):
- **Risk signals** detectados por paths del PR (schema/migraciones, auth, secrets/config, API publica, dependencias, PR grande) + hints del titulo (breaking, hotfix, refactor).
- **Preguntas de review sugeridas** dirigidas por esos riesgos (adaptadas de la funcion `buildReviewQuestions` del plugin github-workflow de chris-openclaw, portada a gh CLI + jq).

Si el cambio es local (sin PR), Kanam aplica las mismas heurisiscas manualmente sobre los paths del diff. El objetivo es darle al Agente B (revisor) las senales de riesgo antes de que revise, no confiar en que las descubra solo.

La logica del detector esta portada del plugin (ver `sandbox/github-workflow/` para el analisis original). Uso bajo demanda, no en el batch del dashboard - el dashboard es una vista rapida; el risk es para el review puntual de un PR.

Cada prompt de agente sigue esta estructura:

```
Estas trabajando en <proyecto>, <fase>. Sos el Agente <X> (<entorno>). Tu rol en el pipeline de revision cruzada: REVISAR la <unidad> que acaba de completar <otro agente> y DESARROLLAR la <unidad siguiente>.

## Contexto del pipeline
<como funciona el pipeline, paridad, revision en cadena>

## Estado actual del repo
<lista de commits por unidad, con el hash>

## Tu tarea - Parte 1: REVISAR la <unidad> de <agente>
<descripcion de la unidad + checklist de verificacion (build, tests, lint, edge cases, invariantes)>
<Si encontran bugs, corregilos (commit atomico). Si esta correcta, dejala.>

## Tu tarea - Parte 2: DESARROLLAR la <unidad>
<descripcion + criterios de aceptacion>

## Reglas
<commit atomico, idioma (commits en ingles, UI en espanol), no romper invariantes, actualizar docs>

## Nota para el proximo agente
<que revisaste, que corregiste, que necesita revision del siguiente>
```

## Checklist de cierre

- [ ] Todas las unidades desarrolladas y revisadas (al menos 1 ronda de cross-review por unidad).
- [ ] Build + tests + lint verdes en el estado final.
- [ ] PLAN-FASE-X.md con todas las unidades marcadas (hecho + revisada por quien).
- [ ] STATUS.md y ROADMAP.md actualizados.
- [ ] CHANGELOG con la entrada del release.
- [ ] Version bump + tag + GitHub Release (si aplica).
- [ ] Leccion aprendida registrada (si el cross-review atrapo un bug, documentarlo).

## Relacion con otros pipelines

Este skill es la capa de ORQUESTACION que coordina el pipeline existente (`docs/pipeline/kanam-product-pipeline.md`). Se aplica en las fases Build/Review del ciclo Define→Plan→Build→Verify→Review→Ship: en vez de un solo agente implementando, se dividen las unidades entre multiples agentes con cross-review. Las skills de Build/Review (`incremental-implementation`, `test-driven-development`, `code-review-and-quality`, etc.) siguen aplicando a nivel de cada unidad; este skill coordina el "quien hace que y quien revisa que".

## Ejemplo real (kanam-story Fase 3 y Fase 5)

- **Fase 3 (2026-08-13):** orquestador dividio en U1-U8 (editor refinado + sync biblia-tabs), A=impares/B=pares. Pipeline en cadena. Resultado: 189 tests, release v0.7.0. El Agente B atrapo un bug real de la U5 (sync corria antes de regenerar la biblia).
- **Fase 5 (2026-08-20, con Qwen Code via Ollama):** U1-U6 completadas (capitulo como unidad de trabajo). 434 tests. El Agente B atrapo un bug real de la U3 (reorden de efectos que corrompia contenido al cambiar de target). Evidencia del valor del cross-review multi-ronda con el nuevo motor.

## Como orquestar desde OpenClaw (Kanam)

Kanam (este agente, corriendo en OpenClaw) es el orquestador. El flujo de trabajo desde aqui:

1. **Recibir la meta del desarrollador** (Gonzo da el objetivo, no escribe prompts).
2. **Planificar** la tarea en unidades atomicas con criterios de aceptacion (como en PLAN-FASE-X.md).
3. **Lanzar el Agente A** con `exec`: `ollama launch qwen --model <modelo> -- -p "<tarea redactada por Kanam>" -y`.
4. **Verificar el output de A** (leer archivos, correr build/tests/lint).
5. **Lanzar el Agente B** pasando el codigo/output de A como contexto en el prompt: "revisa este codigo que escribio A...".
6. **Iterar en cadena** hasta que el codigo pase las gates de calidad (A revisa el fix de B, etc.).
7. **Reportar a Gonzo** el resultado: que se hizo, que se reviso, que quedo pendiente.

- **NOTA sobre el motor (ADR-049):** el harness estandar es **Claude Code** (headless contra el gateway Ollama). Qwen Code queda como fallback. No usar `ollama launch claude --model` (bug: rechaza el flag).

### Pasos tecnicos en OpenClaw
- **Claude Code (estandar, ADR-049):** `exec` con `ollama launch claude --model <tag> -- -p "..."`, o directo `ANTHROPIC_BASE_URL=http://127.0.0.1:11434 ANTHROPIC_AUTH_TOKEN=<x> claude -p "..." --model <tag>` (`claude` ya esta en el PATH, 2.1.280; `pty: true` para sesiones largas).
- **Qwen Code (fallback):** `exec` con `ollama launch qwen --model <modelo> -- -p "..." -y`.
- **Modelo dinamico en ambos:** elegir por tarea via `--model` (deepseek-v4-flash:cloud default, kimi-k2.7-code:cloud cuando se justifica).
- La redaccion de prompts y el encadenado de outputs es responsabilidad del orquestador, no del desarrollador.
- Verificar siempre el resultado real (archivos, build, tests) - no confiar solo en el texto de salida del agente.
- **SIGKILL:** aplica al fallback Qwen (~3 min en tareas largas). Con Claude Code (estandar) es menos frecuente; si un agente muere a mitad, el orquestador verifica, commitea y relanza con prompt mas corto.
