# NORTH.md - El norte de Kanam

**Fecha:** 2026-09-14
**Estado:** Vivo. Este documento fija el "para qué" de largo plazo, que hasta hoy vivía solo en conversaciones.
**Autor:** Kanam, a pedido de Gonzo. Contenido revisado contra los BRIEF/ROADMAP/ADRs reales de cada proyecto.

---

## Por qué existe este documento

`docs/ROADMAP.md` define **cómo trabajamos** (4 capas: fundaciones, pipeline, portfolio, crecimiento).
`projects/portfolio-strategy/ADR-001` define **cómo te vendés** (3 pilares + 3 proyectos ancla).

Ninguno define **qué queremos que exista**. Ese es el gap que este archivo cierra.

Sin un norte escrito, cada bifurcación se siente igual de válida y ninguna se puede priorizar contra las demás. El 2026-09-14 la sesión tocó OSS, CV tailoring, kanam-lab y diseño en un mismo día: cuatro frentes, todos defendibles, ninguno comparable. Eso no es falta de disciplina - es el síntoma exacto de un norte no escrito.

---

## Qué es Kanam (la respuesta corta)

**Kanam es un sistema operativo personal de trabajo con IA, y su constelación de productos.**

No es "el bot". No es "el workspace". Es las tres cosas a la vez:

| Capa | Qué es | Nombre | Estado |
|---|---|---|---|
| **1. El sistema** | El OS de trabajo: agente, pipeline A/B, memoria DB-first, skills, decisiones documentadas | `workspace_openclaw` + Kanam | En producción diaria |
| **2. La constelación** | Los productos que salen de ese sistema | 9 proyectos `kanam-*` + a11y | Mixto: 3 anclas, 3 de infraestructura interna, 3 en la línea narrativa, 2 experimentos |
| **3. El hilo** | La especialización que atraviesa todo | Accesibilidad (a11y) | Diferenciador real, con evidencia OSS |

El nombre no es azar: **Kanam** viene del "segundo cerebro" original que descartaste en 2026 y que resucitó como `kanam-mind`. El nombre sobrevivió a su primer proyecto y hoy nombra al ecosistema entero. Eso no es un detalle: significa que la idea de fondo era más grande que cualquiera de sus implementaciones.

---

## El norte, en tres horizontes

### Horizonte 0 - Sostener y capitalizar (ahora, 0-6 meses)
**Para qué:** conseguir trabajo. Situación económica urgente.

Kanam cumple acá dos funciones concretas:
1. **Portfolio vivo:** los PRs mergeados en design systems OSS + los proyectos ancla son la prueba, no el relato.
2. **Diferenciador:** a11y + AI-native es una combinación rara. El CV tailoring de hoy (95% de match) es este horizonte en acción.

**Criterio de listo:** un proceso llega a oferta. Punto.

### Horizonte 1 - Kanam como sistema que se sostiene (6-24 meses)
**Para qué:** que el sistema deje de depender de tu atención constante y empiece a devolverte tiempo.

La clave no es agregar productos nuevos: es que **1 o 2 piezas funcionen solas y con usuarios reales**. Los candidatos ya están definidos por ADR-001:

- **`a11y-fixer`** - el puente entre tu especialización y OSS. Un bot de auditoría a11y que cualquiera puede instalar.
- **`kanam-pulse`** - open source, community-first, local-first. El ancla del pilar de privacidad.

**Criterio de listo:** una pieza con usuarios reales que no seas vos, con issues y PRs de terceros. Eso es la validación de que Kanam dejó de ser solo para vos.

### Horizonte 2 - Kanam como plataforma (2-5 años)
**Para qué:** que la infraestructura de trabajo con IA que construiste para vos mismo sirva para otros.

Acá vive la apuesta más grande, y ya está nombrada en el BRIEF de `kanam-forge`:

> "Sueño final: Lovable cloud + AI multi-tenant, self-hosted, donde en vez del agente genérico corre el pipeline de Gonzo (stack opinado, memoria persistente, a11y integrada, multi-agente con review cruzado)."

Ese es el techo real de Kanam: **el pipeline que te hace productivo, empaquetado para que otros construyan con él**. No un generador de landings - una infraestructura.

**Criterio de listo:** alguien que no sos vos construye algo real con Kanam, y le sale mejor que sin Kanam.

---

## La constelación (qué hace cada pieza)

Verificado contra el estado real de cada repo el 2026-09-14.

### El sistema (la base que sostiene todo)
- **`workspace_openclaw`** - el OS de trabajo. Memoria DB-first, pipeline A/B, skills, AGENTS/SOUL/IDENTITY. Es lo que hace posible el resto.

### Las anclas del portfolio (ADR-001)
- **`kanam-forge`** - Lovable self-hosted con tu pipeline. *Infraestructura AI.* Fase 0, MVP local con Docker.
- **`a11y-fixer`** - Bot de auditoría a11y para PRs de GitHub (axe-core + Playwright). *Especialización a11y.* v0.6.0 reescrito.
- **`kanam-pulse`** - Monitor y cleaner de macOS local-first, web-first, a11y de fábrica, IA local. *Local-First / Privacidad.* En desarrollo.

### La línea narrativa (el "segundo cerebro" que evolucionó)
- **`kanam-mind`** - El segundo cerebro original. Timeline + resumen IA, IndexedDB puro. Archivado del portfolio, repo conservado.
- **`kanam-story`** - Co-writer de ficción local-first donde **el chat ES el producto** y el agente tiene manos. v0.11.0, Fases 1-4 completas.
- **`kanam-studio`** - Taller de construcción de mundos y planificación narrativa. La **versión superada** de kanam-story: grafo de nodos en vez de manuscrito lineal. v0.6.0, slices 1-4 completos.

> Nota: `kanam-story` y `kanam-studio` nacieron como proyectos separados y hoy se pisan parcialmente. **DECISION (Gonzo, 2026-09-14): son UNO.** kanam-studio se documentó como "la versión superada" de kanam-story (grafo de nodos + world-building con IA sobre el manuscrito lineal). La consolidación está pendiente de plan: qué dirección toma (studio absorbe story, o un nombre nuevo), qué pasa con el recorrido ya hecho (story v0.11.0 Fases 1-4 vs studio v0.6.0 slices 1-4) y qué repo queda.

### La infraestructura interna
- **`kanam-insight`** - Motor de inteligencia transversal: cruza los `.knowledge/` de todos los proyectos, detecta patrones y deuda técnica. Es Kanam mirándose a sí misma.
- **`kanam-lab`** - Playground local de IA (Gradio + Python): chat comparativo, STT, RAG sobre la memoria. Es **donde Kanam aprende sobre sí misma** - el RAG de la Fase 3 lee tu propia memoria.
- **`kanam-skills`** - Repo público de skills. Sanitizado, es la cara pública del sistema.

### Los experimentos (valor de aprendizaje, no de producto)
- **`kanam-solitaires`** - Colección de solitarios PWA. Prueba de producto consumer pulido.
- **`kanam-tetris`** - Tetris single-file como banco de pruebas del pipeline de agentes. v0.3.0. Su valor es **validar el pipeline**, no el juego.

---

## El potencial (qué pasa si funciona)

Hoy el sistema es **para uno**. El potencial es que deje de serlo en tres direcciones:

1. **Comercial** - `kanam-forge` como infraestructura: cobrar por el pipeline, no por las apps.
2. **Comunidad** - `kanam-pulse` y `a11y-fixer` como open source con usuarios reales. Construyen reputación técnica sin intermediarios.
3. **Personal** - Kanam como el sistema que te devuelve foco. Es el horizonte que más importa y el menos documentado: si el sistema cuesta más atención de la que devuelve, no está funcionando.

**La tesis de fondo, tomada de ADR-001:** la IA como infraestructura, no como chat. Kanam no usa IA - construye los sistemas que hacen posible usarla bien.

---

## Cómo decidir (el criterio que faltaba)

Cuando aparezca un frente nuevo (una idea, un proyecto, una bifurcación a mitad de sesión), pasa por estas tres preguntas **en orden**:

1. **¿A qué horizonte sirve?** Si no sirve al Horizonte 0 (trabajo) y tampoco empuja una ancla hacia el Horizonte 1, es una distracción - aunque sea interesante.
2. **¿Es nueva capacidad o es dispersión?** Sumar una pieza a un proyecto ancla = capacidad. Abrir un proyecto número 11 = dispersión. El ROADMAP ya lo dice: *"sin esto, el pipeline optimiza lo equivocado"*.
3. **¿La puedo sostener?** Una persona, búsqueda laboral activa, situación económica urgente. Si no hay energía para mantenerla viva, no se abre.

**La regla del norte:** si una bifurcación no pasa las tres, se anota en `memory/inbox.md` y se sigue con lo que estaba. No se descarta - se posterga con registro.

<details><summary>Nota honesta sobre la dispersión</summary>

El conteo real: 9 proyectos `kanam-*`, 11 activos en el catálogo, una persona. El propio ROADMAP marca "Estrategia de proyectos" como P0 justamente por esto.

No es un problema de capacidad - es que hoy no hay un documento que diga *cuál de todas las piezas importa más*. Este NORTH.md intenta responderlo, pero la respuesta corta es incómoda: **en el Horizonte 0, el proyecto más importante no es ninguno de la constelación - es conseguir trabajo.** Los proyectos son el medio, no el fin.

Eso está bien. Pero conviene tenerlo escrito para no confundir actividad con progreso.

</details>

---

## Decisiones abiertas (que este documento NO cierra)

1. **kanam-story + kanam-studio (DECIDIDO: son uno):** falta el plan de consolidación - dirección del merge, qué repo queda, y cómo se preserva el recorrido de cada uno (story v0.11.0 vs studio v0.6.0).
2. **`accessible-ui`:** archivado en ADR-001 pero con trabajo real hecho (3 componentes APG, 3 capas de test, Storybook con a11y addon, nunca publicado a npm). Plan de resurrección propuesto 2026-09-14.
3. **`kanam-skills` público:** sigue vivo pero desactualizado (54/59 skills divergen del local, último push 2026-08-12) y con referencias personales a sanitizar. Regla: contenido **genérico**, sin mención a nuestro trabajo ni identidades - debe servir como plantilla para cualquier proyecto.
4. **La métrica del Horizonte 1:** "usuarios reales" es vago. Falta el número concreto (¿10 descargas? ¿1 issue externo?).

---

## Notas de creación

- Creado 2026-09-14, en la sesión donde Gonzo preguntó "¿cuál era el objetivo, el para qué de este proyecto?".
- Fuentes: `docs/ROADMAP.md`, ADRs del workspace, `projects/portfolio-strategy/ADR-001`, BRIEFs y ROADMAPs de cada `kanam-*`, `IDENTITY.md`.
- Principio: no inventar. Todo lo que este documento afirma sobre un proyecto sale de su BRIEF/ROADMAP real. Las aspiraciones están marcadas como tales (Horizontes 1 y 2).
