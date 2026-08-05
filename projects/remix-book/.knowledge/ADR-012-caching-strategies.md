# ADR-012 — HTTP Caching Strategies with Headers Function and ETags

**Fecha:** 2026-08-05
**Contexto:** Capitulo 12 de "Full Stack Web Development with Remix"
**Fuente:** Andre Landgraf / Remix team

## Decision

Adoptar el patron de caching con `headers` export en route modules para controlar Cache-Control por ruta, y ETags para recursos que requieren auth check pero se benefician de evitar redownload del body.

## Detalle

### Estrategias por tipo de ruta

| Tipo de ruta | Cache-Control | Por que |
|---|---|---|
| Publicas (home, login, signup) | `public, max-age=3600` | Sin datos de usuario, CDN-friendly |
| Dashboard (autenticadas) | `no-cache, private` | Datos de usuario, siempre revalidar |
| Assets estaticos (JS, CSS) | `public, max-age=31536000, immutable` | Hash en filename, built-in de Remix |
| Archivos de usuario (attachments) | ETag + `private, max-age=31536000, immutable` | Auth check + cache en browser |

### Implementacion

```tsx
// _layout.tsx — rutas publicas
export const headers: HeadersFunction = () => {
  return { 'Cache-Control': 'public, max-age=3600' };
};

// dashboard.tsx — rutas privadas
export const headers: HeadersFunction = () => {
  return { 'Cache-Control': 'no-cache, private' };
};

// attachments — ETag
const headers = new Headers();
headers.set('ETag', expense.attachment);
if (request.headers.get('If-None-Match') === expense.attachment) {
  return new Response(null, { status: 304, headers });
}
return buildFileResponse(expense.attachment, headers);
```

### ETags: ventajas y desventajas

**Ventajas:**
- Permite auth check en el server antes de decidir si servir cache
- Evita redownload del body (304 Not Modified)
- El cliente puede usar el body cachead

**Desventajas:**
- Igual hay roundtrip al server (no evita la request)
- Requiere computar el ETag (costo adicional en server)
- No sirve si el recurso cambia frecuentemente

### Seguridad

- `private` evita que CDNs cacheen datos de usuario
- ETag + auth check previene acceso a archivos de otros usuarios
- `no-cache` permite back/forward navigation sin refetch (diferente de `no-store`)
- Cuidado con caches en computadoras publicas

## Consecuencias

**Positivas:**
- Control granular de caching por ruta
- ETags permiten auth + cache simultaneamente
- Remix built-in caching para assets (sin configuracion)
- Headers function permite mergear headers de padres

**Negativas:**
- ETags requieren roundtrip al server
- Cache invalidation sigue siendo compleja
- No todas las rutas se benefician del caching
- In-memory caching requiere logica manual

## Notas

Remix provee caching out of the box para assets estaticos. Para datos de usuario, la mejor estrategia es `no-cache, private` combinado con revalidation automatica post-action.
