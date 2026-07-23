# ADR-005 — Supabase como base de datos y BaaS

## Estado
Aceptado

## Contexto
Necesitamos persistir leads, conversaciones, knowledge base, eventos y cache de inventario. Se busca una solución con mínima operación y buen integración con el stack Next.js/Vercel.

## Decisión
Usar Supabase:
- PostgreSQL para datos estructurados
- PostgREST para queries simples
- pgvector para embeddings del RAG
- Auth opcional para panel admin
- Edge Functions como respaldo

## Consecuencias

### Positivas
- SQL relacional con JSONB flexible.
- pgvector nativo para RAG.
- Buena DX con TypeScript.
- Generous free tier; Pro a ~25 USD/mes si escala.

### Negativas
- Row Level Security requiere diseño cuidadoso.
- Concurrencia y límites del free tier en escala.

## Mitigaciones
- Usar service role desde servidor; nunca exponer al cliente.
- RLS bien configurado.
- Monitorear uso desde el día 1.

## Alternativas consideradas
1. **PlanetScale (MySQL):** no tiene vector nativo. Rechazado.
2. **MongoDB Atlas:** más flexible pero menos ideal para datos relacionales; costo vector separado. Rechazado.
3. **SQLite local/Fly:** más operación. Rechazado.