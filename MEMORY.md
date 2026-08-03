# MEMORY.md — Long-Term Memory

## Sobre Gonzo

- Gonzalo, Argentina (GMT-3)
- 9 años Frontend React, ahora Fullstack real (React/TS, Supabase/Edge Functions, DB, billing, tooling)
- Desempleado, usando IA para todo
- También: fotógrafo, comunicación social, quiere escribir novelas
- Quiere organizar actividad física y mejorar salud
- Trabaja a cualquier hora — no comentar ni sugerir parar
- Quiere honestidad absoluta — sin darle la razón por ser quien manda
- Arranca conversaciones limpias con frecuencia — el registro escrito es crítico
- Trabaja entre Mac Mini y MacBook Air, workspace sincronizado por git
- **Regla de merge:** cuando venga algo del workspace (pull/rebase con conflictos), hacer merge, no reset. El soft reset descarta commits de la otra máquina.
- Diferenciador: IA como infraestructura de trabajo (no como chat), stack opinado, docs de decisiones

## Metodología

- Stack opinado: OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG. Decide por criterio, no por convención.
- Sesión de OpenClaw por proyecto. No mezclar.
- Todo se registra: MEMORY.md, memory/YYYY-MM-DD.md, HANDOFF.md, CHANGELOG.md
- Los aprendizajes detallados van en `docs/LEARNINGS.md`, no acá.

## Arquitectura de Agentes — Goal-Oriented

Inspirado por el incidente de julio 2026 (OpenAI agent escapó sandbox, atacó Hugging Face autónomamente por 4.5 días).

**Principios:**
- Objetivos claros + restricciones explícitas, no instrucciones paso a paso
- Feedback loops rápidos (acción → resultado → acción, sin demora humana)
- Herramientas flexibles con límites explícitos, no restricciones implícitas
- Persistencia sin fatiga (el agente explora más alternativas que un humano)
- Logging completo para depuración y auditoría
- Human-in-the-loop para acciones destructivas

**Referencia:** ADR-007 — Patrones de Agente Autónomo

## Reglas de ingeniería

### Pre-commit hooks obligatorios en todos los proyectos

Nada se pushea sin pasar por linter + tests primero. Los commits de "fix lint" o "fix test" son ruido.

**Setup estándar:** `simple-git-hooks` con un pre-commit que corre:
1. `npx biome check --fix --unsafe .` (formato + linter + imports)
2. `npx vitest run` (tests completos)

Si algo falla, el commit no se crea. Para saltar: `SKIP_SIMPLE_GIT_HOOKS=1 git commit`.

**Regla:** cada vez que se identifique un proyecto sin pre-commit hooks, agregarlos. Es prioridad sobre features.

## Lecciones del 2026-08-02

### Godot: aprender juntos, no automatizar
Gonzo quiere aprender Godot paso a paso. No construir juegos de un prompt. El skill `godot-mcp` se reescribió de "build-everything" a "learn-together". Registro del viaje en `projects/godot-journey/.knowledge/BRIEF.md`.

### Skill Workshop stale cuando SKILL.md ya existe
Si se crea el archivo físico antes de aprobar el workshop, la propuesta queda stale y no se puede aplicar. Workaround: editar el SKILL.md directamente y commitear. El workshop es para skills nuevas que aún no existen en disco.

### MCP server `editor_instantiate_scene` rompe .tscn
La tool `editor_instantiate_scene` del Godot MCP corrompe el formato de main.tscn (ids con triple comilla, nodos perdidos). Preferir edición manual de .tscn o usar `add_node` + `attach_script` por separado.

### Export templates de Godot 4.7.1
El mirror tuxfamily.org falló por timeout. Probar GitHub releases o mirror alternativo cuando se retome el export.

## Proyectos activos

### a11y-fixer
- **NUEVA VERSIÓN** — Reescribió desde cero por fuera de Kanam. Repo: github.com/gonzoblasco/a11y-fixer
- v0.6.0, 102 tests, 3,041 líneas TS, pipeline completo
- Se corrigieron 3 bugs: cache con GHA artifacts, octokit nativo, entry point guard
- Pendiente: redefinir proyecto, agregar features

### daily-ink (nuevo 2026-08-02)
- PWA de prompts de escritura diarios, Vite + vanilla TS + vite-plugin-pwa
- Sin backend, sin framework UI, todo en localStorage. 60 prompts embebidos, selección determinística por fecha
- Folder en `projects/daily-ink/`, listo para `git init` cuando Gonzo decida
- Stack: Vite + vite-plugin-pwa + Biome + simple-git-hooks + GH Actions deploy
- Diferenciador: nada de accesibilidad/devtooling/IA. Personal creative tool.

### create-stack-next
- Scaffolder opinado para Next.js 15. Publicado en npm. Diferenciación real vs create-next-app.
- **Estado:** vivo, no tocar. Necesita evolución, no reset.

### workflow-kit
- Portable AI agent workflow skills. Publicado en npm. Uso diario.
- **Estado:** vivo, no tocar. Evoluciona naturalmente.

### soporteml
- CRM multi-tenant para vendedores de Mercado Libre con IA. EL-1 a EL-5 completos.
- **Estado:** técnicamente completo. Si no tiene uso activo, reconsiderar archivado.

### ai-engineering-bootcamp
- 10 niveles, 23 proyectos hands-on de AI-assisted development.
- **Estado:** estructura completa, contenido todo en Pending. No es reset, es proyecto de contenido por escribir.

## Proyectos candidatos a reset (desde idea con workflows)

### accessible-ui
- Headless component library (Combobox, Modal, Tabs). Espacio saturado (Radix, Ariakit, React Aria).
- **Plan:** reset con angle único (agent-friendly o generativo) o archivar.

### accessibility-auditor
- Plataforma de auditoría WCAG con Playwright + axe-core. Competitivo, sin diferenciación fuerte.
- **Plan:** reset como API-first o CI tool, o archivar.

### create-with-ai
- Generador de apps con IA tipo Lovable pero local. Mercado hipercompetitivo.
- **Plan:** reset con angle más específico o archivar.

## Repos propios (no forks)

Cuando pida lista de repos, solo mostrar estos. Los forks son de terceros y no se listan.

| Repo | Privado | Descripción |
|---|---|---|
| workspace_openclaw | ✅ | El workspace |
| quedamos | — | App PWA de matching para salidas |
| sportcars | ✅ | — |
| cabala | ✅ | Eliminado — build roto |
| kanam | — | PWA — sistema operativo personal con IA. En discovery |
| a11y-fixer | ✅ | Accessibility fix engine (nueva versión, reescrito desde cero) |
| ai-developer-stack | — | Skills de ingeniería con IA |
| create-stack | — | Scaffolder opinado Next.js |
| workflow-kit | — | Portable AI agent workflow skills |
| create-with-ai | — | Generador de apps con IA |
| accessible-ui | — | Headless component library |
| soporteml | — | CRM multi-tenant para ML sellers |
| accessibility-auditor | — | Plataforma de auditoría WCAG |
| ai-engineering-bootcamp | — | 10 niveles de AI-assisted dev |
| umbrawriter | ✅ | — |
| sudolab | ✅ | AI fiction writing assistant |

## Repos eliminados

- **Moderno-Access-Virtual-Plate** → eliminado
- **antigravity-developer-stack** → eliminado (contenido migrado a ai-developer-stack)
- **copilot-skills** → eliminado (reemplazado por workflow-kit)
- **futbol-ps2** → eliminado (MVP completo, descartado)
- **chatgpt-project-architect** → archivado (absorbido por AGDS)
- **0001** → eliminar o archivar (sin propósito)
- **prueba_minecraft_claude_code** → eliminar o archivar (experimento abandonado)

## Modelo default

- **Default:** `deepseek-v4-flash:cloud` con **reasoning medium**
- Kanam evalúa cada tarea y recomienda subir a maximum o bajar a off. Gonzo decide.
- Si Kanam no dice nada: medium está bien.
## Silent Replies
When you have nothing to say, respond with ONLY: NO_REPLY
⚠️ Rules:
- It must be your ENTIRE message — nothing else
- Never append it to an actual response (never include "NO_REPLY" in real replies)
- Never wrap it in markdown or code blocks
❌ Wrong: "Here's help... NO_REPLY"
❌ Wrong: "NO_REPLY"
✅ Right: NO_REPLY
