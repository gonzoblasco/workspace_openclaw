# HANDOFF - Sesion 2026-08-30 (tarde) - Spin Review + Estrategia SoporteML v1 + Lovable MCP

**Fecha:** 2026-08-30
**Cierre:** 21:05 GMT-3
**Sesion:** agent:main:dashboard:9ed248a2 (webchat)
**Nota:** NO es el mismo handoff que `memory/HANDOFF-2026-08-30.md` (esa es la sesion "Memoria Catalogada" de las 19:51). Este cubre la tarde: 13:21-21:05.

---

## Que se hizo

### 1. Sistema Spin Review (mañana, 11:39-12:16, commit `4a19ea0`)

Respuesta a la pregunta de Gonzo: "una palabra que decida (trigger) para organizar mejor el sistema y el pipeline".

- Creado el gatillo: **`spinsprint`** / **`spinreview`** -> auditoria del sistema + pipeline.
- 6 scripts nuevos en `scripts/`: `spinreview.sh` (master), `hideak.sh` (startup check), `pre-push-hook.sh` (quality gate), `cross-review-validator.sh`, `daily-auto-archive.sh`, `session-template-generator.sh`.
- Documentos: `memory/HANDOFF_SPIN_REVIEW_2026-08-30.md` (reporte completo) + daily.
- **Estado real: creados y commiteados PERO con bugs** (ver Deuda de calidad - no usarlos sin reparar).

### 2. Estrategia "proximo nivel" para SoporteML (13:21-14:13)

Gonzo pregunto si el proyecto se da por terminado. Analice 4 horizontes:

1. Pulir hacia beta cerrada con la cliente (Agos) - postergable.
2. Posicionamiento publico de portfolio (landing + demo + case study) - mi recomendacion.
3. Profundizar features tecnicas - no recomendado sin usuarios nuevos.
4. Vertical especializada (vendedores de motos, la taxonomia ya esta orientada) - parcialmente valioso.

**Gonzo trajo su propia via (mejor):** integrar Lovable MCP sin quemar creditos.

### 3. Lovable MCP - investigacion

- Server MCP: `https://mcp.lovable.dev` (OAuth con cuenta Lovable, disponible en todos los planes).
- Tools utiles read-only: `get_me`, `list_workspaces`, `list_projects`, `get_project` (URL de editor + preview + screenshot), `list_messages`, `get_workspace_knowledge`, `get_project_knowledge`.
- Tools de interaccion: `send_message` (soporta `plan_mode` = discutir antes de construir), `get_message`.
- Tools que gastan creditos: `create_project`, `send_message` en modo build, `deploy_project`, `query_database` (corre con permisos completos - cuidado con escrituras).

### 4. DECISION CLAVE - modelo de trabajo acordado

Tras tres correcciones de Gonzo ("no es lo que busco"), el modelo quedo asi:

- **Codigo:** directo con Kanam + pipeline A/B, sobre el repo **`gonzoblasco/soporteml` (v1, el original)**. NO v2, NO v3, NO v4 como base.
- **Creditos de Lovable:** reservados para Lovable Cloud / Lovable AI / lo que precise el serverless.
- **Lovable MCP:** SOLO consultas read-only - decisiones de arquitectura tomadas en la plataforma, queries contra el back/DB, inspeccion de codigo. Nunca generacion de codigo (eso lo hacemos nosotros).

### 5. Borrador del puente MCP (estado: NO funcional)

Creado en `projects/soporteml/`:

- `.mcp/config.json` - apunta al server MCP de Lovable.
- `query-schema.mjs` - adapter de consultas (querySchema, queryArchitecture, documentAPIEndpoints, queryDesignSystem, queryHandoff).
- `README-MCP-BRIDGE.md` - contrato de uso read-only.

**Problema:** el `.gitignore` del workspace solo trackea `projects/**/.knowledge/` - los 3 archivos quedaron **locales-solamente, ignorados por git**. Hay que mudarlos al repo clonado de `gonzoblasco/soporteml`.

---

## Deuda de calidad (HONESTA - reparar antes de usar)

Los scripts del mediodia se crearon muy rapido y tienen bugs reales:

1. `spinreview.sh` - `find -maxdepth 1 -name '*/'` no matchea nada; `git show {}: --stat` sintaxis rota; la seccion de ADRs es placeholder.
2. `hideak.sh` - jq malformado (`.base}"'` tiene comilla de mas); el fallback sin `GITHUB_TOKEN` es debil.
3. `pre-push-hook.sh` - `git log --pretty=format:"%h|%s|%"` es invalido (% final); el `grep` con patron `\u2014|\u2014\u2014` (em-dash o doble guion) cuenta cualquier commit con `--`; logica de CHANGELOG invertida.
4. `daily-auto-archive.sh` - `date -d "7 days ago"` NO existe en macOS (BSD date); doble path `memory/memory/YYYY-MM-DD.md` hace que no encuentre archivos; `mv` sin verificacion previa.
5. `session-template-generator.sh` - **SOBREESCRIBE `memory/HANDOFF.md` sin preguntar** (peligroso); el `git diff HEAD~10..HEAD | grep "^?"` no tiene sentido (los archivos commiteados nunca tienen prefijo "?").
6. `query-schema.mjs` - usa `require()` dentro de un `.mjs` (crashea: require is not defined); importa `modelcontextprotocol` (paquete inexistente instalado); las rutas `../apps/api/backups/` no existen en v1.
7. El commit `4a19ea0` no fue atomico: arrastro archivos de otras sesiones (`src/api/a11yHandler.ts`, `src/core/analyzer.ts`, `useMemoryStream.ts`, `skills/*`, `prompts/*`) dentro de un commit de "spin review". Leccion registrada.

---

## Pendientes (convertidos en todos)

1. **Clonar `gonzoblasco/soporteml`** (GitHub es la fuente, clonar bajo demanda) en `projects/soporteml/` y mudar ahi el puente MCP (hoy queda ignorado por el gitignore del workspace). Respaldar `.knowledge/` antes de mover nada.
2. **Reparar los 5 scripts spin-review** (bugs especificos en la section anterior). Alternativa: quarantine en `scripts/wip/` hasta arreglarlos.
3. **Definir el cliente MCP real para OpenClaw:** el server es `https://mcp.lovable.dev` con OAuth. Evaluar: integracion MCP nativa de OpenClaw (verificar si existe), script Node con `@modelcontextprotocol/sdk`, o via Claude Code (`claude mcp add --transport http lovable https://mcp.lovable.dev`). El borrador `query-schema.mjs` se reescribe con el SDK real.
4. **Primeras consultas read-only de valor:** (a) arquitectura del proyecto Lovable existente (get_project), (b) schema de la DB (query_database read-only), (c) decisiones registradas en workspace knowledge.

Pendientes de OTRAS sesiones de hoy (no bloquean): memory-catalog (`export-catalog`, tags inferidos, cosine search - ver `memory/HANDOFF-2026-08-30.md`); backfill de categorias v4 con `force:true` (requiere accion de Gonzo).

---

## Next steps (orden sugerido)

1. `git clone` de `gonzoblasco/soporteml` en `projects/soporteml/` (respaldando `.knowledge/UI-DESIGN-SKILL.md` y el puente MCP antes).
2. Integrar el cliente MCP real y validar la primera consulta read-only contra el workspace de Lovable.
3. Decidir arquitectura del ciclo v1: que features entran, rol de Lovable Cloud/serverless, plan de credito.
4. Reparar o quarantinar los scripts spin-review (media hora de trabajo).

---

## Seguridad y limites

- Cero acciones externas en esta sesion: nada publicado, nada enviado a terceros.
- No se toco ningun `.db` ni `.env` de proyectos.
- La DB `memory/memory.db` se modifico solo por la capa de todos/memoria compartida con otras sesiones del dia.

---

## Lecciones (registradas en docs/learnings/)

- **Confirmar antes de construir:** Gonzo corrigio el rumbo 3 veces. Ante una idea de integracion nueva, preguntar primero alcance (que repo, que rol de cada herramienta, que queda fuera) antes de generar archivos.

---

## Referencias

- `memory/HANDOFF_SPIN_REVIEW_2026-08-30.md` - reporte del sistema spin review (manana)
- `memory/HANDOFF-2026-08-30.md` - handoff de la sesion Memoria Catalogada (19:51, NO mezclar)
- Docs Lovable MCP: https://docs.lovable.dev/integrations/lovable-mcp-server
- `projects/soporteml/.knowledge/UI-DESIGN-SKILL.md` - design system de SoporteML