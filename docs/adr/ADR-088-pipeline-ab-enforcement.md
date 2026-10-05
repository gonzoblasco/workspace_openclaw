# ADR-088: El pipeline A/B tiene enforcement, no buena voluntad

**Fecha:** 2026-10-05
**Estado:** Aceptado
**Decisores:** Gonzo (pedido explicito: "encargate de nunca volver a cometerlo")
**Origen:** Sesion 2026-10-05 - el CORE delego una sesion entera de codigo sobre `ollama-visor` con un solo agente y el modelo por defecto del rol, sin correr el pipeline A/B.
**Relacionado:** ADR-077 (pipeline A/B asimetrico), ADR-083 (frontera de roles y su enforcement), ADR-049 (Claude Code como motor A/B)

---

## Contexto

Durante la sesion de rediseno de `ollama-visor` el CORE spawneo cinco subagentes de trabajo con `sessions_spawn(agentId: "kanam-dev")`. En los cinco:

- **No paso `model`**, asi que corrio el **primario del rol** (`glm-5.3-flash:cloud`), no el modelo del pacto.
- **Corrio UN agente por tarea.** No hubo agente B. La "verificacion" la hizo el propio CORE.

Gonzo lo detecto por el consumo: *"no veo consumos de ese modelo"*. El pacto (ADR-077) dice que en `pipeline_ab` el **A escribe con `gpt-oss:120b-cloud`** y el **B revisa con `deepseek-v4.1-flash:cloud`**, y que **el revisor ve mas que el ejecutor**.

### Por que paso (causa mecanica)

La regla estaba escrita en cuatro lugares (AGENTS.md, ADR-077, la skill de arbitraje, `scripts/model-router.sh`) y **ninguno la aplicaba en el camino real**:

1. **`scripts/model-router.sh` sugiere, no obliga.** Hay que consultarlo a mano. Si el CORE no lo consulta, no pasa nada.
2. **La plomeria del pipeline asume otro mecanismo.** Los scripts (`model-router.sh`, `pipeline-track.sh`, `pipeline-queue.sh`, `complexity-scorer.sh`) fueron escritos para el harness de ADR-049: `exec` con `ollama launch claude --model <tag>`. Ninguno invoca `sessions_spawn`. El CORE corre por `sessions_spawn` y salteo el pipeline entero.
3. **La instruccion operativa se contradecia a si misma.** El bloque de AGENTS.md decia *"Kanam-dev genera los prompts de ambos"* - falso per ADR-077: los prompts los redacta el **orquestador (CORE)**, no el rol. Una instruccion incoherente no se puede seguir.

Es el mismo patron que ADR-083: **una regla sin un check que la mida es indistinguible de una regla ausente.** La regla no se puede dejar en la buena voluntad del CORE.

## Decision

**El pacto A/B queda con enforcement mecanico, no solo escrito.**

### 1. La regla vive en AGENTS.md (bloque administrado `pipeline-ab`)

El bloque lo genera `scripts/managed-blocks.py` desde la tabla `settings` de `memory.db` (claves `model_pipeline_a`, `model_pipeline_b`). Se elige AGENTS.md porque es **lo unico que el CORE lee siempre** y **lo unico que reciben sus subagentes**; una regla en un ADR o en `SKILLS-INDEX.md` no es contexto permanente del turno.

### 2. Un check que la verifica: `scripts/check-pipeline-enforcement.py`

Caza tres cosas, sin escribir:

1. **Fuente que no declara el pacto** - el router sin la ruta `pipeline_ab`, o managed-blocks sin los settings: entonces el bloque de AGENTS.md no puede propagarlo.
2. **Dos verdades** - router y managed-blocks declarando A/B distintos: el pacto se puede citar a conveniencia.
3. **Asimetria rota** - A == B: "pedir otro ojo" con el mismo modelo no es un segundo ojo (el defecto que origino ADR-077).

El check **lee las fuentes reales** (regex sobre `model-router.sh`, `managed-blocks.py`, la skill de arbitraje y ADR-077), no una tabla hardcodeada: si una deriva, falla ruidosamente. Tiene tests en `tests/python/test_check_pipeline_enforcement.py` que **siembran cada defecto** y exigen que el check distinga limpio de sucio.

### 3. Conectado al pre-commit

El gate corre cuando el commit toca `scripts/`, `skills/`, `docs/` o `AGENTS.md` (disparador propio, no el de skills/scripts, por la misma leccion que ADR-083: la violacion se comete cambiando una fuente que el disparador generico no matchea). Se aplica en `.git/hooks/pre-commit` y en `scripts/pre-commit.template` (el hook instalado y la plantilla no pueden divergir).

### 4. Corregida la instruccion contradictoria

El bloque `model-operativo` de AGENTS.md ya no dice que kanam-dev genera los prompts: dice que los redacta el CORE.

## Consecuencias

- **El CORE delega con DOS agentes y los modelos del pacto, o el commit falla.** No se puede mergear una deriva de la fuente sin que el gate la marque.
- **El check es de las FUENTES, no del runtime.** Verifica que el pacto este bien declarado y consistente; no puede ver un `sessions_spawn` sin `model` en un turno. Esa parte sigue siendo disciplina del CORE - pero ahora el pacto esta a la vista en AGENTS.md (que si lee) y la fuente de verdad es consultable con `model-router.sh model pipeline_ab`.
- **El trabajo ya hecho con el modelo equivocado no se rehace por decreto.** Las cinco tareas de `ollama-visor` corriendo con `glm-5.3-flash` quedan como estan salvo pedido explicito; lo que cambia es que las proximas ya no pueden salir asi en silencio.
- **La skill de arbitraje y el router siguen siendo la fuente del modelo por tarea**; este ADR les suma el gate que faltaba.

## Artefactos

- `scripts/check-pipeline-enforcement.py` - el gate.
- `tests/python/test_check_pipeline_enforcement.py` - pruebas con siembra de defectos.
- `scripts/managed-blocks.py` - bloque `pipeline-ab` + settings `model_pipeline_a` / `model_pipeline_b`.
- `.git/hooks/pre-commit` y `scripts/pre-commit.template` - el disparador.
