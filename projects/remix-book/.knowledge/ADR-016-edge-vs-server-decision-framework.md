# ADR-016 — Edge vs Server Decision Framework

**Fecha:** 2026-08-05
**Contexto:** Capitulo 16 de "Full Stack Web Development with Remix"
**Fuente:** Andre Landgraf

## Decision

Adoptar el framework de decision para evaluar si un proyecto debe deployarse en edge runtime o server tradicional, basado en requerimientos de infraestructura, latencia, y complejidad.

## Detalle

### Ejes de decision

| Factor | Preferir Server | Preferir Edge |
|--------|-----------------|---------------|
| Filesystem | Necesitas leer/escribir archivos | Sin archivos locales |
| DB | SQLite, DB centralizada | DB distribuida (PlanetScale, Neon, D1) |
| Estado en memoria | Cache, sesiones en RAM | Redis externo |
| Long-running | SSE, WebSocket, background jobs | No necesario |
| Node.js libs | Dependes de paquetes Node.js | Paquetes web-standards-only |
| Latencia | Usuarios en una region | Usuarios globales |
| Cold start | Toleras 100-500ms | Necesitas <10ms |
| Complejidad | Prefieres simplicidad | Aceptas complejidad extra |

### Preguntas clave

1. **?Donde esta tu DB?** Si tenes una sola DB en un datacenter, deploya cerca de ahi. Edge no te va a ayudar si la DB esta lejos.
2. **?Usas SQLite?** SQLite requiere filesystem. Edge no tiene filesystem. Necesitas otra DB.
3. **?Necesitas SSE o WebSocket?** Edge runtimes no soportan long-running connections. Necesitas un server aparte.
4. **?Tus usuarios estan en una sola region?** Server tradicional en esa region es mas simple y probablemente igual de rapido.
5. **?Usas npm packages con Node.js APIs?** Edge runtimes (workerd) no soportan Node.js std libs.

### Cuando elegir edge

- Usuarios globalmente distribuidos
- Sin dependencia de filesystem
- Sin long-running connections
- DB distribuida o serverless-first
- Necesitas minimo cold start

### Cuando elegir server

- DB centralizada (SQLite, PostgreSQL en un datacenter)
- Filesystem (uploads, archivos locales)
- SSE, WebSocket, background jobs
- Dependencias Node.js
- Prefieres simplicidad sobre escalabilidad

### Alternativa: Fly.io (edge-like)

Fly.io ofrece server distribuido regionalmente SIN las limitaciones de edge puro:
- Filesystem access
- Long-running connections
- Node.js compatible
- DB cerca del server (podes deployar DB en la misma region)

## Consecuencias

**Positivas:**
- Framework de decision claro y portable
- Evita over-engineering (no asumir edge si no hace falta)
- Ayuda a documentar decisiones de infraestructura

**Negativas:**
- El panorama cambia rapido (nuevos runtimes, providers)
- Algunos providers borran la linea entre categorias

## Notas

Este ADR complementa a ADR-003 (Deployment Target Decision Framework). Mientras ADR-003 cubre la taxonomia de deployment targets, este ADR cubre la decision especifica entre edge y server.
