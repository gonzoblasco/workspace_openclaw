# Lección 5: Gestión de Límites de Contexto de Canal
Clase: OpenClaw Use Cases

## Concepto Central
Controlar qué datos tiene permitido ver el agente en función de dónde ocurre la interacción. El objetivo es evitar la "contaminación cruzada" de datos, asegurando que el contexto de un usuario o de un hilo no se filtre a otro, protegiendo la privacidad y la precisión.

## Estrategias de Aislamiento de Contexto
1. **Silos de Identidad**:
   - Uso de `session_keys` vinculadas estrictamente a `user_id` y `channel_id`.
   - Aislamiento por `thread_ts` para hilos específicos, evitando que la charla de un hilo contamine la conversación raíz del canal.
2. **Ventanas de Inactividad (TTL)**:
   - Implementación de un `ttl_seconds` para resetear la memoria. Si el tiempo transcurrido desde el último mensaje supera el umbral, el contexto se limpia para evitar que el bot asuma que el estado actual es una continuación de algo ocurrido hace días.
3. **Filtros Deterministas vs. Semánticos**:
   - El filtrado por `channel_id` es obligatorio y prioritario (filtro hard).
   - La búsqueda semántica solo ocurre *dentro* del espacio ya filtrado por identidad, evitando fugas de información entre canales.

## Seguridad y Gobernanza
- **RBAC en Memoria**: Aplicación de Control de Acceso Basado en Roles sobre los fragmentos de contexto recuperados, filtrando datos sensibles según el rol del usuario solicitante.
- **Prevención de Contaminación**: Asegurar que la recuperación de contexto pasado no cruce fronteras de permisos, incluso si el contenido es semánticamente similar.

## Notas
La gestión del contexto es la barrera final de seguridad. Un error aquí no es solo una alucinación, sino una potencial brecha de privacidad. La regla de oro es: la identidad manda sobre la similitud.
