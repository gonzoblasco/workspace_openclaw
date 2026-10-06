# NORTH.md - El norte de Kanam

**Fecha:** 2026-10-06 (reconstruido desde cero)
**Estado:** Vivo. Fija el "para qué" de largo plazo.
**Autor:** Kanam, a pedido de Gonzo. Reescrito contra fuentes reales (git, ADRs, BRIEF de cada proyecto en `~/projects/`, `docs/APUESTAS.md`, `docs/entrevistas/job-search-tracker.md`) - no contra la memoria de una sesión.

> **Nota de la reconstrucción (2026-10-06):** la versión anterior era del 2026-09-14 y arrastraba errores graves: hablaba de la constelación como si los proyectos vivieran en `projects/*` (hoy viven en `~/projects/`, ADR-075), y su Horizonte 0 estaba armado sobre una "oferta aceptada" de EIT/Disney que **nunca existió** (era un bench req; ver `job-search-tracker.md`). Este documento reemplaza aquel. El histórico queda en git.

---

## Por qué existe este documento

Tres documentos distintos responden tres preguntas distintas:

| Documento | Pregunta |
|---|---|
| `docs/ROADMAP.md` | **¿Cómo trabajamos?** (capas: fundaciones, pipeline, portfolio, ecosistema, crecimiento) |
| `~/projects/portfolio-strategy/ADR-001` + `docs/APUESTAS.md` | **¿Cómo te vendés y qué construimos?** (pilares, anclas, orden de apuestas) |
| `docs/NORTH.md` (este) | **¿Qué queremos que exista?** |

Sin un norte escrito, cada bifurcación se siente igual de válida y ninguna se puede priorizar contra las demás. Ese sigue siendo el problema que este archivo cierra.

---

## Qué es Kanam (la respuesta corta)

**Kanam es un sistema operativo personal de trabajo con IA, y su constelación de productos.**

No es "el bot" ni "el workspace". Es tres cosas a la vez:

| Capa | Qué es | Nombre | Estado |
|---|---|---|---|
| **1. El sistema** | El OS de trabajo: agente multi-rol, pipeline A/B, memoria DB-first, skills, decisiones documentadas | `workspace_openclaw` + Kanam | En producción diaria en la Mac Mini |
| **2. La constelación** | Los productos/proyectos que salen de ese sistema | ~11 repos propios + `~/projects` de trabajo | Mixto: 2-3 piezas con foco, el resto en pausa o experimento |
| **3. El hilo** | La especialización que atraviesa todo | Accesibilidad (a11y) + IA como infraestructura | Diferenciador real, con evidencia OSS (18 PRs abiertos, 8 mergeados) |

El nombre no es azar: **Kanam** viene del "segundo cerebro" original que Gonzo descartó en 2026 y que resucitó como `kanam-mind`. El nombre sobrevivió a su primer proyecto y hoy nombra al ecosistema entero.

---

## El norte, en tres horizontes

### Horizonte 0 - Sostener y capitalizar (ahora, 0-6 meses)
**Para qué:** conseguir trabajo. Situación económica urgente.

> **Corrección (2026-10-06):** al 2026-09-24 **no hay ningún proceso abierto**; el tablero de búsqueda está vacío. La versión anterior de este documento y del ROADMAP afirmaban una oferta aceptada que nunca existió. El Horizonte 0 no está "cumplido": está **en rojo**.

Kanam cumple acá dos funciones concretas:
1. **Portfolio vivo:** los PRs mergeados en design systems OSS (a11y/agentic) + los proyectos con foco son la prueba, no el relato.
2. **Diferenciador:** a11y + AI-native es una combinación rara y defendible.

**Palanca viva:** la certificación **CPACC** (antes del 30/11) como entregable que desbloquea el hilo con reclutadores.
**Criterio de listo:** un proceso **nuevo** llega a oferta y onboarding.

### Horizonte 1 - Kanam como sistema que se sostiene (6-24 meses)
**Para qué:** que el sistema deje de depender de la atención constante de Gonzo y empiece a devolverle tiempo.

La clave no es agregar productos: es que **1 o 2 piezas funcionen solas y con usuarios reales**. Los candidatos están definidos por `docs/APUESTAS.md` (orden confirmado por Gonzo el 2026-09-24):

- **`kanam-insight`** (prioridad 1) - motor de inteligencia transversal: cruza los `.knowledge/` de todos los proyectos, detecta patrones y deuda. Riesgo cero, valor inmediato: mejora nuestro propio trabajo.
- **`kanam-fixer`** (prioridad 3) - el puente entre la especialización a11y y OSS. **Su alcance está SIN DEFINIR** - no se puede afirmar todavía que sea el engine de fixes de `a11y-fixer` (archivado). El diferenciador técnico es real: mira **lo que el lector de pantalla efectivamente anuncia**, no solo el DOM.
- **`soporteml-v4`** (prioridad 2, producto privado) - CRM/contable SaaS para pymes. La apuesta comercial más sólida por un motivo frío: el MVP ya incluye bandeja, KB y autopilot.

**Criterio de listo:** una pieza con usuarios reales que no seas vos, con issues y PRs de terceros.

### Horizonte 2 - Kanam como plataforma (2-5 años)
**Para qué:** que la infraestructura de trabajo con IA construida para uno mismo sirva para otros.

La apuesta más grande, ya nombrada en el BRIEF de `kanam-forge`:

> "Sueño final: Lovable cloud + AI multi-tenant, self-hosted, donde en vez del agente genérico corre el pipeline de Gonzo (stack opinado, memoria persistente, a11y integrada, multi-agente con review cruzado)."

El techo real de Kanam: **el pipeline que te hace productivo, empaquetado para que otros construyan con él**. No un generador de landings - una infraestructura.

**Criterio de listo:** alguien que no sos vos construye algo real con Kanam, y le sale mejor que sin Kanam.

---

## La constelación (qué hace cada pieza)

Los proyectos **ya no viven en el workspace**: viven en `~/projects/<slug>/` (ADR-075); el `.knowledge/` de cada uno viaja con el proyecto. Verificado 2026-10-06 contra el filesystem.

### El sistema (la base que sostiene todo)
- **`workspace_openclaw`** - el OS de trabajo. Memoria DB-first, pipeline A/B, multi-agente (ADR-073/074), skills, AGENTS/SOUL/IDENTITY. Es lo que hace posible el resto.

### Foco actual (las apuestas)
- **`kanam-insight`** - inteligencia transversal sobre los `.knowledge/`. *Uso interno.* Apuesta 1.
- **`kanam-fixer`** - puente a11y -> OSS. *Producto.* Apuesta 3. Alcance a definir.
- **`soporteml`** - CRM/contable para pymes (v4 en curso). *Producto privado* (ADR-068). Apuesta 2.
- **`kanam-pulse`** - monitor de salud de macOS, local-first, a11y de fábrica. Público. M1 en curso (migración JS->TS del core).
- **`kanam-onwheels`** - sitio de concesionario multi-marca con chatbot RAG con evidencia citada. Regalo para el local de Esteban, sin billing. Fase 1 en curso; Supabase conectado, 14/14 checks de invariantes.

### Infraestructura interna
- **`kanam-os`** - app local sobre la memoria (RAG + NL a SQL).
- **`kanam-lab`** - playground local de IA; donde Kanam aprende sobre sí misma.
- **`ollama-visor`** - observabilidad del stack de modelos local.
- **`kanam-spec` / `kanam-spec-v2`** - infraestructura de especificaciones (SDD).
- **kanam-skills** - repo público de skills (regla de sanitización obligatoria; ADR-079 cambió su rol).

### La línea narrativa (el "segundo cerebro" que evolucionó)
- **`kanam-mind`** - el segundo cerebro original (timeline + resumen IA, IndexedDB). Archivado del portfolio, repo conservado.
- **`kanam-story` / `kanam-writer` / `kanam-story-bible`** - co-writer de ficción local-first.
- **`kanam-worldbuilding`** - taller de construcción de mundos y planificación narrativa.

> **DECISIÓN (Gonzo, 2026-09-14): `kanam-story` y `kanam-studio` son UNO.** El segundo se documentó como "la versión superada" del primero (grafo de nodos vs manuscrito lineal). La consolidación sigue pendiente de plan. Hoy el trabajo narrativo aparece repartido en `kanam-writer`, `kanam-story-bible` y `kanam-worldbuilding`.

### Los experimentos (valor de aprendizaje, no de producto)
- **`kanam-tetris`** - banco de pruebas del pipeline de agentes.

### Archivados / pausa
- **`a11y-fixer`** (archivado 2026-09-14 en GitHub; sucesor `kanam-fixer`), **`create-with-ai`** (fusionado a `kanam-forge`), y otros en `MEMORY.md`.

---

## El potencial (qué pasa si funciona)

Hoy el sistema es **para uno**. El potencial es que deje de serlo en tres direcciones:

1. **Comercial** - `kanam-forge` / `soporteml-v4` como infraestructura/producto: cobrar por la capacidad, no por las apps.
2. **Comunidad** - `kanam-pulse` (y `kanam-fixer` cuando su alcance se defina) como open source con usuarios reales.
3. **Personal** - Kanam como el sistema que devuelve foco. El horizonte que más importa y el menos documentado: si el sistema cuesta más atención de la que devuelve, no está funcionando (ver el hallazgo del bootstrap truncado en el ROADMAP).

**La tesis de fondo, tomada de ADR-001:** la IA como infraestructura, no como chat. Kanam no usa IA - construye los sistemas que hacen posible usarla bien.

---

## Cómo decidir (el criterio que faltaba)

Cuando aparezca un frente nuevo, pasa por estas tres preguntas **en orden**:

1. **¿A qué horizonte sirve?** Si no sirve al Horizonte 0 (trabajo) y tampoco empuja una ancla hacia el Horizonte 1, es una distracción - aunque sea interesante.
2. **¿Es nueva capacidad o es dispersión?** Sumar una pieza a un proyecto ancla = capacidad. Abrir un proyecto número 12 = dispersión.
3. **¿La puedo sostener?** Una persona, búsqueda laboral activa, situación económica urgente, una sola máquina. Si no hay energía para mantenerla viva, no se abre.

**La regla del norte:** si una bifurcación no pasa las tres, se anota en `memory/inbox.md` y se sigue con lo que estaba. No se descarta - se posterga con registro.

<details><summary>Nota honesta sobre la dispersión</summary>

El conteo real: ~11 repos propios, ~17 directorios de trabajo en `~/projects`, una persona. `docs/APUESTAS.md` y el ROADMAP marcan "Estrategia de proyectos" como P0 justamente por esto.

No es un problema de capacidad - es que el orden de lo que importa vive repartido entre documentos que se pisan. No hay un lugar único que diga *cuál de todas las piezas importa más*. Este NORTH.md intenta responderlo, y la respuesta corta es incómoda: **en el Horizonte 0, el proyecto más importante no es ninguno de la constelación - es conseguir trabajo.** Los proyectos son el medio, no el fin.

Eso está bien. Pero conviene tenerlo escrito para no confundir actividad con progreso.

</details>

---

## Decisiones abiertas (que este documento NO cierra)

1. **`kanam-story` + `kanam-studio` (DECIDIDO: son uno):** falta el plan de consolidación - dirección del merge, qué repo queda, y cómo se preserva el recorrido de cada uno. Hoy el trabajo narrativo está repartido en `kanam-writer`, `kanam-story-bible`, `kanam-worldbuilding`.
2. **`kanam-fixer`:** alcance sin definir. Es lo que desbloquea el ancla formal del pilar *Accesibilidad*.
3. **`kanam-skills` público:** desactualizado y con referencias personales a sanitizar. Regla: contenido **genérico**, sin mención al trabajo propio ni identidades.
4. **La métrica del Horizonte 1:** "usuarios reales" es vago. Falta el número concreto (¿10 descargas? ¿1 issue externo?).
5. **Respaldo de `~/projects`:** 135 archivos `.knowledge/` viven solo en disco, sin respaldo en git (decisión diferida, 2026-09-27).

---

## Notas de creación

- Creado 2026-09-14, en la sesión donde Gonzo preguntó "¿cuál era el objetivo, el para qué de este proyecto?".
- **Reconstruido 2026-10-06** contra fuentes reales. Motivo: la versión del 09-14 describía una constelación en ubicaciones obsoletas y un Horizonte 0 cumplido que nunca se cumplió. Fuentes de esta reconstrucción: `docs/ROADMAP.md`, `docs/APUESTAS.md`, ADRs del workspace (001, 068, 073-075, 079, 090), `~/projects/*/.knowledge/`, `docs/entrevistas/job-search-tracker.md`, `memory/memory.db`.
- Principio: no inventar. Lo que este documento afirma sobre un proyecto sale de su BRIEF/ROADMAP real o del filesystem. Las aspiraciones están marcadas como tales (Horizontes 1 y 2).
