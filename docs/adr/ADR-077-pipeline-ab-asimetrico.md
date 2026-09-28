# ADR-077: Pipeline A/B asimetrico (ejecutor liviano, revisor grande)

**Fecha:** 2026-09-28
**Estado:** Aceptado
**Decisores:** Gonzo (definicion explicita)
**Origen:** sesion 2026-09-28 - Gonzo pidio usar el pipeline para ejecutar y revisar, con modelos distintos por rol
**Relacionado:** ADR-049 (Claude Code como motor A/B), ADR-053 (modelos), ADR-076 (cloud primero)

---

## Contexto

Durante el review de los sprints 3-6 se pidio "otro ojo". El review **no fue otro ojo**: el modelo que reviso era el mismo que habia ejecutado. Gonzo lo marco: *"no se por que no estas usando el pipeline que para estas cosas fue creado: ejecucion y reviews"*.

El pipeline A/B (`agent-orchestration-pipeline`, ADR-049) existe justamente para esto: A escribe, B revisa. Pero la ruta `pipeline_ab` del router apuntaba a tres modelos intercambiables (`deepseek-v4-flash | glm-5.3-flash | kimi-k2.7-code`) sin distinguir el rol.

## Decision

**En `pipeline_ab`, los dos agentes usan modelos distintos segun su rol:**

```
pipeline_ab → gpt-oss:120b-cloud / deepseek-v4.1-flash:cloud
              ^ Agente A (ejecutor)   ^ Agente B (evaluador y corrector)
```

- **Agente A (ejecutor):** modelo liviano y barato (`gpt-oss:120b-cloud`). Produce el primer borrador. Necesita velocidad y costo bajo.
- **Agente B (evaluador y corrector):** modelo grande con contexto amplio (`deepseek-v4.1-flash:cloud`, 1M de contexto). Revisa y corrige.

**La asimetria es intencional: el revisor ve mas que el ejecutor.** Darle a B el modelo mas grande y de mayor contexto le permite expandirse y ver el contexto completo -el codigo de A, el repo, las reglas- y corregir con fundamento en lugar de opinar sobre un fragmento.

### Aplicado

- `scripts/model-router.sh`: ruta `pipeline_ab` cambiada a `gpt-oss:120b-cloud / deepseek-v4.1-flash:cloud`.
- `skills/agent-orchestration-pipeline/SKILL.md`: documentada la division y el porque.

## Evidencia del valor de la asimetria

Un review con el mismo modelo que ejecuto no aporta. Con A y B distintos, el review adversarial del gate de verificacion (sprints 7-9) encontro **3 evasiones reales** en `scripts/verify-delegation.sh` que la suite del propio autor no cubria: patron con forma de path, patron universal `*`, y cwd no declarado.

## Consecuencias

- **Verificar que el modelo revisora sea distinto del ejecutor.** No basta con "pedir otro ojo": hay que comprobar el modelo efectivo. En el review de los sprints 3-6 no lo fue.
- El **motor** sigue siendo Claude Code (ADR-049); lo que cambia es el `--model` por rol.
- Limitacion conocida y no resuelta: `ollama launch claude` **se cuelga con prompts largos** (verificado con `glm-5.3-flash:cloud` y `kimi-k3:cloud`; los mismos modelos responden bien con prompts cortos). Como el pipeline real usa prompts largos, conviene investigarlo antes de depender del pipeline para reviews de verdad.

## Modelos probados en Claude Code (2026-09-28)

| Modelo | Prompt corto | Prompt largo |
|---|---|---|
| `gpt-oss:120b-cloud` | OK | - |
| `deepseek-v4.1-flash:cloud` | OK | - |
| `glm-5.3-flash:cloud` | OK | **se cuelga** |
| `kimi-k3:cloud` | OK | **se cuelga** |
| `minimax-m2.7:cloud` | OK | - |
| `qwen3.5:cloud` | **Error exit 1** | - |

Los dos elegidos para A y B son los que mejor responden en Claude Code.
