# Módulo 2 · Lección 8 de 30: Rutinas Nocturnas para Depurar Archivos Temporales

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 2 - Tareas Programadas y Rutinas Autónomas
**Lección:** 8 de 30
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo (2026-10-12), tratado como **dato externo** (sandbox). Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

El agente genera artefactos continuos (audios transcodificados, descargas intermedias, vistas previas, volcados de depuración) que saturan el disco si no se gestionan. La **ventana nocturna** (baja concurrencia) es el entorno idóneo para depurar sin competir por cómputo ni bloquear transacciones activas.

Una rutina nocturna **no es un `rm -rf` a ciegas**: un agente puede tener descriptores de archivo abiertos, temporales en fases intermedias o bloqueos atómicos sobre cachés. La depuración debe seguir **reglas de retención por marcas temporales**, distinguir datos efímeros de metadatos persistentes, y **registrar métricas de espacio liberado**.

---

## Anatomía del almacenamiento temporal en OpenClaw

Según el curso, los archivos no persistentes viven en un subárbol dedicado del workspace, típicamente bajo **`.openclaw/tmp/`**, con categorías de ciclo de vida diferenciado:

| Subdirectorio | Contenido típico | Política de retención nocturna |
|---|---|---|
| `media/` | Audios `.ogg`, imágenes de canales de chat | Eliminar con `atime > 24h` |
| `tool_runs/` | Salidas de subprocesos, scripts generados | Eliminar ejecuciones finalizadas `> 12h` |
| `sessions/` | Cachés de contexto serializadas | Conservar activas; purgar cerradas |
| `locks/` | Marcadores de concurrencia y semáforos | Purgar huérfanos con timeout vencido |

Para evitar borrar un archivo en uso, la rutina evalúa **`mtime` y `atime`**, y verifica la ausencia de **descriptores activos**.

---

## Pipeline de depuración selectiva

Riesgo principal: romper tareas en ejecución en segundo plano. Si un proceso hijo transcribe un audio de 20 MB y la rutina borra el intermedio a mitad del cálculo, la herramienta lanza un error de descriptor huérfano (`ENOENT`).

### Script de depuración (Python)

Resuelve `OPENCLAW_WORKSPACE` y recorre cada carpeta aplicando umbrales:

```python
#!/usr/bin/env python3
import os
import sys
import time
import subprocess
from pathlib import Path

# Definición de umbrales en segundos por categoría
RETENTION_POLICIES = {
    "media": 86400,        # 24 horas para audios y renders
    "tool_runs": 43200,    # 12 horas para salidas de comandos
    "locks": 3600,         # 1 hora para bloqueos estancados
}

def is_file_open(path: Path) -> bool:
    """Verifica si un proceso del sistema tiene descriptores abiertos sobre el archivo."""
    try:
        # fuser retorna código 0 si el archivo está en uso por algún proceso
        result = subprocess.run(
            ["fuser", "-s", str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except FileNotFoundError:
        # Fallback seguro si fuser no está disponible en la imagen base
        return False

def clean_temporary_directory(workspace_path: Path) -> dict:
    now = time.time()
    tmp_root = workspace_path / ".openclaw" / "tmp"
    stats = {"inspected": 0, "deleted": 0, "skipped_in_use": 0, "bytes_reclaimed": 0}
    if not tmp_root.exists():
        return stats
    for category, ttl_seconds in RETENTION_POLICIES.items():
        category_dir = tmp_root / category
        if not category_dir.is_dir():
            continue
        for item in category_dir.iterdir():
            if not item.is_file():
                continue
            stats["inspected"] += 1
            file_stat = item.stat()
            file_age = now - max(file_stat.st_atime, file_stat.st_mtime)
            if file_age > ttl_seconds:
                if is_file_open(item):
                    stats["skipped_in_use"] += 1
                    continue
                size = file_stat.st_size
                try:
                    item.unlink()
                    stats["deleted"] += 1
                    stats["bytes_reclaimed"] += size
                except OSError as err:
                    print(f"Error purgando {item.name}: {err}", file=sys.stderr)
    return stats

if __name__ == "__main__":
    workspace_env = os.environ.get("OPENCLAW_WORKSPACE", ".")
    workspace = Path(workspace_env).resolve()
    report = clean_temporary_directory(workspace)
    mb_reclaimed = report["bytes_reclaimed"] / (1024 * 1024)
    print(f"Depuración finalizada. Inspeccionados: {report['inspected']} | "
          f"Borrados: {report['deleted']} | Bloqueados: {report['skipped_in_use']} | "
          f"Espacio liberado: {mb_reclaimed:.2f} MB")
```

Salida que muestra el curso:

```text
Depuración finalizada. Inspeccionados: 142 | Borrados: 118 | Bloqueados: 3 | Espacio liberado: 487.35 MB
```

Los 3 "bloqueados" serían transcodificaciones activas que `is_file_open` evitó truncar.

### PITFALL del curso (correcto y valioso)

> **Nunca uses `st_ctime` para evaluar la antigüedad de un temporal en Linux.** En POSIX, `st_ctime` es el **cambio de metadatos/inodo**, no la creación. Usar el máximo entre `st_atime` (último acceso) y `st_mtime` (última modificación) garantiza que un archivo leído recientemente no se considere obsoleto.

---

## Check your understanding

**Un subproceso está transcodificando un audio descargado hace 26h bajo `.openclaw/tmp/media/`. ¿Qué decide la rutina y por qué?**

- [ ] Se elimina porque su `mtime` superó las 24h, provocando un error en ffmpeg.
- [x] **La rutina omite el archivo porque `is_file_open` detecta el descriptor abierto vía `fuser`, preservándolo hasta la próxima noche.**
- [ ] OpenClaw suspende la ejecución de ffmpeg de forma atómica para purgar el contenido.
- [ ] Se borra porque la política `media` tiene prioridad sobre las herramientas del agente.

---

## Integración en el orquestador

Según el curso, OpenClaw gestiona rutinas recurrentes mediante **`tasks.json`** en la raíz del workspace, o por bloques con **triggers cron**:

```json
{
  "tasks": [
    {
      "id": "nightly-cleanup-tmp",
      "name": "Depuración nocturna de temporales",
      "schedule": "0 3 * * *",
      "timeout_seconds": 300,
      "command": "python3 tools/clean_tmp.py",
      "env": { "OPENCLAW_WORKSPACE": "${WORKSPACE_DIR}" },
      "on_success": { "log_level": "info", "emit_event": "system:tmp_cleaned" },
      "on_failure": {
        "alert_channel": "ops-alerts",
        "retry": { "max_attempts": 2, "backoff_seconds": 60 }
      }
    }
  ]
}
```

`0 3 * * *` programa a las 03:00 hora local, minimizando impacto sobre sesiones de mensajería y evitando solaparse con los heartbeats.

---

## Gestión de bloqueos huérfanos

Un caso crítico: acumulación de `.lock` en `.openclaw/tmp/locks/`. Si un subproceso muere por OOM killer o corte de red, el `.lock` queda para siempre y bloquea futuras adquisiciones.

```python
def clean_orphaned_locks(locks_dir: Path, lock_timeout_seconds: int = 3600) -> int:
    """Elimina bloqueos huérfanos verificando la vigencia del PID asociado."""
    cleared = 0
    now = time.time()
    if not locks_dir.exists():
        return cleared
    for lock_file in locks_dir.glob("*.lock"):
        file_age = now - lock_file.stat().st_mtime
        if file_age <= lock_timeout_seconds:
            continue
        try:
            # Los bloqueos de OpenClaw registran el PID en su contenido
            pid_str = lock_file.read_text().strip()
            if pid_str.isdigit():
                pid = int(pid_str)
                # kill -0 no envía señal real; comprueba si el proceso vive
                os.kill(pid, 0)
                # Si no lanza OSError, el proceso sigue vivo: no tocar
                continue
        except ProcessLookupError:
            # El proceso ya no existe: el lock es huérfano
            pass
        except OSError:
            # Permiso denegado u otro fallo del sistema
            pass
        try:
            lock_file.unlink()
            cleared += 1
        except OSError:
            pass
    return cleared
```

> **REMEMBER del curso (correcto):** un `.lock` **nunca** se borra solo por tiempo transcurrido; hay que verificar que el PID que lo creó ya no esté en la tabla de procesos. `os.kill(pid, 0)` valida la existencia del proceso sin enviar señal.

---

## Ejercicio: depuración de cachés con reporte estructurado

Purga `.openclaw/tmp/sessions/*.session` con TTL de 48h y escribe un JSON de diagnóstico:

```python
import json
import time
from pathlib import Path

def purge_sessions(workspace: Path) -> Path:
    sessions_dir = workspace / ".openclaw" / "tmp" / "sessions"
    reports_dir = workspace / ".openclaw" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    now = time.time()
    ttl = 172800
    purged_files = []
    total_bytes = 0
    if sessions_dir.exists():
        for session_file in sessions_dir.glob("*.session"):
            stat = session_file.stat()
            if (now - stat.st_mtime) > ttl:
                size = stat.st_size
                session_file.unlink()
                purged_files.append(session_file.name)
                total_bytes += size
    report_payload = {
        "timestamp": int(now),
        "purged_count": len(purged_files),
        "bytes_reclaimed": total_bytes,
        "files": purged_files
    }
    report_path = reports_dir / "cleanup_last_run.json"
    report_path.write_text(json.dumps(report_payload, indent=2))
    return report_path
```

Persistir `cleanup_last_run.json` enlaza la rutina con los flujos de resúmenes matutinos (próxima lección).

---

## Resumen

Rutina nocturna defensiva: categoriza el ciclo de vida de los artefactos, valida concurrencia activa (descriptores + PID), y evita que la eliminación física corrompa flujos en vuelo.

**UP NEXT · Lección 9 de 30:** *Recopilación Automática de Reportes Matutinos Diarios*. Faltan **2 lecciones** para cerrar el Módulo 2.

---

## Preguntas abiertas del propio curso ("Can you answer these?")

1. ¿Por qué no basta un cron con `find` y `rm` para depurar temporales de OpenClaw?
2. ¿Qué impacto tiene montar discos con `noatime` en las políticas basadas en último acceso?
3. ¿Cómo evita OpenClaw borrar un archivo a mitad de subida/procesamiento de un subagente?
4. ¿Qué pasa si un `.lock` registra un PID reasignado a otro proceso no relacionado?

(Anotadas para profundizar. La #4 es un agujero real del enfoque PID-verifica: el PID puede reciclarse.)

---

## Notas de verificación (Kanam)

**El núcleo de ingeniería es lo más sólido del curso hasta ahora.** Las tres reglas defensivas son correctas y aplicables a cualquier limpieza con estado:

- ✅ **No borrar por tiempo solo** → verificar descriptores abiertos (`fuser`/`lsof`) y vigencia de PID. Correcto.
- ✅ **PITFALL de `st_ctime`** → en POSIX es cambio de inodo, no creación. **Correcto y valioso.** Usar `max(atime, mtime)` es el criterio correcto.
- ✅ **`os.kill(pid, 0)`** para verificar existencia de proceso sin señal. Técnica UNIX correcta.
- ✅ **REMEMBER de los locks** (verificar PID, no borrar por tiempo). Correcto.
- ✅ **Registro de métricas** de espacio liberado para diagnósticos. Buena práctica real.
- ⚠️ **La pregunta #4 del curso apunta a un agujero real** que su propio código no resuelve: el PID puede **reciclarse**; `os.kill(pid,0)` daría falso "vivo" (o falso "muerto"). Un lock robusto necesita PID + timestamp de creación + identidad del proceso, no solo PID.

**Lo que NO coincide con la instalación real:**
- ⚠️ **`~/.openclaw/tmp/` existe, pero su estructura real es PLANA**, no las cuatro categorías con ciclos de vida. Contenido real: `.tmpXXXX`, `bats-run-*`, `openclaw-web-fetch-*.log`, `heartbeat-snapshot.*`, dylibs, `node-compile-cache`, etc. (~77 entradas). Los subdirectorios `media/`, `tool_runs/`, `sessions/`, `locks/` **no existen**. La categorización por ciclo de vida es **buena idea de diseño**, pero no es la estructura del producto.
- ❌ **La ubicación está equivocada en el curso.** Dice que `.openclaw/tmp/` vive "en el workspace". Real: el tmp del runtime vive en el **STATE dir** (`~/.openclaw/tmp/`). El workspace tiene su propio `~/.openclaw/workspace/.openclaw/` (con `portals.json`, `trajectory-exports/`).
- ❌ **`OPENCLAW_WORKSPACE` no es la variable real.** La que usa el producto es **`OPENCLAW_WORKSPACE_DIR`** (según docs de instalación Docker/Railway).
- ❌ **`tasks.json` no existe.** El scheduler real es **automations/cron** (jobs en SQLite), no un `tasks.json` en la raíz del workspace. El JSON del curso con `on_success`/`on_failure.retry`/`env` no mapea a ningún esquema real.
- ⚠️ **`fuser -s`** existe en este macOS (`/usr/bin/fuser`), así que ese fragmento correría - pero la semántica de `fuser` varía entre Linux y macOS, y el curso asume Linux. En la práctica se usa `lsof` en macOS.
- ❌ **`.openclaw/reports/`** como directorio de diagnósticos no existe.

**Patrón (octavo caso, mismo):** **excelente contenido de ingeniería** (las reglas defensivas de limpieza son las de un sysadmin serio) montado sobre la fachada inventada de siempre (rutas del workspace, `tasks.json`, `OPENCLAW_WORKSPACE`, los subdirectorios). La parte defendible es la **lógica**; la **ubicación y el registro** hay que reescribirlos contra el sistema real.

**Nota de contexto (Módulo 2):** tras esta L08 el propio curso indica *"2 lessons left in Tareas Programadas y Rutinas Autónomas"* → Módulo 2 = 5 lecciones (L06-L10). Lección 9: *Recopilación Automática de Reportes Matutinos Diarios*.
