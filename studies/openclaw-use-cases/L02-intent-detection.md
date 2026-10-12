# Módulo 1 - Lección 02: Detección e Interpretación de Intenciones

**Curso:** OpenClaw Use Cases  
**Módulo:** 1/6 - Asistentes de Mensajería Contextuales  
**Lección:** 02/30  
**Fecha:** 2026-10-10  
**Estado:** 🔄 En curso

---

## 📌 Concepto Central

La **detección precisa de intenciones** es el mecanismo que permite al asistente decidir:
1. ¿Este mensaje lo puedo responder automáticamente?
2. ¿Qué tipo de respuesta necesita (FAQ, Escalación, Delegación)?
3. A qué persona/dominio debo enrutarlo?

> "Sin detección correcta de intención, todo lo demás falla." - Principio del Módulo 1.

---

## 🎯 Objetivos de esta Lección

Al finalizar, podrás:
- Clasificar mensajes entrantes en categorías de intención (FAQ vs Escalación)
- Calcular confidence scores precisos para decisiones binarias
- Implementar umbrales de decisión optimizados por canal
- Manejar casos de ambigüedad sin perder información

### Métricas de Éxito Esperadas

| Indicador | Objetivo Mínimo | Objetivo Óptimo |
|-----------|----------------|-----------------|
| Accuracy de clasificación de intención | 90% | 95%+ |
| Tasa de escalación apropiada | 20-30% | <25% |
| Falso positivo (escaló cuando no hacía falta) | 0% | 0% |
| Falso negativo (no escaló cuando debería) | 0% | 0% |

---

## 🧠 Modelos de Detección de Intención

### Clasificación de Intenciones Primarias

```
┌─────────────────────────────────────────────────┐
│              INTENT CLASSES                      │
├─────────────────────────────────────────────────┤
│  ✅ FAQ/Info       → Respuesta directa           │
│  ⚠️ ESCALACION     → Requiere humano             │
│  🔄 DELEGACION     → Acción a otra persona/tool  │
│  ❌ ERROR          → Problema técnico            │
└─────────────────────────────────────────────────┘
```

### Jerarquía de Prioridad

1. **Primero**: ¿Es FAQ? (Respuesta automática segura)
2. **Segundo**: ¿Necesita acción en otra persona/herramienta? (Delegación)
3. **Tercero**: ¿Requiere decisión humana crítica? (Escalación)
4. **Cuarto**: ¿Es error técnico o spam?

---

## 🛠️ Componentes Técnicos

| Componente | Función | Tecnologías Sugeridas |
|------------|---------|---------------------|
| **Intent Classifier** | Detecta categoría de mensaje | LLM ligero (Tier 1) |
| **Confidence Calculator** | Puntuación 0-100% | Modelo de scoring |
| **Threshold Engine** | Define umbrales por intención | Configurable por canal |
| **Router** | Asigna a persona/herramienta | Plugin/router OpenClaw |

---

## 🎯 Ejemplos de Clasificación

### Ejemplo 1: FAQ Simple → Auto
```json
{
  "message": "¿cuál es el status del deploy?",
  "intent": "FAQ",
  "confidence": 96,
  "action": "RESPOND_AUTOMATICALLY"
}
```

### Ejemplo 2: Solicitud Crítica → Escalación
```json
{
  "message": "Revisa inmediatamente los números de Q3 antes de las 3PM",
  "intent": "ESCALACION",
  "confidence": 98,
  "action": "ESCALATE_TO_HUMAN",
  "reason": "Solicitud comercial urgente con deadline crítico"
}
```

### Ejemplo 3: Ambigüedad → Aclaración
```json
{
  "message": "podrías pasarme X?",
  "intent": "AMBIGUO",
  "confidence": 42,
  "action": "REQUEST_CLARIFICATION"
}
```

---

## 📋 Criterios de Clasificación por Intención

### ✅ FAQ / Información (Auto-respuesta)
- Preguntas de conocimiento común
- FAQs del sistema/producto
- Estado de servicios operativos
- Peticiones de información no crítica

### ⚠️ Escalación a Humano
- Decisiones comerciales/financieras
- Acciones con impacto crítico en negocio
- Problemas que requieren investigación profunda
- Solicitudes fuera del dominio del agente

### 🔄 Delegación a Herramienta/Otra Persona
- Acciones ejecutables por plugins/tools
- Transferencia de contexto a persona especializada
- Ejecución de tareas técnicas no críticas

### ❌ Error/Spam
- Mensajes con errores técnicos
- Spam/duplicate messages
- Contenido malicioso/toxic

---

## 🧪 Implementación Técnica

### Paso 1: Classifier (Modelo Ligero Tier 1)

```python
# Ejemplo pseudo-código para la estructura
from openclaw.skill_workshop import llm_call

def detect_intent(message_text, channel_context):
    prompt = f"""
    Clasifica esta intención en: FAQ | ESCALACION | DELEGACION | ERROR
    
    Mensaje: {message_text}
    Contexto canal: {channel_context}
    
    Devuelve JSON:
    {{
      "intent": "...",
      "confidence": 0-100,
      "reasoning": "..."
    }}
    """
    
    result = llm_call(model="tier1-llm", prompt=prompt)
    return parse_json(result)
```

### Paso 2: Umbrales de Decisión

```yaml
# config/intents/thresholds.yaml
faq_min_confidence: 85      # Si confidence >= 85, auto-responder
escalation_max_auto: 60     # Si confidence < 60 en escalación, escalar directo
delegation_min_confidence: 75
ambiguous_threshold: 40      # Si confidence <= 40, solicitar aclaración
```

### Paso 3: Lógica de Decisión

```python
confidence = classifier.score(message)
intent = classifier.intent(message)

if intent == "FAQ":
    if confidence >= faq_min_confidence:
        return ACTION_AUTO_RESPOND
    else:
        return ACTION_ESCALATE
    
elif intent == "ESCALACION":
    # Para escalaciones, si confidence es muy bajo, siempre escalar
    if confidence < escalation_max_auto:
        return ACTION_ESCALATE
    
elif intent == "DELEGACION":
    if confidence >= delegation_min_confidence:
        return ACTION_DELEGATE

return ACTION_REQUEST_CLARIFICATION if confidence <= ambiguous_threshold
```

---

## 🔍 Ejercicios Prácticos

### Ejercicio 1: Clasifica estos mensajes
```
1. "¿Cómo configuro el webhook de Slack?"
2. "Necesito aprobar el presupuesto para Q4 antes del viernes"
3. "El error que muestra la API no tiene sentido, ¿puedes revisar los logs?"
4. "ping"
5. "¿Cuál es la policy de retention de mensajes en este canal?"
```

### Ejercicio 2: Optimiza umbrales
Dado un dataset de 1000 mensajes con ground truth, ajusta los umbrales para:
- Maximizar resolución automática sin perder calidad
- Mantener <25% de escalaciones
- Reducir falsos positivos a 0%

---

## 🧩 Casos Complejos

### Caso A: Mensaje Híbrido (Intención mixta)
```json
{
  "message": "Hola, necesito información sobre pricing y también configurar el webhook",
  "intents_detected": ["FAQ", "DELEGACION"],
  "primary_intent": "FAQ",
  "confidence": 78,
  "action": "RESPOND_FAQ_AND_DELEGATE_TO_TOOLS"
}
```

### Caso B: Evolución de Intención en Thread
```
Usuario: "¿cómo está la infraestructura?" → FAQ (Auto)
Usuario: "Revisa esos números de Q3, son críticos para el board" → ESCALACION (por evolución)
```

---

## 📊 Métricas y Observabilidad

| Métrica | Herramienta | Frecuencia |
|---------|-------------|------------|
| Confidence score promedio | Logging classifier output | Cada mensaje |
| Accuracy por intención | A/B testing ground truth | Semanal |
| Tasa de escalación % | Dashboard | Diario |
| Tiempo promedio clasificación | Performance tracking | Continuo |

---

## 🔗 Siguientes Pasos

Tras completar la detección de intenciones, avanzamos hacia el enrutamiento especializado por dominio y persona.

**Lección 03:** Enrutamiento por Dominio y Persona → Asignar consultas a especialistas según intención detectada

---

*Documento actualizado siguiendo la reestructuración del curso OpenClase Use Cases (6 módulos, 30 lecciones totales)*
