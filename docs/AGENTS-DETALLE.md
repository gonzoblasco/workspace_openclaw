# AGENTS.md - Detalle de Referencia

> Este archivo contiene el detalle operativo completo que se movió de AGENTS.md para mantenerlo bajo el límite de inyección de contexto (20K chars). AGENTS.md tiene las reglas esenciales; acá está el detalle ampliado. Si AGENTS.md referencia este archivo, consultarlo cuando se necesite el detalle.

## Reglas de feedback en PRs/issues ajenos (detalle ampliado)

Reglas duras de Gonzo para publicar feedback/review en repos de terceros. Corregidas 24/08 - no repetirlas.

1. **Leer SIEMPRE toda la vida del ticket ANTES de comentar o hacer nada.** Y ANTES DE ESO, chequear contexto interno: `memory_search()` + `sessions_search()` por el numero de issue - si ya participamos, contextualizar con nuestro rol (lecciones carbon #16031, 2026-09-09/10). Body, reviews, TODOS los comments (incluidos los de autores/maintainers posteriores al review), inline comments, estado actual. El contexto que Gonzo comparte es el punto de partida, nunca el hilo completo: leer siempre body + todos los comments e interacciones antes de responder. Si no tengo el repo clonado y el claim depende del código base, plantear como pregunta/"worth checking" honesto, NO como afirmación. Opción: clonar el repo en `forks/` para poder verificar.
2. **El autor del PR/issue define, no el invitado.**** Para saber con quién se habla, basta con ver quién creó el PR/issue (el autor). No cerrar con elogios/"nice work"/adulación hacia el autor - el invitado no valida el trabajo ajeno; eso es ruido. El reconocimiento va implícito en la interacción.
3. **No subir un comentario solo para disculparse por otro.** Disculparse no está mal, pero subir un comentario nuevo únicamente para pedir disculpas por uno anterior malo genera ruido. Lo correcto: si un comentario salió mal (desactualizado, mal contexto, error), BORRARLO y volver a generarlo correcto - sin comentario de disculpa adicional.
4. **Nunca repetir lo que ya se dijo en el hilo** ni repetir mis propios comentarios. Siempre aportar algo nuevo que ayude, sin huevadas.
5. **NO exponer notas internas/borradores en el hilo público.** El archivo de borrador (con encabezado "Borrador", "Notas para Gonzo", análisis interno) es SOLO para revisión de Gonzo - NUNCA publicarlo directo. Al publicar, usar SOLO el texto del comentario final limpio (sin encabezado de borrador ni notas internas). (Error real en #5204 y #4611: publiqué el archivo con notas internas; se borró y se republicó limpio.)
6. **Siempre dar la URL** del PR/issue al reportar trabajo hecho.
7. **No agradecer a bots de review.** Cuando el review/comentario de un PR es de una IA (ej: Enough1122 en hermes-agent, "AI code review - automated review for reference"), NO ponerle "Thanks for the review" - solo se agradece a humanos. Los reviews de IA con puntos accionables se responden directo a la sustancia con evidencia (qué se arregló, cómo se verificó), sin saludo. (Corrección de Gonzo en hermes-agent #93848.)
8. **Atribución por login, nunca por contexto (2026-09-22).** La autoría de cada review/comentario del hilo se verifica por el `user.login` en la API - NUNCA se infiere de la cercanía temporal, del contexto de otra sesión ni de que esa persona haya revisado PRs nuestros antes. Error real en astryx #4690: el CHANGES_REQUESTED de `humbertovirtudes` (maintainer que revisó #4157 y quedaba pendiente en #4298, ambos nuestros) fue reportado a Gonzo como si fuera suyo, por proximidad de contexto. Regla dura: "nuestro" = login `gonzoblasco` verificado en la fuente; toda otra cuenta es tercero, INCLUIDOS maintainers que revisan nuestro trabajo en ese repo. Verificación mecánica: `scripts/pr-thread-brief.sh <owner/repo> <n> [login]` clasifica cada evento del hilo OURS/BOT/THIRD, resume por actor y nombra el último acto no-bot (quién tiene la pelota). Corolario: nunca narrar un acto del hilo como "vos/nuestro/nos pidieron" sin ese chequeo o su equivalente API.

**Regla de contexto:** los borradores de feedback se guardan en `docs/feedback/<repo>-<numero>-draft.md` para revisión de Gonzo. El archivo de borrador y el texto a publicar son cosas DISTINTAS - al publicar, nunca usar el archivo de borrador directo; extraer solo el texto final del comentario.

## Pausa obligatoria: agentes iteran -> revision final -> push -> redactar borrador (detalle ampliado)

Flujo completo al trabajar en un PR propio con el pipeline de agentes (Kanam en MAX, agentes en HIGH):

1. **Kanam** analiza, planifica y redacta el prompt (MAX).
2. **Agente A** hace los cambios (HIGH).
3. **Agente B** revisa los cambios del Agente A (HIGH).
4. **Si hay mas cambios:** repetir pasos 2 y 3, **alternando el orden** de los agentes (si A escribio y B reviso, en la siguiente ronda B escribe y A revisa, y asi).
5. **Revision final:** Kanam analiza TODO el trabajo ya iterado por A y B como una unidad (el PR completo, no piezas sueltas), desde OpenClaw, en MAX (nivel fijo de Kanam - no hay pausa de cambio de nivel).
6. **Push** (solo despues de la revision final aprobada).
7. **Redactar el borrador** del PR/feedback.

El cross-review del Agente B (paso 3) es parte de la cadena de escritura (HIGH, ojos frescos de otro agente). La revision final de Kanam en MAX (paso 5) es la SEGUNDA revision, despues de que los agentes terminaron de iterar, y analiza el conjunto completo - es la oportunidad mas valiosa de MAX: atrapar errores de TU PR antes de que los vea un reviewer.

**La pausa es agnostica a como se escribio el codigo.** Da igual si el codigo lo escribe Kanam, Gonzo, o el pipeline A/B de agentes (Qwen/Claude Code via `ollama launch qwen` / ANTHROPIC_BASE_URL). Todo eso termina en los commits del PR, y ahi viene la pausa, la revision final de Kanam en MAX analizando el conjunto, el push, y el borrador del PR.

Referencia completa de la tabla MAX vs HIGH: `docs/adr/ADR-040-modelos-seleccion-por-tarea.md` (seccion "Guia rapida: cuando MAX vs HIGH").

## Skills Públicas - Sanitización (detalle ampliado)

El repo `kanam-skills` (github.com/gonzoblasco/kanam-skills) es **público**. Las skills que van ahí NO deben contener referencias personales de Gonzo (nombre, handle `gonzoblasco`, repos, rutas `/Users/gonzoblasco/`, issues específicos).

**Dos versiones de cada skill:**
- **Workspace** (`skills/` + mirror `.github/skills/`): privado, **mantiene** las referencias personales - son el setup de Gonzo y el contexto es valioso.
- **kanam-skills** (`projects/kanam-skills/skills/`): público, **sanitizado** - se escribe como si la usara un extraño.

**Regla obligatoria:** al copiar una skill del workspace al repo público, sanitizar en el camino:
- `Gonzo` / `Gonzalo` → `el usuario` (con artículos correctos: al/del usuario)
- `@gonzoblasco` → `@usuario`
- Author filters en scripts → `$(gh api user --jq '.login')` (username del gh autenticado)
- Rutas `/Users/gonzoblasco/...` → relativas
- Repos `github.com/gonzoblasco/...` → `github.com/<usuario>/...`
- Issues específicos (ej. `astryx #4777`) → enseñanza genérica sin la referencia

**Regla ampliada (Gonzo, 2026-09-14): contenido genérico, no solo sin nombres.** El material publicado NO debe mencionar nuestro trabajo ni nuestras identidades en ninguna forma. No alcanza con reemplazar `Gonzo` -> `el usuario`: hay que sacar toda referencia a nuestros proyectos, repos, herramientas y flujos particulares (ej. `a11y-fixer`, proyectos `kanam-*` internos, `workspace_openclaw`, issues específicos, rutas locales, nombres de modelos del setup). El contenido se escribe como **plantilla genérica que sirve para cualquier proyecto**, no como la receta de nuestro setup con los nombres cambiados.

**La marca Kanam SÍ se queda (corregido por Gonzo, 2026-09-14).** `Kanam` es el **nombre del producto** que se publica, no una identidad personal. Distinción clave:
- **Se queda:** `Kanam` como nombre/marca del producto y de sus skills (ej. `author: Kanam` en frontmatter, "Kanam, consolidá la memoria" como ejemplo de invocación del agente, `kanam-skills` como nombre del repo).
- **Sale:** datos personales (`Gonzo`, `Gonzalo`, `gonzoblasco`, `@gonzoblasco`, `/Users/gonzoblasco/`) y **proyectos internos** que no son parte del producto publicado (ej. `a11y-fixer`, `kanam-lab`, `soporteml`, `workspace_openclaw`, issues propios).

El error a evitar: tratar la marca como si fuera un dato personal. `Kanam` nombra lo que publicamos; `Gonzo` nombra a quién se lo publicamos.

**Verificación obligatoria (dos pasadas):**
1. Referencias personales: `grep -rn "gonzoblasco\|Gonzalo\|Gonzo\|@gonzoblasco" skills/ | grep -v __pycache__` debe dar vacío.
2. Referencias a proyectos internos: `grep -rn -E "a11y-fixer|workspace_openclaw|soporteml|/Users/" skills/ | grep -v __pycache__` debe dar vacío. (`Kanam` NO entra en este grep - es la marca.)

**Puntos de fuga tipicos (auditados 2026-09-14):** ejemplos que citan un proyecto interno propio; rutas locales; el handle personal en scripts (author filters -> `$(gh api user --jq '.login')`).

**Excepción legítima:** las referencias a `gonzoblasco/kanam-skills` en README, docs y web/generate.js (identidad de instalación del repo) y el LICENSE (copyright legal) se mantienen.

## Estructura de Proyectos - Triple Git (detalle ampliado)

**Filosofía:** cada proyecto tiene su carpeta en `projects/<slug>/`, y el cruce de repos se resuelve en TRES capas git que conviven:

```
workspace/                    (repo: workspace_openclaw)
└── projects/                 (repo agregado: projects_openclaw, PRIVADO - archivo de todo el código)
    └── <slug>/               (repo individual del proyecto: gonzoblasco/<slug>)
        ├── .knowledge/       # memoria institucional (BRIEF, ADRs, STATUS, HANDOFF) - SOLO workspace
        ├── src/              # código fuente (trackea el repo individual)
        └── .gitignore        # del proyecto (lo respetan el agregado y el workspace)
```

**Capas y responsabilidades:**
- **Workspace git** (`workspace_openclaw`): trackea `projects/**/.knowledge/` (la memoria: el qué y por qué). Ignora el resto de `projects/`.
- **Repo agregado** (`projects_openclaw`): trackea el código fuente de los 20 proyectos como archivos planos (sin `.git/`, sin node_modules/.env/*.db). Es el archivo "ver todo junto", NO la fuente de la verdad para trabajar. Su `.gitignore` raíz tiene `*/.git/` para que git descienda al contenido en vez de crear gitlinks, y `PROYECTOS.md` + `.gitignore-template` (son del workspace).
- **Repo individual** (`gonzoblasco/<slug>`): la fuente de la verdad del código. Ahí viven commits, branches, PRs, push. Cada uno con su propio `.gitignore`.

**Reglas clave:**
- **Los `.git/` de los subrepos se ignoran** en el agregado (`*/.git/`) y en el workspace (`/projects/*/.git/`). Ese es el truco que evita los gitlinks: git desciende al contenido cuando el `.git/` está ignorado.
- **NUNCA committear los `.git/` de los subrepos** en el agregado (rompería todo: gitlos vería como repos embebidos/gitlinks).
- **La fuente de la verdad para trabajar es el repo individual.** El agregado se mantiene al día con `scripts/aggregate-sync.sh` (no es automático: un cambio en `<slug>/` es visible para ambos repos; hay que commitear en cada uno).
- **OJO con `git reset --hard` en `projects/`:** como los `.gitignore` de varios proyectos excluyen su `.knowledge/` (doble-git correcto), el reset borra esos `.knowledge/` del disco. Restaurar con `git restore --worktree -- projects/` desde el workspace (la memoria está commiteada ahí).

**Flujo típico:**
1. Nuevo producto → `./scripts/init-project.sh <slug>`
   - Crea `projects/<slug>/.knowledge/` con BRIEF.md + STATUS.md
   - Crea repo privado en gh, inicializa el git del proyecto (excluye `.knowledge/` vía `.git/info/exclude`) y pushea
   - Commitea `.knowledge/` al workspace
   - Registra el proyecto en el repo agregado (commit inicial de la carpeta)
2. Go decision → scaffold en `projects/<slug>/` (repo individual, ignora `.knowledge/`)
3. Desarrollo → actualizar `projects/<slug>/.knowledge/STATUS.md` con cada hito (commit al workspace)
4. Commits: `.knowledge/` al workspace, código al repo del proyecto, cambios del archivo al agregado (`aggregate-sync.sh`)

**Sin submódulos.** Los proyectos se clonan en `projects/<slug>/` bajo demanda (cuando se trabajan), no como submódulos. Si una carpeta de `projects/` no tiene repo en GitHub, se elimina.

**Excepciones:**
- Forks de terceros (TanStack/router, shadcn/ui, etc.) → viven en `forks/<slug>/`, carpeta ignorada AL 100% en el workspace. No llevan `.knowledge/` (no se modifica el `.gitignore` de proyectos ajenos). El repo del fork vive por si solo; la memoria de la sesion de contribucion va a `docs/` o `memory/` del workspace. La distincion: `projects/` = proyectos propios (trackea `.knowledge/`), `forks/` = repos ajenos (ignora todo).
- Skills de OpenClaw → viven en `skills/` con su propio SKILL.md
- Proyectos sin documentación completa → los archivos faltantes se documentan en HANDOFF.md en `.knowledge/`

**Ventajas:**
- Cero conflictos: el workspace nunca intenta commitear `node_modules` ni código de build.
- Portabilidad: el código viaja en sus repos, la memoria institucional en el workspace, el archivo completo en el agregado.
- Forks limpios: no colisiona con carpetas `docs/` de repos externos.

## Project Cleanup - Al Finalizar un Proyecto (detalle ampliado)

Cuando un proyecto (libro, curso, tutorial, o app) se completa:

1. **Commit + push final** con todo el contenido del proyecto
2. **Extraer ADRs generales** a `docs/adr/` si corresponde
3. **Limpiar local:** borrar ejercicios crudos (chapters/, node_modules/, configs de build), dejar solo:
   - `.knowledge/` (BRIEF, ROADMAP, ADRs, LEARNINGS, STATUS)
   - `README.md` (opcional, si resume el proyecto)
4. **Commit + push de la limpieza**
5. **Registrar en daily note** que el proyecto se completó y limpió

**Motivación:** los ejercicios crudos son andamio. Los ADR + LEARNINGS son el activo permanente. El workspace no necesita 50MB de node_modules por proyecto completado.

## Verify Before Push (detalle ampliado)

Para proyectos con build step (Vite, Next.js, etc.):

1. **Run `npm run build` before every commit that changes source code.** Biome + tests pueden pasar mientras el build falla por issues de runtime (imports duplicados, exports sin resolver, sintaxis que rolldown no detecta).
2. **No encadenar build + commit en un solo comando largo** salvo que el build sea el último paso antes del commit. Si el comando se cortó o interrumpió, re-correr build por separado y solo después commitear.
3. **Si un build roto llega al repo**, el commit de fix debe incluir la verificación de build también - no solo parchear el archivo y pushear; correr la secuencia pre-commit completa de nuevo.
4. **Preferir el pre-commit hook para enforcear esto.** Orden del hook: lint → test → build. Si el hook se saltea (`SKIP_SIMPLE_GIT_HOOKS=1`), correr la misma secuencia manualmente.

Rationale: un build que falla en `main` bloquea el deploy y quema confianza.
