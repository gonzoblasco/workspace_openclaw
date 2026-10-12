# Módulo 2 · Lección 7 de 30: Monitorización del Sistema Mediante Heartbeats Periódicos

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 2 - Tareas Programadas y Rutinas Autónomas
**Lección:** 7 de 30
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo (2026-10-12), tratado como **dato externo** (sandbox). Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

Un heartbeat periódico es un **pulso temporal persistente** emitido a intervalos fijos para evaluar la salud del entorno de ejecución, verificar conectividades críticas y detectar anomalías antes de que degraden las operaciones del agente. A diferencia de las tareas cron (orientadas a ejecutar scripts puntuales a horas determinadas), el heartbeat funciona como un **electrocardiograma continuo** del sistema.

El pulso no se limita a escribir en un log: el agente evalúa la gravedad del fallo según políticas declarativas y puede **autocurar** el servicio o enviar **alertas enriquecidas** a los canales conectados.

---

## Anatomía de un ciclo de heartbeat

Cuatro fases secuenciales por cada intervalo (`pulse_interval`):

1. **Emisión:** el planificador genera un pulso.
2. **Sondeo de sondas:** conectores especializados recopilan memoria del host, latencia contra la API del LLM, cuotas de tokens y persistencia del socket (Telegram/Discord/Slack).
3. **Agregación de métricas.**
4. **Evaluación de umbrales:** si todo cae en cotas tolerables → estado `nominal` + actualización de telemetría local; si una métrica cruza un umbral crítico → protocolo de contingencia.

El lote de comprobaciones es **no bloqueante** para no penalizar el hilo principal del agente.

### Ciclo de decisión y remediación

El archivo central, según el curso, es **`heartbeat.json`** en `.openclaw/`:

```json
{
  "heartbeat": {
    "enabled": true,
    "pulse_interval_sec": 60,
    "max_consecutive_failures": 3,
    "probes": {
      "llm_endpoint": { "provider": "anthropic", "timeout_ms": 2500, "max_latency_ms": 4000 },
      "system_resources": { "max_memory_percent": 85, "max_disk_percent": 90 },
      "chat_gateways": { "channels": ["telegram_ops", "slack_alerts"], "ping_interval_sec": 120 }
    },
    "alerting": { "channel": "telegram_ops", "cooldown_minutes": 15 }
  }
}
```

`max_consecutive_failures` filtra fluctuaciones temporales: un error aislado **incrementa un contador** sin disparar alerta; solo al superar el umbral consecutivo el subsistema pasa de `DEGRADED` a `FAILING`.

---

## Monitor de latidos en Python

El curso presenta una clase `OpenClawHeartbeatMonitor` que sondea memoria del sistema (`psutil`), conectividad LLM (`requests`) y gateway, con despacho de alertas estructuradas:

```python
import os, time, psutil, requests
from typing import Dict, Any

class OpenClawHeartbeatMonitor:
    def __init__(self, interval_sec: int = 60, fail_threshold: int = 3):
        self.interval_sec = interval_sec
        self.fail_threshold = fail_threshold
        self.consecutive_failures: Dict[str, int] = {"memory": 0, "llm_ping": 0, "gateway": 0}

    def probe_system_memory(self) -> Dict[str, Any]:
        mem = psutil.virtual_memory()
        is_ok = mem.percent < 85.0
        return {"status": "healthy" if is_ok else "unhealthy",
                "percent_used": mem.percent,
                "available_mb": round(mem.available / (1024 * 1024), 2)}

    def probe_llm_connectivity(self) -> Dict[str, Any]:
        start = time.time()
        api_url = os.getenv("OPENCLAW_LLM_PING_URL", "https://api.anthropic.com/v1/models")
        headers = {"x-api-key": os.getenv("ANTHROPIC_API_KEY", "")}
        try:
            resp = requests.get(api_url, headers=headers, timeout=3.0)
            elapsed_ms = round((time.time() - start) * 1000, 2)
            is_ok = resp.status_code == 200 and elapsed_ms < 3000
            return {"status": "healthy" if is_ok else "unhealthy", "latency_ms": elapsed_ms}
        except requests.RequestException as e:
            return {"status": "unhealthy", "error": str(e), "latency_ms": None}

    def dispatch_alert(self, component: str, details: Dict[str, Any]) -> None:
        alert_payload = {"type": "HEARTBEAT_ALERT", "component": component,
                         "failures": self.consecutive_failures[component],
                         "details": details, "timestamp": time.time()}
        print(f"[ALERTA EMITIDA] Componente: {component} | Datos: {alert_payload}")

    def evaluate_pulse(self) -> None:
        probes = {"memory": self.probe_system_memory(), "llm_ping": self.probe_llm_connectivity()}
        for comp, res in probes.items():
            if res["status"] == "unhealthy":
                self.consecutive_failures[comp] += 1
                print(f"[WARN] Sonda '{comp}' anómala ({self.consecutive_failures[comp]}/{self.fail_threshold})")
                if self.consecutive_failures[comp] >= self.fail_threshold:
                    self.dispatch_alert(comp, res)
            else:
                if self.consecutive_failures[comp] > 0:
                    print(f"[INFO] Sonda '{comp}' recuperada a estado nominal.")
                self.consecutive_failures[comp] = 0

    def run_forever(self) -> None:
        print(f"Iniciando monitorización por heartbeat (intervalo: {self.interval_sec}s)...")
        while True:
            self.evaluate_pulse()
            time.sleep(self.interval_sec)

if __name__ == "__main__":
    monitor = OpenClawHeartbeatMonitor(interval_sec=10, fail_threshold=2)
    monitor.evaluate_pulse()
```

Salida que muestra el curso (todo nominal):

```text
[INFO] Evaluando pulso del sistema...
[INFO] Sonda 'memory': 72.1% de uso | 3824.50 MB disponibles.
[INFO] Sonda 'llm_ping': latencia 410.25 ms (HTTP 200).
[OK] Todas las sondas nominales. Latido registrado con éxito.
```

Y ante dos fallos consecutivos, evita la alarma en el primero y la dispara en el segundo.

---

## Control de oscilación (flapping) y ventanas de mitigación

Un riesgo de la monitorización de alta frecuencia es el **flapping**: un recurso bordeando el límite (p. ej. oscilando entre 84% y 86% de memoria), generando avalanchas de avisos que fatigan a la guardia.

Mitigación: **histéresis** + **ventanas de enfriamiento (cooldown)**. La histéresis exige que la métrica se recupere **sensiblemente por debajo** del umbral de disparo antes de volver a marcar `saludable` (si la alerta se activa al 85%, el componente no se declara nominal hasta bajar del 78%).

> **REMEMBER del curso:** un heartbeat debe monitorizar salud y actuar sobre la conectividad, **nunca** inyectar prompts de generación artificial ni tareas de usuario en la cola conversacional.

---

## Check your understanding

**Un agente envía alertas de sobrecarga de memoria cada 3 minutos porque el consumo oscila entre 79% y 81%. ¿Solución adecuada?**

- [ ] Migrar la comprobación a cron cada minuto.
- [x] **Implementar histéresis: umbral de disparo al 80% y umbral de recuperación inferior (p. ej. 70%).**
- [ ] Subir el límite crítico al 95%.
- [ ] Reiniciar el proceso cada vez que toque el 80%.

---

## Ejercicio: sonda de base de datos local

Sonda para verificar la integridad de la base SQLite de OpenClaw: no solo que exista, sino que responda a consultas rápidas en <100 ms. Archivo `probe_sqlite.py` dentro de `.openclaw/probes/`:

```python
import sqlite3
import time
from typing import Tuple, Dict, Any

def check_sqlite_health(db_path: str, timeout_ms: float = 100.0) -> Tuple[bool, Dict[str, Any]]:
    start_time = time.perf_counter()
    try:
        conn = sqlite3.connect(db_path, timeout=1.0)
        cursor = conn.cursor()
        cursor.execute("PRAGMA quick_check;")
        result = cursor.fetchone()
        conn.close()
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        if result and result[0] == "ok" and elapsed_ms <= timeout_ms:
            return True, {"latency_ms": round(elapsed_ms, 2), "status": "nominal"}
        else:
            return False, {"latency_ms": round(elapsed_ms, 2), "integrity": result[0] if result else "unknown"}
    except sqlite3.Error as e:
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return False, {"latency_ms": round(elapsed_ms, 2), "error": str(e)}

if __name__ == "__main__":
    db_file = "/tmp/openclaw_test.db"
    init_conn = sqlite3.connect(db_file)
    init_conn.execute("CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY, k TEXT, v TEXT);")
    init_conn.commit()
    init_conn.close()
    ok, info = check_sqlite_health(db_file)
    print(f"Salud de la base de datos: {ok} | Telemetría: {info}")
```

Salida esperada: `Salud de la base de datos: True | Telemetría: {'latency_ms': 0.42, 'status': 'nominal'}`.

---

## Resumen

El heartbeat periódico garantiza resiliencia operativa supervisando memoria, conectividad LLM y sockets de chat. Con umbrales con histéresis y contadores de fallos consecutivos, mitiga el flapping y ejecuta correcciones autónomas antes de alertar innecesariamente al operador.

**UP NEXT · Lección 8 de 30:** *Rutinas Nocturnas para Depurar Archivos Temporales*. Faltan **3 lecciones** para cerrar el Módulo 2.

---

## Preguntas abiertas del propio curso ("Can you answer these?")

1. ¿Cómo se sincronizan los heartbeats con las tareas batch de cron?
2. ¿Qué impacto tiene el heartbeat en la cuota RPM de la API del LLM?
3. ¿Cómo actúa OpenClaw si `heartbeat.json` tiene un error de sintaxis al arrancar?
4. ¿Es posible enviar la telemetría del heartbeat a Prometheus o Datadog?

(Anotadas para profundizar.)

---

## Notas de verificación (Kanam)

**El heartbeat SÍ existe en OpenClaw, pero su arquitectura real es casi la OPUESTA a la que describe el curso.** El curso lo pinta como un **daemon de sondas de infraestructura** (memoria del host vía `psutil`, latencia HTTP, umbrales, histéresis). El heartbeat real de OpenClaw es un **turno de agente programado que corre en la sesión principal** para que *el modelo* levante lo que necesite atención - no un monitor de recursos del sistema.

| El curso dice | OpenClaw real |
|---|---|
| Existe un "heartbeat" periódico | ✅ Sí, existe. |
| Config en `heartbeat.json` con `pulse_interval_sec`, `probes`, `alerting` | ❌ **No existe `heartbeat.json`.** La config vive en `openclaw.json`, bajo `agents.defaults.heartbeat` / `agents.entries.*.heartbeat`. Campos reales: `every`, `target`, `directPolicy`, `lightContext`, `isolatedSession`, `activeHours`, `prompt`, `timeoutSeconds`. |
| "Electrocardiograma continuo" con sondas de memoria/CPU/latencia | ❌ **No es un monitor de recursos.** Es un **turno de agente** (`every` default 30m; 1h con Anthropic OAuth). El modelo decide qué reportar. La doc es explícita: *"recurring tasks are automations, not heartbeat"*. |
| Sondas vía `psutil`, latencia contra `api.anthropic.com`, `requests` | ❌ No hay tales sondas. Además **`psutil` no está instalado aquí** (el script del curso no corre tal cual), y `requests` es incidental. |
| Estados `DEGRADED` → `FAILING`, `max_consecutive_failures` | ❌ No existen esos estados ni ese contador configurable. |
| Histéresis con umbral de disparo/recuperación | ❌ No es una feature de config del heartbeat (el "check your understanding" es conceptualmente sensato, pero **no mapea a OpenClaw**). |
| `OPENCLAW_LLM_PING_URL`, `ANTHROPIC_API_KEY` como env del heartbeat | ❌ Variables inventadas; no aparecen en la doc. |
| `.openclaw/probes/probe_sqlite.py` | ❌ No existe esa convención de directorio de sondas. |
| Cooldown / anti-flapping | ✅ **Existe `cooldown`** y guardas de flood/busy - pero como parte del runner del heartbeat real, no con la semántica del curso. |

**Contrato de respuesta real (que el curso omite y es lo importante):**
- Si nada requiere atención, el agente responde **`NO_REPLY`** (o usa el tool `heartbeat_respond` con `notify:false`).
- Para alertar: `heartbeat_respond` con `notify:true` + `notificationText`, o texto de alerta. Legado: `HEARTBEAT_OK`.
- `activeHours` se chequea en la zona horaria configurada (fuera de la ventana, se salta).
- `isolatedSession:true` = sesión nueva por corrida; `lightContext:true` = sin bootstrap.
- El **"REMEMBER" del curso se contradice con la realidad**: el heartbeat real **es** un turno de agente en la sesión principal, no "solo infraestructura". Lo que sí es cierto es su espíritu: no debe *inventar* trabajo recurrente (el prompt real dice literalmente *"Do not infer or repeat old tasks from prior chats"*).

**CLI real relacionado:** `openclaw cron list --all` (muestra `Heartbeat (agent-id)`), `openclaw cron scratch <jobId> --set`, `openclaw system heartbeat last --json`.

**Patrón (séptimo caso, el más marcado):** acá el curso no solo inventa la fachada (archivo/comandos) - **describe una arquitectura diferente**. Acierta el *concepto* (latido periódico, anti-flapping, no inventar tareas) y yerra el *modelo* (es un monitor de recursos, cuando OpenClaw usa un turno de agente con contrato `NO_REPLY`/`heartbeat_respond`). Es el caso donde más importa **no diseñar sobre el dibujo del curso**: si vas a implementar health-checks reales, van como **automatizaciones** (cron) con un payload de comando/script, no como "sondas de heartbeat".

**Nota de contexto (Módulo 2):** tras esta L07 el propio curso indica *"3 lessons left in Tareas Programadas y Rutinas Autónomas"* → Módulo 2 = 5 lecciones (L06-L10). Lección 8: *Rutinas Nocturnas para Depurar Archivos Temporales*.
