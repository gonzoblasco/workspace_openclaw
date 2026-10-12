# Módulo 4 · Lección 20 de 30: Limpieza Selectiva de Registros de Contexto

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 4 - Gestión Proactiva del Workspace
**Lección:** 20 de 30 · **cierra el Módulo 4**
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

Un agente continua genera dos clases de artefactos: **información consolidable con valor duradero** y **ruido instrumental efímero**. Preservar todo degrada la ventana de contexto (más costo por inferencia, interferencia atencional, pérdida de foco en `SOUL.md`). Borrar todo destruye trazabilidad y aprendizajes.

La limpieza selectiva puntúa cada registro en **cuatro dimensiones** (antigüedad/distancia de turno, ratio semántico vs instrumental, menciones de entidades de configuración, marcadores de resolución) y **poda el ruido mientras retiene conclusiones**.

---

## Anatomía de los registros de contexto

Según el curso, las interacciones residen en **`.openclaw/context/logs/`** en **JSON Lines** (`.jsonl`), donde conviven mensajes, tool calls y volcados:

```jsonl
{"timestamp": "2025-02-14T08:12:00Z", "role": "assistant", "type": "tool_call", "name": "bash_exec", "args": {"cmd": "docker ps --format json"}, "session_id": "sess-8492"}
{"timestamp": "2025-02-14T08:12:02Z", "role": "tool", "type": "tool_output", "content": "[{...} , ... 48 contenedores más ...]", "session_id": "sess-8492"}
{"timestamp": "2025-02-14T08:12:05Z", "role": "assistant", "type": "message", "content": "El contenedor redis-cache está operativo sin anomalías de memoria.", "session_id": "sess-8492"}
```

- **Ruido podable:** el volcado de `docker ps` (1.400 tokens, 48 contenedores irrelevantes).
- **Conclusión retenible:** "redis-cache está operativo".

---

## Criterios de poda (cuatro dimensiones)

1. **Antigüedad / distancia de turno:** inmunidad temporal en los últimos 15-30 turnos.
2. **Ratio semántico vs instrumental:** salidas crudas >300 tokens se penalizan si el asistente ya extrajo la conclusión.
3. **Entidades de configuración:** hosts, contraseñas temporales, env vars, rutas críticas → retención alta hasta verificar persistencia en `MEMORY.md`.
4. **Marcadores de cierre:** si la sesión terminó en `task_completed`, los intentos fallidos intermedios son candidatos a compresión/purga.

**Destilación:** el bloque masivo se sustituye por una referencia condensada: `[TOOL_SUMMARY: docker ps listó 49 contenedores; 1 relevante (redis-cache, Up)]`.

---

## Implementación de la rutina

```python
import json
import re
from datetime import datetime, timezone
from pathlib import Path
LOG_DIR = Path(".openclaw/context/logs")
ARCHIVE_DIR = Path(".openclaw/context/archive")
TOKEN_THRESHOLD_RAW = 200  # Más de 200 caracteres de salida cruda es candidato a poda

def calculate_prune_priority(entry: dict, age_hours: float) -> str:
    entry_type = entry.get("type")
    content = str(entry.get("content", ""))
    if entry.get("role") in ["user", "system"]:
        return "KEEP"
    if entry_type == "tool_output":
        if age_hours > 24 and len(content) > TOKEN_THRESHOLD_RAW:
            if "CRITICAL" in content or "FATAL" in content:
                return "KEEP"
            return "PURGE"
        elif len(content) > TOKEN_THRESHOLD_RAW:
            return "COMPACT"
    if entry_type == "tool_call" and entry.get("name") in ["bash_exec", "file_cat"]:
        if age_hours > 72:
            return "COMPACT"
    return "KEEP"

def compact_tool_output(content: str) -> str:
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    if not lines:
        return "[Empty Output]"
    return f"[PRUNED_TOOL_OUTPUT: {len(lines)} lines, starts: '{lines[0][:80]}...']"

def process_session_log(log_path: Path):
    now = datetime.now(timezone.utc)
    retained_records = []; pruned_count = 0; compacted_count = 0
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            entry_time = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
            age_hours = (now - entry_time).total_seconds() / 3600.0
            action = calculate_prune_priority(entry, age_hours)
            if action == "KEEP":
                retained_records.append(entry)
            elif action == "COMPACT":
                entry["content"] = compact_tool_output(entry["content"])
                entry["_pruned"] = True
                retained_records.append(entry); compacted_count += 1
            elif action == "PURGE":
                pruned_count += 1
    with open(log_path, "w", encoding="utf-8") as f:
        for record in retained_records:
            f.write(json.dumps(record) + "\n")
    print(f"Log: {log_path.name} | Purgados: {pruned_count} | Compactados: {compacted_count} | Retenidos: {len(retained_records)}")
```

Salida que muestra el curso: `Log: sess-8492.jsonl | Purgados: 18 | Compactados: 7 | Retenidos: 12`.

> **PITFALL del curso (correcto):** no elimines registros con `export`, credenciales temporales o URLs de endpoints si la tarea aún no alcanzó confirmación final - un reintento posterior fallará por falta de credenciales.

> **REMEMBER del curso (correcto):** la poda debe reducir la longitud del prompt **sin alterar el grafo de dependencias** de las decisiones.

### Check your understanding
**¿Qué estrategia minimiza tokens sin amnesia operativa?**
- [x] **Destilar las salidas de herramientas a resúmenes breves tras verificar que los datos críticos ya residen en `MEMORY.md`.**

---

## Sincronización con archivos persistentes (dos fases)

1. **Barrido de extracción activa:** antes de podar un `tool_output`/`message` con configuraciones, verificar cruzado contra `MEMORY.md`/`notes/`; si el dato no está, forzar sincronización proactiva.
2. **Índices de trazabilidad fría:** los descartados no se borran con `unlink`; se mueven **comprimidos con gzip** a `.openclaw/context/archive/` (`YYYY-MM/session-id.jsonl.gz`).

---

## Automatización por triggers

**Umbral de tokens en sesión activa:** al superar el 60% de la ventana, se dispara `context:pre_overflow` y el gestor poda en background los turnos intermedios ya resueltos.

```yaml
# .openclaw/config.yaml
workspace:
  context_management:
    auto_prune: true
    trigger_threshold_percent: 60
    retention_strategy: "selective_semantic"
    protected_roles: ["system", "user"]
    compact_tool_outputs_after_turns: 5
    archive_directory: ".openclaw/context/archive"
```

**Integración con heartbeat:** las sesiones inactivas >6 h se delegan al ciclo de heartbeat, que poda y deja reporte en la bitácora diaria.

---

## Ejercicio: filtro de poda para salidas de red

Reemplaza volcados de herramientas de red (`curl`/`netstat`/`nmap`) por un resumen, dejando intactas las decisiones.

`test_context.jsonl` (del curso):
```jsonl
{"timestamp": "2025-02-14T10:00:00Z", "role": "user", "type": "message", "content": "Verifica si el servicio de base de datos está respondiendo en el puerto 5432."}
{"timestamp": "2025-02-14T10:00:02Z", "role": "assistant", "type": "tool_call", "name": "bash_exec", "args": {"cmd": "nc -zv 127.0.0.1 5432"}}
{"timestamp": "2025-02-14T10:00:03Z", "role": "tool", "type": "tool_output", "content": "Connection to 127.0.0.1 5432 port [tcp/postgresql] succeeded!\n" + "x" * 600}
{"timestamp": "2025-02-14T10:00:05Z", "role": "assistant", "type": "message", "content": "El puerto 5432 de PostgreSQL está accesible y aceptando conexiones locales."}
```

`prune_exercise.py`:
```python
import json
def prune_network_output(entry: dict) -> dict:
    if entry.get("type") == "tool_output":
        raw_text = entry.get("content", "")
        if "Connection to" in raw_text and "succeeded" in raw_text:
            first_line = raw_text.splitlines()[0]
            entry["content"] = f"[VERIFIED_PORT_STATUS: {first_line}]"
            entry["_compacted"] = True
    return entry
with open("test_context.jsonl", "r") as src, open("pruned_context.jsonl", "w") as dst:
    for line in src:
        if line.strip():
            entry = json.loads(line)
            dst.write(json.dumps(prune_network_output(entry)) + "\n")
```

**Salida real de mi corrida** (con el `.jsonl` corregido a JSON válido):
```
{'role': 'user', 'content': 'Verifica si el servicio de base de datos está respondiendo en el puerto 5432.'}
{'role': 'assistant', 'type': 'tool_call', 'args': {'cmd': 'nc -zv 127.0.0.1 5432'}}
{'role': 'tool', 'type': 'tool_output', 'content': '[VERIFIED_PORT_STATUS: Connection to 127.0.0.1 5432 port [tcp/postgresql] succeeded!]', '_compacted': True}
{'role': 'assistant', 'content': 'El puerto 5432 de PostgreSQL está accesible y aceptando conexiones locales.'}
```

---

## Resumen

Limpieza **selectiva**: evalúa por antigüedad, rol y valor instrumental, compacta/purga volcados transitorios y preserva decisiones. Deja preparado el terreno para el **bucle agéntico multi-etapa** (Módulo 5).

**UP NEXT · Lección 21 de 30:** *Desglose Estratégico de Tareas Complejas* - **inicia el Módulo 5: Encadenamiento en Bucle Agéntico.**

---

## Preguntas abiertas del propio curso

1. ¿Cómo evita la poda descartar variables temporales que el agente aún necesita para reintentar?
2. ¿En qué se diferencia la destilación sintética de un resumen conversacional estándar?
3. ¿Qué impacto tiene mantener trazas de error completas vs condensarlas en una línea?
4. ¿Cuándo conviene mover al archivo frío comprimido en lugar de purga definitiva?

---

## Notas de verificación (Kanam)

**Concepto: correcto y valioso.** La disciplina "podar ruido, retener conclusiones, no perder credenciales/config" es lo que el workspace ya practica (pruning + compactación nativa).

**Lo que SÍ existe en la instalación real (y el curso no lo nombra así):**
- ✅ **La poda/compactación de contexto es real**, pero con otra forma: **`agents.defaults.contextPruning`** (`mode: "cache-ttl"`) recorta resultados de tool; y el **hard-clear** reemplaza el contenido por el placeholder **`[Old tool result content cleared]`** (`contextPruning.hardClear.placeholder`). Hay además compactación (`compaction`) y `/compact`.
- ✅ El **espíritu** del "PITFALL/REMEMBER" es válido: la poda no debe romper dependencias.

**Lo que NO coincide con la instalación real:**
- ❌ **`.openclaw/context/logs/` no existe** (verificado). No hay un directorio de logs de contexto en JSON Lines como el descrito. El estado real de sesiones vive en el **transcript SQLite**; el tmp, en el state dir.
- ❌ **`.openclaw/config.yaml` con sección `workspace: context_management:`** es **inventado**. La config real es **`openclaw.json`** y no tiene esa sección.
- ❌ **`context:pre_overflow`** como señal interna, y el umbral "60% dispara poda en caliente": **inventados** como API. Lo real es el disparador automático de `contextPruning`/compaction (sin ese nombre de evento).
- ❌ **`.openclaw/context/archive/*.jsonl.gz`**: convención inventada.
- ⚠️ **El output `Purgados: 18 | Compactados: 7 | Retenidos: 12`** es de una sesión externa (`sess-8492`) que no viene con el material: **no es reproducible** (sin input no hay número).

**HALLAZGO - el ejercicio, tal como lo da el curso, NO corre:**
- ❌ **El `test_context.jsonl` del curso es JSON INVÁLIDO.** La línea del `tool_output` contiene literalmente:
  `"content": "Connection to ... succeeded!\n" + "x" * 600`
  Es decir, una **expresión de concatenación de Python escrita dentro de un string JSON**. Un `.jsonl` real no puede tener eso; `json.loads` falla con `JSONDecodeError: Expecting ',' delimiter` (verificado; el script revienta en la línea 3).
- ✅ **Corregido a JSON válido** (concatenando el relleno *de verdad* al generar el archivo), el ejercicio **corre y produce exactamente** el `[VERIFIED_PORT_STATUS: ...]` prometido, dejando intactas las decisiones. Es decir: la **idea** funciona; el **material** está roto.
- Nota: el curso presenta el `.jsonl` como "contenido de un archivo"; el `+ "x" * 600` es un artefacto de haber escrito el ejemplo como código Python pero rotulado como JSON.

**Patrón (vigésimo caso, consistente):** **buena ingeniería** (poda por dimensiones, destilación, dos fases con archivado comprimido, no perder credenciales) montada sobre **rutas/eventos/config inventados** (`.openclaw/context/logs/`, `context:pre_overflow`, `config.yaml`) **+ un ejercicio que no corre por un JSON inválido**. Y el mecanismo real (**`contextPruning` + hard-clear + compaction**) es más simple y ya está en el producto.

**Cierre del Módulo 4.** Con esta lección se completan las 5 lecciones de *Gestión Proactiva del Workspace* (L16-L20). La Lección 21 abre el **Módulo 5: Encadenamiento en Bucle Agéntico** (arranca con *Desglose Estratégico de Tareas Complejas*).
