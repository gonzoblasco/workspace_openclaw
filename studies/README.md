# Estudios

Este directorio agrupa los análisis y estudios técnicos del workspace.

## Contenido

| Sub-directorio | Qué es | Índice |
|---|---|---|
| `narrative-engineering/` | Análisis de estructuras narrativas con el **modelo de 4 ejes** (Premisa & Regla de Hierro, Gestión de Información, World-building Funcional, Arco de Identidad). | [`narrative-engineering/`](narrative-engineering/) |
| `openclaw-use-cases/` | Registro de las lecciones del curso **OpenClaw Use Cases** (roadmap.sh), con verificación contra la instalación real. | [`openclaw-use-cases/`](openclaw-use-cases/) |
| `oss-alternatives-triage.md` | Triaje de alternativas open source: qué se adapta, qué se adopta y qué se descarta, con licencias verificadas. | - (archivo suelto) |
| `entrevistas-tecnicas/` | Clase de estudio derivada de la charla «Preparándote para entrevistas técnicas sin morir en el intento» (Nerdearla Chile 2026, Tatiana Rodríguez): transcript ASR, outline v2 y auditoría de la re-evaluación 2026-11-09. | [`entrevistas-tecnicas/`](entrevistas-tecnicas/) |
| `software-to-ai-engineer/` | Clase de estudio derivada del video «De Software Engineer a AI Engineer: El Roadmap Más Realista» (Fazt): transcript ASR, outline de 14 módulos alineado a los capítulos oficiales y auditoría de la re-evaluación 2026-11-09. | [`software-to-ai-engineer/`](software-to-ai-engineer/) |
| `cpacc-study-guide/` | Clase de estudio derivada de **FULL CPACC Study Guide** (Derek Mei, 1:35:11, captions manuales): 15 capítulos oficiales, outline de 9 módulos con el contenido real de los tres dominios (7 modelos, 8 categorías de discapacidad, UDL, POUR, marco legal y madurez organizacional) y 19 citas verificadas. **Es el material de estudio**; el video de Practice Test Geeks queda como roadmap. | [`cpacc-study-guide/`](cpacc-study-guide/) |
| `cpacc-certification/` | Clase de estudio derivada del video **CPACC Test Preparation 2026** (Practice Test Geeks, 07:39). **Uso: roadmap, no fuente** (criterio de Gonzo, 2026-11-11): outline de 8 módulos 1:1 con los capítulos oficiales, 17 citas verificadas, y cada cifra contrastada contra el BoK y el Handbook de IAAP - lo que el video sostiene, lo que matiza y lo que no tiene fuente. El material de estudio es el BoK; el plan vigente, `docs/cpacc/study-plan.md`. | [`cpacc-certification/`](cpacc-certification/) |
| `agentic-coding-codex/` | Clase de estudio derivada del curso «Codex & AI Coding Agents — Learn Agentic Coding» (Scrimba, Tom Chant, 1:50:43): transcript ASR con glosario y outline de 13 módulos alineado a los 27 capítulos oficiales, con ejercicios y banco de preguntas. | [`agentic-coding-codex/`](agentic-coding-codex/) |
| `n8n-ai-automations/` | Clase de estudio derivada del curso «n8n Full Course – Architect Scalable AI Automations from Scratch» (freeCodeCamp.org, Rahul Joshi, 43:05): transcript ASR con glosario y outline de 14 módulos 1:1 con los capítulos oficiales, más ejercicios y banco de preguntas. | [`n8n-ai-automations/`](n8n-ai-automations/) |
| `ai-agents-for-beginners/` | Clase de estudio derivada del curso «AI Agents For Beginners – OpenClaw Case Study» (freeCodeCamp.org, KodeKloud, Mumshad Mannambeth, 3:05:58): transcript ASR con glosario y outline de 22 módulos 1:1 con los capítulos oficiales, más ejercicios y banco de preguntas. | [`ai-agents-for-beginners/`](ai-agents-for-beginners/) |
| `rag-mcp-fundamentals/` | Clase de estudio derivada del curso «RAG & MCP Fundamentals – A Hands-On Crash Course» (freeCodeCamp.org, 1:39:53): transcript ASR con glosario y outline de 38 módulos 1:1 con los 27 + 12 capítulos oficiales (Parte 1 RAG, Parte 2 MCP), con ejercicios por módulo y banco de 14 preguntas. | [`rag-mcp-fundamentals/`](rag-mcp-fundamentals/) |
| `ai-engineer-full-course/` | Clase de estudio derivada del curso «AI Engineer Full Course in 3 Hours» (Cloud X Berry, 2:53:54): transcript ASR con glosario y outline de 6 módulos / 33 capítulos 1:1 con los oficiales, con 41 citas verificadas, ejercicios por módulo y banco de 21 preguntas. | [`ai-engineer-full-course/`](ai-engineer-full-course/) |
| `cs50-ai-python/` | Clase de estudio derivada de «Harvard CS50's Artificial Intelligence with Python – Full University Course» (freeCodeCamp.org, Brian Yu, 11:51:22): transcript de 14.299 cues con glosario, outline de 7 módulos 1:1 con los capítulos oficiales y 79 citas verificadas, más `ADOPCION.md` con el gate de evaluación en held-out (`heldout.py`) corrido sobre las nueve clases del catálogo. | [`cs50-ai-python/`](cs50-ai-python/) |

| `sql-full-course/` | Clase de estudio derivada del curso **SQL Full Course for Beginners (30 Hours) – From Zero to Hero** (Data with Baraa, 29:48:27): transcript de subtítulos automáticos con 41 capítulos 1:1 con los oficiales, outline de 22 módulos en tres niveles (Beginner/Intermediate/Advanced) + tres proyectos, citas verificadas y banco de 18 preguntas. | [`sql-full-course/`](sql-full-course/) |
| `miniseries-con-ia-google-flow/` | Clase de estudio derivada del tutorial «Crea tu Propia Miniserie con IA 100% GRATIS (Paso a Paso)» (Edwin Arenas, 25:37): transcript ASR con glosario y outline de 8 módulos derivado del transcript (sin índice oficial en la descripción), con citas verificadas, ejercicios por bloque y banco de 8 preguntas. | [`miniseries-con-ia-google-flow/`](miniseries-con-ia-google-flow/) |
## Método

Un estudio acá es **verificación contra la fuente**, no resumen de secondhand. Los datos mutables (stars, licencias, actividad de un repo) se confirman contra la API o el repo original antes de quedar escritos; las afirmaciones que no se pudieron confirmar no entran.

Cada estudio es un artefacto de análisis: no es spec, ni ADR, ni implementación. Es el insumo para decidir.

## Clase montada: CPACC — Certified Professional in Accessibility Core Competencies (Practice Test Geeks, 7:39)

- Gonzo pasó `https://www.youtube.com/watch?v=VScwzuegeUo` con "curso"; la clase está en `studies/cpacc-certification/` (`outline.md`, `transcripcion.md`).
- Fuente: video de **Practice Test Geeks** (2026-01-08, 07:39). Se usa como **roadmap**, no como fuente de verdad. Subtítulos automáticos de YouTube (222 cues), no ASR local.
- **Lo que sostiene** (verificado contra el BoK v4.0 y el Handbook 2026): los pesos 40/40/20 de los tres dominios, la validez de 3 años, los 45 créditos de renovación, la escala 200-800 con passing 600, los siete modelos de discapacidad, la estructura A-F de cada dominio.
- **Lo que no sostiene:** el salto salarial de $5.000-$15.000 sin fuente, el "70% más productivos / 80% más calidad" sin fuente, y el "56% de premium" que es real pero de **PwC, 2025 Global AI Jobs Barometer** sobre skills de IA, no del CPACC.
- **No es el estudio principal:** el plan vigente vive en [`docs/cpacc/study-plan.md`](../docs/cpacc/study-plan.md). Esta clase aporta el mapa del examen y la auditoría de claims, no el contenido de los dominios.
- **Se estudia, no se rinde (Gonzo, 2026-11-11):** no hay presupuesto para el fee, así que el objetivo es aprender el contenido, sin fecha de examen. Las fechas de sesión del plan quedaron como referencia, no como deadline.
