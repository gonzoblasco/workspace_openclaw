# Tempo.io - Qué es el producto y qué hace un "Senior Frontend Developer (Growth)"

**Entrevista:** lunes 26/10/2026, 10:00 ART
**Puesto:** Senior Frontend Developer (Growth), Tempo Software, vía TEAM International
**Consultado:** 2026-10-21
**Regla de este documento:** cada afirmación está marcada como **[CONFIRMADO]** (fuente abierta y leída), **[PROBABLE]** (inferencia con base) o **[SUPOSICIÓN]** (hipótesis a validar en la entrevista). Nada se presenta como hecho sin fuente.

---

## 1. Resumen ejecutivo: qué es Tempo hoy (5 líneas)

1. Tempo es un vendor del ecosistema Atlassian, fundado en 2007 en Reikiavik, hoy con sede en Boston: vende **apps que se instalan dentro de Jira** para medir tiempo, capacidad, costo y portafolio. **[CONFIRMADO]**
   **Geografía de oficinas (verificada 26/10/2026, hora de idioma):** Boston MA (sede), Burlington MA, Burlington VT, **Reykjavík (Islandia, origen)**, **Montréal QC (Canadá)**. Fuente: Lead Edge Capital job board (portfolio company, `jobs.leadedge.com`), Glassdoor (3 oficinas), y la noticia de adquisición de ALM Works (Boston/Reikiavik/Montréal).
   **Dato que importa y que desmiente una generalización fácil:** el equipo del cliente que entrevista para este rol está en **Europa**, pero **Reikiavik es lingua franca en inglés** (verificado: la propia documentación académica islandesa sobre comunicación en empresas multinacionales, y el gobierno de Islandia describe el inglés como la lingua franca de la vida cotidiana). **O sea: "el equipo está en Europa" NO implica "el equipo no es angloparlante".** La exigencia de Tempo era de **nivel de fluidez para discutir y explicar temas técnicos**, no de lengua materna. La geografia no predice nada: el filtro real es de **nivel**, no de pais.
2. Su positioning actual ya no es "time tracking": es **"Intelligent Portfolio Orchestration" (IPO)** - "Portfolio Management Software for the AI Enterprise", con un producto nuevo, **Tempo Loop**, que orquesta personas *y agentes de IA* contra la estrategia. **[CONFIRMADO]**
3. Sigue siendo dueño **Diversis Capital** (private equity): mayoría en 2018, 100% en 2022, y una **recapitalización apalancada cerrada en septiembre 2025** - o sea, empresa con deuda y presión de eficiencia, no un startup. **[CONFIRMADO]**
4. Escala: **30.000+ clientes**, un tercio del Fortune 500, **53% del Fortune 100**, 350+ partners; superó **$100M ARR en 2022**. **[CONFIRMADO]**
5. El rol "Growth" cae sobre un negocio **seat-based dentro de Jira**: la palanca de ingresos es que más gente en la instancia use las apps y que se sumen módulos. Eso define qué experimentos tienen sentido. **[CONFIRMADO el modelo de precios / PROBABLE la consecuencia]**

---

## 2. Quién es quién (para no confundir el mapa)

| Actor | Rol | Qué implica para vos |
|---|---|---|
| **Tempo Software** | El cliente final. El producto es de ellos. | Tu trabajo real es para Tempo; TEAM es el intermediario. |
| **TEAM International** | Consultora de staffing/outsourcing que recluta para Tempo. | El contrato, el rate y el modelo de employment los maneja TEAM. Preguntá si es *staff augmentation* (sos un contractor de TEAM dentro del equipo de Tempo) o *outsourcing por proyecto*. Cambia todo: acceso a métricas, ownership, duración. |
| **Diversis Capital** | Fondo PE dueño de Tempo. | Explica el foco en eficiencia, márgenes y "growth medible". |
| **Atlassian** | Plataforma sobre la que corre el producto (Forge, Marketplace). | Es un tercero con poder de veto técnico: sus reglas de CSP y egress limitan lo que podés instrumentar. |

> **[SUPOSICIÓN]** Que la entrevista la haga alguien de TEAM y no de Tempo es señal de que el filtro inicial es de staffing. Conviene detectar temprano si del otro lado hay un hiring manager de Tempo: eso determina si el puesto tiene dueño técnico real.

---

## 3. Verificación punto por punto de los hechos que traías

### 3.1 ¿Sigue siendo "Portfolio Management Software for the AI Enterprise"? - **SÍ [CONFIRMADO]**

La home de tempo.io hoy tiene exactamente ese `<title>`, y el H1 es **"INTELLIGENT PORTFOLIO ORCHESTRATION - Ambition delivered at the speed of AI"**. Textual de la home:

- *"Direct every human, every agent, and every dollar to the work that matters most."*
- *"Trusted for over 20 years in time, cost, and project and portfolio management."*
- *"Tempo connects work across Jira, Azure DevOps, Linear, and the systems your teams already use."*
- Bloque de seguridad: **SOC 2 Type II / ISO-IEC 27001 Certified / GDPR Compliant**.
- Testimonio destacado: Jamie Stanley, SiriusXM.

**Lo que cambió respecto de tu info:** el discurso se corrió de "time tracking + PPM" a **"un modelo operativo para personas y agentes de IA"**. Ya no venden software de horas; venden gobernanza del gasto en IA y de la capacidad híbrida humano-agente.

### 3.2 Tempo Loop - **existe y es el producto estrella [CONFIRMADO, con matiz]**

- Loop es *"Tempo's first ecosystem-independent platform"*, arranca conectado a **Jira y Azure DevOps**, con otros sistemas "en los próximos meses".
- Ciclo: **See → Decide → Orchestrate → Adapt**. Detecta *strategic drift*, recomienda una acción con datos, y **escribe el cambio de vuelta en los sistemas conectados** ("dynamically updates your systems to reflect the change you've just approved").
- Gobierna el nivel de autonomía: de *recommend-only* a más autonomía "over time".
- Métricas que ellos mismos publican de early customers: 85% mejora en mantener estrategia y ejecución conectadas, 38% delivery más rápido, 82% mejor replanificación.

**Matiz importante:** existen las rutas `/loop-eap` y `/learning-center/tempo-loop` en el sitemap, lo que sugiere **early access / EAP** más que GA plena. **[PROBABLE: Loop todavía está en rollout, no masificado]**. En la entrevista conviene preguntar si el equipo de Growth trabaja sobre Loop o sobre las apps de Jira - son dos productos con superficies de growth completamente distintas.

### 3.3 Dueño y estructura corporativa - **Diversis, con recapitulación 2025 [CONFIRMADO]**

| Fecha | Evento | Fuente |
|---|---|---|
| Nov 2018 | Diversis Capital adquiere mayoría | tempo.io/news |
| 2022 | Diversis compra el resto (salida de Origo hf) | PRNewswire / PE Hub |
| Jun 2024 | Diversis corre proceso de single-asset (busca salida o recap) | PE Hub |
| **Sep 3, 2025** | **Leveraged recapitalization** asesorada por Paul, Weiss | paulweiss.com |

**Lectura:** una recap apalancada significa que el fondo **extrajo liquidez y cargó deuda a la empresa**. Consecuencia práctica para un candidato: presión por métricas de eficiencia, headcount cuidadoso, y probablemente un mandato explícito de "growth con ROI demostrable". No es un lugar donde un experimento sin métrica sobreviva mucho. **[PROBABLE]**

### 3.4 Adquisiciones - el producto es un roll-up [CONFIRMADO]

| Año | Adquisición | Qué aportó | Producto actual |
|---|---|---|---|
| Nov 2021 | **Roadmunk** | Roadmapping | Strategic Roadmaps (Roadmunk) |
| 2022 | **ALM Works** (Structure for Jira, ~5.000 organizaciones) | Jerarquías/portafolio | Structure PPM + Gantt Charts |
| Mar 2023 | **LiquidPlanner** | Predictive scheduling (Monte Carlo) | Portfolio Manager (LiquidPlanner) |

Esto importa: Tempo no tiene *un* frontend. Tiene **varias bases de código heredadas de distintas empresas**, cada una con su stack y su deuda. Un puesto "Growth" en esta empresa muy probablemente implique trabajar en la capa nueva (Loop y/o las apps Cloud), no en todo.

### 3.5 Números de cliente y de negocio - **CONFIRMADO, con cifras que se contradicen entre fuentes**

| Dato | Valor | Fuente / año |
|---|---|---|
| Clientes | **30.000+** | Home + JD + Loop blog (2026) |
| Fortune 500 | **1 de cada 3** | JD (2026) |
| Fortune 100 | **53%** | Blog "What is Loop" (2026) |
| Partners | **350+** (Accenture, PwC nombrados) | Blog Loop / press release |
| Clientes nombrados | Cisco, Airbus, Oracle, SiriusXM, Škoda, BAE Systems, Staples, BDO | Press releases / customer stories |
| ARR | **> $100M (2022)**, Rule of 40 | Press release LiquidPlanner (mar 2023) |
| Empleados | **402** (LinkedIn, +26% YoY) vs **328** (Revelio, mar 2026) | **En conflicto** - ver §12 |

> **Ojo con el histórico:** en 2022 decían 20.000 clientes, en 2023 28.000, hoy 30.000. El crecimiento de base es real pero se está desacelerando en términos relativos. **[PROBABLE]**

### 3.6 El conector multi-herramienta - **CONFIRMADO y es la apuesta estratégica**

Jira + Azure DevOps + Linear. Esto es lo que separa Loop de las apps de Jira: **Loop no vive dentro de Atlassian**. Es la jugada para dejar de ser un vendor cautivo del Marketplace y pasar a ser plataforma propia. Si te preguntan "¿por qué Tempo?", esta es la respuesta estratégica correcta.

---

## 4. Tabla de las apps (el catálogo real, verificado en tempo.io/products y /pricing)

**Corrección a tu lista:** ya no se llaman "Tempo Planner" ni "Tempo Account" ni "Tempo Teams" como productos separados - Planner se renombró **Capacity Planner**, y Accounts/Teams pasaron a ser **features dentro de Timesheets**. **[CONFIRMADO]**

| App | Qué hace | Usuario primario |
|---|---|---|
| **Timesheets** | Time tracking nativo en Jira. Worklogs con contexto financiero (billable/no billable, CapEx/OpEx), aprobaciones por equipo y por proyecto, reportes, sugerencias automáticas desde calendario/IDE/Slack, agente Rovo para loguear tiempo. "El #1 time tracking para Jira". | Dev individual (loguea), team lead (aprueba), finance (consume) |
| **Capacity Planner** (ex Tempo Planner) | Planificación de capacidad y recursos: asigna personas y equipos a issues/proyectos, sync bidireccional con Jira, vista de FTE planificado vs disponible, detección de sobreasignación. Único en el Marketplace que permite planificar **múltiples recursos en un mismo issue**. | PM, resource manager, PMO |
| **Financial Manager** (ex Tempo Budgets) | Costos, presupuestos, revenue, CapEx/OpEx, earned value. **Requiere Timesheets** para funcionar (consume worklogs). Portfolios para agregar varios proyectos. | Finance, PMO, project owner |
| **Structure PPM** (ex ALM Works) | Jerarquías de issues personalizadas en vista tipo planilla, fórmulas, tracker de epics/proyectos, sprint planner, release management. Incluye **Structure Formula Assistant** (agente Rovo que escribe fórmulas en lenguaje natural). | Program manager, PMO, portfolio lead |
| **Gantt Charts for Structure PPM** | Gantt sobre Structure. "#1 add-on de Structure". | PMO |
| **Custom Charts for Jira / Confluence** | Dashboards y gráficos custom sobre datos de Jira y de Tempo. | Jira admin, PM |
| **Strategic Roadmaps** (ex Roadmunk) | Roadmaps multi-vista, portfolio roadmaps, Idea Manager, feedback vinculado a ideas. Integra Jira, Azure DevOps, Asana, Monday, Trello, GitHub, GitLab. | Product manager, exec |
| **Portfolio Manager** (ex LiquidPlanner) | Predictive scheduling con **simulaciones Monte Carlo** y fechas al 90% de confianza, leveling automático de carga. Producto standalone + integración Jira/Slack. | PMO de portafolios complejos |
| **Workforce Intelligence** ⭐ nuevo | Atribución de actividad de **agentes de IA a issues de Jira**: telemetría de inference APIs, esfuerzo humano+IA combinado, costo. Responde "¿qué nos costó la IA y qué entregó?". Lanzado **25/08/2026**. | Engineering leader, CFO, CTO |
| **Conectores BI** | Power BI, Tableau, BigQuery para Jira (y Power BI para Monday/ServiceNow). | Data/analytics team |
| **Tempo Loop** | La plataforma nueva, ecosystem-independent (ver §3.2). | PMO, strategy, exec |

**Modelo de precios [CONFIRMADO en /pricing]:** por usuario de Jira, y **la licencia de Tempo debe igualar el tamaño de la licencia de Jira**. Cloud tope 100.000 usuarios. Ejemplo Timesheets: $10/user/mes flat de 1-10, $5.99 de 11-100, $4.21 de 101-250, bajando hasta $0.28 en volúmenes grandes.

> **Esto es la clave de todo el rol.** Tempo no tiene un funnel de signup como una SaaS normal. Tiene: **Marketplace listing → trial de instancia → activación de la instancia → uso por asiento → upgrade de tier → attach de otro módulo**. El "growth" acá es en buena parte **product-led growth dentro de una instancia ajena (Jira del cliente)**, con un admin como gatekeeper. Cualquier respuesta tuya sobre funnels que ignore eso va a sonar genérica.

---

## 5. Qué es "Growth" en una empresa B2B como esta

### 5.1 El modelo mental correcto

Growth no es marketing. Growth es **un equipo con ownership de una métrica del funnel, que cambia el producto para moverla**. La diferencia con un equipo de plataforma:

| | Frontend de plataforma | Frontend de Growth |
|---|---|---|
| Pregunta que responde | "¿Cómo construimos esta feature bien?" | "¿Esta feature mueve la métrica, y cómo lo sabemos?" |
| Unidad de entrega | Feature shipped | **Aprendizaje validado** |
| Métrica de éxito | Latencia, cobertura, correctness | Activación, retención, conversión, NRR |
| Velocidad | Ciclos de release planificados | Semanas; experimentos de bajo costo, alto volumen |
| Tolerancia al fracaso | Baja (no podés romper el core) | **Alta y explícita: un test que pierde es un resultado** |
| Riesgo principal | Deuda técnica | **Métrica vanity / test inválido / novelty effect** |
| Herramientas propias | CI, observabilidad, design system | **Feature flags, A/B, event tracking, dashboards** |

### 5.2 Las 6 tareas concretas de una semana típica

*(Inferido del JD + práctica estándar de growth engineering. Marcado **[PROBABLE]** - validar en la entrevista.)*

1. **Instrumentar.** Agregar eventos a un flujo existente con una taxonomía consistente (`object_action`: `timesheet_submitted`, `worklog_created`, `trial_activated`). Definir propiedades, validar que lleguen, y **escribir el test que falla si el evento desaparece** - el equivalente frontend de un contrato de API.
2. **Construir la variante.** Implementar una variante de UI (copy, orden de pasos, onboarding, empty state) detrás de un flag, con la misma calidad que código de producción: tipos, tests, accesibilidad, performance.
3. **Diseñar y correr el experimento.** Hipótesis escrita, métrica primaria, métrica de guarda (la que no podés empeorar), tamaño de muestra y MDE calculados antes de lanzar, regla de decisión definida de antemano.
4. **Leer el resultado y decidir.** Ship / kill / iterate. Documentar el aprendizaje aunque haya perdido. Actualizar el *results log*.
5. **Arreglar fricción de funnel.** Mirar dónde se cae la gente (drop-off en el wizard de instalación, en el primer worklog, en la invitación de un compañero) y sacar hipótesis de ahí.
6. **Colaborar y desbloquear.** PM para priorizar, diseño para la variante, data para validez estadística, QA para no romper producción, y **el equipo de plataforma** para no construir un fork paralelo del design system.

### 5.3 Qué métricas mira (aplicadas al modelo de Tempo)

| Etapa | Métrica | Cómo se ve en Tempo específicamente |
|---|---|---|
| **Activación** | Time-to-first-value | Instalación → primer worklog creado. Y a nivel instancia: instalación → primer proyecto configurado con cuentas/equipos |
| | % de asientos activados | Usuarios con licencia que loguearon ≥1 vez en 14 días |
| | Completion rate del onboarding | Cuántos admins terminan de configurar workload schemes, holidays, accounts |
| **Retención** | **Seat utilization** | WAU / asientos licenciados. Si es bajo, el cliente no renueva al mismo tier |
| | Retención de instancia D30/D90 | Instancias que siguen activas tras el trial |
| | Ciclo de aprobación completado | Timesheets sin aprobar = fricción que precede al churn |
| **Conversión** | Trial → paid (nivel instancia) | El trial es de la instancia entera, no de un usuario |
| | **Attach rate / cross-sell** | Timesheets → Capacity Planner → Financial Manager. Este es el motor real de ARR |
| | Expansión de asientos | Cliente suma gente en Jira = sube el tier automáticamente |
| **Calidad del experimento** | Guardrails | Performance (el editor de timesheet tiene que ser rápido), error rate, a11y |

> **[PROBABLE]** En un negocio seat-based con licencia atada al tamaño de Jira, el growth de mayor leverage casi nunca es "traer usuarios nuevos" sino **"que los asientos que el cliente ya paga se usen"** y **"que la instancia sume el módulo siguiente"**. Si decís esto en la entrevista, vas a sonar como alguien que entendió el negocio, no como alguien que memorizó un framework.

### 5.4 Herramientas del rubro (para nombrarlas con criterio, no para fingir uso)

| Categoría | Herramientas | Nota para la entrevista |
|---|---|---|
| Product analytics | **Amplitude, Mixpanel, PostHog** | PostHog es la opción obvia si querés self-host y control de datos (relevante con SOC 2) |
| Experimentación / A/B | **Optimizely, LaunchDarkly (Experimentation), GrowthBook, Split** | GrowthBook es open source y barato; LaunchDarkly es el estándar enterprise |
| Feature flags | **LaunchDarkly, Unleash, GrowthBook, Split** | Preguntá cuál usan - define si el flag es solo un booleano o un sistema de targeting |
| Session replay / qual | FullStory, Hotjar, LogRocket | Ojo con PII: en enterprise esto se audita |
| Warehouse / CDP | Segment, Snowflake, dbt | En enterprise, los eventos suelen terminar en el warehouse, no en la tool |

**Cómo hablar de esto sin mentir:** "Conozco el landscape y sé para qué sirve cada categoría y cuáles son los trade-offs (self-host vs SaaS, costo por evento, control de PII). Lo que no tengo es haber operado un stack de experimentación en producción a escala. Eso lo aprendo rápido porque la parte difícil no es la tool, es la disciplina del experimento." - Eso es honesto y es exactamente lo que un buen hiring manager quiere oír.

---

## 6. El stack probable de Tempo

| Capa | Qué | Estado | Evidencia |
|---|---|---|---|
| UI framework | **React** | **[CONFIRMADO]** (histórico) | Artículo de ingeniería de Tempo: el frontend monolith de Tempo Cloud era "ReactJS, Redux, ImmutableJS" |
| Lenguaje | **TypeScript + JavaScript** | **[CONFIRMADO]** | JD: "1+ año en TypeScript con React"; "Excelente conocimiento de TypeScript, JavaScript, CSS3, HTML5" |
| Estado | Redux/Immutable en el monólito; Context + hooks en módulos nuevos | **[CONFIRMADO]** (2020) | Mismo artículo: migraron de un HOC propio a "Context powered hook based state management, completely typesafe" |
| Testing | **react-testing-library** (test what you see), unit + integration | **[CONFIRMADO]** (2020) | Mismo artículo, explícito |
| Bundler/serving | Django (monólito) y Flask (Cost Tracker) sirviendo bundles | **[CONFIRMADO]** (2020) | Mismo artículo |
| Backend | **Java / Kotlin** | **[CONFIRMADO]** | JD: "Experiencia con Java/Kotlin es un plus"; repo público `tempo-events-example` en Kotlin; los interview test tasks del GitHub de Tempo son en **Java** |
| Plataforma | **Atlassian Forge Remote** | **[CONFIRMADO]** | Blog + product-news: frontend pasa a estar hosteado por Atlassian, backend queda en Tempo. Migración arrancó **31/03/2026** |
| Design system | **Atlassian Design System** | **[PROBABLE]** | Forge Custom UI docs recomiendan explícitamente Atlassian Design System para consistencia; es lo estándar en apps de Marketplace |
| Feature flags | Desconocido | **[SUPOSICIÓN]** | No hay evidencia pública. Es la pregunta más importante que podés hacer |
| Analytics | Desconocido | **[SUPOSICIÓN]** | Ídem |
| IA en producto | **Rovo agents** (Atlassian) + agentes propios | **[CONFIRMADO]** | Structure Formula Assistant, "ask your Rovo Agent to log time", Workforce Intelligence |

### 6.1 Repos públicos de Tempo - hay muy poco, y eso también es un dato

`github.com/tempo-io` existe y está verificado contra el dominio tempo.io. Contenido:

- `tempo-events-example` (Kotlin, 8 stars) - ejemplo de listener de eventos Jira
- `jiraclient`, `deskzilla` (Java, viejos)
- `as-interview-test-task` y `as-interview-test-task-middle-dc` (**Java**) - **los tests técnicos de sus entrevistas son backend**
- `html-to-image` (fork de TypeScript, 717 forks) - la única cosa frontend
- `custom-charts-api-docs`, `primetimesheet.net`, `timereports.primetimesheet.net` (legacy)

**Conclusión:** no hay frontend público. No vas a poder leer su código React. Y el dato lateral es interesante: **sus pruebas técnicas públicas son de Java**, lo que históricamente sugiere un perfil más full-stack/backend-leaning que frontend puro. Para un puesto *Growth* frontend eso probablemente ya cambió, pero vale preguntar cómo es el proceso técnico.

### 6.2 La restricción técnica que casi nadie ve venir: Forge y el CSP

Esto puede ser tu mejor carta en la entrevista. **[CONFIRMADO en docs de Atlassian]**

Cuando el frontend corre en **Forge Custom UI**, la app vive en un **iframe** con un Content Security Policy por defecto que:

- **Bloquea scripts de orígenes externos** - textual: *"you cannot use scripts or images from external sources, such as Google Analytics or Sentry, in your static assets"*.
- **Bloquea fetch a APIs externas desde el frontend** - hay que pasar por `invoke()` a una función backend de Atlassian, y desde ahí salir.
- Existe un mecanismo de **content security and egress controls** para habilitar dominios externos explícitamente, con permisos.

**Traducción para growth:** no podés pegar el snippet de Amplitude en el `<head>` y listo. Instrumentar requiere **diseñar el pipeline de eventos** (frontend → `invoke` → backend de Tempo → collector), declarar egress permissions, y justificarlo ante security. Eso convierte "agregar analytics" en un problema de arquitectura, no de copy-paste.

> Si en la entrevista decís: *"Asumo que con Forge Remote el CSP les impide cargar SDKs de analytics de terceros en el frontend, así que los eventos tienen que salir por el bridge o por el backend. ¿Cómo lo resolvieron?"* - demostrás que leíste la plataforma, no solo el JD. Es una pregunta que muy pocos candidatos pueden hacer.

---

## 7. El JD: lo que dice públicamente y lo que no

Verifiqué la versión pública del aviso "Senior Frontend Developer (Growth)" (Built In, HubMub, ambos cacheados; el original de Ashby ya está dado de baja). **Hallazgo relevante:**

La versión pública **no menciona A/B testing, feature flags, analytics ni métricas de activación/retención/conversión**. Dice:

> "We are looking for a passionate front-end developer... You will collaborate with product managers, designers, developers, QA engineers, and technical writers to develop some of our flagship products - **Tempo Timesheets, Capacity Planner and Financial Manager for Jira Cloud**."

Y los requisitos son los genéricos: 4+ años frontend comercial, 1+ año TS+React, CS fundamentals (big-O, estructuras, algoritmos), TS/JS/CSS3/HTML5, UIs complejas, usabilidad, performance, inglés upper-intermediate, autonomía remota, Java/Kotlin un plus.

**Interpretación [PROBABLE]:** hay dos posibilidades, y conviene cubrir ambas:
- **(a)** El JD que te pasó TEAM International es una **versión adaptada/ampliada** - le agregaron el bloque de growth porque el equipo realmente lo necesita. Entonces el texto que tenés es más preciso que el público.
- **(b)** Es un **req distinto** con el mismo título (Tempo postea el mismo rol en varias geos: Argentina, Canadá, UK, España, Portugal, Polonia, Ucrania, Irlanda, Eslovaquia, Rumania).

**Dato de apoyo a (a):** Tempo sí tiene una función de growth con perfil frontend. En agosto 2025 publicaron **"Senior Growth Engineer"** con stack explícito **TypeScript, React, JavaScript, HTML5, CSS3**, para *"help shape the future of Structure for Jira Cloud"*. Eso confirma que existe el equipo y que es frontend. **[CONFIRMADO el posteo; [PROBABLE] que siga existiendo]**

> **Acción concreta:** llevá el JD que te dieron impreso y, si surge, preguntá: *"El aviso público no menciona experimentación ni flags; el que me pasaron sí. ¿Cuál es la versión vigente del rol?"* Es una pregunta legítima y te posiciona como alguien que hizo la tarea.

---

## 8. Preguntas que te van a hacer - y qué responder

> **Regla:** todo lo que sigue usa **solo hechos reales de tu carrera**. Donde no tenés experiencia directa, la respuesta es honesta y explícita. Inventar growth es la forma más rápida de perder este proceso: el interviewer va a repreguntar dos veces y se cae.

### 8.1 Técnicas de growth

---

**P: "¿Cómo diseñás un experimento A/B?"**

Estructura la respuesta en 7 pasos, en ese orden, porque el orden *es* la respuesta:

> "Antes de tocar código escribo la hipótesis en una frase falsable: *'Si cambio X, entonces la métrica Y sube Z%, porque [razón basada en evidencia]'*. Si no puedo escribir el 'porque', no tengo hipótesis, tengo una corazonada.
>
> Después fijo cuatro cosas **antes** de lanzar: la **métrica primaria** (una sola), las **métricas de guarda** que no puedo empeorar, el **MDE** (minimum detectable effect) que me interesa detectar, y el **tamaño de muestra** que necesito para detectarlo con la potencia adecuada. De ahí sale la duración: no se decide mirando el calendario, se decide mirando cuántos usuarios por semana entran al flujo.
>
> La **regla de decisión** se escribe antes también: qué resultado me hace shipear, cuál me hace matar, cuál me hace iterar. Si la escribo después de ver los datos, ya no es un experimento, es una justificación.
>
> En la implementación: la variante va detrás de un flag, asignación aleatoria y estable por usuario, y me aseguro de que el evento de exposición se dispare cuando el usuario **realmente ve** la variante, no cuando se le asigna. Ese es el error clásico que invalida el análisis.
>
> Después chequeo validez: ¿los grupos están balanceados en las covariables? ¿La muestra llegó al tamaño planeado? ¿Hubo algo raro en el período (un feriado, un incidente, un release)? Y ahí decido.
>
> Y lo que casi nadie hace y yo sí haría: **documentar el resultado aunque pierda**. Un test perdido bien documentado evita que el equipo vuelva a probar la misma idea en ocho meses.
>
> **Lo que no hice**: no corrí experimentos A/B con asignación aleatoria en producción a escala. Lo más cercano que hice fue en ARO, en 2019, con Adobe Target: implementaba las variantes como snippets de JS nativo y las servía por el motor de Adobe. Eso me dio el músculo de *construir* la variante y pensar en el costo de mantenerla, pero el diseño estadístico del experimento lo manejaba otra persona. Es la parte que quiero aprender acá y sé exactamente cuál es."

**Por qué funciona:** das el framework completo (demostrás que estudiaste), nombrás los dos errores que separan a un senior de un junior (exposición vs asignación, regla de decisión ex-ante), y cerrás con el gap acotado y específico en lugar de un "no tengo experiencia" global.

---

**P: "¿Qué métrica elegís para este producto?"**

> "Depende de qué etapa del funnel me pidan mover, pero para Tempo hay una particularidad que cambia la respuesta estándar: **la licencia se ata al tamaño de la licencia de Jira**. O sea, el cliente ya paga por todos los asientos de la instancia. Entonces la métrica que más mueve el negocio no es 'usuarios nuevos', es **seat utilization**: qué porcentaje de los asientos que ya se pagan efectivamente loguea tiempo.
>
> Si la utilización es baja, el cliente no ve el valor, y en la renovación baja de tier o se va. Si es alta, el crecimiento viene solo cuando suman gente a Jira.
>
> Así que si me preguntás por activación, miraría **time-to-first-worklog** y **% de asientos con ≥1 worklog en 14 días**. Si me preguntás por conversión, miraría **attach rate del módulo siguiente** - cuántas instancias que tienen Timesheets suman Capacity Planner o Financial Manager. Y siempre con una guarda: la velocidad del editor de timesheet, porque si la instrumentación o la variante lo hace más lento, ganás la métrica y perdés el producto."

**Por qué funciona:** demuestra que leíste el pricing, entendiste el modelo seat-based, y traducís growth a la economía real de Tempo. Es la respuesta que ningún candidato genérico puede dar.

---

**P: "¿Cómo instrumentás eventos de analytics?"**

> "Con tres capas. Primero una **taxonomía** consistente, con convención `objeto_accion` (`worklog_created`, `timesheet_submitted`, `trial_activated`), versionada en el repo, no en un Notion que se desactualiza. Cada evento con sus propiedades tipadas y un diccionario de datos que dice de dónde sale cada campo.
>
> Segundo, **el evento se dispara donde el usuario ve el resultado**, no donde el código cree que pasó algo. Si el worklog falla al guardar, no se emite `worklog_created`. Eso suena obvio y es la causa número uno de dashboards mentirosos.
>
> Tercero, **el contrato se testea**. Un test que falla el build si un evento declarado deja de emitirse, igual que testearías una respuesta de API. En un equipo de growth eso es lo que evita que un refactor silencioso te rompa seis meses de serie histórica.
>
> Acá hay una restricción específica de Tempo que me interesa: con Forge, el frontend corre en un iframe con CSP que bloquea scripts de terceros. No podés cargar el SDK de Amplitude y listo. Los eventos tienen que salir por el bridge a una función backend o por el backend de Tempo, con egress permissions declarados. Eso hace que el diseño del pipeline sea una decisión de arquitectura y de security, no de marketing. **¿Cómo lo resolvieron ustedes?**"

**Por qué funciona:** el cierre en pregunta es legítimo (es una entrevista, no un examen) y demuestra lectura de plataforma.

---

**P: "¿Qué es un feature flag y cómo hacés un rollout gradual?"**

> "Un feature flag es un interruptor evaluado en runtime que desacopla **deploy** de **release**. El código puede estar en producción y apagado; prenderlo es una decisión de producto, no un deploy.
>
> Para un rollout gradual yo distinguiría tres usos que se confunden y no son lo mismo:
> - **Kill switch**: para poder apagar algo rápido si rompe. Es el uso más valioso y el más subestimado.
> - **Targeting**: por instancia, por plan, por país, por rol. En el caso de Tempo, targetear por tamaño de instancia es clave: no querés que un cambio de onboarding le llegue primero a Cisco.
> - **Experimento**: asignación aleatoria y estable, con exposición registrada. Es un flag con esteroides y con análisis estadístico atrás.
>
> El rollout lo haría por etapas con métricas de guarda en cada una: internal users → 1% → 5% → 25% → 100%, con criterios de avance definidos antes (error rate, latencia, quejas de soporte). Y con la disciplina de **limpiar el flag**: un flag que queda prendido para siempre es deuda técnica con un nombre amigable. Se le pone fecha de vencimiento al crearlo."

**Honestidad obligatoria:** no has operado LaunchDarkly en producción. Decilo si te repreguntan: *"No operé un sistema de flags a escala; sí usé el patrón de rollout por audiencia y de feature detrás de configuración. La mecánica de la herramienta se aprende en una semana; la disciplina de limpieza y de guardas es la que no se aprende sola."*

---

**P: "Contame de un caso donde tu trabajo impactó una métrica de negocio."**

Acá **no inventes un A/B**. Contá impacto medible real:

> "En Minutentag migramos de jQuery a React una plataforma con más de 2M de usuarios mensuales activos. El impacto medible no fue un test A/B, fue performance y estabilidad en un producto que la gente usa todos los días: menos tiempo de carga, menos bugs de UI, y la posibilidad de iterar rápido porque el código dejó de ser un monolito de jQuery. En un producto con esa base, una mejora de performance **es** una métrica de negocio: retención y conversión se mueven con velocidad percibida.
>
> Y en ARO, en 2019, trabajé con Adobe Target implementando variantes como snippets de JS nativo. Ahí vi de cerca cómo se arma un test y cómo se lee, aunque el diseño experimental no era mío.
>
> Lo que no tengo es un caso donde yo haya sido dueño de la métrica de activación o retención de punta a punta. Tengo impacto medible en calidad, performance y accesibilidad - que son habilitadores de esas métricas - pero no el ownership directo. Es exactamente el salto que quiero dar."

---

### 8.2 El gap de analytics/funnel/flags - cómo responderlo sin quedar afuera

Te lo van a notar. La forma de manejarlo es **acotarlo, no negarlo**:

> "Te lo digo derecho porque prefiero que lo sepas ahora: no vengo de un equipo de growth. No fui dueño de un funnel, no corrí tests multivariados en producción a escala, y no operé LaunchDarkly ni Amplitude día a día.
>
> Lo que sí tengo es lo que en la práctica es el 70% del trabajo de un frontend de growth, y lo tengo con profundidad:
>
> - **Calidad medible como disciplina.** En EY, en Motif, llevé 50+ componentes a WCAG 2.2 AA y armé el pipeline de accesibilidad en CI. Eso es exactamente el mismo músculo que instrumentar: definir un estándar, medirlo automáticamente, y que el build falle cuando se rompe. La diferencia entre un a11y check y un tracking plan check es el nombre del archivo de configuración.
> - **Auditoría y diagnóstico a escala.** En Super7UI audité los Screeners de Warner Bros y encontré más de 200 violaciones. Eso es leer un sistema ajeno, encontrar los patrones que se repiten, y priorizar por impacto. Es el mismo trabajo que mirar un funnel y encontrar dónde se cae la gente.
> - **Experimentar sin framework formal.** En ARO, 2019, con Adobe Target: implementé variantes, entendí el costo de mantenerlas, y vi cómo se decide un ganador.
> - **Ownership end-to-end real.** Mi CRM multi-tenant freelance: React, Vite, Supabase, RLS, Edge Functions, Stripe. Diseñé el modelo de datos, la seguridad por fila, el billing y el frontend. Nadie me escribió la spec. Eso es lo que un equipo de growth necesita: alguien que agarre un problema difuso y lo convierta en algo que se puede medir.
> - **Contribuciones a design systems de terceros.** 11 PRs mergeados en react-spectrum, carbon-design-system, astryx, base-ui y material-ui. Eso significa que puedo entrar a un codebase que no escribí, entender sus convenciones, y aportar sin romperlo. En una empresa que es un roll-up de cuatro productos, eso vale más de lo que parece.
>
> Lo que me falta es la parte de **diseño experimental y lectura de métricas de producto**, y no la voy a disfrazar. Lo que te ofrezco es que esa curva es corta para mí y que la parte larga - escribir el código, instrumentarlo bien, no romper producción, y hacerlo accesible y rápido - ya la tengo resuelta."

**Por qué funciona:** nombrás el gap antes de que lo encuentren (controlás la narrativa), lo acotás a dos cosas concretas, y mapeás cada cosa que sí tenés a la habilidad de growth que representa. No pedís indulgencia: hacés un argumento.

---

### 8.3 Ownership

---

**P: "¿Por qué te interesa ESTE rol?"**

Tres razones, específicas de Tempo, no genéricas:

> "Tres cosas, y son específicas.
>
> **Una: el momento del producto.** Tempo está pasando de ser un vendor de apps de Jira a una plataforma ecosystem-independent, con Loop, y al mismo tiempo metiendo agentes de IA en el modelo de datos - Workforce Intelligence atribuye corridas de agentes a issues de Jira. Eso es un cambio de categoría, no una feature. Estar en el frontend de growth en ese momento es estar donde se decide si el producto nuevo se entiende o no.
>
> **Dos: la restricción técnica me atrae.** Migrar a Forge Remote con el frontend hosteado por Atlassian, con CSP que bloquea terceros, implica que instrumentar y experimentar es un problema de arquitectura. Eso es mucho más interesante que pegar un snippet.
>
> **Tres: el tipo de problema.** Es un producto B2B donde el usuario no eligió la herramienta - se la instaló su empresa. Eso hace que la activación sea un problema de **diseño y de fricción**, no de adquisición. Y la fricción es lo que yo sé encontrar: pasé años auditando interfaces ajenas y midiendo cuánto fallan."

---

**P: "Contame algo que demuestre ownership end-to-end."**

> "El CRM multi-tenant que hice como freelance. No había backend team, no había spec, no había diseñador. Definí el modelo de datos multi-tenant, la seguridad a nivel de fila con RLS en Supabase, las Edge Functions, la integración de Stripe para billing, y el frontend en React con Vite. Cuando algo no funcionaba, no había a quién escalar: era mío.
>
> Lo que aprendí ahí es lo que haría en growth: **cuando sos el único dueño, la métrica deja de ser abstracta**. Si el usuario no entiende el flujo de alta, no es un ticket para otro equipo: es tu problema, y lo arreglás vos.
>
> El otro es el pipeline de accesibilidad en EY. No me lo pidieron: lo armé. Definí el estándar, lo puse en CI, y desde entonces el equipo no puede mergear algo que rompa a11y. Eso es ownership: no arreglar instancias, cambiar la regla que las produce."

---

**P: "¿Cómo trabajás con PMs, QA y technical writers?"**

> "Con dos reglas. Primera: **el ticket no es la unidad de trabajo, el problema del usuario lo es**. Si el ticket dice 'agregar tooltip' y el problema real es que nadie entiende el paso 3, lo digo antes de escribir código.
>
> Segunda: **QA y technical writers son mi primera línea de detección, no mi último paso**. QA encuentra los edge cases que yo no pensé; el writer encuentra las inconsistencias de lenguaje que yo ya no veo porque estoy dentro del código. En un producto con 30.000 clientes y 10 idiomas, el copy es UI.
>
> Y con PMs: pido que la hipótesis y la métrica estén escritas antes de estimar. Si no están, ayudo a escribirlas. Un ticket de growth sin métrica es un ticket de plataforma disfrazado."

---

**P: "¿Cómo manejás un experimento que perdió?"**

> "Como un resultado, no como un fracaso. Lo que hago es separar dos preguntas: *¿perdió la hipótesis?* o *¿falló la implementación?* Si la variante tenía un bug, o el evento no disparaba bien, o la muestra no llegó, el test no perdió: fue inválido, y hay que repetirlo.
>
> Si perdió de verdad, lo documento: qué probamos, qué esperábamos, qué pasó, y qué aprendimos sobre los usuarios. Ese documento es el activo. Un equipo que no documenta sus tests perdidos repite las mismas ideas cada dos años y cree que está innovando.
>
> Y hay un caso que me parece el más interesante: **cuando la variante gana la métrica primaria pero empeora una guarda**. Ahí no se shipea. Se investiga. Un aumento de conversión que sube el error rate o hace más lento el editor es un préstamo, no una ganancia."

---

**P: "¿Cómo te mantenés actualizado / AI-first?"**

> "Uso agentes en mi trabajo diario, con memoria persistente: tengo un sistema propio donde los agentes tienen contexto del proyecto y no arrancan de cero cada vez. Eso me cambió el trabajo: la parte de exploración y de boilerplate se acelera mucho, y lo que queda es criterio - decidir qué construir, cómo medirlo, y qué no hacer.
>
> Pero soy cuidadoso con eso: un agente escribe código plausible, no código correcto. La revisión sigue siendo humana, y en un producto con SOC 2 e ISO 27001 la trazabilidad de por qué cambió algo importa tanto como el cambio. Uso IA para acelerar, no para delegar el juicio."

---

### 8.4 Preguntas incómodas que conviene tener preparadas

| Pregunta | Qué NO hacer | Qué hacer |
|---|---|---|
| "¿Tenés experiencia con experimentación en producción?" | Inflar Adobe Target 2019 a "dueño de la estrategia de experimentación" | Acotar: implementaste variantes, no diseñaste el test. Nombrar exactamente qué te falta. |
| "¿Cuántos años de React?" | Redondear para arriba | Dar el número real y **anclarlo en el caso más fuerte** (Minutentag, Motif, el CRM). |
| "¿Por qué tantos trabajos/freelance?" | Justificarte | Narrativa de profundidad: design systems, a11y, migraciones grandes, y el CRM como prueba de end-to-end. |
| "¿Sos frontend o full-stack?" | Decir "full-stack" para parecer más | "Frontend con capacidad de backend cuando el problema lo pide. El CRM lo prueba; mi centro de gravedad es la UI." |
| "¿Inglés?" | "Intermediate" si no lo es | Nivel real + evidencia (entrevistas, PRs en repos internacionales, trabajo remoto). |
| "¿Aceptás contractor vía TEAM?" | Aceptar sin preguntar | Preguntar modelo, duración, y si hay path a Tempo directo. |

---

## 9. Preguntas que VOS deberías hacer (elegí 5-7 según el aire)

Estas están ordenadas por **cuánto te dicen sobre si el puesto es real**. Si te queda una sola, hacé la 1.

1. **"¿Este equipo de Growth ya existe o me están contratando para formarlo?"**
   *Por qué:* la diferencia entre "te sumás a un equipo de 4 con métricas y stack definidos" y "sos el primer growth engineer y hay que construir todo" es abismal, y ninguna de las dos es mala - pero tenés que saber cuál es. Si es la segunda, preguntá quién es el dueño de la métrica hoy.

2. **"¿Qué métrica es dueña el equipo, y cómo se mide hoy?"**
   *Por qué:* si no pueden nombrar una métrica concreta y una fuente de datos, el "rol de growth" es un título, no una función. Escuchá si dicen "activación" y después no saben cómo la instrumentan: eso te dice que el trabajo real va a ser construir la medición desde cero.

3. **"¿Qué usan para feature flags y para analytics, y desde cuándo?"**
   *Por qué:* revela madurez. Si la respuesta es "estamos viendo", sabés que vas a pasar los primeros meses construyendo infraestructura. Si nombran LaunchDarkly + Amplitude con años de historia, sabés que vas a poder experimentar desde el día uno.

4. **"¿Cómo convive el equipo de Growth con el de plataforma? ¿Comparten el design system y el repo, o hay un fork?"**
   *Por qué:* en empresas que son un roll-up (Tempo compró cuatro productos), el riesgo real es que growth construya un código paralelo. Preguntalo directo: *"¿Growth commitea al mismo repo que el producto?"* La respuesta te dice si vas a acumular deuda o a construir sobre algo.

5. **"La migración a Forge Remote: ¿cómo resolvieron la instrumentación con el CSP de Custom UI? ¿Los eventos salen por el bridge o por el backend?"**
   *Por qué:* es tu pregunta de poder. Demuestra que leíste la plataforma y te obliga a hablar con alguien técnico. Si el interviewer no sabe qué es Forge Remote, es señal de que el filtro no es técnico.

6. **"¿Cuál es el ciclo de un experimento acá, de la hipótesis al ship? ¿Semanas o quarters?"**
   *Por qué:* mide si "growth" significa iteración rápida o si en realidad es un roadmap de producto con nombre nuevo. En una empresa con deuda de PE, el ciclo suele estar comprimido - pero verificá.

7. **"¿Cómo es el día a día en inglés? ¿El equipo es distribuido y las reuniones son en inglés, o hay un equipo local en español?"**
   *Por qué:* es tu pregunta de higiene. El JD pide "upper-intermediate" y "multicultural environment". Saber si son 4 horas de meetings en inglés o 30 minutos de standup cambia tu preparación. Preguntalo sin vergüenza: es una pregunta profesional, no una confesión.

**Bonus si el clima es bueno:** *"¿Qué pasó con el equipo después de la recapitalización de 2025? ¿Cambió el mandato de ingeniería?"* - Es directo, y la forma en que lo responden te dice más que el contenido.

---

## 10. Mercado de Jira apps y competencia

### 10.1 Tamaño y dinámica

| Dato | Valor | Fuente |
|---|---|---|
| Apps en el Marketplace | **8.000+** | Aventis Advisors (2025) |
| Partners | **1.800+** | Aventis Advisors (2025) |
| Gasto anual estimado | **~$1.8B (2024)**, CAGR ~19% desde 2021 | Aventis Advisors (2025) |
| Consolidación | Activa: PE-backed roll-ups (Appfire ~200 apps; Tempo con playbook similar) | Aventis Advisors (2025) |

**[CONFIRMADO como fuente secundaria]** - Aventis es un asesor M&A del ecosistema, así que tiene interés en que el mercado parezca atractivo. Tomá las cifras como orden de magnitud, no como auditoría.

**Lo que esto significa para vos:** es un mercado grande pero **maduro y consolidándose**. Los vendors independientes chicos se venden. Tempo es un comprador serial, no un target - al menos por ahora. Eso da estabilidad relativa, y también explica por qué el puesto existe: hay que hacer que cuatro productos comprados crezcan juntos.

### 10.2 Competencia (por categoría, no por empresa)

| Categoría | Competidores | Nota |
|---|---|---|
| Time tracking en Jira | **Everhour, Clockwork, Harvest (integraciones)**, el time tracking nativo de Jira | Tempo es el líder de la categoría; la amenaza real es que Atlassian mejore el nativo |
| Capacity / resource planning | **Float, Runn, Productive** | Fuera del Marketplace son más fuertes en agencias |
| PPM / SPM enterprise | **Jira Align (Atlassian), Planview, Clarity (Broadcom), ServiceNow SPM, Monday, Smartsheet** | Tempo tiene comparativas públicas contra todos: `/comparison/clarity-vs-tempo`, `/blog/planview-alternatives`, `/blog/smartsheet-alternatives`, `/blog/jira-align-vs-tempo` |
| Engineering intelligence | **Jellyfish, LinearB, Swarmia, GetDX** | Este es el espacio donde entra **Workforce Intelligence**. Tempo tiene contenido comparativo contra todos. Es el flanco donde la competencia es más nueva y agresiva. |
| Roadmapping | **Aha!, Productboard, Jira Product Discovery** | Roadmunk compite acá |

**Lectura estratégica [PROBABLE]:** el riesgo existencial de Tempo no es un competidor de time tracking. Es **(a)** que Atlassian absorba la funcionalidad en Jira Cloud (como hizo con otras categorías), y **(b)** que la categoría de "engineering intelligence" se coma el presupuesto de "portfolio management" con productos nativos de IA. Loop y Workforce Intelligence son la respuesta a ambos: salir del Marketplace y subir en la cadena de valor.

Ese es un ángulo de conversación muy fuerte para la entrevista: *"Veo que la jugada de Loop es salir de la dependencia del Marketplace, y la de Workforce Intelligence es capturar el presupuesto de IA antes de que lo haga Jellyfish. ¿El equipo de Growth tiene un rol en alguna de las dos?"*

### 10.3 Qué implica SOC 2 / ISO 27001 para un dev frontend

Esto **no es un trámite de compliance**: te cambia el trabajo diario. **[CONFIRMADO que Tempo tiene las tres certificaciones; PROBABLE/INFERIDO el detalle operativo]**

| Área | Qué significa en la práctica |
|---|---|
| **Analytics y PII** | No podés mandar datos de usuario a un tercero sin contrato, base legal y minimización. Los eventos se diseñan con IDs seudonimizados, no con emails. Cada herramienta nueva pasa por review de security y aparece en la lista de **subprocessors** pública. |
| **Scripts de terceros** | Es justo lo que el CSP de Forge bloquea. Un SDK de analytics es, desde el punto de vista de auditoría, **un subprocessor ejecutando código en el browser del cliente**. Se justifica o no se usa. |
| **Change management** | SOC 2 audita que los cambios pasen por PR review y CI. Tu pipeline de a11y en CI no es solo calidad: es **evidencia de control**. Si lo tenés, nombralo así en la entrevista. |
| **Audit logging** | Toda acción sensible deja traza. Si agregás un flujo nuevo, tenés que pensar qué se loguea. En Tempo ya hay "audit logging for Capacity Planner" en product news - es un tema vivo. |
| **Least privilege** | El frontend no pide más scopes de los que necesita. En Jira, cada scope es visible al admin del cliente. |
| **Data residency** | Los clientes enterprise eligen región. Un evento que sale a un collector en US cuando el cliente está en EU es un incidente. |
| **Supply chain** | Dependencias nuevas = superficie de ataque y evidencia de auditoría. En un producto que instalan bancos y defensa (BAE Systems, Sultan Bank), `npm install` no es gratis. |
| **Accesibilidad** | No es SOC 2, pero en enterprise es un requisito de compra (VPAT/EN 301 549). Tu experiencia en WCAG 2.2 AA es **directamente vendible** acá. |

> **Cómo usarlo:** *"Entiendo que en un producto con SOC 2 Type II y ISO 27001, agregar una herramienta de analytics no es una decisión de frontend: es un subprocessor nuevo, con review de security, minimización de PII y actualización de la página de subprocessors. Eso cambia cómo diseño la instrumentación: menos SDKs de terceros, más eventos propios que salen por nuestro backend."* - Eso es exactamente el tipo de criterio que separa a un senior en enterprise.

---

## 11. Tu mapa de fortalezas contra este JD

| Lo que pide el rol | Tu evidencia real | Fuerza |
|---|---|---|
| TypeScript + React, UIs complejas | Minutentag (jQuery→React, 2M+ MAU), Motif en EY (50+ componentes), CRM propio, liderazgo de 3 ingenieros en Next.js | **Alta** |
| Tests unitarios / integración / performance | Pipeline de a11y en CI, estándares en Motif, PRs en design systems con sus suites | **Alta** |
| Code review | 11 PRs mergeados en react-spectrum, carbon, astryx, base-ui, material-ui - revisado por maintainers de primer nivel | **Muy alta** |
| UX / accesibilidad | WCAG 2.2 AA en 50+ componentes; auditoría Warner Bros con 200+ violaciones encontradas | **Muy alta** (diferenciador) |
| Performance | Migración jQuery→React en 2M+ MAU; auditorías de performance | **Alta** |
| Seguridad | CRM multi-tenant con RLS y Edge Functions | **Media-alta** (buen anclaje conceptual) |
| Colaborar con PM/QA/writers | Equipos multidisciplinarios en EY, Minutentag, liderazgo de 3 | **Alta** |
| **A/B y multivariado** | Adobe Target 2019, implementación de variantes | **Baja-media** (honestidad) |
| **Instrumentación / analytics events** | No directa; analogía fuerte con a11y-as-CI | **Baja** (gap real) |
| **Feature flags / rollout** | Patrón conceptual, no herramienta | **Baja** (gap real) |
| **Ownership de métricas de growth** | No directa | **Baja** (gap real) |
| AI-first mindset | Sistema propio de agentes con memoria persistente; producto con IA en Next.js | **Alta y diferencial** |

**La estrategia de la entrevista se desprende de esto:** entrás como **senior frontend de altísima calidad técnica con criterio de producto**, no como growth engineer experimentado. El argumento es que la parte difícil de growth en un producto enterprise no es la estadística - es construir variantes rápidas, instrumentarlas bien, no romper nada, y hacerlas accesibles y rápidas. Eso ya lo hacés.

---

## 12. Fuentes (consultadas 2026-10-21)

| # | Fuente | URL | Qué aportó |
|---|---|---|---|
| 1 | Tempo - Home | https://www.tempo.io/ | Positioning, Loop, SOC2/ISO/GDPR, conectores, "20+ years" |
| 2 | Tempo - Timesheets | https://www.tempo.io/products/jira-time-tracking | Features, SiriusXM 3.000 usuarios / 99% accuracy, Rovo agent |
| 3 | Tempo - Capacity Planner | https://www.tempo.io/products/capacity-planner | Features, "único que planifica múltiples recursos en un issue", workload schemes |
| 4 | Tempo - Financial Manager | https://www.tempo.io/products/project-financial-management | Features, dependencia de Timesheets, BAE Systems |
| 5 | Tempo - Structure PPM | https://www.tempo.io/products/project-portfolio-management-software-ppm | Features, Formula Assistant (Rovo), Škoda |
| 6 | Tempo - Strategic Roadmaps | https://www.tempo.io/products/roadmaps | Ex Roadmunk, integraciones, ISO 27001:2013 + 27701:2019 |
| 7 | Tempo - Portfolio Manager | https://www.tempo.io/products/portfolio-manager | Ex LiquidPlanner, Monte Carlo 90% confidence |
| 8 | Tempo - Pricing | https://www.tempo.io/pricing | **Modelo seat-based, licencia = tamaño de Jira, tiers de precio, tope 100k** |
| 9 | Tempo - Workforce Intelligence | https://www.tempo.io/news/tempo-introduces-workforce-intelligence | Lanzamiento 25/08/2026, 30k clientes, 53% Fortune 100, CEO/CTO quotes |
| 10 | Tempo - What is Loop | https://www.tempo.io/blog/what-is-loop | Loop ecosystem-independent, métricas de early customers, 350+ partners |
| 11 | Tempo - Why Forge | https://www.tempo.io/blog/why-tempo-is-moving-to-forge | Connect on Forge completo a fin de 2025 |
| 12 | Tempo - Forge migration | https://www.tempo.io/product-news/tempo-moves-to-forge | **Forge Remote elegido, migración desde 31/03/2026, frontend en Atlassian** |
| 13 | Tempo - Adquiere ALM Works | https://www.tempo.io/news/tempo-acquires-alm-works | Structure, 5.000 orgs, 20.000 clientes en ese momento, Boston/Reykjavik/Montreal |
| 14 | Tempo - Adquiere LiquidPlanner | https://www.tempo.io/news/tempo-acquires-liquidplanner | **> $100M ARR en 2022, Rule of 40**, 28.000 clientes |
| 15 | Tempo - Adquiere Roadmunk | https://www.tempo.io/news/tempo-acquires-roadmunk | Roadmunk (nov 2021) |
| 16 | Paul, Weiss | https://www.paulweiss.com/insights/client-news/tempo-software-completes-leveraged-recapitalization | **Recapitalización apalancada, sep 2025, portfolio de Diversis** |
| 17 | PE Hub | https://www.pehub.com/diversis-runs-single-asset-process-on-saas-focused-tempo/ | Diversis: mayoría 2018, resto 2022, proceso single-asset 2024 |
| 18 | Medium - Tech at Tempo (Kiran Gopalakrishnan, nov 2020) | https://medium.com/tech-at-tempo/the-cost-of-tracking-cost-how-we-built-the-frontend-for-cost-tracker-2b25274174d7 | **React + Redux + ImmutableJS + Django; TS+React+Flask en Cost Tracker; react-testing-library** |
| 19 | GitHub - tempo-io | https://github.com/tempo-io | Repos públicos: Kotlin/Java, tests de entrevista en Java, `html-to-image` (TS) |
| 20 | Atlassian - Forge Custom UI | https://developer.atlassian.com/platform/forge/extend-ui-with-custom-options/ | **CSP bloquea scripts externos (Google Analytics, Sentry), requiere `invoke`; egress controls** |
| 21 | Built In - Senior Frontend Developer (Growth) | https://builtin.com/job/senior-frontend-developer-growth/7809698 | **JD público completo (removido el 13/05/2026, cacheado)** |
| 22 | HubMub - mismo JD, Argentina | https://www.hubmub.com/jobs/745101/senior-frontend-developer-growth | Versión Argentina del aviso |
| 23 | LinkedIn - post Senior Growth Engineer (ago 2025) | https://www.linkedin.com/posts/annumkhalid_senior-growth-engineer-activity-7359206712253304834-Jjh7 | **Growth team existe; stack TS/React/JS/HTML5/CSS3; producto Structure for Jira Cloud** |
| 24 | Aventis Advisors - Marketplace M&A | https://aventis-advisors.com/atlassian-marketplace-ma/ | **8.000+ apps, 1.800+ partners, ~$1.8B en 2024, CAGR ~19%** |
| 25 | Growth Engineer - Operating System | https://growthengineer.ai/blog/growth-engineering-operating-system | 6 sistemas de growth engineering, madurez, benchmarks de experimentos |
| 26 | Growth Engineer - Team Structure | https://growthengineer.ai/blog/growth-team-structure-benchmarks | Tamaño de equipos por ARR, reporte a CPO 44%, ratio engineers:marketers |

---

## 13. INCERTIDUMBRE - lo que no pude verificar

Marcado explícito, porque es lo que te permite no pisar un charco en la entrevista.

### 13.1 No verificado (no hay fuente accesible)

1. **El JD exacto que te pasó TEAM International.** Verifiqué la versión pública (Built In, HubMub) y **no contiene las líneas de A/B testing, feature flags ni analytics events**. Puede ser una versión adaptada por TEAM, o un req distinto. **No pude confirmar cuál es el vigente.** → Llevá el tuyo impreso.
2. **Herramientas reales de analytics y feature flags de Tempo.** Cero evidencia pública. Todo lo que digas de "ustedes usan X" es especulación. Preguntá.
3. **Si el equipo de Growth existe hoy como tal.** Confirmé un posteo de "Senior Growth Engineer" en agosto 2025. No pude confirmar que el equipo siga existiendo, ni su tamaño, ni si depende de Producto, Marketing o Ingeniería.
4. **Estado de GA de Tempo Loop.** Hay páginas de EAP y de learning center. No pude confirmar si Loop está en disponibilidad general o todavía en early access.
5. **Métricas de instalaciones de Jira / base instalada.** Tempo publica "30.000+ clientes" pero no cuántas instalaciones de Jira ni cuántos usuarios finales. El dato de "70 millones de usuarios en el ecosistema" que aparece en el press release de ALM Works es del **ecosistema Atlassian**, no de Tempo - no lo uses como si fuera base propia.
6. **Número de empleados.** LinkedIn dice 402 (+26% YoY); Revelio Labs dice 328 a marzo 2026. **Están en conflicto.** No uses ninguna cifra.
7. **Detalle del contrato TEAM International** (rate, modelo, duración, path a Tempo). Es la mayor incógnita práctica y no es verificable desde afuera.
8. **Páginas de Atlassian Marketplace.** Intenté leer las fichas de las apps (reviews, número de instalaciones, ranking) y **el contenido se renderiza por JS**: sólo obtuve el chrome de la página. No pude verificar install counts ni reviews.
9. **El proceso técnico de la entrevista.** Los test tasks públicos de Tempo son en **Java**, lo cual es un dato del pasado. No sé si para este rol hay take-home, live coding o system design.

### 13.2 Inferencias que conviene chequear antes de afirmarlas como hecho

| Inferencia | Base | Nivel |
|---|---|---|
| El growth de Tempo es principalmente in-product / seat utilization | Precio atado a licencia de Jira + apps que se instalan en la instancia | **Probable, no confirmado** |
| Usan Atlassian Design System | Recomendación oficial de Forge + convención del ecosistema | **Probable** |
| El equipo usa LaunchDarkly o similar | Estándar enterprise | **Suposición** - no repetir como hecho |
| Loop todavía en EAP | Existencia de `/loop-eap` y `/learning-center/tempo-loop` | **Probable** |
| La recap de 2025 implica presión de eficiencia | Naturaleza de una leveraged recap | **Probable** (razonamiento financiero estándar, no dato de Tempo) |

### 13.3 Riesgo de la fuente secundaria

Los benchmarks de growth (12 experimentos/quarter mediana, 50 alta velocidad, tamaños de equipo por ARR) vienen de **growthengineer.ai**, un sitio de contenido con interés comercial. Los uso como **marco mental**, no como estadística dura. Si los citás en la entrevista, decí "benchmarks públicos del rubro", no "los datos dicen".

### 13.4 Lo que este documento NO cubre

- **Compensación.** No busqué ni verifiqué rangos salariales para este rol/geografía. Si te interesa, es una investigación aparte (y TEAM es quien tiene el dato real).
- **Cultura interna, manager directo, on-call, proceso de release.** Nada de esto es público. Son preguntas para la entrevista, no para el documento.
- **Detalle de la deuda técnica post-Forge.** Sólo sé que la migración arrancó el 31/03/2026 y que el frontend ahora lo hostea Atlassian. El impacto real en el día a día de un dev frontend no es público.

---

## 14. Los tres puntos que hay que recordar de todo esto

1. **Tempo es un roll-up de PE que se está reposicionando de "time tracking para Jira" a "orquestación de portafolios para humanos y agentes de IA".** Loop y Workforce Intelligence son la apuesta; las apps de Jira son el ingreso actual. Un equipo de Growth en ese contexto tiene un mandato claro: hacer que la base existente valga más, y que el producto nuevo se entienda.
2. **El growth acá es seat-based dentro de la instancia de Jira del cliente.** La licencia se ata al tamaño de Jira, así que la métrica que mueve el negocio es utilización de asientos y attach de módulos, no adquisición de usuarios. Decir esto te distingue de cualquier candidato genérico.
3. **Tu entrada no es "soy growth engineer", es "soy el senior frontend que hace que los experimentos sean confiables".** A11y en CI, auditorías de sistemas ajenos, migraciones a escala y PRs en design systems de terceros son exactamente las habilidades que hacen que un experimento no sea un desastre. El gap de estadística y herramientas es real, es acotado, y se dice de frente.
