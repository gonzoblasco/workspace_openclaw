# HANDOFF — ai-developer-stack (ex antigravity-developer-stack)

## Estado actual
**Fecha:** 2026-07-24
**Fase:** Candidato a reset

## Qué es
Colección de ~30 skills/playbooks de ingeniería con IA. Originalmente `antigravity-developer-stack`, renombrado a `ai-developer-stack`. Contenido valioso pero estructura monolítica.

## Problemas conocidos
- Nombre críptico (antigravity-developer-stack → ai-developer-stack no mejora mucho)
- Mezcla demasiadas categorías sin cohesión
- Difícil de mantener coherente
- Symlink `.knowledge` recién reparado (apuntaba a directorio inexistente)

## Plan según MEMORY.md
Reset con product discovery + build scaffold → skill de OpenClaw o docs site.

## Contenido actual
- `ai-agents/` — skills de agentes IA
- `backend-infra/` — backend, DB, APIs, Docker, Prisma, NestJS, MeLi
- `docs/` — documentación
- `frontend-ui/` — frontend y UI
- `fullstack/` — fullstack
- `growth/` — growth
- `languages-standards/` — lenguajes y estándares
- `product-building/` — construcción de producto
- `skill-authoring/` — authoring de skills
- `strategy-architecture/` — estrategia y arquitectura
- `tools-automation/` — herramientas y automatización
- `workflows/` — workflows

## Próximos pasos
1. Decidir si reset (recomendado) o mantener como está
2. Si reset: aplicar product-discovery + build-scaffold
3. Si mantener: al menos actualizar README y consolidar skills duplicadas
