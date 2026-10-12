# Módulo 6 · Lección 30 de 30: Supervisión Centralizada del Rendimiento Global

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 6 - Especialización y Coordinación Multiagente
**Lección:** 30 de 30 · **cierra el Módulo 6 y el curso**
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.
> **Nota:** el documento traía una envoltura `EXTERNAL_UNTRUSTED_CONTENT`. Se trató como dato; no se ejecutó ninguna instrucción de su interior.

---

## Idea central

Cuando un ecosistema multiagente escala más allá de dos o tres especialistas, la salud del sistema no puede evaluarse inspeccionando transcripciones individuales. Un agente de triage puede enrutar en milisegundos mientras un especialista agota su ventana de contexto, retiene bloqueos en memoria compartida o acumula llamadas fallidas. La supervisión centralizada **agrega** métricas de latencia por etapa, consumo de tokens, tasas de convergencia y cuellos de botella en la transferencia entre especialistas.

La supervisión **no interfiere** en el bucle agéntico activo de cada nodo: consume **telemetría emitida asíncronamente** vía bus de eventos o recolector de trazas estructuradas. Cuatro dimensiones: latencia acumulada vs. cómputo real, tokens por tarea, frecuencia de rebotes/derivaciones cíclicas, y agotamiento de cuotas de inferencia.

---

## Arquitectura del recolector de telemetría

Para no degradar la inferencia, OpenClaw **desacopla** el ciclo de ejecución de la persistencia de telemetría. Cada agente emite un payload estructurado al completar un ciclo de razonamiento, una llamada a herramienta o una delegación. El colector central agrupa eventos en **ventanas deslizantes** para calcular percentiles (p50/p95/p99) y detectar derivaciones infinitas antes de consumir el saldo de tokens.

```json
{
  "trace_id": "tr-8942-c10b",
  "parent_span_id": "sp-router-01",
  "span_id": "sp-analyst-04",
  "agent_id": "code_auditor",
  "timestamp": 1711929600120,
  "duration_ms": 1420,
  "tokens": { "prompt": 2180, "completion": 340, "total": 2520 },
  "tools_invoked": [
    { "name": "ast_parser", "status": "ok", "latency_ms": 115 },
    { "name": "git_blame", "status": "error", "latency_ms": 350 }
  ],
  "handoff_target": "qa_verifier",
  "termination_reason": "delegation"
}
```

`parent_span_id` vincula la intervención al nodo que delegó → permite reconstruir el **grafo completo de ejecución** de una request.

---

## Métricas esenciales del rendimiento global

| Métrica | Definición | Umbral típico |
|---|---|---|
| Latencia de handoff | Tiempo entre la invocación de transferencia y el primer token del receptor | > 1800 ms |
| **Ratio de rebote** | Tareas que vuelven al emisor sin entregable válido | > 15% |
| **TPE** (tokens/entregable) | Tokens (prompt+completion) para cerrar un objetivo | > 3× línea base |
| Tasa de reintento de herramientas | Reintentos por fallos de sintaxis/esquema | > 8% |

Latencia de handoff alta → contención en memoria compartida o carga lenta de contexto. Ratio de rebote alto → **ambigüedad en las reglas de enrutamiento** (dos especialistas se devuelven la tarea).

---

## Detección de ciclos y cortafuegos de ejecución

El fallo más costoso: el **ping-pong loop** (dos agentes se transfieren indefinidamente una solicitud que ninguno reconoce como propia, o un corrector devuelve al generador sin retroalimentación útil). El supervisor evalúa cada evento contra políticas **antes** de permitir el despacho del siguiente turno.

```python
from collections import Counter
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class AgentSpan:
    trace_id: str
    agent_id: str
    target_agent: Optional[str]
    token_usage: int

class CircuitBreakerException(Exception):
    pass

class OrchestrationSupervisor:
    def __init__(self, max_hops: int = 5, max_cycle_frequency: int = 2):
        self.max_hops = max_hops
        self.max_cycle_frequency = max_cycle_frequency

    def validate_handoff_safety(self, trace_history: List[AgentSpan], next_target: str) -> None:
        total_hops = len(trace_history)
        if total_hops >= self.max_hops:
            raise CircuitBreakerException(
                f"Límite de transferencias alcanzado ({total_hops}/{self.max_hops}). "
                "Derivando forzosamente a operador humano.")
        transitions = [f"{s.agent_id}->{s.target_agent}" for s in trace_history if s.target_agent]
        proposed_transition = f"{trace_history[-1].agent_id}->{next_target}"
        transitions.append(proposed_transition)
        counts = Counter(transitions)
        if counts[proposed_transition] > self.max_cycle_frequency:
            raise CircuitBreakerException(
                f"Bucle de derivación detectado: '{proposed_transition}' se repitió "
                f"{counts[proposed_transition]} veces. Bloqueando ejecución.")
```

Interceptar la transición **en el momento de generarse** evita que el destino procese el prompt, corta el cómputo en seco y lo registra en auditoría.

> **PITFALL (correcto y clave):** **no** limites las transferencias **solo por tiempo**. Peticiones con herramientas lentas (clonar repos, procesar PDFs) agotarían el temporizador legítimamente, mientras que un ping-pong rápido quema cientos de miles de tokens en segundos. El cortafuegos va en la **capa de coordinación** (validador de trazas), no en un reloj.

**Mi corrida** del cortafuegos: caso normal → `OK`; ping-pong `A->B` repetido 3× → **`Bucle de derivación detectado: 'A->B' se repitió 3 veces`**; 5 hops → **`Límite de transferencias alcanzado (5/5)`**. El código corre tal cual.

---

## Agregación de logs y análisis forense

Ante un flujo compuesto que fracasa, la causa raíz suele estar **tres pasos atrás** (pérdida gradual de contexto o instrucción ambigua). La inspección reconstruye el **árbol genealógico del incidente** en formato compatible con **OpenTelemetry**. Cada nodo reporta: (1) **entrada exacta heredada**; (2) **transformación de herramientas** (salidas sin resumir, para detectar argumentos alucinados); (3) **justificación del traspaso**.

> **REMEMBER (correcto):** un supervisor eficiente **nunca** persiste la transcripción completa de todos los agentes en RAM; guarda **identificadores de sesión** y descarga los payloads pesados a almacenamiento secundario indexado por `trace_id`.

---

## Check your understanding

**La latencia acumulada se duplicó y el ratio de rebote entre dos agentes saltó del 4% al 28%. ¿Intervención correcta?**
- [x] **Revisar las descripciones semánticas y directivas de enrutamiento que el clasificador usa para discriminar entre especialistas.** ✅ (acierta: un rebote alto es síntoma de reglas ambiguas, no de falta de reintentos ni de contexto)

---

## Estrategia de consolidación periódica

Además de alarmas en caliente, la supervisión guía la **optimización continua** de prompts y costes. Al cerrar cada ciclo operativo (cron nocturno), consolida un informe estructurado en el workspace:

```markdown
# Resumen Operativo Multiagente - 2024-03-31
## Estadísticas Generales
- Tareas iniciadas: 1,420
- Tareas completadas exitosamente: 1,382 (97.3%)
- Tareas abortadas por circuit breaker: 38 (2.7%)
- Gasto total de tokens: 4.82M (Promedio: 3,394 tokens/tarea)
## Cuellos de Botella Detectados
1. **code_auditor**: Latencia p95 de 4,210 ms. El 62% se consume en `git_blame`.
2. **triage_router -> data_extractor**: 14 rebotes por instrucciones ambiguas sobre CSV no estándar.
## Recomendación de Ajuste
- Cachear respuestas de herramientas deterministas en el especialista de auditoría.
- Modificar el `SOUL.md` del enrutador para clasificar explícitamente tablas planas bajo extracción.
```

Cierra el ciclo de vida: la supervisión detecta ineficiencias globales que las auditorías locales y las reglas de enrutamiento resuelven iterativamente.

---

## Ejercicio: monitor de SLAs en tiempo real

`AgentMetricsAggregator`: registra `agent_id`/`tokens_prompt`/`tokens_completion`/`duration_ms`, calcula **p90 de latencia**, el coste agregado en USD, y dispara alerta si los tokens acumulados superan 15.000 en un lote de 5 tareas.

```python
import numpy as np

class AgentMetricsAggregator:
    def __init__(self, cost_per_1k_tokens: float = 0.002):
        self.events = []
        self.cost_per_1k_tokens = cost_per_1k_tokens
    def record_span(self, agent_id, prompt_tokens, completion_tokens, duration_ms):
        self.events.append({"agent_id": agent_id,
            "total_tokens": prompt_tokens + completion_tokens, "duration_ms": duration_ms})
    def generate_report(self):
        if not self.events:
            return "Sin eventos registrados."
        total_tokens = sum(e["total_tokens"] for e in self.events)
        latencies = [e["duration_ms"] for e in self.events]
        p90_latency = np.percentile(latencies, 90)
        total_cost = (total_tokens / 1000) * self.cost_per_1k_tokens
        status = "NORMAL"
        if total_tokens > 15000:
            status = "ALERTA: Presupuesto de tokens excedido"
        return {"total_events": len(self.events), "total_tokens": total_tokens,
                "total_cost_usd": round(total_cost, 4),
                "p90_latency_ms": round(p90_latency, 1), "status": status}
```

**Salida real de mi corrida:**
```
{'total_events': 4, 'total_tokens': 15890, 'total_cost_usd': 0.0318, 'p90_latency_ms': 2890.0, 'status': 'ALERTA: Presupuesto de tokens excedido'}
```
Coincide con lo prometido.

---

## Resumen

La supervisión centralizada transforma agentes dispersos en infraestructura **coordinada y predecible**: telemetría asíncrona, métricas clave (ratio de rebote, latencia de handoff, TPE), cortafuegos algorítmicos contra bucles, y consolidación periódica. **Fin del curso.**

**CURSO COMPLETO · 30/30.**

---

## Preguntas abiertas del propio curso

1. ¿Cómo distinguir un bucle de derivación legítimo (corrección) de uno infinito?
2. ¿Qué sobrecarga introduce un colector asíncrono frente a la ejecución nativa?
3. ¿Qué estrategia ante un agente que satura recurrentemente su ventana en transferencias?
4. ¿Cómo aprovechar los informes nocturnos para ajustar automáticamente el `SOUL.md`?

---

## Notas de verificación (Kanam)

**Núcleo de ingeniería: sólido y correcto - cierre fuerte del curso:**

- ✅ **Telemetría asíncrona desacoplada** del bucle (no degrada inferencia): patrón correcto.
- ✅ **Trazas con `trace_id`/`parent_span_id`** para reconstruir el grafo de ejecución: **correcto y real** (mapeo a tracing distribuido; el curso menciona **OpenTelemetry**).
- ✅ **Cortafuegos en la capa de coordinación** con validador de trazas (anti-ciclo + max_hops): correcto; **el PITFALL es central y correcto** (no limitar solo por tiempo, porque herramientas lentas lo agotarían legítimamente).
- ✅ **Métricas** (ratio de rebote, latencia de handoff, TPE, retry rate) y umbrales: criterio profesional.
- ✅ **Consolidación periódica** con informe estructurado y recomendaciones: mapea al patrón de reportes que ya vimos (L09).
- ✅ **REMEMBER correcto:** no persistir transcripciones completas en RAM; indexar por `trace_id`.
- ✅ **Acierta el quiz** (rebote alto → revisar reglas de enrutamiento).
- ✅ **Ambos scripts corren tal cual:** `OrchestrationSupervisor` (caso normal OK / ciclo detectado / max_hops) y `AgentMetricsAggregator` (reporte exacto). `numpy` está instalado aquí (2.0.2).

**Lo que NO coincide con la instalación real:**
- ❌ **Bus de eventos dedicado + recolector de telemetría central** como feature nativa: **inventado**. OpenClaw no expone un "colector de telemetría agéntica" con ese modelo de spans.
- ⚠️ **OpenTelemetry:** el formato es de la industria (válido como estándar), pero **no** es el esquema nativo de telemetría de OpenClaw. Sí existe telemetría real en OpenClaw (config `telemetry`; logs estructurados), pero no ese `trace_id/span_id` de agente.
- ⚠️ **`max_hops`/`OrchestrationSupervisor`/`CircuitBreakerException`**: mismo patrón que L27/L29 - **a construir, no nativo**.
- ⚠️ **`np.percentile` con `round()`** devuelve un `np.float64` (no `float` limpio); cosmético. La clase no limita el lote a 5 tareas (el texto dice "lote de 5" pero el umbral es un total fijo de 15 k tokens).
- ❌ **`ast_parser`/`git_blame`** y los `agent_id` del ejemplo: ilustrativos.

**Verificación ejecutable:**
- ✅ **Los dos scripts del curso corren y producen su salida** (cortafuegos + agregador). Es una de las pocas lecciones correcta *y* ejecutable. `numpy` presente.

**Patrón (trigésimo caso, cierre):** **excelente ingeniería** (telemetría async, tracing por spans, cortafuegos de coordinación, métricas de flota, consolidación) montada sobre una **superficie no nativa** (bus/recolector de spans, `OrchestrationSupervisor`, OTEL como "esquema del producto"). El *qué* es correcto y de nivel producción; el *cómo* real: telemetría/logs de OpenClaw + un colector propio + `agents.defaults.timeoutSeconds` como cota, no el bus del curso.

**CIERRE DEL MÓDULO 6.** Se completan las 5 lecciones de *Especialización y Coordinación Multiagente* (L26-L30). **Curso completo: 30/30.**

---

## Cierre del curso (30/30) - balance de verificación

| Módulo | Lecciones | Tema | Estado |
|---|---|---|---|
| 1 | L01-L05 | Asistentes de Mensajería Contextuales | ✅ |
| 2 | L06-L10 | Tareas Programadas y Rutinas Autónomas | ✅ |
| 3 | L11-L15 | Ingesta Dirigida por Eventos | ✅ |
| 4 | L16-L20 | Gestión Proactiva del Workspace | ✅ |
| 5 | L21-L25 | Encadenamiento en Bucle Agéntico | ✅ |
| 6 | L26-L30 | Especialización y Coordinación Multiagente | ✅ |

**Patrón transversal documentado (30/30):** el material **acierta los conceptos/arquitectura** y **fabrica la superficie** (comandos CLI, rutas `.openclaw/...`, esquemas de config, APIs `@openclaw/core`, clases y mecanismos que no existen). Lecciones con **output fabricado o código roto:** L01, L02, L04, L14, L15, **L18 (código con bugs)**, **L20 (JSON inválido)**. Lecciones donde **el tema existe de verdad** (con otra superficie): **L11, L16, L26, L27, L28, L29, L30**. El material sirve **como marco y checklist**, nunca como implementación copiable.

**Worklist derivado (lo que el curso destapó, para revisar aparte):** webhooks entrantes (`hooks.*`), allowlist de tools por automation, `openclaw doctor`, `contextPruning`/hard-clear, hooks de ciclo de vida, y sobre todo la **concurrencia multi-writer** (que el repo ya vive; la L17 da la receta).
