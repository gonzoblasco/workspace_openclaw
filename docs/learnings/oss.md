# Learnings - oss

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## 2026-08-10 (cierre) - Sesión OSS: conflictos, PR nuevo, reconstrucción de skill

**Context:** Sesión de contribución OSS. Barrido de 27 PRs, resolución de conflictos (astryx #4023, TanStack #7834), PR nuevo en shadcn (#11465), y reconstrucción de la skill `oss-contribution` que se había perdido en la consolidación.

**Lesson - el commit vacío es una herramienta de diagnóstico, no solo de refresh:**
- `git commit --allow-empty` re-dispara CI y fuerza a GitHub a recalcular mergeability. Pensé que los CONFLICTING eran falsos positivos, pero el recálculo reveló conflictos reales ocultos (cruce de ramas en astryx #4023, main desactualizado en TanStack #7834).
- Lección: cuando GitHub muestra CONFLICTING, NO asumir que es un artefacto. Verificar contra el upstream real antes de descartarlo.

**Lesson - el main del fork puede estar desactualizado vs el upstream:**
- En TanStack #7834, mi main local del fork estaba 70 commits atrás del main real de TanStack. Por eso GitHub veía conflicto y yo no. Siempre fetch del upstream real (`git fetch upstream main`), no del origin (fork).
- `--force-with-lease` falla con "stale info" tras un rebase. Usar `--force-with-lease=<branch>:<sha-esperado>` con el sha del remote verificado.

**Lesson - la jugada del "robo de PR" (astryx #4777):**
- Cuando otro contributor quiere tomar un issue/PR en el que ya trabajamos, la jugada ganadora no es pelear por quién manda el PR de la opción débil - es resolver su objeción dentro de la opción fuerte. Validar su punto técnico (le da crédito), pero mostrar que la dirección que defendemos tiene una variante que resuelve su objeción.

**Lesson - el valor del análisis en el issue antes del PR (shadcn #11125):**
- Hacer el análisis técnico en el issue antes de mandar el PR (validando el approach con otro contributor) hace que el PR salga limpio y con el root cause ya consensuado. El issue es el lugar para converger; el PR es la ejecución.

**Lesson - skills públicas: sin referencias personales:**
- Una skill pública (kanam-skills) NO debe contener referencias a issues específicos de Gonzo (astryx #4777, shadcn #11125) ni menciones por nombre (Gonzo, gonzoblasco). Eso filtra contexto personal y no aporta a quien la use.
- La enseñanza sí, la referencia concreta no. Reemplazar por términos genéricos (el usuario, el operador) y parametrizar scripts (username del gh autenticado en vez de hardcodear gonzoblasco).
- Gonzo me corrigió dos veces en esto - es una regla que hay que internalizar: **toda skill pública se escribe como si la fuera a usar un extraño.**

**Self-reflection:**
- CONTEXT: sesión OSS multi-step (barrido de PRs, conflictos, PR nuevo, reconstrucción de skill)
- REFLECTION: la sesión fue productiva (2 conflictos resueltos, 1 PR nuevo, 1 skill reconstruida), pero cometí el error de asumir que los CONFLICTING eran falsos positivos sin verificar contra el upstream real, y de escribir la skill pública con referencias personales.
- LESSON: verificar contra el upstream real antes de descartar un conflicto; escribir skills públicas como si las usara un extraño.
- BIASES DETECTED: confirmation bias (asumí que el conflicto era falso porque mi main local estaba desactualizado y confirmaba mi hipótesis).

**Tags:** Sesión OSS: conflictos, PR nuevo, reconstrucción de skill

---

## 2026-08-11 - OSS astryx: diagnóstico de CI + PR de fix (doble contribución)

**Context:** Sesión OSS en facebook/astryx. El PR #4298 (a11y AvatarStatusDot) estaba aprobado pero bloqueado por un check de CI que fallaba con `no merge base`. Al investigar, resultó ser un bug del workflow, no del código.

**Lesson - verificar el job exacto del run que falla antes de diagnosticar:**
- Confundí el workflow "CLI Smoke Test" con el job `build-storybook` del workflow "CI". El `gh pr checks` mostraba "smoke-test" y asumí que era ese job. El `gh run view --log-failed` del run correcto (31191734656) reveló que el job real era `build-storybook`.
- LESSON: cuando un check falla, rastrear el run exacto (`gh run list` + `gh run view --json jobs`) y el job que falló antes de escribir el diagnóstico. Un diagnóstico con el job equivocado es peor que no diagnosticar - tuve que corregir el comentario del PR.

**Lesson - `fetch-depth: 50` es una ventana fija que se rompe con PRs viejos:**
- El bug real: `analyze-pr.js` hace three-dot diff (`base...head`) que necesita merge base. Con `fetch-depth: 50`, si el PR lleva días abierto y main avanza más de 50 commits, el merge base queda fuera de la ventana y el diff falla con `no merge base`.
- No es un checkout olvidado (ese era mi primer diagnóstico equivocado) - es un límite de diseño del workflow. El propio ci.yml documenta el patrón en dos jobs.
- LESSON: los límites fijos (depth, timeouts, paginación) fallan silenciosamente con el tiempo. Un PR que pasa hoy puede fallar mañana sin tocar nada.

**Lesson - el fallback a two-dot diff es el fix correcto:**
- En `getChangedFiles()`, cuando el three-dot falla, caer a two-dot (`base..head`) que no necesita merge base. Nunca hard-faila. Puede sobre-reportar (incluye commits ya en base) pero nunca sub-reporta los cambios del PR.
- Validado con simulación real: reproduje el caso exacto (clone shallow, merge base fuera de ventana) y confirmé que el three-dot falla y el two-dot funciona.

**Self-reflection:**
- CONTEXT: diagnóstico de CI + issue + PR de fix en repo de Facebook
- REFLECTION: el flujo fue bueno (diagnóstico → issue → PR), pero el primer comentario del PR tenía el job equivocado. La corrección oportuna (antes de que el maintainer lo leyera como definitivo) evitó daño, pero el proceso correcto es verificar el job exacto ANTES de postear.
- LESSON: en contribuciones OSS, un diagnóstico técnico incorrecto en un thread público resta credibilidad. Verificar el run/job exacto con `gh run view --log-failed` antes de afirmar la causa.
- BIASES DETECTED: anchoring (me anclé en el nombre "smoke-test" del `gh pr checks` sin verificar el job real del run).

**Tags:** OSS astryx: diagnóstico de CI + PR de fix (doble contribución)

---

## 2026-08-14 - radix-ui: cuando alguien implementa tu análisis, sé el reviewer

**Context:** Gonzo documentó en el issue #4110 de radix-ui/primitives la causa raíz de un bug de a11y (race de timing: VoiceOver lee la primera opción antes de que el re-render pinte los atributos) y 2 opciones de fix. No subió código, solo análisis. Días después, otro contributor (waterWang) abrió el PR #4112 implementando literalmente la opción A - y con un approach técnicamente superior (setAttribute directo en el DOM en useLayoutEffect, evitando el state round-trip).

**Lesson - cuando alguien implementa tu análisis, el mejor move no es reclamar autoría, es convertirte en el reviewer con el contexto completo:**
- No es robo de código (Gonzo no subió código, solo análisis) - es robo de dirección, y la ejecutó mejor. Decir "está mal" sería deshonesto y quemaría credibilidad con los maintainers.
- El review honesto (validar el approach + señalar gaps reales) posiciona mejor que reclamar. El gap real del PR ajeno (falta de tests) es la puerta de entrada para tu propio trabajo: el #4109 de Gonzo ya tiene 3 tests que cubren exactamente ese comportamiento.
- Cerrar el review con "happy to help if useful" deja la puerta abierta para que te pidan los tests, y quedás como co-autor de facto del fix completo.
- Regla: en OSS, la autoría del análisis vale menos que la capacidad de demostrar que entendés el problema a fondo. El reviewer que ya tiene el contexto completo gana la posición.

**Self-reflection:**
- CONTEXT: review de PR OSS (radix-ui #4112)
- REFLECTION: el instinto inicial de Gonzo fue "nos quieren robar". Mi lectura honesta lo reencuadró: no es robo, es validación de que el análisis era correcto, y la ejecución ajena fue mejor. El review honesto posiciona mejor que el reclamo.
- LESSON: en OSS, cuando alguien implementa tu análisis, sé el reviewer con el contexto completo - no el reclamante. El gap de tests del otro PR es tu puerta de entrada.
- BIASES DETECTED: sunk cost / territorialidad (querer defender "nuestro" reporte). Contrarrestado con honestidad y foco en el resultado.

**Tags:** radix-ui: cuando alguien implementa tu análisis, sé el reviewer

---

## 2026-08-14 - colinhacks/zod: el diagnóstico correcto no garantiza el merge si la implementación no respeta la arquitectura

**Context:** PR #6385 de Gonzo en zod (fix exactOptional + coerce, bug #6236) fue cerrado por colinhacks sin merge. El diagnóstico de causa raíz era correcto y colinhacks lo reconoció ("The diagnosis is right", "Thanks for the investigation, it's what pinned down the JIT/jitless split"). Pero la implementación (helper `hasApplicableFallback` que enumeraba tipos de wrapper en el object loop) no era la arquitectura que el maintainer quería. colinhacks indicó la dirección (fix en `$ZodExactOptional.parse` via `optin`) y abrió su propio PR #6405 implementándola.

**Lesson - en repos con maintainer fuerte y opinado, la dirección de diseño pesa tanto como la corrección:**
- El feedback accionable (los 2 P2 del bot Codex) se arregla y se mergea. La dirección de fondo (cómo debe expresarse el fix en la arquitectura del repo) no es negociable - si no la respetás, el maintainer cierra y lo implementa él mismo.
- El diagnóstico correcto es necesario pero no suficiente. Antes de implementar un fix en un repo con maintainer opinado, vale la pena mirar cómo el maintainer ya resolvió problemas similares (qué patrones usa, qué rechaza) para alinear la implementación con su visión desde el arranque.
- Riesgo de reviews automatizados (Codex, etc.): dan feedback de corrección (P2 puntuales), no de diseño. Ninguno señaló el problema arquitectónico de fondo (hardcoded list de tipos). El problema real lo vio el maintainer al leer el código.
- No fue un "robo" ni un cierre injusto: fue un maintainer que prefirió implementar él mismo con su arquitectura. El trabajo de Gonzo no se perdió - fue el trampolín que validó el diagnóstico y le dio al maintainer la dirección. Eso tiene valor de portfolio (crédito explícito del maintainer).

**Self-reflection:**
- CONTEXT: post-mortem de PR OSS cerrado (zod #6385)
- REFLECTION: el instinto de Gonzo fue "¿hicimos algo mal?". La respuesta honesta: no fue un error de proceso grave, pero sí una lección de alineación con la arquitectura del maintainer. El diagnóstico fue el activo; la implementación fue el punto de fricción.
- LESSON: en repos con maintainer opinado, alinear la implementación con la visión del maintainer desde el arranque (mirar cómo resolvió problemas similares) vale más que un fix funcionalmente correcto con arquitectura ajena.
- BIASES DETECTED: confirmation bias (asumir que un fix con 3921 tests verdes y 2 P2 arreglados estaba "listo para mergear" sin considerar la dirección de diseño del maintainer).

**Tags:** colinhacks/zod: el diagnóstico correcto no garantiza el merge si la implementación no respeta la arquitectura

---

## 2026-08-17 - Verificar el estado real de los PRs ANTES de proponer acciones

**Context:** Durante la revisión de PRs OSS, propuse cerrar mi PR #4109 (radix Select) a favor del #4112 de waterWang. Gonzo me corrigió: ya había dejado un review en #4112 dando visto bueno al enfoque con 4 mejoras. No lo había leído.

**Lesson:** al revisar un set de PRs/discusiones donde ya participé, la fuente de verdad es el estado ACTUAL de cada PR (reviews, comentarios, últimas acciones), no mi memoria de lo que hice o el resumen que armé antes. Asumí que #4112 era "un PR nuevo que criticaba el mío" sin leer que ya lo había reviewado. Verificar antes de proponer destruir/cerrar trabajo.

**Proceso que evita esto:** antes de recomendar cerrar/mergear/actualizar un PR, hacer `gh pr view <n> --repo <r> --json reviews,comments` y leer el thread completo. En particular, buscar MIS reviews previos - son la señal más fuerte de lo que ya decidí.

**Self-reflection:**
- CONTEXT: revisión de PRs OSS, propuse acción incorrecta
- REFLECTION: no leí mi propio review en #4112 antes de proponer cerrar #4109
- LESSON: verificar el estado real (reviews/comentarios) de cada PR antes de proponer acciones; mis reviews previos son señal de decisiones ya tomadas
- BIASES DETECTED: recency bias (el #4112 era "reciente" en mi lectura y lo traté como pendiente) + falta de verificación (no chequé el thread completo antes de opinar)

**Tags:** Verificar el estado real de los PRs ANTES de proponer acciones

---

## 2026-08-20 - Buscar oportunidades OSS ≠ revisar mis PRs (repos nuevos de terceros)

**Context:** Sesión de OSS. Gonzo pidió "buscar issues/PRs en los que aportar". Arranqué mal: usé `gh pr list --author gonzoblasco --state open` que devolvió `[]` y me confundió. Gonzo corrigió: la búsqueda de oportunidades NO debe usar `--author` ni mirar mis forks/repos - debe ir a repos NUEVOS de terceros.

**La distinción clave (dos usos distintos de `gh`):**
- **Revisar MIS PRs** (seguimiento): iterar repo por repo con `gh pr list --repo <org/repo> --author gonzoblasco` (los repos donde ya tengo PRs abiertos).
- **Buscar OPORTUNIDADES** (triaje): NUNCA con `--author`. Triajear issues de repos NUEVOS de terceros con `gh issue list --repo <org/repo> --label accessibility`, y verificar que no haya PR competidor (`gh search prs --repo <org/repo> "#<issue>" --state open`) antes de invertir tiempo.

**Regla de repos:** buscar en repos donde NO hemos trabajado. Ya trabajamos en: astryx, radix-ui, shadcn-ui, TanStack (router/query), vercel/ai, zod, payloadcms, nextra, google/skills, ibelick/ui-skills, hallmark, carbon-design-system, swift-testing, supabase, ariakit, dub. Repos nuevos buenos para el perfil (React/TS + a11y): adobe/react-spectrum (GOLD: a11y es el core), mui/material-ui, mui/base-ui, elastic/eui, microsoft/fluentui.

**Lección:** para encontrar oportunidades de contribución, mirar hacia afuera (repos nuevos de terceros, issues sin competencia), no hacia adentro (mis propios forks/PRs). El `gh pr list --author` sirve para seguimiento de lo que ya existe, no para descubrir qué aportar.

**Self-reflection:**
- CONTEXT: búsqueda de oportunidades OSS
- REFLECTION: usé `gh pr list --author` (herramienta de seguimiento) para una tarea de descubrimiento (buscar oportunidades), y me confundió el resultado vacío. Gonzo aclaró: buscar en repos nuevos de terceros, no donde ya trabajamos.
- LESSON: separar las dos operaciones - seguimiento de PRs propios (por repo, con --author) vs triaje de oportunidades (repos nuevos, sin --author, verificar competencia).
- BIASES DETECTED: anchoring (me anclé en el workflow de seguimiento de PRs propios y lo apliqué mal a la búsqueda de oportunidades).

**Tags:** Buscar oportunidades OSS ≠ revisar mis PRs (repos nuevos de terceros)

---

## 2026-08-21 - Serializers de hash: colisión de tipos es un bug real (y el humano manda sobre el bot)

**Context:** PR TanStack/router #7834. Redirigí el PR a `stringifyLoaderDeps` configurable (pedido de schiller-manuel). CodeRabbit detectó un major: `safeStringify({ id: 123n })` y `safeStringify({ id: '123n' })` producían el mismo hash (`{"id":"123n"}`). Como el output alimenta `loaderDepsHash`, dos deps distintas podían colisionar y reusar datos stale.

**La lección - colisión de tipos en serializers:**
- Un serializer que convierte tipos distintos a la misma representación de string es un bug de integridad, no cosmético. `123n` vs `'123n'`, `undefined` vs `''`, `Date` vs su ISO string: todos colisionan si no se taggea el tipo.
- Fix correcto: **prefijo tag reservado** (`\u0000`) + **escape por duplicación** para strings de usuario que empiecen con el prefijo. Así los tags nunca colisionan con datos de usuario.
- `JSON.stringify` NO lanza con Set/Map - los serializa silenciosamente como `{}` (pérdida de datos sin error). Solo bigint lanza. Un fallback por excepción cubre bigint pero NO Set/Map; para esos hay que pasar el serializer explícito.

**La lección - el humano manda sobre el bot:**
- CodeRabbit empujaba al search serializer (la dirección que schiller-manuel rechazó en #7818). El humano pidió lo contrario: configurable opt-in. Seguí al humano, no al bot. El bot es un filtro técnico, no la autoridad de diseño.
- PERO: los hallazgos técnicos del bot (colisión, default que revienta con bigint) eran reales y valió la pena arreglarlos. Leer el review técnicamente, no descartarlo ni aceptarlo ciego.

**La lección - backticks en `gh pr comment` vía shell:**
- zsh interpreta los backticks como command substitution. `gh pr comment --body "texto con \`code\`"` ejecuta el contenido entre backticks como comando y lo reemplaza, corrompiendo el comentario.
- Fix: escribir el body en un archivo y pasarlo con `gh api ... -f body="$(cat archivo)"`, o escapar los backticks. Verificar el comentario publicado después (no confiar en que quedó bien).

**Self-reflection:**
- CONTEXT: redirección de PR OSS + respuesta a review de bot
- REFLECTION: el major de CodeRabbit era un bug real de diseño del serializer que yo no había visto. Y el comentario de respuesta se corrompió por backticks en el shell.
- LESSON: (1) al diseñar serializers para hashes, taggear tipos y escapar colisiones; (2) el humano define la dirección, el bot aporta hallazgos técnicos válidos; (3) nunca pasar backticks crudos a `gh pr comment` por shell.
- BIASES DETECTED: confirmation (asumí que el serializer era correcto porque los tests pasaban, sin pensar en colisiones entre tipos distintos).

**Tags:** Serializers de hash: colisión de tipos es un bug real (y el humano manda sobre el bot)

---

## 2026-08-22 - Em dash se me escapa en textos largos en ingles (error recurrente)

**Context:** Gonzo me marcó que usé un guion largo (em dash, U+2014) en el body del PR #5344 de astryx y lo corrigió manualmente. Escaneé todo lo publicado ese dia: meti em dashes en 2 bodies de PR (#5344 y #4605) aunque mis comments de issues quedaron limpios.

**Root cause:** el em dash es idiomatico en ingles (separador natural entre clausulas), y cuando escribo bodies/comments largos en ingles se me escapa, aunque la regla "guion comun (-) SIEMPRE" este en USER.md y MEMORY.md. La regla escrita no era suficiente para prevenir el error.

**Fix sistemico (no solo correctivo):**
- Script de verificacion `scripts/check_em_dash.py`: detecta em dash (U+2014) y en dash (U+2013) con contexto de linea. Uso: `cat texto | python3 scripts/check_em_dash.py -` (stdin) o pasando un archivo/directorio. Exit 0 = limpio, 1 = encontro guiones largos.
- Regla operativa en AGENTS.md (seccion "Commits - Reglas de oro"): antes de publicar CUALQUIER texto a GitHub (PR body, comment, issue), escanear con el script. NO publicar hasta que diga "OK: sin guiones largos".
- MEMORY.md: entrada reforzada con el mecanismo obligatorio.

**Lesson:** una regla escrita en memoria no es suficiente para prevenir un error que reaparece. Hace falta un MECANISMO de verificacion automatizado en el flujo (un guard) que se ejecute antes de la accion riesgosa, no solo una nota. Ademas, el em dash es un caso clasico de "el modelo sigue la idiomatica del idioma de salida" - el output en ingles trae patrones de puntuacion ingleses, hay que forzar el override explicito.

**Self-reflection:**
- CONTEXT: correccion de Gonzo sobre escritura en GitHub
- REFLECTION: la regla existia pero no la aplique al escribir bodies de PR en ingles - el em dash es idiomatico en ingles y se me escapo.
- LESSON: escribir el guard automatizado (check_em_dash.py) y correrlo SIEMPRE antes de publicar a GitHub.
- BIASES DETECTED: ninguno relevante - fue falta de mecanismo, no sesgo cognitivo.

**Tags:** Em dash se me escapa en textos largos en ingles (error recurrente)

---

## 2026-08-22 - Triage de PRs OSS: leer TODOS los comments (inline incluidos) y usar la Search API

**Context:** Sesión de limpieza de PRs de terceros (bajamos de 33 a 19 abiertos). Dos errores de infraestructura y uno de juicio.

**Error de infraestructura (gh):** `gh pr list --author gonzoblasco` SIN `--repo` devuelve `[]` vacío - el flag `--author` sin un repo concreto no itera sobre los repos del usuario. No es un mal uso conceptual (ya documentado 20/08), es un comportamiento de la CLI. **Fix:** usar la GitHub Search API (`gh api "search/issues?q=author:gonzoblasco+is:pr+is:open&per_page=100"`) o `skills/github/scripts/pr-batch-check.sh --mine-only`. Documentado en MEMORY.md y skills/github/SKILL.md.

**Error de juicio (clasificación):** mi primer análisis clasificó PRs sin leer los comentarios inline de código ni las reviews:
- **TanStack/router #7834** parecía "empujable" pero el maintainer schiller-manuel ya lo había rechazado as-is ("too niche, bundlesize impact not warranted"). Gonzalo ya estaba haciendo un rework configurable.
- **payload #17413**: parecía "esperando reviewer" pero el inline comment de sviat-barbutsa ya estaba resuelto ("Thank you! Glad I could help").

**Regla:** antes de empujar/cerrar un PR de terceros, revisar `comments` + `inline comments` (`gh api repos/OWNER/REPO/pulls/N/comments`) + `reviews` (`--json reviews`). El feedback real del maintainer vive en los inline comments y reviews, no solo en los comments generales.

**Self-reflection:**
- CONTEXT: triage masivo de PRs OSS (33 → 19)
- REFLECTION: arranqué con `gh pr list --author` que devolvió vacío y perdí ~10 tools en debuguear el JSON vacío en vez de cambiar rápido a la Search API. Además clasifiqué PRs por estado superficial (mergeable/reviewDecision) sin leer el contenido de los comments inline, lo que me llevó a recomendar empujar un PR que el maintainer ya había rechazado.
- LESSON: (1) para listar MIS PRs usar SIEMPRE la Search API, no `gh pr list --author` a secas; (2) el triage de PRs requiere leer TODOS los comments (inline + reviews), no solo los generales; (3) verificar contra la fuente real (main del repo) antes de force-pushear rebases de PRs viejos - el astryx#4298 parecía aprobado pero main ya lo había absorbido via #4157/#5034.
- BIASES DETECTED: anchoring (me anclé en `gh pr list --author`), sunk cost (seguí debugueando el JSON vacío en vez de pivotar), y confirmation (quería ver el PR aprobado como empujable sin leer los comments del maintainer).

---

**Tags:** Triage de PRs OSS: leer TODOS los comments (inline incluidos) y usar la Search API

---

## Colaborar OSS NO es abrir PRs: sumar sin pisar y leer el link completo

**Context:** Sesion de updates OSS. Gonzo me corrigio un sesgo de fondo: no siempre hacemos PRs. Al analizar hermes-agent #38072 (issue de a11y abierto donde Gonzo se ofrecio a trabajar 05/08 sin respuesta, y elchic00 reclamo el finding #3 el 24/08 con PR en curso), mi instinto fue "que finding me tomo para hacer un PR". Eso es competir, no colaborar.

**Lesson - colaborar en un repo ajeno NO es sinonimo de abrir un PR:**
- La mayoria de las veces el valor esta en comentar, revisar, criticar con sustancia, o ayudar a destrabar algo - no en abrir un PR. Regla dura de Gonzo.
- Si otro contribuidor ya reclamo un finding o tiene un PR en curso, abrir otro PR para lo mismo es pisarle el trabajo, no colaborar. Sumar sin pisar: comentar apoyando, ofrecer review del PR ajeno, senalar que findings siguen vivos, criticar con sustancia.
- Antes de proponer "hacer un PR", preguntar: (1) hay trabajo en curso en esto? (2) que aporta Gonzo sin duplicar/pisar? (3) el valor es un PR, o un comentario/review/critica que posicione?
- Ejemplo aplicado: en hermes-agent #38072, Gonzo aporto un re-audit contra main actual (verificando que findings siguen vivos y cuales se mitigaron tras la refactor a tree/renderer/) - valor colaborativo real sin abrir PR, y validando la direccion de fix de elchic00.

**Lesson - leer SIEMPRE el link completo del issue/PR antes de registrar o proponer accion:**
- Body, todos los reviews, todos los comentarios (incluidos bots), files, estado. Comprender la totalidad antes de registrar. Registrar los cambios sean para un lado u otro (merged, closed, follow-up, trabajo ajeno en curso).
- Ejemplo: el PR astryx #4914 tenia un review sustancial de cixzhang con 5 findings y un follow-up sugerido (second deepen) que no se veia en el primer comentario; el issue hermes #38072 tenia la historia de que elchic00 ya habia reclamado el #3.

**Self-reflection:**
- CONTEXT: sesion de updates OSS (5 updates de gh)
- REFLECTION: mi sesgo default es "proponer un PR" cuando veo un issue con trabajo disponible. Gonzo me corrigio: la mayoria de las veces el valor OSS es colaborativo (comentario, review, critica), no competitivo (PR).
- LESSON: separar "colaborar" de "abrir PR". Antes de proponer un PR, chequear trabajo en curso y que aporta sin duplicar. Leer el link completo siempre.
- BIASES DETECTED: action bias (querer "hacer algo" tangible como un PR en vez del aporte colaborativo correcto) + confirmation (asumi que el valor era el PR sin considerar el contexto de trabajo ajeno).

**Tags:** OSS: colaborar no es abrir PRs, leer link completo

---

## 2026-08-25 - Elegir issue para demo en vivo con reclutador

OSS: bug acotado + fix canonico + reproduccion armada

---

## 2026-08-26 - Reviewer humano que usa AI: tratarlo como humano

Ciclo de review completo del PR astryx #5493 (TreeList a11y). El reviewer (cixzhang) usa AI para responder - sus reviews salen con "[Reviewed by Robohands]", pero son de un humano (CONTRIBUTOR) que dicta la sustancia. Hubo 3 reviews: 2 CHANGES_REQUESTED + 1 APPROVED, merge el mismo dia. Lesson: un reviewer humano con asistencia de AI se trata como humano, no como bot: se le agradece el review con su nombre ("Thanks for the review, cixzhang") - la regla de no agradecer a bots aplica SOLO a reviews de IA puros (sin humano detras). Correccion de Gonzo (2 veces): el primer borrador no agradecia ni nombraba al reviewer. Al detectar que es humano detras de la herramienta, el trato es humano. No dar vueltas cuando el maintainer ya valido la direccion: acotar el PR y ejecutar, no ofrecer happy to iterate. Self-reflection: asumi que un review firmado "[Reviewed by Robohands]" era de bot y omiti el agradecimiento. Gonzo me corrigio: cixzhang es humano aunque use AI para responder (como el mismo Gonzo). El agradecimiento con nombre era lo correcto. LESSON: no inferir es un bot por la firma de la herramienta. Si detras hay un humano (CONTRIBUTOR/maintainer que dicta la sustancia), tratarlo como humano: agradecer, nombrar, ser directo. BIASES DETECTED: pattern matching superficial (firma de bot = tratar como bot) - no distinguir entre revisado por herramienta AI y autor humano.

**Tags:** OSS: reviewer humano con AI, agradecer con nombre

---

## No editar el body de un PR para limpiarlo: la historia importa

Ciclo del PR astryx #4022 (WCAG contrast fix). El reviewer (cixzhang) pidio CHANGES_REQUESTED: quitar los scripts de auditoria y dejar solo el cambio de token. Al ejecutar, edite el body del PR para quitar las referencias a los scripts y dejarlo consistente con el estado final. Gonzo me corrigio: el body del PR es parte de la historia del PR - documenta el que y el porque del cambio, y la evolucion (que se propuso, que se acoto tras el review). Al editarlo borre el rastro de las decisiones. Lesson: el body del PR es un documento vivo, no un snapshot del estado final. No editar el body para que quede limpio o consistente con el estado actual. La forma correcta de responder a un review que pide cambios: dejar el body como esta (o actualizarlo minimamente) y comentar abajo en el PR confirmando que se hizo lo pedido. La historia del PR vive en el body + los comentarios del review. Matiz: si el maintainer/reviewer pide EXPLICITAMENTE limpiar el body, entonces SI se edita - es un pedido directo del reviewer, no una iniciativa propia. Distinguir: edicion pedida por el reviewer = ok; edicion auto-iniciada por consistencia = no.

**Tags:** OSS, body de PR, historia del PR, responder review

---

## Chequear si un issue ya esta ASIGNADO antes de abrir PR (astryx #4022)

PR #4022 (WCAG 2.1 AA contrast en --color-border-emphasized) fue CERRADO por ownership, no por calidad. Aprobado 2x por cixzhang (27/08) tras limpiar scripts + regenerar tokens.doc.mjs, todo en verde. Motivo del cierre: el issue #3654 ya estaba ASIGNADO a @rubyycheung y hay un programa coordinado (#4475) de contrast de color-tokens con ownership de a11y + design. 'Parallel implementation PRs' no son bienvenidos. LECCION: antes de abrir un PR en astryx (y en general), chequear si el issue ya esta ASIGNADO (no solo abierto) - pisar ownership ya reclamado es contraproducente aunque el trabajo sea tecnico y solido. El audit y la metodologia quedaron documentados en la conversacion, pero el PR no mergeo.

**Tags:** oss,astryx,ownership,contrast,wcag

---

## Gonzo compartio link de cierre de carbon #16031; Kanam lo trato como novedad sin chequear memoria (participamos el dia previo) y sin leer el hilo completo. Segunda vez que ocurre.

Antes de responder cualquier URL de issue/PR: (1) chequear contexto interno con memory_search + sessions_search por numero de issue, (2) leer el hilo externo completo (body, todos los comentarios, reviews, inline, estado), (3) contextualizar con nuestro rol si participamos. Regla codificada en CONTRIBUTING.md + AGENTS.md paso 0 + AGENTS-DETALLE.md regla 1.

**Tags:** oss,reflexion-post-tarea

---

## Verificar diff real antes de afirmar que un PR resolvio un issue (anchoring)

Antes de afirmar que un PR 'resolvio parte de un issue', leer files+diff reales: el nombre del PR (doctor, plain text) puede colgar de otra superficie (gateway daemon, UI web) sin tocar la barrera reportada. Caso: #129954 y #131427 en openclaw/openclaw parecian cubrir el #126876 por nombre, pero ninguno toca el terminal del usuario. Anchoring: queria confirmar el claim inicial, no refutarlo.

**Tags:** anchoring,oss-review,verificacion

---

## El cierre de un hilo que salio bien ES el resultado, no un problema a gestionar

Cuando un hilo de OSS cierra bien (el autor recibio aporte, lo integro, y cerro el mismo), el cierre es el desenlace - no un problema de triage para resolver ni una oportunidad de seguir aportando. Distinguir: Gonzo comparte la evolucion de un hilo como INFORMACION (como ayudo nuestro comentario) vs como pedido de accion. Bias detectado: querer ser util tocando algo mas en cada turno - a veces el mejor output es no hacer nada mas. No somos nadie en repos ajenos: no validar decisiones de cierre de quien reporto, el autor estudio el tema mejor que nosotros.

**Tags:** bias,oss,boundaries,cierre-hilos

---

## Cambio en helper compartido: grepear consumidores por simbolo Y por asercion, no solo el archivo editado

Al cambiar comportamiento en un helper compartido (hook/effect/util que otros componentes consumen), el archivo de test del componente que tocaste no alcanza: hay que buscar en TODO el repo los hermanos que consumen el mismo helper y actualizarlos en el mismo commit.

Caso #10503 (adobe/react-spectrum, react-aria useComboBox): se gateo el announcement effect a solo cambios de seccion. Se actualizaron los tests de ComboBox.test.js, pero SearchAutocomplete usa useComboBox internamente y sus tests seguian asertando el comportamiento viejo (per-item announce). CI quedo rojo con 4 jobs test FAILURE. Mismo patron ya habia pasado en el commit del 02/09 (mismo archivo, mismo motivo) - o sea que no era un descuido aislado: era un metodo incompleto que se repitio.

Como encontrarlo rapido: grep por el nombre del helper/simbolo en packages/*/test/ (los consumers no siempre estan en el mismo paquete) y por las aserciones tipicas del comportamiento viejo (toHaveBeenLastCalledWith('One'), toHaveBeenCalledTimes(N), NthCalledWith). En este repo: grep -rn "announce" --include="*.test.js" packages/ habria mostrado los dos archivos de una.

Regla: antes de pushear un cambio de comportamiento en algo compartido, grepear consumidores por simbolo Y por asercion, no solo por el archivo que editaste. Y si el fix pasa por un test, correr la suite del vecindario, no solo el archivo propio. Reproducir el fallo en local ANTES de tocar: el error da el archivo y la linea exactos.

**Tags:** oss,ci,tests,react-spectrum,consumers,regresion

---

