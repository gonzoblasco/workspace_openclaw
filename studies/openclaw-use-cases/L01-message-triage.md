# Lección 1: Patrones de Triaje de Mensajes en Apps de Chat
Clase: OpenClaw Use Cases

## Concepto Central
El "sistema inmunológico" de OpenClaw cuando se expone a entornos de chat ruidosos. Evita el desperdicio de tokens y la generación de ruido asegurando que el agente reaccione a pensamientos completos, no a fragmentos.

## El Pipeline
1. **Normalización**: Conversión de payloads específicos de la plataforma (Slack, Discord, etc.) a un formato de `MensajeCanónico`.
2. **Filtrado Determinista**: Verificaciones rápidas (menciones, palabras clave) para descartar ruido irrelevante sin consumir tokens de LLM.
3. **Debounce (Ventana Deslizante)**: Espera una breve pausa en la escritura para agrupar mensajes fragmentados en un único contexto.
4. **Clasificación**: Uso de un LLM ligero (Tier 1) para decidir si el mensaje requiere la respuesta de un agente o es simple charla.

## Detalles Técnicos Clave
- **Techo de Debounce**: Un tiempo límite fijo (ej. 15s) para evitar "buffers eternos" de usuarios que no dejan de escribir.
- **Mapeo Canónico**: Los adjuntos de medios se mapean a un array genérico de `attachmentUrls` independientemente del origen.
- **Estrategia de Triaje**: Balance entre la *latencia percibida* (ventana corta) y la *coherencia del prompt* (ventana larga).

## Notas
Esencial para mantener la eficiencia en canales de alto tráfico. El objetivo es pasar de un "Bot Reactivo" a un "Asistente Consciente del Contexto".
