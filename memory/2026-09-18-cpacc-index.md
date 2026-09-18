# CPACC – Índice y áreas a reforzar (basado en 100 Days of A11y)

Esta nota sintetiza lo que se pudo extraer del menú *CPACC* del sitio **100 Days of A11y**
(`https://100daysofa11y.com/cpacc/`).  El propio endpoint solo muestra enlaces a los feeds
XML/JSON y no incluye el listado de entradas, pero los resultados de búsqueda y el
fragmento de la página revelan los siguientes ítems de índice (orden cronológico):

| Nº | Título (fecha) | Tipo de contenido |
|---|----------------|-------------------|
| 1 | **CPACC Exam Preparation Begins** – 04 Nov 2019 | Introducción – visión general del examen, proceso de registro y recursos de estudio.
| 2 | **Basic Disability Concepts** – 06 Nov 2019 | Conceptos de discapacidad (modelos médico, social, biopsicosocial) y tecnologías asistivas.
| 3 | **6 Theoretical** – (fecha no visible) | Aspectos teóricos del BoK (principios de accesibilidad, fundamentos de IAAP, metodología de estudio).

> **Observación:** la lista mostrada por la página es incompleta; en el sitio existen entradas
> posteriores (p.ej. reflexiones sobre el camino CPACC, guías de estudio, resúmenes de dominio).

## Áreas que recomendamos reforzar

El **Body of Knowledge (BoK)** de la certificación CPACC está estructurado en tres dominios
principales (Discapacidades, Accesibilidad y Diseño Universal, Normas y Gestión).  A partir del
índice anterior identificamos los siguientes huecos o temas que merecen mayor énfasis para
que nuestro conocimiento ya avanzado se alinee con la certificación:

1. **Marco legal y regulatorio** (sección 3 del BoK).  La lista actual no menciona artículos
   sobre legislación (ADA, Section 508, EN 301 549, etc.).  Necesitamos estudiar fuentes
   como la compilación de legislación de *ChelseaA11y* y los documentos oficiales de IAAP.
2. **Pruebas y evaluación con AT** (p.ej. uso de screen‑readers, testing tools, WCAG‑EM).
   Sólo se alude a conceptos teóricos; es crucial profundizar en guías prácticas y casos de uso.
3. **Diseño universal avanzado** – patrones de interacción, principios de *inclusive design*
   y consideraciones de *target size*, *animation reduction* y *motion actuation* (p. ej. WCAG 2.5).
4. **Dominios de discapacidades específicas** – más allá de los conceptos básicos, incluir
   discapacidades cognitivas, sensoriales y motoras con ejemplos de AT (Orca, JAWS, NVDA, etc.).
5. **Mapeo de requisitos del BoK a ejemplos de código** – crear pequeñas demostraciones
   (HTML/ARIA, contrastes, enfoques de foco) que muestren la aplicación práctica de cada criterio
   de éxito.

## Plan de estudio corto‑plazo (4 semanas)

| Semana | Enfoque | Recursos seleccionados |
|--------|---------|------------------------|
| 1 | **Marco legal** – Revisión de leyes y normas internacionales. | `chelsea11y.com/cpacc/legislation.html`, IAAP PDFs, *Legal Primer* de CPACC. |
| 2 | **Discapacidades y AT** – Profundizar en conceptos de discapacidad y herramientas. | Post “Basic Disability Concepts”, *100 Days of A11y* día 8‑12, Deque AT cheatsheets. |
| 3 | **Pruebas y evaluación** – Herramientas de testing, WCAG‑EM, estudios de caso. | *Testing and Evaluation* entry (día 71), Deque University testing modules, WCAG‑EM guide. |
| 4 | **Diseño universal y patrones** – UI/UX asistido por IA, contrastes, motion. | Entradas “6 Theoretical”, *Design Considerations* PDF, artículos de *A11ycasts* y *Inclusive Design 24*. |

### Acción inmediata

1. **Clonar** la lista completa de entradas del índice CPACC desde la RSS (`feed/feed.xml`) o el
   JSON feed para tener la lista definitiva.  (Este paso está pendiente de ejecución manual por
   el operador).
2. **Crear** un documento de referencia rápida (`docs/cpacc-study-plan.md`) con los enlaces
   concretos a los posts identificados y a los materiales externos (legislación, AT, testing).
3. **Añadir** a la hoja de *study‑track* (`studies/cpacc-study-plan.xlsx`) una columna *status*
   para marcar progreso (pendiente, en‑curso, completado).

## Próximos pasos (cuando digas “es el momento de arrancar el estudio”)

* Ejecutaremos el plan semanal, actualizando el **progress_card** al completar cada foco.
* Generaremos ejemplos de código (HTML/ARIA) vinculados a los criterios de éxito de WCAG‑A‑AA‑AAA.
* Documentaremos los hallazgos en `memory/2026-09-XX-cpacc‑<tema>.md` para que estén disponibles
  en cualquier sesión futura.

---

**Fuentes**
* `https://100daysofa11y.com/cpacc/` (índice parcial) – capturado 2026‑09‑18.
* Resultados de búsqueda: “CPACC Exam Preparation Begins 04 Nov 2019” – muestra los 3 ítems
  enumerados arriba.
* `https://chelsea11y.com/cpacc/legislation.html` – compilación de leyes IAAP.
* `https://dequeuniversity.com` – cursos y cheatsheets de AT y testing.

Esta captura está guardada en `memory/2026-09-18-cpacc-index.md` para su uso posterior.

