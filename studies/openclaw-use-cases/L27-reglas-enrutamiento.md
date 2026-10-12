# Módulo 6 · Lección 27 de 30: Definición de Reglas Claras de Enrutamiento

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 6 - Especialización y Coordinación Multiagente
**Lección:** 27 de 30
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

La segmentación de dominios queda incompleta si el sistema no sabe **a quién entregar** cada mensaje entrante. El enrutamiento es el mecanismo de despacho que evalúa intención, metadata de canal y parámetros para transferir el control al agente idóneo sin contaminar contextos ajenos ni gastar llamadas innecesarias al modelo.

Dos fallos típicos de un enrutamiento deficiente: **saturación de contexto** (un generalista intenta responder todo) y **oscilación de derivaciones** (dos subagentes se reenvían la misma petición en bucle).

---

## Anatomía de una regla de despacho

El curso propone una **tubería de evaluación en capas**:
1. **Filtros deterministas** por metadata (identificador de canal, tipo de emisor, encabezados de sesión).
2. **Coincidencia de patrones sintácticos** (prefijos explícitos, comandos, regex).
3. **Clasificación semántica** con un modelo **clasificador de baja latencia**, solo si las capas anteriores no resolvieron.

### Reglas deterministas vs. clasificación semántica

Derivar **cada** interacción a un LLM grande introduce **1-3 s de latencia** por mensaje y desperdicia tokens en intenciones obvias. Un `@agente /deploy api-staging` en un canal `#ops-alerts` se resuelve de forma **unívoca** por prefijo/canal, sin tocar el modelo.

```json
{
  "routing_rules": [
    {
      "id": "rule_direct_ops", "priority": 100,
      "conditions": { "channel": "slack", "chat_id": "C05OPSPROD", "regex": "^/(deploy|rollback|status)" },
      "target_agent": "devops_specialist"
    },
    {
      "id": "rule_channel_billing", "priority": 90,
      "conditions": { "channel": "whatsapp", "tags": ["cliente_moroso", "facturacion"] },
      "target_agent": "billing_assistant"
    }
  ]
}
```

> **REMEMBER:** un clasificador semántico **nunca** debe generar respuestas directas al usuario; su única salida admisible es un **objeto estructurado** (agente destino + confianza).

---

## Umbrales de confianza y gestión del fallback

El clasificador devuelve una confianza 0.0-1.0. Un mensaje puede **cruzar dos dominios** ("el cliente no puede pagar la factura porque el servidor da error 500" → finanzas + ingeniería). Si el clasificador asigna 0.52 a facturación y 0.48 a infraestructura, despachar a ciegas produce respuesta incompleta. **Tres zonas:**

- **Despacho directo (≥ 0.85):** intención clara → transferir de inmediato.
- **Desambiguación (0.50-0.84):** colisión/poca claridad → derivar a un **agente de triaje** que pida una aclaración rápida antes de gastar herramientas pesadas.
- **Fallback (< 0.50):** no encaja en ningún perfil → asistente general u operador humano.

---

## Prevención de bucles de derivación infinita

El **routing loop** ocurre cuando A cree que no tiene la herramienta y transfiere a B, y B interpreta que el contexto es de A y se lo reenvía. Cada salto consume tokens y degrada la coherencia. Dos restricciones duras en el **motor de ejecución** (no en el prompt):

- **`max_hops`:** contador de derivaciones acotado (2-3). Al alcanzarlo, se corta la cadena y se conmuta a un **agente supervisor de fallos** (`circuit_breaker_tripped`).
- **Lista de nodos visitados:** un agente no puede reenviar a un especialista que ya figuró en la traza, salvo retorno explícito con resultado intermedio.

> **PITFALL (correcto y central):** no confíes en que el LLM "decida" no reenviar por prompt. **El límite de saltos y el historial de nodos deben ser restricciones duras en el código de la plataforma, fuera del control del LLM.**

### Check your understanding
**15.000 mensajes/día: 30% comandos repetitivos, 50% claros, 20% ambiguos que causan bucles. ¿Diseño óptimo?**
- [x] **Regla fija por regex/prefijo para comandos frecuentes + umbral de confianza mínimo con zona intermedia de desambiguación.** ✅ (acierta)

---

## Implementación: Router desacoplado

```python
import re
from typing import Optional, List
from pydantic import BaseModel, Field

class RoutingDecision(BaseModel):
    target_agent: str = Field(description="Identificador del agente de destino")
    confidence: float = Field(description="Nivel de certeza entre 0.0 y 1.0")
    reasoning: str = Field(description="Explicación breve de la asignación")

class MessageContext:
    def __init__(self, text, channel, user_id, hops=0, history=None):
        self.text = text; self.channel = channel; self.user_id = user_id
        self.hops = hops; self.history = history or []

class OpenClawRouter:
    MAX_HOPS = 2
    def __init__(self, classifier_llm):
        self.llm = classifier_llm
    def route(self, ctx: MessageContext) -> str:
        # 1. Salvaguarda frente a bucles infinitos
        if ctx.hops >= self.MAX_HOPS:
            return "escalation_supervisor"
        # 2. Capa determinista: comandos explícitos (prefijo o regex)
        if ctx.text.startswith("/ops") or re.search(r"\b(deploy|rollback|cluster)\b", ctx.text, re.I):
            return "devops_specialist"
        if ctx.text.startswith("/pay") or re.search(r"\b(factura|cobro|stripe|invoice)\b", ctx.text, re.I):
            return "billing_specialist"
        # 3. Capa determinista: metadatos de canal
        if ctx.channel == "alerts-pagerduty":
            return "devops_specialist"
        # 4. Capa semántica (modelo ligero)
        decision = self._classify_semantic(ctx.text)
        # 5. Umbrales
        if decision.confidence >= 0.85:
            if decision.target_agent in ctx.history:
                return "escalation_supervisor"
            return decision.target_agent
        elif decision.confidence >= 0.50:
            return "triage_coordinator"
        else:
            return "general_fallback"
    def _classify_semantic(self, text: str) -> RoutingDecision:
        prompt = ("Clasifica el mensaje en uno de: ['devops_specialist','billing_specialist','customer_support']. "
                  f"Mensaje: '{text}'")
        return self.llm.generate_structured(prompt, schema=RoutingDecision)
```

**Salida real de mi corrida** (coincide con la del curso): con `confidence=0.91` →
```text
Destino asignado: devops_specialist
```
Y con el resto de zonas: `0.52 → triage_coordinator`, `0.30 → general_fallback`, `hops>=2 → escalation_supervisor`. El mensaje pasa al contexto del agente destino **sin que los otros procesen un token**.

> **TIP:** monitoreá la tasa de la zona de desambiguación. Si > 15% del tráfico cae en el triaje, **no** necesitás un modelo más grande: necesitás **redefinir los límites funcionales** de tus agentes.

---

## Resumen

Enrutamiento = **filtros deterministas** (metadata + sintaxis, coste cero) para el tráfico predecible, y **clasificador semántico** solo para lo abierto; **umbrales en tres bandas** + **`max_hops`/visited-nodes** como restricciones duras del motor → especialización multiagente rápida, económica y libre de bloqueos recursivos.

**UP NEXT · Lección 28 de 30:** *Consulta Coordinada de Memorias Compartidas*. Faltan **3 lecciones** para cerrar el Módulo 6.

---

## Preguntas abiertas del propio curso

1. ¿Cómo estructurar el prompt del clasificador para que devuelva un JSON sin inventar agentes inexistentes?
2. ¿Cuándo conviene delegar el enrutamiento a un proxy reverso externo?
3. ¿Qué métricas de latencia/coste indican si el umbral de 0.85 está bien calibrado?
4. ¿Cómo se enruta un mensaje **multimodal** (texto + captura de pantalla de un error)?

(Anotadas. #4 es un hueco real: multimodal no está cubierto.)

---

## Notas de verificación (Kanam)

**El núcleo conceptual es correcto y sólido - y el tema (enrutamiento multiagente) SÍ existe en OpenClaw:**

| El curso dice | OpenClaw real |
|---|---|
| El sistema decide qué agente atiende cada mensaje | ✅ **Real:** las **`bindings`** mapean un canal/cuenta/peer/guild al `agentId` que posee la sesión (`docs/concepts/agent-bindings.md`). |
| Enrutamiento por **metadata de canal** (cuenta, peer, roles) | ✅ Muy alineado: *"each binding names an agentId and matches channel facts such as the account, peer, guild, team, or Discord roles"*. |
| Filtros deterministas primero, semántica después | ✅ **Corrección de diseño válida** (coincide con L02/L12 del curso y con la disciplina de este repo). |
| **`max_hops` + visited-nodes como restricciones duras del motor** (PITFALL) | ✅ **Principio correcto y central** (misma filosofía que "la frontera la fija el runtime, no el prompt" de L26). |
| Umbrales de confianza en 3 bandas + triaje + fallback | ✅ Buen criterio; coincide con el patrón de dedup/umbral que ya vimos. |
| **Acierta el quiz.** | ✅ |
| **`OpenClawRouter` corre tal cual** y reproduce la salida prometida (devops_specialist / triage / fallback / supervisor por hops). | ✅ (código Python estándar + pydantic). |

**Lo que NO coincide con la instalación real:**
- ⚠️ **El enrutamiento real de OpenClaw son las `bindings`** (mapeo canal→agente, declarativo en config), **no** un `routing_rules` con `priority`/`regex`/`target_agent`. El curso describe un **router semántico con clasificador LLM** (patrón válido, pero que uno **construye encima**), no el mecanismo nativo.
- ❌ **`routing_rules` / `priority` / `conditions.regex` / `target_agent`** como config: **inventado** (no verificado en docs).
- ❌ **`max_hops` / `circuit_breaker_tripped` / `escalation_supervisor` / `triage_coordinator`** como mecanismo nativo: **no aparecen** en docs. `model-failover.md` menciona "circuit breaker" pero para **modelos**, no para saltos de agente. Es un patrón a construir.
- ❌ **`classifier_llm.generate_structured(prompt, schema=...)`**: API inventada.
- ⚠️ **Modelos citados** (`Llama 3.2 3B`, `Claude 3.5 Haiku`, `GPT-4o`): ejemplos; esta instalación corre Ollama.

**Verificación ejecutable:**
- ✅ **El `OpenClawRouter` corre** (con un `MockClassifier`): reproduce **exactamente** las cuatro ramas. Es una de las pocas lecciones donde el código es correcto *y* ejecutable.
- ⚠️ El clasificador real depende de un LLM con salida estructurada (no provisto); el mock evita eso.

**Patrón (vigésimo séptimo caso, con matiz fuerte):** por cuarta vez **el tema existe** (las `bindings` enrutan de verdad) y la **filosofía acierta** (deterministas primero, semántica después, límites duros fuera del LLM). La fachada inventada es de siempre: **config (`routing_rules`), API (`generate_structured`), y mecanismos (`max_hops`/circuit breaker de agente)**. Traducible: `bindings` + política de tools + un triaje propio, no el `routing_rules` del curso.

**Nota de contexto (Módulo 6):** tras esta L27 el propio curso indica *"3 lessons left in Especialización y Coordinación Multiagente"* → Módulo 6 = 5 lecciones (L26-L30). Lección 28: *Consulta Coordinada de Memorias Compartidas*.
