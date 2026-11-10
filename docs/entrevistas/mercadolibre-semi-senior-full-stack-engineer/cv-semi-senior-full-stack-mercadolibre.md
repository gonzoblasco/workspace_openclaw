# Gonzalo Blasco

**Semi Senior Full Stack Engineer (Mercado Libre) | React, TypeScript y AI en producción**

Núñez, Buenos Aires, Argentina | Híbrido Buenos Aires | +54 11 4937 4656 | gonzoblasco@icloud.com | linkedin.com/in/gonzalo-blasco | github.com/gonzoblasco

## Perfil

Ingeniero de software con más de 10 años de experiencia, los últimos 1,5 construyendo productos con IA. Trabajo entre producto y código: relevo lo que el equipo necesita, lo convierto en solución full stack y dejo el camino pavimentado para que otros la usen. Stack principal: React, TypeScript y Next.js en frontend, y Node.js + Supabase/PostgreSQL en backend. Design systems y accesibilidad son el estándar de calidad, no un plus. Hoy tengo una ventaja de dominio que pocos candidatos tienen: SoporteML, un CRM con IA para vendedores de Mercado Libre, producto propio en producción con integración real a MeLi - el mismo dominio de este rol. Tengo experiencia entregando con squads ágiles cross-regionales y manejo de bases de datos relacionales en producción.

## Competencias

- **Frontend:** React, TypeScript, JavaScript, Next.js, Vite, HTML5, CSS3, Tailwind, Storybook, arquitectura de componentes, design systems, design tokens, prototipado rápido.
- **Backend y datos:** Node.js, APIs REST, Supabase (PostgreSQL, Auth, Realtime, RLS, Edge Functions), pgvector, SQL (modelado de datos, consultas, transacciones, cambios de esquema), webhooks.
- **IA aplicada al producto:** flujos agénticos con subagentes y skills, RAG con pgvector, automatización de tareas de exploración y verificación del código generado antes de integrarlo.
- **Calidad y entrega:** Vitest, Playwright, Jest + React Testing Library, Biome, Zod, Git/GitHub, CI/CD, Azure DevOps (pipelines, tickets y user stories), Jira, SDLC ágil, code review, seguimiento de servicios en producción.
- **Colaboración y producto:** relevo de necesidades de equipos internos, traducción a requisitos técnicos con guía de código, acompañamiento a desarrolladores, equipos matriciales US/India.
- **Accesibilidad (diferencial):** WCAG 2.2 AA, patrones ARIA, lectores de pantalla (JAWS, NVDA, VoiceOver, TalkBack), Axe DevTools, Lighthouse, validación automatizada en CI.

## Experiencia

### Freelancer - Software Engineer
*05/2025 - Presente | Remoto*

- Construyo **SoporteML**, un CRM multi-tenant con IA para vendedores de Mercado Libre: frontend React + Vite + TypeScript, backend Supabase (PostgreSQL, Auth, Realtime, RLS, Edge Functions), sugerencias de respuesta con RAG sobre pgvector, Autopilot con guardrails de confianza, multi-empresa y roles de equipo, y billing con Stripe vía webhooks. Primer cliente en producción: Pro Motors (pro-motors.com.ar), con integración real de Mercado Libre.
- Construí un AI Engineering OS sobre OpenClaw: sesiones por proyecto, memoria persistente, handoffs, subagentes, skills reutilizables y pipeline de contribución open source. Método de trabajo: quarantine -> analyze -> verify -> adopt.
- Diseño e implemento flujos agénticos en producción: sesiones por proyecto con contexto acotado y verificación antes de que la salida llegue al usuario.
- Construyo y mantengo el design system de mis propios productos: sistema de tokens semánticos (color, tipografía, spacing, focus-ring, estados), escala tipográfica y mapa token -> componente, con las reglas WCAG AA como criterio del sistema.

### EY (Ernst & Young) - Senior Full Stack / Frontend Engineer, Team Lead
*09/2021 - 05/2025 | Híbrido*

- Lideré un equipo de 3 ingenieros construyendo una plataforma de inteligencia financiera con IA en Next.js, con interfaces accesibles de arquitectura a producción. Ese Next.js es el origen documentado de mi trabajo con SSR.
- Trabajé en equipo matricial cross-regional (US / India), con varias fases del SDLC en paralelo dentro de squads ágiles y múltiples stakeholders.
- Lideré la accesibilidad de EY Motif, librería de componentes React enterprise consumida por productos de cliente e internos: remedié 50+ componentes a WCAG 2.2 AA (navegación por teclado, soporte de lector de pantalla, manejo de foco, contraste), con Axe DevTools, Lighthouse, JAWS y NVDA.
- Fui referente de accesibilidad del equipo en varios proyectos: revisaba componentes en Storybook antes de implementarlos, definía estándares y anotaciones a nivel componente, y escribía requisitos técnicos de accesibilidad con guía de código para las historias de UI.
- Prioricé defectos de accesibilidad por impacto WCAG en Jira, con guía de remediación a desarrolladores dentro del sprint.

### Super7UI - Accessibility Engineer (Contratista)
*08/2020 - 05/2021 | Remoto*

- Lideré la auditoría y remediación de frontend de Warner Bros. Screeners (WBTVD), la plataforma de streaming privada que distribuidores globales usan para revisar contenido.
- Validé y expandí una auditoría previa de terceros reproduciendo cada issue reportado en NVDA, VoiceOver y TalkBack, y usé Axe para identificar y documentar violaciones WCAG en los flujos clave.
- Resolví 200+ violaciones WCAG y produje documentación de remediación lista para desarrollo.
- Establecí un pipeline de testing de accesibilidad con axe-core + Playwright integrado en CI/CD.

### Minutentag - Frontend Developer, Accessibility Owner
*02/2016 - 11/2019 | Híbrido*

- Participé de la migración a React y mejoré un sitio con 2M+ usuarios mensuales, manteniendo los flujos de compra (checkout, carrito) para Ann Taylor, LOFT y Lou & Grey.
- Crecí de junior a referente de accesibilidad del equipo.
- Corrí experimentos A/B en producción con Adobe Target contra segmentos de usuarios en vivo sobre features y diseños, dentro de squads ágiles junto a diseño y producto, implementando las variantes como snippets en JavaScript nativo.

## Contribuciones a design systems - Pull Requests mergeados

Fixes mergeados en librerías de componentes y design systems de producción, cada uno revisado y publicado por sus maintainers. Total: 11 PRs mergeados en Adobe React Spectrum, IBM Carbon/ibm-products, Meta Astryx y MUI Base UI / Material-UI.

- **adobe/react-spectrum #10503** - Gate del anuncio de live-region del ComboBox a cambios de sección; dejaba de pisar el anuncio nativo por ítem de VoiceOver.
- **adobe/react-spectrum #10554** - Test de regresión (test-only) para `aria-posinset` global entre secciones.
- **carbon-design-system/carbon #22887** - Soporte explícito de la prop `aria-describedby` en `ComposedModal`, por la ruta nativa `<dialog>` y la de `div[role=dialog]`.
- **carbon-design-system/ibm-products #9878** - `CreateFullPage` (issue #9864).
- **carbon-design-system/ibm-products #9879** - Datagrid (issue #9839).
- **facebook/astryx #4605** - Indicador no cromático (font-weight) en el breadcrumb actual; WCAG 1.4.1.
- **facebook/astryx #4914** - `build-storybook` fallaba con "no merge base" en PRs viejos (fetch-depth); fallback a diff de dos puntos.
- **facebook/astryx #5419** - HoverCard con label se exponía como dialog popup: `aria-haspopup=dialog` + `aria-controls` gateado en open, `aria-expanded` sincronizado.
- **facebook/astryx #5493** - `TreeList` reenvía `aria-label`/`aria-labelledby` al `<ul role=tree>`; un tree sin header no podía nombrarse.
- **mui/base-ui #5551** - `aria-orientation` movido a los dueños del rol; el rol grid no lo soporta.
- **mui/material-ui #49003** - Links focusables en slides ocultos del carrusel; WCAG 4.1.2 `aria-hidden-focus`.

## Contribuciones con revisión y diagnóstico (sin autoría propia)

- **facebook/astryx #4777 (avatar status):** cerrado por cixzhang con crédito explícito a mi diagnóstico ("the parent-reads-child framing is what made this fixable").
- **facebook/astryx #5107 (dividers / selector de accesibilidad):** el trabajo previo fue el punto de partida del fix que entró.
- **facebook/astryx #3764 (selector typeahead):** el audit fue la base; el fix entró por un PR ajeno.
- **facebook/astryx #4157 / #5034 (avatar status labels):** diagnóstico compartido con el mantenedor.
- **facebook/astryx #3349 (RFC InfoTip):** único feedback sustantivo; el comportamiento implementado coincidió.
- **carbon-design-system/ibm-products #9869 (Tearsheet layer hierarchy):** primer reviewer humano del PR ajeno; el diagnóstico del cluster React 19 quedó en #9865 y el PR mergeó.
- **vercel/next.js #73474:** diagnóstico validado por el maintainer al cerrar el issue.

## Formación y certificaciones

- **Digital House - React (2018)**
- **Deque University - Accessibility Specialist Program (2021)**

## Idiomas

- Español - nativo
- Inglés - B2+

## Notas / gaps

- **Go no es parte de mi stack.** Mi backend de producción es Node.js/TS sobre Supabase/Postgres. Declaramos el gap; mi aporte en el corto plazo está en el full-stack y la capa de API/BD, y aprendo rápido con tests.
- **Python: working proficiency**, no nivel avanzado; no Django.
- **Redis / cache en producción:** no la tengo documentada como propia; solo la declaro si el equipo la necesita y me el tiempo para levantarla.
- **Observabilidad en producción:** seguimiento día a día de servicios y logs; no profunda en APM/tracing distribuido.
- **Seniority:** tengo 10+ años totales, pero solo ~1,5 año de backend de servicios. Por eso "semi senior" es el nivel honesto para este eje, no "senior backend".
- **Sin título universitario completo.** Deque es un programa 2021, no una credencial IAAP. Incompleta toda la formación universitaria.
- **Figma:** lo uso desde ingeniería (revisión de componentes y diseño antes de implementar), no como diseñador.
- **Fuerza real a capitalizar:** SoporteML comparte dominio, APIs reales de Mercado Libre y autonomía full-stack. Lo segundo más fuerte es el trabajo con Next.js SSR y design systems.

## Mapa de keywords

| Keyword del JD | Cobertura |
|---|---|
| Experiencia backend con Go o lenguajes similares orientados a servicios | Parcial - Node.js/TS + Postgres; Go no está en el stack (gap declarado) |
| Python + frameworks modernos de frontend (React, Next.js) + TypeScript | Fuerte en React/Next/TS; Python working proficiency |
| Soluciones full stack en producción y contexto de múltiples equipos | Cubierto (SoporteML, EY Next.js + equipos US/India) |
| Bases de datos relacionales y SQL (modelado, consultas, transacciones, cambios de esquema) | Cubierto (PostgreSQL/Supabase, RLS, migraciones) |
| Buenas prácticas de calidad y mantenimiento, pruebas | Cubierto (Vitest, Playwright, Jest + RTL, CI/CD) |
| Control de versiones | Cubierto (Git/GitHub) |
| Seguimiento de servicios en producción | Parcial |
| Redis u otras tecnologías de caché | Gap (no declarada propia) |
| CI/CD y observabilidad | CI/CD cubierto; observabilidad parcial |
| Diseñar herramientas de autoservicio que reduzcan dependencia en especialistas técnicos | Cubierto (SoporteML multi-tenant, design system) |
| Soluciones backend robustas para automatizaciones financieras | Cubierto (Stripe, Edge Functions, validación de pagos) |
| Experiencias full stack que integren procesos de negocio con IA | Cubierto (RAG, agentes, Autopilot) |
| Identificar patrones comunes y convertirlos en capacidades reutilizables | Cubierto (tokens, AI Engineering OS, subagentes/skills) |
| Relevar necesidades de equipos usuarios y traducirlas en soluciones simples y confiables | Cubierto (EY: requisitos técnicos, anotaciones; SoporteML) |
| Estándares de calidad y pruebas para adoptar cada nueva herramienta con seguridad | Cubierto (tests en CI, gates, axe-core) |
