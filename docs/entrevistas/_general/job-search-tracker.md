# Job Search Tracker

> **Estado 2026-11-16: 3 procesos vivos.** Infjini/Disney (entrevista pendiente, **fecha sin coordinar**), Mercor/Project Odin (form completo, falta postular) y TEAM International (relación viva, posición cerrada). Lo que falta de Disney no es una respuesta a un rechazo: es que **todavía no se coordinó la entrevista**. Gonzo, 16/11: *"No dije nunca hubo noticias. Digo que aún no coordinamos la entrevista con Disney."*
>
> **Estado 2026-10-28: 3 procesos vivos (Mercor/Project Odin nuevo, Infjini/Disney con entrevista en noviembre, TEAM International con reevaluación prometida).** Los 5 contactos recontactados por el filtro de inglés respondieron (5/5); **solo uno tiene fecha concreta** (la entrevista de Disney). Staffy/Pfizer **cerrado 20/10** y Sol Bisio **cerrado 21/10**, ambos por el filtro de inglés C1 conversacional. **TEAM: la posición de Tempo CERRÓ 26/10, pero la relación con TEAM NO** - David mantiene el perfil en el talent pool y reevalúa cuando mejore el inglés. **Infjini: DISNEY ENTREVISTA EN NOVIEMBRE** (1ra o 2da semana, confirmada por Siraj el 26/10) - el idioma dejó de bloquear la presentación y pasó a ser el riesgo de la entrevista misma. **Plan de inglés: B2+ intensivo en el CUI, dos meses, martes y jueves de 10 a 13 h por Zoom (desde el 27/10 hasta el 22/12)** - desoxidar y mejorar la base; el examen CUI-ING C1 y el TOEFL quedan para después.
>
> **Mercor/Project Odin (28/10): AO EXCEPCIÓN A LA REGLA DE RITMO.** No salió del radar ni de un postulado: entró por un **mail directo** de Chloe Chee (Growth team de Mercor, persona verificada) y Gonzo se anotó en el formulario de interés ese mismo día. Es el único proceso con **entrevista con IA de 3 minutos** en vez de con recruiter humano, y el único cuyo pago **depende del inglés hablado** en el momento exacto. Por eso va aparte, con su propia carpeta: `docs/entrevistas/mercor-project-odin/`.
>
> Regla de trabajo: cualquier proceso con +10 días sin respuesta humana real se cierra. Energía de follow-up: solo si ellos escriben. No se insiste más de una vez por proceso.

## Mercor - Project Odin (Software Developers, Must own MacBook) - INICIADO 28/10/2026

> **Entrada por mail directo, verificada.** No es una postulación de radar: es una invitación de Growth.
> Veredicto de veracidad del mail: **legitimo con reservas** (persona real, proyecto real, form real y
> sin pedir datos peligrosos; pero el link de confirmacion no esta linkeado desde ningun sitio oficial
> y el SPF de mercor.com solo autoriza Google aunque Mercor usa SES desde mail.mercor.com).
> **Por eso la postulacion va por `work.mercor.com`, no por el link del mail.**

| Empresa | Puesto | Ubicacion | Canal | Riesgo #1 | Estado |
|---|---|---|---|---|---|
| **Mercor** | Software Developers (Must own MacBook) - Project Odin | Remoto global, **Argentina soportada** (Stripe Connect) | `work.mercor.com` → Explore → Apply Now | **Ingles B2+ hablado vs "excellent verbal communication" del JD**, en una **entrevista con IA de 3 minutos**. Es el gap que define el resultado. | **MAIL RECIBIDO Y FORM COMPLETADO 28/10** (Gonzo). **CV LISTO: markdown + DOCX + PDF en `docs/entrevistas/mercor-project-odin/` (2 paginas, texto extraible, gate OK).** Falta: crear cuenta en `work.mercor.com` con `gonzoblasco@gmail.com`, subir el PDF, tomar la Practice Interview y postular al listing. |

**El CV paso por el pipeline A/B completo (ADR-077):** A redactó (STUDIO, gpt-oss:120b), B reviso adversarial
(CRITIC, deepseek-v4.1-flash) y el CORE aplico los fixes. **Lo que B encontro y el gate NO caza** (el gate
solo compara contra el corpus; no mideAgainst el JD ni el ATS):
- **Las PRs iban en tabla markdown**, y Mercor prohibe explicitamente tablas en la subida ("avoid images, tables,
  or complex designs"). Ahora son bullets.
- **35 guiones U+2011 (non-breaking hyphen) y 35 U+202F (narrow no-break space)**: el ATS busca "multi-tenant"
  con guion ASCII y no matcheaba. Normalizados.
- **`---` renderizado como parrafo visible** en el PDF. Eliminado.
- **"Lead accessibility"** (presente) por un rol terminado: corregido a "Led".
- **El Summary ponia "macOS" y "narrating" como tesis** sin sostenerlas con un hecho, y repetia "macOS" dos
  veces en la misma oracion (lectura de keyword stuffing). Reescrito.
- **"Managed a team of 3"** por "Led" (el corpus dice *lidero*), y "financial-insights" por "financial intelligence".
- **El design system propio de SoporteML no estaba nombrado** (el corpus lo registra: tokens semanticos, mapa
  token→componente, WCAG AA como criterio del sistema). Agregado.
- **El CV cerraba con la limitacion** ("spoken English is my current development area") y ahora cierra con la
  evidencia escrita + el curso, sin cambiar el nivel declarado.
- **El keyword map minimizaba la posicion propia**: decompensado por "2-3 years" a "10+ years vs. los 2-3 que
  pide el JD".

**El gate NO es suficiente para un CV de US:** pasa, y aun asi el CV era/subible. El gate compara contra el
corpus; no mide contra el JD, ni contra las guidelines de subida de Mercor, ni contra el parseo del ATS. Para
un posting a US, **el veredicto real es el del revisor B + las verificaciones propias del CORE** (pdftotext,
pdfinfo, grep de unicode y de tablas).

**Dos hallazgos de hardware que cambian el plan:**
- **La entrevista es en la MacBook Air M2, NO en el Mac mini.** El Mac mini (Mac16,10, M4) **no tiene camara ni
  microfono** (`SPCameraDataType` vacio; `SPAudioDataType` solo lista salidas). El nodo de OpenClaw del Mac mini
  tambien reporta `camera: false`, `microphone: false`. Sin eso no hay entrevista: la IA te ve y te escucha.
- **La app de tracking es Workpuls** (antes Insightful), NO esta instalada. Requisito macOS 11+ (tenes 27.2).
  Solo hace falta con contrato activo; la asignacion de proyecto tarda 12-24 h. **Toma screenshots periodicos de
  la pantalla mientras el timer corre**: es parte del modelo del proyecto, pero conviene saberlo antes de
  clockear con material de clientes abierto.

**El email de la cuenta es `gonzoblasco@gmail.com`** (ahi llego la invitacion y el formulario lo pedia), pero
**el CV va con `gonzoblasco@icloud.com`**: es el dueno del dato de contacto en el corpus (`contact_email`) y el
gate lo exige. Las otras tres postulaciones vivas (Mural, Mercado Pago, RYZ) ya van con icloud.

**Pendiente de definicion con Gonzo (no bloquea):** el hueco de **9 meses entre 11/2019 (Minutentag) y 08/2020
(Super7UI)**. El corpus no lo registra, asi que el CV no lo inventa (ADR-101). La respuesta de una frase para la
repregunta ya esta en el pack de entrevista (T7). Si ese periodo tuvo trabajo real, el hecho va al corpus
primero y despues al CV.

**Por que este listing y no los otros dos de Odin:** hay tres ("Computer Power Users and Automation
Builders", "Software Developers (Must own MacBook)", "STEM Researchers - MSc/PhD"), todos a $50-60/hr
con el mismo requisito de hardware. Se elige **Software Developers** porque:
- el corpus no registra Shortcuts, AppleScript, Raycast, Alfred, Keyboard Maestro, Automator, Zapier ni
  Make (cero menciones en `memory/career-facts.md`): el listing de "Computer Power Users" pide
  **"experience building automations with tools such as..."** y eso no lo puede respaldar;
- el listing de "STEM Researchers" exige **MSc/PhD en curso o conseguido** - no aplica (corpus §3);
- "Software Developers" pide **"2-3 years of professional coding experience"** (rama que se cumple) +
  herramientas de desarrollo de macOS (VS Code, Terminal, Git, package managers: todo verificado en
  uso real) + "ability to clearly explain your reasoning while you work" (que es literalmente lo que
  el corpus sostiene).

**Lo que el corpus no tiene y el JD pide:** "Bachelors from a prestigious institution". Ninguna de las
cuatro universidades se completo (corpus §3). Se cumple por la rama de los 2-3 anos de experiencia y se
declara `Universidad de Palermo - Ingenieria en Informatica (2001-2002, incomplete)`. Gap declarado, no
oculto.

**La app de tracking es Workpuls** (antes Insightful), NO esta instalada. Requisito macOS 11+ (tenes
27.2). Solo hace falta cuando hay contrato activo; la asignacion de proyecto tarda 12-24 h. **Ojo:
toma screenshots periodicos de la pantalla mientras el timer corre** - es parte del modelo de trabajo
del proyecto, pero conviene saberlo antes de clockear con material de clientes abierto.

**Proceso de la postulacion (documentado en la carpeta del proceso):**
`docs/entrevistas/mercor-project-odin/brief.md` (brief de redaccion) ·
`docs/entrevistas/mercor-project-odin/pack-entrevista.md` (pack de preparacion para la AI interview) ·
`docs/entrevistas/mercor-project-odin/cv-mercor-software-developer.md` (el CV, en armado)

## Radar 2026-10-25 - 43 candidatos, 32 verificados contra el posting real

> **Decision de Gonzo (2026-10-27): NO se postula a mas puestos desde esta tanda.** El
> radar se deja como esta, con los tres candidatos verificados, para cuando vuelva el
> momento. No es un cierre de los procesos: los que ya se postaron (Mural, Mercado Pago,
> RYZ) siguen su curso con el tracker como fuente. Es una decision de ritmo, no de umbral.
> Lo que queda abierto y en manos de Gonzo: el hCaptcha de RYZ (sale en Safari sin tocar
> nada) y las tres respuestas abiertas de XBOW.


> Barrido con `find-jobs.mjs` (5 fuentes: LinkedIn guest API, remotive, arbeitnow,
> jobicy, himalayas) + la API de MeLi (866 vacantes). Cada candidato se leyo contra su
> posting real para separar **empresa de producto** de **nearshore-agency**: la regla sale
> de la evidencia del 22-10 (los dos cierres por C1 fueron en agencies, donde el idioma
> es filtro de elegibilidad; en producto es ruido de fondo).

| Empresa | Puesto | Ubicacion | Canal | Riesgo #1 | Estado |
|---|---|---|---|---|---|
| **Backblaze** | AI Workflow Engineer \| LATAM | Remote Argentina (tambien CO/CR/MX) | Greenhouse `job-boards.greenhouse.io/backblaze/jobs/5287532008` | **Idioma: NO declarado en el posting** (0 menciones). El rol pide construir workflows con IA, prompt layers, agentes livianos, RAG e integraciones: encaja con el AI Engineering OS | **CANDIDATO #1.** Producto real: IPO en Nasdaq, 500K+ clientes, 175+ paises. Es el puesto que mejor calza con el perfil "AI-native" del corpus |
| **XBOW** | Software Engineer - AI Systems | **Remote Argentina** (confirmado en `secondaryLocations`) | Ashby `jobs.ashbyhq.com/xbowcareers/304f9f4e-.../application` | **Idioma: no declarado.** El posting pide prompting, orquestacion y TypeScript en produccion | **CANDIDATO #2.** Producto real: fundada por el creador de GitHub Copilot, respaldada por Sequoia. Yahoo un bounty de #1 en HackerOne. **Sin rango salarial publicado** |
| Prex | Software Engineer - AI Solutions | Argentina | A confirmar (carreras SPA) | Pedir Rust + Python, MCP, agentes autonomos con sandboxing | **Candidato #3.** Fintech con 6M+ usuarios. El JD pide MCP explicitamente y control de agentes autonomos: es el posting que mas calza con el kanam-fixer |
| Medallia | Senior AI Systems Engineer | Buenos Aires | A confirmar | **Es un puesto de IT/automation interna**, no de producto: el angulo del corpus no es el que busca | Descartado por encaje |
| Zaigo | Senior Forward Deployed Engineer, AI Transformation | Argentina (equipo en LATAM, base NY) | A confirmar | **Es agencia/consultoria**: "production engineering inside someone else's company" | Descartado por la regla |
| Oowlish, Proxify, Fusionhit, Talent Connect, EPAM, Nortal, Fullstack, Marvik, AlixPartners | varios | Argentina | varios | **Agencies**: "collaborate with premier clients" / "serve clients" | Descartados |

> **XBOW ya tiene el formulario probado**: el adaptador de Ashby, que antes solo servia
> para Mural, se generalizo (los `name` son UUIDs por puesto, y las opciones de
> autorizacion y patrocinio a veces son BOTONES y no inputs de radio). Verificado
> end-to-end: `ok: true`, 3 campos + 2 opciones + CV.
>
> **XBOW pide tres preguntas abiertas** ("why are you interested", "describe a recent
> project", "how did you hear about us") que necesitan tu voz, no se rellenan solas.

## Vacantes de la tanda 2026-10-22 - las TRES POSTULADAS y CONFIRMADAS

> Busqueda activa (no a proposito de postulaciones). Barrido de a11yjobs, LinkedIn guest API,
> vacantesdigitales, remotive, himalayas, remoteok, jobicy, arbeitnow, getonbrd, landing.jobs y
> boards de Greenhouse/Ashby + 10Pearls, Svitla, Infojini, FullStack, Blacksmith.
> **Hallazgo:** el mercado de accesibilidad activo es casi entero US-only, y los avisos que
> filtran "LATAM" son casi todos el mismo bench de recruiters ya visto (Infojini, E-IT, FullStack:
> el mismo req de Disney/HTC). Lo nuevo son vacantes de front-end con a11y en empresas de producto.
> **Regla operativa que sale del relevamiento:** apuntar a empresas de producto con su propio
> equipo, no a nearshore-agencies que reasignan el tiempo a clientes US. En agencies el idioma es
> un filtro de elegibilidad; en producto es ruido de fondo.

| Empresa | Puesto | Ubicacion | Por que | Riesgo #1 | Estado |
|---|---|---|---|---|---|
| **RYZ Labs** | AI-First Frontend Software Engineer | Remoto US+LATAM | El JD pide "AI coding tools en el flujo de trabajo diario" + design systems + UI polish: es el perfil "AI-native frontend" del corpus | **Idioma conversacional** (el JD no declara nivel) | **POSTULADO 22/10 Y CONFIRMADO** (Lever), enviado desde Safari: **no pidio hCaptcha**. Salario USD 3.200/mes, nivel Upper Intermediate. En paralelo quedo enviada la **invitacion de conexion** a Sonia Langone (recruiter tecnica de RYZ) con nota de 833 caracteres: por que encaja, el AI Engineering OS, el servidor MCP propio, los 11 PRs, y las dos preguntas de screening (overlap con US en EST, y nivel de ingles conversacional). |
| **Mural** | Senior Software Engineer, Growth & Engagement | Argentina | React/TS + ownership end-to-end + experimentos A/B reales (Adobe Target, Minutentag 2019) | **Idioma**: el JD pide feature flags/analytics/event pipelines, que no tenes (declarados como gap en el CV) | **POSTULADO 22/10 Y CONFIRMADO** (Ashby): banner verde "Your application was successfully submitted". Salario USD 3.400/mes, CV + cover letter adjuntos. Captura: `outreach-2026-10-22/evidencia/mural-form-filled-submitted.png` |
| **Mercado Pago (ML)** | UX Expert - Software | Buenos Aires, hibrido | Diseno↔ingenieria (revision de disenos antes de implementar + requisitos con guia de codigo, en EY) + design system propio + SoporteML (CRM para vendedores de MeLi, el mismo dominio) | **No es el idioma: es que el puesto es mas de diseno que de ingenieria** | **POSTULADO 22/10 Y CONFIRMADO** (Eightfold): "¡Gracias por su solicitud, Gonzalo!" + `201 success: true` del servidor. Salario no aplica (el ATS de MeLi no lo pide). Captura: `outreach-2026-10-22/evidencia/meli-form-filled-submitted.png` |

**El mensaje de idioma NO aplica a los tres por igual:** en RYZ y Mural va al final del primer
mensaje (el filtro de Staffy/Sol se filtro tarde y caro). En Mercado Pago no se pregunta: es un
puesto local, con equipos locales, y la pregunta proyectaria una duda que no hace falta.

**Gaps declarados, no escondidos:** los tres CVs traen una seccion "Notes / gaps" con lo que el
JD pide y no se cubre. En Mural eso es deliberado: un gap declarado se discute, un gap callado se
descubre tarde. En el archivo que se posta esas secciones quedan excluidas (el CV son 2 paginas,
no 3); el mapa completo esta en el `.md` fuente.

**Estado 2026-10-23 (CIERRE DE LA TANDA): los TRES POSTULADOS y CONFIRMADOS.** Mural ("Your application was successfully submitted"), Mercado Pago ("Gracias por su solicitud, Gonzalo!" + 201 success) y RYZ Labs (enviado desde Safari, sin hCaptcha). Ademas quedo enviada la invitacion de conexion a la recruiter de RYZ, que abre la conversacion con las dos preguntas de screening.

**Lo que costo la tanda: el hCaptcha de Lever no lo puede resolver un navegador automatizado, y el problema lo causo el propio intento de automatizarlo.** El token daba 0 en Chrome de Playwright (`navigator.webdriver: true`) y en el perfil `imported` de OpenClaw (`--headless=new`, "HeadlessChrome" en el User-Agent). En Safari, sin tocar el captcha, salio el envio directo. La leccion: ante un captcha, la unica via es cambiar de navegador, no insistir con el mismo.

**CVs de apoyo (sin preparar):** Bluelight (React Engineer, Remote LATAM, 23/09), Makai Labs
(Senior Next.js, 29/09), Nortal (Lead Frontend React, WFH, 09/10), Google (Senior Frontend
Remoto LATAM - pide "ingles avanzado" explicito: es un test del filtro, no una opcion segura).
Descartados: GraceMark (pide 10+ anos y es 100% remote within Mexico), FOURSYS (QA de a11y, te
encasilla en testing), Blacksmith (pide portfolio de diseno en Figma), Speria y Profound (diseno,
no ingenieria), Infojini (ya es tu proceso vivo).

## EFISAT (efisat.com.ar) - outreach directo a Agustín Bermúdez (fundador) - 15/11/2026

> **No es un puesto ni una postulación.** Es un cold outreach a la empresa (20+ años, 500+ clientes,
> 10K+ vehículos monitoreados; gestión de flotas, telemetría, recaudación, apps para transporte de
> pasajeros). Se llega por el padre de Gonzalo, que es el contacto. Por eso el mensaje va en
> **español** y el tono es de presentación, no de búsqueda.

| Empresa | Puesto | Contacto | Canal | Riesgo #1 | Estado |
|---|---|---|---|---|---|
| **EFISAT** | Sin puesto definido (desarrollador full stack / sistemas de gestión) | **Agustín Bermúdez**, fundador (vía el padre de Gonzalo) | WhatsApp o email, referido | **No hay vacante**: el mensaje compite contra la percepción de "me mandan CVs". Se gana con un gancho de dominio (unificar fuentes de datos, automatizar sin perder control) y una salida de 20 minutos. | **MATERIAL LISTO 15/11**, no enviado. `docs/entrevistas/efisat-cold-outreach/`: `cv-efisat.md` (verdad), `Gonzalo_Blasco_CV_EFISAT.docx` y `.pdf` (2 páginas), `mensaje.md` (borrador WhatsApp + email). |

**Decisiones de esta versión (15/11):** sin título de ingeniero (Gonzo no está recibido: regla nueva en
`memory/career-facts.md` §7-bis), liderazgos en tono bajo, sin carreras universitarias en Formación, y
las contribuciones OSS **dentro del CV** (11 PRs agrupados por familia + 7 hilos de revisión), porque es
la prueba más difícil de refutar que tiene para mostrar a un fundador.

## Procesos activos

| Empresa | Puesto | Contacto | Tarifa | Estado 2026-10-21 |
|---|---|---|---|---|
| **TEAM International** (cliente **tempo.io**) | Senior Frontend Developer (Growth) | David Sanin Valencia | USD 5.000/mes fijos (≈ USD 31,25/h a 160 h) | **POSICIÓN DE TEMPO CERRADA 26/10; LA RELACIÓN CON TEAM SIGUE VIVA.** El Delivery Manager de Tempo pidió más nivel de inglés: **el equipo del cliente que entrevista y trabaja con la persona está en Europa**, y es exigente con la fluidez **al discutir y explicar temas técnicos**. David: *"no avanzar con tu perfil para esta posición en particular"*; el nivel técnico *"es muy bueno"* y la decisión es de idioma. **Lo mantiene en el talent pool** y reevalúa cuando Gonzo esté más cómodo con el idioma. **Dos capas, dos estados: Tempo cierra la posición; TEAM mantiene la relación y la vía de reevaluación (1-2 meses).** Antes: el perfil técnico le gustó ("le encanta mi perfil"), el bloqueo fue el **nivel de inglés conversacional**, y David había aceptado en dos vías (hablar con Tempo, o reevaluación para ese u otro proyecto). **El JD dice B2+ y el requisito real es C1**: en una agency el idioma es **condición de elegibilidad**, no requisito del rol. **Dato nuevo y relevante: el equipo del cliente está en Europa, no en US** - por eso el tracker necesita la regla ampliada. Referencia temporal: el B2 intensivo del CUI termina el 21-23/12/2026. Análisis fiscal (de la oferta que no prosperó): **neto ≈ USD 4.140-4.270/mes**. Detalle: `docs/entrevistas/team-international-tempo/entrevista-26-10-y-seguimiento.md`. |
| **Infjini Inc** (cadena **Disney -> HTC -> Infojini**) | Lead Software Engineer - Digital Accessibility | Siraj Shaik | **USD 24/h** all-inclusive (piso era 22; Gonzo pidió 25 y aceptó 24 el 19/10), 1 año **ABIERTO — FECHA SIN COORDINAR.** Screening hecho (19/10) con feedback técnico positivo (*"technically you are excellent"*), **RTR firmado el 19/10 a USD 24/h**, y el único feedback negativo fue **fluidez en inglés hablado** (no escrita). El 26/10 Siraj confirmó que Disney entrevista en la 1ra o 2da semana de noviembre; **al 16/11 la fecha concreta todavía no se coordinó**. No hubo rechazo ni cierre: falta que se agende. Pendientes: coordinar fecha y formato, y el gate de "relevant regional certification" (la JD lo lista en Required; Siraj lo chequeaba con su manager el 19/10 y no hay respuesta registrada). |

### Interna.work (2026-11-06) - FUNNEL DE BENCHMARK LABOR, NO ES UN PROCESO

Mail inbound de `recruiter@ses.interna.software` ("Alex Reed | Lead Talent Partner @ Interna.work"):
Frontend / UI Engineer, USD 80-100/h "benchmark equivalent", ~USD 640-800 **por entregable aprobado**,
~8 h por tarea. El trabajo descrito no es construir UI: es convertir mockups en **benchmarks de codigo
con tests objetivos**, o sea produccion de datos de evaluacion.

Verificado el 2026-11-06:

- `ses.interna.software` **no tiene registros DNS** (A, MX ni TXT), asi que la direccion del remitente
  no puede recibir. El canal real es `talents@interna.work` (apex con MX Zoho).
- `interna.work` registrado **2026-02-19**, registrar Spaceship, registrante US. Landing unica en
  Next.js: sin vacantes, sin entidad legal, sin direccion, sin equipo.
- `preflight-a11y` (el repo que citan como descubrimiento) se creo el **04/11** y tiene **0 estrellas**:
  el "vimos tu trabajo" es un scraper de actividad reciente de GitHub.
- La privacy policy promete que el codigo del candidato no entrena modelos, mientras el trabajo
  ofrecido **es** producir benchmarks: el benchmark es el producto.

**Decision de Gonzo:** responder igual, porque contestar un mail sin links ni adjuntos no tiene
riesgo. Se envio el 2026-11-06 11:34 con tres preguntas (cliente y entregable, criterio de aprobacion
y rejection rate, terminos de contrato y rail de pago). Se recorto la pregunta sobre el dominio del
remitente y la linea de "no intake form".

**Criterio de cierre:** el propio sitio promete matching en 24-48 business hours -> **hasta el
2026-11-11**. Silencio, o respuesta con link a formulario, = funnel, cerrado. Solo sigue si responden
con nombre de cliente, criterio de aprobacion escrito, entidad y rail de pago.

### Notas Staffy (2026-10-20) - PROCESO CERRADO

- JD: https://jobs.wearestaffy.com/positions/ai-software-engineer-1976
- **Desenlace (20/10, 17:42 ART):** Julieta propuso call de 30 min para el 21/10 y planteo el nivel de inglés. Al contestarle con honestidad (hablado B2, escrito C1, "a little rusty"), ella confirmó que **C1 conversacional es requisito clave** del rol (entrevista y comunicación diaria con clientes en US y Canadá) y cerró el proceso: *"Given what you've shared about your current speaking level, I think it would be best not to move forward with this opportunity at this stage."* Dejó puerta abierta para oportunidades futuras.
- **Causa raíz:** el filtro de idioma se filtró al final del screening, no al principio. El JD no lo declaraba y el pitch inicial de Julieta no lo mencionaba. Con un puesto de 30-35/h, la pregunta "¿el cliente exige C1 conversacional?" era la que define el proceso, y tenía que llegar antes.
- **Lo que sí se ganó:** contacto con una reclutadora que leyó el CV y dijo "your technical background is very strong". La relación queda para futuros procesos.
- **Aprendizaje reutilizable (ampliado el 26/10 con 4 casos):** para roles LATAM que exigen **comunicación técnica fluida en inglés**, **preguntar por el nivel de inglés requerido en el PRIMER mensaje**. Es la variable que más rápido descarta y la que más caro cuesta descubrir tarde. El filtro de idioma no se negocia con el CV: se negocia con la pregunta. **En los 4 casos, la barra la puso el cliente final, nunca el intermediario** - por eso recontactar al intermediario es lo correcto: es el que puede matchearte contra otro req. **Ojo con la geografia: no predice nada** - el caso de Tempo (equipo del cliente en Europa) exige lo mismo que Pfizer (US) o Disney: fluidez para discutir y explicar temas técnicos. Detalle en `docs/learnings/evaluacion.md`.

### Notas Infjini (2026-10-16) - **ABIERTO**

- Oferta aceptada para avanzar. CV en `docs/entrevistas/infjini-infotech-lead-a11y/`.
- **Estado real (confirmado por Gonzo el 21/10):** el screening con Siraj **ya se hizo** y el proceso **sigue abierto**. Es el único proceso vivo. (El desenlace no había quedado registrado en los dailies: la sesión no se guardó.)
- **Riesgo a vigilar:** es un puesto 9-5 ET con comunicación diaria en inglés, **misma clase que los dos cerrados por el filtro de C1 conversacional** (Staffy y Sol). Si Siraj tiene el mismo criterio, aplica el mismo filtro.
- **Acción sugerida:** en la próxima call, preguntar de entrada el nivel de inglés conversacional que exige el cliente. Es la pregunta de costo cero que más rápido descarta.
- Precedente: es el mismo req que EIT/HTC/Disney (bench amplio). No insistir.

### Infjini - ENTREVISTA CON DISNEY EN NOVIEMBRE (WhatsApp 26/10, 12:30-12:34)

> **Siraj 12:30:58** "We got an update that client is going to conduct interviews in 1st or 2nd week of November."
> **Siraj 12:31:41** "Thank you for working on english."
> **Gonzo 12:32:29** "Hope it's the second week so I'd already had a couple of hours in.."
> **Gonzo 12:33:39** "So I'm still in the run…. Great… Keep me posted…"
> **Siraj 12:34:02** "yes" / 12:34:07 "Yeah!"

**Lo que cambia: el gate de idioma NO bloquea la presentacion.** El cliente (Disney) **va a entrevistar en la 1ra o 2da semana de noviembre**. El idioma dejo de ser condicion para la presentacion y paso a ser el riesgo de la propia entrevista. El proceso deja de ser "espera con condicion" y pasa a ser **"entrevista agendada en ventana cerrada"**.

**ESTADO 2026-11-16: FECHA SIN COORDINAR (no cerrado).** La ventana prometida era la 1ra o 2da semana de noviembre. Al 16/11 **la entrevista todavía no se coordinó**: no hay fecha, no hay formato y no hay feedback nuevo. Gonzo lo precisó ese día: *"Digo que aún no coordinamos la entrevista con Disney."* No es un proceso muerto ni un rechazo — es un agendamiento pendiente. Lo único que se sabe del gap real: el idioma sigue siendo lo que se juega en esa entrevista, y el plan del CUI (hasta el 22/12) sigue siendo la respuesta a ese gap, con o sin Disney.

**Riesgo de timing (el calculo que hay que hacer):**

| Si entrevista en | Fecha | Horas de curso B2 (arrancó 26/10) | Inglés real |
|---|---|---|---|
| 1ra semana | ~2-6/11 | ~1 semana | **B2 de hoy, sin cambio** |
| 2da semana | ~9-13/11 | ~2 semanas | B2 + desoxidacion marginal |

**Conclusión operativa: el curso NO resuelve la entrevista de noviembre.** Con 1-2 semanas no se cambia un nivel oral. La preparación de la entrevista tiene que ser **específica y oral**: mock interviews de a11y en inglés, no curso general. El B2 intensivo del CUI sirve para el plano de fondo (fin de diciembre) y para la reevaluacion de TEAM, no para esto.

**Lectura del mensaje de Gonzo (confirmada por Gonzo, 26/10):** el "yes" de Siraj fue a "hope it's the second week" y el "Yeah!" a "still in the run". La ventana quedo en **la 2da semana de noviembre** segun la lectura de Gonzo, pero **sin confirmacion explicita de Siraj**: el mensaje quedo en ambiguo y la ventana sigue siendo "1ra O 2da" hasta que el invite llegue.

**Decision de Gonzo (26/10): NO re-preguntar lo de la certificacion.** Siraj ya sabe de los examenos: Gonzo lo declaro el 19/10 ("course completion certificates, not IAAP credentials, CPACC next window, certification in January") y Siraj respondio "I am going to check this with my manager". **No se repite ni se invade.** Lo que faltaba en el proceso era el ingles, y eso fue lo unico que se agarro. Queda como dato de que el gate se consulta con el manager, sin gestion activa.

**Pendientes concretos:**
1. **Esperar el invite.** Cuando llegue, se confirma el dia exacto y el formato (duracion, quien entrevista: recruiter de HTC, hiring manager de Disney o cliente final; screen o tecnica). No se insiste antes.
2. **Preparar la entrevista en ingles speaking**, no solo escrita. Las 4 historias ancla: react-spectrum #10503, EY Motif, Warner Bros 200+ violations, liderazgo de equipo de 3.
3. **Dejar asentado por mail** (no solo WhatsApp) la fecha y el formato. El negocio va por mail.

**El plan de ingles de Gonzo para la segunda semana de noviembre (26/10):**
- **B2+ intensivo del CUI (UBA): dos clases de 3 horas por semana (6h/semana), martes y jueves de 10 a 13 h por Zoom**, en curso desde el **27/10** (corregido el mismo día: la inscripción inicial lo había dejado en **B1+** y le cambiaron el ciclo). Para la 2da semana de noviembre (9-13/11) lleva **6 clases**, no 3. **Choque de horario con la ventana de la entrevista:** de las 6 clases contadas, el **10/11 no existe**: es
**feriado en CABA y Córdoba** por la visita del Papa León XIV (Decreto 1103/2026, Boletín Oficial del
28/09/2026; feriados del 8 al 11 de noviembre). En CABA también el **9/11** es feriado nacional y
el **11/11** feriado en Provincia de Buenos Aires. **Clases reales hasta el 13/11: 5** (27/10, 29/10,
3/11, 5/11, 12/11), y **una sola** cae dentro de la ventana de la entrevista: la del **jueves 12/11**.
**No hay que mover nada salvo que la entrevista caiga exactamente ese día;** en ese caso se coordina
con el CUI.
- **Practica conversacional con gente afuera (en un bar), a pedido de su hermana: GRINGO TUESDAYS** (martes 19hs a 3hs, el intercambio de idiomas mas grande de Latam; el reel que compartio es de este grupo). El reel que compartio (instagram.com/reel/Dep4YBruByu/) no se pudo leer: Instagram devuelve el HTML vacio a un fetch sin sesion, asi que el contenido no esta verificado. Las citas clasicas de intercambio de idiomas en Buenos Aires que si se verificaron: **Gringo Tuesdays** (martes 19hs a 3hs, el intercambio mas grande de Latam - **ELECCION DE GONZO**), **Spanglish Exchange BA** (Rabieta bar, Palermo; jueves y viernes 19hs, sabado 20hs; chats rotativos de 5 minutos por idioma, ~2h por sesion), **Mundo Lingo BA** (The Flags Place, 6.552 miembros), **Mate Club de Conversacion** (Rabieta bar, sabados 18hs).
- **Roadmap.sh Pro como material**: curso de a11y (16 lecciones en 4 modulos: focus architecture, ARIA dinamica, verificacion AT cross-platform, operaciones de accesibilidad enterprise) leido **en voz alta**; la Lección 1.1 (focus trap) ya esta al 3/5.
- **Mock interviews en ingles**: es lo que ataca el gap real (explicar decisiones tecnicas en vivo). El curso solo no alcanza.

### Recontacto por inglés a recruiters previos (26/10/2026) - **5 respuestas de 5** (cerrado el 27/10)

Gonzo mandó a las **cinco** personas con las que había hablado y que lo rebotaron por el filtro de
idioma. A Sol en **español** (con ella habló todo en español); a Samarth, Parthasarathy, Siraj y
Julieta en **inglés**.

| Contacto | Proceso | Respuesta |
|---|---|---|
| **Samarth** (Ritz-Carlton) | cerrado 22/09 | **Respondió 26/10: "Sure thing, Gonzalo and All the Best"** |
| **Julieta Costa** (Staffy/Pfizer) | cerrado 20/10 | **Respondió 26/10: "Hi, Gonzalo. Of course :) Best!"** - acepta el reencuentro. El gate real lo ponía **Pfizer** (cliente), no ella |
| **Siraj Shaik** (Infjini) | **ABIERTO** | **Respondió 26/10 con contenido: "estudiá inglés para cuando me presente a Disney"** - el idioma bloquea la presentación al cliente, no el proceso |
| **Sol Bisio** (cliente sin nombre) | cerrado 21/10 | **Respondió 27/10 08:48: "¡Qué bueno que hayas arrancado las clases para reforzar tu inglés! Sí, por supuesto! Podemos volver a hablar en uno o dos meses y ver cómo venís con el idioma y qué oportunidades hay disponibles en ese momento. Muchos éxitos con las clases y seguimos en contacto!"** - acepta el reencuentro. **Ojo con la lectura: NO reabre el req de Full Stack** (USD 5.600/mes) - es un **"vemos en el momento"**, sin fecha y sin puesto comprometido. |
| **Parthasarathy** (EIT/HTC/Disney) | cerrado 24/09 | **Respondió 26/10 13:36: "Great. We will update you if we have response. Position is on hold it seems"** - No menciona el inglés ni la reevaluación: es un "te avisamos si hay novedades" + "la posición está en pausa". **Lo que dice es que la POSICIÓN está en pausa** (el req de Disney, en el canal de EIT). **Lo que NO dice es por qué ni si el candidato queda en pie** - eso no está registrado y no se afirma. |

**Lo que significa la respuesta de Samarth:** "Sure thing" es **acuerdo de reencuentro**, no
compromiso: no menciona puesto, ni fecha, ni acción concreta. Y **nunca dijo por qué se había
cerrado el proceso** (ver la fila de Ritz-Carlton: el motivo del silencio de la empresa no está
registrado; hay dos hipótesis y ninguna verificada). Lo que sí sabemos: **no fue un rechazo** -
no hubo feedback ni decisión, y el proceso estaba explícitamente ABIERTO el 11/09. Cerró por la
regla de los 10 días.
**Consecuencia práctica: el mensaje de "reevaluación de nivel" no era exactamente lo que Samarth
necesitaba.** (Aun así no hizo daño: los tres que respondieron aceptan el reencuentro sin
objeciones.) A él lo que le hacía falta es que el proceso se reabriera por otro motivo (una
vacante nueva para Principal Full Stack en BA, o que la apertura de la oficina se activara). La
reevaluación de idioma le sirve para **otro** puesto. Si vuelve a escribir, el ángulo a ofrecer
es **disponibilidad y rol**, no nivel de inglés: preguntarle si el rol sigue abierto y si hay
algo nuevo del lado del cliente. El mensaje de idioma ya está enviado y no hizo daño (la relación
quedó tibia y viva, que era el objetivo), pero **no esperes que él lo lea como "reabre el proceso
de Ritz"**.

**Sobre Siraj (Infjini): el proceso estaba VIVO, y el filtro de idioma YA se había filtrado.**
El 26/10 Siraj respondió: **"estudiá inglés para cuando me presente a Disney"**. O sea, el
idioma no bloquea el proceso: bloquea **la presentación al cliente**. El proceso queda en
espera con condición, no cerrado. (Corrección a la lectura del 26/10 al mediodía: se había
supuesto que el filtro de este proceso todavía no se había filtrado. **Sí se había filtrado**, y
el propio Siraj lo dijo. El mensaje de recontacto no propuesta nada que chocara: coincidía con lo
que él ya pensaba.)

### Resultado final: 5 de 5 respondieron (26-27/10/2026)

| Contacto | Proceso | Respuesta | Que abre |
|---|---|---|---|
| **Samarth** | Ritz-Carlton (cerrado 22/09) | "Sure thing, Gonzalo and All the Best" | reencuentro; el puesto (~USD 82k, 2 viajes a US/mes) nunca dio feedback |
| **Julieta Costa** | Staffy/Pfizer (cerrado 20/10) | "Of course :) Best!" | reencuentro; el gate lo ponía **Pfizer** (cliente) |
| **Siraj Shaik** | Infjini/Disney (**vivo**) | "estudiá inglés para cuando me presente a Disney" | **entrevista en la 1ra o 2da semana de noviembre**; el idioma pasó de bloquear la presentación a ser el riesgo de la entrevista |
| **Parthasarathy** | EIT/HTC/Disney (cerrado 24/09) | "We will update you if we have response. Position is on hold it seems" | la **posición** del req está en pausa en el canal de EIT (el mismo req vive en Infojini) |
| **Sol Bisio** | cliente sin nombre (cerrado 21/10) | "Qué bueno que hayas arrancado las clases... Podemos volver a hablar en uno o dos meses y ver... qué oportunidades hay disponibles" | reencuentro + vía del **req Full Stack a USD 5.600/mes** |

**Lo que pasó, en una frase:** de 5 procesos cerrados por el mismo motivo (filtro de inglés
conversacional), **5 respondieron y ninguno cerró la puerta**. **Solo uno tiene fecha concreta:
Siraj/Disney (entrevista en la 1ra o 2da semana de noviembre).** Los otros cuatro aceptaron
"volvemos a hablar en uno o dos meses" o "te avisamos": es una **puerta abierta sin fecha**, no
un compromiso. Sol mismo lo dijo así: *"podemos volver a hablar en uno o dos meses y ver... qué
oportunidades hay disponibles"* - o sea **"vemos en el momento"**, **no la reapertura del puesto
de Full Stack**. Ninguno lo había hecho solo: el factor común fue que Gonzo **no se quedó con el
no**.

**Por qué funcionó (lo que se puede repetir):** el mensaje **no pidió reconsideration**. Dijo
"estoy arrancando el curso de inglés hoy" y ofreció reevaluar. Eso cambia la naturaleza de la
conversación: no es un individuo rogando que le den una oportunidad, es alguien que **está
resolviendo el bloqueante y avisa**. La respuesta natural a eso no es un no.

**Cuarta respuesta: Parthasarathy (EIT/HTC/Disney), 26/10 13:36 - "Great. We will update you if we have response. Position is on hold it seems."**
Es la única de las cuatro que **no engancha con la reevaluación**: su respuesta no menciona el
inglés ni la capacitación, y su contenido es "te avisamos si hay novedades" + "la posición está en
pausa". **Lo verificable es que la POSICIÓN del req de Disney está en pausa en el canal de EIT.**
Lo que **no** está registrado (y no se afirma): por qué está en pausa, ni si el candidato queda en
pie en ese canal, ni si el "Great" es un rechazo o un acknowledgment. **Un "Great" seguido de "on
hold" no es una señal unívoca: puede ser cortesía o puede ser un no.**
**Por qué importa: EIT e Infojini son DOS sub-vendors del MISMO req** (cadena Disney -> HTC ->
sub-vendor), y no se conocen entre sí. El req está "on hold" en EIT y **vivo, con entrevista en
noviembre, en Infojini**. Un mismo puesto puede estar pausado en un canal y vivo en el otro, y eso
explica por qué el tracker los tenía en estados distintos.
**Acción: no preguntar nada a Parthasarathy** (la regla del proceso sigue siendo no insistir), pero
**ese dato se cruza con Siraj**: si el req estuviera en pausa a nivel de cliente (Disney/HTC),
afectaría a los dos. El que puede confirmarlo es Siraj, y él tiene la entrevista en noviembre.

**Lo que muestra el patrón de las 3 respuestas (Samarth, Julieta, Siraj):** en los tres casos, el
**intermediario no es quien pone la barra de idioma** - la pone el cliente final (Pfizer, Disney,
el cliente de Samarth). El recontacto reabre la puerta **en el intermediario**, que es donde se
decide si hay otro req que encaje. El gate real se levanta con el inglés, que es lo que ya está en
curso. **Por eso el mensaje no era una súplica: era unanotification de que el cuello de botella se
estaba destrabando.**

**Corrección de credibilidad que hay que aplicar en los próximos contactos:** el mensaje dice
*"I'm retaking the course to regain my fluency"* y *"re-validate my B2 level"*. **El corpus no
tiene certificado de B2 (§4 solo Deque) ni antecedente de un curso de inglés previo** (verificado
por grep en todo el workspace). Ambas frases presuponen una acreditación o un curso anterior que
no están registrados. **La forma verificable, igual de fuerte:** *"I started a B2 intensive
course at the CUI (UBA) today - two months - and I plan to take the C1 certification exam next
year."* Es literal lo que dice el corpus, y tiene el plus de que el curso empieza HOY.

### Plan de inglés C1 (decisión de Gonzo, 2026-10-21)

A raíz de los dos cierres por C1 conversacional, Gonzo se anota en el **CUI (Centro Universitario de Idiomas, UBA)** para la capacitación de C1 y su certificación, **mientras tanto sigue buscando**.

- **Plan completo con instrumentos, costos y fechas:** `studies/english/README.md`
- **Plazo a no perder:** la inscripción al examen **CUI-ING C1** cierra el **viernes 30 de octubre de 2026** (mesa del **6 de noviembre**, $140.000, online con oral por Zoom). Fuentes de `cui.edu.ar` leídas el 2026-10-21; **verificar en el centro antes de pagar**.
- **Declarado hasta que exista el certificado: B2.** Un C1 de papel que no se sostiene en una call es peor que un B2 honesto.

## Historial / cerrados

| Empresa | Puesto | Fecha contacto | Cierre | Motivo |
|---|---|---|---|---|
| Sol Bisio (cliente sin nombre) | Senior Full Stack Developer (AI-first) | 2026-10-14 | **cerrado 21/10 → REABIERTO 27/10** | El cliente exige **C1 conversacional sí o sí** para esa posición; el CV declara B2 y no pudieron avanzar. No es rechazo de perfil: Sol dijo que mandó toda la info y que te tiene presente para próximas búsquedas Full Stack. **27/10: Sol responde al recontacto de inglés y reabre explícitamente** ("podemos volver a hablar en uno o dos meses y ver... qué oportunidades hay disponibles"). Es el req **Full Stack a USD 5.600/mes**, el mejor pagado de todos. Detalle en `docs/entrevistas/sol-senior-fullstack/sol-seguimiento.md`. |
| EIT/HTC (cliente Disney) | Lead Software Engineer Digital Accessibility | 2026-09-11 | **cerrado 24/09** | Nunca hubo oferta firme: el rate lo aceptó el reclutador, el cliente jamás hizo call. Cierre del vendor: "we will update if they want to schedule call" (23/09). El mismo req lo publica Infojini: era bench amplio, no búsqueda urgente. No volver a escribir. Palanca que queda: CPACC antes del 30/11 si quiere retomar el hilo con un entregable. |
| Wigou | AI-Native Software Engineering | 2026-08-31 | **cerrado 24/09** | Meet con Andrés Abraham (COO) el 02/09, sin feedback concreto. Tres semanas sin contacto. Cerrado por la propia regla del 02/09 ("si no hay novedad en ~1 semana, cerrado"). |
| OpenSistemas | AI-Native (colaboración freelance) | proceso previo | **cerrado 11/09** | Avanzaron con otro candidato, después de la entrevista técnica del 03/09 con Fernando. |
| Cruceros / Ritz-Carlton (oficina BA) | Principal Full Stack Developer | 2026-08-24 | **cerrado 22/09 por la regla de +10 días. Motivo del cierre NO SABIDO** | Lo que consta: test 69% -> re-test OK -> primera ronda con la empresa 02/09 (30 min) -> **silencio de la empresa**: ni feedback ni decisión. El documento de seguimiento (`docs/entrevistas/ritz-carlton/ritz-carlton-retest-seguimiento.md`) lo dejó explícitamente como **ABIERTO** el 11/09 ("pese a no haber tenido una respuesta directa, aun no la demos por cerrada"). Cerró por la regla de los 10 días, **no por un rechazo**. **El motivo concreto del silencio nunca se registró: hay dos hipótesis y ninguna verificada** - (a) el idioma (en una ronda de hiring en inglés y un puesto Principal Full Stack para una apertura de oficina en BA, es plausible), (b) el cliente reordenó prioridades, o el rol se cubrió con otra persona. Lo que NO hay: "Samarth dijo let me check with the manager x7" ni "feedback 24-48h incumplido" - **esas dos frases estaban en este tracker sin fuente y se sacaron el 26/10** (ver `git log -S`). **Es el proceso que más Gonzo valoraba**: abrir la oficina de BA, ~USD 82k, 2 viajes a US por mes, **directo en nómina del cliente** (no agency). **Samarth respondió el 26/10 al recontacto por idioma: "Sure thing, Gonzalo and All the Best"** - y **nunca dijo por qué se había cerrado**. |
| Kake | (a definir) | 2026-09-10 | **cerrado 22/09** | Pidieron video asincrónico el 10/09; nunca se envió ni hubo contacto posterior. |
| Koin Limited | AI Product Engineer (Next.js + Supabase) | 2026-09-09 | **cerrado 22/09** | Confirmación humana (Lyliana Padilla) y nada más. Stack match perfecto. Si escribe ella, reactivar. |
| Aliancers | (a definir) | 2026-09-09 | **cerrado 22/09** | Solo auto-confirmación genérica. Nunca hubo señal humana. |
| Ciklum | Senior JavaScript Engineer (4417) | 2026-09-09 | **cerrado 22/09** | Solo auto-confirmación. Hay portal para trackear si se reactiva. |

## Backlog de prospectos (relevado 2026-09-23, fuera del seguimiento)

No es seguimiento activo. Relevamiento hecho de costado; se retoma cuando Gonzo lo pida.

Filtro: remote real (LATAM/global), foco a11y o design systems, sin requisito de residencia US.

| Empresa | Puesto | Canal | Ubicación | Encaje | Estado |
|---|---|---|---|---|---|
| Infojini Inc | Lead Software Engineer - Digital Accessibility | a11yjobs (vivo) | LATAM Remote, 9-5 EST, 12 meses | Muy alto - JD idéntico al de Disney (mismo stack: Evinced, AMP, ZoomText, Narrator, Jira, Figma) | Posible mismo req que EIT |
| E-IT (EIT Professionals) | Lead Digital Accessibility Engineer | a11yjobs (vivo) | LATAM/US Remote, contract | Muy alto - es el mismo rol ya en curso | Referencia |
| Cheesecake Labs | [Contractor] Digital Accessibility Consultant | a11yjobs / trakstar | Brazil Remote (LATAM) | Alto - contractor a11y puro | Confirmar vigencia (listing de julio) |
| Equals True | Senior React Engineer (Design Systems) | web / LinkedIn | Remote-first, Argentina listada | Alto - design systems + React/TS | Confirmar vigencia |
| FullStack Labs | Senior Accessibility Engineer (Americas/LATAM) | fullstack.com talent pool | Remote LATAM | Alto - nearshore a11y | Reclutan continuo |
| BairesDev | Remote Accessibility Engineer - WCAG & Inclusive UI | a11yjobs | Anywhere US (pide residencia US) | Medio - encaje técnico alto, filtro de residencia | Revisar si aceptan LATAM |
| GitLab | Senior Accessibility Engineer | handbook/careers | Americas, EMEA - all-remote | Alto - a11y en design system propio | Listing vencido; revisar si reabre |
| Clipboard | Senior Design Engineer, Design Systems | Ashby | US Remote (USD 180-250k) | Medio - design systems, sin foco a11y explícito | Revisar filtro de residencia |

### Hallazgo del relevamiento

El req de Disney/HTC lo estaba pitcheando **más de un vendor**: E-IT e **Infojini Inc** publicaban el mismo puesto (LATAM Remote, 9-5 EST, 12 meses, stack idéntico de herramientas a11y). Confirmaba que era un bench req amplio, no una búsqueda exclusiva ni urgente.

## Cadencia

- Objetivo: 3-5 aplicaciones/día, calidad (stack match) sobre volumen.
- Cada aplicación nueva se agrega con fecha.
