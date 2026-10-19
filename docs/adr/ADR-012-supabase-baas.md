# ADR-012: Supabase como BaaS por Defecto

**Estado:** Aceptado
**Fecha:** 2026-08-05
**Actualizado:** 2026-10-15
**Decisores:** Gonzo / Kanam
**Origen:** workspace (extraído de evaluación sportcars, generalizado)

## Contexto

Proyectos web necesitan persistir datos (leads, conversaciones, knowledge base, eventos, cache, embeddings). Se busca una solución con mínima operación y buena integración con el stack Next.js/Vercel + TypeScript.

## Decisión

Usar **Supabase** como BaaS por defecto:
- PostgreSQL para datos estructurados
- PostgREST para queries simples
- pgvector para embeddings (RAG, búsqueda semántica)
- Auth opcional para paneles admin
- Edge Functions como respaldo para tareas que excedan límites de Vercel

## Consecuencias

### Positivas
- SQL relacional con JSONB flexible
- pgvector nativo para RAG
- Buena DX con TypeScript (tipos generados)
- Generous free tier; Pro ~25 USD/mes si escala

### Negativas
- Row Level Security requiere diseño cuidadoso
- Concurrencia y límites del free tier en escala

## Mitigaciones
- Usar service role desde servidor; nunca exponer al cliente
- RLS bien configurado desde día 1
- Monitorear uso desde el día 1

## Alternativas consideradas
1. **PlanetScale (MySQL):** no tiene vector nativo
2. **MongoDB Atlas:** más flexible pero menos ideal para datos relacionales; costo vector separado
3. **SQLite local / Fly.io / Neon:** más operación

## Alcance
Opción recomendada para proyectos que ya usan Next.js/Vercel y necesitan PostgreSQL + vector search sin operar infraestructura propia. Para proyectos que no necesitan vector search, evaluar alternativas más ligeras.

## Referencias
- [ADR-011](./ADR-011-nextjs-fullstack-platform.md): Plataforma full-stack
- [ADR-050](./ADR-050-memoria-sqlite-local-umbral-migracion.md): Memoria local vs migración a Postgres/Supabase
- [ADR-057](./ADR-057-data-layer-memory-db-refactor-integral.md): El data-layer de memory.db (fase 1: embeddings en BLOB float32)