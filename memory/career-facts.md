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
english: B2
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
- **Idiomas:** español nativo; **inglés B2** (dato duro, ver §7).

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
- **AI Engineering OS sobre OpenClaw** - sistema propio de trabajo con IA: sesiones por proyecto,
  memoria persistente, handoffs, subagentes, skills, pipeline de contribución OSS.
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
- **Referente de accesibilidad del equipo** en varios proyectos: revisaba componentes de Storybook
  y diseños **antes** de implementar, definía estándares y anotaciones a nivel componente, y
  escribía requisitos técnicos de accesibilidad con guía de código para las historias de UI.
- **Defectos de accesibilidad priorizados por impacto WCAG** en Jira, con guía de remediación a
  desarrolladores en sprint.
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

- Agencia de e-commerce para marcas de EE.UU. Desarrolló y mantuvo **flujos de compra** (checkout,
  carrito).
- Participó de la **migración a React** y mejoró un sitio con **2M+ usuarios mensuales**.
- **Accesibilidad desde el inicio**: creció de junior a referente de accesibilidad del equipo.

### 2.5 Antes de 2016 - backend PHP, 2001 a 2008

Trabajo real, pero **no se suma al total ni se usa como headline**: es backend (no a11y) y hay un
gap de ~8 años (2008-2016). Solo defendible como amplitud ("20+ años en software") ante audiencia
que no vaya a preguntar por el gap. Decidir por audiencia, nunca por defecto.

---

## 3. Educación y formación

- **Formación continua en accesibilidad digital y calidad de software.** No hay título
  universitario registrado en el corpus.
- **Deque University - Accessibility Specialist Program (2021).** Programa de cursos, NO una
  credencial profesional. Cursos: Accessibility Fundamentals, Designing an Accessible User
  Experience, Semantic Structure and Navigation, Images/SVG/Canvas, IAAP Certification Quick Guide.
  **`IAAP Certification Quick Guide` es el nombre de un curso.** No insinúa estar certificado.
- **`ai-engineering-bootcamp`:** curso propio completado 10/10, archivado.

> **Falta relevar:** si hubo estudios formales (universitarios o terciarios), hoy no están
> documentados. No inventar ni inferir. Preguntar antes de escribir cualquier línea de educación
> en un CV.

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
- **Inglés: B2.** Dato duro, definido por Gonzo y reafirmado tras un error que lo declaró C1.
  **Nunca** C1, C2, "fluent", "bilingual" ni "Advanced" en formularios, screenings, CVs o
  entrevistas. **Se actualiza a C1 solo cuando exista el certificado en la mano**: un C1 de papel
  que no se sostiene en una call es peor que un B2 honesto.
- **El gap es oral, no escrito.** Lectura, escritura y trabajo diario están aceitados; falta
  práctica hablada. No ofrecerle cursos generales, academias ni gramática.
- **Plan vigente (decisión de Gonzo, 2026-10-21):** a raíz de dos procesos cerrados por el mismo
  filtro de **C1 conversacional** (Staffy 20/10, Sol 21/10). Gonzo se anota en el **CUI (Centro
  Universitario de Idiomas, UBA)** para la capacitación de C1 y su certificación, **mientras tanto
  sigue buscando**. Instrumentos, costos, fechas y el riesgo de la mesa del 6/11 están en
  `studies/english/README.md` (con fuentes de `cui.edu.ar` leídas el 2026-10-21).
- **Regla de proceso que sale de los 2 casos:** en el **primer mensaje** de cualquier proceso
  LATAM remoto, preguntar el **nivel de inglés conversacional que exige el cliente**. El filtro
  apareció al final en ambos casos, cuando ya se había armado CV, screening y prep de call.

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

**Regla del filtro:** si un perfil necesita un hecho que no está en este archivo, se agrega acá
primero. Un CV no puede ser la fuente de un hecho nuevo.

---

## 11. Falta relevar

Lo que el corpus todavía no tiene y no se debe inventar:

1. **Estudios formales** (universitario / terciario / secundario): sin registro.
2. **Fechas exactas de inicio y fin del PHP 2001-2008**: hay años, no meses.
3. **Nombres de clientes o empleadores bajo NDA**, si los hubiera.
4. **Referencias laborales**: quién puede hablar de su trabajo en EY o Super7UI.
