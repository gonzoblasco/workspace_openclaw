# Hechos de carrera - el corpus completo

> **Dueño único de la verdad sobre la carrera de Gonzo.** Todo lo que hizo, lo que dejó de hacer
> y lo que decidió no hacer vive acá. Los CVs, las cartas, los formularios y los screenings
> **seleccionan** de este archivo; ninguno inventa ni reescribe.
>
> **El corpus es la verdad. El perfil es un filtro.** Un perfil distinto (a11y, fullstack,
> evaluator, no técnico) elige **qué** se muestra, en qué orden y con qué énfasis. Nunca cambia
> **los hechos**: fechas, años, títulos, idioma, certificaciones, contacto.
>
> Si un CV necesita un dato que no está acá, el archivo se completa primero y después se
> propaga. Ver ADR-101. Gate: `scripts/check-cv-facts.py`.

---

## Bloque de hechos (lo lee el gate)

```facts
total_years: 10
a11y_years_internal: 5
a11y_claim: roles
ai_years: 1
backend_years_internal: 1
sdlc_years: 3
english: B2+
spanish: native
contact_phone: +54 11 4937 4656
contact_email: gonzoblasco@icloud.com
contact_linkedin: linkedin.com/in/gonzalo-blasco
contact_github: github.com/gonzoblasco
contact_location: Nunez, Buenos Aires, Argentina
role_freelance: 05/2025 - Present
role_ey: 09/2021 - 05/2025
role_super7: 08/2020 - 05/2021
role_minutentag: 02/2016 - 11/2019
oss_merged: 11
pending: 0
```

---

## 1. Identidad y contacto

- **Nombre:** Gonzalo Blasco. Se lo llama Gonzo, Gonza o Gonzalo.
- **Ubicación:** Núñez, Buenos Aires, Argentina (GMT-3). Remoto LATAM, alineado a US EST.
- **Contacto:** `+54 11 4937 4656` · `gonzoblasco@icloud.com` · `linkedin.com/in/gonzalo-blasco` · `github.com/gonzoblasco`.
- **Idiomas:** español nativo; **inglés B2+** (dato duro, ver §7).

---

## 2. Trayectoria

### 2.1 Freelance / Software Engineer - 05/2025 a hoy

**Título canónico:** Software Engineer. El sufijo lo pone el perfil: Accessibility Expert (a11y),
Full Stack Engineer (fullstack), Frontend Engineer (frontend).
**Se dice "freelance" o "Freelancer".** Prohibido "Independent", "Independiente" o "Founder".

Qué hizo:

- **SoporteML** - CRM multi-tenant con IA para vendedores de Mercado Libre. Bandeja unificada de
  preguntas, sugerencias de respuesta con RAG (pgvector + embeddings), Autopilot con guardrails de
  confianza, multi-empresa y roles de equipo, billing con Stripe. Stack: React, Vite, TypeScript,
  Supabase (PostgreSQL, Auth, Realtime, RLS, Edge Functions). v4 cerrado; el producto sigue por la
  versión funcional de Lovable. **Pro Motors como primer cliente** (`pro-motors.com.ar`,
  integración MeLi real).
- **Design system propio de SoporteML** (verificado 2026-10-22 sobre el repo): sistema de tokens
  semánticos (color, tipografía, spacing, radius, sombras, focus-ring, estados), escala tipográfica,
  paleta y mapa token→componente, documentado en `projects/soporteml/.knowledge/UI-DESIGN-SKILL.md`
  y aplicado con Tailwind en `projects/soporteml/tailwind.config.ts`. Reglas WCAG AA como criterio
  del sistema. **Es trabajo propio de diseño de sistema, no consumo de uno ajeno.**
- **AI Engineering OS sobre OpenClaw** - sistema propio de trabajo con IA: sesiones por proyecto,
  memoria persistente, handoffs, subagentes, skills, pipeline de contribución OSS. El método de
  trabajo con material de terceros es **quarantine → analyze → verify → adopt** (ver AGENTS.md):
  nada de lo que entra del exterior se adopta sin verificarse.
- **Servidor MCP propio** (verificado 2026-10-22 sobre `projects/kanam-fixer/`): el proyecto
  `kanam-fixer` expone un **MCP companion server** con dos tools, que permite a un agente consultar
  qué anuncia un lector de pantalla para un fragmento de HTML. Habla MCP sobre stdio: cualquier
  cliente MCP-aware (Claude Code, el tool gateway de OpenClaw) lo lanza como subproceso. **Lo
  construyó y lo mantiene Gonzo.** Documentado en `projects/kanam-fixer/README.md` y ADR-0003 del
  proyecto.
- **Herramientas de IA en el flujo diario** (verificado 2026-10-22 sobre los repos del workspace):
  Claude Code y Codex como motores de agentes headless en tareas largas, y el stack propio de
  OpenClaw (subagentes, memoria, skills) como sistema de trabajo. Lovable como herramienta de
  prototipo rápido (SoporteML v4). No se declara "Cursor" ni "GitHub Copilot" porque el corpus no
  los registra como uso propio.
- **PROHIBIDO declarar "computer-use" o "agentes de computer-use".** El 2026-08-27 un subagente
  se desvió a CuaDriver (computer-use) en una tarea que no lo requería y **Gonzo lo bloqueó**, y el
  proceso se relanzó sin computer-use (`memory/archive/dailies/2026-08-27.md:66`). No hay ninguna
  experiencia en computer-use que declarar. Los flujos agénticos que sí existen son de **subagentes
  con contexto acotado sobre codigo** (AI Engineering OS), no de agentes que manejan una pantalla.
- **Contribuciones OSS continuas** a design systems (ver §5).
- **Soluciones internas de IA para Pro Motors.**

Es el mismo período en que empezó a usar IA para desarrollo (ver §6.1) y el backend de producción
(ver §6.2). No son años distintos.

### 2.2 EY (Ernst & Young) - 09/2021 a 05/2025

**Título canónico:** Senior Frontend Engineer, Accessibility Lead.
**Variante admitida (perfil fullstack):** "Senior Full Stack / Frontend Engineer, Team Lead".
Es el mismo empleo con otro encuadre. Lugar: híbrido.

Qué hizo:

- **EY Motif**, librería de componentes React enterprise consumida por productos de cliente e
  internos: auditó y remedió **50+ componentes** a WCAG 2.2 AA (navegación por teclado, soporte de
  lector de pantalla, manejo de foco, contraste), con Axe DevTools, Lighthouse, JAWS y NVDA.
  **La librería de componentes es EY Motif, NO Minutentag** (corrección de Gonzo, 27/10/2026): en
  Minutentag nunca trabajó sobre una librería de componentes. Lo que sí hizo en Minutentag fue
  revisar componentes en **Storybook** y escribir requisitos técnicos de accesibilidad. **Lo que
  NO está confirmado en ningún lado, ni en EY:** haber *construido* la librería, o haberla
  distribuido a "5 equipos de producto". El corpus sostiene **auditar, remediar, definir
  estándares y escribir los requisitos** - no "desarrollar la librería".
- **Referente de accesibilidad del equipo** en varios proyectos: revisaba componentes de
  **Storybook (React)** **antes** de implementar, definía estándares y anotaciones a nivel
  componente, y escribía requisitos técnicos de accesibilidad con guía de código para las
  historias de UI.
  **Herramientas:** Storybook (revisión de componentes en React), Axe DevTools, Lighthouse, Jira.
  **NO usa Figma** (corrección de Gonzo, 26/10/2026): la revisión de diseño era sobre los
  componentes en Storybook, no sobre Figma. Figma salió de los CVs el 26/10/2026.
  **Conocimiento de ARIA:** WAI-ARIA Authoring Practices y el cableado de `role`, `state` y
  `property` en componentes propios - es el trabajo de los 11 PRs mergeados de §5.1, que son
  precisamente correcciones de semántica ARIA.
  **Toolset de código (verificado 2026-10-22 sobre los repos del workspace):** TypeScript, React,
  Vitest, Playwright, Biome, Tailwind, Storybook, Zod.
- **Mentoría y guía en sprint:** "coaching" a desarrolladores dentro de sus ramas y guía de
  remediación a desarrolladores en sprint. **No** es un programa de mentoría formal: no hay un
  corpus de "a quién mentoreaste y por cuánto tiempo". En los CVs, escribir *developer guidance* /
  *coaching*, no *mentorship*.
- **Equipo matricial cross-regional (US / India)**, varias fases del SDLC en paralelo dentro de
  squads ágiles.
- **Lideró un equipo de 3 ingenieros** construyendo una plataforma de inteligencia financiera con
  IA en Next.js, con interfaces accesibles de arquitectura a producción.

### 2.3 Super7UI - 08/2020 a 05/2021

**Título canónico:** Accessibility Engineer (Contractor). Lugar: remoto.

Qué hizo:

- Contratado para liderar la **auditoría de remediación de Warner Bros. Screeners (WBTVD)**, la
  plataforma de streaming privada que distribuidores globales usan para revisar contenido de WB.
- **Validó y expandió una auditoría previa de terceros (Applause)**, probando cada issue reportado
  en varios lectores de pantalla: **NVDA, VoiceOver y TalkBack**.
- Usó **Axe** para identificar y documentar violaciones WCAG en los flujos clave.
- Produjo **documentación completa de remediación**: soluciones propuestas, guía de implementación
  y especificaciones listas para desarrollo.
- **Resolvió 200+ violaciones WCAG** en la plataforma.
- **Estableció un pipeline de testing de accesibilidad** con axe-core + Playwright integrado en
  CI/CD.

### 2.4 Minutentag / EULAS - 02/2016 a 11/2019

**Título canónico:** Frontend Developer, Accessibility Owner. Lugar: híbrido.

Qué hizo:

- Agencia de e-commerce para marcas de EE.UU.: **Ascena Retail Group**, con los sitios de **Ann Taylor, LOFT y Lou & Grey** (tres marcas). Registrado 2026-10-20 en `memory/2026-10-20.md` (decisión de Gonzo sobre la trayectoria de a11y desde 2016).
- Participó de la **migración a React** y mejoró un sitio con **2M+ usuarios mensuales**.
- **Accesibilidad desde el inicio**: creció de junior a referente de accesibilidad del equipo.
  **Lo que NO hizo en Minutentag** (corrección de Gonzo, 27/10/2026): **no trabajó sobre una
  librería de componentes** (esa fue EY Motif) **ni sobre una arquitectura de micro-frontends**.
  Los dos bullets *"Architected and built micro frontend architecture serving 2M+ monthly active
  users"* y *"Developed shared component library used across 5 product teams"* sequitaron de los
  CVs: no tienen respaldo y el primero le era falso. Lo que sí queda del corpus sobre Minutentag
  es la migración a React, los 2M+ usuarios mensuales, la accesibilidad desde el inicio, los
  experimentos con Adobe Target y la implementación de variantes en JS nativo.
- **Experimentación en producción (2019):** trabajó con **Adobe Target** para correr experimentos
  A/B sobre features y diseños contra segmentos de usuarios en vivo, dentro de squads ágiles
  junto a diseño y producto. Hecho confirmado por Gonzo el 21/10/2026 (la duda estaba abierta en
  §11: los CVs declaraban esto desde agosto 2026 sin que estuviera en el corpus).
  **Alcance:** esto es **usar la herramienta y participar de los experimentos**, que es lo que
  Gonzo confirmó. **No hay evidencia de que haya construido la infraestructura** de experimentación
  del equipo: ese claim se sacó de los CVs (ver §11, punto 2). Si alguna vez Gonzo confirma que
  la implementó, se agrega acá primero y después vuelve a los CVs.
  **Cantidad de experimentos:** el corpus **no registra un número**. Un CV que diga "20+ A/B
  experiments" inventaría la cifra (sacado 2026-10-22 de los CVs de Mural). La redacción
  defendible es "ran A/B experiments in production", sin cantidad.
- **Implementación de los experimentos (2019, temporada final):** las variantes se implementaban
  **escribiendo código directo en JavaScript nativo como snippets**, que se probaban contra
  usuarios reales. Detalle confirmado por Gonzo el 21/10/2026. **Alcance:** implementación
  *client-side* de las variantes, no construcción de la plataforma de experimentación ni
  configuración de la herramienta. Es escritura de la prueba, no de la infraestructura.

### 2.5 Antes de 2016 - backend PHP, 2001 a 2008

Trabajo real, pero **no se suma al total ni se usa como headline**: es backend (no a11y) y hay un
gap de ~8 años (2008-2016). Solo defendible como amplitud ("20+ años en software") ante audiencia
que no vaya a preguntar por el gap. Decidir por audiencia, nunca por defecto.

---

## 3. Educación y formación

- **Formación continua en accesibilidad digital y calidad de software.**
- **Deque University - Accessibility Specialist Program (2021).** Programa de cursos, NO una
  credencial profesional. Cursos: Accessibility Fundamentals, Designing an Accessible User
  Experience, Semantic Structure and Navigation, Images/SVG/Canvas, IAAP Certification Quick Guide.
  **`IAAP Certification Quick Guide` es el nombre de un curso.** No insinúa estar certificado.
- **`ai-engineering-bootcamp`:** curso propio completado 10/10, archivado.

### Estudios formales (relevados por Gonzo el 27/10/2026)

**Antes esta sección decía "no hay título universitario registrado", y la lista de "falta relevar"
daba los estudios por inexistentes. Era incorrecto.** Los estudios están registrados, en fuentes
que no coincidían entre sí, y la contradicción se resolvió preguntándoselo a Gonzo el 27/10/2026.

**El relevamiento, textual de Gonzo (27/10/2026):**

| Período | Institución | Carrera | Estado |
|---|---|---|---|
| 2001-2002 | Universidad de Palermo (UP) | Ingeniería en Informática | **abandonada** |
| 2003-2004 | Universidad Argentina de la Empresa (UADE) | Diseño Gráfico | **abandonada** |
| 2006-2009 | Universidad del Cine (FUC) | Montaje cinematográfico | **abandonada**. Gonzo: "esta creo no la puse en ninguno" |
| 2010-2012 | Universidad Adventista del Plata (UAP) | Comunicación Social | **abandonada** |
| 2018 | Digital House (terciario) | React | bootcamp |

**Todas fueron abandonadas.** Gonzo, 27/10/2026: *"UADE tampoco la completé... todas fueron
abandonadas, no tengo título universitario"*. **No hay ni un título universitario, y ninguna
carrera se completó.**

**Dos precisiones sobre lo que quedó afuera y por qué:**

- **El listado de "agosto 2026" no era evidencia.** La sesión del 19/08 copió seis universidades de
  un perfil que Gonzo había pegado, y esa misma sesión lo dice textual: *"No verifiqué los datos
  personales ni los rangos de educación - los copié del perfil que me pasaste, pero las fechas... las
  asumí como estaban."* En ese listado además figuraba **Palermo 2018-2019, que Gonzo no menciona**
  en su relevamiento: queda como registro dudoso, no como hecho.
- **FUC (2006-2009) y UAP (2010-2012) nunca salieron a la calle:** no están en ningún CV, PDF ni
  DOCX. Lo único que salió fue **Digital House** y **UADE**.

**Lo verificado, y es lo que gobierna:**

- **NO hay título universitario: ninguna carrera se completó.** UP (Ing. en Informática),
  UADE (Diseño Gráfico), FUC (Montaje cinematográfico) y UAP (Comunicación Social) fueron
  **abandonadas todas**. La UP fue un año de ingeniería inconcluso; las otras tres tampoco
  llegaron al título. **Y aunque hubieran llegado, ninguna es CS ni "related studies"** en el
  sentido que un equipo de engineering lee.
- **Digital House (2018, React)** es un bootcamp: formación real y en React. **No es un título
  universitario.** Es defendible como "formación", nunca como degree.
- **Consecuencia operativa:** cuando un JD exige *"Degree in Computer Science, Software
  Engineering, or related studies"* (como el de TEAM International / tempo.io del 21/10), **la
  respuesta honesta es que no hay título completo.** No inventar, no presentar "dropped" como si
  fuera título, y no llamar "bootcamp" a un degree. **Lo que SÍ es defendible** es la línea de
  UP como "studied Computer Science at Universidad de Palermo (incomplete)" - que además tiene
  más peso para un JD de CS que UADE, FUC o UAP.
- **Lo que sí va en un CV** (y ya está en 5 de ellos): Digital House + UADE. FUC, UAP y UP **no se
  declaran** salvo que el JD pida algo específico o Gonzo lo pida: no aportan al perfil y suman
  ruido. **Gonzo: "no suelo comentar Universidad del Cine o UAP ya que no aportan a nuestro
  perfil... luego vemos cuáles van según el puesto"** - la selección por puesto es suya.
- **Ojo con la implicancia de "abandonada":** listar una carrera en una sección EDUCATION sin
  marcar que quedó incompleta **se lee como título obtenido**. Por eso los CVs que declaran UADE
  llevan el "(incomplete)" explícito, y el gate lo verifica (control 9).

### Formación continua: sí, y es parte de la historia

**Gonzo (27/10/2026): "hice muchos cursos durante mi carrera".** La sección ya decía "formación
continua en accesibilidad digital y calidad de software"; ahora queda el detalle: **Platzi** y
**Deque University** (2021, ya detallado en §4), **entre otros, muchos más**. Los cursos de
Platzi no están enumerados uno por uno: **no se inventan** - cuando se declaren, van con el nombre
real del curso.

> **Lo que falta precisar (no urgente):** la lista de cursos de Platzi y de otras plataformas, con
> nombre y año, si en algún momento se decide declararlos en un CV. El corpus registra la
> existencia de la formación continua; el detalle queda pendiente.

---

## 4. Certificaciones y credenciales

| Credencial | Estado | Cómo se escribe |
|---|---|---|
| Deque University Accessibility Specialist Program | Completado 2021 | "Deque University - Accessibility Specialist Program (2021)". Nunca "certification" |
| IAAP CPACC / WAS / CPWA | **NO la tiene** | No se menciona como obtenida |

**Gap real y único: sin certificación IAAP.** Es la palanca en curso (CPACC antes del 30/11), no un
hecho consumado. Prohibido insinuar una credencial IAAP: se verifica en el registro público y el
costo es la credibilidad completa.

---

## 5. Contribuciones open source

### 5.1 PRs propios mergeados (11)

| Repo | PR | Qué resolvió |
|---|---|---|
| adobe/react-spectrum | #10503 | Gate del anuncio de live-region del ComboBox a cambios de sección; dejaba de pisar el anuncio nativo por ítem de VoiceOver |
| adobe/react-spectrum | #10554 | Test de regresión (test-only) para `aria-posinset` global entre secciones |
| carbon-design-system/carbon | #22887 | Soporte explícito de la prop `aria-describedby` en `ComposedModal`, por la ruta nativa `<dialog>` y la de `div[role=dialog]` |
| carbon-design-system/ibm-products | #9878 | `CreateFullPage` (issue #9864) |
| carbon-design-system/ibm-products | #9879 | Datagrid (issue #9839) |
| facebook/astryx | #4605 | Indicador no cromático (font-weight) en el breadcrumb actual; WCAG 1.4.1 |
| facebook/astryx | #4914 | `build-storybook` fallaba con "no merge base" en PRs viejos (fetch-depth); fallback a diff de dos puntos |
| facebook/astryx | #5419 | HoverCard con label se exponía como dialog popup: `aria-haspopup=dialog` + `aria-controls` gateado en open, `aria-expanded` sincronizado |
| facebook/astryx | #5493 | `TreeList` reenvía `aria-label`/`aria-labelledby` al `<ul role=tree>`; un tree sin header no podía nombrarse |
| mui/base-ui | #5551 | `aria-orientation` movido a los dueños del rol; el rol grid no lo soporta |
| mui/material-ui | #49003 | Links focusables en slides ocultos del carrusel; WCAG 4.1.2 `aria-hidden-focus` |

### 5.2 Colaboración sin merge propio (valor real, sin autoría)

Trabajo cuyo diagnóstico o diseño fue la base de un fix que entró por otro autor. **No es material
de post** (la regla de branding lo prohíbe), sí es material de entrevista: evidencia de proceso.

- astryx #3764 - selector typeahead: el audit fue la base; el fix entró por PR ajeno (11/08).
- astryx #5107 - dividers/selector a11y: el trabajo previo (#5344, cerrado) fue el punto de partida.
- astryx #4157 / #5034 - avatar status labels.
- astryx #4777 - avatar status: cerrado por cixzhang **con crédito explícito** a Gonzo ("the
  parent-reads-child framing is what made this fixable").
- astryx #3349 - RFC InfoTip: único feedback sustantivo; el comportamiento implementado coincidió.

### 5.3 PRs cerrados sin merge (y qué enseñaron)

No son fracasos ocultos: son el registro de criterio.

- astryx #4994 - diagnóstico correcto (bug a11y crítico), pero entró otro PR con `aria-hidden`:
  trade de `aria-required-children` por `aria-allowed-attr`. El maintainer invitó a seguir.
- TanStack/router #7873 - el `console.log` de `AbortError` ya se había removido en main: el guard
  quedó redundante.
- TanStack/router #7861 y el PR de #9556 en react-spectrum - **lección durable: verificar contra
  main ANTES de abrir un PR cuando el issue es viejo.** El helper `getPosInSet` hacía doble conteo
  y el bug ya estaba resuelto upstream.
- swiftlang/swift-testing #686 - documentar `.serialized` en suites anidadas; quedó en hold porque
  la guía va a quedar obsoleta con el proposal de serialización.

### 5.4 En curso

PRs abiertos o esperando review en react-spectrum, shadcn/ui, vercel/ai, TanStack/router,
docusaurus, create-t3-app y otros. **Nunca contarlos como mergeados.**

---

## 6. Años, y por qué cada uno se dice así

### 6.1 Desarrollo total: 10+ años (feb 2016 - hoy)

Único headline permitido. No se suma el PHP 2001-2008.

### 6.2 Accesibilidad: SIN número

**Nunca** "N years of accessibility" ni "N+ años de accesibilidad", en ningún CV, carta o
screening. Ni 5, ni 6.

- **Por qué:** la aritmética de las fechas da 4.42 años de función central (Super7 0.75 + EY 3.67)
  y 5.83 contando todo el freelance. Un redondo obliga a elegir entre quedar corto o inflar, y el
  reclutador puede hacer la misma resta.
- **Cómo se cuenta:** nombrando los roles donde fue central -Super7UI (auditoría de Warner Bros.
  Screeners) y EY (50+ componentes enterprise a WCAG)- más las contribuciones OSS continuas.
- `a11y_years_internal: 5` es calibración interna. No es dato de salida.

### 6.3 IA para desarrollo: desde 05/2025, ~1 año y medio

**Nunca 3 ni 5.** Empieza cuando deja EY. Antes no usaba IA para desarrollo. Prohibido "5+ years
working AI-first", "three years" o "since 2021". Es el mismo período que el freelance.

### 6.4 Backend de producción: ~1 año y medio, nunca 4

Node.js/TypeScript con Supabase, Edge Functions y Stripe, todo del período freelance. En EY el rol
fue **full stack con foco frontend**, no backend de producción. Split declarado: **70/30
frontend/backend**.

### 6.5 SDLC en fases concurrentes: 3+ años (EY)

Trabajo en varias fases del SDLC en paralelo dentro de squads ágiles matriciales (US / India).

---

## 7. Idiomas

- **Español: nativo.**
- **Inglés: B2+.** Dato duro, definido por Gonzo y reafirmado tras un error que lo declaró C1.
  **Subió de B2 a B2+ el 27/10/2026**, cuando el CUI corrigió el nivel del curso por un error de
  inscripción (lo había anotado en B1+). **El '+' es confianza en el nivel, no un nivel CEFR
  distinto**: a efectos de gate, B2+ se normaliza a B2 (ver `scripts/check-cv-facts.py`,
  `normalize_level`).
  **Nunca** C1, C2, "fluent", "bilingual" ni "Advanced" en formularios, screenings, CVs o
  entrevistas. **Se actualiza a C1 solo cuando exista el certificado en la mano**: un C1 de papel
  que no se sostiene en una call es peor que un B2+ honesto.
- **El gap es oral, no escrito.** Lectura, escritura y trabajo diario están aceitados; falta
  práctica hablada. No ofrecerle cursos generales, academias ni gramática.
- **Plan vigente (decisión de Gonzo, 2026-10-22):** Gonzo **se anotó en el CUI (Centro Universitario
  de Idiomas, UBA) en el curso B2+ INTENSIVO de dos meses, martes y jueves de 10 a 13 h por Zoom, que arranca el martes 27/10/2026**. El
  objetivo declarado es **desoxidar y mejorar la base**, sin credencial de por medio: el nivel declarado sigue
  siendo B2+ y el gap sigue siendo oral. **El examen CUI-ING C1 y el TOEFL quedan para después**
  (TOEFL, 2027). **Mientras tanto, sigue buscando.**
  Esto **corrige** el plan del 2026-10-21, que era cursar el C1 completo y después el examen:
  la decisión de fondo del 2026-10-22 es **B2+ intensivo primero**, porque el nivel que Gonzo
  declara y el nivel que el CUI certifica son el mismo, y subir la base oral es lo que destraba
  el filtro de C1 conversacional. Calendario, costos y fuentes están en `studies/english/README.md`.
  **Lo que no es supuesto: B2+ intensivo, dos meses, arranca el 26/10/2026.**
- **Corrección del 27/10/2026 (Gonzo, desde la clase):** el curso es **B2+**, no B2: hubo un
  error de inscripción y quedó anotado en **B1+**, y lo corrigieron en el momento. **Horario:
  martes y jueves de 10 a 13 h, por Zoom.** La carga es la misma que se planificó (2 clases x 3 h
  por semana), así que **no cambia el diagnóstico sobre la entrevista de noviembre** (3 semanas de
  clases para el 9-13/11). **Lo que esto no cambia: el nivel declarado sigue siendo B2+** - anotarse
  en un curso no sube el nivel declarado, y el CUI-ING C1 sigue siendo el examen del 2027.
- **Situación al 27/10/2026 (actualización de Gonzo):** el curso **ya arrancó** (26/10). Los
  5 recruiters recontactados por el tema del inglés respondieron (5/5) y **2 tienen próximo paso
  con fecha concreta: solo Siraj/Disney (entrevista en la 1ra o 2da semana de noviembre)**. Los
  otros 3 aceptaron "volver a hablar en uno o dos meses" o "te avisamos", que **no es una fecha
  ni una promesa de puesto** (ver `docs/entrevistas/_general/job-search-tracker.md`).
  **Lo que se declara ante terceros mientras tanto: B2+.** El nivel sube cuando el nivel real sube.
  **Advertencia de credibilidad (registrada el 27/10):** el mensaje de recontacto decía *"I'm
  retaking the course"* y *"re-validate my B2 level"*, que presuponen un curso previo y un
  certificado de B2 que **este corpus no tiene** (§4 solo tiene Deque). Si un recruiter
  repregunta fechas, no hay respuesta. **La forma verificable y con el mismo impacto:** *"I started
  a B2+ intensive course at the CUI (UBA) today - two months - and I plan to take the C1
  certification exam next year."*
- **Regla de proceso que sale de los 3 casos:** en el **primer mensaje** de cualquier proceso
  LATAM remoto, preguntar el **nivel de inglés conversacional que exige el cliente**. El filtro
  apareció al final en ambos casos cerrados (Staffy 20/10, Sol 21/10), cuando ya se había armado
  CV, screening y prep de call.
- **Cuarto caso (TEAM International / tempo.io, 26/10/2026):** la posición de Tempo **cerró** (el
  Delivery Manager recomendó no avanzar: el equipo del cliente que entrevista y trabaja con la
  persona **está en Europa** y es exigente con la fluidez **"al discutir y explicar temas
  técnicos"**), pero **la relación con TEAM sigue viva**: David mantiene el perfil en el talent
  pool y reevalúa cuando Gonzo esté más cómodo con el idioma. **Dos capas, dos estados: la
  posición se cae, la relación no.** El mismo David lo había adelantado en la entrevista
  ("reevaluación para ese u otro proyecto").
  **El dato que generaliza la regla:** el filtro no depende de la geografía del cliente. El equipo
  de Tempo estaba en Europa, y el de Pfizer en US, y el de Disney en US, y la exigencia es la
  misma: **poder sostener una conversación técnica en vivo y explicar decisiones** - no es de
  acento, ni de horario, ni de lengua materna (Reikiavik, sede de Tempo, es lingua franca en
  inglés). La regla que sirve: **roles que exigen comunicación técnica fluida en inglés** - y esa
  habilidad ya la tiene Gonzo (en EY escribía los requisitos técnicos de accesibilidad con
  ejemplos de código y revisaba diseños antes de implementar). **El gap de idioma es oral; la
  habilidad que el cliente pide no es su gap.**
- **Tercer caso (Infjini / Disney, 26/10/2026):** en la
  entrevista el recruiter dijo que le encantaba el perfil técnico y que el bloqueo era el **nivel
  de inglés conversacional (C1), "como a todos los demás"**. Gonzo ya había propuesto el curso de
  inglés y una reevaluación en 1-2 meses; David aceptó: habla con el cliente (Tempo) para
  continuar, y si no puede, **reevaluación para ese u otro proyecto**. **Compromiso de
  reevaluación, no cierre.**
  **La variante nueva del patrón: el nivel exigido NO coincide con el del JD.** El JD pedía
  **B2+** y el requisito real del cliente es **C1 conversacional**. En una **agency** (nearshore)
  el idioma no es un requisito del rol sino una **condición de elegibilidad** que impone el
  cliente, y por eso el recruiter no decide: tiene que hablar con el cliente.
  **Consecuencia operativa: un JD no es un contrato de elegibilidad cuando el cliente es una
  agency.** La pregunta del nivel de inglés es la que descubre eso, y por eso va en el primer
  mensaje.
- **Lo que NO se afirma (regla de credibilidad):** Gonzo no tiene certificado de B2 registrado en
  el corpus (§4 solo tiene Deque) ni antecedente de un curso de inglés previo. Los mensajes a
  recruiters que rebotaron por el idioma **no** deben decir "I'm retaking the course" ni
  "re-validate my B2 level": presuponen una acreditación o un curso anterior que no están
  registrados. **La forma verificable y igual de fuerte:** "I started a B2+ intensive course at
  the CUI (UBA) today, two months, and I plan to take the C1 certification exam next year." -
  eso es exactamente lo que dice el corpus. En un proceso donde el idioma es el filtro, la
  credibilidad es lo único que no se negocia, y un recruiter repregunta fechas.

---

## 8. Proyectos propios

| Proyecto | Estado | Qué es |
|---|---|---|
| SoporteML | Activo (producto) | CRM con IA para vendedores de MeLi. Pro Motors como cliente. Stripe operativo |
| Kanam OnWheels | En curso | Sitio de concesionario multi-marca (KTM, Husqvarna, Can-Am, Sea-Doo, Ski-Doo, Segway) con chatbot RAG que responde **solo con evidencia citada**. Regalo para el local de su hermano, sin billing |
| kanam-pulse | Activo | Monitor de salud del sistema. M1: engine a `packages/core` (TS), dashboard read-only |
| kanam-forge | Activo | Lovable self-hosted, fusionado con `create-with-ai` |
| Kanam Mind | Activo | Segundo cerebro local-first: timeline, CRUD accesible, resumen IA, IndexedDB |
| create-stack | Vivo | Scaffolder opinado Next.js (`@gonzoblasco/create-stack`) |
| kanam-solitaires / tetris / minesweeper / sudoku / match3 | Vivos | Juegos, ejercicios de UI |
| a11y-fixer | **Archivado 2026-09-14** | v0.6.0. Su sucesor es `kanam-fixer`, proyecto NUEVO (no un renombre) |
| a11y-playground | Dependencia en riesgo | Capa visual de testing sobre a11y-fixer; su base quedó archivada |
| kanam-insight | **Descontinuado 2026-10-06** | Motor de insights sobre los `.knowledge/`. El repo existe; el proyecto no |
| kanam-skills | **Archivado 2026-09-28** | Repo público de skills; la colección ya no se publica (ADR-079) |
| create-with-ai / ai-engineering-bootcamp | Archivados | Fusionado / curso completado 10/10 |
| accessibility-auditor | **Archivado 2026-10-20** | **NO mencionar en CVs, portfolios, propuestas ni narrativa pública.** Ya no resuelve en GitHub |

---

## 9. Lo que NO se hace (decisiones cerradas)

Evita que un CV nuevo o una propuesta los reintroduzcan por descuido:

- **Cripto / Web3:** nada de blockchain, tokens, wallets, DeFi, NFT, chains ni mercados on-chain.
  Descartado de plano, sin analizar.
- **Mercado Pago:** fuera. **Stripe es el proveedor único** (ADR-042), con o sin Lovable.
- **`accessibility-auditor`:** nunca se menciona. Para el mismo eje a11y + tooling, usar los PRs
  mergeados y Super7UI/Warner Bros.
- **SoporteML:** va al CV y a las propuestas laborales, pero **no** al portfolio público (repo
  privado) ni como ancla de la estrategia de proyectos.
- **Kotlin, Rust, Go:** no son parte del stack. No listarlos por completitud.

---

## 10. Perfiles: qué selecciona cada uno

Todos parten del mismo corpus. Cambia el énfasis, nunca el hecho.

| Perfil | Headline | Destaca | Omite | Nunca cambia |
|---|---|---|---|---|
| **a11y** | Digital accessibility engineer | Super7UI/Warner Bros, EY Motif, WCAG 2.2 AA, lectores de pantalla, PRs de a11y en Adobe/IBM/Meta/MUI | Backend, billing | Fechas, años, B2, Deque como programa |
| **Fullstack / AI-native** | Senior full stack engineer | SoporteML end-to-end, Supabase/Edge/Stripe, 70/30, AI Engineering OS | Detalle de auditorías WCAG | Años totales 10+, IA desde 2025 |
| **Frontend / code evaluator** | Frontend engineer | Lectura de estructura (ARIA, landmarks, headings), reviews con evidencia, Playwright/Vitest | Producto propio | Pruebas de que revisa código real |
| **No técnico** | Perfil de gestión y operaciones | Coordinación, clientes internacionales, atención al detalle, procesos | Stack, siglas | Los mismos 10+ años y el mismo Deque |
| **Agentic / AI-native** | AI-first engineer | Sistema propio de trabajo, subagentes, memoria persistente, skills | Historia pre-2025 | IA desde 2025, nunca antes |
| **AI-native frontend** (agregado 2026-10-22) | AI-first Frontend Engineer | React/TS + design systems + a11y + IA en el flujo; AI Engineering OS, método quarantine→verify→adopt, 11 PRs mergeados | Detalle de auditorías WCAG, backend | Años totales 10+, IA desde 2025, B2, Deque como programa |

**Regla del filtro:** si un perfil necesita un hecho que no está en este archivo, se agrega acá
primero. Un CV no puede ser la fuente de un hecho nuevo.

---

## 11. Falta relevar

Lo que el corpus todavía no tiene y no se debe inventar:

1. **Estudios formales:** **resuelto el 21/10/2026** - ver §3. No hay título universitario
   completo; hay registros parciales contradictorios (Digital House 2018, UADE Diseño Gráfico
   2003-2004, Palermo Ing. en Informática 2001-2002 incompleta) que hay que confirmar con Gonzo
   antes de escribir cualquier línea de educación. **Lo que queda abierto:** el motivo de haber
   abandonado la carrera de Palermo, y si hay algún título o certificación de CS fuera de la lista.
2. **Arquitectura de micro frontends y biblioteca de componentes (Minutentag):** **PENDIENTE DE
   RESOLVER CON GONZO.** El markdown del CV de Infjini declara que Gonzo "architect and built"
   la arquitectura de micro frontends para 2M+ usuarios mensuales y que desarrolló una biblioteca
   de componentes compartida por 5 equipos de producto. **El corpus no lo registra**: dice que
   *participó* de la migración a React y que mejoró un sitio con 2M+ usuarios mensuales, sin
   atribuirle la arquitectura ni las bibliotecas. Esos dos bullets **no están en los DOCX ni PDF
   que se mandaron**, solo en el markdown fuente. Si no los confirma, salen del markdown; si los
   confirma, van a §2.4 primero y después vuelven al CV (ADR-101).
   **Lo que ya está resuelto y no vuelve a ser pregunta:** la primera mitad de este punto, el uso
   de la herramienta de experimentación del equipo en 2019, está confirmado por Gonzo y
   registrado en §2.4 (incluyendo el detalle de implementar las variantes con snippets en
   JavaScript nativo, confirmado el 21/10/2026). El claim de haber construido la infraestructura
   de experimentación **no** está confirmado, y ese bullet se sacó del markdown del CV de Infjini.
   **Lo que sigue abierto:** (a) si Gonzo construyó la arquitectura de micro frontends y la
   biblioteca de componentes compartida, y (b) el alcance de su rol en la librería (¿la construyó
   entero, la mantenía, o la consumía?).
3. **Fechas exactas de inicio y fin del PHP 2001-2008**: hay años, no meses.
4. **Nombres de clientes o empleadores bajo NDA**, si los hubiera.
4. **Referencias laborales**: quién puede hablar de su trabajo en EY o Super7UI.
