# ADR-007 — Nested Error Boundaries Pattern

**Fecha:** 2026-08-05
**Contexto:** Capitulo 7 de "Full Stack Web Development with Remix"
**Fuente:** Andre Landgraf / Remix team

## Decision

Adoptar el patron de nested error boundaries con `ErrorBoundary` en route modules para manejar tanto errores inesperados como expected failures (thrown responses) de forma declarativa.

## Detalle

### El patron

Cada route module puede exportar un componente `ErrorBoundary`. Cuando ocurre un error (unexpected o thrown Response), Remix:

1. Busca el ErrorBoundary mas cercano en la jerarquia de rutas (desde la ruta actual hacia arriba)
2. Renderiza ese ErrorBoundary en lugar del route component
3. Si no encuentra ninguno, usa el default de Remix

### Reglas

1. **Root ErrorBoundary** (`root.tsx`) — ultimo recurso, maneja 404 global y errores no atrapados
2. **Nested ErrorBoundary** — atrapa errores de una seccion especifica, permite que el layout padre siga funcionando
3. **No usar useLoaderData** en ErrorBoundary — loader data no esta disponible cuando hay error
4. **Compartir layout** entre route component y ErrorBoundary via un componente `Layout` reutilizable
5. **Usar `isRouteErrorResponse`** para diferenciar entre thrown responses y errores inesperados

### Implementacion tipica

```tsx
// En cualquier route module
export function ErrorBoundary() {
  const error = useRouteError();
  const { id } = useParams();

  let heading = 'Something went wrong';
  let message = 'Apologies, something went wrong on our end.';

  if (isRouteErrorResponse(error) && error.status === 404) {
    heading = 'Not found';
    message = `The resource with id ${id} cannot be found.`;
  }

  return (
    <Layout>
      <H2>{heading}</H2>
      <p>{message}</p>
    </Layout>
  );
}
```

### Cuando usar throw vs return

| Escenario | Usar |
|-----------|------|
| Dato no encontrado (404) | `throw new Response('Not found', { status: 404 })` |
| No autorizado (401) | `throw new Response('Unauthorized', { status: 401 })` |
| Error de validacion | `return json({ errors })` (no throw) |
| Error inesperado | Dejar que React lo maneje (throw normal) |
| Success post-mutation | `return json({ success: true })` |

## Consecuencias

**Positivas:**
- Manejo declarativo de errores (no try/catch en cada loader)
- Errores contenidos: el resto de la app sigue funcionando
- Experiencia uniforme para errores de server y cliente
- Mensajes de error especificos por status code

**Negativas:**
- ErrorBoundary no puede acceder a loader data (limita lo que podes mostrar)
- Hay que mantener un componente `Layout` separado del route component
- La burbuja de errores puede ser confusa si hay muchos niveles de nesting

## Notas

Este patron es una extension del error boundary de React, adaptado para server-side rendering y route-level handling. Es especifico de Remix pero el concepto de nested error boundaries es transferible.
