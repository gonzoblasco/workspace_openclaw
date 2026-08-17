# ADR-027 - Server Components como Estandar de SSR (Next.js App Router)

**Status:** Accepted
**Date:** 2026-08-05
**Source:** React 18 Design Patterns - Chapter 12 (Server-Side Rendering)
**Scope:** Global - aplica a cualquier proyecto React con SSR

## Context

El libro presenta SSR de dos formas:

1. **Manual:** Express + webpack + Babel + `renderToString` + dehydration/hydration con `window.__DATA__`
2. **Next.js Pages Router:** `getInitialProps` para data fetching en SSR

Ambos enfoques son legacy. El manual requiere configurar webpack, Babel, Express, y manejar dehydration manualmente. Pages Router con `getInitialProps` esta deprecado desde Next.js 13 (2023).

## Decision

Usar **Next.js App Router con Server Components** como estandar para SSR en proyectos nuevos. Los Server Components permiten:

- Data fetching directo en el componente (async component)
- Zero JS enviado al cliente para componentes que solo renderizan en servidor
- Streaming de HTML progresivo
- Sin necesidad de hydration explicita

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
4. **Streaming:** el HTML se envia progresivamente, mejorando Time To First Byte
5. **Fetch nativo:** desde Node 18, no necesita `isomorphic-fetch`
6. **React 19:** `use()` + Suspense + Server Components son el futuro de React

## Consequence

- Proyectos nuevos con SSR usan Next.js App Router
- Proyectos existentes con Pages Router migran gradualmente (Next.js soporta ambos)
- SSR manual con Express solo se justifica para casos muy especificos (custom server, non-Next.js)
- `getInitialProps` se considera deuda tecnica

## Referencias

- Next.js App Router: https://nextjs.org/docs/app
- React Server Components: https://react.dev/reference/rsc/server-components
- Next.js Pages to App migration: https://nextjs.org/docs/app/building-your-application/upgrading/app-router-migration
- React 19 Server Components: https://react.dev/blog/2024/12/05/react-19
