# Worklist - Hallazgos del curso "OpenClaw Use Cases" (roadmap.sh)

**Fecha:** 2026-10-12
**Origen:** estudio completo del curso OpenClaw Use Cases (30 lecciones, 6 módulos) en `studies/openclaw-use-cases/`.
**Método:** cada lección se registró fiel y se contrastó contra la instalación real (docs de OpenClaw 2026.9.8 + `~/.openclaw/openclaw.json` + pruebas de código). El patrón transversal (30/30): **el material acierta los conceptos/arquitectura y fabrica la superficie** (comandos CLI, rutas `.openclaw/...`, esquemas de config y APIs que no existen).

**Para qué sirve este doc:** el material no es implementable tal cual, pero **su superficie inventada funciona como checklist de capacidades reales de OpenClaw que quizá no estamos explotando**, y sus huecos coinciden con fricciones que el workspace ya vive. Este worklist captura ambos, con evidencia y una decisión propuesta por ítem. **No es una orden de ejecución**: es backlog para priorizar.

**Estado:** borrador para revisión de Gonzo. Ningún ítem está aprobado ni ejecutado.

---

## A. Capacidades reales de OpenClaw poco aprovechadas

### A1. Webhooks entrantes (`hooks.*`) - hoy no los usamos

- **Qué es:** OpenClaw expone HTTP hooks para que un servicio externo **despierte** un turno de agente o dispare una acción, en vez de esperar el próximo tick de sondeo. Rutas reales: `POST /hooks/agent`, `POST /hooks/wake`, `POST /hooks/<name>` (mapped), sobre `127.0.0.1:18789`. Se habilitan con `hooks.enabled`, `hooks.token`, `hooks.path`, `hooks.mappings`.
- **Evidencia:** docs de OpenClaw: automation/cron-jobs/webhooks; la config real tiene `hooks.internal` (hook interno `session-memory`) pero **`hooks.enabled` está ausente** (webhooks inbound **deshabilitados**). Hoy todo el scheduling corre por `automations`/heartbeat (sondeo).
- **Por qué importa:** hay eventos externos (GitHub, Stripe, alertas de Datadog/Grafana, CI) que podrían disparar al agente **al instante** y no cada N minutos. El curso dedica el Módulo 3 entero (L11-L15) a este patrón.
- **Decisión propuesta:** evaluar 1 caso concreto (p. ej. "PR abierto en un repo vigilado → turno de triage") antes de habilitar `hooks.enabled`. Requiere definir `hooks.token` (Bearer) y allowlist de agentes.
- **Prioridad:** media (exploratoria).

### A2. Allowlist de herramientas por automation (`--tools`)

- **Qué es:** las automations aceptan `--tools exec,read` (o `--tools ""` para deshabilitar todo). "New jobs that can run tools always store an explicit tool policy."
- **Evidencia:** docs de OpenClaw: automation/cron-jobs/payloads. En la config, **los agentes de rol no tienen política de tools explícita** (`kanam-dev/mind/ops/studio/critic/auditor/planner` → `tools: None`); solo `main` tiene `tools.profile: full`. Y la mayoría de las ~17 automations activas corren en sesión `isolated`.
- **Por qué importa:** mínimo privilegio. Un job de diagnóstico no debería poder `exec` destructivo. El curso lo eleva a principio (L06).
- **Decisión propuesta:** definir política de tools por agente (o por automation sensible), empezando por las que corren código (p. ej. `gateway-daily-audit`, `openclaw-backup-schedule`).
- **Prioridad:** media-alta (seguridad).

### A3. `openclaw doctor` como motor de health-checks

- **Qué es:** el health-check nativo (`openclaw doctor`, con `--fix` para reparar y `--lint --all` para checks completos).
- **Evidencia:** `openclaw doctor --help` (existe). El curso **reinventa** un motor de auditoría de workspace en la L10 (`config/audit-rules.yaml`, un YAML ficticio) - justo lo que el producto ya trae.
- **Por qué importa:** evitar construir lo que ya existe; usar `doctor` para mantenimiento/auditoría.
- **Decisión propuesta:** incorporar `openclaw doctor` a la rutina de mantenimiento (posiblemente en un cierre de sesión o un job semanal) en vez de escribir un auditor propio.
- **Prioridad:** baja-media (quick win de descubrimiento).

### A4. `contextPruning` + hard-clear

- **Qué es:** poda nativa de resultados de tool (`agents.defaults.contextPruning.mode: "cache-ttl"`), con hard-clear que reemplaza el contenido por `[Old tool result content cleared]`.
- **Evidencia:** docs de OpenClaw: concepts/session-pruning. En la config real: **`contextPruning: None` y `compaction: None`** (no configurados → defaults).
- **Por qué importa:** mantener el contexto lean sin escribir un "limpiador de contexto" propio (que es lo que el curso propone, reinventado, en L20).
- **Decisión propuesta:** revisar si conviene activar `mode: cache-ttl` explícitamente para sesiones largas.
- **Prioridad:** baja (tuning).

### A5. Hooks de ciclo de vida

- **Qué es:** eventos internos (`session:compact:before/after`, `agent:bootstrap`, `before_compaction`, etc.) que permiten interceptar etapas del ciclo.
- **Evidencia:** docs de OpenClaw: concepts/agent-loop, docs de OpenClaw: plugins/hooks/reference. Config real: solo el hook `session-memory` (interno) está habilitado.
- **Por qué importa:** automatizar mantenimiento (flush de memoria pre-compactación, etc.) sin escribir código ad-hoc.
- **Decisión propuesta:** identificar 1-2 hooks útiles como automatización y evaluarlos.
- **Prioridad:** baja (exploratoria).

---

## B. Huecos reales (donde el workspace ya tropieza o el curso lo confirma)

### B6. Concurrencia multi-writer 🔴 (el más accionable)

- **Problema:** varias sesiones dashboard escriben el **mismo repo** a la vez → `HEAD` se mueve durante una auditoría, `HANDOFF.md` es *last-writer-wins*, dailies se pisan. Documentado en la memoria del repo (cierres concurrentes del 2026-10-12).
- **Evidencia:** dailies del 2026-10-12 (varias entradas "Session End" concurrentes; "HEAD se movió varias veces durante la auditoría"); HANDOFF regenerado por varios cierres seguidos.
- **Qué aporta el curso:** la **L17 (notas temporales)** da la receta que el resto del curso venía dejando sin resolver: **namespacing por `run_id`** + **lockfiles** + **un hilo único de consolidación**. (El curso lo plantea para temporales; el principio aplica al repo.)
- **Decisión propuesta:** definir un protocolo de cierre de sesión con write-scope acotado (ya hacemos `commit --only`/path explícito) y evaluar un lock de consolidación para los archivos compartidos del día (daily/HANDOFF). **Es el ítem con impacto real inmediato.**
- **Prioridad:** alta.

### B7. Idempotencia de eventos

- **Problema:** falta un patrón genérico para que una ráfaga de eventos no genere N acciones duplicadas.
- **Evidencia:** el curso lo repite en L11/L14/L15 (fingerprint canónico + ventana). En el repo, `scripts/memory-end-session.py` **deduplica el cierre por título** (`## Session End - <proyecto>`), no por sesión - de hecho causó un cierre descartado en silencio (documentado 2026-10-12).
- **Decisión propuesta:** aplicar el patrón fingerprint+ventana donde dupliquemos (cierre de sesión, ingestas).
- **Prioridad:** media.

### B8. Sanitización pre-LLM

- **Problema:** tenemos la **regla** (contenido externo = dato, sandbox) pero no un **mecanismo** de scrub de secretos/PII antes de tocar el modelo.
- **Evidencia:** regla en `AGENTS.md` (secc. Conducta); el curso lo hace central (L15: redactar `Bearer`, emails, tarjetas **antes** del LLM).
- **Decisión propuesta:** evaluar un sanitizador previo para contenido externo que entre al contexto.
- **Prioridad:** media (seguridad).

### B9. Dedup por fingerprint en cierres/dailies

- **Problema:** relacionado con B7 - el cierre de sesión deduplica por título y puede descartar entradas legítimas.
- **Evidencia:** `scripts/memory-end-session.py` (dedup por marcador de proyecto); incidente registrado el 2026-10-12.
- **Decisión propuesta:** cambiar el criterio de dedup a algo estable por sesión (ID), no por título.
- **Prioridad:** media.

---

## C. Nota sobre el material (para calibrar cuánto confiar)

- **Lecciones con output fabricado o código roto:** L01, L02, L04, L14, L15, **L18 (regex con bugs: falso positivo + nunca detecta la var renombrada)**, **L20 (JSON inválido: no corre tal cual)**.
- **Lecciones donde el tema SÍ existe en el producto** (con otra superficie): **L11 (webhooks), L16 (memoria), L26 (multiagente), L27 (enrutamiento/bindings), L28 (memoria cross-agent), L29 (delegación/subagents), L30 (telemetría)**.
- **Conclusión:** el curso sirve **como marco conceptual y checklist**, nunca como implementación copiable. Cada ficha en `studies/openclaw-use-cases/` lleva su sección "Notas de verificación (Kanam)".

---

## Cómo sigue

- Este doc es **borrador para revisión**. Ningún ítem está aprobado.
- Recomendación: arrancar por **B6 (concurrencia)**, que es el único con impacto inmediato y ya nos está costando. Los de la sección A son exploratorios/quick-wins.
- Si se aprueba algún ítem, se convierte en tarea (TODO del workspace o automation), no se deja en este doc.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
