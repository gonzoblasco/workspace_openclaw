# DEFINITION — Accessible UI

> Phase 2 — Product Definition
> Fecha: 2026-07-16

## MVP Scope

### Core value
Librería de componentes React headless con accesibilidad WCAG 2.2 garantizada. El dev elige el diseño, nosotros garantizamos que es accesible.

### In scope (actual)
1. **Componentes headless** — sin estilos, solo lógica accesible
2. **Storybook** — documentación visual de cada componente
3. **Tests de accesibilidad** — jest-axe en cada componente
4. **WAI-ARIA compliance** — patrones según WAI-APG

### Out of scope (post-MVP)
- Publicación en npm
- Componentes con estilos por defecto
- Integración con frameworks (Next.js, Remix, etc.)

## User Personas

### Dev que necesita accesibilidad
- 25-40 años, frontend o fullstack
- Sabe que necesita accesibilidad pero no quiere aprender WCAG
- Quiere componentes que "funcionen" sin pensar en ARIA
- Valora que el diseño sea decisión suya, no de la librería

## Success Metrics

1. Componentes implementados
2. Tests de accesibilidad pasando
3. Uso en proyectos reales (Gonzo, comunidad)
4. Stars en GitHub
