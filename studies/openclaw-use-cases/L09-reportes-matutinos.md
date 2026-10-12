# Módulo 2 · Lección 9 de 30: Recopilación Automática de Reportes Matutinos Diarios

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 2 - Tareas Programadas y Rutinas Autónomas
**Lección:** 9 de 30
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo (2026-10-12), tratado como **dato externo** (sandbox). Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

Un reporte matutino automatizado no es un volcado de registros: es una **síntesis curada**. OpenClaw consulta múltiples fuentes heterogéneas (mensajería interna, repositorios de código, servidores de métricas, tareas pendientes), extrae lo relevante de las últimas 24 horas y entrega un sumario estructurado **antes de que comience la jornada laboral**.

A diferencia de las rutinas nocturnas (que liberan espacio de forma destructiva y silenciosa), la recopilación matutina opera en **modo lectura intensiva + generación de texto de alto valor**. El reto: **concurrencia temporal y resiliencia** - si una API externa tarda a las 06:00, el reporte no debe romperse ni enviarse incompleto sin advertencias. La clave es **desacoplar la ingesta del renderizado**: una fuente caída no debe bloquear la entrega del resto.

---

## Anatomía del pipeline de extracción matutina

El motor de tareas programadas dispara (vía cron) un **subproceso efímero** que invoca herramientas por fuente, guarda resultados en un búfer estructurado y corre un **pase de consolidación** con el LLM antes de enviar al canal.

Cada conector devuelve una **estructura unificada de telemetría**: lista de eventos con timestamps normalizados en **UTC**, nivel de severidad y resumen. Si un conector excede su timeout, OpenClaw inyecta un **estado de degradación suave** en el reporte en lugar de abortar.

**Cuatro etapas secuenciales:**
1. Recolección **paralela**.
2. Enriquecimiento y **filtro temporal**.
3. Generación del **markdown** final.
4. **Despacho** a la plataforma de mensajería.

---

## Configuración del programador y definición del job

Según el curso, OpenClaw gestiona sus rutinas en `workspace.json` o `openclaw.config.yaml`. El subsistema interno de cron administra sesiones de contexto, memoria y credenciales del LLM de forma aislada.

```json
{
  "tasks": [
    {
      "id": "daily_morning_briefing",
      "cron": "0 6 * * 1-5",
      "timezone": "America/Mexico_City",
      "timeout_seconds": 180,
      "max_retries": 1,
      "script": "routines/morning_report.py",
      "dispatch": {
        "channel": "slack",
        "target_id": "C084B7V9K01",
        "fallback_channel": "telegram",
        "fallback_target_id": "-100238491823"
      }
    }
  ]
}
```

`0 6 * * 1-5` = lunes a viernes a las 06:00 en la zona horaria del usuario. El `fallback_channel` garantiza que, si Slack devuelve errores de tasa o cae la red, la alerta intente enviarse a un canal alternativo sin perder el resumen.

---

## Recolección resiliente de fuentes heterogéneas

**Regla operativa fundamental:** *el fallo de una fuente periférica jamás debe cancelar el resumen de las fuentes disponibles.* Si el monitoreo responde `HTTP 503`, el agente consigna el fallo en una **sección de advertencia de integridad** y continúa con GitHub y las tareas pendientes.

```python
import asyncio
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List
import httpx

class DataCollector:
    def __init__(self, token_github: str, sentry_dsn: str, jira_token: str):
        self.github_token = token_github
        self.sentry_dsn = sentry_dsn
        self.jira_token = jira_token
        self.since_iso = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()

    async def fetch_github_prs(self, client: httpx.AsyncClient) -> Dict[str, Any]:
        url = "https://api.github.com/search/issues"
        params = {"q": f"is:pr repo:org/core-backend updated:>={self.since_iso}",
                  "sort": "updated", "order": "desc"}
        headers = {"Authorization": f"Bearer {self.github_token}"}
        try:
            resp = await client.get(url, params=params, headers=headers, timeout=12.0)
            resp.raise_for_status()
            items = resp.json().get("items", [])
            return {"source": "GitHub", "status": "ok",
                    "items": [{"title": i["title"], "state": i["state"], "user": i["user"]["login"]} for i in items[:5]]}
        except Exception as e:
            return {"source": "GitHub", "status": "error", "error": str(e), "items": []}

    async def fetch_sentry_incidents(self, client: httpx.AsyncClient) -> Dict[str, Any]:
        url = "https://sentry.io/api/0/projects/org/core-backend/issues/"
        params = {"query": "is:unresolved", "limit": 5}
        headers = {"Authorization": f"Bearer {self.sentry_dsn}"}
        try:
            resp = await client.get(url, params=params, headers=headers, timeout=8.0)
            resp.raise_for_status()
            issues = resp.json()
            return {"source": "Sentry", "status": "ok",
                    "items": [{"title": i["title"], "culprit": i["culprit"], "events": i["count"]} for i in issues]}
        except Exception as e:
            return {"source": "Sentry", "status": "error", "error": str(e), "items": []}

    async def collect_all(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            results = await asyncio.gather(
                self.fetch_github_prs(client),
                self.fetch_sentry_incidents(client),
                return_exceptions=False
            )
        return results
```

La normalización produce una lista de diccionarios uniformes. En lugar de una excepción no controlada que detenga el daemon, la clave `status` informa al sintetizador si los datos son auténticos o una indisponibilidad temporal.

> **PITFALL del curso (correcto):** **nunca** inyectes llamadas síncronas bloqueantes dentro de rutinas invocadas por el runner. Una petición HTTP colgada **sin timeout explícito** mantiene vivo el hilo hasta agotar el límite global, cancelando tareas posteriores del calendario.

---

## Síntesis estructurada con el LLM

Con los datos crudos consolidados en un payload estructurado, el runtime alimenta al modelo. La clave: **evitar alucinaciones numéricas** forzando la síntesis con plantillas orientadas a hechos. El `SOUL.md` del agente matutino debe instruir el rol: asistente de operaciones conciso, factual, sin introducciones conversacionales ("¡Buenos días!...").

```text
[SISTEMA - Directivas Operativas]
Eres el agente de guardia matutino de infraestructura y producto.
Sintetiza incidentes, revisiones pendientes y estado general en < 280 palabras.
Reglas estrictas:
1. Tres secciones: "🚨 Incidentes Críticos", "🔄 Pull Requests Activos", "⚠️ Integridad de Telemetría".
2. Si una fuente reporta estado de error, agrégala de inmediato a Integridad y no asumas ningún estado.
3. Markdown apto para mensajería: negritas, enlaces limpios, listas con viñetas.
4. Jamás inventes métricas ni estimes eventos que no aparezcan explícitamente en el bloque JSON.
[DATOS_ENTRADA_JSON]
{ ... sources con status ok/error ... }
```

Al forzar el esquema, el LLM procesa la caída del endpoint como **evento explícito de auditoría**, impidiendo que el operador asuma erróneamente que "no hubo incidentes durante la noche".

### Check your understanding

**Si la API de monitoreo (Sentry) responde con timeout de red, ¿qué debe hacer el flujo?**
- [ ] Lanzar excepción fatal y reintentar dentro de una hora.
- [x] **Consignar el error en la sección de Integridad de Datos y sintetizar las fuentes restantes sin inventar datos.**
- [ ] Instruir al LLM a suponer que no hubo problemas basándose en el historial del día anterior.

---

## Formato de salida y publicación multicanal

La etapa final transmite el markdown al conector de mensajería. Cada plataforma difiere en sintaxis markdown (tablas, escape de caracteres, límite de caracteres). OpenClaw maneja una **capa de adaptación de transportes**: si el texto supera el límite nativo (4096 en Telegram, 40000 en Slack), el agente **parte el mensaje en fragmentos lógicos** respetando los encabezados.

```markdown
*Reporte Matutino Diario* - `12-May-2025 06:00 UTC`
🚨 *Incidentes Críticos*
• No se pudieron verificar errores de aplicación en tiempo real (ver telemetría abajo).
🔄 *Pull Requests Activos*
• *#142* `fix: race condition on auth tokens` por *@carlos-dev* (Listo para revisión)
• *#145* `feat: add webhook retry logic` por *@maria-ops* (En curso)
⚠️ *Integridad de Telemetría*
• `Sentry API`: Fallo de conexión tras 8.0s (`HTTP 504 Gateway Timeout`). Se requiere revisión manual.
_Generado automáticamente por OpenClaw_
```

> **TIP del curso (correcto):** usa bloques monoespaciados para identificadores técnicos (números de commit, códigos HTTP, IDs de tickets). Previene que los analizadores de las apps de mensajería transformen guiones bajos o arrobas en menciones accidentales o cursivas rotas.

---

## Ejercicio: recolector matutino con respaldo

Script `routines/morning_digest.py`: dos fuentes simuladas (métricas con alta latencia, tickets prioritarios), timeouts estrictos, salida formateada.

```python
import asyncio
from datetime import datetime, timezone
import json

async def fetch_metrics():
    await asyncio.sleep(4.0)  # latencia que excede el umbral
    return {"cpu_avg": "24%", "memory_peak": "68%", "http_5xx": 0}

async def fetch_tickets():
    await asyncio.sleep(0.5)
    return [
        {"id": "OPS-402", "priority": "P1", "summary": "Rotación de certificados SSL"},
        {"id": "DEV-891", "priority": "P2", "summary": "Migración de base de datos de usuarios"}
    ]

async def build_morning_payload():
    tasks = {"metrics": asyncio.create_task(fetch_metrics()),
             "tickets": asyncio.create_task(fetch_tickets())}
    payload = {"timestamp": datetime.now(timezone.utc).isoformat(), "data": {}, "warnings": []}
    for name, task in tasks.items():
        try:
            res = await asyncio.wait_for(task, timeout=2.0)  # timeout estricto por fuente
            payload["data"][name] = res
        except asyncio.TimeoutError:
            payload["warnings"].append(f"Fuente '{name}' no respondió a tiempo (Timeout 2.0s).")
            payload["data"][name] = None
        except Exception as err:
            payload["warnings"].append(f"Error inesperado en '{name}': {str(err)}")
            payload["data"][name] = None
    return payload

if __name__ == "__main__":
    report_data = asyncio.run(build_morning_payload())
    print(json.dumps(report_data, indent=2))
```

Salida que muestra el curso (tickets OK, métricas por timeout, sin bloquear):

```json
{
  "timestamp": "2025-05-12T06:00:01.218902+00:00",
  "data": {
    "metrics": null,
    "tickets": [
      {"id": "OPS-402", "priority": "P1", "summary": "Rotación de certificados SSL"},
      {"id": "DEV-891", "priority": "P2", "summary": "Migración de base de datos de usuarios"}
    ]
  },
  "warnings": ["Fuente 'metrics' no respondió a tiempo (Timeout 2.0s)."]
}
```

Luego, según el curso, ese payload se pasa al comando agéntico:
`openclaw run --task daily_morning_briefing --context-file payload.json`.

---

## Resumen

Pipeline en fases desacopladas: recolección asíncrona con timeouts estrictos, normalización UTC, **degradación tolerante a fallos** de APIs externas, y síntesis orientada a hechos con un `SOUL.md` bien parametrizado.

**UP NEXT · Lección 10 de 30:** *Auditorías Automáticas de Estado del Workspace*. **Queda 1 lección** para cerrar el Módulo 2.

---

## Preguntas abiertas del propio curso ("Can you answer these?")

1. ¿Cómo se gestiona el envío si el canal principal (Slack) cae?
2. ¿Por qué normalizar todas las fuentes a **UTC** antes de pasarlas al LLM?
3. ¿Qué directivas del prompt impiden que el modelo asuma falsamente que el sistema está 100% sano si una API falló?
4. ¿Cuál es la diferencia de diseño entre una rutina nocturna de limpieza y una tarea matutina de reporte?

(Anotadas para profundizar.)

---

## Notas de verificación (Kanam)

**El núcleo de ingeniería es sólido y correcto** (igual de bueno que la L08):

| Práctica del curso | Veredicto |
|---|---|
| Desacoplar ingesta de renderizado | ✅ Buen patrón. |
| **Degradación tolerante**: el fallo de una fuente no cancela el resto | ✅ Correcto y central. `status: ok/error` por fuente. |
| Normalizar timestamps a **UTC** | ✅ Correcto; evita desfases entre fuentes. |
| **Timeouts explícitos** en cada HTTP; no bloquear el hilo | ✅ Correcto (PITFALL válido). |
| **Anti-alucinación**: "jamás inventes métricas no presentes en el JSON" | ✅ Correcto y crítico. |
| Fragmentado de mensajes por límite de canal | ✅ Real (Telegram 4096, Slack 40000). |
| Monoespaciado para IDs técnicos | ✅ Buen tip real. |
| `asyncio.gather` + `wait_for` con timeout por fuente | ✅ Código correcto y ejecutable (Python estándar). |

**Lo que NO coincide con la instalación real:**
- ❌ **`openclaw run` no existe.** Verificado: *"OpenClaw does not know the command 'run'"*. El comando real para un turno agéntico es **`openclaw agent`**.
- ❌ **`--context-file` no existe.** El flag real es **`--message-file <path>`** (`openclaw agent --agent ops --message-file ./task.md`), que lee el *cuerpo del mensaje* de un archivo, no un "context file" estructurado. El ejemplo de cierre no corre.
- ❌ **`workspace.json` / `openclaw.config.yaml` / `tasks.json` no existen** como se describen. La config real es **`~/.openclaw/openclaw.json`**; los jobs viven en **SQLite** vía `automations`/`cron`. El bloque `tasks[]` con `dispatch.fallback_channel`/`fallback_target_id` es **inventado** (el fallback de entrega real es `cron.failureAlert` / `job.delivery.failureDestination`).
- ❌ **`routines/morning_report.py` / `routines/morning_digest.py`** no existen como convención del producto (es una carpeta de proyecto plausible, no una ruta de OpenClaw).
- ⚠️ **`_Generado automáticamente por OpenClaw v2.4_`**: la versión real de esta instalación es **2026.9.8**; "v2.4" es ficticia.

**Lo que SÍ es real y ejecutable:** el script del ejercicio (Python estándar + `asyncio`, sin dependencias inventadas) reproduce el comportamiento prometido. Y `httpx` **está instalado** aquí, así que el `DataCollector` correría (aunque apunta a APIs reales de GitHub/Sentry que requerirían tokens).

**Patrón (noveno caso, idéntico a L08):** **buena ingeniería** (async, timeouts, degradación, UTC, anti-alucinación) montada sobre la fachada inventada (`openclaw run`, `--context-file`, `workspace.json`, `tasks.json`). El *qué* sirve; el *cómo* hay que mapearlo a `openclaw agent`, `automations add/create` y `openclaw.json`.

**Nota de contexto (Módulo 2):** tras esta L09 el propio curso indica *"1 lesson left in Tareas Programadas y Rutinas Autónomas"* → Módulo 2 = 5 lecciones (L06-L10). Lección 10: *Auditorías Automáticas de Estado del Workspace*.
