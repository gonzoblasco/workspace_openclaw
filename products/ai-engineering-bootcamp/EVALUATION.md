# EVALUATION.md — AI Engineering Bootcamp

> Phase 1 — Product Evaluation
> Fecha: 2026-07-15

## Problem

Los devs saben que la IA cambió la forma de desarrollar, pero no hay un camino estructurado para aprender a usarla bien. La mayoría aprende por prueba y error, sin metodología, sin workflows, sin auditoría. Los cursos existentes enseñan ML/AI engineering, no "cómo ser un mejor dev usando IA".

## Audience

- **Devs junior/mid** que quieren aprender AI-assisted development
- **Devs senior** que quieren formalizar su workflow con IA
- **Gente preparándose para roles** tipo "AI-Driven Engineering Specialist"
- Tamaño: nicho grande. Hay 38K stars en un repo similar (pero de AI engineering, no de AI-assisted dev)

## Existing solutions

| Proyecto | Stars | Enfoque | Diferencia |
|---|---|---|---|
| rohitg00/ai-engineering-from-scratch | 38K | AI/ML engineering full stack | No es AI-assisted development |
| ai-builders-curriculum | 141 | Full-stack AI apps | Vendor-neutral, no específico de Copilot |
| sudo-make-me-a-developer | 1 | Zero to AI-powered coder | Principiantes absolutos |
| Open Vibe (Wasp) | — | Learn web dev with AI tutor | Enfocado en web dev, no en workflow |

**Gap:** Nadie ofrece un **bootcamp práctico y gamificado** específicamente para **AI-assisted development con VS Code + Copilot**, que cubra desde prompts hasta producción, con proyectos reales y self-reviews.

## Differentiation

1. **Gamificado** — 10 niveles con progresión clara, cada nivel desbloquea el siguiente
2. **Práctico** — 23 proyectos reales, no teoría
3. **VS Code + Copilot** — no requiere Cursor/Claude Code, accesible para más devs
4. **Cubre el ciclo completo** — desde "Hola Mundo" hasta producción y multiplicador de equipo
5. **Self-review en cada nivel** — el dev evalúa su propio progreso antes de avanzar
6. **Gratuito y open source** — MIT, cualquiera puede usarlo y contribuir

## Revenue model

**Gratuito + GitHub Sponsors.** Es contenido educativo, no un producto SaaS. Pero:
- **Portfolio piece** — muestra que Gonzo puede estructurar y enseñar metodología
- **Diferenciador en entrevistas** — "creé un bootcamp usado por X personas"
- **Tráfico al perfil de GitHub** — más visibilidad = más oportunidades

## Technical feasibility

- **Ya existe** — 10 niveles documentados, 23 proyectos definidos, algunos con código
- **Lo que falta:** pulir docs, traducir a inglés, crear repo, completar proyectos faltantes
- **Complejidad:** baja (es contenido + proyectos Express.js simples)
- **Tiempo estimado MVP:** 2-3 días

## Strategic fit

- **Fit con objetivos de Gonzo:** ALTO — muestra capacidad de enseñanza + metodología + open source
- **Fit con ecosistema Kanam:** ALTO — los patrones y convenciones del bootcamp son los mismos del Kanam Workflow Kit
- **Sinergia:** el bootcamp puede recomendar el Kanam Workflow Kit en niveles avanzados
- **Opportunity cost:** bajo — es contenido, no código complejo

## Verdict: 🟢 GO

### Recommendation
Convertir `pr_vscode_niveles` en un bootcamp público open source. Incluye:
1. Los 10 niveles existentes (traducidos a inglés)
2. Proyectos completos con código
3. README atractivo con progresión visual
4. Integración con Kanam Workflow Kit en niveles avanzados
