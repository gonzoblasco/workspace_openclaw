# Módulo 6 · Lección 29 de 30: Transferencia Limpia de Tareas entre Especialistas

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 6 - Especialización y Coordinación Multiagente
**Lección:** 29 de 30
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

Una transferencia limpia cede la ejecución de un subobjetivo a otro agente **sin arrastrar el historial de razonamiento previo ni corromper el contexto del receptor**. Pasar el prompt completo acumulado satura la ventana, introduce ruido conversacional y genera alucinaciones cruzadas.

La delegación limpia sustituye el reenvío indiscriminado de mensajes por un **payload de traspaso estructurado** (*handover token*) que encapsula solo: la meta inmediata, las precondiciones validadas, los artefactos generados y los punteros a la memoria compartida.

---

## Anatomía del protocolo de transferencia

El emisor condensa su estado en un **contrato formal** con cuatro campos indispensables:

- **`task_id`:** identificador unívoco del subobjetivo en la traza.
- **`handoff_context`:** resumen declarativo de hallazgos indispensables, **omitiendo** los pasos de prueba y error.
- **`workspace_artifacts`:** rutas relativas a archivos consolidados en disco (evita transportar blobs en el prompt).
- **`acceptance_criteria`:** lista determinista de condiciones que el receptor debe certificar para cerrar o devolver el control.

```json
{
  "protocol_version": "1.2",
  "handoff_source": "triage_agent",
  "handoff_target": "infra_specialist",
  "task_id": "task_srv_audit_9481",
  "intent": "analyze_nginx_outage",
  "handoff_context": "Se detectó degradación de latencia en webhooks tras el deploy 0.9.4. El agente de triage verificó conectividad DNS satisfactoria.",
  "workspace_artifacts": ["memory/shared/deploy_state_0.9.4.json", "tmp/triage_dns_report.txt"],
  "acceptance_criteria": [
    "Identificar códigos de error HTTP 5xx en logs de Nginx",
    "Emitir sugerencia de rollback o hotfix en /workspace/reports/"
  ]
}
```

---

## Hand-off directo vs. Hub-and-Spoke

| Característica | Peer-to-Peer Hand-off | Hub-and-Spoke Router |
|---|---|---|
| Topología | Directa entre especialistas | Centralizada por un orquestador |
| Consumo de tokens | Menor (salta la reevaluación del hub) | Mayor (el router procesa cada entrega) |
| Control de desviaciones | Menor (confía en el juicio de cada agente) | Alto (valida contratos intermedios) |
| Manejo de fallos | Si un agente falla, debe saber a quién escalar | El router absorbe excepciones y reasigna |
| Caso óptimo | Pipelines deterministas de 2-3 pasos | Flujos complejos con bifurcaciones dinámicas |

> **PITFALL (correcto):** transferir un `thread_id` completo en lugar de un `handoff_token` sintetizado contamina la memoria a corto plazo del receptor: el modelo intentará resolver contradicciones pasadas en vez de ejecutar la tarea delegada.

---

## Implementación de la delegación estructurada

`delegate_subtask` valida el esquema (Pydantic), **verifica que los artefactos existan en disco**, persiste el contrato y construye el **seed prompt** mínimo para el receptor:

```python
import json
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field

WORKSPACE_ROOT = Path("/workspace")

class CleanHandoffPayload(BaseModel):
    task_id: str = Field(description="Identificador único del subobjetivo")
    target_agent: str = Field(description="Nombre del agente especialista destino")
    intent: str = Field(description="Propósito conciso de la tarea delegada")
    handoff_context: str = Field(description="Resumen de hechos consolidados, sin razonamiento previo")
    workspace_artifacts: List[str] = Field(description="Rutas relativas a archivos producidos")
    acceptance_criteria: List[str] = Field(description="Condiciones observables para dar por concluida la tarea")

def delegate_subtask(payload_raw: dict) -> dict:
    payload = CleanHandoffPayload(**payload_raw)
    # 1. Validar que los archivos referenciados existan en disco
    missing_files = [rel for rel in payload.workspace_artifacts
                     if not (WORKSPACE_ROOT / rel).is_file()]
    if missing_files:
        return {"status": "rejected",
                "error": f"Artefactos inexistentes en workspace: {missing_files}. Debe persistir los datos antes de delegar."}
    # 2. Persistir el contrato para trazabilidad
    handoff_dir = WORKSPACE_ROOT / "handoffs"; handoff_dir.mkdir(parents=True, exist_ok=True)
    handoff_file = handoff_dir / f"{payload.task_id}.json"
    with open(handoff_file, "w", encoding="utf-8") as f:
        json.dump(payload.model_dump(), f, indent=2, ensure_ascii=False)
    # 3. Orden de ejecución aislada para el receptor
    seed = (f"--- INICIO DE DELEGACIÓN [{payload.task_id}] ---\n"
        f"OBJETIVO: {payload.intent}\nCONTEXTO: {payload.handoff_context}\n"
        f"ARTEFACTOS DE ENTRADA: {', '.join(payload.workspace_artifacts)}\n"
        f"CRITERIOS DE ACEPTACIÓN:\n" + "\n".join([f"- {c}" for c in payload.acceptance_criteria]) + "\n"
        f"--- FIN DE DELEGACIÓN ---")
    return {"status": "dispatched", "target": payload.target_agent, "seed_prompt": seed,
            "handoff_record": str(handoff_file.relative_to(WORKSPACE_ROOT))}
```

Ejemplo (security_scanner → firewall_ops): el receptor recibe **~120 tokens de instrucciones nítidas** en vez de ~4.000 de transcripciones previas.

---

## Control de ciclo de vida: TTL, fallbacks y retorno

1. **Time-to-Live (TTL):** cada payload define una ventana máxima (`max_turns: 4` o `timeout_seconds: 90`); si el receptor la supera sin entregable, el runtime interrumpe el bucle.
2. **Bloqueo de redelegación circular:** el token incorpora una lista inmutable `delegation_chain: ["triage","sec_ops"]`; delegar a un nodo ya presente → rechazo inmediato.
3. **Payload de retorno:** al concluir/abortar, el receptor emite un bloque estandarizado (`status`, `execution_summary`, `output_artifacts`, `unmet_criteria`). Si `status: "failed"`, el emisor escala a humano o toma ruta alternativa en vez de congelar el flujo.

> **REMEMBER (correcto):** nunca permitir que un especialista devuelva **texto libre** como confirmación de fin de tarea. Exigir una **herramienta de resolución de contrato** (`resolve_handoff`) que garantice `status` y `output_artifacts` presentes.

### Check your understanding
**¿Cómo transferir de un agente de diagnóstico a un especialista en DB sin degradar rendimiento?**
- [x] **Empaquetar un contrato formal con objetivo, contexto sintetizado, criterios de aceptación y punteros a los archivos en disco.** ✅ (acierta)

---

## Ejercicio (`HandoffValidator`) - verificado

Rechaza traspasos circulares y con artefactos faltantes; genera el prompt mínimo. **Salida real de mi corrida** (idéntica a la del curso):
```text
Estado: True
Cadena actualizada: ['router_agent', 'postgres_specialist']

Prompt generado para el especialista:
IDENTIFICADOR: db_mig_01
MISIÓN: migrar_esquema
RESUMEN TÉCNICO: Se validó la sintaxis básica del dump en el paso anterior.
ARCHIVOS DE TRABAJO: dump.sql
CRITERIOS DE ÉXITO:
- Ejecutar script contra entorno staging
- Reportar número de tablas creadas
```
Y reenviar con `target_agent: router_agent` **aborta** con `Ciclo de delegación detectado`. El código corre tal cual.

---

## Resumen

La transferencia limpia sustituye el arrastre caótico de conversaciones por **contratos estructurados e inmutables**: tokens de traspaso, verificación de artefactos en disco y control estricto de la cadena de delegación. El paso siguiente es **centralizar la supervisión y auditoría del rendimiento de la flota**.

**UP NEXT · Lección 30 de 30:** *Supervisión Centralizada del Rendimiento Global*. **Última lección** - cierra el Módulo 6 y el curso.

---

## Preguntas abiertas del propio curso

1. ¿Cómo se gestiona si el receptor necesita el razonamiento original descartado?
2. ¿Persistir un artefacto en JSON vs. pasarlo serializado en el token?
3. ¿Cómo reporta el receptor criterios técnicamente imposibles de cumplir?
4. ¿Cuándo conviene hub-and-spoke sobre peer-to-peer?

(Anotadas. #2 conecta con L25; #4 con la tabla del propio material.)

---

## Notas de verificación (Kanam)

**Núcleo de ingeniería: sólido y correcto - y la delegación multiagente ES real en OpenClaw, con otra superficie:**

| El curso dice | OpenClaw real |
|---|---|
| Delegar un subobjetivo a otro agente | ✅ **Real:** los agentes se delegan vía **subagents** (`subagents.allowAgents`) y **`tools.agentToAgent`** (`docs/concepts/multi-agent.md`). |
| Payload estructurado en vez de reenviar el historial | ✅ Principio correcto (contexto limpio para el receptor). Coincide con la práctica de handoff del workspace. |
| Verificar artefactos en disco antes de delegar | ✅ Buen control determinista (coherente con L23). |
| **Detección de ciclos en la cadena de delegación** | ✅ **Principio correcto y valioso** (misma familia que `max_hops`/visited-nodes de L27). |
| TTL + payload de retorno estructurado (no texto libre) | ✅ Correcto y central; el **REMEMBER** (exigir `resolve_handoff`, no texto libre) es válido. |
| **Acierta el quiz.** | ✅ |
| **`HandoffValidator` corre tal cual**: verifiqué el caso válido + la excepción de ciclo. | ✅ |

**Lo que NO coincide con la instalación real:**
- ❌ **`delegate_task` / `resolve_handoff` / `handoff_token` / `delegation_chain`** como mecanismos nativos: **inventados** (no aparecen en docs). La delegación real es **`sessions_spawn`/subagents + `agentToAgent`**, con contrato propio (no un `handoff_token` formal).
- ❌ **`/workspace/tmp/...`, `/workspace/reports/`, `/workspace/handoffs/`**: rutas de ejemplo; `handoffs/` no es convención del producto.
- ❌ **`protocol_version: "1.2"`**: invención.
- ⚠️ **`max_turns` / `timeout_seconds` por handoff:** el concepto (TTL) es válido, pero el mecanismo real de acotación es el **timeout de ejecución del agente** (`agents.defaults.timeoutSeconds`) y los timeouts por turno, no un campo del token.

**Verificación ejecutable:**
- ✅ **El `HandoffValidator` del ejercicio corre tal cual** (Python + pydantic): reproducí `Estado: True` + cadena actualizada + el prompt limpio, y la **excepción de ciclo**. Una de las pocas lecciones correctas *y* ejecutables.

**Patrón (vigésimo noveno caso, con matiz fuerte):** quinta vez que **el tema existe** (delegación vía subagents/`agentToAgent`) y la **filosofía acierta** con fuerza (contrato estructurado, contexto limpio, verificación de artefactos, anti-ciclo, retorno estructurado). La fachada inventada: **`delegate_task`/`resolve_handoff`/`handoff_token`/`delegation_chain`**. Traducible: `sessions_spawn` + `agentToAgent` + contrato propio, no el token del curso. **Muy buena lección conceptualmente.**

**Nota de contexto (Módulo 6):** tras esta L29 el propio curso indica *"1 lesson left in Especialización y Coordinación Multiagente"* → Módulo 6 = 5 lecciones (L26-L30). Lección 30 (última): *Supervisión Centralizada del Rendimiento Global*.
