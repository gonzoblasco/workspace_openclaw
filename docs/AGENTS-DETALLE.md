# AGENTS.md - Detalle de Referencia

> Este archivo contiene el detalle operativo completo que se movió de AGENTS.md para mantenerlo bajo el límite de inyección de contexto (20K chars). AGENTS.md tiene las reglas esenciales; acá está el detalle ampliado. Si AGENTS.md referencia este archivo, consultarlo cuando se necesite el detalle.

## Registro automático tras cada PR/ticket (2026-10-13, regla de Gonzo)

**Cuando Gonzo pasa un link a un PR, issue, o su evento/comentario, se registra SIEMPRE en el daily, sin preguntar.** No es opcional y no se pregunta "¿registro?". El registro es la conducta por defecto.

Receta:
1. Leer el hilo externo COMPLETO (body, reviews, todos los comments, timeline del evento referenciado). Nunca responder solo con el link.
2. Analizar el rol de Gonzo en el hilo y el desenlace.
3. Cerrar con: `./scripts/memory-end-session.py --project "OSS / <repo> #<n>" --summary "..."` (DB-first; NUNCA editar `memory/YYYY-MM-DD.md` a mano).
4. Si el cambio quedó en el workspace (ej. AGENTS.md), commit + push del workspace al finalizar.

Casos que originaron la regla (2026-10-13): TanStack/router#7825 (fix upstream merged), vercel/ai#15704 + PR#17274 (cerrado por decisión de producto), facebook/astryx#5204 (superseded con crédito).

## Reglas de feedback en PRs/issues ajenos (detalle ampliado)

Reglas duras de Gonzo para publicar feedback/review en repos de terceros. Corregidas 24/08 - no repetirlas.

1. **Leer SIEMPRE toda la vida del ticket ANTES de comentar o hacer nada.** Y ANTES DE ESO, chequear contexto interno: `memory_search()` + `sessions_search()` por el numero de issue - si ya participamos, contextualizar con nuestro rol (lecciones carbon #16031, 2026-09-09/10). Body, reviews, TODOS los comments (incluidos los de autores/maintainers posteriores al review), inline comments, estado actual. El contexto que Gonzo comparte es el punto de partida, nunca el hilo completo: leer siempre body + todos los comments e interacciones antes de responder. Si no tengo el repo clonado y el claim depende del código base, plantear como pregunta/"worth checking" honesto, NO como afirmación. Opción: clonar el repo en `forks/` para poder verificar.
2. **El autor del PR/issue define, no el invitado.** Para saber con quién se habla, basta con ver quién creó el PR/issue (el autor). No cerrar con elogios/"nice work"/adulación hacia el autor - el invitado no valida el trabajo ajeno; eso es ruido. El reconocimiento va implícito en la interacción.
3. **No subir un comentario solo para disculparse por otro.** Disculparse no está mal, pero subir un comentario nuevo únicamente para pedir disculpas por uno anterior malo genera ruido. Lo correcto: si un comentario salió mal (desactualizado, mal contexto, error), BORRARLO y volver a generarlo correcto - sin comentario de disculpa adicional.
4. **Nunca repetir lo que ya se dijo en el hilo** ni repetir mis propios comentarios. Siempre aportar algo nuevo que ayude, sin huevadas.
5. **NO exponer notas internas/borradores en el hilo público.** El archivo de borrador (con encabezado "Borrador", "Notas para Gonzo", análisis interno) es SOLO para revisión de Gonzo - NUNCA publicarlo directo. Al publicar, usar SOLO el texto del comentario final limpio (sin encabezado de borrador ni notas internas). (Error real en #5204 y #4611: publiqué el archivo con notas internas; se borró y se republicó limpio.)
6. **Siempre dar la URL** del PR/issue al reportar trabajo hecho.
7. **No agradecer a bots de review.** Cuando el review/comentario de un PR es de una IA (ej: Enough1122 en hermes-agent, "AI code review - automated review for reference"), NO ponerle "Thanks for the review" - solo se agradece a humanos. Los reviews de IA con puntos accionables se responden directo a la sustancia con evidencia (qué se arregló, cómo se verificó), sin saludo. (Corrección de Gonzo en hermes-agent #93848.)
8. **Atribución por login, nunca por contexto (2026-09-22).** La autoría de cada review/comentario del hilo se verifica por el `user.login` en la API - NUNCA se infiere de la cercanía temporal, del contexto de otra sesión ni de que esa persona haya revisado PRs nuestros antes. Error real en astryx #4690: el CHANGES_REQUESTED de `humbertovirtudes` (maintainer que revisó #4157 y quedaba pendiente en #4298, ambos nuestros) fue reportado a Gonzo como si fuera suyo, por proximidad de contexto. Regla dura: "nuestro" = login `gonzoblasco` verificado en la fuente; toda otra cuenta es tercero, INCLUIDOS maintainers que revisan nuestro trabajo en ese repo. Verificación mecánica: `scripts/pr-thread-brief.sh <owner/repo> <n> [login]` clasifica cada evento del hilo OURS/BOT/THIRD, resume por actor y nombra el último acto no-bot (quién tiene la pelota). Corolario: nunca narrar un acto del hilo como "vos/nuestro/nos pidieron" sin ese chequeo o su equivalente API.

**Regla de contexto:** los borradores de feedback se guardan en `docs/feedback/<repo>-<numero>-draft.md` para revisión de Gonzo. El archivo de borrador y el texto a publicar son cosas DISTINTAS - al publicar, nunca usar el archivo de borrador directo; extraer solo el texto final del comentario.

## El CORE verifica ANTES de reportar (2026-10-08, regla de Gonzo)

**El visto bueno de Gonzo cierra la fase; nunca es el primer chequeo.** El orden es: el writer entrega $\rightarrow$ **el CORE corre los gates él mismo** $\rightarrow$ arregla lo que esté roto $\rightarrow$ **recién entonces reporta**, con la salida cruda del comando pegada $\rightarrow$ Gonzo aprueba una vez y la fase cierra.

- **Prohibido reportar "funciona / N tests pasan / E2E OK" sin la salida real del comando abajo.** Si no corrí el gate, digo "no verificado". El auto-reporte de un subagente no es prueba - es una hipótesis a chequear.
- **Si el gate está rojo, no hay reporte de fase.** Un "fase completa" con `tsc` o tests en rojo no sale de esta sesión.
- **Por qué:** el 2026-10-08 reporté "182 tests pasan, streaming implementado, E2E 200 OK" sobre un working tree que tenía `tsc` roto, 2 tests fallando, un `return` faltante en `handler.ts` y el shim Deno sin tocar. Gonzo terminó siendo el QA y rehaciendo el trabajo: exactamente lo que esta regla evita.
- **Objetivo:** cada fase cierra con **un solo visto bueno**. El número de correcciones por fase baja, no sube. Si aparece un error, que sea más simple que el anterior, nunca más complejo.

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

Referencia completa de niveles de pensamiento y asignacion de modelo por rol: **ADR-090** (vigente, cata 2026-10-06). La tabla MAX vs HIGH de `docs/adr/ADR-040-modelos-seleccion-por-tarea.md` es **historica**: ADR-053 la reemplazo para modelo/thinking y ADR-090 reemplaza ambas. No usarla para decidir niveles hoy.

## Skills Públicas - Sanitización (detalle ampliado)

El repo `kanam-skills` (github.com/gonzoblasco/kanam-skills) es **público**. Las skills que van ahí NO deben contener referencias personales de Gonzo (nombre, handle `gonzoblasco`, repos, rutas `/Users/gonzoblasco/`, issues específicos).

**Dos versiones de cada skill:**
- **Workspace** (`skills/`): privado, **mantiene** las referencias personales - son el setup de Gonzo y el contexto es valioso. (El mirror `.github/skills/` se elimino el 2026-09-28, ADR-079.)
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

> **Actualizado 2026-10-12 al modelo ADR-098 (2026-10-08).** Los proyectos viven en `<workspace>/projects/`, **dentro** del árbol que el gateway gobierna; `~/projects` es un **symlink** a `<workspace>/projects` (el humano llega por ahí, los agentes usan el path real porque los sandboxes rechazan escribir a través de symlinks). El `.gitignore` conserva `/projects/`, pero el motivo se invirtió (no "afuera del worktree" sino "adentro, y cada proyecto trae su propio `.git`"). El workspace no trackea el código ni el `.knowledge/` de los proyectos. Modelo previo (2026-09-27 a 2026-10-08): los proyectos vivían en `~/projects/` como carpeta real, fuera del worktree (ADR-075, hoy superseded). Si encontrás texto que diga que viven "fuera del workspace", es deriva vieja.

**Filosofía:** cada proyecto tiene su carpeta en `projects/<slug>/` y es **su propio repo git** (con su `.knowledge/` adentro). La carpeta contenedora `projects/` es plana y el workspace la ignora al 100%.

```
projects/                     (carpeta plana, ignorada al 100% por el workspace git - NO es repo)
└── <slug>/                   (repo individual del proyecto: gonzoblasco/<slug>)
    ├── .knowledge/           # memoria institucional (BRIEF, ADRs, STATUS, HANDOFF) - vive CON el proyecto
    ├── src/                  # código fuente (lo trackea el repo individual)
    └── .git/                 # del proyecto, nunca se absorbe en el workspace
```

**Capas y responsabilidades:**
- **Workspace git** (`workspace_openclaw`): **no trackea `projects/`.** Su `.gitignore` tiene `/projects/` (ADR-098). No hay capa intermedia.
- **Repo individual** (`projects/<slug>` -> `gonzoblasco/<slug>`): la fuente de la verdad. Ahi viven commits, branches, PRs, push. Cada uno con su propio `.gitignore`; el `.knowledge/` se trackea en el repo del proyecto (los que lo excluyen lo hacen vía `.git/info/exclude`).

**Reglas clave:**
- **`projects/` no es repo.** No tiene `.git` propio; cada `<slug>/` es su propio repo. Ninguna capa absorbe ni commitea los `.git/` de los proyectos.
- **La fuente de la verdad para trabajar es el repo individual del proyecto.** No hay repo agregado que sincronizar.
- **Backup de datos locales antes de limpiar:** los `.knowledge/`, `.env`, `*.db` y uploads son irrecuperables si se borran. Respaldar ANTES de cualquier `git reset --hard` o limpieza.

**Flujo típico:**
1. Nuevo producto → `./scripts/init-project.sh <slug>`
   - Crea `projects/<slug>/.knowledge/` con BRIEF.md + STATUS.md
   - Crea repo privado en gh e inicializa el git del proyecto
2. Go decision → scaffold en `projects/<slug>/` (repo individual)
3. Desarrollo → actualizar `projects/<slug>/.knowledge/STATUS.md` con cada hito
4. Commits: código + `.knowledge/` al repo del proyecto

> **Nota de estado (actualizada 2026-10-13).** `init-project.sh` y `initial-setup.sh` todavia referencian la capa "agregado" (`projects_openclaw`) retirada; ver la fila de cada uno en `docs/SETUP.md`. El modelo vigente (ADR-098): `projects/` es carpeta plana ignorada, cada proyecto es su propio repo con su `.knowledge/`.

**Sin submódulos.** Los proyectos se clonan en `projects/<slug>/` bajo demanda (cuando se trabajan), no como submódulos. Si una carpeta de `projects/` no tiene repo en GitHub, se elimina.

**Excepciones:**
- Forks de terceros (TanStack/router, shadcn/ui, etc.) → viven en `forks/<slug>/`, carpeta ignorada AL 100% en el workspace (no existe como `projects/forks`). No llevan `.knowledge/` (no se modifica el `.gitignore` de proyectos ajenos). El repo del fork vive por si solo; la memoria de la sesion de contribucion va a `docs/` o `memory/` del workspace.
- Skills de OpenClaw → viven en `skills/` (Core) y `agents/<rol>/skills/` (rol) con su propio SKILL.md
- Proyectos sin documentación completa → los archivos faltantes se documentan en HANDOFF.md en `.knowledge/` (que reemplazo al BRIEF)

**Ventajas:**
- Cero conflictos: el workspace nunca intenta commitear `node_modules` ni código de build ni memoria de proyecto.
- Portabilidad: el código y su memoria viajan juntos en el repo del proyecto; el archivo completo en el agregado.
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
