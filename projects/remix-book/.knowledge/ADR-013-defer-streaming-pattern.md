# ADR-013 — Defer + Await Streaming Pattern

**Fecha:** 2026-08-05
**Contexto:** Capitulo 13 de "Full Stack Web Development with Remix"
**Fuente:** Andre Landgraf / Remix team

## Decision

Adoptar el patron de `defer()` + `<Await>` + `<Suspense>` para streaming de loader data lenta o secundaria, como alternativa a bloquear el render inicial con queries lentas.

## Detalle

### El patron

```tsx
// Loader: devolver promise sin resolver
export async function loader({ params, request }: LoaderFunctionArgs) {
  const userId = await requireUserId(request);
  const { id } = params;

  // Iniciar query lenta PRIMERO (sin await)
  const slowData = db.slowQuery.findMany({ where: { id, userId } })
    .then((result) => result);

  // Query rapida con await (bloquea el render inicial)
  const fastData = await db.fastQuery.findUnique({ where: { id, userId } });
  if (!fastData) throw new Response('Not found', { status: 404 });

  return defer({ fastData, slowData });
}

// Componente: Suspense + Await
export default function Component() {
  const { fastData, slowData } = useLoaderData<typeof loader>();

  return (
    <>
      <FastComponent data={fastData} />
      <Suspense fallback={<Loading />}>
        <Await resolve={slowData} errorElement={<Error />}>
          {(resolved) => <SlowComponent data={resolved} />}
        </Await>
      </Suspense>
    </>
  );
}
```

### Requisitos

- HTTP streaming soportado por el runtime
- `renderToPipeableStream` en entry.server.tsx
- `npx remix reveal` si no existe entry.server.tsx
- PrismaPromise → Promise nativa con `.then()`

### Cuando usar defer

| Escenario | defer? |
|-----------|--------|
| Datos criticos above the fold | No (await) |
| Datos secundarios below the fold | Si |
| Queries lentas (>500ms) | Si |
| Datos que no afectan LCP | Si |
| Datos necesarios para render inicial | No |

### Tradeoffs

**Positivos:**
- Initial page load mas rapido
- LCP mejora (datos criticos llegan antes)
- El usuario ve contenido util mientras carga lo secundario

**Negativos:**
- Introduce pending UI (loading spinners)
- Layout shifts cuando se resuelve
- Crawlers pueden no ver contenido diferido
- No funciona en todos los runtimes

## Consecuencias

**Positivas:**
- Mejora perceived performance
- Control granular de que datos deferir
- Misma API de loader (solo cambiar json por defer)

**Negativas:**
- Complejidad adicional (Suspense boundaries)
- Tradeoff entre velocidad y pending UI
- No universal (depende del runtime)

## Notas

defer es un LEVER (ver ADR-001). No es la solucion default, sino una opcion para casos donde una query lenta es un bottleneck comprobado.
