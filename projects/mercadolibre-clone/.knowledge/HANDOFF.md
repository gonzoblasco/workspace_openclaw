# HANDOFF — MercadoLibre Clone v2

## Qué es

Clon funcional de MercadoLibre construido originalmente en 2 días con Claude Code + sistema Pre-Flight + 5 Gates (v1.0.0). 14 fases, 16 modelos de DB, 15 endpoints REST, auth con roles, PWA, dark mode.

**Repo:** https://github.com/gonzoblasco/mercadolibre-clone (privado)

## Objetivo de v2

Reconstruir el mismo concepto pero con el stack actual de OpenClaw + workflows del workspace + skills nativos. Demostrar que el nuevo sistema es más rápido, más ordenado y produce mejor código que la versión original.

## Stack para v2

- OpenClaw con workflows del workspace
- `create-stack` para scaffolding
- Workflows: task-execution, review-quality, session-lifecycle
- Skills: según lo que requiera cada fase
- Mismo target: Next.js + Supabase + TypeScript

## Lo que v1 demostró

- 14 fases en 2 días con Claude Code
- 16 modelos de DB, 15 endpoints, auth con roles
- Build limpio, 0 errores de TypeScript
- PWA, dark mode, responsive

## Lo que v2 debe demostrar

- Mismo alcance en menos tiempo
- Mejor calidad (reviews automáticos, security audit integrados)
- Mejor documentación (ADRs, HANDOFFs, CHANGELOG)
- Skills reutilizables que queden para futuros proyectos

## Estado

Pendiente — no iniciado.
