---
name: "agent-orchestration-pipeline-model-arbitration"
description: "Elegir el modelo de Ollama Cloud para cada paso del pipeline A/B: default, escalada y nivel superior, segun costo y calidad."
disable-model-invocation: true
---

# Arbitraje de modelo en Agent Orchestration Pipeline

## Resumen
Define como el orquestador elige el modelo de Ollama Cloud para cada paso del pipeline A/B. El objetivo es reducir costos manteniendo calidad: `deepseek-v4-flash:cloud` es el default, `glm-5.3-flash:cloud` es la escalada intermedia, y `kimi-k2.7-code:cloud` es el nivel superior (solo cuando se justifica).

## Motivacion
- Gonzo esta en el plan mas barato de Ollama Cloud con limite fijo.
- Comparativa 2026-08-30 (mismo prompt, razonamiento apagado): GLM 5.3 Flash gana en profundidad tecnica y robustez sobre DeepSeek Flash, pero cuesta ~2.4x mas recursos en Ollama Pro.
- DeepSeek Flash es mas conciso y prolijo; GLM anticipa problemas reales (carreras, dedupe en reconexion, setState tras unmount).
- Kimi K2.7 Code es el nivel superior (mejor pensador, validado en high el 29/08), reservado para cuando GLM no alcanza.
- El cross-review ya introdujo un bug (SoporteML V4 U7, 2026-08-21), asi que el revisor necesita calidad donde importa, no ahorro a ciegas.

## Reglas de arbitraje

### 1. Default
Cada tarea del pipeline A/B parte en `deepseek-v4-flash:cloud`.

### 2. Escalada a GLM 5.3 Flash (iteracion 3)
Escalar a `glm-5.3-flash:cloud` cuando:
- **Diseño/arquitectura puntual:** donde la profundidad tecnica paga (GLM gana en robustez).
- **Revision/debug con ambiguedad real:** test falla sin motivo obvio, logica de negocio cruzada, bug no trivial.
- **Contexto extenso:** archivos grandes, diff grueso, refactor de multiples modulos donde Flash tiende a perderse.
- **Multimodalidad:** GLM 5.3 Flash es multimodal nativo (imagen/video/PDF).

### 3. Feature compleja / mucho contexto
No va directo a GLM. Secuencia:
1. **Intento 1:** Flash con prompt normal.
2. **Intento 2:** Flash con prompt mejorado (mas estructurado, contexto resumido, ejemplos, instrucciones explicitas).
3. **Intento 3:** recien `glm-5.3-flash:cloud`.

### 4. Nivel superior: Kimi K2.7 Code (iteracion 4)
Si GLM no alcanza o la tarea es critica, escalar a `kimi-k2.7-code:cloud` (mejor pensador, contexto largo). Reservado para cuando se justifica - no es default.

### 5. Veto por presupuesto
Si el uso semanal supera el 85%:
- Default a Flash en todos los casos.
- Mantener GLM solo para multimodalidad obligatoria o diseño critico puntual.
- En revision/debug y contexto extenso, aplicar la regla de doble retry con Flash antes de considerar GLM.

### 6. Retry post-error
Si una tarea con Flash falla:
- Reintentar una vez mas con Flash mejorando el prompt.
- Si sigue fallando, escalar a GLM 5.3 Flash.
- Si GLM tampoco, escalar a Kimi K2.7 Code.

### 7. GLM sin output: volver a Flash (validado 2026-09-02)
Si un agente con `glm-5.3-flash:cloud` corre sin escribir nada (working tree limpio tras ~10-20 min, proceso vivo sin cambios): matar el proceso y relanzar la misma tarea con `deepseek-v4-flash:cloud`. DeepSeek escribio el fix completo en ~10 min donde GLM no produjo nada en 20. Verificar con `git status`/`git diff --stat` antes de relanzar; si el agente muerto ya dejo cambios, completar y verificar directamente (ver skill agent-orchestration-pipeline).

## Asignacion por rol en el pipeline

| Paso | Modelo |
|---|---|
| Agente A escribe feature simple / refactor mecanico | `deepseek-v4-flash:cloud` |
| Agente A escribe feature compleja / mucho contexto | Flash → Flash mejorado → `glm-5.3-flash:cloud` |
| Agente A genera interpretacion de imagen / UI / screenshot | `glm-5.3-flash:cloud` |
| Agente B revisa cambios triviales | `deepseek-v4-flash:cloud` |
| Agente B revisa cambios complejos / debug / arquitectura | Flash → Flash mejorado → `glm-5.3-flash:cloud` |
| Orquestador verifica contra API/spec / fuente real | `deepseek-v4-flash:cloud` |
| Nivel superior (si GLM no alcanza) | `kimi-k2.7-code:cloud` |

## Notas
- No se propone cambiar el motor base (Qwen Code via Ollama).
- `minimax-m3:cloud` queda como variante de costo similar a GLM (opcional, decision de Gonzo).
- Modelos purgados del ecosistema (2026-08-30): `kimi-k3`, `deepseek-v4-pro`, `nemotron-3-nano`, `qwen3.5:cloud`, `gemma4:31b-cloud`. No usar.
