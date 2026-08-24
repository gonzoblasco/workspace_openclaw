---
name: "agent-orchestration-pipeline"
description: "Orquestar agentes A/B en cadena con cross-review multi-ronda, usando Qwen Code (estandar) o Claude Code (alternativo) via Ollama, con modelo dinamico."
---

# Agent Orchestration Pipeline

Orquestar multiples agentes implementadores con revision cruzada multi-ronda, coordinados por un agente orquestador, para desarrollar unidades atomicas con gates de calidad en cada etapa.

> **ESTANDAR DE TRABAJO DESDE 2026-08-20:** la forma de programar de ahora en mas es este pipeline con **Qwen Code lanzado via Ollama como el motor de los agentes A/B** (estandar). Desde 2026-08-21, **Claude Code esta disponible como agente alternativo** con el mismo modelo dinamico. Kanam (orquestador) redacta las tareas, encadena los outputs (pasa el codigo de A a B), verifica y reporta. El desarrollador no escribe prompts de agentes - solo da la meta.

## Motor: Qwen Code via Ollama (spike validado 2026-08-20)

Los agentes implementadores son instancias de **Qwen Code** lanzadas por el orquestador a traves de Ollama, usando los modelos locales/cloud de Ollama. Esto da acceso a los modelos sin APIs externas de pago.

### Comando base
```bash
ollama launch qwen --model deepseek-v4-flash:cloud -- -p "<tarea>" -y
```
- `-y` = auto-approve (YOLO mode) para que ejecute tools (write, edit, shell) sin pedir aprobacion en headless.
- Modelo: cualquiera de los disponibles en `ollama list` (deepseek-v4-flash:cloud por defecto).
- El prompt (`-p`) lo redacta el ORQUESTADOR (Kanam), no el desarrollador.

### Flujo en CADENA (no paralelo) - validado
A escribe → [orquestador pasa el output/codigo de A como contexto a B] → B revisa y corrige → [orquestador verifica] → A revisa el fix de B → ... hasta aprobar.

Ejemplo validado: A escribio `sumar()` (bug latente: concatena strings) → B reviso el codigo de A (pasado como contexto) y lo corrigio a `Number(a)+Number(b)` → orquestador verifico. Iterable indefinidamente.

### Aislamiento entre agentes
- Cada agente trabaja en su propia carpeta/directorio (no se pisan).
- El orquestador pasa el estado (archivo/codigo) de un agente a otro como contexto en el prompt.
- Dos instancias paralelas funcionan, PERO el flujo de trabajo estandar es EN CADENA (dependencia de orden: B necesita el output de A).

### Motor alternativo: Claude Code via Ollama (desbloqueado 2026-08-21)

Claude Code tambien puede ser agente implementador/revisor con el mismo modelo dinamico de Ollama. NO usar `ollama launch claude` (roto: pide `--model` para headless pero lo rechaza como "unknown option"). En su lugar, correr Claude Code directo con env vars + modelo dinamico:

```bash
ANTHROPIC_BASE_URL=http://localhost:11434 \
ANTHROPIC_AUTH_TOKEN=<cualquier-token> \
claude -p "<tarea>" --model <modelo>
```

**Requisitos:**
1. **Claude Code >= 2.x** (`npm install -g @anthropic-ai/claude-code@latest`). La 0.2.18 crashea con "Expected first content item to be text, but got thinking" porque no maneja el bloque `{type:thinking}` de los modelos de razonamiento. La 2.x lo maneja.
2. **Env vars:** `ANTHROPIC_BASE_URL=http://localhost:11434` (endpoint Anthropic-compatible de Ollama) + `ANTHROPIC_AUTH_TOKEN` (Ollama no valida el token).
3. **Modelo dinamico:** `--model <cualquier-modelo-de-ollama>` (deepseek-v4-flash:cloud, kimi-k2.7-code:cloud, etc.).
4. **Permisos headless:** `~/.claude/settings.json` con `permissions.allow` (Edit, Write, Bash, Read) para auto-aprobar herramientas.
5. **Warnings cosmeticos:** Claude Code no reconoce modelos custom y emite warnings (unrecognized_model / deprecacion). Ruido, no bloquean.

**Validado (spike 2026-08-21):** Agente A escribio `sumar.js` correcto (conservo comentarios, ejecuto node); Agente B cross-review encontro y corrigio el bug de concatenacion de strings con `Number(a)+Number(b)`. Modelo dinamico con `--model kimi-k2.7-code:cloud` funciono.

### Limitaciones
- **OpenCode:** no instalado por defecto. Requiere instalacion si se quiere usar.
- **Qwen Code es el motor estandar** por su integracion directa con Ollama via flag (un solo comando). Claude Code queda como alternativa para cuando Qwen se cuelgue (SIGKILL en tareas largas) o para un segundo par de ojos con distinta implementacion de edicion.

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
- **Redacta los prompts/tareas** para los agentes Qwen (el desarrollador no escribe prompts de agentes - solo da la meta).
- Asigna unidades a los agentes (paridad: A = impares, B = pares) y **encadena los outputs** (pasa el codigo de A a B como contexto).
- **Verifica el resultado real** de cada agente (leer archivos, correr build/tests/lint) antes de avanzar.
- Define las reglas del pipeline y el flujo de revision cruzada.
- Coordina el cierre (release, changelog, tag).
- Documenta el plan en un archivo dedicado (ej. `PLAN-FASE-X.md`) + STATUS + ROADMAP.
- NO desarrolla unidades de los agentes (salvo tareas de orquestacion como tests de infra, refactors, o cuando el orquestador asume una unidad directamente).

### Agentes implementadores (A, B, C, ...)
- **Son instancias de Qwen Code lanzadas por el orquestador via Ollama** (`ollama launch qwen --model <modelo> -- -p "<tarea>" -y`).
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

Este skill es la capa de ORQUESTACION que coordina el pipeline existente (`kanam-product-pipeline.md`). Se aplica en las fases Build/Review del ciclo Define→Plan→Build→Verify→Review→Ship: en vez de un solo agente implementando, se dividen las unidades entre multiples agentes con cross-review. Las skills de Build/Review (`incremental-implementation`, `test-driven-development`, `code-review-and-quality`, etc.) siguen aplicando a nivel de cada unidad; este skill coordina el "quien hace que y quien revisa que".

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

### Pasos tecnicos en OpenClaw
- **Qwen (estandar):** `exec` con `ollama launch qwen --model <modelo> -- -p "..." -y` (background o con yieldMs para tareas largas).
- **Claude Code (alternativo):** `exec` (pty: true) con `ANTHROPIC_BASE_URL=http://localhost:11434 ANTHROPIC_AUTH_TOKEN=<x> claude -p "..." --model <modelo>`.
- **Modelo dinamico en ambos:** elegir por tarea via `--model` (deepseek-v4-flash:cloud default, kimi-k2.7-code:cloud cuando se justifica).
- La redaccion de prompts y el encadenado de outputs es responsabilidad del orquestador, no del desarrollador.
- Verificar siempre el resultado real (archivos, build, tests) - no confiar solo en el texto de salida del agente.
- **Nota sobre SIGKILL:** los procesos de Qwen pueden morir (SIGKILL) en tareas largas (~3 min). Para revisiones, usar prompts cortos/concisos para que terminen antes de morir. Si un agente muere a mitad, el orquestador verifica y commitea el trabajo, y relanza la revision con prompt mas corto. Claude Code (2.x) tiene mejor manejo de sesiones largas y puede usarse como recurso en estos casos.
