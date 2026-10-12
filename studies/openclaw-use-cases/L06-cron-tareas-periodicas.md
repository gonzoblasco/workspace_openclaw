# Módulo 2 · Lección 6 de 30: Configuración de Tareas Periódicas con Cron

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 2 - Tareas Programadas y Rutinas Autónomas
**Lección:** 6 de 30 · **abre el Módulo 2**
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo (2026-10-12), tratado como **dato externo** (sandbox). Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

Una tarea programada traslada al agente de un modelo **reactivo** (solo opera tras recibir un mensaje en Slack/Telegram) a uno **proactivo impulsado por el tiempo**. El scheduler interno evalúa **expresiones cron estándar** contra el reloj del sistema, instanciando un **contexto aislado de ejecución** con las herramientas y variables necesarias para un objetivo recurrente.

A diferencia del cron clásico Unix (un proceso efímero ejecuta un script y termina), una tarea cron en OpenClaw levanta un **subproceso conversacional completo**: el runtime inyecta un *prompt inicial sintético* en el modelo configurado, suministra acceso a las herramientas autorizadas y ejecuta un **bucle de acción** hasta agotar la tarea o alcanzar un límite de pasos.

---

## Anatomía del subsistema de cron

El demonio administra las tareas mediante un **registro declarativo**. Cada entrada define: *cuándo* activar, *qué* entorno de ejecución ocupar, y *qué* instrucciones guían la inferencia.

**Ciclo de vida de un trabajo cron (3 fases):**

1. **Evaluación de cadencia:** el despachador consulta el reloj frente a la máscara de 5 campos (`minuto hora día_mes mes día_semana`).
2. **Hidratación de contexto:** se levanta una **sesión efímera** que hereda las instrucciones maestras de `SOUL.md`, **sin arrastrar el historial sucio** de conversaciones pasadas (evita desbordes de ventana).
3. **Ejecución y emisión:** el modelo evalúa la directiva, invoca herramientas de lectura/análisis, y **canaliza su resolución** hacia un destino: almacenamiento local silencioso, actualización de estado, o notificación a un canal.

**Aislamiento = idempotencia.** Cada corrida arranca de un estado limpio: una revisión de métricas a las 08:00 no sufre interferencia si a las 07:59 un humano le pidió al agente escribir un poema en el canal de soporte.

---

## Sintaxis de definición y configuración

OpenClaw soporta la especificación clásica de cron **ampliada con metadatos orientados a agentes**. Una tarea no es un comando bash: es un **prompt estructurado** + una **política de entrega** + un **conjunto restringido de herramientas**.

```json
{
  "version": "1.0",
  "timezone": "America/Mexico_City",
  "jobs": [
    {
      "id": "health-check-api",
      "schedule": "*/15 * * * *",
      "enabled": true,
      "timeout_seconds": 90,
      "execution": {
        "model": "claude-3-5-sonnet",
        "temperature": 0.1,
        "tools_allowed": ["http_request", "fs_write"],
        "prompt": "Consulta https://api.internal.local/healthz. Si el status code es diferente de 200 o la latencia supera 1200ms, genera un log en /logs/incidents.json y notifica al canal.",
        "output": {
          "mode": "conditional_broadcast",
          "target_channel": "ops-alerts",
          "condition": "status != 200"
        }
      }
    },
    {
      "id": "sync-knowledge-index",
      "schedule": "0 2 * * *",
      "enabled": true,
      "timeout_seconds": 300,
      "execution": {
        "model": "claude-3-5-sonnet",
        "temperature": 0.0,
        "tools_allowed": ["fs_read", "fs_write", "ripgrep"],
        "prompt": "Escanea el directorio /docs en busca de archivos Markdown modificados en las últimas 24 horas y regenera el índice resumido en /docs/INDEX.md.",
        "output": { "mode": "silent" }
      }
    }
  ]
}
```

| Campo | Función |
|---|---|
| `schedule` | Formato cron de 5 campos. `*/15 * * * *` cada 15 min; `0 2 * * *` diario a las 02:00 según la `timezone` global. |
| `timeout_seconds` | Tiempo máximo de razonamiento + herramientas. Si la API tarda o el modelo no converge, el runtime **mata el subproceso**. |
| `tools_allowed` | **Principio de mínimo privilegio.** El health-check solo puede hacer HTTP y escribir logs; sin bash ni herramientas destructivas. |
| `output.mode` | `conditional_broadcast` (publica si se cumple `condition`), `silent` (solo archivos en disco), etc. |

> **PITFALL del curso:** una tarea cron **sin `timeout_seconds`** permite que un fallo de red deje la sesión abierta indefinidamente, consumiendo tokens en reintentos descontrolados. Establecer siempre un límite estricto.

---

## Validación y cálculo de ventanas de ejecución

Uno de los errores más frecuentes es el **desfase horario o solapamiento** de tareas intensivas. Si una tarea tarda 4 minutos y se programa `*/3` (cada 3 min), las instancias compiten por **locks de archivos** y cuotas de tokens.

Cuando la duración media supera el intervalo, OpenClaw activa por defecto una **política de descarte selectivo**: si la ejecución previa con el mismo `id` aún no liberó su lock, el disparo actual se **omite** y se emite un aviso en los registros de diagnóstico.

---

## Implementación paso a paso: rutina de auditoría

Script que interactúa con la **API de control del runtime** para registrar un trabajo, verificar su registro y simular el disparo:

```python
import time
import requests
import json

BASE_URL = "http://127.0.0.1:18789/api/v1"
HEADERS = {
    "Authorization": "Bearer oc_live_sk_8921a8f9c0e4",
    "Content-Type": "application/json"
}

audit_job_payload = {
    "id": "workspace-integrity-cron",
    "schedule": "0 */4 * * *",  # Cada 4 horas en punto
    "enabled": True,
    "timeout_seconds": 120,
    "execution": {
        "model": "claude-3-5-sonnet",
        "temperature": 0.0,
        "tools_allowed": ["fs_list", "fs_read", "fs_write"],
        "prompt": (
            "Examina /workspace/inbox. Si existen más de 50 archivos sin clasificar, "
            "genera una alerta resumida en /workspace/reports/backlog.json indicando "
            "los 5 nombres de archivo más antiguos."
        ),
        "output": {
            "mode": "conditional_broadcast",
            "target_channel": "dev-ops-feed",
            "condition": "backlog_count > 50"
        }
    }
}

def setup_and_trigger():
    print("[1/3] Registrando tarea periódica en OpenClaw...")
    res = requests.post(f"{BASE_URL}/cron/jobs", headers=HEADERS, data=json.dumps(audit_job_payload))
    if res.status_code not in (200, 201):
        raise RuntimeError(f"Fallo al registrar cron: {res.text}")
    print("      Tarea registrada satisfactoriamente:", res.json()["job_id"])

    print("[2/3] Verificando estado en el daemon...")
    job_info = requests.get(f"{BASE_URL}/cron/jobs/workspace-integrity-cron", headers=HEADERS).json()
    print(f"      Próxima ejecución calculada: {job_info['next_run_iso']}")

    print("[3/3] Disparando ejecución manual (dry-run/test trigger)...")
    trigger_res = requests.post(f"{BASE_URL}/cron/jobs/workspace-integrity-cron/trigger", headers=HEADERS)
    run_id = trigger_res.json()["run_id"]
    print(f"      Ejecución iniciada con run_id: {run_id}")

    time.sleep(3)
    run_status = requests.get(f"{BASE_URL}/cron/runs/{run_id}", headers=HEADERS).json()
    print("\n--- Resultado de la Ejecución ---")
    print("Estado:", run_status["status"])
    print("Herramientas invocadas:", run_status["tools_called"])
    print("Tokens consumidos:", run_status["tokens_used"])
    print("Acción de salida:", run_status["output_action"])

if __name__ == "__main__":
    setup_and_trigger()
```

Salida que muestra el curso (transición inmediata de estados):

```text
[1/3] Registrando tarea periódica en OpenClaw...
      Tarea registrada satisfactoriamente: workspace-integrity-cron
[2/3] Verificando estado en el daemon...
      Próxima ejecución calculada: 2025-05-18T12:00:00-06:00
[3/3] Disparando ejecución manual (dry-run/test trigger)...
      Ejecución iniciada con run_id: run_7f9b1c03e8
--- Resultado de la Ejecución ---
Estado: completed
Herramientas invocadas: ['fs_list', 'fs_read']
Tokens consumidos: 842
Acción de salida: omitted (backlog_count <= 50)
```

El agente listó `/workspace/inbox`, halló 12 elementos, evaluó `backlog_count > 50` y, al no cumplirse, **terminó limpio sin ruido** en el canal.

---

## Check your understanding

**¿Cuál es la forma segura y canónica de impedir que una tarea periódica de análisis de logs ejecute comandos shell o modifique el sistema de archivos?**

- [ ] Redactar el prompt indicando que no debe ejecutar comandos shell.
- [x] **Limitar el array `tools_allowed` únicamente a las herramientas requeridas.**
- [ ] Configurar un `timeout_seconds` más corto.
- [ ] Definir `output.mode` como `silent`.

---

## Control de concurrencia y persistencia de estado

Dos vectores de riesgo cuando conviven varias tareas: **colisión** de accesos concurrentes sobre el workspace y **pérdida de continuidad** entre ejecuciones.

Para las colisiones, el motor implementa **file-locking por exclusión mutua por identificador**. Si una rutina pesada sigue en progreso cuando expira el temporizador, se aplica la directiva de conflicto:

| Estrategia de conflicto | Comportamiento | Caso de uso típico |
|---|---|---|
| **skip** (por defecto) | Omite la nueva iteración; espera al próximo intervalo. | Indexación profunda, análisis no críticos. |
| **queue** | Encola la nueva corrida para arrancar tras liberar el lock. | Reconciliación de balances, transacciones. |
| **kill_previous** | Cancela el subproceso anterior; arranca con datos frescos. | Comprobaciones de latencia en tiempo real. |

**Persistencia:** a diferencia de los canales activos (memoria acumulada en el hilo), una tarea cron **no retiene un hilo perpetuo**. Lo que deba persistir entre ejecuciones se vuelca deliberadamente en **disco estructurado** (JSON/Markdown local) o en un almacén persistente. Si no, la siguiente sesión efímera arranca con **conocimiento nulo** de lo ocurrido.

> **REMEMBER del curso:** **nunca** usar la ventana conversacional de una tarea cron como almacén de memoria a largo plazo. Persistir métricas o marcas temporales en archivos locales dedicados si se necesita comparar variaciones entre corridas.

---

## Ejercicio práctico: monitor de cuotas de almacenamiento

Trabajo que corre cada hora, evalúa el consumo de espacio de la carpeta temporal y notifica **solo** si supera un umbral.

**1. Archivo de trabajo** (`cron/storage_guard.json`):

```json
{
  "id": "storage-guard-hourly",
  "schedule": "0 * * * *",
  "enabled": true,
  "timeout_seconds": 60,
  "execution": {
    "model": "claude-3-5-sonnet",
    "temperature": 0.0,
    "tools_allowed": ["fs_stat", "fs_read"],
    "prompt": "Comprueba el tamaño total acumulado de los archivos dentro de /tmp/agent_cache. Si el peso combinado supera los 200MB, genera un informe detallando los 3 archivos más pesados.",
    "output": {
      "mode": "conditional_broadcast",
      "target_channel": "infrastructure-alerts",
      "condition": "total_megabytes > 200"
    }
  }
}
```

**2. Carga y verificación en el daemon:**

```bash
openclaw cron register --config cron/storage_guard.json
openclaw cron list
```

Salida esperada:

```text
ID                      SCHEDULE     ENABLED   TIMEOUT   NEXT RUN (LOCAL)
storage-guard-hourly    0 * * * *    true      60s       2025-05-18 13:00:00
```

**3. Validar sin esperar la hora en punto:**

```bash
openclaw cron test storage-guard-hourly --dry-run
```

---

## Resumen

Las tareas cron convierten a OpenClaw en un **motor proactivo** que opera sin supervisión continua. Al **aislar cada invocación** en sesiones efímeras sin historial acumulado, **limitar permisos** con `tools_allowed` y **gestionar concurrencia** con políticas de descarte/encolamiento, el agente ejecuta rutinas de diagnóstico y mantenimiento con alta fiabilidad. Lo siguiente: coordinación de la monitorización continua con **heartbeats periódicos** de baja latencia.

**UP NEXT · Lección 7 de 30:** *Monitorización del Sistema Mediante Heartbeats Periódicos*. Faltan **4 lecciones** para cerrar el Módulo 2 (*Tareas Programadas y Rutinas Autónomas*).

---

## Preguntas abiertas del propio curso ("Can you answer these?")

1. ¿Cómo se sincronizan las zonas horarias si OpenClaw corre en un contenedor Docker con hora UTC?
2. ¿Qué pasa si una tarea falla por un error de sintaxis en el prompt del modelo?
3. ¿Cómo se gestiona el consumo de tokens en tareas que corren cada minuto?
4. ¿Es posible que una tarea cron dispare sub-agentes secundarios de forma autónoma?

(Anotadas para profundizar.)

---

## Notas de verificación (Kanam)

**Esta lección es de las más acertadas en su núcleo.** El scheduler de cron de OpenClaw es real y casi todos los conceptos mapean:

| El curso dice | OpenClaw real |
|---|---|
| Tareas programadas con cron de 5 campos | ✅ `openclaw cron` (alias de `openclaw automations`); cron de 5 o 6 campos vía `--cron` (parser: **croner**). |
| Zona horaria por tarea | ✅ `--tz America/New_York` (IANA); sin `--tz`, usa la tz del host. |
| Sesiones **aisladas** efímeras, sin historial | ✅ `--session isolated` = *"a dedicated agent turn with a fresh session"*. |
| Sin memoria de largo plazo entre corridas | ✅ Correcto: jobs aislados arrancan en limpio; persistir en disco. Es exactamente el **REMEMBER** del curso. |
| `timeout_seconds` por trabajo | ✅ `--timeout-seconds` (y watchdog por defecto: 60 min para agent-turn, 10 min para comandos, 5 min para scripts). |
| Allowlist de herramientas (mínimo privilegio) | ✅ `--tools exec,read`; `--tools ""` deshabilita todo. *"New jobs that can run tools always store an explicit tool policy."* |
| Modos de entrega (broadcast / silencioso) | ✅ Existen modos reales: **`announce`**, **`webhook`**, **`none`** (+ `--no-deliver`). |
| Corridas omitidas por solapamiento | ✅ Real: runs `skipped` (p. ej. preflight de modelo local caído) con contador de skips. |
| Disparo manual de prueba | ✅ `openclaw automations run <jobId>` (+ `--wait`, `--due`). |
| Prompt estructurado + política de entrega + tools | ✅ El payload real incluye `--prompt`, `--model`, `--tools`, delivery, sesión. |

**Extra real que el curso no menciona (mejora el diseño):**
- Las expresiones **top-of-hour se escalonan automáticamente hasta 5 min** para evitar picos (`--exact` para forzar, `--stagger 30s`).
- **día_mes + día_semana usan lógica OR** (Vixie/croner), no AND.
- `cron.skipMissedJobs: true` para no recuperar slots perdidos estando el Gateway offline.

**Lo que NO existe en la instalación real (fabricado):**
- ❌ **Los comandos del curso no existen:** `openclaw cron register --config ...` y `openclaw cron test ... --dry-run` → **no son subcomandos**. La CLI real ofrece `add/create`, `edit`, `list`, `get`, `run`, `runs`, `enable/disable`, `rm`, `show`, `status`. El "dry-run" se hace con `automations run`.
- ❌ **El archivo y el esquema son ficticios.** No hay `cron/jobs.json` versionable ni `openclaw.config.yaml` (el archivo real es `~/.openclaw/openclaw.json`, y los jobs viven en **SQLite**; el viejo `~/.openclaw/cron/jobs.json` solo se importa una vez con `doctor --fix`). Los campos `execution.tools_allowed`, `output.mode: conditional_broadcast/silent`, `output.condition` **no existen** con esos nombres (el real: `--tools`, delivery `announce/webhook/none`).
- ❌ **La API REST `/api/v1/cron/jobs` es inventada.** El puerto `18789` es real, pero para **webhooks** (`/hooks/agent`, `/hooks/wake`), no para un CRUD de cron. El token `oc_live_sk_8921a8f9c0e4` es ficticio. La interfaz real es la **CLI** (o el tool `automations`), no esa REST.
- ❌ **Las estrategias `skip`/`queue`/`kill_previous`** no están documentadas como tales: el comportamiento real es "skip" (runs `skipped`/coalescing) y disparo manual `--wait`; no hay una tabla de conflicto con esos tres modos.
- ❌ **`claude-3-5-sonnet` / `temperature`:** ejemplos irrelevantes para esta instalación (Ollama). El `--model` real debe resolver a un modelo permitido.

**Patrón (sexto caso):** el curso enseña **exactamente la arquitectura correcta** (scheduler, aislamiento efímero, allowlist, timeout, sin memoria en la ventana) sobre una **fachada de CLI/config/API inventada**. Es la más útil conceptualmente hasta ahora y la más "cercana" a la verdad; pero copiar el `jobs.json`, los comandos `register/test` o la REST **no funciona**. Traducir cada idea a la CLI real (`automations add/edit/run`, `--tools`, `--timeout-seconds`, delivery `announce/webhook/none`).

**Nota de cierre del Módulo 1 (contexto):** con la L05 quedó cerrado el Módulo 1 (*Asistentes de Mensajería Contextuales*). Esta L06 abre el **Módulo 2: Tareas Programadas y Rutinas Autónomas**, que según el propio curso tiene **5 lecciones** (faltan 4 tras esta).
