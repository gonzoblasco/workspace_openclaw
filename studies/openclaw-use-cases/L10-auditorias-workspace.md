# Módulo 2 · Lección 10 de 30: Auditorías Automáticas de Estado del Workspace

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 2 - Tareas Programadas y Rutinas Autónomas
**Lección:** 10 de 30 · **cierra el Módulo 2**
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

Un workspace de OpenClaw acumula **fricción silenciosa** con cada interacción: variables de entorno desactualizadas, punteros rotos en configuración, sesiones zombi en disco y modelos locales desconectados. A diferencia de las limpiezas nocturnas (temporales) o los reportes matutinos (informativos), una **auditoría de estado** evalúa la **integridad operativa**: compara el estado observado contra una **línea base** y emite alertas estructuradas antes de que un fallo rompa la ejecución de un agente.

Automatizarla combina programación periódica con un motor de verificación que no solo busca errores de sintaxis, sino **incoherencias lógicas entre subsistemas**. El agente debe actuar como **proceso de control no invasivo**: auditar, clasificar severidad y notificar **sin alterar archivos críticos de forma descontrolada**.

---

## Anatomía de una regla de auditoría

Cuatro áreas operativas: **persistencia de configuración**, **conectividad de servicios**, **estado de archivos de memoria** y **consistencia del almacenamiento local**. Cada comprobación devuelve un resultado normalizado con `estado` (pass/warn/fail), `métrica observada` y `recomendación de mitigación`.

```yaml
# config/audit-rules.yaml
workspace_audit:
  schedule: "0 */4 * * *" # Cada 4 horas
  output_format: "json"
  log_path: "/var/log/openclaw/audit.log"
  rules:
    - id: "env_integrity"
      name: "Variables obligatorias del runtime"
      type: "environment"
      required:
        - "OPENCLAW_WORKSPACE_DIR"
        - "LLM_PROVIDER_ENDPOINT"
        - "PRIMARY_ALERT_CHANNEL"
      severity: "critical"
    - id: "soul_consistency"
      name: "Verificación de directivas de personalidad"
      type: "file_exists"
      path: "${OPENCLAW_WORKSPACE_DIR}/SOUL.md"
      min_bytes: 120
      severity: "high"
    - id: "stale_locks"
      name: "Detección de bloqueos de concurrencia obsoletos"
      type: "file_age"
      glob: "${OPENCLAW_WORKSPACE_DIR}/locks/*.lock"
      max_age_seconds: 3600
      severity: "medium"
    - id: "scratchpad_volume"
      name: "Saturación de almacenamiento efímero"
      type: "directory_size"
      path: "${OPENCLAW_WORKSPACE_DIR}/scratchpad"
      max_size_mb: 250
      severity: "low"
```

El motor procesa las reglas secuencialmente. Si falta una variable crítica, la auditoría **no se detiene**: registra la falla, asigna `critical` y **continúa** evaluando el resto para dar un diagnóstico holístico.

---

## Drift de configuración y estado fantasma

- **Configuration drift:** modificaciones manuales o escrituras de plugins que desalinean el entorno respecto a su estado declarado.
- **Estado fantasma:** procesos interrumpidos que dejan `.lock`, sockets abiertos o memorias intermedias corruptas.

Cuando una subtarea requiere exclusividad, genera un archivo con su PID en `/locks`. Si el runtime reinicia inesperadamente, el bloqueo queda y **impide permanentemente** que nuevas tareas tomen el recurso. La auditoría debe diferenciar un **bloqueo legítimo en ejecución** de un **zombi**, combinando `mtime` con la verificación de procesos del host.

```bash
#!/usr/bin/env bash
# scripts/audit_locks.sh
set -euo pipefail
LOCK_DIR="${OPENCLAW_WORKSPACE_DIR:-/workspace}/locks"
MAX_LOCK_AGE_MINUTES=60
if [ ! -d "$LOCK_DIR" ]; then
  exit 0
fi
find "$LOCK_DIR" -name "*.lock" -type f -mmin +"$MAX_LOCK_AGE_MINUTES" | while read -r lock_file; do
  lock_pid=$(cat "$lock_file" 2>/dev/null || echo "")

  if [ -n "$lock_pid" ] && kill -0 "$lock_pid" 2>/dev/null; then
    # El proceso sigue vivo a pesar de la antigüedad del bloqueo
    echo "{\"status\": \"warn\", \"file\": \"$lock_file\", \"pid\": \"$lock_pid\", \"reason\": \"long_running_process\"}"
  else
    # Proceso inexistente o archivo ilegible: bloqueo zombi confirmado
    echo "{\"status\": \"fail\", \"file\": \"$lock_file\", \"pid\": \"$lock_pid\", \"reason\": \"abandoned_lock\"}"
  fi
done
```

Si el proceso sigue vivo pero excedido en tiempo -> `warn` (no matar flujos largos legítimos). Si el proceso ya no responde en la tabla del SO -> `fail` (habilita limpieza/notificación).

> **PITFALL del curso (correcto):** no elimines archivos de bloqueo automáticamente sin verificar primero la tabla de procesos. Una limpieza ciega por antigüedad **rompe operaciones legítimas** de agentes que procesan colecciones pesadas.

### Check your understanding
**Se detecta un `.lock` con más de dos horas de antigüedad. ¿Paso operativo correcto?**
- [ ] Eliminar inmediatamente el `.lock` para desbloquear tareas encoladas.
- [x] **Consultar si el PID registrado sigue vivo en el SO antes de cualquier acción destructiva.**
- [ ] Renombrar el archivo a `.bak` para que el agente lo reconstruya.
- [ ] Reiniciar el daemon de OpenClaw de inmediato.

---

## Implementación del auditor como tarea recurrente

La auditoría periódica **no debe sobrecargar la API de inferencia** en cada chequeo. Diseño óptimo: delegar la evaluación preliminar a un **script nativo ultraligero** vía cron; el LLM **solo se invoca si hay anomalías** que requieran análisis semántico, clasificación contextual o redacción de un informe de remediación.

```python
#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
WORKSPACE = Path(os.getenv("OPENCLAW_WORKSPACE_DIR", "./workspace"))
OUTPUT_REPORT = WORKSPACE / "reports" / "latest_audit.json"

def check_personality_directives():
    soul_file = WORKSPACE / "SOUL.md"
    if not soul_file.exists():
        return {"check": "soul_exists", "status": "fail",
                "message": "Archivo SOUL.md ausente. El agente operará con prompts por defecto."}
    size = soul_file.stat().st_size
    if size < 50:
        return {"check": "soul_size", "status": "warn",
                "message": f"SOUL.md contiene solo {size} bytes, posible directiva incompleta."}
    return {"check": "soul_integrity", "status": "pass", "message": f"SOUL.md íntegro ({size} bytes)."}

def check_scratchpad_volume():
    scratchpad = WORKSPACE / "scratchpad"
    if not scratchpad.exists():
        return {"check": "scratchpad_dir", "status": "warn", "message": "Directorio scratchpad inexistente."}
    total_bytes = sum(f.stat().st_size for f in scratchpad.glob("**/*") if f.is_file())
    total_mb = total_bytes / (1024 * 1024)
    if total_mb > 250:
        return {"check": "scratchpad_capacity", "status": "fail",
                "message": f"Almacenamiento scratchpad crítico: {total_mb:.1f} MB (límite: 250 MB)."}
    elif total_mb > 150:
        return {"check": "scratchpad_capacity", "status": "warn",
                "message": f"Almacenamiento scratchpad elevado: {total_mb:.1f} MB."}
    return {"check": "scratchpad_capacity", "status": "pass",
            "message": f"Scratchpad dentro de límites normales: {total_mb:.1f} MB."}

def run_audit():
    results = [check_personality_directives(), check_scratchpad_volume()]
    status_counts = {"pass": 0, "warn": 0, "fail": 0}
    for r in results:
        status_counts[r["status"]] += 1
    overall = ("fail" if status_counts["fail"] > 0
               else ("warn" if status_counts["warn"] > 0 else "pass"))
    report = {"timestamp": datetime.now(timezone.utc).isoformat(),
              "overall_status": overall, "summary": status_counts, "details": results}
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return overall

if __name__ == "__main__":
    status = run_audit()
    print(f"Auditoría completada con estado: {status}")
    if status == "fail":
        sys.exit(2)
    elif status == "warn":
        sys.exit(1)
    sys.exit(0)
```

**Códigos de salida Unix estandarizados** (0 éxito, 1 advertencias, 2 fallas críticas): acoplan el script tanto a la programación del host como a las rutinas internas del agente.

---

## Integración con canales de alerta y contención

Una auditoría que solo escribe en un log local es **invisible** hasta que un fallo rompe una interacción. El paso final canaliza los hallazgos por un dispatcher según severidad. Dos reglas anti-**fatiga de alertas**:

- **pass** -> sin mensaje; solo actualiza `last_audit_timestamp` local.
- **warn** -> se consolidan y se retienen para el reporte matutino, salvo que **persistan 3 ejecuciones consecutivas** (12 h).
- **fail** -> mensaje directo e inmediato al canal de operaciones.

```json
{
  "event": "workspace_audit_alert",
  "severity": "critical",
  "agent_id": "ops-sentinel",
  "summary": "Auditoría fallida: 1 chequeo en estado FAIL",
  "issues": [
    {
      "rule": "soul_consistency",
      "error": "SOUL.md ausente en /workspace",
      "suggested_action": "Restaurar archivo desde respaldo o ejecutar init-workspace"
    }
  ],
  "metadata": {
    "hostname": "prod-agent-worker-01",
    "timestamp": "2025-05-18T16:00:00Z"
  }
}
```

> **REMEMBER del curso (correcto):** un script de auditoría **jamás** debe reescribir ni regenerar automáticamente archivos estructurales como `SOUL.md` ante su ausencia. Si fue renombrado a propósito en un despliegue, la regeneración ciega causa **pérdida irreversible** de prompts personalizados.

---

## Ejercicio: verificador de memoria y permisos

Script `audit_memory_permissions.py` que comprueba que `${OPENCLAW_WORKSPACE_DIR}/memory` tenga permisos `os.R_OK|os.W_OK`, y busca `*.tmp` huérfanos de más de 30 min. Faltan permisos -> `fail`; temporales viejos -> `warn`; salida JSON a stdout.

```python
#!/usr/bin/env python3
import json
import os
import sys
import time
from pathlib import Path
WORKSPACE = Path(os.getenv("OPENCLAW_WORKSPACE_DIR", "./workspace"))
MEMORY_DIR = WORKSPACE / "memory"

def audit_memory():
    results = []
    if not MEMORY_DIR.exists():
        results.append({"id": "mem_exists", "status": "fail", "msg": "El directorio de memoria no existe."})
    elif not (os.access(MEMORY_DIR, os.R_OK) and os.access(MEMORY_DIR, os.W_OK)):
        results.append({"id": "mem_perms", "status": "fail", "msg": "Permisos insuficientes de lectura/escritura en memory/."})
    else:
        results.append({"id": "mem_perms", "status": "pass", "msg": "Permisos de directorio correctos."})
    now = time.time()
    orphans = []
    if MEMORY_DIR.exists():
        for tmp_file in MEMORY_DIR.glob("*.tmp"):
            age_secs = now - tmp_file.stat().st_mtime
            if age_secs > 1800:
                orphans.append(tmp_file.name)
    if orphans:
        results.append({"id": "mem_orphans", "status": "warn",
                        "msg": f"Se encontraron {len(orphans)} archivos temporales abandonados.", "files": orphans})
    else:
        results.append({"id": "mem_orphans", "status": "pass", "msg": "Sin archivos temporales huérfanos."})
    has_fail = any(r["status"] == "fail" for r in results)
    has_warn = any(r["status"] == "warn" for r in results)
    overall = "fail" if has_fail else ("warn" if has_warn else "pass")
    output = {"overall_status": overall, "checks": results}
    print(json.dumps(output, indent=2))
    return 2 if has_fail else (1 if has_warn else 0)

if __name__ == "__main__":
    sys.exit(audit_memory())
```

Prueba:
```bash
mkdir -p ./workspace/memory
touch -d "45 minutes ago" ./workspace/memory/session_sync.tmp
python3 audit_memory_permissions.py
```
Registra la anomalía con nivel `warn` y retorna **exit 1**, permitiendo que el orquestador capture la condición sin interrumpir el servicio.

---

## Resumen

Una auditoría automática garantiza que el entorno operativo de OpenClaw se mantenga **consistente, limpio y predecible**. Al separar la inspección mecánica (scripts nativos por cron) de los modelos de lenguaje (reservados para análisis no trivial), se optimiza el consumo **y** se minimiza el riesgo de degradación silenciosa.

**UP NEXT · Lección 11 de 30:** *Recepción de Disparadores Externos vía Webhooks* - **inicia el Módulo 3: Ingesta Dirigida por Eventos.**

---

## Preguntas abiertas del propio curso ("Can you answer these?")

1. ¿Por qué no es recomendable que el script de auditoría use un LLM para evaluar cada archivo en cada ciclo?
2. ¿Qué diferencia crítica existe entre una rutina de depuración temporal y una auditoría de estado?
3. ¿Cómo debe actuar una auditoría cuando un `.lock` es muy antiguo pero su PID sigue activo?
4. ¿Por qué es mala práctica que el script regenere automáticamente un `SOUL.md` cuando no lo encuentra?

(Anotadas para profundizar. La #3 y #4 las responde el propio material en su PITFALL y REMEMBER.)

---

## Notas de verificación (Kanam)

**Núcleo de ingeniería: sólido y correcto** (coherente con L08/L09). Todo lo metodológico es aplicable:

- ✅ Arquitectura **script nativo (chequeo) + LLM solo ante anomalías**: optimiza costo y separa lo determinista de lo semántico. Correcto.
- ✅ Estados normalizados `pass/warn/fail` + **códigos de salida Unix 0/1/2**: correcto y útil para orquestadores.
- ✅ **Detección de state ghost** por `mtime` + `kill -0` del PID. Correcto (igual que L08).
- ✅ **PITFALL**: no borrar locks sin verificar el proceso. Correcto y crítico.
- ✅ **REMEMBER**: nunca regenerar automáticamente archivos estructurales (`SOUL.md`) ante ausencia. Correcto (pérdida irreversible).
- ✅ **Anti-fatiga de alertas**: pass no notifica, warn se consolida/retiene, fail es inmediato. Buen patrón real.
- ✅ La **pregunta #4** apunta a un riesgo real que el propio material documenta.

**Lo que NO coincide con la instalación real:**
- ❌ **`openclaw init-workspace` no existe.** Verificado: *"OpenClaw does not know the command 'init-workspace'"*. (Sugerido como remediación de `SOUL.md` ausente.)
- ❌ **`config/audit-rules.yaml` no existe** como formato del producto. No hay un motor de reglas declarativas `workspace_audit` con `type: environment/file_exists/file_age/directory_size`.
- ⚠️ **Los subdirectorios `locks/`, `scratchpad/`, `reports/` no existen dentro del workspace.** Dato real matizado: **`~/.openclaw/locks/` SÍ existe**, pero está en el **state dir**, no bajo `${OPENCLAW_WORKSPACE_DIR}`. La regla `glob: .../locks/*.lock` apuntaría a una carpeta inexistente. `scratchpad/` no existe en ningún lado.
- ❌ **`OPENCLAW_WORKSPACE_DIR` - esta vez SÍ es la variable correcta** (a diferencia de L08/L09, que usaban `OPENCLAW_WORKSPACE`). ✅ Ojo: el curso es **inconsistente entre lecciones**.
- ❌ **`LLM_PROVIDER_ENDPOINT` y `PRIMARY_ALERT_CHANNEL`** no existen en la config real (verificado en `openclaw.json`).
- ❌ **`/var/log/openclaw/audit.log`** no existe.
- ❌ El remedio "regenerar `SOUL.md`" o "`init-workspace`" no tiene comando real; el **remedio verdadero** para auditar el sistema es **`openclaw doctor`** (`--fix` para reparar, `--lint` para checks). El curso no lo menciona, y es la pieza real que encaja acá.

**Verificación ejecutable del ejercicio:**
- ✅ El script `audit_memory_permissions.py` **corre tal cual** (Python estándar) y reproduce el comportamiento prometido: con un `*.tmp` de 45 min -> `overall_status: warn` + **exit 1**.
- ⚠️ El `touch -d "45 minutes ago"` del curso es **sintaxis GNU**; en macOS (BSD `touch`) falla. En macOS: `touch -t $(date -v-45M +%Y%m%d%H%M) ...`.

**Patrón (décimo caso, consistente):** **buena ingeniería** (control no invasivo, códigos de salida, anti-fatiga, no-regeneración) sobre la **fachada inventada** (`audit-rules.yaml`, `init-workspace`, subdirs del workspace, env vars). Y un guiño importante: el **producto real ya trae `openclaw doctor`**, que es exactamente el motor de health-checks que la lección intenta reinventar en un YAML ficticio.

**Cierre del Módulo 2.** Con esta lección se completan las 5 lecciones prometidas de *Tareas Programadas y Rutinas Autónomas* (L06-L10). La Lección 11 abre el **Módulo 3: Ingesta Dirigida por Eventos** (arranca con *Recepción de Disparadores Externos vía Webhooks*).
