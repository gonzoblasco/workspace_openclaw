# ADR-017 — Incremental Migration Strategies to Remix

**Fecha:** 2026-08-05
**Contexto:** Capitulo 17 de "Full Stack Web Development with Remix"
**Fuente:** Andre Landgraf / Remix team

## Decision

Adoptar la estrategia de migracion incremental a Remix usando side-by-side deployment con subdominio compartido y cookies, combinado con el patron BFF (Backend for Frontend) para integrar backends legacy.

## Detalle

### Estrategias por tipo de app

| App actual | Estrategia | Dificultad |
|---|---|---|
| Non-React | Side-by-side en subdominio, reimplementar componentes en React | Alta |
| React (otro framework) | Copiar componentes, adaptar a Remix, migrar pagina por pagina | Media |
| Client-only React (CRA/Vite) | Mover app dentro de Remix, refactorizar incrementalmente | Media-Baja |
| React Router v6 | Migrar directamente (mismos primitives) | Baja |

### Proceso generico

1. Crear nueva app Remix en subdominio (compartir cookies)
2. Reimplementar componentes reusables y layout
3. Desarrollar nuevas pages/flows en Remix
4. Migrar paginas existentes incrementalmente
5. Eventualmente descomisionar la app legacy

### BFF Pattern

Remix no requiere migrar el backend junto con el frontend:

```ts
// Loader puede llamar a downstream API en lugar de DB
export async function loader({ request }) {
  const userId = await requireUserSession(request);
  const response = await fetch(`https://api.legacy.com/expenses?userId=${userId}`);
  return response.json();
}
```

### Future flags

```js
// remix.config.js
module.exports = {
  future: {
    v2_errorBoundary: true,
    v2_meta: true,
    v2_routeConvention: true,
  },
};
```

- Permiten adoptar features de la nueva major version gradualmente
- `unstable_` = API en desarrollo, puede cambiar
- `v2_` = API estable, prepara para la proxima major

## Consecuencias

**Positivas:**
- Migracion sin冻结 de features
- Compartir cookies entre apps via subdominio
- BFF pattern permite migrar frontend sin tocar backend
- Future flags evitan upgrades traumaticos

**Negativas:**
- Codigo duplicado durante la migracion
- Complejidad de mantener dos apps en produccion
- BFF agrega latencia (request extra a downstream)
- Future flags requieren refactorizacion eventual

## Notas

Este ADR cierra la serie de 17 ADRs del libro. La estrategia de migracion mas recomendable es via React Router v6, ya que comparte el mismo equipo creador y los mismos primitives que Remix.
