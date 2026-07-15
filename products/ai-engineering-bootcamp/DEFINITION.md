# DEFINITION.md — AI Engineering Bootcamp

> Phase 2 — Product Definition
> Fecha: 2026-07-15

## MVP Scope

### Core value
Un bootcamp gratuito y open source de 10 niveles para dominar el desarrollo asistido por IA con VS Code + GitHub Copilot. 23 proyectos prácticos, desde principiante hasta producción.

### In scope (MVP)
1. **10 niveles documentados** — traducidos a inglés, con objetivos claros y self-reviews
2. **Proyectos completos** — código funcional para los 23 proyectos
3. **README.md** — atractivo, con tabla de progreso visual
4. **Guía de herramientas** — VS Code + Copilot como equivalente a Cursor/Claude Code
5. **Repositorio público** — bajo la organización Kanam o cuenta personal

### Out of scope (post-MVP)
- Videos / screencasts — post-MVP
- Foro de comunidad — post-MVP
- Certificaciones — post-MVP
- Versión en español — post-MVP (el MVP es en inglés)

### Explicit non-goals
- No es un curso de ML/AI engineering
- No reemplaza la documentación oficial de Copilot
- No es interactivo (no hay plataforma, solo repo)

## User Personas

### Persona 1: El dev junior que quiere acelerar
- **Quién:** Dev con 1-3 años de experiencia, usa Copilot básico (autocomplete)
- **Context:** Sabe que la IA puede hacerlo más productivo pero no tiene un método
- **Necesita:** Un camino estructurado para pasar de "aceptar sugerencias" a "orquestar agentes"
- **Éxito:** Completa los 10 niveles y puede diseñar workflows complejos con IA

### Persona 2: El dev senior que formaliza
- **Quién:** Dev senior, 8+ años, ya usa IA pero sin metodología
- **Context:** Quiere estandarizar su workflow y poder enseñar a su equipo
- **Necesita:** Un framework completo con auditoría, CI/CD, y patrones de equipo
- **Éxito:** Implementa los patrones del bootcamp en su equipo y mide el impacto

## User Flows

### Flow 1: Descubrimiento y primer nivel
- **Trigger:** Dev encuentra el repo en GitHub
- **Steps:**
  1. Lee README, ve la tabla de progreso
  2. Clona el repo
  3. Abre `docs/level-01-hola-mundo.md`
  4. Sigue los pasos, completa los 2 proyectos
  5. Marca el nivel como completo
- **Outcome:** Primer nivel completado, motivado para seguir

### Flow 2: Progresión entre niveles
- **Trigger:** Dev completa un nivel
- **Steps:**
  1. Hace self-review (responde preguntas)
  2. Si pasa, avanza al siguiente nivel
  3. Cada nivel introduce nuevos conceptos y proyectos más complejos
- **Outcome:** Progresión natural, sin saltos

### Flow 3: Proyecto con código
- **Trigger:** Dev llega a un nivel con proyecto
- **Steps:**
  1. Lee la descripción del proyecto en `docs/`
  2. Abre el proyecto en `projects/level-XX-nombre/`
  3. Sigue las instrucciones, usa Copilot para implementar
  4. Compara con la solución de referencia (si existe)
- **Outcome:** Proyecto funcional, aprendizaje práctico

## Success Metrics

1. **GitHub stars** — 50+ en 3 meses
2. **Forks** — señal de uso real
3. **Issues/PRs** — comunidad contribuyendo
4. **Completitud de proyectos** — al menos 10/23 proyectos con código funcional
