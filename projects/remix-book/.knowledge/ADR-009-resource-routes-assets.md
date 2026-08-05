# ADR-009 — Resource Routes for Dynamic Assets

**Fecha:** 2026-08-05
**Contexto:** Capitulo 9 de "Full Stack Web Development with Remix"
**Fuente:** Andre Landgraf / Remix team

## Decision

Adoptar resource routes (rutas sin componente, solo loader) para servir assets que requieren logica del lado del server (auth, generacion dinamica, etc.), y el `public/` folder para assets puramente estaticos.

## Detalle

### Cuando usar public/ folder

- Assets completamente estaticos (favicon, robots.txt, sitemap.xml)
- Archivos que no cambian entre requests
- No requieren autenticacion ni logica server-side
- Se sirven directamente por el web server (Express, etc.)

### Cuando usar resource routes

- Assets que requieren autenticacion (ej: archivos privados)
- Assets generados dinamicamente (PDF, imagenes, texto)
- Assets cuyo contenido depende del request (user-specific)
- Cualquier respuesta HTTP que no sea HTML

### Implementacion

```tsx
// routes/robots[.txt].tsx
const textContent = `User-agent: *
Disallow: /dashboard/
Allow: /login
Allow: /signup
Allow: /$`;

export function loader() {
  return new Response(textContent, {
    headers: { 'Content-Type': 'text/plain' },
  });
}
```

### Bracket notation

Los corchetes `[.txt]` en el filename escapan caracteres especiales:
- `robots[.txt].tsx` → ruta `/robots.txt`
- `sitemap[.xml].tsx` → ruta `/sitemap.xml`
- `image[$id].tsx` → ruta `/image/:id`

### Ventajas sobre public/ folder

- Puedes hacer auth checks antes de servir
- Puedes generar contenido dinamicamente
- El asset vive en el mismo codebase que el resto de la app
- Tipado y testing como cualquier otra ruta

## Consecuencias

**Positivas:**
- Assets protegidos detras de autenticacion
- Generacion dinamica sin infraestructura adicional
- Co-location con el resto del codigo

**Negativas:**
- Mas lento que servir desde public/ (pasa por el runtime de Remix)
- No aprovecha caching del web server para assets estaticos
- Mayor consumo de recursos del server

## Notas

Para assets estaticos sin logica, siempre preferir `public/` folder. Resource routes son para cuando necesitas control server-side sobre el asset.
