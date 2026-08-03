---
name: "code-mentor"
metadata:
  category: "Education"
  tags:
    - programacion
    - tutor
    - aprendizaje
    - algoritmos
description: "Tutor integral de programación: lecciones interactivas, code review, debugging, práctica de algoritmos y guía de proyectos."
user-invocable: false
---

# Workflow: Code Mentor

## Propósito

Tutor integral de programación con 8 modos de enseñanza: conceptos, code review, debugging, algoritmos, arquitectura, design patterns, entrevistas y aprendizaje de lenguajes.

## Cuándo usarlo

- Aprender un nuevo lenguaje o concepto
- Debuggear código con método socrático
- Practicar algoritmos y estructuras de datos
- Preparar entrevistas técnicas
- Revisar y refactorizar código

## Teaching Modes

| Mode | Purpose | Method |
|---|---|---|
| **Concept Learning** | Aprender conceptos nuevos | Ejemplos progresivos + práctica guiada |
| **Code Review** | Feedback sobre código existente | Análisis por categorías + mejora guiada |
| **Debugging Detective** | Debug sistemático | Método socrático de 5 niveles |
| **Algorithm Practice** | Algoritmos y DS | Problemas con hint system progresivo |
| **Project Guidance** | Arquitectura de proyectos | Requirements → stack → diseño → implementación |
| **Design Patterns** | Patrones y best practices | Bad code → análisis → pattern → refactor |
| **Interview Prep** | Entrevistas técnicas | Problemas timed + feedback estructurado |
| **Language Learning** | Nuevo lenguaje | Mapeo desde lenguaje conocido |

## Outputs

- Lecciones interactivas
- Code reviews con diagnóstico STAR
- Debug reports con root cause
- Algoritmos resueltos con análisis de complejidad
- Guías de arquitectura de proyectos

## Tooling relacionado

| Skill / Script | Uso |
|---|---|
| `debug-investigation/scripts/reproduce-check.sh` | Verificar pasos de reproducción en Debugging Detective. |
| `debug-investigation/scripts/bisect.sh` | Encontrar primer commit malo cuando se sospecha regresión. |
| `review-quality/scripts/review-pr.sh` | Code review automatizado de PRs reales. |
| `mock-interview-drill/scripts/question-generator.py` | Generar problemas para Interview Prep. |
| `sql-insight/scripts/sql_query_helper.py` | Analizar y optimizar queries en proyectos. |

## Related Skills

- [Task Execution](../task-execution): Para implementar lo aprendido
- [Review & Quality](../review-quality): Para code review de PRs reales
