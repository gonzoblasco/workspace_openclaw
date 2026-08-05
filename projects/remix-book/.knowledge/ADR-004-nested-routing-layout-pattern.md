# ADR-004 — Nested Routing with Layout Routes Pattern

**Fecha:** 2026-08-05
**Contexto:** Capitulo 4 de "Full Stack Web Development with Remix"
**Fuente:** Andre Landgraf / Remix team (Ryan Florence, Michael Jackson)

## Decision

Adoptar el patron de nested routing con layout routes como estrategia principal de organizacion de UI en aplicaciones fullstack, donde cada segmento de URL mapea a un nivel de composicion de componentes.

## Detalle

### El patron

En Remix, las rutas no son solo paginas — son una jerarquia de modulos que se componen via `<Outlet />`. Cada nivel de la URL puede tener:

1. **Parent layout route** — provee layout compartido para sus hijos. Usa `<Outlet />` para renderizar el child route activo.
2. **Index route** — default child, se renderiza cuando la URL coincide exactamente con el path del parent.
3. **Leaf route** — ruta sin hijos, renderiza contenido final.
4. **Pathless layout route** — layout route que NO agrega segmento a la URL. Util para compartir layout entre rutas que no comparten prefijo de path.

### Reglas

- Los parent routes envuelven child routes con su layout (header, nav, sidebar, etc.)
- Los child routes solo renderizan su contenido especifico — el layout viene del parent
- Los pathless layouts se declaran con prefijo `_` (ej: `_layout.tsx`)
- Los index routes se declaran con prefijo `_index` (ej: `dashboard._index.tsx`)
- Los parametros de ruta se declaran con `$` (ej: `$id.tsx`)

### Ventajas

- **Composicion natural:** cada pagina es la suma de sus route modules ancestors
- **DRY:** layouts compartidos sin duplicacion
- **URL-driven:** la estructura de archivos refleja la estructura de la app
- **Code splitting:** cada route module es un chunk separado
- **Data colocation:** cada loader vive con su ruta

### Cuando usar pathless layouts

- Cuando rutas en el mismo nivel necesitan el mismo layout pero no comparten prefijo de URL
- Ej: `/`, `/login`, `/signup` comparten header pero son paths distintos
- Solucion: `_layout.tsx` como parent, `_layout._index.tsx`, `_layout.login.tsx`, `_layout.signup.tsx`

### Cuando usar parent layout routes

- Cuando rutas comparten prefijo de URL y layout
- Ej: `/dashboard/expenses`, `/dashboard/income` comparten `/dashboard` y su nav
- Solucion: `dashboard.tsx` como parent, `dashboard.expenses.tsx` y `dashboard.income.tsx` como children

## Consecuencias

**Positivas:**
- Estructura predecible y escalable
- Cada ruta es autonoma (su loader, su componente, su error boundary)
- Facil de refactorizar (mover archivos = cambiar URLs)

**Negativas:**
- La estructura de archivos puede ser profunda (mucha indentacion visual)
- Pathless layouts requieren renombrar archivos existentes (cambiar `login.tsx` a `_layout.login.tsx`)
- No es intuitivo al principio para devs que vienen de React Router tradicional

## Notas

Este patron es especifico de Remix pero el concepto de nested routing con layouts es transferible a cualquier framework que soporte anidamiento de rutas (Next.js App Router, SvelteKit, etc.).
