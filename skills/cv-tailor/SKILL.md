---
name: "cv-tailor"
metadata:
  category: "Career"
  tags:
    - cv
    - resume
    - busqueda-laboral
    - ats
    - star
description: "Optimizar CVs: matching de keywords contra JD, reescritura STAR con datos cuantificados, y verificación de compatibilidad ATS."
user-invocable: false
---

# Workflow: CV Tailor

## Propósito

Optimizar currículums para maximizar el rate de aprobación en procesos de selección. Tres pilares: análisis de keywords contra la descripción del puesto, reescritura de experiencia con método STAR y datos cuantificados, y verificación de compatibilidad con ATS (Applicant Tracking System).

## Filosofía

> Your resume doesn't get you the job. It gets you the interview.

Cada palabra cuenta. Cada número suma. Cada keyword mal ubicada resta.

---

# Cuándo usarlo

- Optimizar CV para una postulación específica
- Analizar cobertura de keywords contra un JD
- Reescribir experiencia laboral con STAR
- Verificar compatibilidad ATS
- Preparar CV para búsqueda activa

---

# Fases

## 1. Input Collection

Recolectar:
- CV actual (texto o archivo)
- JD target (texto o descripción del rol)
- Si no hay JD, preguntar: industria + posición + seniority

## 2. Keyword Match Analysis

Extraer keywords del JD en 3 categorías:

| Categoría | Ejemplos |
|---|---|
| **Hard skills** | Python, SQL, React, A/B testing, Scrum |
| **Soft skills** | Cross-team collaboration, data-driven, project management |
| **Industry/domain** | DAU, conversion rate, SaaS, user growth |

Generar matriz de matching:
- Required keyword coverage ≥ 80% = passing, ≥ 90% = excellent
- Recomendar dónde agregar keywords faltantes

### ⚠️ Checkpoint obligatorio

**Después de Fase 2, PAUSAR.** Presentar al usuario:
- Matriz de cobertura con gaps identificados
- Preguntar: ¿tenés experiencia en [gap 1], [gap 2], [gap 3]?
- Esperar respuesta antes de continuar a Fase 3

No asumir ni inventar. El usuario decide qué gaps puede cubrir y cómo.

## 3. STAR Rewriting

Reescribir cada entrada de experiencia:

| Elemento | Checkpoint |
|---|---|
| **S** Situation | Contexto, escala, cuándo |
| **T** Task | Objetivo, responsabilidad personal |
| **A** Action | Acciones específicas, métodos, herramientas |
| **R** Result | Outcomes cuantificados, datos |

Cada entry rewrite debe:
- [ ] Al menos 1 dato cuantificado
- [ ] Cubrir ≥ 3 de 4 elementos STAR
- [ ] Empezar con verbo de acción (led, built, optimized, drove)
- [ ] Máximo 3 líneas (legibilidad ATS)
- [ ] Incorporar keywords faltantes del Phase 2, según lo confirmado por el usuario

## 4. ATS Compatibility Check

| Check | Standard |
|---|---|
| File format | PDF o DOCX (PDF preferred) |
| Layout | Single-column, standard headings |
| Fonts | Arial, Calibri, Times New Roman |
| Tables | Avoid complex layouts |
| Section titles | "Work Experience", "Education", "Skills" |
| Date format | Consistent (Jan 2023 – Jun 2024) |
| File naming | FirstName_LastName_Role_Resume.pdf |

## 5. Output

- Optimization summary (coverage %, STAR score, ATS score)
- CV reescrito con cambios en **bold**
- Recomendaciones adicionales

---

# Outputs

- Keyword match matrix
- Before/after STAR comparison
- ATS compatibility scorecard
- CV optimizado listo para postular

---

# Principios

- Autenticidad primero: no inventar datos
- Cada cambio debe servir al JD alignment
- Recomendaciones accionables, no genéricas
- Privacidad: recordar redactar datos sensibles

---

# Related Skills

- [Mock Interview Drill](../mock-interview-drill): Para practicar entrevistas post-CV
- [Narrative Content](../narrative-content): Para contar tu historia profesional
