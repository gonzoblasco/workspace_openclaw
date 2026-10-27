<!-- project: github.com/gonzoblasco/workspace_openclaw -->

# Educación en los CVs: qué va y cuándo

> **Por qué existe (27/10/2026).** Gonzo, al ver que FUC y UAP quedaban "registrados pero no
> declarados" con un "la selección es tuya": *"esto tú debes ayudarme a decidir cuándo va o no
> según el puesto al que me presento"*. Y tiene razón: la decisión de qué entra en un CV es del
> CORE, con un criterio escrito. La selección no es un juicio improvisado en cada postulación.
>
> **El problema que esta tabla resuelve.** En octubre 2026, 5 CVs declaraban
> *"Universidad Argentina de la Empresa - Diseño Gráfico (2003-2004)"* sin ninguna marca. A un
> recruiting, eso **se lee como título obtenido**. Y era falso: **ninguna de las 4 universidades
> se completó** (UP 2001-2002 Ing. Informática, UADE 2003-2004 Diseño Gráfico, FUC 2006-2009
> Montaje cinematográfico, UAP 2010-2012 Comunicación Social - las cuatro abandonadas). El gate
> ahora lo caza (control 9).

## Los hechos (dueño único: `memory/career-facts.md` §3)

| Período | Institución | Carrera | Estado |
|---|---|---|---|
| 2001-2002 | Universidad de Palermo (UP) | Ingeniería en Informática | **abandonada** |
| 2003-2004 | Universidad Argentina de la Empresa (UADE) | Diseño Gráfico | **abandonada** |
| 2006-2009 | Universidad del Cine (FUC) | Montaje cinematográfico | **abandonada** |
| 2010-2012 | Universidad Adventista del Plata (UAP) | Comunicación Social | **abandonada** |
| 2018 | Digital House (terciario) | React | **completado** |

**Formación continua:** Platzi, Deque University (2021) y muchos más cursos. **Los cursos de
Platzi no están enumerados** (no se inventan): cuando se declaren, van con su nombre real.

**No hay título universitario.** Ninguno. Y Digital House es un bootcamp, no un título.

## La tabla: qué va según qué pida el JD

El criterio es **verificable contra el posting**, no una impresión. Se lee el requisito y se
aplica la fila.

| Qué pide el JD | Sección EDUCATION | Razón |
|---|---|---|
| **No menciona educación** | `Digital House - React (2018)` + `UADE - Diseño Gráfico (2003-2004, incomplete)` | Línea base. Son formación real en React y en diseño. La marca `(incomplete)` es **obligatoria**: sin ella, se lee como título. |
| **"Degree in Computer Science / Engineering / related"** (Medallia, TEAM/tempo.io) | `Digital House - React (2018)` + `UADE - Diseño Gráfico (2003-2004, incomplete)` + **`Universidad de Palermo - Ingeniería en Informática (2001-2002, incomplete)`** + formación continua (Platzi/Deque) en CERTIFICATIONS | **La línea de UP es la única que toca "Computer Science"**, y declararla incompleta es honesto y es lo que da chance en un filtro de degree. Sin ella, un ATS que busca "Computer Science" no encuentra nada. |
| **Pide "certificación relevante" / "relevant regional certification"** (EIT/HTC/Disney) | `Digital House - React (2018)` + **CERTIFICATIONS: `Deque University - Accessibility Specialist Program (2021)`** | Deque es **exactamente** un programa de certificación de entrenamiento técnico en accesibilidad. Es la palanca real para ese JD, y ya está en el corpus como completada. |
| **Puesto de diseño / UX** (Mercado Pago UX Expert) | `Digital House - React (2018)` + `UADE - Diseño Gráfico (2003-2004, incomplete)` + el design system propio en el cuerpo del CV | **Único caso donde UADE aporta de verdad**: es diseño gráfico, y el rol es diseño↔ingeniería. Aun así va marcada incompleta. |
| **Puesto de comunicación / contenido** | `UAP - Comunicación Social (2010-2012, incomplete)` + Digital House | Solo si el rol es de comunicación editorial. No es el caso de ninguno de los postings activos. |
| **Puesto de video / audiovisual** | `FUC - Montaje cinematográfico (2006-2009, incomplete)` | Solo si el rol es de video o audio. No es el caso de ninguno de los postings activos. |

**FUC y UAP no van en ningún posting que tenemos.** No por decisión de estilo: porque los postings
que tenemos son de software y ninguno toca esos dominios. Si algún día aparece un rol de diseño
audiovisual, FUC entra con su marca.

## Las tres reglas que no se negocian

1. **Toda carrera listada lleva su marca `(incomplete)`.** El gate lo verifica (control 9). Sin
   la marca, la línea **se lee como título obtenido** - y eso es mentir sobre un hecho duro.
2. **Nunca se escribe "degree" ni "graduated" ni el nombre de un título que no existe.** No hay
   título. "Studied Computer Science at Universidad de Palermo (incomplete)" es la forma máxima
   defendible.
3. **El corpus es la fuente; esta tabla es el filtro.** Si un CV necesita un hecho que no está en
   `memory/career-facts.md`, el hecho va al corpus primero (ADR-101).

## Qué pasa cuando el JD exige degree y no hay

**No es motivo para descartar la candidatura, y tampoco motivo para mentir.**

El filtro de "degree" en un ATS es de papel: mira la cadena de texto, no evalúa a la persona. La
mayoría de los equipos que reclutan a senior filtran por *otro* - años, stack, evidencia. Un
recruiter senior que ve "10+ años, 11 PRs mergeados en las librerías que usan, a11y enterprise"
lee la línea UP incompleta como **"hizo carrera técnica y la dejó"**, que es más honesto y más
convincente que un título de bootcamp.

**Lo que sí hay que hacer en ese caso**, en la llamada o en el mensaje:
- No esconder la sección: si el CV la declara con la marca, está declarada.
- Si preguntan, la respuesta es una línea: *"Estudié Ingeniería en Informática en la Universidad
  de Palermo entre 2001 y 2002 y no lo terminé. Mi formación técnica real es el trabajo: 10 años
  de frontend, 11 PRs mergeados en librerías de producción."*

**Nunca** decir "sí, tengo título en CS". Un C1 de papel sin nivel real es peor que un B2
honesto, y un título inventado es peor que un título ausente: el equipo lo descubre en la
primera repregunta y pierde la confianza que el CV compró.
