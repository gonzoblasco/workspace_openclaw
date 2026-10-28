<!-- project: github.com/gonzoblasco/workspace_openclaw -->

# Pack de preparación - AI interview de Mercor (Project Odin)

> Para Gonzo. Todo verificado contra la documentación oficial de Mercor el 28/10/2026.
> Links: [AI Interview](https://talent.docs.mercor.com/support/ai-interview) ·
> [LLM Usage Policy](https://talent.docs.mercor.com/policies/llm-usage) ·
> [Apply](https://talent.docs.mercor.com/how-to/apply) ·
> [Insightful/Workpuls](https://talent.docs.mercor.com/how-to/use-insightful)

---

## 1. Qué es exactamente

- **Es una entrevista con una IA, no con una persona.** La IA hace preguntas específicas del rol,
  transcribe y evalúa. No hay opción humana: *"Our AI interview is the standard and only method
  for screening candidates."*
- **Dura ~3 minutos en este listing** (el listing dice "brief (3-minute) conversation"). El doc
  general dice ~20 min, pero los listings de Odin acortan: usá 3.
- **Cámara y micrófono ON.** Te graba y transcribe.
- **Screen sharing**: solo full-screen, y solo si el listing lo pide. En Odin probablemente sí
  (el trabajo es narrar workflows en pantalla), pero el setup check te avisa.
- **Los transcripts no se comparten** ni se descargan. Las grabaciones quedan guardadas para
  evaluar candidacy.
- **Retakes: hasta 3** (compartidos entre postulaciones al mismo interview). Los hiring managers
  **ven la cantidad de retakes**, así que no los quemes por nerves: reservalos para problemas
  técnicos o para una respuesta que salió mal de verdad.
- **"Interview too short"** no cuenta: si termina antes de tiempo, hay que rehacerla.
- **Solo cuenta el último intento.** Si retakeás, el anterior se descarta.
- **Practice interview: gratis, ilimitada, no cuenta y no se comparte.** Es el instrumento ideal
  para calibratear tu inglés y tu forma de responder. Tomala **antes** de la oficial.
  `https://work.mercor.com/auth-wall?type=interview_config_49baee86-0da1-4ee6-b701-8a842b09b9d5`

## 2. La regla que puede costarte la postulación: LLM Usage Policy

Mercor es explícito y la infra es de detección:

| Permitido | PROHIBIDO |
|---|---|
| Corrección de gramática y dicción | Que un LLM **escriba** la respuesta |
| Refinar la redacción sutilmente, manteniendo tus ideas y estructura | Pedirle justificaciones o explicaciones |
| Preparar antes (esto que estás leyendo) | Evaluar calidad de respuestas de modelos |
| | Predecir comportamiento de código o resultados de runtime |

> *"Submissions that are evidently produced by artificial intelligence will be identified and
> flagged accordingly."*

**Cómo lo aplico yo, en concreto:**
- Este documento, los resúmenes de tus carreras, el guion de Practice: **sí**.
- Que yo te escriba un texto que vos recitás en inglés ante la IA: **no** (y además no te sirve:
  la IA evalúa si suena a vos y si lo hacés, se nota).
- Lo que sí hago: darte **los temas y el esqueleto**, y que vos digas las palabras.

**El corollary importante:** la entrevista es de 3 minutos, en inglés, y evalúa *cómo razonás*.
No podés ensayar la respuesta. Podés ensayar **el tema** y **tu forma de explicar**.

## 3. Los 5 temas que casi seguro van a aparecer

Son los que salen del CV + el JD. Para cada uno, la respuesta tiene que ser un **hecho tuyo con
número o nombre**, no una definición.

### T1. "Walk me through a project you're proud of" (el clásico)
**Usá SoporteML.** Es tu activo más fuerte y el único con cliente real, producto en producción y
facturación.
- Qué es: un CRM multi-tenant con IA para vendedores de Mercado Libre.
- El problema real: los vendedores responden consultas de clientes todo el día; la IA sugería
  respuestas y el cliente lo adoptó.
- Tu rol: end-to-end (producto, implementación, tests, deploy).
- Números que tenés y podés usar: multi-tenant con roles de equipo y multi-empresa, RAG con
  pgvector, Autopilot con guardarraíles de confianza, Stripe con webhooks, primer cliente en
  producción (**Pro Motors**), integración real con Mercado Libre.
- **El remate (esto es lo que más suma):** *"I built it with AI coding agents in the loop - Claude
  Code and Codex - but the rule I applied was quarantine → analyze → verify → adopt. Nothing from
  outside went into the codebase without being read and verified first."*
  Eso no es "usé AI": es un **método**. Es exactamente lo que un AI lab quiere evaluar.

### T2. "Tell me about a hard bug you solved" (el que más筛查 filtra)
Tenés dos buenos y son distintos entre sí. Elegí según lo que te salga más natural:
- **Opción A (producto):** el sistema multi-tenant / RAG / Autopilot de SoporteML. Debug de
  concurrency en Supabase, RLS, o el guardarraíl de confianza del Autopilot.
- **Opción B (OSS, y es la más diferenciadora):** uno de tus 11 PRs. El mejor para "explain your
  reasoning" es **`facebook/astryx #4605`** (indicador no cromático del breadcrumb, WCAG 1.4.1) o
  **`carbon-design-system/carbon #22887`** (`aria-describedby` en `ComposedModal`, con las dos
  rutas: `<dialog>` nativo y `div[role=dialog]`).
  El segundo es perfecto para una pregunta de razonamiento: el bug era que el atributo no se
  propagaba, y la decisión de diseño fue **no** poner la lógica en un `useEffect` sino en el
  punto donde el componente renderiza, para que el valor por defecto se comporte igual en
  ambas rutas. Eso es razonamiento de senior, y es verificable.
- **Y si te preguntan cómo lo explicaste:** ese es el hook. Escribiste la descripción del PR, la
  documentación de remediación, y explicaste decisiones a devs dentro del sprint.

### T3. "How do you work with a team?" / "How do you explain technical decisions?"
Acá tu evidencia es fuerte y es el JD literal ("ability to clearly explain your reasoning"):
- Referente de accesibilidad del equipo en EY: revisaba componentes **antes** de implementarlos,
  definía estándares y anotaciones a nivel de componente, escribía **requisitos técnicos con guía
  de código** para las historias de UI.
- Priorización de defectos por impacto WCAG en Jira, con guía de remediación **dentro** del sprint.
- Coaching a desarrolladores dentro de sus ramas.
- Equipo matricial cross-regional (US / India) con varias fases del SDLC en paralelo.
- Lideré un equipo de 3 ingenieros en una plataforma de inteligencia financiera con IA en Next.js.
- **El remate:** *"My default is writing the reasoning down. Most of my work is written artifacts:
  PR descriptions, remediation docs, ADRs in my own projects, technical requirements with code
  guidance. If I can't explain it in writing, I don't understand it well enough yet."*

### T4. "¿Cómo usás IA en tu trabajo?" (pregunta casi segura: es un AI lab)
Acá hay que ser **preciso y sin fanfarronear**, porque evalúan a alguien que va a hacer training
data de workflows con IA:
- Herramientas: **Claude Code y Codex** como motores headless en tareas largas, y un stack propio
  (OpenClaw) con subagentes, memoria, skills y handoffs.
- El método: **quarantine → analyze → verify → adopt**. Nada del exterior entra al código sin
  leerse, analizarse y verificarse.
- Lo que **NO** es: no declaro Cursor ni GitHub Copilot, y no tengo experiencia en computer-use.
  Si te preguntan, decí la verdad: *"I don't use computer-use agents. My work is bounded-context
  subagents over code."* (Es un hecho del corpus y además es una respuesta coherente: para este
  rol, la honestidad sobre el alcance es un activo.)
- Concreto: el `kanam-fixer` expone un **servidor MCP propio** (2 tools) que le permite a un
  agente consultar qué anuncia un lector de pantalla para un fragmento de HTML. Lo construiste y
  lo mantenés vos. **MCP es un keyword fuerte** en este rubro.

### T5. "¿Qué te interesa de este proyecto?" / "¿Por qué Mercor?"
No seas genérico. Conectá el rol con lo que hacés:
- *"This is the kind of work I already do: real workflows on my own machine, with the reasoning
  narrated, not abstracted. The part I find genuinely interesting is that the output is training
  data - so the quality of the explanation matters as much as the result."*
- Si preguntan por el hardware/macOS: usás VS Code, Terminal, Git, npm/pnpm/bun, Docker. La Mac
  es tu herramienta de trabajo diaria, no un requisito a cumplir.

### T6 (si aparece). "Do you have a degree?"
Acá va la respuesta que ya está escrita en `skills/job-application/references/educacion.md`:
> *"I studied Computer Science at Universidad de Palermo between 2001 and 2002 and did not finish.
> My actual technical formation is the work: 10+ years of frontend, 11 merged PRs in production
> component libraries, and a product in production with a real client."*
**No digas "yes, I have a degree". No digas "I dropped out" como si fuera título.** Decilo una
vez, con naturalidad, y seguí con la evidencia. Si insiste, repetí la misma respuesta: no te
pDstés de contexto ni lo justifiques de más.

### T7 (si aparece). "What were you doing between Nov 2019 and Aug 2020?"
**Este es el hueco real del CV**: entre Minutentag (hasta 11/2019) y Super7UI (desde 08/2020) hay
9 meses sin rol declarado. La AI interviewer genera preguntas **específicas sobre el CV**, asi que
esta repregunta es probable.

**Lo que NO hay que hacer:** inventar un rol, y tampoco hacer un hueco de 9 meses sonar a
problema. El corpus no lo registra, asi que no se escribe en el CV (ADR-101: el corpus es el dueño).

**Respuesta honesta y corta (adaptala a lo que sea verdad, pero no inventes):**
> *"I left Minutentag in late 2019 and started at Super7UI in mid-2020. In between I was looking
> for a role where I could go deeper on accessibility, which is what Super7UI turned out to be -
> auditing Warner Bros' internal review platform. The gap was job search, not a break in the work."*

**La forma que funciona en una entrevista de 3 minutos:** reconocer el hueco, decir en una frase
qué estabas buscando, y cerrar mirando adelante. Un hiring manager prefiere eso a un CV con un
hueco inventado. Si la IA insiste con la segunda repregunta, no te extensions: *"I was between
roles, and I used the time to consolidate my accessibility focus. The Super7UI role that followed
is the most relevant piece for this project."*

**Nota de trazabilidad:** si Gonzo recuerda que ese período tuvo trabajo real (freelance, un
proyecto, un curso), el dato va primero al corpus (`memory/career-facts.md` §2) y despues al CV.
hasta despues al pack. Es el unico caso donde el CV no se toca hoy.

## 4. Tu riesgo real: el inglés (B2+)

El listing pide **"Excellent written and verbal communication skills"** y la evaluación es una
entrevista hablada de 3 minutos. Este es **el gap que define el resultado**, más que el degree.

Reglas prácticas para ese inglés:
- **Frases cortas, ideas completas.** No es un examen de gramática: es comprensión + convicción.
- **El " filler y las muletillas matan el score más que los errores.** Estudiá *um* y *you know*:
  pausá una fracción de segundo en vez de llenar.
- **Cifras y nombres propios en inglés** (nombres de repo, de librería, de herramienta) pero
  **sin traducir**: `react-spectrum`, `carbon-design-system`, `aria-describedby`.
- **Estructura explícita al responder:** "Two things. First... Second..." Funciona perfecto en
  inglés B2 y le da a la IA un transcript fácil de evaluar.
- **Si no entendés una pregunta, que te la repita.** La IA lo dice: *"request the AI to repeat or
  clarify a question"*. Pedir que repita NO penaliza. Inventar una respuesta sí.
- **Pausas largas la interrumpen.** Hablá sin parar.
- Ya tenés el plan de inglés intensivo (martes y jueves 10-13 h por Zoom, hasta el 22/12). **Esta
  entrevista cae en esa ventana**: es una razón extra para priorizarlo.

## 5. Setup técnico (hacelo antes, no el día de la entrevista)

### En la Mac
- [ ] **La entrevista se hace en la MacBook Air M2, NO en el Mac mini.** Verificado 2026-10-28:
      el **Mac mini (Mac16,10, M4) no tiene cámara ni micrófono** (`system_profiler SPCameraDataType`
      no devuelve nada y `SPAudioDataType` solo lista salidas: parlantes + HDMI). El nodo de
      OpenClaw del Mac mini también reporta `camera: false` y `microphone: false`. Sin eso no hay
      entrevista posible: la IA te ve y te escucha.
      La **MacBook Air M2 (Mac14,2) sí cumple**: macOS 27.2, chip M-series (requisito del listing:
      "Apple M-series chip or Intel processor, running macOS 15 or higher").
- [ ] **Chrome** (última versión). Firefox no sirve. Safari tampoco para la interview.
- [ ] Permisos de **cámara y micrófono** para `work.mercor.com`: candado en la barra de dirección →
      Permissions → Camera y Microphone = Allow. Después refresh.
- [ ] **Sin VPN, sin extensiones** (ad blockers, privacy extensions). El doc lo dice: estorban el
      streaming de la IA.
- [ ] **Setup checks** en la waiting room: Working mic (obligatorio), Screenshare (obligatorio si
      el listing lo pide), Face in frame, Good lighting, Working camera, Steady camera. Los
      obligatorios habilitan el botón "Start interview".
- [ ] **Pantalla completa** al compartir: "Only full-screen sharing is supported". El efecto
  "hall of mirrors" al arrancar es normal y temporal.
- [ ] **Audio externo y auriculares** recomendados. Ambiente silencioso.
- [ ] Lápiz y papel (y calculadora) a mano. Algunos interviews incluyen whiteboard (se guarda
  solo).
- [ ] **Timezone**: Argentina (GMT-3) vs el equipo de US. El job es part-time 10-20 h/semana.
 -ofrecé disponibilidad en US EST core hours, que es lo que ya dice tu CV.

### Workpuls (la app de tracking) - NO la tenés

### Decisiones tomadas (28/10)

#### El email de la cuenta: `gonzoblasco@gmail.com`

El formulario de interés pedía *"the email address where you received the invitation"*, y ahí
llegó la invitación. Así que **la cuenta de Mercor se crea con `gonzoblasco@gmail.com`**.

**El CV sigue con `gonzoblasco@icloud.com`**, y no es un descuido:
- `gonzoblasco@icloud.com` es el **dueño del dato de contacto** en el corpus (`career-facts.md`,
  `contact_email`), y el gate `check-cv-facts.py` lo exige: cualquier otro email en un CV es
  violación.
- Las otras tres postulaciones vivas (Mural, Mercado Pago, RYZ) ya van con icloud. Cambiarlo
  ahora desalinearía el dossier entero por un proceso nuevo.
- Los dos emails son tuyos y los dos te llegan. Un recruiter que los compare no ve nada raro: es
  tener dos correos.

**Lo que sí hay que hacer:** en `work.mercor.com`, el email de la cuenta (gmail) tiene que coincidir
con el de LinkedIn, porque Mercor recomienda que coincidan para el matching. Si tu LinkedIn está
con icloud, avisame y lo dejamos consistente, o se cambia la cuenta.

#### Usarme durante la entrevista: **no**, y el motivo es concreto

Entiendo la idea y la propuesta es ingeniosa, pero choca contra la LLM Usage Policy de Mercor de
forma literal, no teórica:
- La policy **prohíbe explícitamente** usar LLMs para "providing justifications or explanations" y
  para componer respuestas. Que yo te pase la respuesta mientras vos hablás es exactamente eso.
- Mercor dice: *"Submissions that are evidently produced by artificial intelligence will be
  identified and flagged accordingly."* La IA transcribe y evalúa. Si el 60% de tus respuestas
  tienen mi sintaxis, se nota, y lo que se pierde no es un puntaje: es la candidatura entera.
- Además es visible en la grabación: la entrevista te mira por cámara, pide screen sharing
  full-screen, y el transcript es lo que evalúa. Mirar una segunda pantalla mientras hablás es
  comportamiento observable, y en una entrevista de 3 minutos con webcam encendida.
- Y el más práctico: son 3 minutos. No hay tiempo humano para saltar a otra pantalla, leer,
  traducir y volver. En la práctica, la versión con interrupciones te haría hablar PEOR, que es el
  resultado opuesto al que buscás.

**Lo que sí puedo hacer, y es lo que más valor aporta:**

1. **Antes:** preparación de fondo (esto ya está), y un **ensayo de roleplay en inglés** donde yo
   hago de entrevistador de IA, te hago las preguntas del rol, y te doy feedback sobre claridad,
   estructura y nivel de inglés. Se puede repetir varias veces. Eso es exactamente lo que la
   "Practice Interview" gratis de Mercor hace, pero con feedback.
2. **Después:** debrief. Si me pasás las preguntas que te hicieron (las de la Practice son
   gratis y no se comparten con empresas) y cómo respondiste, te digo qué funcionó y qué no.
3. **Durante:** vos, solo, con el esqueleto de 6 respuestas en una nota. Eso es preparación, no
   composición: permitido, y es lo único que además funciona.

**La versión que sí funciona y es legal:** vos contame en inglés cómo responderías, yo te doy
feedback. El ensayo es tuyo; la corrección es mía. Esa frontera la respeta la policy y te deja
mucho mejor parado en la entrevista real.
- **La app se llama Workpuls** (antes Insightful). Se baja de `https://app.insightful.io/#/token/download`
- **Requisito: macOS 11+**, y vos tenés macOS 27.2. Va.
- **No hace falta instalarla para la entrevista.** Solo hace falta cuando tenés contrato activo.
  Bajala cuando te la pidan (la asignación de proyecto tarda **12-24 h** después del onboarding).
- **Cuidado con esto:** Insightful/Workpuls **toma screenshots periódicos mientras el timer
  corre**. Sobre tu Mac, eso significa que **queda registro de lo que hacés en pantalla durante
  las horas pagadas**. Es parte del modelo del trabajo, pero conviene que lo sepas: si tenés
  clientes o material confidencial abierto, cerralo antes de clockear. El propio listing dice que
  el trabajo no involucrará información confidencial de empleadores o clientes.
- Solo podés clockear en **un dispositivo a la vez**. Si cambiás de máquina: deslogueate y cerrá
  la app, o las horas no se registran y no te las pagan.
- **Internet estable, siempre.** Offline no trackea.
- Espacio en disco: te quedan 107 Gi. Las grabaciones de pantalla y las copias de video pesan.
  No es un problema ahora, pero no dejes que se te llene durante un mes de trabajo.

## 6. Tu plan, en orden

1. **Hoy:** creá la cuenta en `work.mercor.com` con **`gonzoblasco@icloud.com`**
   (el mismo del CV). Verificá el mail.
2. **Hoy:** subí el CV (PDF, texto, 1-2 páginas, <2 MB) en Profile → Résumé.
3. **Hoy:** tomá la **Practice Interview**. Es gratis y no cuenta. Tomala 2 o 3 veces. Sirve para
   dos cosas: calibrar tu inglés hablado y ver cómo la IA formula las preguntas.
   **Anotá textualmente las preguntas que te haga.** Eso te dice qué preparar.
4. **Mañana:** prepará las 6 respuestas de arriba con tus palabras, en voz alta, cronometradas
   (30-45 segundos cada una).
5. **Cuando tengas el CV:** postulá al listing desde `work.mercor.com` → Explore → *Software
   Developers (Must own MacBook)* → Apply Now.
6. **Después de la postulación:** el paso siguiente es un **assessment pago** ("Complete a brief
   paid assessment"). Cuando te lo asignen, avisame y lo armamos.

## 7. Lo que el listing promete (para que sepas qué esperar)

- **$50-$60/hr** en el listing (el mail decía $40-$150/hr: el rango amplio es marketing; el real
  del listing es $50-60). Contrato hourly, part-time 10-20 h/semana.
- **Pagos semanales** (miércoles) por Stripe o Wise. Argentina está soportada con **Stripe
  Connect**, así que cobrás en USD. Vas a necesitar على cuenta en Stripe; preparate para el
  onboarding fiscal (alta como contractor, y revisar cómo declarás).
- **Contrato como contractor independiente**, sin W-2. En Argentina eso significa que vos gestionás
  los impuestos de esa ingreso: es un gasto deducible, pero la carga real es tuya.
- **El proyecto puede acortarse o cortarse antes** ("projects can be extended, shortened, or
  concluded early").
- **El pago puede ser por tarea aprobada**, no por hora efectiva (advertencia de la comunidad de
  workers de Project Odin). El onboarding puede no estar pago. **Anotá tus horas y los pagos**: es
  lo único que te protege si hay un reclamo.
- **No pagan ni piden que compres hardware.** Si eso aparece, es phishing.

## 8. Verificación del mail, para que cierres el círculo

El mail **era legítimo** (verificado el 27-10):
- `chloechee@mercor.com` → Chloe Chee existe, se unió al Growth team de Mercor (post propio en
  LinkedIn del 20-oct-2026). Coincide firma, rol y timing.
- El link iba por `awstrack.me` (click-tracking nativo de Amazon SES) a un **Google Form real**
  llamado "Mercor Project Interest Form" que pide solo nombre, email, disponibilidad, hardware e
  inglés. **No pide passwords, datos bancarios, documentos ni fees.**
- "Project Odin" existe: hay listings públicos en `work.mercor.com` con el **mismo requisito de
  hardware** (Mac, macOS 15+, M-series o Intel) y la misma forma de trabajo (grabar y narrar).
- **Anomalía que quedó abierta** (sin impacto, pero anotála): el link de confirmación no está
  linkeado desde ningún sitio oficial de Mercor, y el `SPF` de `mercor.com` solo autoriza Google
  (Mercor usa SES desde `mail.mercor.com`). Mi lectura: el form es real pero el canal de mail es
  de una campaña de Growth, no del flujo oficial de postulación. **Por eso: postulá desde
  `work.mercor.com`, no desde el link del mail.** Es el camino que no depende de ninguna campaña
  y el que hace que tu postulación quede registrada en la plataforma.
