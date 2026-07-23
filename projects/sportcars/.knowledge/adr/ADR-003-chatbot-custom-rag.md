# ADR-003 — Chatbot custom con LLM + RAG en lugar de Cliengo

## Estado
Aceptado

## Contexto
Sport Cars no usa Cliengo ni ningún chatbot actualmente. Gonzo quiere un chatbot propio para el sitio, con control total y sin depender de un SaaS de terceros. Además, se desconoce si todos los vehículos están cargados en Pilot.

## Decisión
Construir un chatbot custom usando:
- Vercel AI SDK para el frontend streaming
- LLM API (OpenAI / DeepSeek / Anthropic)
- RAG sobre base de conocimiento almacenada en Supabase (pgvector)
- Captura progresiva de datos del usuario
- Derivación a WhatsApp cuando corresponda

## Consecuencias

### Positivas
- Control total del comportamiento, tono y flujos.
- No costo de SaaS adicional por usuario/agente.
- Se integra nativamente con la captura de leads en Supabase.
- Diferenciador frente a competidores que solo tienen WhatsApp link.

### Negativas
- Mayor esfuerzo de desarrollo inicial.
- Costo variable de API de LLM.
- Requiere mantenimiento de la base de conocimiento.

## Mitigaciones
- Usar modelos económicos (gpt-4o-mini, DeepSeek-chat, claude-3-haiku).
- Limitar conversaciones a 10-15 mensajes por sesión.
- Prompt caching y embeddings eficientes.
- Base de conocimiento curada inicialmente con ayuda de la hermana.

## Alternativas consideradas
1. **Cliengo:** ya integrado con Pilot. Rechazado por preferencia explícita de Gonzo.
2. **Bot reglas simple (sin LLM):** más barato pero frágil y con mala experiencia. Rechazado.
3. **Chatbot de Pilot (módulo de IA/bots):** requiere acceso admin. Rechazado por misma razón que ADR-001.