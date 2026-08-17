# Kanam Forge — BRIEF

**Estado:** Activo (Fase 0)
**Última actualización:** 2026-08-17

## Qué es

Un Lovable self-hosted (fork de freestyle-sh/Adorable, MIT) que construye proyectos completos con el pipeline de Gonzo. No un generador de landings - un creador de proyectos completos estilo soporteml v1, pero con estándar superior.

**Sueño final:** Lovable cloud + AI multi-tenant, self-hosted, donde en vez del agente genérico corre el pipeline de Gonzo (stack opinado, memoria persistente, a11y integrada, multi-agente con review cruzado).

**MVP actual:** Local con Docker, uso personal. Sandbox Freestyle cloud reemplazado por Docker local.

## Decisiones tomadas (2026-08-17)

- **Nombre:** Kanam Forge (placeholder aprobado por Gonzo)
- **Imagen Docker:** A - Node + Next.js base + git (MVP rápido). Biome/create-stack en Fase 2.
- **Persistencia:** A - volumen local por proyecto. Doble git con `.knowledge/` como evolución.
- **Agente:** único en MVP. Multi-agente en Fase 3.
- **Stack:** fork Adorable (Next.js 16, React 19, assistant-ui, Vercel AI SDK). LLM OpenAI/Anthropic configurable.

## Stack técnico

- Fork Adorable: Next.js 16, React 19, assistant-ui, Vercel AI SDK
- LLM: OpenAI (gpt-5.2-codex / gpt-5-mini) o Anthropic (claude-sonnet) via `.env`
- Docker: container por proyecto (Node LTS + Next.js + git + ttyd)
- Orquestación: Docker CLI / dockerode (SDK Node)

## Referencias

- Repo original: https://github.com/freestyle-sh/Adorable (MIT)
- Plan completo: `projects/kanam-forge/.knowledge/PLAN.md` y artifact `aec3a3f9`
- Análisis de arquitectura en el artifact Kanam Forge
