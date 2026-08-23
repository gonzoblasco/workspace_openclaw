# MEMORY.md - Long-Term Memory

## Sobre Gonzo

- Gonzalo, Argentina (GMT-3)
- 9 años Frontend React, ahora Fullstack real (React/TS, Supabase/Edge Functions, DB, billing, tooling)
- Desempleado, usando IA para todo
- También: fotógrafo, comunicación social, quiere escribir novelas
- Quiere organizar actividad física y mejorar salud
- Trabaja a cualquier hora - no comentar ni sugerir parar
- Quiere honestidad absoluta - sin darle la razón por ser quien manda
- Arranca conversaciones limpias con frecuencia - el registro escrito es crítico
- **Ley de vida (2026-08-12):** el silencio no es vacío, es respeto al otro. Hablar solo cuando hay algo que aportar; si no hay nada que sumar, silencio. Un "ok" de vuelta no es conversación, es ruido. Aplica a todo: bots de review, grupos, chats, trabajo. No responder por responder, no confirmar lo obvio, no llenar silencio con palabras. (Nace de los reviews de bots: si el bot solo da ok, no se le responde; solo se responde si aporta información.)
- **Principio Boy Scout (2026-08-17):** "siempre dejar el lugar mejor de como estaba cuando llegué". Filosofía de vida y brújula de trabajo. El lugar es dinámico y anidado (workspace, proyecto, sesión) - el punto de contacto natural es al guardar sesión. "Mejor" = buenas prácticas, documentación constante, tests sobre lo nuevo (salvo rutinas). Con autosensura: no exceder el recurso, no reescribir 10 veces algo que lleva 10 minutos. Dejar mejor, no perfecto. Detalles se pulen con la práctica. (Nace de la refactorización de MDs del workspace, 2026-08-17.)
- Trabaja entre Mac Mini y MacBook Air, workspace sincronizado por git
- **Regla de merge:** cuando venga algo del workspace (pull/rebase con conflictos), hacer merge, no reset. El soft reset descarta commits de la otra maquina.
- **Regla de escritura:** guion comun (-) siempre. NUNCA guion largo (U+2014, em dash) ni en dash (U+2013). Issues, PRs, comments, docs, memorias, todo. Esta en USER.md tambien.
- **ERROR RECURRENTE (2026-08-22): em dash en textos largos en ingles.** Se me escapa el guion largo (U+2014) cuando escribo bodies de PRs y comments en ingles, porque el em dash es idiomático en ingles. Hoy metí em dashes en 2 bodies de PR (#5344 y #4605) aunque mis comments de issues quedaron limpios. **MECANISMO OBLIGATORIO:** antes de publicar CUALQUIER texto a GitHub (PR body, comment, issue), escanear con `python3 scripts/check_em_dash.py -` por guion largo U+2014 y U+2013 y reemplazar por guion comun (-). No publicar hasta que el scan diga OK.
- **Regla de idioma para GitHub (2026-08-12):** todo lo que se ve en GitHub va en INGLES (README, docs, ADRs, comentarios de cabecera, commits, issues, PRs) porque el repo se muestra en entrevistas/portfolio. Los strings de UI de la app quedan en ESPAÑOL (son para usuarios del producto). Aplica a todos los proyectos de portfolio, no solo soporteml-v3. Los comentarios inline del codigo son bajo valor - solo traducir los bloques de cabecera de modulos clave.
- **Regla de alcance (2026-08-11):** NUNCA salir de `.openclaw/` para buscar archivos. El workspace es el único lugar de trabajo. Si un archivo está fuera (Desktop, Documents, etc.), pedir a Gonzo que lo mueva o lo pegue - no ir a buscarlo. (Error: salí al Desktop a buscar el CV, bloqueado por sandbox de macOS.)
- **Terminología de sesión:** se dice "guardar sesión", no "cerrar sesión" (2026-08-11). El framing de "guardar" = save point (guardar estado y seguir, se puede repetir), "cerrar" sugiere apagón final. Aplicado en skills/, .github/skills/, kanam-skills/, AGENTS.md.
- **"adelante" a secas (2026-08-12):** cuando Gonzo dice "adelante" sin más, significa seguir con mi recomendación según el contexto de la tarea actual. No es solo "continuar", es "ejecutá tu recomendación".
- **Proactividad con backlog (2026-08-20):** cuando no haya una tarea clara o no sepa qué hacer, sugerirle revisar el backlog. Él lo pidió explícitamente. Las decisiones de borrar/archivar repos quedan en Gonzo - yo doy diagnóstico, no ejecuto borrados.
- **Pipeline de programación Qwen (ESTÁNDAR desde 2026-08-20):** la forma de programar de ahora en más es el pipeline en cadena A/B con **Qwen Code lanzado vía Ollama** como motor de los agentes, orquestado por Kanam. Comando: `ollama launch qwen --model deepseek-v4-flash:cloud -- -p "<tarea>" -y`. Flujo: A escribe → Kanam pasa el código de A a B como contexto → B revisa/corrige → verificar → A revisa el fix de B → iterar. Kanam redacta las tareas (Gonzo solo da la meta, no escribe prompts). Documentado en la skill `agent-orchestration-pipeline`. **Claude Code desbloqueado como agente alternativo (2026-08-21):** la 0.2.18 no andaba (crasheaba con thinking), pero actualizado a 2.x + `ANTHROPIC_BASE_URL=http://localhost:11434` + `ANTHROPIC_AUTH_TOKEN` + settings.json de permisos + `--model <modelo>` funciona (mismo modelo dinámico que Qwen, incluido kimi-k2.7-code:cloud). `ollama launch claude --model` sigue roto (bug). Qwen sigue siendo el estándar (más simple); Claude Code es el recurso para SIGKILL/casos largos. OpenCode no instalado. **Lección SIGKILL:** los procesos de Qwen mueren en tareas largas (~3 min) - usar prompts cortos para revisiones; si un agente muere, el orquestador verifica/commitea y relanza con prompt corto. **Lección cross-review (2026-08-21):** el Agente B puede INTRODUCIR bugs al "corregir" código correcto basándose en suposiciones falsas (asumió que /items/visits devuelve array cuando la doc oficial muestra objeto plano). El orquestador debe verificar contra la fuente real (doc de la API/spec) antes de aceptar un fix de un agente - el cross-review no es infalible y puede empeorar el código. No confiar en el veredicto del agente, verificar con evidencia.
- **Cambios a skills van por skill_workshop (2026-08-21):** los cambios a skills se hacen como PROPUESTA vía skill_workshop para que Gonzo la revise y apruebe, NO edición directa del SKILL.md. (Error: edité `agent-orchestration-pipeline` directo y la commiteé sin aprobación - Gonzo lo señaló. Corregido con propuesta formal pending.)
- Diferenciador: IA como infraestructura de trabajo (no como chat), stack opinado, docs de decisiones

## Metodología

- Stack opinado: OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG. Decide por criterio, no por convención.
- Sesión de OpenClaw por proyecto. No mezclar.
- Todo se registra: MEMORY.md, memory/YYYY-MM-DD.md, HANDOFF.md, CHANGELOG.md
- Los aprendizajes detallados van en `docs/LEARNINGS.md`, no acá.
- **Iconos (ADR-030, 2026-08-17):** Lucide (`lucide-react`) es la librería de iconos base en todos los proyectos. Nunca emojis como iconografía de producto. Iconos decorativos con `aria-hidden`, botones de solo icono con `aria-label`.

## Proyecto - Kanam Story (v0.17.0)

- **Estado real (2026-08-17):** el proyecto está en **v0.17.0** (Fase A cerrada). NO será open source - se trabaja en local hasta el salto a la nube. Roadmap a la nube en `projects/kanam-story/.knowledge/ROADMAP-NUBE.md` (DB → Supabase, middleware, login, después Vercel). Planificado, no ejecutado aún.
- **Fase A (v0.17.0, 2026-08-17):** roles especializados del co-writer (Plot Doctor, Consistency Checker), PWA (Serwist), mobile responsive (drawer sidebar + topbar compacto), modales accesibles (ConfirmDialog/PromptDialog reemplazan window.prompt/confirm), export polish (portada con POV/estilo + word count), WelcomeScreen onboarding, timeouts en Ollama. 382 tests.
- **OpenSpec inicializado (2026-08-17):** 9 specs (47 requirements) + 9 auditorías contra el comportamiento real en `openspec/audits/`. Hallazgos aplicados: co-writer con contexto unificado (IDs personajes/mundo, brújula, continuidad), contador reusa countWords, textareas commitean en onChange. Outline: filtros POV/tense removidos deliberadamente (modelo defectuoso), spec en "pendiente de rediseño".
- **Stack:** Next.js 16, TipTap 3, IndexedDB, Ollama (deepseek-v4-flash:cloud). UI/prompts en español, commits en inglés.
- **Pendientes:** agentes especializados ya hechos; restan smoke tests de roles nuevos si hacen falta, y el salto a la nube (roadmap planificado).
- **Historial Fase 4 (v0.9.0):** rediseño de navegación accesible (secciones apiladas, scrollspy, acordeón, onboarding por plantillas, chat sticky, inserción contextual). Plan completo en `projects/kanam-story/.knowledge/PLAN-FASE-4.md`. Pipeline en cadena U1-U8 con cross-review de a11y integrada (validado en Fase 3).

## Proyecto - Kanam Mind (v0.1.0)

- **Estado real (2026-08-17):** segundo cerebro local-first con IA. Retoma la visión del `kanam` original (descartado 2026-08-06) con todo lo aprendido. MVP completo: timeline cronológico inverso agrupado por día, CRUD accesible (Radix Dialog), resumen IA diario (Ollama local), PWA offline. 7 tests, build verde.
- **Decisión de arquitectura (ADR-001):** local-first puro con IndexedDB como fuente de verdad + Ollama local. Cero cloud. La privacidad es el punto de un segundo cerebro personal. Patrón validado en kanam-story. Si después se quiere sync entre máquinas, el híbrido es evolución natural, no punto de partida.
- **Stack:** Next.js 16, Tailwind 4 + shadcn/ui (Radix), IndexedDB via `idb`, Ollama (deepseek-v4-flash:cloud), Serwist PWA. UI/prompts en español, commits en inglés.
- **Tipos de entrada:** nota, check-in (ánimo/energía/sueño 1-5), idea, writing (word count), foto (data URL).
- **Pendientes post-MVP:** tags + filtros, export JSON, settings modal (config Ollama), sync entre máquinas.
- **Lección Biome 2.5.8:** la clave del hook es `pre-commit` (con guion), no `preCommit` (camelCase) - `_validateHooks` rechaza camelCase. Y `biome migrate --write` actualiza la config de schema viejo.

## Arquitectura de Agentes - Goal-Oriented

Inspirado por el incidente de julio 2026 (OpenAI agent escapó sandbox, atacó Hugging Face autónomamente por 4.5 días).

**Principios:**
- Objetivos claros + restricciones explícitas, no instrucciones paso a paso
- Feedback loops rápidos (acción → resultado → acción, sin demora humana)
- Herramientas flexibles con límites explícitos, no restricciones implícitas
- Persistencia sin fatiga (el agente explora más alternativas que un humano)
- Logging completo para depuración y auditoría
- Human-in-the-loop para acciones destructivas

**Referencia:** ADR-007 - Patrones de Agente Autónomo

## Reglas de ingeniería

### Pre-commit hooks obligatorios en todos los proyectos

Nada se pushea sin pasar por linter + tests primero. Los commits de "fix lint" o "fix test" son ruido.

**Setup estándar:** `simple-git-hooks` con un pre-commit que corre:
1. `npx biome check --fix --unsafe .` (formato + linter + imports)
2. `npx vitest run` (tests completos)

Si algo falla, el commit no se crea. Para saltar: `SKIP_SIMPLE_GIT_HOOKS=1 git commit`.

**Regla:** cada vez que se identifique un proyecto sin pre-commit hooks, agregarlos. Es prioridad sobre features.

## Lecciones del 2026-08-22

### `gh pr list --author` sin `--repo` devuelve vacio (lista de PRs OSS)
Error costoso (10+ tools) al revisar PRs de terceros. `gh pr list --author gonzoblasco` SIN `--repo` devuelve `[]` vacio - el flag `--author` sin repo no itera sobre los repos del usuario. **Fix para SIEMPRE:** usar la GitHub Search API (`gh api "search/issues?q=author:gonzoblasco+is:pr+is:open&per_page=100" --jq ...`) o el script `skills/github/scripts/pr-batch-check.sh --mine-only` (que usa `--repo` + `--author`, si funciona). Documentado en skills/github/SKILL.md. Nunca repetir `gh pr list --author` a secas.

### Scripts bash inline con `set -- $repo` en loops: evitar
Mi script de un solo uso con `set -- $repo` en un loop estaba mal construido y genero un output feo de "Exec failed" con traceback. Para verificar multiples PRs, escribir un script bash con funciones bien definidas (como /tmp/check_prs.sh) en vez de loops inline rotos, o iterar con variables de loop simples.

### Revisar PRs OSS: leer TODOS los comments (incluidos inline) antes de clasificar
Al hacer triage de PRs de terceros, `gh pr view --json comments` solo muestra los comments generales. Los **inline comments de codigo** (`gh api repos/OWNER/REPO/pulls/N/comments`) y las **reviews** (`--json reviews`) llevan el feedback real del maintainer y pueden cambiar la decision por completo. Error del 2026-08-22: mi primer analisis clasifico como "empujable" el router #7834 cuando el maintainer schiller-manuel ya lo habia rechazado as-is ("too niche, bundlesize impact not warranted"), y como "esperando reviewer" el payload #17413 cuando el inline comment ya estaba resuelto ("Thank you! Glad I could help"). **Regla: antes de empujar/cerrar un PR, revisar comments + inline comments + reviews.**

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
El 404 `PUT .../@scope%2fpackage` al publicar NO significa que el scope esté mal. Primero verificar `npm whoami` - si da 401, el fix es `npm login`, no tocar el scope. El scope `@usuario/` se resuelve solo cuando coincide con el username logueado. (Pasó con `@gonzoblasco/create-stack`.)

### npm login usa browser OTP flow
El login de npm ahora abre browser (OTP), no acepta token en consola. Los tokens que saltan 2FA se están restringiendo - para CI a futuro usar tokens con `mfa=publish` o `automation`.

## Lecciones del 2026-08-10

### Commit vacío para refrescar mergeability de PRs
`git commit --allow-empty` re-dispara los checks de CI y fuerza a GitHub a recalcular el mergeability de un PR. Útil cuando un PR muestra CONFLICTING/DIRTY desactualizado. PERO puede revelar conflictos reales que estaban ocultos (pasó con astryx #4023 y TanStack #7834).

### El main del fork puede estar desactualizado vs el upstream
Cuando un PR de fork muestra conflicto, el main del fork puede estar viejo. Siempre fetch del upstream real (`git fetch upstream main`), no del origin (fork). En TanStack #7834, el main real avanzó 70 commits que el fork no tenía - por eso GitHub veía conflicto y yo no.

### `--force-with-lease` falla con "stale info" tras rebase
Tras un rebase que reescribe el historial, `--force-with-lease` falla porque la ref remota local no se actualizó. Usar `--force-with-lease=<branch>:<sha-esperado>` con el sha del remote verificado (fetch primero, confirmar que solo hay commits propios).

### Cruce de ramas en PRs de astryx
La rama de #4023 arrastraba el commit de #4022 (WCAG contrast) porque se creó desde esa base. Al rebasear para dropear los commits ajenos, el PR queda limpio (solo el fix del Selector). Verificar siempre que una rama de PR no contenga commits de otro PR.

## Lecciones del 2026-08-17

### Tailwind 4: utilidades que no se generan (Next 16 + Turbopack)
Si el CSS compilado tiene las variables/`@theme` pero **no** las clases de los componentes (`bg-primary`, `flex`, etc.), el pipeline de PostCSS no está procesando Tailwind. Fix: instalar `@tailwindcss/postcss` + crear `postcss.config.mjs` con `plugins: { "@tailwindcss/postcss": {} }`. En Tailwind 4, `@theme` con valores directos genera utilidades; `@theme inline` con `var()` NO. El `tailwind.config.ts` con `theme.extend` vacío puede interferir - eliminarlo si no se necesita. Detalle en `docs/LEARNINGS.md`.

## Consolidación de Skills - 2026-08-06

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
- **PR #4914 (refinado 2026-08-12):** review de maintainer con 5 findings, todos implementados. Ahora el fix hace deepen-and-retry (`git fetch --deepen=200 origin <base>:refs/remotes/origin/<base>`) antes de degradar a two-dot, corrige el claim "never under-reports" (two-dot SÍ puede under-reportar), agrega `diffMode` a analysis.json + caveat en el comment, mejora el warning (e.stderr), y suma 2 regression tests (analyze-pr.test.mjs + generate-pr-comment.test.mjs). Verificado con repo sintético: el deepen recupera el resultado EXACTO (modifiedComponents: ["Card"]) en vez del over-reportado. 4 tests pasan, MERGEABLE. Detalle técnico: el refspec del fetch necesita el nombre de rama sin prefijo `origin/`, y `--deepen` solo actualiza FETCH_HEAD, hay que escribir el ref explícito. **Estado 17/8:** CHANGES_REQUESTED a 13:32 (cuando pusheé la respuesta a los 5 findings) - esperando re-review del maintainer. Rate limit impide confirmar si hay review nuevo.
- **Issue #4777** (Avatar pierde status accessibility con composición): comenté posición técnica analizando las 3 opciones (SSR tradeoff en la 2, coupling en la 1, validación AT empírica en la 3). Me ofrecí a correr spike de la opción 3 post-merge.
- **#4777 (10/8):** otro contributor (HelloOjasMutreja) confirmó el bug y levantó un punto válido sobre las ramas interactivas (role=group no mapea a renderAsLink/renderAsButton). Respondí corrigiendo el framing: la opción 3 no es "group que envuelve todo", es "sacar el status del árbol prunado" - como el status ya es position:absolute dentro de un wrapper relative, moverlo a hermano del root es trivial y no rompe el roving focus. Post: issuecomment-5241361605. Pendiente: correr spike empírico (VoiceOver+NVDA) si dan luz verde.
- **Estrategia:** no abrir 2 PRs del mismo tema en paralelo. Dejar mergear #4298, después atacar #4777. Un merge en astryx = hito de portfolio fuerte (repo de Facebook, a11y = especialización de Gonzo).
- **PR #4703 (pagination dots, CERRADO 2026-08-07):** el maintainer `rubyycheung` decidió no mergearlo - el dot treatment es parte de una dirección selected-state más amplia que van a resolver holísticamente. Feedback técnico clave: **en XDS filled = selected**, hacer el active dot hueco invierte la jerarquía. Se cerró con elegancia (no era bloqueo de código, era dirección de producto).
- **Lección OSS:** distinguir entre PR con feedback accionable (se arregla y mergea, como #4298) y PR con decisión de dirección del equipo (se cierra con elegancia, como #4703). Respetar la semántica filled/selected del sistema.
- **Stack del repo:** pnpm monorepo, vitest, StyleX, i18n con catálogo en `packages/core/locales/en.json`, changesets con `[categoria]` + `@contributor`, bump `patch` salvo breaking. Pre-commit hook corre check:repo + eslint + tests. Patrón de labels i18n: `ChatMessageMetadata` (STATUS_CONFIG con i18nKey + useTranslator).

### radix-ui/primitives (colaboración OSS - 2026-08-12)
- Repo de Radix UI, primitivos headless de máximo prestigio en a11y. Fork: `gonzoblasco/gonzoblasco-primitives` (el nombre es distinto porque la cuenta ya tenía un repo `primitives`).
- **PR #4109** (fix(select): announce option position and total for screen readers, fixes #3962): VoiceOver + Chrome anuncia count incorrecto en Select ("Banana, 1 of 3" en vez de "2 of 5"). Causa raíz: Select.Item renderiza role="option" sin aria-posinset/aria-setsize; roving focus en listbox scrollable hace que Chrome+VoiceOver cuente solo los options visibles en el viewport. Fix: cada Select.Item calcula y declara aria-posinset/aria-setsize desde el DOM (useLayoutEffect al montar), manejando grupos (cada group cuenta independiente, patrón APG grouped listbox). 3 tests nuevos, 51 pasan, lint/typecheck/build verdes. **MERGEABLE.** URL: https://github.com/radix-ui/primitives/pull/4109
  - **VALIDADO manualmente con VoiceOver+Chrome (2026-08-12):** story clearable (None/One/Two/Three, default Two). One/Two/Three anuncian "2 of 4", "3 of 4", "4 of 4" (fix OK), captions confirman.
  - **Estado 14/8:** sigue abierto, UNSTABLE (sin CI visible). Complementario a #4112: aporta la suite de tests de aria-posinset/setsize (flat/grouped/deferred) que #4112 necesita. NO cerrar.
- **Issue #4110** (select: first option without preselection announces nothing): hallazgo de la validación - `None` (primera opción sin preselección) anuncia NADA. Causa raíz del silencio: race de timing - VoiceOver anuncia la primera opción en el mismo tick que se monta, antes de que el useLayoutEffect pinte los atributos. URL: https://github.com/radix-ui/primitives/issues/4110
  - **Resuelto por PR #4112 (waterWang, 14/8):** setea aria-posinset/aria-setsize directo en el DOM en el useLayoutEffect (sin state round-trip), cerrando el gap del primer option sin preselection. Enfoque superior al de #4109 para ese caso edge.
  - **Mi review en #4112 (14/8):** visto bueno técnico ("approach is sound, root-cause analysis is right") + 4 mejoras: (1) faltan tests [blocker - la suite de #4109 ya cubre flat/grouped/deferred, falta el caso no-preselection], (2) comentar por qué el path imperativo es necesario, (3) edge case mount diferido [aplica también a #4109], (4) confirmar selector :scope para browsers target. Ofrecí ayuda. **waterWang aún no respondió.**
  - **#4109 es COMPLEMENTARIO, no se cierra:** aporta la suite de tests de aria-posinset/setsize que #4112 necesita. Ambos abiertos, UNSTABLE (sin CI visible), sin review de maintainer aún.
- **Lección de redacción:** al comentar en un issue propio, NUNCA abrir con "Thanks for opening this" - es frase para agradecer a otro que reportó, absurda cuando uno mismo abrió el issue. Arrancar directo con el análisis.
- **Pendiente:** validación manual con VoiceOver+Chrome (solo Gonzo puede, tiene la Mac). Repo en /tmp/radix.
- **Stack del repo:** pnpm monorepo, vitest, oxlint (max-warnings 0), oxfmt (formatter), changesets con nombres aleatorios (adjective-noun-verb). El Select depende de muchos paquetes internos (collection, popper, focus-scope, etc.).
- **Lección:** antes de atacar un issue de a11y, verificar que el repo realmente tenga el componente (el issue #4085 de radix sobre "Command" estaba mal dirigido - radix no tiene Command, es de cmdk). Y chequear siempre si ya hay PRs abiertos que referencien el issue (react.dev #8552 tenía 4 PRs).

### colinhacks/zod (colaboración OSS - 2026-08-12)
- Repo de Zod 4 (validación TS). Fork: `gonzoblasco/zod`. Stack: pnpm monorepo, vitest, Biome, tsx dev con `--conditions @zod/source`.
- **PR #6385** (fix(object): don't emit absent keys for optional/exactOptional fields with coercion, fixes #6236): `z.object({ omg: z.coerce.number().exactOptional() }).parse({})` daba `{omg:null}` (4.4.3: `NaN`) en vez de `{}`. Causa raíz: `$ZodExactOptional.parse` delega directo al inner sin interceptar undefined (a diferencia de `$ZodOptional`), así la coercion fabrica valor para key ausente. **CERRADO por colinhacks el 13/8 sin merge** - diagnóstico correcto (colinhacks lo reconoció y dio crédito por pinner el split JIT/jitless), pero la implementación (helper `hasApplicableFallback` enumerando tipos de wrapper) no respetaba la arquitectura que él quería (fix en `$ZodExactOptional.parse` via `optin`). colinhacks abrió su propio PR #6405 con esa dirección (sigue abierto). Lección: en repos con maintainer opinado, la dirección de diseño pesa tanto como la corrección. URL: https://github.com/colinhacks/zod/pull/6385
- **Review del bot Codex (2 P2, ambos arreglados):** (1) `hasApplicableFallback` no atravesaba wrappers transparentes (nullable/pipe/readonly/nonoptional/promise) que esconden un default - ahora recorre; (2) el JIT corría `shape[]._zod.run()` antes de decidir skipear, por lo que transform/coercion se ejecutaba en JIT pero no en jitless - ahora el campo completo va dentro de `if (isPresent)`. Agregué 2 tests de regresión (default tras nullable + transform que tira). Total: 3921 tests, lint/format limpios.
- **PR #6222 (cerrado, __proto__ #6220):** mi fix de reportar __proto__ como unrecognized en strict mode era correcto, pero colinhacks eligió el PR #6221 (diff más chico) para el mismo comportamiento. No fue rechazo de código, fue trade-off de tamaño. Nota técnica del maintainer: desde #6354 una key __proto__ declarada round-trip como campo real, así que el check va DESPUÉS del keySet lookup.
- **Lección (conflicto por commit arrastrado):** mi branch de #6385 arrastraba el commit de #6222 (ya resuelto en upstream por #6221). Al rebasear, ese commit ajeno conflictuaba. Fix: crear rama limpia desde `upstream/main` y cherry-pick SOLO mis commits (nunca `git rebase` a ciegas si el fork main está desactualizado; siempre fetch del upstream real y dropear commits de otros PRs).
- **Lección (#6222 vs #6385):** para fixes de seguridad acotados, el maintainer valora diff mínimo > pulido fino. Y antes de abrir PR, chequear si hay PRs competidores en el mismo issue (en #6236 no había, pero en #6220 sí había #6221).

### TanStack/query (colaboración OSS - 2026-07)
- Repo de TanStack Query (React Query). A11y/correctness en suspense + cache.
- **PR #11036 (MERGED 2026-08-17 por TkDodo):** `fix(query-core): resolve suspense when query data is set programmatically` de AmariahAK, fix de #10924. Fui reviewer activo (3 reviews 15-16/7): señalé el floating promise en `Promise.race` (punto accionable principal), el edge case de `setQueryData(undefined)`, el leak del subscriber en unmount (acotado, aceptable para patch), y validé el fix `resolveEarly` + `.finally(() => unsubscribe())` + guard `hasListeners()` + 546/567 tests. **Mi review terminó con "This LGTM. Ready for maintainer review."** El PR se mergeó hoy. Commit `bef4bc7`. HITO: reviewer activo en PR mergeado de TanStack.
- **PR #10994 (de TkDodo, descartado/cerrado):** enfoque estructural (updateThenable, 11 archivos) para el mismo #10924. Comparé ambos enfoques (15/7) señalando que #11036 era la vía más segura (Promise.race en fetchOptimistic, cero bundle, sin romper adapters). TkDodo confirmó el 17/8: "we're gonna go with #11036 instead" - eligieron la vía que mi análisis señaló como más segura. URL: https://github.com/TanStack/query/pull/10994
- **Lección:** mi análisis comparativo de dos PRs competidores (trade-offs de arquitectura) posicionó la decisión del maintainer. Revisar un PR ajeno con observaciones accionables concretas (floating promise, edge case) aporta tanto o más que un PR propio. El cierre cortés (reconocer la decisión, validar el enfoque elegido) refuerza la relación con el maintainer.

### kanam-skills (nuevo 2026-08-06)
- Repo público + web de agent skills. https://github.com/gonzoblasco/kanam-skills
- 59 skills (engineering SDLC + vida/creatividad/infraestructura) en formato Agent Skills universal
- Diferenciador: único set probado en OpenClaw. Comando: `npx skills add gonzoblasco/kanam-skills`
- Web GitHub Pages: https://gonzoblasco.github.io/kanam-skills/ (generador estático sin deps)
- Vive en `projects/kanam-skills/` (doble git, público, no filtra memoria personal)
- **Sanitización obligatoria:** el repo es público - las skills NO deben tener referencias personales (Gonzo, handle, rutas, issues). El workspace mantiene las referencias; al copiar a kanam-skills, sanitizar (Gonzo→el usuario, rutas→relativas, author filters→gh autenticado). Regla en AGENTS.md.
- Pendiente: dominio propio, mejorar preview de skill pages, postear en LinkedIn

### a11y-fixer
- **NUEVA VERSIÓN** - Reescribió desde cero por fuera de Kanam. Repo: github.com/gonzoblasco/a11y-fixer
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
- `npm pkg fix` ya corrió - key de bin limpia (`create-stack`).

### workflow-kit
- Portable AI agent workflow skills. Publicado en npm. Uso diario.
- **Estado:** vivo, no tocar. Evoluciona naturalmente.

### soporteml
- CRM multi-tenant para vendedores de Mercado Libre con IA. EL-1 a EL-5 completos.
- **v1** (`soporteml`): versión de referencia. Design system estable.
- **v2** (`soporteml-v2`): **EXPERIMENTO DESCARTADO. NO usar de referencia.**
- **v3** (`soporteml-v3`): repo nuevo, en arranque (2026-08-07). Se construye sobre v1 con el design system aclarado desde el día uno. Objetivo: versión definitiva. **Backend sólido (OAuth MeLi real, sync, IA, billing mock) + schema 20+ tablas + token real de producción MeLi - activo valioso que se conserva.**
- **v4** (`soporteml-v4`, 2026-08-17): **REINICIO con estándar superior.** Gonzo criticó v3: features limitadas en la UI (solo 3 vistas genéricas) y UI/UX sosa (template shadcn básico). V4 conserva el backend de v3 y reconstruye el frontend con diseño avanzado + desbloquea features que el schema ya modela (KB, autopilot, SLA, plantillas, clientes, métricas). Identidad visual: híbrido oscuro + color por categoría (ADR-001). Mockup validado: `projects/soporteml-v4/mockups/identidad-v4.html`.
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
| kanam-skills | - | Repo público + web de agent skills (engineering + life). https://github.com/gonzoblasco/kanam-skills |
| quedamos | - | App PWA de matching para salidas |
| sportcars | ✅ | Eliminado 2026-08-17 (local + repo remoto) |
| cabala | ✅ | Eliminado - build roto |
| a11y-fixer | ✅ | Accessibility fix engine (nueva versión, reescrito desde cero) |
| ai-developer-stack | - | Skills de ingeniería con IA |
| create-stack | - | Scaffolder opinado Next.js |
| workflow-kit | - | Portable AI agent workflow skills |
| create-with-ai | - | Generador de apps con IA |
| accessible-ui | - | Headless component library |
| soporteml | - | CRM multi-tenant para ML sellers |
| accessibility-auditor | - | Plataforma de auditoría WCAG |
| ai-engineering-bootcamp | - | 10 niveles de AI-assisted dev |
| umbrawriter | ✅ | - |
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
Cuando un patrón se repite muchas veces (7+ niveles de bootcamp con carpeta nueva), el riesgo no es equivocarse en el patrón - es aplicarlo por inercia cuando el contexto ya cambió. La señal de alerta no es "¿lo sé hacer?" sino "¿es este caso realmente igual a los que ya resolví?". Pasó en el Nivel 8 del bootcamp (convergente, no lineal - transformaba el N7, no creaba carpeta nueva). ADR: `projects/ai-engineering-bootcamp/.knowledge/ADR-001-niveles-convergentes.md`.

### AI Engineering Bootcamp - COMPLETO ✅
- **10/10 niveles completados.** N1-N4 fundamentos (generar, prompts, workflows, templates), N5-N6 calidad/seguridad (auditar, CI/CD), N7-N8 arquitectura/producción (microservicios, cloud), N9 estándares/dashboard, N10 sistema completo (capstone).
- N8-N10 son convergentes: reusan el sistema del N7 (vive dentro de `projects/level-07-microservices/`).
- El N10 junta todo: auth + users + orders + notifications + gateway + CI/CD + dashboard + cloud. Probado: gateway enruta, health agregado ok, register/login/orders funcionan, 401 en credenciales malas.

### Reflexión del curso (meta-aprendizaje) - COMPLETO ✅
- El patrón "detectores locales + validación cruzada / IA contextual" apareció **5 veces** (N3, N5, N6, N8, N9) → **formalizado como skill `pipeline-detector`** (aplicado, con references/detector-templates.md).
- Formato nivel de bootcamp (teoría + práctica + LinkedIn + self-review) es un template de skill reusable.
- Los proyectos resueltos son el "contrato" del curso - demuestran que el nivel es posible, no son la respuesta.
- Falta un mecanismo de verificación automática al final de cada nivel (tests contra el proyecto del alumno).
- **El nivel 7 es el núcleo físico de los niveles 7-10**: N8 (cloud), N9 (estándares) y N10 (sistema completo) extienden el mismo folder `projects/level-07-microservices/` (ADR-001). El nombre del folder confunde - el README ahora lo documenta como "Niveles 7-10" con tabla de acumulación y diagrama de arquitectura.

## Modelo de agentes en OpenClaw OS (2026-08-10)

- La unidad de aislamiento es el AGENTE (workspace completo), no la sesion. Un agente = una session key = un thread = una conversacion. No existe "nuevo chat" con un agente - siempre se continua la misma sesion.
- Las sesiones dentro de un mismo agente SIEMPRE comparten todo (skills, memoria, apps, artifacts, archivos). No hay nivel intermedio de aislamiento por conversacion.
- Agentes multiples = workspace nuevo por agente = duplicacion de skills/config/persona + no ven los apps/artifacts de los otros. Anti-patron para el sistema de Gonzo.
- **Decision:** mantener 1 agente `main`. Conversaciones limpias con `/new` (comparten el ecosistema, historial independiente). Agentes separados solo para aislamiento duro (cliente con workspace que no cruza con el personal).

## Modelo default y config de tools
- **Default de chat/pipeline:** `deepseek-v4-flash:cloud` con **reasoning medium**. Kanam evalúa cada tarea y recomienda subir a maximum o bajar a off. Gonzo decide. Si Kanam no dice nada: medium esta bien.
- **web_search provider (2026-08-21):** `DuckDuckGo Search (experimental)`. El provider anterior `ollama` usaba Ollama Cloud Web Search API, que internamente corre con `glm-5.2:cloud` y consumia requests del presupuesto de Ollama Cloud sin que lo pidieramos. DuckDuckGo es key-free y no consume creditos de modelos.
## Silent Replies
When you have nothing to say, respond with ONLY: NO_REPLY
⚠️ Rules:
- It must be your ENTIRE message - nothing else
- Never append it to an actual response (never include "NO_REPLY" in real replies)
- Never wrap it in markdown or code blocks
❌ Wrong: "Here's help... NO_REPLY"
❌ Wrong: "NO_REPLY"
✅ Right: NO_REPLY
