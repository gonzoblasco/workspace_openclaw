# AGENTS.md - Detalle de Referencia

> Este archivo contiene el detalle operativo completo que se movió de AGENTS.md para mantenerlo bajo el límite de inyección de contexto (20K chars). AGENTS.md tiene las reglas esenciales; acá está el detalle ampliado. Si AGENTS.md referencia este archivo, consultarlo cuando se necesite el detalle.

## Registro automático tras cada PR/ticket (2026-10-13, regla de Gonzo)

**Cuando Gonzo pasa un link a un PR, issue, o su evento/comentario, se registra SIEMPRE en el daily, sin preguntar.** No es opcional y no se pregunta "¿registro?". El registro es la conducta por defecto.

Receta:
1. Leer el hilo externo COMPLETO (body, reviews, todos los comments, timeline del evento referenciado). Nunca responder solo con el link.
2. Analizar el rol de Gonzo en el hilo y el desenlace.
3. Cerrar con: `./skills/session-lifecycle/scripts/session-end.sh --project "<owner>-<repo>" --summary "..."` (DB-first; NUNCA editar `memory/YYYY-MM-DD.md` a mano). El `--project` es el slug de la **carpeta** (`oss/<owner>-<repo>/`), sin barras ni `#`: un slug con separadores creaba un arbol anidado (ver Excepciones). El numero del PR y el titulo del hilo van en el `--summary`, no en el slug.
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

Referencia completa de niveles de pensamiento y asignacion de modelo por rol: **ADR-090** (vigente, cata 2026-10-06). No usar configuraciones de modelo/thinking anteriores: quedaron retiradas.

## Estructura de Proyectos (detalle ampliado)

> **Modelo vigente: ADR-098.** Dos capas, no tres. Los proyectos viven en `<workspace>/projects/`, dentro del árbol que el gateway gobierna; `~/projects` es un **symlink** (el humano llega por ahí, los agentes usan el path real porque los sandboxes rechazan escribir a través de symlinks). El workspace tiene `/projects/` en su `.gitignore`: no es que estén afuera del worktree, es que están adentro y cada uno trae su propio `.git`.

**Filosofía:** cada proyecto es **su propio repo git**, con su `.knowledge/` adentro. La carpeta `projects/` es plana y el workspace la ignora al 100 %.

```
projects/                     (carpeta plana, ignorada por el workspace - NO es repo)
└── <slug>/                   (repo individual: gonzoblasco/<slug>)
    ├── .knowledge/           # BRIEF, ADRs, STATUS, HANDOFF - vive CON el proyecto
    ├── src/
    └── .git/                 # del proyecto, nunca se absorbe en el workspace
```

**Reglas clave:**

- **`projects/` no es repo.** No tiene `.git` propio; cada `<slug>/` sí.
- **La fuente de la verdad es el repo del proyecto.** No hay repo agregado que sincronizar (la capa `projects_openclaw` se retiró y está archivada).
- **`.knowledge/` viaja con el proyecto**, en su repo. El workspace nunca lo trackea.
- **Backup antes de limpiar:** `.knowledge/`, `.env`, `*.db` y uploads son irrecuperables. Respaldar ANTES de cualquier `git reset --hard` o limpieza.

**Flujo típico:**

1. Nuevo producto → `./scripts/init-project.sh <slug>` (crea `.knowledge/` con BRIEF + STATUS, repo privado en gh, git inicializado).
2. Scaffold en `projects/<slug>/`.
3. Desarrollo → actualizar `.knowledge/STATUS.md` en cada hito.
4. Commits: código + `.knowledge/` al repo del proyecto.

**Sin submódulos.** Los proyectos se clonan bajo demanda, no como submódulos. Si una carpeta de `projects/` no tiene repo en GitHub, se elimina.

**Dónde vive qué (clasificación por destino, no por gusto):**

| Tipo | Dónde | `.knowledge/` |
|---|---|---|
| Proyecto propio | `projects/<slug>/` | Sí, en su repo |
| Fork para mandar un PR | `forks/<slug>/` | **No** — entraría al diff del maintainer |
| Tercero que corre como servicio | `services/<slug>/` | Sí, en nuestro fork |
| Contribución a repo ajeno | `oss/<owner>-<repo>/.knowledge/` | Sí, es el registro del hilo |
| Skill de OpenClaw | `skills/` (Core) o `agents/<rol>/skills/` (rol) | — |

Notas de cada una:

- **Forks:** ignorados al 100 %. Si un `.knowledge/` ya quedó trackeado: `git rm -r --cached .knowledge/` (queda en disco) y agregarlo a `.git/info/exclude` del clon, que es privado. Tocar el `.gitignore` del fork **sí** ensucia el repo ajeno. Lo verifica `scripts/check-foreign-knowledge.py`.
- **Servicios:** no se les manda PR, se los opera. Caso actual: `services/vane/`.
- **Contribuciones:** el slug es `<owner>-<repo>`. `scripts/session-handoff.py` rechaza slugs con separadores o `..` — el 2026-10-29 un `--project "OSS / astryx #3335"` creó un árbol fantasma.
- **Proyectos sin doc completa:** lo que falte se documenta en `.knowledge/HANDOFF.md`.

**Ventajas:** el workspace nunca commitea `node_modules` ni código de build ni memoria de proyecto; código y memoria viajan juntos; los forks quedan limpios.

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

## Tools — detalle

Resumen operativo que vive en `AGENTS.md` (subagentes solo reciben ese archivo). Acá va el detalle que no entra ahí.

- **Scripts clave:** `scripts/complexity-scorer.sh` (T-score antes de spawnear agentes), `scripts/pipeline-track.sh` (estado durable del pipeline).


## Verificar la palabra de Gonzo contra el repo, no contra mi lectura (detalle ampliado)

La regla vive en `AGENTS.md` §0. Acá quedan los casos que la motivaron.

Dos casos del 2026-10-27, el mismo error dos veces en una tarde:

- Leí `skills/job-application/SKILL.md`, que dice *"deja el submit al humano"*, y afirmé que el flujo de postulaciones **nunca enviaba**. El repo tenía `6c24187b9d` *"cierre de la tanda - las TRES postulaciones confirmadas"*: Mural, Mercado Pago y RYZ, **confirmadas por el servidor**. Lo correcto era "envía con tu OK", no "no envía".
- Afirmé que el MCP de browser-use no podía subir archivos. Cierto, pero por el motivo equivocado: no era una limitación del diseño, era que el tool no existe en las 16 del server.

El mecanismo del error es siempre el mismo: **generalizo una línea de un documento a un hecho del mundo.** La regla de `memory/user-profile.md` "verificar antes de descartar" (2026-09-13) ya lo cubría; lo que faltaba era el caso de "verificar antes de *confirmar*", que es el que se repite.

Corolario operativo: cuando Gonzo dice "ya lo hemos hecho", la respuesta correcta es **buscar el commit**, no argumentar. Si aparece, se corrige el registro y se sigue.
