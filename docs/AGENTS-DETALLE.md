# AGENTS.md - Detalle de Referencia

> Este archivo contiene el detalle operativo completo que se movió de AGENTS.md para mantenerlo bajo el límite de inyección de contexto (20K chars). AGENTS.md tiene las reglas esenciales; acá está el detalle ampliado. Si AGENTS.md referencia este archivo, consultarlo cuando se necesite el detalle.

## Reglas de feedback en PRs/issues ajenos (detalle ampliado)

Reglas duras de Gonzo para publicar feedback/review en repos de terceros. Corregidas 24/08 - no repetirlas.

1. **Leer SIEMPRE toda la vida del ticket ANTES de comentar o hacer nada.** Body, reviews, TODOS los comments (incluidos los de autores/maintainers posteriores al review), inline comments, estado actual. Si no tengo el repo clonado y el claim depende del código base, plantear como pregunta/"worth checking" honesto, NO como afirmación. Opción: clonar el repo en `forks/` para poder verificar.
2. **El autor del PR/issue define, no el invitado.** Para saber con quién se habla, basta con ver quién creó el PR/issue (el autor). No cerrar con elogios/"nice work"/adulación hacia el autor - el invitado no valida el trabajo ajeno; eso es ruido. El reconocimiento va implícito en la interacción.
3. **No subir un comentario solo para disculparse por otro.** Disculparse no está mal, pero subir un comentario nuevo únicamente para pedir disculpas por uno anterior malo genera ruido. Lo correcto: si un comentario salió mal (desactualizado, mal contexto, error), BORRARLO y volver a generarlo correcto - sin comentario de disculpa adicional.
4. **Nunca repetir lo que ya se dijo en el hilo** ni repetir mis propios comentarios. Siempre aportar algo nuevo que ayude, sin huevadas.
5. **NO exponer notas internas/borradores en el hilo público.** El archivo de borrador (con encabezado "Borrador", "Notas para Gonzo", análisis interno) es SOLO para revisión de Gonzo - NUNCA publicarlo directo. Al publicar, usar SOLO el texto del comentario final limpio (sin encabezado de borrador ni notas internas). (Error real en #5204 y #4611: publiqué el archivo con notas internas; se borró y se republicó limpio.)
6. **Siempre dar la URL** del PR/issue al reportar trabajo hecho.
7. **No agradecer a bots de review.** Cuando el review/comentario de un PR es de una IA (ej: Enough1122 en hermes-agent, "AI code review - automated review for reference"), NO ponerle "Thanks for the review" - solo se agradece a humanos. Los reviews de IA con puntos accionables se responden directo a la sustancia con evidencia (qué se arregló, cómo se verificó), sin saludo. (Corrección de Gonzo en hermes-agent #93848.)

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

**Verificación:** tras copiar, `grep -rn "gonzoblasco\|Gonzalo\|Gonzo\|@gonzoblasco" skills/ | grep -v __pycache__` debe dar vacío.

**Excepción legítima:** las referencias a `gonzoblasco/kanam-skills` en README, docs y web/generate.js (identidad de instalación del repo) y el LICENSE (copyright legal) se mantienen.

## Estructura de Proyectos - Doble Git (detalle ampliado)

**Filosofía:** Cada proyecto tiene su carpeta en `projects/<slug>/` con sincronización selectiva:

```
projects/<slug>/
├── .knowledge/     # Documentación interna: BRIEF, EVALUATION, DEFINITION, ROADMAP, STATUS, HANDOFF, ADRs, decisiones
├── src/            # Código fuente (con su propio .git y remote)
├── package.json    # Configuración del proyecto
└── .gitignore      # Ignora .knowledge/ (ya lo guarda el workspace) + node_modules, etc.
```

**Reglas de Doble Git:**
- **Workspace git:** Trackea solo `projects/**/.knowledge/`. Ignora el resto del código (`.gitignore` raíz: `projects/` + `!projects/**/.knowledge/`).
- **Proyecto git:** Trackea todo el código. Ignora `.knowledge/` (ya lo guarda el workspace).
- **Memoria institucional:** El workspace git versiona intensivamente `.knowledge/` (el qué y por qué).
- **Código:** Cada proyecto tiene su propio repo para la implementación (el cómo).

**Flujo típico:**
1. Nuevo producto → `./scripts/init-project.sh <slug> [--repo <url>]`
   - Crea `projects/<slug>/.knowledge/` con BRIEF.md + STATUS.md
   - Crea `.gitignore` que ignora `.knowledge/` para el repo del proyecto
   - Si tiene `--repo`, inicializa git y pushea
2. Go decision → scaffold en `projects/<slug>/` (repo separado, ignora `.knowledge/`)
3. Desarrollo → actualizar `projects/<slug>/.knowledge/STATUS.md` con cada hito
4. Commits: `.knowledge/` al workspace, código al repo del proyecto

**Sin submódulos.** GitHub es la fuente de la verdad. Los proyectos se clonan en `projects/<slug>/` bajo demanda (cuando se trabajan), no como submódulos del workspace. El workspace trackea solo `.knowledge/` (la memoria institucional); el código vive en su repo. Si una carpeta de `projects/` no tiene repo en GitHub, se elimina.

**Excepciones:**
- Forks de terceros (TanStack/router, shadcn/ui, etc.) → viven en `forks/<slug>/`, carpeta ignorada AL 100% en el workspace. No llevan `.knowledge/` (no se modifica el `.gitignore` de proyectos ajenos). El repo del fork vive por si solo; la memoria de la sesion de contribucion va a `docs/` o `memory/` del workspace. La distincion: `projects/` = proyectos propios (trackea `.knowledge/`), `forks/` = repos ajenos (ignora todo).
- Skills de OpenClaw → viven en `skills/` con su propio SKILL.md
- Proyectos sin documentación completa → los archivos faltantes se documentan en HANDOFF.md en `.knowledge/`

**Ventajas:**
- Cero conflictos: el workspace nunca intenta commitear `node_modules` ni código de build.
- Portabilidad: el código viaja en su repo, la memoria institucional en el workspace.
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
