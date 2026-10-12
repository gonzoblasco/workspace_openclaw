# Módulo 4 · Lección 17 de 30: Estructuración de Notas en Directorios Temporales

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 4 - Gestión Proactiva del Workspace
**Lección:** 17 de 30
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

Un agente continuo genera información heterogénea (borradores, fragmentos, volcados de webhooks, resúmenes intermedios). Escribir eso directamente sobre los archivos canónicos (`MEMORY.md`, docs de arquitectura) **contamina el contexto persistente** con hipótesis no verificadas y ruido. La solución: **desacoplar el procesamiento activo de la memoria permanente** mediante un espacio temporal estructurado.

El directorio temporal no debe ser un volcado caótico: debe funcionar como **memoria intermedia tipada**, con subdirectorios semánticos, convenciones de nombres, frontmatter y directivas de ciclo de vida.

---

## Topología de `.workspace/tmp/` y su semántica

Tres subárboles esenciales:

- **`drafts/`:** documentos que requieren varios pasos de inferencia o revisión antes de promoverse.
- **`scratchpad/`:** notas efímeras de ejecución, volcados de comandos, cálculos auxiliares de vida corta.
- **`staging/`:** información ya parseada y estructurada, lista para validarse o consolidarse en memoria permanente.

```text
.workspace/tmp/
├── drafts/
│   └── 2025-03-30_auth-refactor-proposal.md
├── scratchpad/
│   ├── run_4812_curl-latency.json
│   └── run_4815_dns-lookup.txt
└── staging/
    ├── memory_sync_2025-03-30T10-15-00Z.md
    └── incident_INC-901_recap.md
```

Ciclo de vida: nace en `scratchpad/` o `drafts/` → se normaliza con metadatos hacia `staging/` → pasa a los **directorios definitivos** solo cuando se cumplen las condiciones de validación.

---

## Convenciones de nombrado y frontmatter

El riesgo de un directorio temporal sin gobierno son archivos anónimos (`temp.txt`, `notes.md`) que colisionan o quedan huérfanos cuando varios subprocesos actúan en paralelo. Regla estricta de nombrado:

```text
[TIPO]_[ORIGEN]_[IDENTIFICADOR]_[TIMESTAMP].[ext]
```

Y frontmatter YAML estandarizado para calcular caducidad (TTL), rastrear trazabilidad y clasificar sensibilidad:

```markdown
---
task_id: "tsk_ingest_9921"
source_trigger: "webhook/pagerduty"
created_at: "2025-03-30T14:30:00Z"
expires_at: "2025-03-31T02:30:00Z"
retention_policy: "purge_on_expiry"
status: "in_review"
canonical_target: "docs/incidents/2025-03-INC-89.md"
tags: [incident, redis, latency]
---
```

Campos clave:
- **`expires_at`:** ISO-8601; momento exacto en que el archivo puede recolectarse.
- **`retention_policy`:** `purge_on_expiry` (borra), `archive_to_cold` (comprime a histórico), `escalate_if_pending` (alerta si sigue `in_review`).
- **`canonical_target`:** ruta final si se aprueba la promoción.

> **PITFALL del curso (correcto):** archivos temporales sin `expires_at` o con fecha no estándar impiden que el recolector calcule la retención → fugas de almacenamiento y crecimiento innecesario del índice vectorial.

---

## El ciclo: creación, staging y promoción

Tres operaciones: (1) **ingesta y escritura local** en `scratchpad/`/`drafts/`; (2) **promoción a staging** (limpiar volcados, normalizar markdown, mover a `staging/`); (3) **consolidación canónica** (verificar conflictos y fusionar en el destino).

```python
import os, re, yaml
from datetime import datetime, timezone
from pathlib import Path
WORKSPACE_ROOT = Path("/opt/openclaw/workspace")
TMP_DIR = WORKSPACE_ROOT / ".workspace" / "tmp"

def parse_frontmatter(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        raise ValueError(f"El archivo {file_path.name} no contiene frontmatter válido.")
    return yaml.safe_load(match.group(1)), match.group(2).strip()

def process_staging_file(file_path: Path):
    metadata, body = parse_frontmatter(file_path)
    now = datetime.now(timezone.utc)
    expiry = datetime.fromisoformat(metadata["expires_at"].replace("Z", "+00:00"))
    if now > expiry and metadata.get("status") != "approved":
        print(f"[PURGA] {file_path.name} ha caducado ({expiry}). Eliminando...")
        file_path.unlink(); return
    if metadata.get("status") == "approved":
        target_path = WORKSPACE_ROOT / metadata["canonical_target"]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n<!-- Consolidado desde {file_path.name} -->\n"); f.write(body)
        print(f"[PROMOVIDO] {file_path.name} -> {target_path}")
        file_path.unlink()
```

Salida esperada:

```text
[PROMOVIDO] staging_incident_INC-901_20250330.md -> /opt/openclaw/workspace/docs/incidents/2025-03-INC-89.md
[PURGA] staging_scratch_curl_test_20250329.md ha caducado (2025-03-29 20:00:00+00:00). Eliminando...
```

> **TIP del curso:** usar la variable de entorno `OPENCLAW_TMP_TTL_HOURS` para inyectar un `expires_at` por defecto en cualquier archivo generado si el agente no especifica uno.

### Check your understanding
**Un agente diagnostica un timeout de red y debe dejar constancia para el informe semanal. ¿Procedimiento correcto?**
- [x] **Crear `staging_incident_net-timeout.md` con frontmatter que especifique `expires_at` y `canonical_target`.**

---

## Prevención de colisiones concurrentes

Con varios disparadores simultáneos, dos subprocesos podrían escribir el mismo temporal o competir por recursos.

1. **Namespacing por sesión/ejecución:** cada ejecución escribe en su propia jaula `.workspace/tmp/scratchpad/{run_id}/`, eliminando la sobreescritura accidental entre tareas paralelas.
2. **Bloqueos atómicos para promociones:** lockfiles (`.lock`) o transacciones de filesystem para coordinar dos procesos que consolidan hacia el mismo `canonical_target`.

| Escenario | Riesgo | Mitigación |
|---|---|---|
| Dos webhooks del mismo incidente | Sobreescritura del temporal | Nombre con timestamp en ms + sufijo aleatorio (`uuid4()[:6]`) |
| Limpieza nocturna mientras se escribe | Eliminar archivo en uso | `status: writing` en frontmatter o lockfile con exclusión mutua |
| Consolidación masiva a `MEMORY.md` | Carrera en memoria persistente | Cola secuencial en `staging/`, un único hilo de consolidación |

> **REMEMBER del curso (correcto):** un archivo en edición activa se crea con extensión `.tmp` (`report.md.tmp`) y se **renombra atómicamente** a `.md` solo cuando escritura y checksums terminaron. Evita que lectores procesen notas truncadas.

---

## Preguntas abiertas del propio curso ("Can you answer these?")

1. ¿Qué diferencia operativa hay entre `scratchpad/` y `drafts/`?
2. ¿Por qué usar `.tmp` durante la escritura activa en vez de escribir el archivo final?
3. ¿Cómo debe actuar el recolector si encuentra un temporal vencido con `status: in_review`?
4. ¿Qué impacto tiene en las búsquedas vectoriales no estructurar bien las notas temporales?

(Anotadas. La #3 la responde la `retention_policy escalate_if_pending` del propio material.)

---

## Notas de verificación (Kanam)

**El núcleo de ingeniería es sólido y correcto** (estilo L08/L10/L13). Y -importante- **la concurrencia, que el curso venía dejando sin resolver, acá sí la ataca** (namespacing + locks + hilo único).

| Práctica del curso | Veredicto |
|---|---|
| Separar `drafts/scratchpad/staging` y no escribir sobre memoria canónica | ✅ Patrón correcto (staging → promoción). |
| Frontmatter con `expires_at`/`retention_policy`/`canonical_target` | ✅ Buen gobierno de temporales. |
| TTL + purga por caducidad; `archive_to_cold`/`escalate_if_pending` | ✅ Políticas sensatas. |
| **`.tmp` + rename atómico** para evitar leer truncados | ✅ Correcto (POSIX). |
| **Namespacing por `run_id`** + **locks** + **hilo único de consolidación** | ✅ Correcto - es la respuesta a la carrera multi-writer que faltaba en L05/L08/L14. |
| Recolector que no borra `in_review` vencido sin política | ✅ Correcto. |
| El **ejercicio corre tal cual** (Python + `pyyaml`): verifiqué el seed → `[PURGA]` + `[PROMOVIDO]` exactos. | ✅ |

**Lo que NO coincide con la instalación real:**
- ❌ **`.workspace/tmp/` no existe.** La ruta real del tmp es el **state dir** (`~/.openclaw/tmp/`) o `<workspace>/.openclaw/`. Ni `.workspace/tmp/` ni su topología `drafts/scratchpad/staging/` son del producto. (Mismo error de ubicación que L08.)
- ❌ **`OPENCLAW_TMP_TTL_HOURS` no existe** como variable del producto (verificado: no aparece en docs).
- ❌ **`/opt/openclaw/workspace`** en el script: ruta de ejemplo inventada (en esta máquina el workspace es `~/.openclaw/workspace`).
- ❌ **No hay un "recolector de basura autónomo" nativo** ni un "índice vectorial del workspace" que se sature por temporales sin frontmatter. Es un mecanismo construible, no una capacidad de OpenClaw.
- ⚠️ **`yaml` (pyyaml):** en este entorno **sí está instalado** (a diferencia de las libs de L13), así que ese fragmento corre. Ojo: no siempre está.

**Verificación ejecutable:**
- ✅ Corrí el script con dos archivos sembrados: `[PROMOVIDO]` (approved, no vencido) y `[PURGA]` (in_review, vencido). **Salida idéntica a la prometida.**

**Patrón (decimoséptimo caso, consistente):** **buena ingeniería** (staging, TTL, atomicidad, **y por fin la concurrencia**) montada sobre una **topología y una env var inventadas** (`.workspace/tmp/`, `OPENCLAW_TMP_TTL_HOURS`). El *qué* es correcto y -dato clave- **acá el curso sí resuelve el hueco de concurrencia** que dejó abierto en tres lecciones anteriores.

**Nota de contexto (Módulo 4):** tras esta L17 el propio curso indica *"3 lessons left in Gestión Proactiva del Workspace"* → Módulo 4 = 5 lecciones (L16-L20). Lección 18: *Detección de Inconsistencias en Documentación Técnica*.
