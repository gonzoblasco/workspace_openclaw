# Gonzalo Blasco

**Desarrollador Full Stack Senior · Sistemas Web de Gestión, Integraciones y Automatización con IA**

Núñez, Buenos Aires, Argentina | Remoto | +54 11 4937 4656 | gonzoblasco@icloud.com | linkedin.com/in/gonzalo-blasco | github.com/gonzoblasco

## Perfil

Desarrollador full stack con más de 10 años construyendo aplicaciones web de gestión operativa: software que ordena el día a día de un negocio, integra datos de terceros y elimina trabajo manual repetitivo. Trabajo con React, TypeScript y Next.js del lado de la interfaz, y con Node.js, PostgreSQL/Supabase y Edge Functions del lado del servidor, incluyendo productos multi-empresa con permisos por rol y facturación. En el último año y medio incorporé IA al software de forma medible: búsqueda semántica sobre documentos (RAG), automatización con reglas de confianza y asistentes que responden solo con evidencia. Esa combinación —operación, datos en tiempo real y automatización— es exactamente el problema que resuelve un sistema de gestión de flotas.

## Experiencia

### Freelance - Desarrollador Full Stack

*05/2025 - Actualidad | Remoto*

- Construí **SoporteML**, un CRM multi-empresa con IA para vendedores de Mercado Libre, en producción con clientes comerciales: bandeja unificada de consultas, roles de equipo, facturación con Stripe y sugerencias de respuesta con RAG (pgvector + embeddings) sobre React, Vite, TypeScript y Supabase/PostgreSQL. Integración real con la API de Mercado Libre.
- Implementé el modo **Autopilot** con reglas de confianza: las respuestas automatizadas solo se envían dentro de umbrales definidos y el resto queda para una persona. Es automatización que se puede auditar, no una caja negra.
- Diseñé el **design system** del producto: tokens semánticos de color, tipografía, espaciado, estados y foco, documentados y aplicados sobre Tailwind CSS con criterio WCAG AA, para que la interfaz escale sin inconsistencias.
- Desarrollé **herramientas internas con IA** para automatización comercial y una plataforma web con asistente conversacional que responde estrictamente sobre evidencia documental (Kanam OnWheels), más un servidor MCP propio para auditoría automatizada de accesibilidad.

### EY (Ernst & Young) - Desarrollador Senior Frontend / Full Stack

*09/2021 - 05/2025 | Híbrido (Buenos Aires / equipos US e India)*

- Lideré un equipo de 3 ingenieros en una plataforma de inteligencia financiera con IA en Next.js (renderizado en servidor) y TypeScript, desde la arquitectura hasta producción.
- Audité, remedié y documenté **más de 50 componentes React** de la librería EY Motif (componentes accesibles: teclado, lectores de pantalla (NVDA, JAWS), foco y contraste), bajo WCAG 2.2 AA.
- Revisé componentes en Storybook **antes** de implementarlos y escribí los requisitos técnicos de accesibilidad y los patrones WAI-ARIA que el equipo aplicaba en cada historia de UI, con pruebas en Jest, React Testing Library, Vitest y Playwright.
- Sostuve flujos de datos complejos con Redux y React Query y pipelines de CI/CD con entregas diarias en Azure DevOps, en equipos distribuidos entre Estados Unidos e India con varias fases del ciclo de vida en paralelo.

### Super7UI - Especialista en Accesibilidad (contratista)

*08/2020 - 05/2021 | Remoto*

- Lideré la auditoría de accesibilidad de **Warner Bros. Screeners**, la plataforma privada de streaming corporativo: validé y amplié una auditoría de terceros probando cada caso en NVDA, VoiceOver y TalkBack.
- Resolví **más de 200 incidencias WCAG** y documenté la solución de cada una: guía de implementación, especificación y remediación lista para desarrollo.
- Establecí un pipeline de validación continua con **axe-core + Playwright en CI/CD** para frenar el código con regresiones antes del merge.

### Minutentag - Desarrollador Frontend

*02/2016 - 11/2019 | Presencial (Buenos Aires)*

- Participé de la migración a React y la optimización de e-commerce de alto tráfico (**más de 2 millones de usuarios mensuales**) para marcas internacionales de retail: Ann Taylor, LOFT y Lou & Grey.
- Implementé experimentos **A/B en producción con Adobe Target** sobre funcionalidades y diseños contra segmentos reales, en squads ágiles junto a producto y diseño, con las variantes escritas en JavaScript nativo.
- Me ocupé de la accesibilidad de los flujos desde el inicio y me convertí en la referencia del equipo en la materia.

## Contribuciones open source

**11 pull requests mergeados** en librerías de componentes y sistemas de diseño usados en producción, cada uno revisado y aprobado por sus mantenedores.

- **Componentes React y semántica accesible:** `adobe/react-spectrum` #10503 (el anuncio de región viva del ComboBox pisaba el anuncio nativo por ítem de VoiceOver) y #10554 (test de regresión para `aria-posinset`); `facebook/astryx` #5493 (TreeList no podía nombrarse: reenvío de `aria-label`/`aria-labelledby` al `role=tree`) y #5419 (HoverCard con label se exponía como diálogo: `aria-haspopup`, `aria-controls` y `aria-expanded` sincronizados); `mui/base-ui` #5551 (`aria-orientation` movido a los roles que lo soportan); `mui/material-ui` #49003 (links del carrusel en slides ocultos fuera del orden de foco, WCAG 4.1.2).
- **Sistemas de diseño enterprise:** `carbon-design-system/carbon` #22887 (soporte explícito de `aria-describedby` en `ComposedModal`, por la ruta `<dialog>` nativa y por `div[role=dialog]`) y `carbon-design-system/ibm-products` #9878 y #9879 (correcciones en `CreateFullPage` y en el Datagrid).
- **CI de librerías:** `facebook/astryx` #4914 (`build-storybook` fallaba con "no merge base" en PRs viejos por el fetch depth) y #4605 (indicador no cromático en el breadcrumb actual, WCAG 1.4.1).

**Revisión y diagnóstico técnico** (sin autoría de PR): separé los tres escenarios de falla que estaban conflados en `vercel/next.js` #73474, y el mantenedor lo aceptó al cerrar; fui el primer revisor humano del PR de Tearsheet en `ibm-products` #9869 y diagnostiqué un cluster de errores de React 19 a nivel de hook en #9865; resolví y documenté `carbon` #16031; comparé dos PRs en competencia sobre retención de foco en `astryx` #4871; y revisé expectativas de test y alcance en `react-spectrum` #10220 y #9556.

## Stack técnico

- **Frontend:** React, Next.js (SSR), TypeScript, JavaScript (ES6+), HTML5, CSS3, Vite, Tailwind CSS, Storybook, Redux, React Query, design systems y tokens, WAI-ARIA.
- **Backend y datos:** Node.js, PostgreSQL (Supabase, RLS multi-empresa, Realtime, pgvector), Edge Functions, APIs REST e integración con APIs de terceros, webhooks, Stripe, autenticación y roles.
- **IA y automatización:** RAG con embeddings, guardrails de confianza, orquestación de agentes y memoria persistente, Model Context Protocol (MCP), Claude Code y Codex como herramientas de desarrollo.
- **Testing y DevOps:** Vitest, Playwright, Jest, React Testing Library, axe-core, Biome, Git, GitHub Actions, Azure DevOps (pipelines, tickets y user stories), Docker.
- **Accesibilidad:** WCAG 2.2 AA, WAI-ARIA (roles, estados y propiedades), NVDA, JAWS, VoiceOver, TalkBack, Axe DevTools, Lighthouse.

## Formación y certificaciones

- **Deque University** - Accessibility Specialist Program (2021)
- **Digital House** - Programa intensivo de Desarrollo Web / React (2018)
- Formación continua en accesibilidad digital y calidad de software (Platzi y otros cursos a lo largo de la carrera).

## Idiomas

- **Español:** nativo
- **Inglés:** B2+ intermedio alto, cursando el B2+ intensivo en el CUI (UBA); lectura y documentación técnica fluidas.

## Por qué EFISAT

Lo que me interesa de un sistema como el de EFISAT es que el software toca la operación real: una unidad que no reporta, un conductor que no recibe el mensaje, un recaudo que no cierra. Vengo de construir software con esa característica, donde un error se ve en el mismo día, y de unificar fuentes de datos dispersas en una sola plataforma sin perder el control humano. Eso es lo que hice con integraciones, paneles de gestión y automatización con reglas auditables, y es lo que me gustaría hacer acá.
