# Prompt - Agente A, U1 (Ajuste fino RAG)

> Copiar y pegar en el Agente A (VS Code). El workspace que tiene cargado es el mismo que el de Kanam, así que el proyecto está en `projects/soporteml-v4/`.

---

Estás trabajando en SoporteML V4, Fase 1 (pulido + integraciones). Sos el Agente A (VS Code). Tu rol en el pipeline de revisión cruzada: DESARROLLAR la U1 (ajuste fino del RAG). Sos el primero en la cadena, así que no tenés unidad anterior que revisar.

## Contexto del pipeline
SoporteML V4 usa el pipeline A/B de revisión cruzada (skill agent-orchestration-pipeline): el Agente A desarrolla unidades impares, el B pares, y cada uno revisa la del otro antes de avanzar. Vos sos el Agente A. Desarrollás U1, y el Agente B la va a revisar antes de desarrollar U2. Tu trabajo debe quedar impecable porque va a pasar por ojos frescos.

## El proyecto
Todo vive en `projects/soporteml-v4/` (el workspace que tenés cargado es el mismo que el mío). El código está en la raíz de `projects/soporteml-v4/` (monorepo pnpm: apps/api, apps/web, packages/db). El `.knowledge/` (BRIEF, PLAN, STATUS, HANDOFF, PIPELINE-AB) está en `projects/soporteml-v4/.knowledge/`. Leé el HANDOFF y el PIPELINE-AB primero para contexto completo.

## Estado actual del repo
- Repo git: `gonzoblasco/soporteml-v4` (independiente, no es subdirectorio del workspace).
- Último commit: inicial (migración del código desde v3 + .knowledge + mockups).
- 26 tests del API, todos verdes. Build OK. Pre-commit hook corre `pnpm lint && pnpm test`.

## Tu tarea - DESARROLLAR la U1: Ajuste fino del RAG

### Contexto del problema
La búsqueda semántica (RAG) usa `minScore` (default 0.2) en `searchChunks` (packages/db/src/repo/kb.ts). El problema detectado en la validación del 2026-08-17: cuando una consulta no tiene match real en la KB, el minScore bajo (0.2) devuelve el chunk "más cercano" aunque sea irrelevante. Ejemplo: "¿Aceptan cuotas?" (no hay artículo de precios) devolvió el artículo de garantía.

### Criterios de aceptación
1. Una consulta sin match real en la KB NO debe devolver un chunk irrelevante (debe devolver vacío o indicar que no hay contexto).
2. Las consultas con match real (envío, garantía, compatibilidad, stock) siguen devolviendo el chunk correcto.
3. El ajuste debe ser configurable (no hardcodear el minScore en un solo lugar) - idealmente exponerlo en company_settings (kb_similarity_threshold ya existe en el schema) o al menos en una constante clara.
4. Tests actualizados: agregar un test que verifique que una consulta sin match devuelve vacío, y que las consultas con match siguen funcionando.
5. Build + tests + lint verdes.

### Archivos relevantes
- `packages/db/src/repo/kb.ts` - `searchChunks` (minScore default 0.2)
- `apps/api/src/kb-service.ts` - `search` (usa searchChunks)
- `apps/api/src/ai/service.ts` - `suggest` (usa la KB como contexto)
- `packages/db/src/repo/settings.ts` - `kb_similarity_threshold` (ya existe en el schema, default 0.45)
- `apps/api/src/app.test.ts` - tests del API

### Sugerencia de enfoque (no obligatorio)
El schema ya tiene `kb_similarity_threshold` (default 0.45) en company_settings. Considerá usar ese valor como minScore en vez del hardcodeado 0.2. Pero validá que 0.45 no rompa los matches reales (la validación del 17 mostró que los matches reales tienen score alto, así que 0.45 debería estar bien). Si 0.45 es muy agresivo, ajustá a un valor que discrimine bien.

## Reglas
- Commit atómico + push. Un solo commit para U1.
- Commits en inglés, UI/prompts en español.
- No romper invariantes: multi-tenant, ADRs, identidad V4.
- Verificación obligatoria: build + tests + lint verdes antes de commitear (el pre-commit hook lo enforcea).
- Actualizar docs: al cerrar U1, marcar U1 como hecha en `PLAN.md` y `STATUS.md` (en `.knowledge/`), y commitear los docs al repo v4.

## Nota para el próximo agente (Agente B)
Dejá un mensaje claro de qué hiciste, qué ajustaste (el valor de minScore/threshold que elegiste y por qué), y qué necesita revisión del Agente B.
