# Módulo 6 · Lección 28 de 30: Consulta Coordinada de Memorias Compartidas

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 6 - Especialización y Coordinación Multiagente
**Lección:** 28 de 30
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

Varios agentes en paralelo con copias aisladas del contexto → desincronización inmediata (uno actualiza el estado de una orden, otro consulta un archivo local que ya no refleja la realidad → respuestas contradictorias). La consulta coordinada establece **un único plano de estado persistente** con lecturas no bloqueantes y escrituras atómicas.

La memoria compartida **no** es un volcado monolítico en la ventana de contexto: es una estructura organizada (MEMORY.md + `.context/`, key-value, bases vectoriales locales) que expone **interfaces concurrentes** para que agentes con distintos roles extraigan y enriquezcan info sin corromper el estado global.

---

## Topología de acceso concurrente

Patrón fundamental: **segregar lecturas masivas de escrituras controladas**. Muchos lectores concurrentes; toda modificación pasa por **bloqueos cooperativos** o colas de mutación. Cuando un agente resuelve una solicitud, hace una **lectura orientada a claves o fragmentos semánticos**, no carga el historial completo (preserva tokens, evita ruido).

Según el curso, OpenClaw usa un **bus de eventos + gestor de archivos con advisory locking** para que las lecturas concurrentes vean una instantánea consistente mientras hay una actualización en curso.

### Semántica vs. clave-valor

| Dimensión | Clave exacta (KV / state store) | Recuperación semántica (embeddings) |
|---|---|---|
| Caso de uso | Estado de pedidos, IDs de cliente, flags | Preferencias históricas, notas de reunión, incidentes |
| Latencia | Sub-ms (<5 ms) | Decenas de ms (20-80 ms) |
| Garantía | Determinista, exacta | Probabilística (vecinos por distancia coseno) |
| Ambigüedad | Cero (requiere clave exacta) | Alta (tolera variaciones de fraseo) |

Caso típico: "No puedo pagar mi factura de ayer" → **primero** lectura estructurada para obtener el `account_id`; **con ese ID verificado**, consultar el vector store **filtrando por ese identificador** (evita contaminar con datos de otros clientes).

---

## Particionado por namespace

```text
workspace/
├── MEMORY.md                 # Hechos globales de sólo lectura
└── .context/
    ├── shared_state.json     # Clave-valor compartido (bloqueo transaccional)
    └── namespaces/
        ├── billing/          # Escritura exclusiva: billing-agent; Lectura: todos
        │   └── ledger.json
        ├── support/
        │   └── tickets.json
        └── triage/
            └── routes.json
```

Cada agente tiene escritura acotada a **su** subdirectorio; el orquestador otorga **lectura global** sobre `namespaces/` y `MEMORY.md`.

---

## Lectura/escritura con bloqueo no destructivo (Reader-Writer Lock)

Múltiples lectores obtienen **shared locks** simultáneos; un escritor pide **exclusive lock**, encola lecturas entrantes, espera a las activas, escribe **atómicamente** y libera. El código del curso usa `fcntl.flock`:

```python
import json, os, fcntl
from contextlib import contextmanager
STATE_FILE = "workspace/.context/shared_state.json"

@contextmanager
def shared_memory_read(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"El almacén de memoria {filepath} no existe.")
    with open(filepath, "r", encoding="utf-8") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_SH)   # shared: lectores concurrentes; escritores esperan
        try:
            yield json.load(f)
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

@contextmanager
def shared_memory_write(filepath):
    file_mode = "r+" if os.path.exists(filepath) else "w+"
    with open(filepath, file_mode, encoding="utf-8") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)   # exclusive: nadie más lee/escribe
        try:
            f.seek(0)
            try: data = json.load(f)
            except json.JSONDecodeError: data = {}
            yield data
            f.seek(0); f.truncate(); json.dump(data, f, indent=2); f.flush()
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
```

Tres lectores consultan instantáneo; un escritor hace que el kernel **suspenda** nuevos shared locks hasta que la mutación termina y el archivo se sincroniza.

> **PITFALL del curso (correcto y crítico):** no usar archivos de texto planos como buffers de escritura directa **sin** advisory locking (`fcntl`) o transacciones SQLite. Dos agentes escribiendo `MEMORY.md` a la vez **truncan líneas incompletas**, rompen la estructura y desorientan a los modelos.

---

## Snapshot isolation e índice invertido

Contención de I/O + riesgo de inconsistencia temporal si una tarea compuesta lee en dos instantes. Solución: **snapshot isolation** - al iniciar un flujo multi-paso, el orquestador genera una **vista inmutable** con `revision_id` en vez de consultar el archivo dinámico en cada paso.

```json
{
  "revision": "rev_20250514_094012",
  "entities": {
    "usr_8821": { "active_plan": "enterprise", "open_tickets": [402, 409],
      "last_billing_status": "settled", "context_ref": "namespaces/billing/ledger.json#usr_8821" }
  },
  "index_terms": { "factura": ["usr_8821"], "cancelacion": ["usr_8821"] }
}
```

El agente de triaje consulta `entities["usr_8821"]`; si deriva a soporte, transfiere la **referencia exacta del snapshot** para que **ambos observen la misma realidad factual**.

### Check your understanding
**El Agente A lee un saldo; antes de concluir, el Agente B lo modifica en disco. ¿Qué patrón evita la inconsistencia?**
- [x] **Fijar un `revision_id` inmutable mediante snapshot isolation al iniciar la tarea.** ✅ (acierta)

---

## Consulta federada con agregador

Evita acoplamiento fuerte cuando el estado está repartido entre namespaces: un **agente de agregación** consulta en paralelo a los agentes especializados (o lee sus esquemas solo-lectura):

```python
import concurrent.futures
from typing import Dict, Any

def fetch_billing_info(user_id: str) -> Dict[str, Any]:
    with shared_memory_read("workspace/.context/namespaces/billing/ledger.json") as data:
        return data.get(user_id, {"status": "sin_facturas"})

def fetch_support_info(user_id: str) -> Dict[str, Any]:
    with shared_memory_read("workspace/.context/namespaces/support/tickets.json") as data:
        return data.get(user_id, {"tickets": []})

def aggregate_user_context(user_id: str) -> Dict[str, Any]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        fb = executor.submit(fetch_billing_info, user_id)
        fs = executor.submit(fetch_support_info, user_id)
        billing_data = fb.result(timeout=1.0)
        support_data = fs.result(timeout=1.0)
    return {"user_id": user_id, "billing": billing_data, "support": support_data}
```

Tres propiedades: **aislamiento de fallos** (un namespace bloqueado no detiene a los otros; timeout por componente), **contexto mínimo** (respuesta compacta, no volcados), **respeto a fronteras de dominio** (cada agente valida la semántica de su propio archivo).

> **TIP:** en flujos de estado encadenado, usar **`correlation_id`** en cada lectura/escritura para rastrear procedencia en auditoría **sin** bloquear el workspace global.

---

## Ejercicio: lector coordinado con timeout y fallback cache

`resilient_memory_read`: `LOCK_SH | LOCK_NB` en bucle con **backoff exponencial**; si el recurso no se libera en 1 s, **abortar y usar `fallback_cache.json`**; registrar la métrica. Salida real de mi corrida (sobre un `shared_state.json` escrito por `shared_memory_write`):
```text
[OK] leído en 0.000s
```
El código del curso corre tal cual.

---

## Resumen

Bus de estado único + bloqueos consultivos + particionado por namespace + snapshot isolation + consulta federada → colaboración multiagente sin inconsistencias. Deja listo el terreno para **transferir control y resultados intermedios** entre especialistas.

**UP NEXT · Lección 29 de 30:** *Transferencia Limpia de Tareas entre Especialistas*. Faltan **2 lecciones** para cerrar el Módulo 6.

---

## Preguntas abiertas del propio curso

1. ¿Cómo evita `fcntl.LOCK_SH` que dos agentes lean datos corruptos mientras un tercero escribe?
2. ¿Por qué no cargar todo `MEMORY.md` en cada consulta?
3. ¿Cuándo conviene semántica vs. clave-valor?
4. ¿Qué ventaja da un índice invertido por revisiones en flujos multi-paso?

---

## Notas de verificación (Kanam)

**Núcleo de ingeniería: sólido y correcto - y el tema (memoria coordinada entre agentes) existe PARCIALMENTE en OpenClaw, de otra forma:**

| El curso dice | OpenClaw real |
|---|---|
| Memoria compartida entre agentes | ⚠️ **Parcial.** Existe *"Cross-agent memory search"* en docs, **pero**: el path QMD cross-agent **se eliminó en v2026.8.1**; *"Builtin memory does not search another agent's transcript corpus; each agent searches only its own"*. Para material compartido se usa **`memory.search.extraPaths`** (un directorio explícito). |
| Coordinación entre agentes | ✅ Real vía **`tools.agentToAgent`** (acceso cross-agent a sesiones, on por defecto), con `allow`/`enabled` y `tools.sessions.visibility`. |
| Vaults por agente | ✅ Real: **Memory Wiki per-agent vaults** (`~/.openclaw/wiki/<agent>`). |
| **Escrituras atómicas + advisory locking** | ✅ **Correcto y central.** `fcntl.flock` (LOCK_SH/LOCK_EX) es la primitiva real, y el PITFALL (no escribir texto plano sin lock) es válido. |
| Snapshot isolation con `revision_id` | ✅ Buena **práctica de ingeniería** (consistencia temporal), pero **no** es un mecanismo nativo de OpenClaw. |
| Consulta federada con agregador | ✅ Buen patrón (aislamiento de fallos, contexto mínimo), construible. |
| **Acierta el quiz** (snapshot isolation). | ✅ |
| **El código `fcntl` corre tal cual**: verifiqué escritura atómica + lectura LOCK_SH + `resilient_memory_read`. | ✅ |

**Lo que NO coincide con la instalación real:**
- ⚠️ **La "memoria compartida" como plano único nativo con bus de eventos + advisory locking del orquestador** es **inventada**. OpenClaw **NO** ofrece hoy un store cross-agent coordinado (el QMD cross-agent **se removió**); ofrece `extraPaths` para compartir *referencia* de solo-lectura y `agentToAgent` para acceso a sesiones.
- ❌ **`.context/shared_state.json` / `.context/namespaces/<dominio>/`** como estructura del producto: **inventada**. `MEMORY.md` es real, pero el árbol `.context/` con namespaces y ACLs por agente no lo es.
- ❌ **`revision_id` / snapshot isolation / índice invertido** nativos: no existen como feature; son patrones a construir (y `fcntl` es UNIX-only, ver abajo).
- ⚠️ **`fcntl` es UNIX-only** (no funciona en Windows). Verifiqué que está disponible aquí; pero un diseño portable preferiría `filelock` o transacciones SQLite. El curso no lo advierte.
- ⚠️ **SQLite**: el curso lo menciona como alternativa; es justo lo que OpenClaw **usa de verdad** para sesiones (`openclaw-agent.sqlite`) - más cerca de la realidad que el `shared_state.json`.

**Verificación ejecutable:**
- ✅ **El código del curso (`shared_memory_read`/`shared_memory_write`/`resilient_memory_read`) corre tal cual** en este entorno (Python + `fcntl`). Reproduje la escritura atómica y la lectura con lock compartido. Es de las pocas lecciones donde el material es correcto *y* ejecutable.

**Patrón (vigésimo octavo caso, con matiz fuerte):** el tema **existe parcialmente** (memoria cross-agent vía `extraPaths`/`agentToAgent`, vaults por agente), la **filosofía acierta** (lecturas concurrentes, escrituras atómicas, snapshot, federación), y **el código corre**. La fachada inventada: **`.context/namespaces/`, `shared_state.json`, snapshot isolation nativo y el "bus de eventos"**. Y un dato jugoso: **el cross-agent search real se ELIMINÓ en v2026.8.1** - o sea, el curso describe como feature algo que el producto, de hecho, **retiró**. Traducible: `extraPaths` (compartir referencia) + `agentToAgent` + SQLite, no el `shared_state.json` del curso.

**Nota de contexto (Módulo 6):** tras esta L28 el propio curso indica *"2 lessons left in Especialización y Coordinación Multiagente"* → Módulo 6 = 5 lecciones (L26-L30). Lección 29: *Transferencia Limpia de Tareas entre Especialistas*.
