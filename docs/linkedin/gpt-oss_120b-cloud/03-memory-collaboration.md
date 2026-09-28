# Kanam OS: Memoria compartida y RAG entre agentes

**Hook**
> "Una IA sin memoria es como un equipo sin notas de reunión."

## Por qué la memoria es esencial
- Cada agente necesita contexto histórico (historias de usuario, decisiones ADR, resultados de pruebas).
- OpenClaw guarda esa información en la **memory vault** (`MEMORY.md`, `memory.db`).

## Herramientas de memoria (ADR-073)
- `memory_search` - búsqueda semántica en todo el corpus (diarios, ADRs, notas).
- `wiki_get` / `wiki_apply` - acceden y actualizan la *wiki-vault* para datos estructurados y referencias.
- `sessions_history` - lee el historial de una sesión cuando se necesita reproducir un flujo.

## RAG (Retrieval-Augmented Generation)
1. **Agente MIND** consulta la vault con `memory_search` para obtener datos relevantes.
2. El modelo recibe ese contexto como *system prompt* y genera la respuesta.
3. Resultado enviado a **CORE** para registro y a **DEV** para posible código.

## Caso de uso práctico
- **Solicitud:** “¿Cuál es la política de pagos para Argentina?”
- **Flujo:**
  1. *MIND* busca `ADR-042` en la vault.
  2. Recupera el fragmento "Mercado Pago SIEMPRE, NUNCA Stripe".
  3. Devuelve texto a *CORE* que lo incluye en la respuesta final.

## Buenas prácticas
- Mantener la vault actualizada (usar `wiki_apply` para corregir errores).
- Evitar consultas que devuelvan demasiado texto; limitar `maxResults` y `minScore`.
- Registrar cada búsqueda importante en el **daily log** para auditoría.

---
**CTA**: En el próximo post veremos cómo estructurar pipelines automáticos con `automations` y triggers entre agentes.
