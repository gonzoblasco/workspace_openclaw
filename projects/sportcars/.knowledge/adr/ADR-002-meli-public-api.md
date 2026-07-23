# ADR-002 — Consumir inventario de Mercado Libre vía API pública

## Estado
Aceptado

## Contexto
Sport Cars publica sus vehículos (usados y posiblemente 0km) directamente en Mercado Libre. Esas publicaciones luego viajan a Pilot CRM. Para el sitio web necesitamos mostrar inventario real sin duplicar el trabajo de carga.

## Decisión
Consumir el inventario desde la API pública de búsqueda de Mercado Libre:
- `GET /sites/MLA/search?nickname={nickname}`
- `GET /sites/MLA/search?seller_id={seller_id}`

Ambos endpoints son públicos, no requieren autenticación del seller, y devuelven listings activos.

## Consecuencias

### Positivas
- Stock real sin integración privada.
- No dependemos de credenciales de MeLi.
- Fotos, precios y specs se sincronizan automáticamente cuando Sport Cars actualiza MeLi.

### Negativas
- Mercado Libre puede aplicar rate limiting.
- La estructura de atributos puede variar.
- No tenemos control sobre qué publicaciones aparecen (todo lo activo del seller).

## Mitigaciones
- Cache local en Supabase (`vehicles`) con revalidación cada 15-30 minutos.
- Fallback a contenido estático si MeLi falla.
- Mapeo flexible de atributos de MeLi a nuestro schema.

## Alternativas consideradas
1. **API privada de seller (`/users/{user_id}/items/search`):** requiere access token del seller. Rechazada porque no sabemos si Sport Cars nos daría acceso.
2. **Cargar inventario manualmente en Supabase:** rechazada porque duplica trabajo y se desactualiza rápido.
3. **Integración Pilot → nuestro sitio:** rechazada porque no tenemos acceso admin a Pilot.