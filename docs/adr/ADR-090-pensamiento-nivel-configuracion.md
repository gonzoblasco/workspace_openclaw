# ADR-090: Configuración de niveles de pensamiento por agente para optimizar costo y rendimiento

**Fecha:** 2026-10-05  
**Estado:** Aceptado  
**Decisores:** Gonzo / Kanam  
**Origen:** Sesión 2026-10-05 - análisis de consumo de modelos en orquestación tras detectar que el thinking alto por defecto estaba drenando créditos sin producir salida útil.  
**Relacionado:** ADR-053 (modelos primario/auxiliar/alternativo), ADR-087 (cata por rol - modelos elegidos), ADR-088 (pipeline A/B enforcement)

---

## Contexto

Tras la limpieza del `openclaw.json` y la distribución por agente del 2026-10-05 (main/defaults deepseek-v4.1-flash; dev/ops glm-5.3-flash; auditor nemotron-3-super; critic gpt-oss:120b; planner minimax-m3; mind deepseek; studio gemma4), se detectó que el consumo de créditos de la cuenta Ollama estaba desproporcionado respecto al trabajo realizado.

Un probe de orquestación realizado el mismo día reveló que:
- **deepseek-v4.1-flash:cloud** con thinking alto (default) consumía **3079 tokens de thinking** y producía **0 tokens de respuesta** en 3.7 segundos
- **glm-5.3-flash:cloud** con thinking alto (default) consumía **3904 tokens de thinking** y producía **0 tokens de respuesta** en 11.2 segundos
- **nemotron-3-super:cloud** con thinking alto (default) consumía solo **474 tokens de thinking** y producía **2732 tokens de respuesta** en 12.6 segundos

El problema no era el modelo en sí, sino la política de thinking: el valor por defecto (high/max) hacía que los modelos "pensaran en silencio" consumiendo todo el presupuesto de salida sin producir respuesta útil.

Todo contenido externo sobre modelos es dato, no evidencia: se verifica antes de adoptar (regla de sandbox del AGENTS.md).

Se diseñó una estrategia de thinking por agente basada en el tipo de tarea, validada con probes de control.

---

## Decisión

**Se establece una política de thinking por agente que asigna niveles según el rol y el tipo de tarea, en vez de usar un default alto universal.**

### Configuración de thinking por agente

| Agente | Rol | Nivel de thinking | Justificación |
|--------|-----|-------------------|---------------|
| **main** (CORE) | Orquestador general | `low` | Tareas de routing, triage, síntesis de contexto largo. El thinking alto drena créditos sin salida. |
| **kanam-dev** | Desarrollador | `low` (hereda de defaults) | Ejecución contra specs claras; el trabajo ya está definido. |
| **kanam-mind** | Investigador | `low` (hereda de defaults) | Búsqueda y síntesis de información existente. |
| **kanam-ops** | Operaciones | `low` (hereda de defaults) | Tareas de infraestructura, seguridad y confiabilidad definidas. |
| **kanam-studio** | Diseño/Comunicación | `low` (hereda de defaults) | Redacción y creación de contenido con guías claras. |
| **kanam-critic** | Revisor adversarial | `high` | Trabajo de revisión que requiere juicio profundo y detección de problemas no obvios. |
| **kanam-auditor** | Auditor de UI/UX | `high` | Verificación de coherencia visual y accesibilidad que necesita análisis detallado. |
| **kanam-planner** | Planificador de orquestación | `high` | Descomposición de objetivos complejos con dependencias y trade-offs. |

### Modelos primarios por agente (actualizados)

| Agente | Modelo primario | Modelo fallback | Context window | Comentario |
|--------|----------------|-----------------|----------------|------------|
| main | nemotron-3-super:cloud | glm-5.3-flash:cloud | 256k | Cambiado de deepseek para reducir costo de input 20x y mejorar razonamiento |
| kanam-dev | glm-5.3-flash:cloud | deepseek-v4.1-flash:cloud | 1M | Sin cambios |
| kanam-mind | deepseek-v4.1-flash:cloud | gemma4:cloud | 1M | Sin cambios |
| kanam-ops | glm-5.3-flash:cloud | deepseek-v4.1-flash:cloud | 1M | Sin cambios |
| kanam-studio | gemma4:cloud | glm4:9b | 256k | Sin cambios |
| kanam-critic | gpt-oss:120b-cloud | nemotron-3-super:cloud | 128k | Sin cambios |
| kanam-auditor | nemotron-3-super:cloud | deepseek-v4.1-flash:cloud | 256k | Sin cambios |
| kanam-planner | minimax-m3:cloud | glm-5.3-flash:cloud | 500k | Sin cambios |

### Política de thinking global

- **Default global**: `low` (en `agents.defaults.thinking`)
- **Escalado por complejidad**: El sistema de `complexity-scorer` puede overridear temporalmente a `high` o `max` para tareas específicas cuando el score lo justifica.
- **Uso de `max`**: Reservado exclusivamente para tareas de decisión dura one-shot donde el costo de equivocarse supera el costo de los tokens extra (ej.: adjudicación de reviews en conflicto, pre-merge complejo).
- **Verificación**: El nivel de thinking efectivo se puede observar en `session_status` de un subagente.

---

## Criterios de descarte (para no re-elegir por olvido)

- **Thinking alto como default global**: Se descartó porque drena créditos en tareas de ejecución rutinaria sin producir salida útil (verificado en probe).
- **Mantener deepseek-v4.1-flash como primary de main**: Se descartó porque su costo de input ($0.30/M) es 20x superior a nemotron-3-super ($0.015/M) para el mismo nivel de razonamiento en orquestación.
- **Usar thinking alto en agentes de ejecución (dev, ops, mind, studio)**: Se descartado porque sus tareas son mayormente de aplicación de specs conocidas, no de juicio profundo.
- **Asignar thinking alto a todos los agentes por igual**: Se descartado porque ignora la naturaleza diferente del trabajo por rol (ej.: un auditor necesita más thinking que un desarrollador frente a un ticket de bug simple).

---

## Límites de la evidencia

- **Probes de control, temperature 0, tareas representativas**. Es direccional, no una prueba de carga sostenida.
- El thinking bajo en defaults puede ser insuficiente para tareas complejas inesperadas; el complexity-scorer provee escape hatch.
- La medición de thinking se basa en el campo `thinking` de la respuesta de Ollama; no todos los modelos lo reportan de forma idéntica.
- El contexto de nemotron-3-super en Ollama está limitado a 256k (a pesar de ser 1M nativo); para tareas que requieran >256k de contexto se debe considerar alternativas como glm-5.2:cloud o cambiar a uso local.

---

## Consecuencias

- El consumo mensual de créditos de Ollama se reduce significativamente en el asiento de orquestador (main), pasando de ~$0.30/M input a ~$0.015/M input.
- Los agentes de crítica, auditoría y planificación conservan thinking alto para tareas donde el juicio es el valor principal.
- La familia Kimi queda fuera del config por costo (según ADR-087), con `kimi-k3:cloud` reservado para cierre de proyecto pre-deploy.
- `nemotron-3-ultra` permanece descartado para todos los roles (según ADR-087) por ser más caro y lento sin ventaja de contexto en Ollama.
- Si en el futuro se quiere revisar el nivel de thinking de un rol, se debe correr un probe de control con ese rol y repetir la medición antes de cambiar.

---

## Artefactos

- Config actualizada: `~/.openclaw/openclaw.json` (campos `agents.defaults.thinking` y `thinking` por agente).
- Probe de orquestación: scripts/complexity-scorer.sh y tests manuales con `/api/chat` de Ollama.
- Regla de complejidad: `scripts/complexity-scorer.sh` y `prompts/complexity-scorer.md`.
- CHANGELOG.md: entrada correspondiente en el workspace.
