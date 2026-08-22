---
name: "agent-orchestration-pipeline-model-arbitration"
description: "Arbitraje de modelo para pipeline A/B: reducir costos priorizando Kimi K2.7 Code solo cuando se justifica."
---

# Proposal: Arbitraje de modelo en Agent Orchestration Pipeline

## Resumen
Agregar al skill `agent-orchestration-pipeline` una seccion que defina como el orquestador elige el modelo de Ollama Cloud para cada paso del pipeline A/B. El objetivo es reducir costos manteniendo calidad: `deepseek-v4-flash:cloud` es el default, y `kimi-k2.7-code:cloud` se usa selectivamente donde su contexto largo, razonamiento y multimodalidad realmente evitan regresiones.

## Motivacion
- Gonzo esta en el plan mas barato de Ollama Cloud con limite fijo.
- El consumo real (2026-08-21) muestra ~95% de requests en Flash y ~7-8% en Kimi K2.7 Code; GLM 5.2 no destaco en la practica.
- DeepSeek v4 Pro es extra-high usage y no es multimodal; Kimi K3 es aun mas caro (top frontier). No son viables para volumen.
- El cross-review ya introdujo un bug (SoporteML V4 U7, 2026-08-21), asi que el revisor necesita calidad donde importa, no ahorro a ciegas.

## Reglas de arbitraje

### 1. Default
Cada tarea del pipeline A/B parte en `deepseek-v4-flash:cloud`.

### 2. Kimi directo
Escalar a `kimi-k2.7-code:cloud` sin retry cuando:
- **Multimodalidad obligatoria:** imagen, screenshot, diagrama, PDF visual, UI.
- **Revision/debug con ambiguedad real:** test falla sin motivo obvio, logica de negocio cruzada, bug no trivial.
- **Contexto extenso:** archivos grandes, diff grueso, refactor de multiples modulos donde Flash tiende a perderse.

### 3. Feature compleja / mucho contexto
No va directo a Kimi. Secuencia:
1. **Intento 1:** Flash con prompt normal.
2. **Intento 2:** Flash con prompt mejorado (mas estructurado, contexto resumido, ejemplos, instrucciones explicitas).
3. **Intento 3:** recien `kimi-k2.7-code:cloud`.

### 4. Veto por presupuesto
Si el uso semanal supera el 85%:
- Default a Flash en todos los casos.
- Mantener Kimi solo para multimodalidad obligatoria.
- En revision/debug y contexto extenso, aplicar la regla de doble retry con Flash antes de considerar Kimi.

### 5. Retry post-error
Si una tarea con Flash falla:
- Reintentar una vez mas con Flash mejorando el prompt.
- Si sigue fallando, escalar a Kimi.

## Asignacion por rol en el pipeline

| Paso | Modelo |
|---|---|
| Agente A escribe feature simple / refactor mecanico | `deepseek-v4-flash:cloud` |
| Agente A escribe feature compleja / mucho contexto | Flash → Flash mejorado → `kimi-k2.7-code:cloud` |
| Agente A genera interpretacion de imagen / UI / screenshot | `kimi-k2.7-code:cloud` |
| Agente B revisa cambios triviales | `deepseek-v4-flash:cloud` |
| Agente B revisa cambios complejos / debug / arquitectura | Flash → Flash mejorado → `kimi-k2.7-code:cloud` |
| Orquestador verifica contra API/spec / fuente real | `deepseek-v4-flash:cloud` |

## Cambio al SKILL.md
Insertar una nueva seccion entre "Motor: Qwen Code via Ollama" y "Cuando usar", titulada:

```markdown
## Arbitraje de modelo (default: deepseek-v4-flash, escalado selectivo a kimi-k2.7-code)

Cada tarea del pipeline A/B arranca con `deepseek-v4-flash:cloud` por defecto. El orquestador escala a `kimi-k2.7-code:cloud` solo cuando se justifica, siguiendo estas reglas:

1. **Kimi directo:** multimodalidad obligatoria; revision/debug con ambiguedad real; contexto extenso donde Flash pierde coherencia.
2. **Feature compleja / mucho contexto:** doble intento con Flash (prompt normal, luego prompt mejorado) antes de Kimi.
3. **Veto por presupuesto:** si el uso semanal supera el 85%, se mantiene Flash salvo multimodalidad obligatoria.
4. **Retry post-error:** un fallo con Flash se reintenta una vez con Flash mejorado; si persiste, se escala a Kimi.

| Paso del pipeline | Modelo |
|---|---|
| A escribe feature simple / refactor mecanico | `deepseek-v4-flash:cloud` |
| A escribe feature compleja / mucho contexto | Flash → Flash mejorado → `kimi-k2.7-code:cloud` |
| A interpreta imagen / UI / screenshot | `kimi-k2.7-code:cloud` |
| B revisa cambios triviales | `deepseek-v4-flash:cloud` |
| B revisa cambios complejos / debug / arquitectura | Flash → Flash mejorado → `kimi-k2.7-code:cloud` |
| Orquestador verifica contra API/spec / fuente real | `deepseek-v4-flash:cloud` |
```

## Notas
- No se propone cambiar el motor base (Qwen Code via Ollama).
- No se propone usar deepseek-v4-pro ni kimi-k3 para volumen; quedan reservados para tareas puntuales si Gonzo lo decide explicitamente.
- GLM 5.2 queda descartado del arbitraje estandar por no haber destacado en la practica.
