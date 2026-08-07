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
- **Regla de merge:** cuando venga algo del workspace (pull/rebase con conflictos), hacer merge, no reset. El soft reset descarta commits de la otra maquina.
- **Regla de escritura:** guion comun (-) siempre. NUNCA guion largo (—) ni em dash. Issues, PRs, comments, docs, memorias, todo. Esta en USER.md tambien.
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

### Sport Cars: validación visual obligatoria para sitios de marca
El build pasando no garantiza que el sitio se vea profesional. Para proyectos con identidad visual, la validación con screenshots + evaluación crítica debe ser parte del cierre de cada iteración. Issues como contraste bajo, colores inconsistentes o títulos engañosos no los detecta Biome.

### Feature flags portable: no hardcodear en UI
El primer flag (`showPrices`) se implementó con provider client-side + localStorage + componente `PriceDisplay`. El panel de flags solo se renderiza en desarrollo. El siguiente paso es extraerlo a `@workflow-kit/feature-flags` para reuso.

### No commitear mockups intermedios
Los mockups y screenshots de iteración (v2, v3, etc.) son ruido en el repo del proyecto. Solo conservar la evidencia final (home/catálogo) en el commit de release; los intermedios van al daily note o a un artifact.

## Lecciones del 2026-08-04

### npm 404 en publish scoped ≠ problema de scope
El 404 `PUT .../@scope%2fpackage` al publicar NO significa que el scope esté mal. Primero verificar `npm whoami` — si da 401, el fix es `npm login`, no tocar el scope. El scope `@usuario/` se resuelve solo cuando coincide con el username logueado. (Pasó con `@gonzoblasco/create-stack`.)

### npm login usa browser OTP flow
El login de npm ahora abre browser (OTP), no acepta token en consola. Los tokens que saltan 2FA se están restringiendo — para CI a futuro usar tokens con `mfa=publish` o `automation`.

## Consolidación de Skills — 2026-08-06

### Set de skills reducido de 96 a 60 activas (58 archivadas, nada borrado)
Se adoptaron las 24 skills de `addyosmani/agent-skills` como base de ingeniería (ciclo Define→Plan→Build→Verify→Review→Ship). 5 de ellas absorben funcionalidades de skills propias redundantes:
- `frontend-ui-engineering` ← accessibility-studio, ui-design, ui-generation, anti-slop-design, a11y-audit-agent, sovereign-accessibility-auditor
- `code-review-and-quality` ← anti-pattern-czar, code-review-agent, code-mentor, review-quality
- `debugging-and-error-recovery` ← debug-agent, debug-investigation, failure-memory
- `spec-driven-development` ← build-scaffold, anydocs, spec-miner
- `planning-and-task-breakdown` ← timeline-builder, gh-issue-planner, brw-plan-my-day

### Consolidación no-dev (2026-08-06, 21:40) - 60 a 59 activas
Las 29 skills no-dev NO se solapan entre sí (independientes), así que la consolidación no es por duplicación sino por decisión de uso. Primera fusión: `adhd-daily-planner` → dentro de `adhd-assistant` (energy windows, transition buffers, dopamine sequencing, shutdown ritual, recovery protocol). Eliminada de las 3 ubicaciones (workspace, mirror .github, kanam-skills). Total activas: 59.

Candidatas restantes a decidir con Gonzo: `content-serializer`, `curriculum-builder`, `brand-name-forge`, `checkmate`. El resto de las no-dev están bien como están.

Las 58 skills redundantes viven en `skills/archive/` (con README con mapa completo de reemplazo). Se preservaron las skills de vida/creatividad/infraestructura de Gonzo (adhd, apple-photos, supabase-assistant, sql-insight, db-readonly, etc.). Detalles en `memory/2026-08-06.md`.

## Proyectos activos

### kanam-skills (nuevo 2026-08-06)
- Repo público + web de agent skills. https://github.com/gonzoblasco/kanam-skills
- 58 skills (engineering SDLC + vida/creatividad/infraestructura) en formato Agent Skills universal
- Diferenciador: único set probado en OpenClaw. Comando: `npx skills add gonzoblasco/kanam-skills`
- Web GitHub Pages: https://gonzoblasco.github.io/kanam-skills/ (generador estático sin deps)
- Vive en `projects/kanam-skills/` (doble git, público, no filtra memoria personal)
- Pendiente: dominio propio, mejorar preview de skill pages, postear en LinkedIn

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
- Scaffolder opinado para Next.js 15. Publicado en npm como `@gonzoblasco/create-stack`. Diferenciación real vs create-next-app.
- **Estado:** vivo, no tocar. Necesita evolución, no reset.
- Gonzo quiere mantener el scope `@gonzoblasco/` como firma (posible rename futuro de identidad a "kanam", pero el scope queda con firma gonzoblasco).
- `npm pkg fix` ya corrió — key de bin limpia (`create-stack`).

### workflow-kit
- Portable AI agent workflow skills. Publicado en npm. Uso diario.
- **Estado:** vivo, no tocar. Evoluciona naturalmente.

### soporteml
- CRM multi-tenant para vendedores de Mercado Libre con IA. EL-1 a EL-5 completos.
- **v1** (`soporteml`): versión de referencia. Design system estable.
- **v2** (`soporteml-v2`): **EXPERIMENTO DESCARTADO. NO usar de referencia.**
- **v3** (`soporteml-v3`): repo nuevo, en arranque (2026-08-07). Se construye sobre v1 con el design system aclarado desde el día uno. Objetivo: versión definitiva.
- **Docs de v3 en `.knowledge/`:** `UI-DESIGN-SKILL.md` (estándar de implementación, específico de SoporteML), `DESIGN-GUIDE.md` (identidad desde v1), `DESIGN-GUIDE-LOVABLE.md` (guía oficial de Lovable = fuente de verdad visual), `prompts/` (guía de diseño + schemas BD).
- **Pendiente v3:** pedir schemas de BD + edge functions a Lovable (prompt listo), reconciliar tokens nuevos de la guía de Lovable (`--primary-muted`, `--primary-strong`, `--informative`, `--surface-active`), scaffold, implementación.

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
| kanam-skills | — | Repo público + web de agent skills (engineering + life). https://github.com/gonzoblasco/kanam-skills |
| quedamos | — | App PWA de matching para salidas |
| sportcars | ✅ | — |
| cabala | ✅ | Eliminado — build roto |
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
| react-18-design-patterns | ✅ | Libro React 18 (Packt), actualizado a React 19 LTS |
| react-anti-patterns-book | ✅ | Libro React Anti-Patterns (Packt) |
| hyatt-copilot-agent | ✅ | Agente IA para staff de hoteles Hyatt |

## Repos eliminados

- **Moderno-Access-Virtual-Plate** → eliminado
- **antigravity-developer-stack** → eliminado (contenido migrado a ai-developer-stack)
- **copilot-skills** → eliminado (reemplazado por workflow-kit)
- **futbol-ps2** → eliminado (MVP completo, descartado)
- **kanam** → eliminado (PWA sistema operativo personal con IA, decisión de Gonzo 2026-08-06; BRIEF + ROADMAP archivados en `projects/_archived/kanam/`)
- **chatgpt-project-architect** → archivado (absorbido por AGDS)
- **0001** → eliminar o archivar (sin propósito)
- **prueba_minecraft_claude_code** → eliminar o archivar (experimento abandonado)

## Lecciones del 2026-08-03

### Patrón por inercia vs contexto cambiado
Cuando un patrón se repite muchas veces (7+ niveles de bootcamp con carpeta nueva), el riesgo no es equivocarse en el patrón — es aplicarlo por inercia cuando el contexto ya cambió. La señal de alerta no es "¿lo sé hacer?" sino "¿es este caso realmente igual a los que ya resolví?". Pasó en el Nivel 8 del bootcamp (convergente, no lineal — transformaba el N7, no creaba carpeta nueva). ADR: `projects/ai-engineering-bootcamp/.knowledge/ADR-001-niveles-convergentes.md`.

### AI Engineering Bootcamp — COMPLETO ✅
- **10/10 niveles completados.** N1-N4 fundamentos (generar, prompts, workflows, templates), N5-N6 calidad/seguridad (auditar, CI/CD), N7-N8 arquitectura/producción (microservicios, cloud), N9 estándares/dashboard, N10 sistema completo (capstone).
- N8-N10 son convergentes: reusan el sistema del N7 (vive dentro de `projects/level-07-microservices/`).
- El N10 junta todo: auth + users + orders + notifications + gateway + CI/CD + dashboard + cloud. Probado: gateway enruta, health agregado ok, register/login/orders funcionan, 401 en credenciales malas.

### Reflexión del curso (meta-aprendizaje) — COMPLETO ✅
- El patrón "detectores locales + validación cruzada / IA contextual" apareció **5 veces** (N3, N5, N6, N8, N9) → **formalizado como skill `pipeline-detector`** (aplicado, con references/detector-templates.md).
- Formato nivel de bootcamp (teoría + práctica + LinkedIn + self-review) es un template de skill reusable.
- Los proyectos resueltos son el "contrato" del curso — demuestran que el nivel es posible, no son la respuesta.
- Falta un mecanismo de verificación automática al final de cada nivel (tests contra el proyecto del alumno).
- **El nivel 7 es el núcleo físico de los niveles 7-10**: N8 (cloud), N9 (estándares) y N10 (sistema completo) extienden el mismo folder `projects/level-07-microservices/` (ADR-001). El nombre del folder confunde — el README ahora lo documenta como "Niveles 7-10" con tabla de acumulación y diagrama de arquitectura.

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
