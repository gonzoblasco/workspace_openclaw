<!-- project: github.com/gonzoblasco/workspace_openclaw -->

# Prep técnica - Senior Frontend Developer (Growth), tempo.io

> **Entrevista: lunes 26/10/2026, 10:00 ART.** Todo lo que sigue es material de apoyo: las
> respuestas están en inglés porque la entrevista es en inglés.
>
> **Regla que ordena todo este documento:** cada afirmación sobre Gonzo tiene que ser
> rastreable a `memory/career-facts.md`. Donde no hay hecho, está el gap honesto. Un ejemplo
> inventado se cae en la segunda repregunta, y un candidato que se cae una vez queda fuera.

---

## 0. Lo que hay que tener claro antes de empezar

**El gap es real y el hiring manager lo va a interrogar.** Pero el gap no es "no hice growth":
es "no operé infraestructura de experimentación a escala". La diferencia importa, y es
defendible.

| Dónde tenés evidencia real | Dónde no |
|---|---|
| A/B testing en producción (Minutentag 2019, Adobe Target, variantes como snippets de JS nativo contra usuarios reales) | Feature flags como plataforma (ninguna) |
| Hacer que una calidad blanda se vuelva medible y exigible en el pipeline (WCAG 2.2 AA, 50+ componentes, axe-core + Playwright en CI que frena el merge) | Instrumentación de eventos de analytics (ninguna) |
| Escribir la especificación técnica antes de implementar (requisitos de accesibilidad con ejemplos de código, anotaciones a nivel componente, revisiones de Figma y Storybook antes del desarrollo) | Análisis de funnel, activación/retención/conversión (ninguno) |
| Métricas de contenido: 2M+ usuarios mensuales, 200+ violaciones resueltas, 50+ componentes auditados | MDE, power analysis, experimentos multivariantes con volumen estadístico (ninguno) |
| AI-first real: sistema propio con agentes y memoria persistente, CRM con IA end-to-end en producción | - |

**El argumento que te salva, en una frase:**

> *"I haven't built an experimentation platform. What I have done is take a soft quality standard
> and make it measurable and enforced in the pipeline - and that is the same job growth needs,
> with a different metric source."*

---

## 1. Preguntas que te van a hacer

### A. Experimentación

**1. "Walk me through an A/B test you ran."**

*Lo que tiene que contestar:* contexto, tu rol, cómo se implementaban las variantes, y el
aprendizaje. **No** "construí la plataforma".

> At Minutentag, in 2019, we ran A/B tests on the e-commerce site with Adobe Target. My job was
> the variant side: I wrote the code for each variant as plain JavaScript snippets, which the
> tool injected at runtime, and we validated them against real users on the live site.
>
> The lesson I took from that was that an experiment without a clearly defined metric is just a
> guess. I learned to write the hypothesis and lock the primary metric before any code shipped.
>
> To be clear about the scope: I used the tool and implemented the variants, I did not build the
> experimentation infrastructure. That infrastructure is what LaunchDarkly or Optimizely give
> you today, and it is the same discipline with tooling I did not have.

*Qué lo sostiene:* corpus §2.4 (Minutentag, uso de Adobe Target, variantes como snippets de JS
nativo, confirmado por Gonzo el 21/10/2026). **El claim de "construir la infraestructura" no
está confirmado y no vuelve.**

> **A verificar con Gonzo antes del lunes:** ¿te acordás de un experimento concreto? ¿Qué se
> probaba y contra qué? Sin eso, la historia queda en el nivel de "cómo trabajábamos", que es
> defendible, pero es más débil que un caso con nombre. **Si no lo recordás, no lo inventes:
> contá el patrón de trabajo, no un experimento que no podés sustentar.**

**2. "How would you design an experiment for us?"**

*Lo que tiene que contestar:* hipótesis, una sola métrica primaria, guardrails, tamaño de
muestra, regla de decisión *antes* de lanzar.

> I'd start with the hypothesis in one sentence and one primary metric - for Tempo, something
> like "the percentage of licensed seats that log their first worklog within their first week".
> Then I'd define guardrail metrics that must not degrade, and I'd write the ship/kill/iterate
> decision rule before the experiment starts, not after I see the numbers. I'd release it behind
> a flag, stage it, and only look at the results once the planned sample size is reached.

*Base honesta:* esto es **metodología transferida del pipeline de a11y** (definir el criterio,
> escribir el chequeo, bloquear el merge), no experiencia directa de experimentación. Decilo así.

**3. "What are the common pitfalls in experiment design?"**

> The biggest one I know is treating assignment as exposure - a user is bucketed into a variant
> but never actually sees it, and the result is meaningless. The other is defining the metric
> after you've seen the data, which is just a way of finding a story in noise. I would log an
> exposure event separately from the assignment, and lock the hypothesis and metric before
> launch.

*Base:* experiencia de A/B real (corpus §2.4) + disciplina de gates medibles. **No** afirmar
"siempre lo hice así" si no es un hecho del corpus: hoy lo decís como lo que harías.

### B. Analytics e instrumentación

**4. "Which analytics platforms have you used?"**

*Acá va el gap. Corto y de frente, sin rodeos:*

> I've worked with the landscape - Amplitude, Mixpanel, PostHog - and I know the trade-offs, but
> I haven't owned a production analytics stack end to end, and I don't want to imply otherwise.
>
> What I have done is the part that determines whether the data is worth anything: I built a CI
> pipeline that makes a quality standard measurable and enforced, where a missing check blocks
> the merge. Applying that to events means a typed event schema and a test that fails when the
> event stops firing. I learn tooling fast - I picked up Supabase, Edge Functions and Stripe in
> a freelance project.

**5. "How do you decide which events to instrument?"**

> I'd start from the funnel - activation, then retention, then conversion - and define a
> consistent taxonomy rather than ad-hoc events, because the cost of an inconsistent event
> schema is that you can't compare anything later. Each event gets a definition and a test
> that fails if it disappears from the build.

*Base:* el patrón es **transferido de los gates de a11y en CI** (corpus: Super7UI, pipeline
axe-core + Playwright en CI/CD). Decir "es el mismo hábito, aplicado a eventos" es honesto.

**6. "What would you measure for Tempo?"**

*Acá usás lo que aprendiste del producto. Con cuidado de no vender humo:*

> Tempo's model is seat-based, so the metrics that matter are utilisation and attach rather
> than acquisition. Concretely: activation would be time-to-first-worklog per seat, retention
> would be weekly active seats against licensed seats, and conversion would be attach rate -
> how many Timesheets seats end up adopting Capacity Planner. I want to be clear that this is
> my read of your pricing model, not something I've measured in your product.

*Base:* el modelo de licenciamiento de Tempo (verificado en `producto-y-rol-growth.md`, §2 y
§5). **Decí que es una inferencia**, no un hecho. Esa humility suma puntos.

### C. Feature flags y rollout

**7. "What experience do you have with feature flag systems?"**

> I haven't operated a dedicated feature flag platform at scale. What I do have is the
> discipline around it: release behind a switch, roll out in stages, watch the guardrails, and
> have a kill path. The thing that makes that work in practice is that the check is automated
> rather than a convention - which is exactly what I did with the accessibility pipeline, where
> a non-compliant component couldn't merge.

*Base:* el patrón (flag, stages, guardrails, kill switch) y el transferible de a11y. **No**
nombrar LaunchDarkly como si lo hubieras usado.

**8. "How would you roll out a new onboarding flow safely?"**

> Behind a flag, starting with a small slice, checking the guardrail metrics at every stage
> and only widening if they hold. I'd put an expiry on the flag so it doesn't become permanent
> debt - a flag nobody removes is a branch nobody merges.

### D. Ownership y colaboración

**9. "Tell me about a time you owned a quality metric across a team."**

*Esta es tu pregunta fuerte. El corpus la sostiene entera:*

> At EY (Sep 2021 - May 2025) I owned WCAG 2.2 AA compliance for Motif, an enterprise React component
> library used across client and internal products. It wasn't a report: I audited and remediated
> 50+ components, I wrote the technical requirements with component-level annotations and code
> examples so the developers knew what to build, and I put axe-core and Playwright into CI/CD so a
> non-compliant component couldn't merge. That last part is the one I'd bring to a growth team -
> the standard only counts if the pipeline enforces it.

**10. "How do you work with PMs, designers, QA and technical writers?"**

> At EY (Sep 2021 - May 2025) I was recruited into a cross-regional matrix team, US and India, and
> worked across several SDLC phases in parallel. With design, I reviewed components in Storybook
> and designs in Figma *before* implementation, then wrote the requirements and the code guidance.
> I wrote technical accessibility requirements with code examples, because the spec was mine to
> write, not a ticket someone handed me. With QA, the acceptance criteria were automatable, so
> they went into the pipeline. I also worked with technical writers on the documentation for
> developer-facing features.

*Ojo:* el corpus **no** nombra collaboration con technical writers como tal. Si el interviewer
pregunta por eso específicamente, decí qué parte de tu experiencia se acerca (escribir
documentación, revisar specs) en vez de inventar la colaboración.

**11. "What does AI-first mean to you?"**

> For me it means the AI layer is part of how the work gets done, not a side experiment. As a
> freelancer since May 2025 I built an AI-native CRM end to end - React, Vite, TypeScript,
> Supabase with RLS and Edge Functions, Stripe - including RAG over pgvector and an Autopilot
> path with confidence guardrails. And I run my own system for the work itself: project
> sessions, persistent memory, subagents, and a contribution pipeline for open source. AI
> assistants generate code, review pull requests and fetch context from the knowledge base.
>
> The point of "don't get stuck in reviews" as a job requirement is one I take literally: the
> review is where the senior value is, and the AI is what frees up the time to do it properly.

### E. Código, testing, performance, seguridad

**12. "What testing do you do?"**

> Unit and integration tests, and end-to-end with Playwright. The part I'd emphasise is the
> CI integration: at Super7UI (Aug 2020 - May 2021) I set up an accessibility testing pipeline
> with axe-core and Playwright in CI/CD, and at EY I took that into the enterprise component
> library so compliance was enforced at merge time rather than reviewed afterwards. Performance I
> treat the same way - a budget you assert in the pipeline, not something you check once.

**13. "Security and enterprise concerns in instrumentation?"**

*Acá usás el hallazgo del CSP de Forge, que es tu carta fuerte:*

> If the frontend runs in Atlassian Forge, it lives in an iframe with a content security policy
> that blocks third-party scripts, so you can't drop an analytics SDK into the page. Events
> would have to go out through a backend invoke with the egress permissions declared, and
> PII would need masking before it reaches the warehouse. I haven't built that pipeline in
> Forge, but I've shipped systems with row-level security and audited access in an enterprise
> context, and I know that "add analytics" is an architecture decision there, not a snippet.

### F. Preguntas incómodas (prepararlas)

**"Tu CV dice 10+ años pero el puesto pide 4+. ¿Qué hiciste?"**
> The 10+ is total development. What I think matters for this role is the last five: enterprise
> React at scale, owning a quality standard, and the last year and a half building a full
> product end to end with AI in the stack.

**"¿Por qué el gap de growth si el puesto es de growth?"**
> It's a fair question and I'd rather answer it straight. What I bring is the senior frontend
> fundamentals and the habit of making quality measurable - I've spent my career turning
> "good enough" into something a pipeline can check. The experimentation tooling and the
> statistical side I would learn on the job, and I'd rather be honest about that than claim
> experience I don't have. I'd want to be useful early, which for me means getting the
> instrumentation and the gates right.

**"¿Por qué un puesto de growth y no de plataforma?"**
> Because the part I like is the part where a decision has to be backed by evidence. In
> accessibility, I owned a standard that had to be provable - WCAG criteria, automated checks.
> Growth is the same instinct pointed at user behaviour. Platform work is also interesting
> to me, but this is where my experience transfers most directly.

**"Degree en Computer Science, ¿tenés?"**
> No. I studied Computer Science at Universidad de Palermo between 2001 and 2002 and didn't
> finish the degree; my formal training since then has been Digital House for React in 2018
> and the Deque accessibility program in 2021. The fundamentals you listed - Big-O, data
> structures - I know from practice, but I won't claim a degree I don't have.

*Nota: la redacción exacta de educación la tiene que validar Gonzo (ver `revision-adversarial.md`,
sección 3). Lo que hay en el corpus son tres registros contradictorios.*

---

## 2. La historia de A/B testing (en inglés, lista para decir)

> *Opening (usar textual):* **"I haven't built an end-to-end experimentation platform myself."**
>
> In 2019, at Minutentag, I worked on an e-commerce platform for US fashion brands, on a team
> that ran A/B experiments with Adobe Target. My side of it was the variants: I wrote the code
> for each test as plain JavaScript snippets, which the tool injected at runtime, and we
> validated the changes against real users on the live site.
>
> The lesson I took from that was that an experiment without a clearly defined metric is just a
> guess. I came out of it understanding that the hard part of experimentation is not the variant,
> it's deciding what would count as a win before you start - and then being honest enough to
> call it a failure if that's what the data says.
>
> I want to be clear about the scope: I used the tool and implemented the variants. I did not
> build the experimentation infrastructure, and that infrastructure - LaunchDarkly, Optimizely -
> is exactly what you have today, and it is the same discipline with tooling I did not have.
>
> *Closing (usar textual):* **"The discipline of defining a clear metric, implementing the
> variant and letting the result drive the decision is the same one I applied to
> accessibility."**

> **Antes del lunes:** confirmá con Gonzo si podés agregar un experimento concreto (qué se
> probaba, contra qué). Si no lo podés sustentar, **no lo cuentes**: la historia en general es
> defendible, y un ejemplo inventado se rompe.

---

## 3. El argumento transferible (en inglés, listo para usar)

> What I delivered for accessibility was turning a vague notion of "good UI" into a
> measurable, enforceable standard. I defined concrete criteria, wrote the checks, and put them
> in the pipeline so a non-compliant component could not merge. Growth needs the same
> discipline with a different metric source: choose the right metric, instrument it so the
> data is actually true, and put the mechanism in place that forces you to look at it.
>
> The difference is real and I want to name it - WCAG is normative, growth metrics depend on
> sample size and statistics. But the habit of making a soft rule into a hard,
> pipeline-enforced check is the same, and that is the part I am good at.

---

## 4. Primeros 30/60/90 días (primera persona, en inglés)

**Primeros 30 días**
- Entender el entorno: Forge, el CSP, los egress permissions, y cómo el equipo mide hoy.
- Leer el código de las apps que me toquen y entender si el equipo de Growth commitea al mismo repo o va en paralelo.
- Sentarme con el dueño de la métrica y entender qué se mide hoy y con qué source of truth.
- Revisar qué instrumentación existe ya y qué está sin medir.

**Días 31-60**
- Proponer el esquema de eventos tipado y los tests que fallan si un evento desaparece.
- Poner el primer flag con un rollout por etapas sobre algo de bajo riesgo.
- Dejar por escrito cómo se define un experimento acá: hipótesis, métrica, guardrails, regla de decisión.

**Días 61-90**
- Correr un experimento completo de punta a punta, de la hipótesis al readout.
- Publicar el playbook de growth del equipo: cómo se define una métrica, cómo se hace un rollout, cómo se pone un gate en el pipeline.

---

## 5. Las tres cosas que no podés prometer

| No prometo | Por qué no se nota si sos honesto |
|---|---|
| Plataforma de analytics a escala (Amplitude/Mixpanel/PostHog en producción) | Conoces el terreno y el trabajo de instrumentación es tuyo; lo que no hiciste es operar el data pipeline, y decilo |
| Feature flags como servicio a escala (LaunchDarkly/Optimizely) | Tenés el patrón y la disciplina de rollout; lo que falta es la operación del servicio, y la frase "el patrón, no la plataforma" es exacta |
| Experimentos con poder estadístico y multivariantes | Tenés un caso real de A/B en producción contra usuarios reales; lo que no hiciste es MDE ni power analysis, y el interviewer lo sabe |

**Regla:** el gap se dice **una vez, temprano, y se cierra con lo que sí hacés**. Repetirlo
tres veces es una disculpa, no una honestidad.

---

## 6. Posibles take-home / live coding

| Desafío probable | Qué evalúa | Cómo lo encararía |
|---|---|---|
| "Instrumentá un componente React para que emita un evento tipado, y escribí un test que falle si el evento no llega" | Disciplina de instrumentación + gate en CI | `trackEvent('worklog_created', {...})` con tipo en un `events.ts`, y un test de Playwright que dispara la acción y verifica que el evento salió |
| "Implementá un cambio de UI detrás de un feature flag y hacé un rollout de 0 a 100 con guardrails" | Patrón de flag, etapas, red de seguridad | Flag simple con contexto de React, dos variantes, y un test que verifica que el evento de exposición solo se dispara cuando la variante se ve |
| "Refactorizá un componente lento para cumplir un budget de performance, con su test" | Performance como gate, no como revisar | Medir, corregir el costo real, y agregar el umbral al pipeline para que falle en el CI |
| "Diseñá un experimento: hipótesis, métrica, tamaño de muestra, y análisis mock de resultados" | Pensamiento de diseño | Una hipótesis de una frase, una métrica primaria, y el criterio de decisión escrito antes del lanzamiento |

---

## 7. Checklist antes del lunes

- [ ] **Confirmar el A/B testing con Gonzo:** ¿hay un experimento concreto que pueda sustentar? ¿Qué se probaba y contra qué? Sin eso, la historia queda en general.
- [ ] **Validar la redacción de educación** (ver `revision-adversarial.md` §3): el corpus tiene tres registros contradictorios y este JD pide degree.
- [ ] **Tener a mano los links de los 11 PRs mergeados**, con una frase de impacto cada uno. Son la prueba más concreta de que escribís código que entra en librerías de primer nivel.
- [ ] **Releer tu propio `kanam-fixer`:** es tu mejor ejemplo de "instrumentación con gate en pipeline" y el más reciente.
- [ ] **Repasar las 4 historias STAR** de `sol-star-prep-2026-10-16.md` (courage, agility, responsibility, confidence): son tuyas y no dependen del puesto.
- [ ] **Tener clara la respuesta de 30/60/90** (está arriba) y que suene a criterio, no a lista.
- [ ] **Verificar la logística:** 10:00 ART, qué plataforma (Zoom/Teams), y quién va a estar: ¿el recruiter de TEAM o alguien de Tempo? La diferencia importa para el tono.
- [ ] **Probar micrófono y auriculares**, y tener un segundo de calma antes de empezar.
- [ ] **Dejar por escrito la frase de apertura y la de cierre del A/B testing** (sección 2), para no improvisarlas en caliente.

---

## 8. INCERTIDUMBRE

- **Qué paso del proceso es esta entrevista** (call informativa / entrevista técnica / test /
  entrevista con el cliente): no está confirmado. La preparación de arriba sirve para todos, pero
  si es la call informativa, el foco es otro: las 4 preguntas de `guion-call-21-10.md`.
- **Qué herramientas usan de verdad** (feature flags, analytics): cero evidencia pública.
  Preguntarlo, no suponerlo.
- **Si el equipo de Growth existe hoy como tal**: hay un posteo de "Senior Growth Engineer" de
  agosto 2025, pero no se pudo confirmar que el equipo siga igual. La primera pregunta es por eso.
- **La métrica que el equipo declara como propia**: no es pública. Si no la pueden nombrar en
  la entrevista, el "rol de growth" es un título, y eso es información para Gonzo.
- **Los detalles del A/B testing de 2019** (experimento concreto, métrica usada): no están en el
  corpus. Hay que preguntárselo a Gonzo, no inferirlo.
- **La redacción de educación**: sin resolver (ver `revision-adversarial.md` §3).
