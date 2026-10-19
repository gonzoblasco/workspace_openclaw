# ADR-034: Server Components como Estándar de SSR

**Estado:** Aceptado
**Fecha:** 2026-08-05
**Actualizado:** 2026-10-15
**Decisores:** Gonzo / Kanam
**Origen:** workspace (generalizado desde libro "React 18 Design Patterns")

## Contexto

El libro presenta SSR de dos formas:

1. **Manual:** Express + webpack + Babel + `renderToString` + dehydration/hydration con `window.__DATA__`
2. **Next.js Pages Router:** `getInitialProps` para data fetching en SSR

Ambos enfoques son legacy. El manual requiere configurar webpack, Babel, Express, y manejar dehydration manualmente. Pages Router con `getInitialProps` está deprecado desde Next.js 13 (2023).

## Decisión

Usar **Next.js App Router con Server Components** como estándar para SSR en proyectos nuevos. Los Server Components permiten:

- Data fetching directo en el componente (async component)
- Zero JS enviado al cliente para componentes que solo renderizan en servidor
- Streaming de HTML progresivo
- Sin necesidad de hydration explícita

### Ejemplo comparativo

**Libro (SSR manual con Express + webpack):**
```tsx
// server.tsx
app.get('/', (req, res) => {
  fetch('https://api.github.com/users/gaearon/gists')
    .then(response => response.json())
    .then(gists => {
      const body = renderToString(<App gists={gists} />)
      const html = template(body, gists)
      res.send(html)
    })
})
```

**Libro (Next.js Pages Router):**
```tsx
Page.getInitialProps = async () => {
  const res = await fetch('https://api.github.com/users/gaearon/gists')
  const gists = await res.json()
  return { gists }
}
```

**2026 (Next.js App Router):**
```tsx
// app/page.tsx - Server Component
async function Page() {
  const res = await fetch('https://api.github.com/users/gaearon/gists')
  const gists = await res.json()

  return (
    <ul>
      {gists.map(g => <li key={g.id}>{g.description}</li>)}
    </ul>
  )
}
```

## Rationale

1. **Simplicidad:** un componente async reemplaza Express route + renderToString + template + dehydration
2. **Zero-config:** Next.js maneja webpack, Babel, SSR, y routing
3. **Performance:** Server Components no agregan JS al bundle del cliente
4. **Streaming:** el HTML se envía progresivamente, mejorando Time To First Byte
5. **Fetch nativo:** desde Node 18, no necesita `isomorphic-fetch`
6. **React 19:** `use()` + Suspense + Server Components son el futuro de React

## Consecuencias

- Proyectos nuevos con SSR usan Next.js App Router
- Proyectos existentes con Pages Router migran gradualmente (Next.js soporta ambos)
- SSR manual con Express solo se justifica para casos muy específicos (custom server, non-Next.js)
- `getInitialProps` se considera deuda técnica

## Referencias

- Next.js App Router: https://nextjs.org/docs/app
- React Server Components: https://react.dev/reference/rsc/server-components
- Next.js Pages to App migration: https://nextjs.org/docs/app/building-your-application/upgrading/app-router-migration
- React 19 Server Components: https://react.dev/blog/2024/12/05/react-19
- [ADR-011](./ADR-011-nextjs-fullstack-platform.md): Next.js full-stack platform