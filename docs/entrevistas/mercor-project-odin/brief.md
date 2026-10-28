<!-- project: github.com/gonzoblasco/workspace_openclaw -->

# Brief de redacción - CV para Mercor "Software Developers (Must own MacBook)"

> Brief del CORE para STUDIO. El corpus es la verdad; este archivo solo **selecciona**.

## 1. Contexto

- **Empresa:** Mercor (Mercor.io Corporation, SF). Startup de datos/evaluación para AI labs.
- **Proyecto:** "Project Odin" - dataset de training para un AI lab leader. Trabajo: completar y
  **narrar** workflows reales de desarrollo de software en la propia Mac (build, debug, refactor,
  code review) para generar training data.
- **Link del listing (fuente del JD):**
  `https://work.mercor.com/jobs/list_AAABoVBl9Qiee5DoU-hGapwb/software-developers-must-own-macbook`
- **Paga del listing:** $50-$60/hr. Contrato hourly, part-time 10-20 h/semana. contractor
  independiente. Pagos semanales vía Stripe.
- **Onboarding:** "Submit your resume, followed by a brief (3-minute) conversation with our AI
  interviewer to assess research and reasoning skills. Complete a brief paid assessment."

## 2. Requisitos del JD (los que el CV debe cubrir)

| Requisito | Estado en el corpus | Dónde se cubre |
|---|---|---|
| MacBook/Mac con M-series o Intel, macOS 15+ | **Cumple** (M4, macOS 27.2) | No va en el CV; es un requisito de hardware, no una credencial. Mencionar "macOS" en el contexto de herramientas, sin inventar. |
| Hands-on en uno o más lenguajes (Python, JS/TS, Swift, Java, Go) | **JS/TS/TypeScript** es el stack principal. Python: working proficiency AI-assisted (declarado así en el corpus). **No declarar Swift, Java ni Go** (§9: "Kotlin, Rust, Go: no son parte del stack. No listarlos por completitud"). | Core Skills + Freelancer |
| Everyday developer tools on macOS: VS Code, Xcode, Terminal, Git, package managers | VS Code, Terminal, Git, npm/pnpm/bun, Docker están en uso real y verificable. **Xcode: no registrado** - no declararlo. | Core Skills |
| Currently pursuing or recently completed Masters, **or** 2-3 years of relevant experience + Bachelors from a prestigious institution | **GAP REAL.** No hay título (todas las carreras abandonadas, corpus §3). **Se cumple por la rama de los 2-3 años de experiencia**, no por el degree. Declarar UP incompleta. | Education + Summary |
| Ability to clearly explain your reasoning while you work | **Diferencial fuerte:** es literalmente lo que hace el corpus (developer guidance, coaching en sprint, writing code guidance for UI stories, PR descriptions, documentación de remediación, PRs con contexto). | Summary + cada rol |
| Excellent written and verbal communication | Parcial: written es fuerte (documentación, PRs, ADRs), verbal es B2+ (declarado como B2+). | Summary + Languages |

## 3. Perfil a usar y por qué

**Perfil: "AI-native frontend" (corpus §10)**, con un giro: este JD no es de frontend, es de
**software developer que trabaja en su Mac y explica su razonamiento**. El重心 se corre de "UI" a
**"hands-on dev + explica qué hace y por qué"**.

El JD **no pide accesibilidad ni design systems** como tales. Pero los 11 PRs mergeados en
`adobe/react-spectrum`, `carbon-design-system/carbon`, `carbon-design-system/ibm-products`,
`facebook/astryx`, `mui/base-ui`, `mui/material-ui` son la prueba más dura y verificable de
queGonzo lee código ajeno, lo entiende y lo arregla. **Se mantiene la sección de PRs, completa:
es el activo más diferenciador del CV.** Lo que no se hace es abrir la sección con
"accessibility lead" como headline, porque el JD no lo pide.

## 4. Reglas duras (no negociables - el gate `scripts/check-cv-facts.py` las verifica)

1. **Un solo headline de años: "10+ years".** Nunca "12", nunca un número exacto.
2. **PROHIBIDO cualquier número de años de accesibilidad** (ni "5 years of a11y", ni "6+"). El
   corpus §6.2 lo prohíbe explícitamente. Contar nombrando los roles: Super7UI (Warner Bros
   Screeners) y EY (50+ componentes enterprise a WCAG 2.2 AA).
3. **Inglés: "B2+".** Nunca "fluent", "Advanced", "C1", "native". La redacción defendible es la que
   ya usa el CV de RYZ: *"English - B2+ (professional working proficiency; reading and writing are
   comfortable, spoken English is my current development area)"*. **No degradar a B2.** Y no
   mejorarlo: el corpus es explícito en que un nivel inflado se descubre en la primera repregunta.
4. **Sin título universitario.** Toda carrera listada lleva la marca `(incomplete)`. Según
   `skills/job-application/references/educacion.md`, el JD pide degree en CS afín, así que va:
   - `Universidad de Palermo - Computer Science Engineering (2001-2002, incomplete)` (la única
     que toca CS)
   - `Digital House - React (2018)`
   - `UADE - Graphic Design (2003-2004, incomplete)`
   - `Deque University - Accessibility Specialist Program (2021)` en CERTIFICATIONS
   - **FUC y UAP NO van** (no son dominio de este puesto).
   - Nunca escribir "degree", "graduated", "BSc". La forma máxima es "studied Computer Science
     at Universidad de Palermo (incomplete)".
5. **Roles y fechas canónicas, sin cambiar:** Freelancer 05/2025-Present · EY 09/2021-05/2025 ·
   Super7UI 08/2020-05/2021 · Minutentag 02/2016-11/2019. Título de EY: "Senior Frontend
   Engineer, Accessibility Lead" (la variante "Senior Full Stack / Frontend Engineer, Team Lead"
   es admisible para perfil fullstack; **no** para este).
6. **Prohibido declarar "Cursor", "GitHub Copilot"** (no están en el corpus como uso propio), y
   **prohibido declarar "computer-use" o "agentes de computer-use"** (§2.1, con el antecedente del
   27/08). Las herramientas de IA declaradas son **Claude Code y Codex** + el stack propio de
   OpenClaw.
7. **Prohibido:** criptos/Web3, Mercado Pago (Stripe es el proveedor único, ADR-042), Kotlin, Rust,
   Go, Swift, Java, Xcode, Figma, `accessibility-auditor`, "20+ A/B experiments" (el corpus no
   registra una cantidad de experimentos: la redacción defendible es "ran A/B experiments in
   production", sin número), "5 product teams" (esa librería fue EY Motif, no Minutentag),
   micro-frontends en Minutentag, "Independent/Founder" (se dice "Freelancer" o "Freelance").
8. **El archivo es para un ATS y una AI interviewer.** Formato de una columna, sin tablas de
   layout. El CV se sube como **PDF**.
9. **Idioma: inglés.** Todo el CV en inglés. Un ATS de US no lee español.
10. **Dos páginas** como máximo en el archivo final. Las secciones de trabajo ("Notes / gaps" y
    "Keyword map") son el mapa del proceso, **no** van en el archivo que se postea.

## 5. Lo que el CV tiene que resolver (el problema real)

El JD pide dos cosas que el corpus no tiene: **degree** y **excelente comunicación verbal**. El CV
no puede inventar ninguna de las dos. La estrategia es:

- **Degree:** la rama de "2-3 years of relevant experience" del requirement. En el Summary, abrir
  con los 10+ años y el ownership end-to-end, para que el filtro de años se satisfaga por el
  hecho y no por el papel. Y declarar UP incompleta en Education, que es la honestidad que le da
  chance en un filtro de degree sin mentir.
- **Comunicación verbal:** es el activo que el corpus sostiene con evidencia concreta. Hay que
  hacer explícito, en el Summary y en cada rol, que Gonzo **explica su razonamiento**: developer
  guidance con código, coaching in-sprint, documentación de remediación, PR descriptions, ADRs,
 Atlassian/Jira. **No** decir "excellent communication" como adjetivo vacío: mostrarla con hechos.
- **Que el CV parezca el de alguien que va a narrar su trabajo en pantalla** (el job es
  "completing and narrating real software development tasks"). La prosa tiene que ser de
  工程-de-senior, no de lista de skills.

## 6. Referencias en el workspace

- **Corpus (fuente única de los hechos):** `memory/career-facts.md` - leerlo entero antes de
  redactar. Es el dueño; el CV solo cita.
- **CV de referencia con el estilo ya resuelto:**
  `docs/entrevistas/ryz-labs-ai-first-frontend/cv-ai-first-frontend-ryz.md` (mismo perfil base,
  inglés, con keyword map al final).
- **Tabla de educación:** `skills/job-application/references/educacion.md`
- **Gate de hechos:** `scripts/check-cv-facts.py` (lee `memory/career-facts.md` y todos los CVs).

## 7. Qué entregar

1. `docs/entrevistas/mercor-project-odin/cv-mercor-software-developer.md` - el markdown, **es la
   verdad** del CV. Secciones: Profile/Contact · Professional Summary · Core Skills · Professional
   Experience · Open Source - Merged Pull Requests · Education · Certifications · Languages ·
   **Keyword map** (mapa contra el JD) · **Notes / gaps** (lo que el JD pide y no se cubre,
   declarado). Las dos últimas NO van al PDF que se postea.
2. La salida del gate: `python3 scripts/check-cv-facts.py` debe dar **0 violaciones** para este CV.
   Si el gate marca algo, se corrige el CV (no el corpus: el corpus es el dueño y no se toca
   para acomodar un CV).
3. No generar DOCX/PDF en este paso: eso lo hace el CORE con `scripts/cv-md-to-html.py` +
   `scripts/build-cv-docs.sh` después de tu revisión.

## 8. Lo que NO hace este CV

- No es una carta de presentación. No es un post de LinkedIn.
- No es el CV "general sin técnico" ni el de a11y puro: el recorte es otro.
- No menciona a Mercor, ni "Project Odin", ni la Lighthouse, ni el mail. Es un CV, no una
  postulación a medida con nombre de la empresa.
