# ADR-005 - Supabase como base de datos y BaaS

**Status:** Aceptado
**Origen:** sportcars ADR-005
**Fecha:** 2026-08-05

## Contexto

Proyectos web necesitan persistir datos (leads, conversaciones, knowledge base, eventos, cache). Se busca una solucion con minima operacion y buena integracion con el stack Next.js/Vercel.

## Decision

Usar Supabase:
- PostgreSQL para datos estructurados
- PostgREST para queries simples
- pgvector para embeddings (RAG, busqueda semantica)
- Auth opcional para paneles admin
- Edge Functions como respaldo para tareas que excedan limites de Vercel

## Consecuencias

### Positivas
- SQL relacional con JSONB flexible.
- pgvector nativo para RAG.
- Buena DX con TypeScript.
- Generous free tier; Pro a ~25 USD/mes si escala.

### Negativas
- Row Level Security requiere diseno cuidadoso.
- Concurrencia y limites del free tier en escala.

## Mitigaciones
- Usar service role desde servidor; nunca exponer al cliente.
- RLS bien configurado.
- Monitorear uso desde el dia 1.

## Alternativas consideradas
1. **PlanetScale (MySQL):** no tiene vector nativo.
2. **MongoDB Atlas:** mas flexible pero menos ideal para datos relacionales; costo vector separado.
3. **SQLite local/Fly:** mas operacion.

## Notas

Supabase es la opcion recomendada para proyectos que ya usan Next.js/Vercel y necesitan PostgreSQL + vector search sin operar infraestructura propia. Para proyectos que no necesitan vector search, evaluar alternativas mas ligeras.
