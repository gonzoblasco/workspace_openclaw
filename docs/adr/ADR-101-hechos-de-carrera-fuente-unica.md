# ADR-101: Hechos de carrera con dueño único y freno ante contradicción

**Fecha:** 2026-10-20
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** workspace - "por cada postulación tenemos un cv con una verdad distinta y eso no es creíble siendo yo uno solo... los únicos casos son los de distinto perfil, pero para perfiles similares debe ser siempre el mismo"
**Relacionado:** ADR-100 (fuente única de la verdad), ADR-065 (DB-first vs doc-only), ADR-083 (una regla sin guarda se viola sola)

---

## Contexto

ADR-100 cerró el reparto de datos de **gobernanza** (reglas, estado, entorno, decisiones). No cubría el caso que Gonzo nombró como el más caro: **el material de postulación**. Un reclutador puede ver dos CVs del mismo candidato y compararlos; un screening registra el nivel de inglés declarado; un background check llama a la empresa y pregunta por las fechas.

Medido el 2026-10-20 sobre los 5 CVs vivos contra el perfil documentado:

| Hecho | CVs | Perfil documentado |
|---|---|---|
| Años totales | 10+, 10+, 10 años | 10+ años |
| **Años totales (CV a11y)** | **9+** | 10+ años |
| **Años de a11y** | **6+ "enterprise"** (CV a11y) | **sin número** (Super7 ~0.75 + EY ~3.67 = 4.42) |
| **Inglés** | "Advanced written, intermediate spoken" | **B2, nunca C1 ni superior** |
| Certificación | "Deque University accessibility certification" (en un rol de 2020-2021) | Programa Deque 2021; **sin IAAP** |
| Títulos por rol | 4 variantes de EY y 3 de Super7 según el CV | 4 roles canónicos |

Ninguna de esas divergencias la detectó un gate. `check-refs` verificaba rutas; `check-single-source` (ADR-100) verificaba reglas normativas. Un CV es un artefacto de **salida** con hechos de **entrada**, y nadie verificaba la correspondencia.

El daño no es estético. Un CV que declara 9+ años y otro 10+ del mismo autor, con 6+ de a11y en uno y ~5 en el perfil, es exactamente la clase de inconsistencia que un screening detecta y no perdona.

## Decisión

### 1. Perfil ≠ hecho

La distinción que hace viable todo lo demás:

- Un **perfil** distinto (a11y, fullstack, evaluator, no técnico) cambia el **relato**: el resumen, el orden de los bullets, qué proyecto se destaca, qué skill encabeza.
- **Nunca** cambia los **hechos**: fechas, años, títulos por rol, nivel de idioma, certificaciones, contacto.

`cv-general-no-tecnico` puede no mencionar React y hablar de gestión de proyectos. No puede decir "10 años" mientras el de a11y dice "9+".

### 2. Dueño único: `memory/career-facts.md`

Vive bajo `memory/` porque `memory_search` indexa `memory/` y no `docs/`: el dato tiene que ser recuperable al escribir. Contiene un bloque ```facts``` legible por máquina y la prosa que explica cómo contarlo.

Es **doc-only** (ADR-065): no hay tabla en `memory.db` ni export. Un hecho se cambia editando el archivo, y se propaga a los CVs en la misma sesión.

`memory/user-profile.md` deja de declarar años, fechas y títulos: guarda la **lectura** de esos hechos y los cita.

### 3. Enforcement: `scripts/check-cv-facts.py`

Corre **sin condición** en pre-commit y CI. Verifica, contra el bloque `facts`:

| Check | Qué caza |
|---|---|
| Años por categoría | "N years in <frase>" se compara contra la categoría que describe la frase |
| Idioma | Cualquier nivel por encima del declarado (`Advanced` = C1 = bloqueado) |
| Contacto | Teléfono, email, LinkedIn, GitHub que no coinciden |
| Fechas de rol | El periodo del encabezado, con la precisión que el CV declare |
| Certificación | "Deque = certification" o una credencial IAAP inexistente |
| **Pendientes** | Un hecho marcado `pending` **frena el commit** |

### 4. La regla de freno (la parte que Gonzo pidió explícitamente)

> "Si en una conversación futura se define algo contradictorio, se frena en ese momento y se plantea cómo solucionarlo, no se espera a tener 20 fuentes de verdad."

Se implementa en dos capas:

- **En `AGENTS.md`, sección 0:** una contradicción se nombra, se decide y se corrige en el momento. No se promedia, no se arregla después.
- **En el gate:** un hecho con `pending: N` y `pending_note` **no commitea aunque todo lo demás esté verde**. Una contradicción sin decidir no entra al repo "para arreglarla después", porque ese "después" es donde nacen las veinte fuentes.

## Consecuencias

### Positivas
- Los 5 CVs convergen a un solo juego de hechos verificable. La única divergencia admitida es el relato.
- La primera corrida del gate cazó **3 contradicciones reales** (años, Deque, inglés) y **1 decisión pendiente** de aritmética que ni siquiera estaba en discusión: el 6+ de a11y contra los 4.42 a 5.83 calculados.
- Al meter `memory/user-profile.md` en el alcance de ADR-100, aparecieron **13 reglas duplicadas** entre `MEMORY.md` y el perfil. Un dueño fuera del gate es un dueño que nadie verifica.

### Negativas
- Escribir un CV ahora exige pasar por `career-facts.md`. Es la fricción que evita el drift.
- El check de años depende de la frase que sigue al número. Un "N years" sin categoría reconocible no se juzga: el gate elige no adivinar antes que producir falsos positivos.

### Decisión cerrada: accesibilidad no lleva número (2026-10-20)

El CV de a11y declaraba `6+ years in enterprise digital accessibility engineering`. La aritmética de las fechas canónicas da **4.42 años** de función central (Super7 08/2020-05/2021 = 0.75 + EY 09/2021-05/2025 = 3.67), y **5.83** si se cuenta todo el freelance 05/2025-hoy. Ni 5 ni 6 cierran sin definir un alcance que el reclutador no va a leer.

**Decisión de Gonzo: opción C - sacar el número y nombrar los roles.**

- Se cuenta **Super7UI** (auditoría de remediación de Warner Bros. Screeners) y **EY** (referente de a11y, 50+ componentes enterprise a WCAG), más las contribuciones OSS a Adobe, IBM, Meta y MUI.
- **Prohibido** escribir "N years of accessibility" o "N+ años de accesibilidad" en cualquier CV, carta o screening. El gate lo reporta como violación directa, sin comparar contra ningún valor.
- El mismo criterio se aplicó al CV de code evaluator, que declaraba "roughly 5 years with accessibility": dos formas de contar el mismo hecho son dos verdades.
- `a11y_years_internal: 5` queda en el dueño como **calibración interna** para decidir si una propuesta tiene sentido. No es un dato de salida.

El fundamento: los hechos concretos -roles, fechas, 200+ violaciones validadas, 50+ componentes, PRs mergeados- son más fuertes que un redondo, y no se pueden desmontar con una resta.

### La regla se aplicó a mí (mismo día)

Al escribir el dueño puse `ai_years: 5` y el CV decía `5+ years working AI-first`. El diff de `memory/user-profile.md` mostró una corrección de Gonzo del mismo día: **IA para desarrollo desde 05/2025, ~1 año y medio, nunca 3**. Eran dos verdades, una de cada lado, y la mía era la vieja.

Se frenó, se corrigió el dueño (`ai_years: 1`, `backend_years_internal: 1`) y se propagó al CV: `5+ years working AI-first` -> `working AI-first since 2025`, y `backend ... with equal footing` -> `frontend is my home ground, with hands-on backend work since 2025` (el split real es 70/30).

**Ese es el caso que la regla existe para atajar**, y ocurrió en la misma sesión que la escribió. Un dueño nuevo no es inmune al drift: hereda el que ya estaba.
