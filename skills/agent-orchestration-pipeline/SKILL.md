---
name: "agent-orchestration-pipeline"
description: "Orquestar multiples agentes implementadores (A/B) en cadena con revision cruzada multi-ronda, usando Qwen Code via Ollama como motor, para unidades atomicas con gates de calidad."
---

# Agent Orchestration Pipeline

Orquestar multiples agentes implementadores con revision cruzada multi-ronda, coordinados por un agente orquestador, para desarrollar unidades atomicas con gates de calidad en cada etapa.

> **ESTANDAR DE TRABAJO DESDE 2026-08-20:** la forma de programar de ahora en mas es este pipeline con **Qwen Code lanzado via Ollama como el motor de los agentes A/B**. Kanam (orquestador) redacta las tareas, encadena los outputs (pasa el codigo de A a B), verifica y reporta. El desarrollador no escribe prompts de agentes - solo da la meta.

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

### Limitaciones
- **Claude Code:** no acepta `--model` por flag CLI (usa `~/.claude/settings.json`). `ollama launch claude` dio errores de sintaxis. Para usarlo, configurar el modelo en settings, no por flag.
- **OpenCode:** no instalado por defecto. Requiere instalacion si se quiere usar.
- **Qwen Code es el motor preferido** por su integracion directa con Ollama via flag.

### Verificacion del orquestador
El orquestador NO solo lanza y lee output: verifica el resultado real (leer archivos creados/editados, correr build/tests/lint) antes de pasar a la siguiente etapa.

---

## Cuando usar

## Cuando usar

- El trabajo es lo suficientemente grande para dividirse en unidades atomicas (features, slices, bugs) que puedan desarrollarse de forma paralela o secuencial.
- Se quiere calidad alta con revision independiente (no solo self-review del autor).
- Hay 2+ agentes implementadores disponibles (ej. VS Code, ZCode) con un orquestador que coordina.
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

## Ejemplo real (kanam-story Fase 3)

- Orquestador: dividio en U1-U8 (editor refinado + sync biblia-tabs), asigno A=impares/B=pares.
- Pipeline en cadena: A desarrolla U1 → B revisa U1 + desarrolla U2 → A revisa U2 + desarrolla U3 → ...
- Resultado: 189 tests, release v0.7.0. El Agente B atrapo un bug real de la U5 (sync corria antes de regenerar la biblia) que el orquestador no detecto en su revision - evidencia del valor del cross-review multi-ronda.
- Backlog B1-B7: el orquestador implemento B1/B2 (tests), luego cadena de revision A → B para asegurar calidad.

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
- Usar `exec` con el comando `ollama launch qwen --model <modelo> -- -p "..." -y` (background o con yieldMs para tareas largas).
- La redaccion de prompts y el encadenado de outputs es responsabilidad del orquestador, no del desarrollador.
- Verificar siempre el resultado real (archivos, build, tests) - no confiar solo en el texto de salida del agente.
