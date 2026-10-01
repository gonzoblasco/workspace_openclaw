# CPACC - Plan de estudio

> Preparación para el examen **CPACC** (Certified Professional in Accessibility Core Competencies, IAAP).
> Armado 2026-09-29 sobre la fuente primaria: `docs/cpacc/cpacc-bok.pdf` (Body of Knowledge, octubre 2023, 82 pp).
> **Corregido 2026-09-30** con las fechas oficiales de examen (página *Exam Session Dates* de IAAP, aportada por Gonzalo): la aplicación de la sesión objetivo cierra el **12 de noviembre**, no el 9 de diciembre. Ver sección 2.
> Este documento es la fuente de verdad del plan; el material de estudio vive en `docs/cpacc/`.

## 1. Objetivo

- **Motivación:** meta **personal** de Gonzo (crecimiento propio en a11y). Sin urgencia ni compromiso con terceros.
- **Objetivo de calendario (meta fijada por Gonzo, 2026-09-30):** anotarse a la sesión **November/December 2026** **a más tardar la primera semana de noviembre** (meta interna, con colchón). El cierre oficial de aplicación es el **12 de noviembre, 5pm ET**, y el **9 de diciembre** es el último día de examen de la sesión (no el cierre de aplicación).
- **Ritmo:** flexible, sin presión. La ventaja: la experiencia real en a11y web cubre buena parte de los Dominios 2 y 3; el foco va al **lado humano** (Dominio 1).

## 2. Estado del examen (verificado vs a verificar)

**Verificado contra el handbook oficial (`docs/cpacc/cpacc-handbook.pdf`, ene 2026):**
- IAAP abre **6 sesiones de examen por año**; cada una: ventana de examen, apertura y cierre de aplicación, fecha límite de pago, última fecha para agendar. **No hay aplicaciones rodantes.** Ejemplo real del handbook: sesión *September/October 2025* → aplicaciones cerraron 17/09/2025 y el último día de examen fue 08/10/2025.
- Resultados por email **4-6 semanas** después del cierre de la sesión.
- Transferir de sesión: USD 50 (con +4 días hábiles) / USD 100 (con -4 días hábiles).
- Renovación: credencial válida **3 años**; con membresía IAAP activa, sin costo. CPACC requiere **45 CEUs** por ciclo.

**Confirmado contra la página oficial *Exam Session Dates* de IAAP (2026-09-30):**

Sesión objetivo - **November/December 2026**:
- **Exámenes:** 12 de noviembre al 9 de diciembre de 2026.
- **Aplicaciones abren:** 28 de octubre. **Aplicaciones cierran:** 12 de noviembre, 5pm ET.
- **Pago vence:** 18 de noviembre. **Agenda abre:** 2 de noviembre; **cierra:** 30 de noviembre.
- Resultados: entre el 6 y el 20 de enero de 2027.
- Examen presencial adicional en *Accessing Higher Ground*, 17 de noviembre.

**Fallback - January/February 2027** (si no se llega a noviembre): exámenes 20/01 al 17/02/2027; aplicaciones abren 06/01 y cierran 20/01/2027, 5pm ET.

**Sigue a verificar en el portal:**
- **Fee:** ~USD 385-545 según credencial/membresía (fuente de terceros; confirmar en el portal al aplicar).
- Formato vigente: 100 preguntas de opción múltiple, 2 h, aprueba con **600/800**.

## 3. Mapa de dominios (del BoK oficial)

| Dominio | Peso | Subdominios |
|---|---|---|
| **1. Disabilities, Challenges & Assistive Technologies** | **40%** | 1A Modelos teóricos · 1B Categorías/características de discapacidades, barreras y soluciones · 1C Tecnologías de asistencia y estrategias adaptativas · 1D Tendencias de datos e implicaciones · 1E Etiqueta de discapacidad |
| **2. Accessibility and Universal Design** | **40%** | 2A Acomodaciones individualizadas · 2B Beneficios de la accesibilidad · 2C Principios de accesibilidad web (WCAG 2.1) · 2D Accesibilidad del entorno construido · 2E Principios de Diseño Universal · 2F Universal Design for Learning (UDL) |
| **3. Standards, Laws & Management Strategies** | **20%** | 3A Declaraciones/convenciones internacionales · 3B Instrumentos regionales · 3C Instrumentos nacionales/provinciales · 3D Leyes de dominio específico y de compras públicas · 3E Estándares aplicados a las TIC · 3F Integrar accesibilidad TIC en la organización |

**Los 7 modelos de discapacidad (Dominio 1A, alta densidad de preguntas):**
médico · social · biopsicosocial · económico · funcional-solución · identidad social / afiliación cultural · caridad.

## 4. Plan de 10 semanas (hasta el cierre de aplicación, 12/11)

> **Ajuste 2026-09-30:** con el cierre de aplicación el 12/11, el plan original (que se estiraba hasta el 9/12) se **adelanta**. La ventana de examen es 12/11 al 09/12, así que el estudio tiene que estar listo **antes del 12/11**, no del 9/12. Si se apunta al fallback de enero/febrero 2027, el mismo plan corre dos meses más con ritmo más holgado.

| Semana | Foco | Del BoK | Entregable de la semana |
|---|---|---|---|
| **1** (29/09-05/10) | Mapear conocimiento vs BoK. Modelos de discapacidad. | Intro + 1A (pp. 4-8) | Tabla "conocido / por aprender" por subdominio. Flashcards de los 7 modelos. Material armado en [`week-1/`](./week-1/README.md). |
| **2** (06-12/10) | Discapacidades: categorías, barreras, soluciones. | 1B (pp. 9-25) | Fichas por categoría (visual, auditiva, motora, cognitiva, del habla) + barreras típicas. |
| **3** (13-19/10) | Tecnologías de asistencia y estrategias adaptativas. | 1C (pp. 26-34) | Lista de AT por discapacidad (JAWS, NVDA, VoiceOver, lectores, hápticos, switch, etc.). |
| **4** (20-26/10) | Datos e implicaciones + etiqueta. Cerrar Dominio 1. | 1D + 1E (pp. 35) | Autotest de Dominio 1. |
| **5** (27/10-02/11) | WCAG 2.1 en web + beneficios y acomodaciones. (Fortaleza: repaso rápido y a fondo.) | 2A-2C (pp. 36-41) | Repaso de POUR + criterios que suelen confundirse. |
| **6** (03-09/11) | Entorno construido, Diseño Universal, UDL. | 2D-2F (pp. 41-47) | Fichas de los 7 principios del Diseño Universal + UDL. |
| **7** (10-16/11) | Estándares, leyes y gestión: instrumentos internacionales/regionales/nacionales. | 3A-3C (pp. 48-58) | Tabla de instrumentos por alcance (internacional vs regional vs nacional). |
| **8** (17-23/11) | Leyes de dominio específico y compras + estándares TIC + gestión organizacional. Cerrar Dominio 3. | 3D-3F (pp. 59-70) | Fichas de las leyes clave (ADA, Section 508, EN 301 549) y de integración TIC. |
| **9** (24-30/11) | Repaso integrador de los 3 dominios. | Todo | Primer mock completo (100 preguntas, 2 h) + revisión de errores contra el BoK. |
| **10** (01-09/12) | Cierre: puntos débiles + simulacro final. | Todo | Segundo mock; cerrar la tabla "conocido / por aprender". |

**Ventana del examen:** 12/11 al 09/12/2026. El examen se agenda tras la aprobación y el pago (ATT de Pearson en ≤5 días hábiles), y **la agenda cierra el 30/11** - el examen debe rendirse antes de esa fecha (o pedir transferencia de sesión: USD 50/100).
**Acción crítica (meta):** aplicar **dentro de la primera semana de noviembre** (del 28/10 al ~07/11), no esperar al límite del 12/11 - así queda colchón para aprobación, pago (vence 18/11) y agenda. Perdida la ventana del 12/11, el fallback es la sesión de enero/febrero 2027.

## 4.bis Material por semana

- **Semana 1** - [`week-1/README.md`](./week-1/README.md): ficha de 1A, flashcards, 24 preguntas de práctica, mapa de conocimiento y logística del examen.

## 5. Recursos

- **BoK oficial** - `docs/cpacc/cpacc-bok.pdf` (fuente primaria; el mapa del plan).
- **Handbook oficial** - `docs/cpacc/cpacc-handbook.pdf` (logística, políticas).
- **Deque University** - curso CPACC (video + práctica); Gonzo ya usó la plataforma (5 cursos en 2021).
- **Curso de preparación IAAP** (edunext) - verificar apertura de inscripción (hoy aparece "Enrollment is Closed").
- **Quizlet / Anki** - banco propio de términos y acrónimos.
- **100 Days of A11y** - `https://100daysofa11y.com/cpacc/` (diario de estudio, contexto).
- **Preguntas de práctica** - las oficiales de IAAP + banco propio armado desde el BoK.

## 6. Ritmo de práctica

- **Diario:** 15 min de flashcards (términos, modelos, AT, instrumentos legales).
- **2 veces/semana:** sesión de preguntas de práctica, revisando la justificación de cada error contra el BoK.
- **Banco propio:** ir extrayendo preguntas del BoK a Anki/Quizlet desde la semana 1.
- **Simulacros completos:** semanas 9 y 10.

## 7. Logística del día del examen

- Documento de identidad con foto (nombre exacto al del registro).
- Ambiente privado y silencioso; conexión estable (si es remoto proctored) o test center.
- Solo dispositivos aprobados por IAAP (sin teléfonos, smartwatches, notas, segundo monitor).
- Cero comunicación durante el examen (cualquier violación = descalificación).

## 8. Primeras 3 acciones

1. **Aplicar en la primera semana de noviembre** (ventana 28/10-07/11; límite oficial 12/11, 5pm ET). Es la única acción con vencimiento duro del plan. Confirmar el fee en el portal al aplicar.
2. **Registrarse** en la sesión Nov/Dec 2026 dentro de esa ventana (se abre y cierra por sesión; no hay aplicaciones rodantes).
3. **Semana 1:** abrir el BoK, leer Intro + 1A, y armar la tabla "conocido / por aprender".

---

_Nota: corregido el 2026-09-30 con la página oficial de fechas. El 9/12 que se manejaba como "cierre de aplicación" es en realidad el último día de examen; el cierre de aplicación es el 12/11._
