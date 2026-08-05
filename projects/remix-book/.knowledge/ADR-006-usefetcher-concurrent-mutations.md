# ADR-006 — useFetcher for Concurrent Mutations Pattern

**Fecha:** 2026-08-05
**Contexto:** Capitulo 6 de "Full Stack Web Development with Remix"
**Fuente:** Andre Landgraf / Remix team

## Decision

Adoptar `useFetcher` para mutations concurrentes (ej: eliminar multiples items de una lista) donde cada mutation necesita su propio estado de pending independiente del navigation global.

## Detalle

### El problema

Remix tiene un unico `navigation` object global. Cuando hay multiples submissions concurrentes:

1. La primera submission setea `navigation.state = 'submitting'`
2. La segunda submission CANCELA la primera y actualiza el navigation object
3. Se pierde el pending state de la primera submission
4. El usuario no ve feedback visual para la primera accion

Esto es intencional: Remix emula el comportamiento del browser, donde solo hay una navegacion a la vez.

### La solucion: useFetcher

`useFetcher()` crea un contexto de fetch AISLADO con su propio ciclo de vida:

```tsx
const fetcher = useFetcher();
// fetcher.state = 'idle' | 'loading' | 'submitting'
// fetcher.Form = componente Form aislado
// fetcher.submit() = submit programatico
// fetcher.load() = fetch de loader data
```

**Caracteristicas:**
- Estado de navegacion independiente por fetcher
- No trigger page navigation (si JS disponible)
- Sigue revalidando todos los loaders activos post-mutation
- Sigue honrando redirects de action functions
- Fallback a form nativo si JS no disponible

### Reglas de uso

1. Cada item en una lista necesita su propio `useFetcher()` — tipicamente creando un componente item que use el hook
2. Usar `fetcher.Form` en lugar de `<Form>` para mutations que no deben navegar
3. Verificar `fetcher.state !== 'idle'` para pending states
4. No usar para mutations que DEBEN navegar (ej: crear y redirect al detalle)

### Cuando usar Form vs useFetcher.Form

| Escenario | Usar |
|-----------|------|
| Crear + redirect al detalle | `<Form method=\"post\">` |
| Editar in-place | `<Form method=\"post\">` |
| Eliminar desde lista | `useFetcher().Form` |
| Like / votar / toggle | `useFetcher().Form` |
| Busqueda con resultados | `useFetcher().load()` |
| Cualquier mutation sin navegacion | `useFetcher()` |

## Consecuencias

**Positivas:**
- Permite UI con mutations concurrentes (eliminar varios items, likes, etc.)
- Cada mutation tiene su propio pending state
- Sigue aprovechando revalidation automatica
- Sigue funcionando sin JS (fallback a form nativo)

**Negativas:**
- Cada item necesita su propio fetcher = mas componentes
- No reemplaza al navigation global para mutations que deben navegar
- Puede ser confuso al principio (dos mecanismos de form submission)

## Notas

Este patron es similar a `useMutation` de React Query pero integrado en el framework y con progressive enhancement out of the box.
