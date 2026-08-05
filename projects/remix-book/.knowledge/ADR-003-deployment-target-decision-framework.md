# ADR-003 — Deployment Target Decision Framework

**Fecha:** 2026-08-05
**Contexto:** Capitulo 3 de "Full Stack Web Development with Remix"
**Fuente:** Andre Landgraf

## Decision

Adoptar el framework de decision basado en tres ejes (JavaScript runtime, hosting environment, hosting provider) para elegir deployment target en cualquier proyecto fullstack.

## Detalle

### Eje 1: JavaScript Runtime

| Runtime | Compatibilidad Node.js | Ideal para |
|---------|----------------------|------------|
| Node.js | Nativa | Paquetes npm, librerias existentes, ecosistema maduro |
| Deno | Parcial (import special) | Edge, proyectos nuevos sin dependencias Node.js |
| workerd | No | Cloudflare Workers, edge computing puro |
| Bun | Creciente | Proyectos nuevos, rendimiento |

**Pregunta clave:** ?El proyecto depende de paquetes npm que usan Node.js std libs? Si la respuesta es si, Node.js es la unica opcion viable.

### Eje 2: Hosting Environment

| Caracteristica | Server | Serverless | Edge |
|---------------|--------|------------|------|
| Long-running | Si | No | No |
| Filesystem access | Si (depende) | No | No |
| Aisla requests | No | Si | Si |
| Escala por defecto | No | Si | Si |
| Distribuido por defecto | No | No | Si |

**Pregunta clave:** ?Donde esta tu base de datos? Si tenes una sola DB en un datacenter, deploya cerca de ahi. No tiene sentido distribuir globalmente si el cuello de botella es la DB.

### Eje 3: Hosting Provider

Consideraciones:
- Ecosistema de servicios (AWS, Cloudflare, etc.)
- Free tiers y pricing
- Developer experience
- Servicios complementarios (auth, storage, CI/CD)

### Regla practica

> "Picking a deployment target is more about avoiding unnecessary obstacles than anything else."

1. Si usas Node.js libs → Node.js runtime
2. Si tenes DB tradicional → server cerca de la DB
3. Si tenes serverless-first DB → serverless
4. Si necesitas distribucion global → edge (o Fly.io para server distribuido)
5. Si trabajas con archivos → server con filesystem access
6. Si priorizas free tier → serverless providers

## Consecuencias

**Positivas:**
- Framework portable a cualquier proyecto fullstack
- Evita over-engineering (no asumir que necesitas edge/serverless si no)
- Ayuda a documentar decisiones de infraestructura en ADRs

**Negativas:**
- El panorama cambia rapido (nuevos runtimes, providers)
- Algunos providers borran la linea entre categorias (Fly.io: server distribuido)

## Notas

Este ADR complementa a ADR-001 (Primitives, Conventions, Levers) como framework de analisis para decisiones de infraestructura.
