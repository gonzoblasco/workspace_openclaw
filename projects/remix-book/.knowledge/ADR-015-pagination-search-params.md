# ADR-015 — Pagination with URL Search Parameters and Prisma

**Fecha:** 2026-08-05
**Contexto:** Capitulo 15 de "Full Stack Web Development with Remix"
**Fuente:** Andre Landgraf / Remix team

## Decision

Adoptar el patron de pagination usando URL search parameters (`?page=N`) combinado con Prisma `take`/`skip` y `$transaction` para count + data.

## Detalle

### Implementacion

```tsx
const PAGE_SIZE = 10;

// Loader
export async function loader({ request }: LoaderFunctionArgs) {
  const userId = await requireUserId(request);
  const url = new URL(request.url);
  const searchString = url.searchParams.get('q');
  const pageNumber = Number(url.searchParams.get('page')) || 1;

  const where: Prisma.ExpenseWhereInput = {
    userId,
    title: { contains: searchString || '' },
  };

  const [count, expenses] = await db.$transaction([
    db.expense.count({ where }),
    db.expense.findMany({
      orderBy: { createdAt: 'desc' },
      take: PAGE_SIZE,
      skip: (pageNumber - 1) * PAGE_SIZE,
      where,
    }),
  ]);

  return json({ count, expenses });
}

// Componente
const isOnFirstPage = pageNumber === 1;
const showPagination = count > PAGE_SIZE || !isOnFirstPage;

{showPagination && (
  <Form method="GET" action={location.pathname}>
    <input type="hidden" name="q" value={searchQuery} />
    <Button name="page" value={pageNumber - 1} disabled={isOnFirstPage}>
      Previous
    </Button>
    <Button name="page" value={pageNumber + 1}
      disabled={count <= pageNumber * PAGE_SIZE}>
      Next
    </Button>
  </Form>
)}
```

### Edge cases

- **Search + pagination:** hidden input para `q` persiste el filtro entre paginas
- **Reset de pagina:** cuando cambia search, setear `page=1` via hidden input
- **Pagina vacia post-delete:** siempre mostrar pagination si no estamos en page 1
- **Revalidation:** post-action, count se actualiza automaticamente

### Cuando usar offset vs cursor pagination

| Tipo | Cuando usar |
|---|---|
| Offset (`skip`/`take`) | Listas pequeñas, paginacion simple, el usuario puede saltar a cualquier pagina |
| Cursor (keyset) | Listas grandes, tiempo real, evitar saltos por inserciones/eliminaciones |

## Consecuencias

**Positivas:**
- URL es la source of truth (compartible, bookmarkeable)
- Funciona sin JS (GET form)
- Search + pagination combinados naturalmente
- Revalidation post-action mantiene count actualizado

**Negativas:**
- Offset pagination tiene problemas con inserciones/eliminaciones (saltos de pagina)
- No es ideal para listas muy grandes (OFFSET escanea rows)
- `$transaction` requiere soporte de la DB

## Notas

Este patron es generico y aplica a cualquier framework que use URL search params + Prisma. No es especifico de Remix.
