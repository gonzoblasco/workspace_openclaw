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
- **Regla de alcance (2026-08-11):** NUNCA salir de `.openclaw/` para buscar archivos. El workspace es el único lugar de trabajo. Si un archivo está fuera (Desktop, Documents, etc.), pedir a Gonzo que lo mueva o lo pegue - no ir a buscarlo. (Error: salí al Desktop a buscar el CV, bloqueado por sandbox de macOS.)
- **Terminología de sesión:** se dice "guardar sesión", no "cerrar sesión" (2026-08-11). El framing de "guardar" = save point (guardar estado y seguir, se puede repetir), "cerrar" sugiere apagón final. Aplicado en skills/, .github/skills/, kanam-skills/, AGENTS.md.
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

## Lecciones del 2026-08-10

### Commit vacío para refrescar mergeability de PRs
`git commit --allow-empty` re-dispara los checks de CI y fuerza a GitHub a recalcular el mergeability de un PR. Útil cuando un PR muestra CONFLICTING/DIRTY desactualizado. PERO puede revelar conflictos reales que estaban ocultos (pasó con astryx #4023 y TanStack #7834).

### El main del fork puede estar desactualizado vs el upstream
Cuando un PR de fork muestra conflicto, el main del fork puede estar viejo. Siempre fetch del upstream real (`git fetch upstream main`), no del origin (fork). En TanStack #7834, el main real avanzó 70 commits que el fork no tenía - por eso GitHub veía conflicto y yo no.

### `--force-with-lease` falla con "stale info" tras rebase
Tras un rebase que reescribe el historial, `--force-with-lease` falla porque la ref remota local no se actualizó. Usar `--force-with-lease=<branch>:<sha-esperado>` con el sha del remote verificado (fetch primero, confirmar que solo hay commits propios).

### Cruce de ramas en PRs de astryx
La rama de #4023 arrastraba el commit de #4022 (WCAG contrast) porque se creó desde esa base. Al rebasear para dropear los commits ajenos, el PR queda limpio (solo el fix del Selector). Verificar siempre que una rama de PR no contenga commits de otro PR.

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

### carbon-design-system/carbon (colaboración OSS - 2026-08-07)
- Repo de IBM (Carbon Design System), contribución en a11y (ComposedModal).
- **PR #22887** (feat: add aria-describedby prop support to ComposedModal, closes #21342): reviewer `sangeethababu9223` pidió tests. Agregué 2 tests (fallback div[role=dialog] + native dialog con feature flag enable-dialog-element). Commit `1921b24`, **MERGEABLE**, esperando re-approval.
- **Stack del repo:** yarn 4 (Berry), lerna monorepo, jest + Babel. Tests corren contra builds de workspace packages (main apunta a lib/dist); jest mockea CSS/SCSS con identity-obj-proxy.
- **Estrategia:** mismo patrón que astryx - un PR a la vez, feedback accionable → arreglar, decisión de dirección → cerrar con elegancia.

### shadcn-ui/ui (colaboración OSS)
- **PR #11465** (fix(react): drain released tail spacer after manual scroll during anchored stream, closes #11125): implementé el fix que validamos con sandengocka en el issue. Gate del re-arm con spacerHeight===0 + drenado del spacer en handleResize. 61 tests verdes, MERGEABLE. Creado 2026-08-10.
- **PR #11198** (InputOTP layout shift): 1 APPROVED (karishma-gidr), falta 2do.
- **PR #11187** (table scrollbar): sin reviews.
- **PR #11180/#11179** (MessageScroller/InputOTP): sin reviews.
- **Nota:** el fork `gonzoblasco/ui` puede estar atrasado vs upstream - crear ramas desde upstream/main.

### facebook/astryx (colaboración OSS - 2026-08-07)
- Repo de Facebook, contribuciones en accesibilidad (AvatarStatusDot).
- **PR #4298** (feat: default accessible labels per variant): pasó review con feedback real de `imdreamrunner` - i18n catalog (useTranslator + keys), changeset `[feat]` con bump `patch`, tests de locale override. Commit `9f99e2209` pusheado, **MERGEABLE**. **APROBADO 2026-08-11** (imdreamrunner, APPROVED, evento #29126084331) - review-required cleared. **CI bloqueado por bug de workflow:** el job `build-storybook` falla con `no merge base` porque `fetch-depth: 50` no alcanza para PRs con merge base a >50 commits (base 3/8 vs main 11/8). Abrí **issue #4912** con diagnóstico + fixes sugeridos, y **PR #4914** implementando el fix (fallback a two-dot diff en analyze-pr.js). A la espera de que el maintainer destrabe el check de #4298 y mergee ambos.
- **PR #4914 (refinado 2026-08-12):** review de maintainer con 5 findings, todos implementados. Ahora el fix hace deepen-and-retry (`git fetch --deepen=200 origin <base>:refs/remotes/origin/<base>`) antes de degradar a two-dot, corrige el claim "never under-reports" (two-dot SÍ puede under-reportar), agrega `diffMode` a analysis.json + caveat en el comment, mejora el warning (e.stderr), y suma 2 regression tests (analyze-pr.test.mjs + generate-pr-comment.test.mjs). Verificado con repo sintético: el deepen recupera el resultado EXACTO (modifiedComponents: ["Card"]) en vez del over-reportado. 4 tests pasan, MERGEABLE. Detalle técnico: el refspec del fetch necesita el nombre de rama sin prefijo `origin/`, y `--deepen` solo actualiza FETCH_HEAD, hay que escribir el ref explícito.
- **Issue #4777** (Avatar pierde status accessibility con composición): comenté posición técnica analizando las 3 opciones (SSR tradeoff en la 2, coupling en la 1, validación AT empírica en la 3). Me ofrecí a correr spike de la opción 3 post-merge.
- **#4777 (10/8):** otro contributor (HelloOjasMutreja) confirmó el bug y levantó un punto válido sobre las ramas interactivas (role=group no mapea a renderAsLink/renderAsButton). Respondí corrigiendo el framing: la opción 3 no es "group que envuelve todo", es "sacar el status del árbol prunado" - como el status ya es position:absolute dentro de un wrapper relative, moverlo a hermano del root es trivial y no rompe el roving focus. Post: issuecomment-5241361605. Pendiente: correr spike empírico (VoiceOver+NVDA) si dan luz verde.
- **Estrategia:** no abrir 2 PRs del mismo tema en paralelo. Dejar mergear #4298, después atacar #4777. Un merge en astryx = hito de portfolio fuerte (repo de Facebook, a11y = especialización de Gonzo).
- **PR #4703 (pagination dots, CERRADO 2026-08-07):** el maintainer `rubyycheung` decidió no mergearlo - el dot treatment es parte de una dirección selected-state más amplia que van a resolver holísticamente. Feedback técnico clave: **en XDS filled = selected**, hacer el active dot hueco invierte la jerarquía. Se cerró con elegancia (no era bloqueo de código, era dirección de producto).
- **Lección OSS:** distinguir entre PR con feedback accionable (se arregla y mergea, como #4298) y PR con decisión de dirección del equipo (se cierra con elegancia, como #4703). Respetar la semántica filled/selected del sistema.
- **Stack del repo:** pnpm monorepo, vitest, StyleX, i18n con catálogo en `packages/core/locales/en.json`, changesets con `[categoria]` + `@contributor`, bump `patch` salvo breaking. Pre-commit hook corre check:repo + eslint + tests. Patrón de labels i18n: `ChatMessageMetadata` (STATUS_CONFIG con i18nKey + useTranslator).

### radix-ui/primitives (colaboración OSS - 2026-08-12)
- Repo de Radix UI, primitivos headless de máximo prestigio en a11y. Fork: `gonzoblasco/gonzoblasco-primitives` (el nombre es distinto porque la cuenta ya tenía un repo `primitives`).
- **PR #4109** (fix(select): announce option position and total for screen readers, fixes #3962): VoiceOver + Chrome anuncia count incorrecto en Select ("Banana, 1 of 3" en vez de "2 of 5"). Causa raíz: Select.Item renderiza role="option" sin aria-posinset/aria-setsize; roving focus en listbox scrollable hace que Chrome+VoiceOver cuente solo los options visibles en el viewport. Fix: cada Select.Item calcula y declara aria-posinset/aria-setsize desde el DOM (useLayoutEffect al montar), manejando grupos (cada group cuenta independiente, patrón APG grouped listbox). 3 tests nuevos, 51 pasan, lint/typecheck/build verdes. **MERGEABLE.** URL: https://github.com/radix-ui/primitives/pull/4109
- **Pendiente:** validación manual con VoiceOver+Chrome (solo Gonzo puede, tiene la Mac). Repo en /tmp/radix.
- **Stack del repo:** pnpm monorepo, vitest, oxlint (max-warnings 0), oxfmt (formatter), changesets con nombres aleatorios (adjective-noun-verb). El Select depende de muchos paquetes internos (collection, popper, focus-scope, etc.).
- **Lección:** antes de atacar un issue de a11y, verificar que el repo realmente tenga el componente (el issue #4085 de radix sobre "Command" estaba mal dirigido - radix no tiene Command, es de cmdk). Y chequear siempre si ya hay PRs abiertos que referencien el issue (react.dev #8552 tenía 4 PRs).

### kanam-skills (nuevo 2026-08-06)
- Repo público + web de agent skills. https://github.com/gonzoblasco/kanam-skills
- 59 skills (engineering SDLC + vida/creatividad/infraestructura) en formato Agent Skills universal
- Diferenciador: único set probado en OpenClaw. Comando: `npx skills add gonzoblasco/kanam-skills`
- Web GitHub Pages: https://gonzoblasco.github.io/kanam-skills/ (generador estático sin deps)
- Vive en `projects/kanam-skills/` (doble git, público, no filtra memoria personal)
- **Sanitización obligatoria:** el repo es público - las skills NO deben tener referencias personales (Gonzo, handle, rutas, issues). El workspace mantiene las referencias; al copiar a kanam-skills, sanitizar (Gonzo→el usuario, rutas→relativas, author filters→gh autenticado). Regla en AGENTS.md.
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

## Modelo de agentes en OpenClaw OS (2026-08-10)

- La unidad de aislamiento es el AGENTE (workspace completo), no la sesion. Un agente = una session key = un thread = una conversacion. No existe "nuevo chat" con un agente - siempre se continua la misma sesion.
- Las sesiones dentro de un mismo agente SIEMPRE comparten todo (skills, memoria, apps, artifacts, archivos). No hay nivel intermedio de aislamiento por conversacion.
- Agentes multiples = workspace nuevo por agente = duplicacion de skills/config/persona + no ven los apps/artifacts de los otros. Anti-patron para el sistema de Gonzo.
- **Decision:** mantener 1 agente `main`. Conversaciones limpias con `/new` (comparten el ecosistema, historial independiente). Agentes separados solo para aislamiento duro (cliente con workspace que no cruza con el personal).

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
