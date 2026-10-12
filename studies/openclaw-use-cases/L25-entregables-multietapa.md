# Módulo 5 · Lección 25 de 30: Generación de Entregables Finales Multi-Etapa

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 5 - Encadenamiento en Bucle Agéntico
**Lección:** 25 de 30 · **cierra el Módulo 5**
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

Cuando un bucle agéntico concluye su cadena de herramientas, el resultado bruto rara vez sirve como producto final: un agente que recopila métricas, audita registros o sintetiza transacciones acumula fragmentos dispersos (JSON de shell, volcados de DB, notas en `tmp/`, respuestas parciales). La generación de entregables finales es la disciplina de transformar esa telemetría en **artefactos estructurados, auditables y listos para consumo**.

El error recurrente: pedirle al LLM el informe definitivo **en la misma llamada** donde procesa herramientas → **degrada por fatiga/truncamiento de contexto**. La solución: **desacoplar la ejecución del bucle de la síntesis de entrega** mediante un embudo de fases: consolidación de evidencia → verificación de coherencia → formateo → archivo persistente.

---

## Anatomía del embudo de síntesis

El bucle escribe hallazgos en un entorno aislado y, **solo cuando se cumplen las precondiciones de parada**, invoca el pipeline. Tres fases:

1. **Agregación y limpieza de contexto:** leer los fragmentos temporales, extraer hechos concluyentes, descartar reintentos y logs sin valor semántico.
2. **Transformación tipada:** alimentar una plantilla estricta o un contrato de datos (parser JSON, o estilo documentado del workspace).
3. **Persistencia e indexación:** trasladar el entregable de `tmp/` a su destino definitivo (p. ej. `deliverables/reports/2025-05-14-auditoria.md`) y emitir un **resumen ligero** al canal.

> **Regla:** el agente **no** satura el canal con el entregable completo si excede los límites de longitud (Telegram/Discord/Slack). El artefacto completo vive en el filesystem; el canal recibe solo la **notificación con el resumen ejecutivo y la ruta**.

---

## El contrato de datos intermediario: `evidence.json`

Para que la generación sea repetible y determinista, el bucle escribe periódicamente un **manifiesto de evidencia** estructurado (`tmp/run-8491/evidence.json`):

```json
{
  "task_id": "audit-sec-20250514",
  "status": "collected",
  "started_at": "2025-05-14T08:12:00Z",
  "finished_at": "2025-05-14T08:14:22Z",
  "metrics": { "scanned_targets": 12, "issues_detected": 3, "critical_severity": 1 },
  "findings": [
    { "id": "SEC-001", "component": "auth-service", "severity": "critical",
      "summary": "Token JWT sin expiración explícita configurada en auth.py",
      "source_file": "services/auth/config.py:42",
      "remediation": "Establecer DEFAULT_EXPIRY_HOURS = 24 en las variables de entorno." },
    { "id": "SEC-002", "component": "payment-api", "severity": "medium",
      "summary": "Dependencia vulnerable pycrypto encontrada en requirements.txt",
      "source_file": "services/payment/requirements.txt:14",
      "remediation": "Migrar a cryptography 42.0+." }
  ],
  "verification_passed": true
}
```

Tres garantías: (1) si el contexto se reinicia/compacta, el estado **no se pierde** (está en disco); (2) la síntesis recibe solo este objeto compacto, **sin reprocesar** cientos de líneas de stdout; (3) permite una **compuerta estricta**: si `verification_passed` es falso o faltan claves, el pipeline **no avanza**.

> **PITFALL del curso (correcto):** renderizar el documento final **desde el stdout crudo** suele generar alucinaciones de cifras, fechas omitidas o enlaces rotos. **Separar siempre** la fase de extracción a JSON de la fase de renderizado.

---

## Implementación: generador multi-etapa en Python

```python
import json
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE_ROOT = Path("/home/openclaw/workspace")
EVIDENCE_FILE = WORKSPACE_ROOT / "tmp/run-8491/evidence.json"
DELIVERABLE_DIR = WORKSPACE_ROOT / "deliverables/reports"

def load_and_validate_evidence(filepath: Path) -> dict:
    if not filepath.exists():
        raise FileNotFoundError(f"Evidencia no encontrada en {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    for key in ["task_id", "metrics", "findings", "verification_passed"]:
        if key not in data:
            raise ValueError(f"Contrato inválido: falta la clave obligatoria '{key}'")
    if not data["verification_passed"]:
        raise ValueError("La evidencia no superó las pruebas de consistencia interna.")
    return data

def build_markdown_report(data: dict) -> str:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")
    m = data["metrics"]
    lines = ["---", f"id: {data['task_id']}", f"generated_at: \"{now}\"",
        f"targets_scanned: {m['scanned_targets']}", f"critical_issues: {m['critical_severity']}",
        "status: final", "---", "", f"# Informe de Auditoría de Seguridad: {data['task_id']}",
        "", "## Resumen Ejecutivo",
        f"- **Componentes escaneados:** {m['scanned_targets']}",
        f"- **Hallazgos detectados:** {m['issues_detected']} (Críticos: {m['critical_severity']})",
        "", "## Detalle de Hallazgos", ""]
    for item in data["findings"]:
        lines.extend([f"### [{item['severity'].upper()}] {item['id']}: {item['summary']}",
            f"- **Componente:** `{item['component']}`",
            f"- **Ubicación:** `{item['source_file']}`",
            f"- **Mitigación recomendada:** {item['remediation']}", ""])
    lines.extend(["## Acciones Posteriores",
        "1. Crear tickets de remediación inmediata para hallazgos con severidad crítica.",
        "2. Programar re-escaneo automático en el próximo ciclo de cron.", ""])
    return "\n".join(lines)

def export_and_notify(data: dict, content: str) -> dict:
    DELIVERABLE_DIR.mkdir(parents=True, exist_ok=True)
    target_path = DELIVERABLE_DIR / f"{data['task_id']}.md"
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(content)
    chat_summary = (f"✅ **Entregable generado con éxito**\n• Tarea: `{data['task_id']}`\n"
        f"• Componentes: {data['metrics']['scanned_targets']} analizados\n"
        f"• Alertas críticas: {data['metrics']['critical_severity']}\n"
        f"• Archivo: `{target_path.relative_to(WORKSPACE_ROOT)}`")
    return {"status": "success", "file_path": str(target_path), "chat_payload": chat_summary}

if __name__ == "__main__":
    try:
        evidence = load_and_validate_evidence(EVIDENCE_FILE)
        doc = build_markdown_report(evidence)
        print(json.dumps(export_and_notify(evidence, doc), indent=2))
    except Exception as err:
        print(json.dumps({"status": "error", "message": str(err)}), file=sys.stderr)
        sys.exit(1)
```

**Salida real de mi corrida** (idéntica a la del curso, salvo la ruta base):
```json
{
  "status": "success",
  "file_path": "deliverables/reports/audit-sec-20250514.md",
  "chat_payload": "✅ **Entregable generado con éxito**\n• Tarea: `audit-sec-20250514`\n• Componentes: 12 analizados\n• Alertas críticas: 1\n• Archivo: `deliverables/reports/audit-sec-20250514.md`"
}
```
La separación es absoluta: el archivo (45 líneas de detalle) queda indexado en el workspace; el canal recibe 4 líneas.

### Check your understanding
**¿Estrategia para evitar alucinaciones/métricas incoherentes tras un bucle extenso?**
- [x] **Validar programáticamente el contrato de evidencia intermedia antes de invocar la fase de formateo y archivo.** ✅ (acierta)

---

## Patrón de recuperación: lectura reflexiva post-escritura

Incluso con el esquema intermedio validado, el renderizado puede tropezar (plantillas corruptas, caracteres inválidos, límites de escritura). Patrón estándar = **lectura reflexiva**: tras escribir, el siguiente paso **no** es cerrar la tarea, sino invocar verificación que confirme tres propiedades:

1. **Existencia física y tamaño no nulo** (evitar 0 bytes por interrupción de I/O).
2. **Encabezado íntegro** (frontmatter/claves raíz presentes).
3. **Check de formato** (JSON/YAML parseable) **antes** de marcar `completed`.

```python
from pathlib import Path
def verify_generated_artifact(path_str: str, min_bytes: int = 100) -> bool:
    target = Path(path_str)
    if not target.is_file():
        return False
    if target.stat().st_size < min_bytes:
        return False
    with open(target, "r", encoding="utf-8") as f:
        first_line = f.readline().strip()
        return first_line == "---"
```

Si falla: el agente intercepta el error, **borra el archivo parcial** y **reitera el formateo** antes de tocar el canal.

> **REMEMBER del curso (correcto y central):** un entregable **no** se da por concluido cuando el modelo termina de redactarlo; **solo cuando el filesystem valida su tamaño, cabeceras y legibilidad**.

---

## Ejercicio: compuerta de entrega (resumen de dependencias)

Entrada `workspace/tmp/deps_raw.json`:
```json
{ "repo": "core-engine", "scanned_at": "2025-05-14",
  "outdated": [
    { "pkg": "fastapi", "current": "0.95.0", "latest": "0.111.0", "cve": null },
    { "pkg": "urllib3", "current": "1.26.5", "latest": "2.2.1", "cve": "CVE-2023-45803" } ] }
```
Script `build_deliverable.py`: verificar que `outdated` sea lista y que cada objeto tenga `pkg`/`current`/`latest`; compilar `deliverables/deps_report.md` con una tabla que **resalte en negrita** los paquetes con CVE no nulo; si la validación pasa, **eliminar** el temporal.

---

## Resumen

La generación multi-etapa saca del prompt conversacional la responsabilidad de producir documentos extensos: **acumulación en disco → validación estricta de `evidence.json` → renderizado programático → lectura reflexiva post-escritura** elimina discrepancias numéricas y desbordes de ventana. Prepara el terreno para **especialistas independientes** (Módulo 6).

**UP NEXT · Lección 26 de 30:** *Segmentación de Dominios entre Agentes Dedicados* - **inicia el Módulo 6: Especialización y Coordinación Multiagente.**

---

## Preguntas abiertas del propio curso ("Can you answer these?")

1. ¿Por qué almacenar la evidencia intermedia en disco y no solo en la memoria de contexto?
2. ¿Cómo se gestiona el envío cuando el archivo supera el límite de caracteres de Discord/Telegram?
3. ¿Qué debe hacer el bucle si la comprobación post-escritura detecta 0 bytes?
4. ¿En qué casos es admisible redactar el informe sin validador de esquemas?

---

## Notas de verificación (Kanam)

**Núcleo de ingeniería: sólido y correcto - de las mejores del curso, y ya es praxis de este repo:**

- ✅ **Desacoplar ejecución del bucle de la síntesis:** correcto y central (evita la fatiga de contexto).
- ✅ **Contrato intermedio en disco (`evidence.json`)** que sobrevive a compactación/reinicio: correcto y valioso.
- ✅ **Compuerta estricta** antes de renderizar (no avanzar si `verification_passed` es falso / faltan claves).
- ✅ **PITFALL**: no renderizar desde stdout crudo (alucinación de cifras). Correcto.
- ✅ **Resumen ligero al canal, artefacto completo a disco:** exactamente lo que hacemos con HANDOFF/dailies.
- ✅ **Lectura reflexiva post-escritura** (existencia + tamaño>0 + cabecera + parseable): **REMEMBER correcto y central** - es el "verificar el repo real, no el auto-reporte" del AGENTS.md, aplicado a archivos.
- ✅ **Acierta el quiz.**
- ✅ **El pipeline corre tal cual** (Python estándar): reproducí la salida JSON exacta.
- ✅ **`verify_generated_artifact` corre** → `True` sobre el reporte generado.

**Lo que NO coincide con la instalación real:**
- ⚠️ **`workspace_write` / `workspace_read`** como **nombres de tools** no son nativos (verificado). Las herramientas reales son `write`/`edit`/`apply_patch`/`read`. El patrón "escribir y luego releer para verificar" es correcto; los nombres, ilustrativos.
- ❌ **`/home/openclaw/workspace`** es una ruta de ejemplo (en Linux/contenedor); aquí el workspace real es `~/.openclaw/workspace`.
- ❌ **No hay un "pipeline de entrega" nativo** ni `deliverables/` como convención de OpenClaw. Es un patrón a construir (en este repo, el equivalente es la escritura de dailies/HANDOFF + commit por path).
- ⚠️ **`datetime.utcnow()`** está **deprecado** en Python moderno (conviene `datetime.now(timezone.utc)`); en 3.9 aún funciona sin warning.

**Verificación ejecutable:**
- ✅ **El script del pipeline corre y produce la salida prometida** (con la ruta base ajustada). Es una de las pocas lecciones donde el material es correcto *y* ejecutable.
- ✅ `verify_generated_artifact` verificada.

**Patrón (vigésimo quinto caso):** **excelente ingeniería** (embudo de fases, contrato intermedio en disco, compuerta estricta, resumen ligero, lectura reflexiva) que **el repo ya practica** (dailies/HANDOFF derivados, verificación post-escritura). Únicos desajustes: nombres de tools y rutas ilustrativas. **Cierra el Módulo 5.**

**Cierre del Módulo 5.** Con esta lección se completan las 5 lecciones de *Encadenamiento en Bucle Agéntico* (L21-L25). La Lección 26 abre el **Módulo 6: Especialización y Coordinación Multiagente** (arranca con *Segmentación de Dominios entre Agentes Dedicados*).
