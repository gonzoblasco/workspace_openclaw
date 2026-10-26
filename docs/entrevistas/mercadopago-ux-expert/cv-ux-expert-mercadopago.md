# Gonzalo Blasco

**UX Expert - Software (Mercado Pago) | Diseño e Ingeniería de Producto**

Núñez, Buenos Aires, Argentina | Híbrido Buenos Aires | +54 11 4937 4656 | gonzoblasco@icloud.com | linkedin.com/in/gonzalo-blasco | github.com/gonzoblasco

## Perfil

Ingeniero de software con más de 10 años de experiencia, los últimos 1,5 construyendo productos con IA. Trabajo en el medio entre diseño e ingeniería: reviso los componentes en Storybook antes de implementarlos, escribo los requisitos técnicos que hacen que un diseño se implemente bien, y hago que el código y el diseño no se separen. React y TypeScript son el stack principal, con design systems y accesibilidad como estándar de calidad y no como un plus. Hoy construyo productos propios de punta a punta, incluidos flujos AI-native con agentes, y uno de ellos es SoporteML: un CRM con IA para vendedores de Mercado Libre, el mismo dominio de este rol.

## Competencias

- **Frontend:** React, TypeScript, JavaScript, Vite, Next.js, HTML5, CSS3, Tailwind, Storybook, arquitectura de componentes, design systems, design tokens, prototipado rápido.
- **Diseño a código:** revisión de diseño previa a la implementación, requisitos técnicos con guía de código para historias de UI, anotaciones a nivel componente, implementación fiel de los componentes del design system.
- **IA aplicada al producto:** flujos agénticos con subagentes y skills (OpenClaw), RAG con pgvector, automatización de tareas de exploración y verificación del código generado antes de integrarlo.
- **Accesibilidad (diferencial):** WCAG 2.2 AA, patrones ARIA (cableado de role, state y property), lectores de pantalla (JAWS, NVDA, VoiceOver, TalkBack), Axe DevTools, Lighthouse, validación de accesibilidad automatizada en CI.
- **Backend y datos:** Node.js, APIs REST, Supabase (PostgreSQL, Auth, Realtime, RLS, Edge Functions), pgvector, billing con Stripe, webhooks.
- **Calidad y entrega:** Vitest, Playwright, Biome, Zod, CI/CD, Git/GitHub, Jira, SDLC ágil, code review, acompañamiento a desarrolladores.

## Experiencia

### Freelancer - Software Engineer
*05/2025 - Presente | Remoto*

- Construí **SoporteML**, un CRM multi-tenant con IA para vendedores de Mercado Libre: frontend React + Vite + TypeScript, backend Supabase (PostgreSQL, Auth, Realtime, RLS, Edge Functions), sugerencias de respuesta con RAG sobre pgvector, Autopilot con guardrails de confianza, multi-empresa y roles de equipo, y billing con Stripe vía webhooks. Primer cliente en producción: **Pro Motors** (pro-motors.com.ar), con integración real de Mercado Libre.
- Construí un **AI Engineering OS** sobre OpenClaw: sesiones por proyecto, memoria persistente, handoffs, subagentes, skills reutilizables y pipeline de contribución OSS. Su método de trabajo es quarantine → analyze → verify → adopt: nada de lo que entra de afuera se adopta sin leerse, analizarse y verificarse.
- Diseño e implemento flujos agénticos en producción: sesiones por proyecto, subagentes con contexto acotado y verificación de la salida antes de que la salida llegue al usuario.
- Construyo y mantengo el design system de mis propios productos: sistema de tokens semánticos (color, tipografía, spacing, focus-ring, estados), escala tipográfica y mapa token→componente, con las reglas WCAG AA como criterio del sistema.

### EY (Ernst & Young) - Senior Frontend Engineer, Accessibility Lead
*09/2021 - 05/2025 | Híbrido*

- Lideré la accesibilidad de **EY Motif**, librería de componentes React enterprise consumida por productos de cliente e internos: remedie **50+ componentes** a WCAG 2.2 AA (navegación por teclado, soporte de lector de pantalla, manejo de foco, contraste), con Axe DevTools, Lighthouse, JAWS y NVDA.
- Fui el referente de accesibilidad del equipo en varios proyectos: revisaba componentes de Storybook **antes de implementarlos**, definía estándares y anotaciones a nivel componente, y escribía requisitos técnicos de accesibilidad con guía de código para las historias de UI.
- Prioricé defectos de accesibilidad por impacto WCAG en Jira, con guía de remediación a desarrolladores dentro del sprint.
- Lideré un equipo de 3 ingenieros construyendo una plataforma de inteligencia financiera con IA en Next.js, con interfaces accesibles de arquitectura a producción.
- Trabajé en un equipo matricial cross-regional (US / India), con varias fases del SDLC en paralelo dentro de squads ágiles.

### Super7UI - Accessibility Engineer (Contratista)
*08/2020 - 05/2021 | Remoto*

- Lideré la auditoría y remediación de frontend de **Warner Bros. Screeners (WBTVD)**, la plataforma de streaming privada que distribuidores globales usan para revisar contenido.
- validé y expandí una auditoría previa de terceros reproduciendo cada issue reportado en **NVDA, VoiceOver y TalkBack**, y usé Axe para identificar y documentar violaciones WCAG en los flujos clave.
- Resolví **200+ violaciones WCAG** y produje documentación de remediación lista para desarrollo: soluciones propuestas, guía de implementación y especificaciones listas para desarrollo.
- Establecí un pipeline de testing de accesibilidad con **axe-core + Playwright integrado en CI/CD**, para que el código no conforme no pudiera mergear.

### Minutentag - Frontend Developer, Accessibility Owner
*02/2016 - 11/2019 | Híbrido*

- Participé de la **migración a React** y mejoré un sitio con **2M+ usuarios mensuales**, manteniendo los flujos de compra (checkout, carrito) para Ann Taylor, LOFT y Lou & Grey.
- Crecí de junior a referente de accesibilidad del equipo.
- Corrí **experimentos A/B en producción con Adobe Target** contra segmentos de usuarios en vivo sobre features y diseños, dentro de squads ágiles junto a diseño y producto, implementando las variantes como snippets en JavaScript nativo.

## Contribuciones a design systems - Pull Requests mergeados

Fixes mergeados en librerías de componentes y design systems de producción, cada uno revisado y publicado por sus maintainers.

- **carbon-design-system/carbon #22887** - Soporte explícito de la prop `aria-describedby` en `ComposedModal`, por la ruta nativa `<dialog>` y la de `div[role=dialog]`.
- **facebook/astryx #4605** - Indicador no cromático (font-weight) en el breadcrumb actual; WCAG 1.4.1.
- **mui/material-ui #49003** - Links focusables en slides ocultos del carrusel; WCAG 4.1.2 `aria-hidden-focus`.
- Ocho PRs más mergeados en IBM Carbon, Meta Astryx, MUI Base UI y Adobe React Spectrum (semántica ARIA, foco, focus order, cableado de roles).

## Educación y certificaciones

- **Deque University - Accessibility Specialist Program (2021)**
- **Digital House - React (2018)**

## Idiomas

- Español - nativo
- Inglés - B2 (lectura y escritura cómodas; el inglés hablado es mi área de desarrollo actual)

## Notas / vacíos

- **Generación de imágenes con IA para diseño** - mi trabajo de IA es de código, agentes y RAG, no de generación visual.
- **Diseño de producto / research** - mi trabajo de diseño fue siempre desde ingeniería: requisitos técnicos, anotaciones, accesibilidad y design system. No es diseño de producto ni research de usuario.
- **Mobile / plataformas nativas** - mi experiencia es web (React); no he trabajado en apps nativas.
- **Diferencial que sí tengo:** SoporteML es un CRM para vendedores de Mercado Libre - el mismo dominio del rol, como producto propio y no dentro de una plataforma existente.
