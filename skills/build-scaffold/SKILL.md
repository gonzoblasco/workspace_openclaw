---
name: "build-scaffold"
metadata:
  category: "Workflow"
  tags:
    - scaffold
    - construccion
    - proyecto
description: "Workflow de Build & Scaffold: scaffolding y construcción. Reemplaza 5 skills de scaffold."
user-invocable: false
---

# Workflow: Build & Scaffold

## Skills que reemplaza
- `web-app-builder`
- `workspace-scaffold`
- `scaffold-verify`
- `ai-scaffold`
- `ai-copilot-structure`

## Propósito
Scaffolding y construcción de proyectos desde cero o sobre existentes.

## Cuándo usarlo
- Arrancar un proyecto nuevo desde cero (scaffolding inicial)
- Configurar stack: TypeScript, Tailwind, Biome, testing, linting
- Agregar CI/CD a un proyecto existente
- Iterar sobre un proyecto existente (modo --iterate)

## Fases
1. **Análisis** — entender requerimientos, stack deseado, features. Si el proyecto ya pasó por product-discovery, leer DEFINITION.md y ROADMAP en vez de preguntar todo de nuevo
2. **Scaffold** — generar estructura base (React, Next.js, Vite, etc.)
3. **Configuración** — Biome, TypeScript, Tailwind, testing, linting
4. **Verificación** — typecheck, lint, test, build
5. **Estructura** — AGENTS.md, ROADMAP, ADRs, HANDOFF template (adaptado al tamaño del proyecto)
6. **Iteración** — modificar proyectos existentes (modo --iterate)
7. **CI/CD** — configurar GitHub Actions o similar para typecheck + lint + test + build en cada PR

## Outputs
- Proyecto funcional con build verde
- `AGENTS.md`, `ROADMAP.md`, `CHANGELOG.md`
- ADRs de decisiones técnicas
- CI/CD pipeline configurado

## Related Skills

- [Task Execution](../task-execution): Para implementar features post-scaffold
- [Technical Documentation](../tech-docs): Para documentar decisiones arquitectónicas
