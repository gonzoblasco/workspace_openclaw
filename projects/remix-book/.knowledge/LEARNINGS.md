# LEARNINGS — Full Stack Web Development with Remix

## Acumulativo por capítulo

---

## Capítulo 1 — The Era of Full Stack Web Frameworks

### Conceptos clave

1. **Remix no es un React framework, es un full stack web framework.** La diferencia es fundamental: Remix abraza la web platform (HTML forms, URLs, cookies, HTTP headers, Web Fetch API) como ciudadanos de primera clase, no como afterthought.

2. **Filosofía Remix (Ryan Florence + Michael Jackson):**
   - Evitar sobre-abstracción — APIs como thin layer sobre web platform
   - Mirar hacia adelante y atrás: cutting-edge + battle-proven (HTTP2 streaming + HTML forms)
   - Progressive enhancement: primero sin JS, después mejorar con JS, después mover lógica al server
   - Cuidar el network tab y bundle size
   - "Center stack" — el framework es el centro que conecta cliente y servidor

3. **Mental model: Primitives, Conventions, Levers**
   - **Primitives:** funciones, hooks, componentes que el framework expone (thin abstraction de web APIs)
   - **Conventions:** file-based routing, route module exports (loader, action, default component)
   - **Levers:** opciones para optimizar según prioridad (TTFB vs CLS, spinners vs carga lenta). Remix te da el control, no decide por vos.

4. **Remix detrás de escena: tres responsabilidades**
   - **Compiler:** usa esbuild, produce server bundle + client bundle + asset manifest
   - **Router:** React Router v6 + @remix-run/router, client-side + server-side routing integrados
   - **Runtime:** adapters para distintos entornos (Node, Edge, etc.), traduce requests a Web Fetch API

5. **Lo que Remix NO es:**
   - No es un JavaScript server (corre sobre Node/Deno/etc.)
   - No es una base de datos ni ORM
   - No es un cloud provider
   - No es una librería de estilos
   - No es una bola de cristal

### Citas para recordar

> "Learning Remix means learning standard web APIs."
> "Remix aims to avoid over-abstraction."
> "Make everything work without JavaScript. Enhance the experience with JavaScript. Move as much business logic as possible to the server."

### Preguntas para explorar

- ¿Cómo se compara el approach de Remix con Next.js App Router (que también tiene server components, loaders, actions)?
- ¿Sigue vigente la filosofía después de la transición a React Router v7 / Remix v3?
- ¿Cómo se implementa progressive enhancement sin JS en la práctica con formularios?

### Conexiones con experiencia previa

- El concepto de "levers" es similar a la filosofía de OpenSpec: dar opciones explícitas, no esconder decisiones
- Progressive enhancement en 3 pasos resuena con el approach de accesibilidad: primero contenido funcional, después mejorar
- Co-location de server/client code es algo que React Server Components también busca, pero desde otro ángulo

---

## Capítulo 2 — Creating a New Remix App

### Conceptos clave

1. **create-remix CLI** — `npx create-remix@2` para v2, `npx create-remix@latest` para latest. Usa templates (básico = Remix App Server, o `--template` para custom como Express.js).

2. **Estructura de archivos:**
   - `app/entry.client.tsx` — entry point del cliente, hydrata React
   - `app/entry.server.tsx` — entry point del server, exporta `handleRequest`
   - `app/root.tsx` — root route module, renderiza HTML completo (`<html>`, `<head>`, `<body>`)
   - `app/routes/_index.tsx` — ruta default (path `/`)
   - `remix.config.js` — configuración de Remix
   - `public/build/` — client bundle con fingerprints (hashes en filenames para cache forever)
   - `build/` — server bundle

3. **Dos bundles, dos entornos:**
   - **Client bundle** → `public/build/`, expuesto al navegador
   - **Server bundle** → `build/`, usado por el adapter en runtime
   - Remix usa **tree shaking** para inferir qué código va a cada bundle
   - Convención explícita: `.server.ts` y `.client.ts` en filenames para forzar bundle
   - Los route modules NO pueden declararse como server/client porque contienen código de ambos

4. **Adapters:**
   - `@remix-run/express` — adapter para Express.js
   - `@remix-run/serve` — Remix App Server (Express.js interno, no expuesto)
   - El adapter traduce requests del server environment a Web Fetch API Request/Response

5. **Server.js (Express template):**
   - Importa `createRequestHandler` del adapter
   - Expone `public/build` como static (immutable, 1 año de cache)
   - Expone `public/` como static (1 hora de cache)
   - Forwardea todo lo demás a Remix HTTP handler

6. **Componentes built-in de root.tsx:**
   - `<Meta />` — meta tags desde exports de route modules
   - `<Links />` — links/stylesheet desde exports
   - `<Outlet />` — renderiza child route (en lugar de `{children}`)
   - `<ScrollRestoration />` — restaura scroll en navegación SPA
   - `<Scripts />` — inyecta todos los script tags. Si lo sacás, no hay JS en cliente
   - `<LiveReload />` — hot reload en desarrollo

7. **Troubleshooting process:**
   1. Leer error en terminal (source of truth)
   2. Localizar archivo que lanza el error (stack trace)
   3. Determinar si es build time o runtime
   4. Revisar Console y Network tabs del browser
   5. Limpiar build artifacts (`rm -rf build public/build .cache`)
   6. Googlear el issue
   7. Preguntar en Discord de Remix (con código/repo)

8. **Server-side rendering + browser APIs:**
   - `navigator`, `window`, etc. no existen en Node.js
   - Solución: envolver en `useEffect` (solo corre en cliente)
   - Pero ojo: si JS falla o crawler sin JS, el server value se queda
   - Remix ofrece utilities para manejar user data en server, evitando mismatches

### Citas para recordar

> "Remix is not a web server but an HTTP request handler that runs on a server environment."
> "Remix uses adapters to communicate with the underlying server."
> "The Scripts component might be one of the most fascinating components that Remix exposes."

### Preguntas para explorar

- ¿Cómo maneja Remix v3 (React Router v7) esta misma estructura? ¿Cambió algo?
- ¿Sigue siendo esbuild el bundler o migraron a otro?
- ¿Cómo se compara el approach de `.server.ts`/`.client.ts` con los server components de Next.js?
- ¿El troubleshooting process es transferible a cualquier framework SSR?

### Conexiones con experiencia previa

- El patrón de fingerprints en filenames para cache forever es el mismo que usa Vite
- El concepto de adapter es similar a cómo funcionan los adapters en Astro o SvelteKit
- El troubleshooting process es genérico y aplica a cualquier stack SSR

---

## Capítulo 3 — Deployment Targets, Adapters, and Stacks

### Conceptos clave

1. **Deployment targets — tabla de opciones:**
   - Server: Express.js, Remix App Server, Fly.io (Node.js, long-running, filesystem access)
   - Serverless: Architect (AWS), Netlify, Vercel (Node.js, sin filesystem, pay-per-use, escala automatico)
   - Edge: Cloudflare Pages/Workers, Deno, Fastly (workerd/Deno/Wasmtime, distribuido geograficamente, mas restrictivo)

2. **JavaScript runtimes:**
   - Node.js — el mas comun, rico ecosistema de paquetes
   - Deno — compatible con Node.js (con sintaxis especial), edge
   - Workers runtime (workerd) — edge, NO soporta Node.js std libs, npm packages solo si no usan Node.js
   - Bun — mencionado pero no profundizado

3. **Hosting environments — tres categorias:**
   - **Server:** long-running, filesystem access (depende), NO aisla requests, NO escala por defecto
   - **Serverless:** efimero (por request), sin filesystem, aisla requests, escala por defecto, connection pooling necesario
   - **Edge:** serverless + distribuido geograficamente (CDN), mas restrictivo, requiere DB distribuida

4. **Como elegir deployment target:**
   - Si usas Node.js libs → Node-based (Express.js, etc.)
   - Si tenes DB tradicional → server cerca de la DB
   - Si tenes serverless-first DB → serverless
   - Si tenes una sola DB en un datacenter → deploy cerca de la DB, no tiene sentido distribuir globalmente
   - Si queres blog con archivos → server con filesystem access
   - Si queres free tier → serverless providers

5. **Switching adapters — proceso de 9 pasos:**
   1. Abrir proyecto actual
   2. Crear nuevo proyecto con nuevo template
   3. Tener ambos side by side
   4. Mover `app/` del viejo al nuevo (renombrar el nuevo a `temp/`)
   5. Reemplazar `entry.client.tsx` con el de `temp/` (mergear custom code)
   6. Reemplazar `entry.server.tsx` con el de `temp/` (mergear custom code)
   7. Revisar archivos Remix-specific en raiz, mergear cambios
   8. Seguir README del nuevo proyecto
   9. Troubleshooting
   - Clave: cambiar imports del adapter (`@remix-run/node` → `@remix-run/cloudflare`, etc.)

6. **Remix Stacks (oficiales):**
   - **Blues** → Fly.io + PostgreSQL. Large-scale, distribucion regional
   - **Indie** → Express.js + SQLite. Small-scale, datos dinamicos
   - **Grunge** → Architect (AWS Lambda) + DynamoDB. Large-scale en AWS
   - Son opinionated starters, mas complejos que templates basicos

7. **Custom templates:**
   - Cualquier proyecto Remix valido puede ser template
   - Via GitHub, URL, path local, subfolder, tarball
   - `remix.init` script para setup steps custom

8. **BeeRich:**
   - Demo app del libro: personal finance management
   - Express.js template + Tailwind CSS
   - Componentes reusables en `app/components`
   - Ruta `/demo` para inspeccionar componentes

### Citas para recordar

> "Remix can run anywhere where JavaScript can be executed."
> "Picking a deployment target is more about avoiding unnecessary obstacles than anything else."
> "Scaling inevitably introduces complexity."
> "If you have one single database server in Oregon, then having your web app deployed all over the world won't bring you much benefit."

### Preguntas para explorar

- Como se compara la flexibilidad de Remix con Next.js en terminos de deployment targets?
- Sigue siendo relevante la distincion server/serverless/edge con las nuevas capacidades de cada plataforma?
- Como maneja Remix v3 (React Router v7) los adapters?
- Connection pooling en serverless — como se implementa en la practica con Prisma/Drizzle?

### Conexiones con experiencia previa

- El proceso de 9 pasos para switchear adapters es similar a migrar entre frameworks o runtimes en cualquier stack
- La tabla de traits (server vs serverless vs edge) es un buen framework de decision para cualquier proyecto fullstack
- El concepto de stacks opinionados (Blues/Indie/Grunge) es similar a create-stack-next: templates con decisiones pre-hechas

---

## Capitulo 4 — Routing in Remix

### Conceptos clave

1. **File-based routing (v2 convention):**
   - Cada archivo en `app/routes/` es un route module
   - `_index.tsx` = index route (default child de su parent)
   - `login.tsx` = ruta `/login`
   - `dashboard.expenses.tsx` = ruta `/dashboard/expenses` (dot delimiters = path segments)
   - `dashboard.expenses.$id.tsx` = ruta `/dashboard/expenses/:id` ($ = parametro)
   - `dashboard._index.tsx` = index route dentro de `/dashboard`
   - `_layout.tsx` = pathless layout route (no agrega segmento a la URL)
   - `_layout.login.tsx` = ruta `/login` dentro del pathless layout

2. **Route module exports:**
   - **UI route:** debe exportar default component (React component)
   - **Resource route:** NO exporta component, solo loader/action
   - Exports disponibles: `action`, `ErrorBoundary`, `handle`, `headers`, `links`, `loader`, `meta`, `shouldRevalidate`

3. **Nested routing:**
   - `root.tsx` es el parent route raiz, usa `<Outlet />` para child routes
   - Parent routes envuelven child routes con su layout
   - Layout routes son opcionales (se puede tener `/dashboard/expenses` sin `dashboard.tsx`)
   - Pathless layout routes (`_layout.tsx`) comparten layout sin agregar segmentos a la URL

4. **Loader functions:**
   - Se ejecutan server-side ANTES de renderizar el componente
   - Acceden a `params` para route parameters
   - Devuelven datos que el componente consume via `useLoaderData()`
   - Tipado: `useLoaderData<typeof loader>()` infiere el tipo del return
   - Pueden `throw new Response('Not found', { status: 404 })` para errores

5. **Link components:**
   - `<Link>` — navegacion client-side sin full page reload
   - `<NavLink>` — igual que Link pero con estado activo (clase condicional)
   - Remix fetchea solo los datos necesarios para los nuevos route modules
   - Fallback: si JS no carga, funciona como anchor tag normal (progressive enhancement)

6. **useNavigation hook:**
   - `navigation.state` = `'idle' | 'loading' | 'submitting'`
   - Permite mostrar loading indicators durante transiciones
   - Ejemplo: `motion-safe:animate-pulse` condicional en Tailwind
   - `PageTransitionProgressBar` para barra de progreso global

7. **Server-side redirects:**
   - `redirect('/path')` de `@remix-run/node` crea Response 302
   - Equivalente a `new Response(null, { status: 302, headers: { Location: '/path' } })`
   - Ideal para resource routes que redirigen (ej: `/dashboard` → `/dashboard/expenses`)

8. **Request/Response model:**
   - Remix sigue Web Fetch API standard
   - Helpers: `json()`, `redirect()`, `defer()`
   - Loaders devuelven Response objects

### Citas para recordar

> "Routing is possibly the most important concept to understand in Remix."
> "A UI route must export a React component as its default export."
> "By removing the browser's default behavior (the loading spinner), we robbed the user of a clear loading indication."

### Preguntas para explorar

- Como se compara el file-based routing de Remix v2 con el de Next.js App Router?
- Que pasa con los pathless layouts en Remix v3 / React Router v7?
- Como manejar nested layouts mas complejos (3+ niveles de profundidad)?
- El patron de resource routes para API endpoints — como escala?

### Conexiones con experiencia previa

- El concepto de pathless layout routes es similar a grupos de rutas en Next.js `(group)`
- Loader functions son conceptualmente similares a `getServerSideProps` o server components
- El patron de redirect desde loader es util para auth checks (redirigir a login si no autenticado)
- `useNavigation` es similar a `useTransition` de React pero especifico para navegacion

---

## Capitulo 5 — Fetching and Mutating Data

### Conceptos clave

1. **Loader functions — data fetching server-side:**
   - Se ejecutan SOLO en el server, antes de renderizar el componente
   - Deben devolver un Response object (o algo que Remix serialice a JSON)
   - `json()` helper crea Response con Content-Type application/json
   - Se ejecutan en paralelo entre rutas del mismo nivel
   - Remix NO re-ejecuta loaders de rutas ya activas (solo de las nuevas)

2. **useLoaderData con tipado inferido:**
   - `const data = useLoaderData<typeof loader>()` — infiere el tipo del return del loader
   - `JsonifyObject` wrapper porque los datos viajan serializados (Date → string, etc.)
   - Tambien disponibles: `useRouteLoaderData()` y `useMatches()` para acceder datos de otras rutas

3. **Route-level data fetching (no component-level):**
   - Remix promueve fetch en route modules, no en componentes
   - Evita fetch waterfalls (componente padre bloquea hijos mientras carga)
   - Los loaders se ejecutan en paralelo, aplanando la cascada
   - Se puede acceder a loader data desde cualquier componente via hooks

4. **Action functions — mutations server-side:**
   - Manejan POST, PUT, PATCH, DELETE (todo lo que no sea GET)
   - Reciben `request: Request` (Web Fetch API)
   - `request.formData()` parsea el body a FormData
   - Deben devolver Response o JSON (redirect es comun para POST)
   - Validacion de input OBLIGATORIA en server (no confiar en cliente)

5. **Progressive enhancement con formularios:**
   - **Sin JS:** HTML form nativo con `method="POST"` y `action` — full page reload
   - **Con JS:** Remix `<Form>` component — fetch request client-side, evita reload
   - Remix revalida TODOS los loaders activos despues de cada action
   - El `<Form>` component usa los mismos `name` attributes que HTML nativo

6. **Data revalidation:**
   - Despues de cada action, Remix re-fetchea todos los loaders activos
   - Evita stale data sin boilerplate
   - Similar a lo que pasaria con un full page reload post-submit

7. **Optimizacion de loaders:**
   - Queries independientes dentro de un mismo loader → `Promise.all()`
   - Mover toda la logica posible al server (menos JS en cliente, progressive enhancement)
   - Ordenar/filtrar datos en DB query, no en cliente

8. **Formularios con ?index:**
   - Cuando un index route y su parent comparten URL, `?index` en action desambigua
   - Sin `?index`, Remix asume que el action pertenece al parent route

### Citas para recordar

> "Move as much logic as possible to the server."
> "Remix promotes route-level data fetching."
> "Remix revalidates loader data after every action."
> "POST to mutate, GET to load."

### Preguntas para explorar

- Como se compara el data flow de Remix (loader + action + revalidation) con React Server Components + Server Actions?
- Que pasa con optimistic updates en este modelo? (lo cubre el capitulo 6)
- Como manejar validacion compleja con zod en actions?
- Como escalan las revalidaciones cuando hay muchos loaders activos?

### Conexiones con experiencia previa

- El patron loader + action + revalidation es similar a tRPC pero integrado en el framework
- `Promise.all()` en loaders es el mismo patron que en cualquier backend
- La validacion manual en actions es tediosa — zod resolveria eso
- El concepto de revalidation post-mutation es similar a React Query `invalidateQueries`

---

## Capitulo 6 — Enhancing the User Experience

### Conceptos clave

1. **Progressive enhancement en Remix:**
   - Disenar primero sin JS, despues mejorar con JS
   - Remix funciona sin JS por defecto (Link = anchor tag, Form = form nativo)
   - "Making it worse before making it better" — al sacar el full page reload, perdes indicadores nativos (loading spinner, reset de forms) y tenes que re-implementarlos con JS
   - Probar siempre en Slow 3G para detectar missing pending states

2. **Prefetching (levers):**
   - `prefetch="none"` (default) — no prefetchea
   - `prefetch="render"` — fetchea cuando el link se renderiza
   - `prefetch="viewport"` — fetchea cuando el link entra en viewport
   - `prefetch="intent"` — fetchea cuando el usuario hace hover/focus sobre el link
   - Remix conoce el asset manifest en cliente, sabe que loaders llamar
   - Prefetchea tanto datos (JSON) como bundles JS code-split
   - Tradeoff: velocidad vs datos innecesarios

3. **Action data (useActionData):**
   - Las action functions pueden devolver JSON (no solo redirect)
   - `useActionData<typeof action>()` accede al return de la action
   - Util para mostrar feedback post-mutation (success/error messages)
   - `actionData` puede ser `undefined` (si no hubo mutation en esa ruta)
   - Solo funciona en el mismo route module de la action

4. **Formularios de edicion:**
   - Usar `defaultValue` en lugar de `value` + onChange (menos boilerplate)
   - `key={expense.id}` en Form para que React reconstruya el form al cambiar de expense
   - Boton con `name="intent"` y `value="update"` para manejar multiple actions en una misma action function
   - `navigation.formAction` para verificar que el pending state corresponde a este form

5. **Concurrent mutations y useFetcher:**
   - El navigation object es GLOBAL — solo refleja la ULTIMA navegacion
   - Si hay multiples submissions concurrentes, se pierden los pending states de las anteriores
   - `useFetcher()` crea un estado de navegacion AISLADO
   - `fetcher.Form` no trigger page navigation (si JS esta disponible)
   - `fetcher.state` = `'idle' | 'loading' | 'submitting'` (aislado)
   - Sigue revalidando todos los loaders activos post-mutation
   - Sigue honrando redirects de action functions
   - Fallback a form nativo si JS no esta disponible
   - Cada item en una lista necesita su propio `useFetcher()`

6. **Eliminacion con referer header:**
   - Usar `request.headers.get('referer')` para saber desde donde se envio el form
   - Si el referer incluye el id del item eliminado, redirect a la lista
   - Si no, redirect al referer (el usuario se queda donde estaba)

### Citas para recordar

> "Progressive enhancement is a design philosophy that aims to create a baseline user experience for users on older devices and browsers."
> "Making it worse before making it better."
> "Remix provides levers to optimize the experience for what is important to us."
> "Remix tracks all ongoing submissions but only handles the last navigation."

### Preguntas para explorar

- Como se compara `useFetcher` con React Query `useMutation`?
- El patron de `intent` en botones para multiple actions — escala bien o se vuelve complejo?
- Como manejar optimistic updates con `useFetcher`?
- Prefetching en viewport vs intent — cual es mejor para mobile?

### Conexiones con experiencia previa

- `useFetcher` es similar a `useMutation` de React Query pero integrado en el framework
- El patron de `intent` en botones es similar a command pattern en backends
- `defaultValue` en lugar de `value` + onChange = menos boilerplate, mas HTML nativo
- El prefetching con `intent` es similar a lo que hace Next.js con `<Link prefetch={true}>`

---

## Capitulo 7 — Error Handling in Remix

### Conceptos clave

1. **Dos tipos de errores:**
   - **Unexpected errors:** network timeouts, bugs, errores imprevistos. Se manejan con ErrorBoundary.
   - **Expected failures (thrown responses):** 404, 401, etc. Lanzados a proposito con `throw new Response(...)`.
   - Remix maneja ambos de forma uniforme con ErrorBoundary.

2. **ErrorBoundary — componente de ruta:**
   - Se exporta como `ErrorBoundary` en cualquier route module
   - Reemplaza al route component cuando hay un error
   - NO tiene acceso a `useLoaderData` (loader data no disponible en error)
   - Usa `useRouteError()` para acceder al error
   - `isRouteErrorResponse()` para verificar si es un Response thrown
   - Burbujea hacia arriba hasta encontrar el ErrorBoundary mas cercano

3. **Nested error boundaries:**
   - Los errores burbujean hacia arriba en la jerarquia de rutas
   - El ErrorBoundary mas cercano atrapa el error
   - Permite contener errores: el layout padre sigue funcionando
   - Ejemplo: error en expense details → solo esa seccion muestra error, la lista de expenses sigue visible

4. **Root ErrorBoundary:**
   - En `root.tsx`, es el ultimo recurso
   - Maneja 404 global (rutas que no existen)
   - Debe ser simple (no depende de loaders)
   - Recomendado: crear componente `Document` reutilizable entre App y ErrorBoundary

5. **Thrown responses vs returned responses:**
   - `throw new Response('Not found', { status: 404 })` → atrapado por ErrorBoundary
   - `return json({ success: true })` → data normal, no trigger error boundary
   - `throw` es para expected failures que deben interrumpir el flujo
   - `return` es para data exitosa

6. **isRouteErrorResponse helper:**
   - Verifica si el error es un Response thrown
   - Permite acceder a `error.status`, `error.statusText`, `error.data`
   - Util para mensajes de error especificos por status code (401, 404, 500)

7. **Race condition en delete (cap 6):**
   - Eliminar varios items rapidamente crea race condition entre actions
   - La ultima response determina el redirect
   - Si se elimina el item actual del detalle, el redirect apunta a una pagina que ya no existe
   - Solucion: nested ErrorBoundary captura el 404 y muestra mensaje amigable

### Citas para recordar

> "Error boundaries don't have access to useLoaderData."
> "Remix lets us handle both unexpected and expected errors uniformly with the ErrorBoundary component."
> "Declarative error handling."
> "Tight error boundaries keep parts of our application functional if an unexpected error only affects a nested route module."

### Preguntas para explorar

- Como se compara el ErrorBoundary de Remix con los error boundaries de React 18?
- Se puede tener un ErrorBoundary por cada nivel de nested route?
- Como manejar errores de validacion en actions sin throw (return con errores)?
- El patron de `isRouteErrorResponse` escala bien para APIs?

### Conexiones con experiencia previa

- El concepto de error boundaries burbujeando hacia arriba es similar a try/catch pero a nivel de ruta
- `isRouteErrorResponse` es similar a `instanceof` checks en catch blocks
- El patron de `Document` reutilizable es similar a layout components en cualquier framework
- La race condition en delete es un problema real que cualquier app CRUD enfrenta

---

## Capitulo 8 — Session Management

### Conceptos clave

1. **Search parameters para estado de UI:**
   - `URLSearchParams` via `new URL(request.url).searchParams` en loaders
   - `useSearchParams()` hook en cliente
   - Form con `method="GET"` → form data se agrega como search params a la URL
   - `useSubmit()` para submit programatico (onChange, debounced)
   - `SearchInput` component con debounce de 500ms
   - Ventaja vs React state: persiste en reload, funciona con back/forward, cacheable

2. **Tres formas de submit en Remix:**
   - **`<Form>`** — interacciones principales, navegacion global
   - **`useSubmit()`** — submit programatico de un Form (onChange, etc.)
   - **`useFetcher()`** — mutations aisladas, sin navegacion global, concurrentes

3. **Cookies y sesiones:**
   - `createCookieSessionStorage()` — almacena session data en cookie
   - `getSession()` — obtiene session object del request
   - `commitSession()` — serializa session a cookie value
   - `destroySession()` — elimina session cookie
   - Config: `maxAge`, `httpOnly`, `secure`, `sameSite`, `secrets`
   - Solo almacenar `userId` (cookies tienen limite de KB)

4. **Flujo de auth:**
   - Register: `registerUser()` → `createUserSession(user)` → redirect a dashboard
   - Login: `loginUser()` → `createUserSession(user)` → redirect a dashboard
   - Logout: `destroySession()` → redirect a login
   - Logout es un resource route (solo action, sin componente)

5. **Proteccion de rutas:**
   - `requireUserId(request)` — throw redirect a /login si no hay session
   - Llamar en CADA loader y action de rutas protegidas
   - Loaders se ejecutan en paralelo → cada uno debe autenticarse individualmente
   - Filtrar queries por `userId` para evitar acceso a datos de otros usuarios

6. **Acceso global a user data:**
   - Loader en `root.tsx` devuelve `{ user }`
   - `useRouteLoaderData<typeof loader>('root')` para acceder desde cualquier componente
   - Hook custom `useUser()` en `app/modules/session.ts` (no .server!)
   - Deserializar fechas (createdAt, updatedAt) porque viajan como string

7. **Seguridad:**
   - `httpOnly: true` — cookie no accesible desde JS en cliente
   - `secrets` — firma criptografica de la cookie
   - `SESSION_SECRET` en .env
   - No exponer password en queries (select: { id: true, name: true })
   - Thrown redirect NO trigger ErrorBoundary (es un redirect, no un error)

### Citas para recordar

> "The URL is the perfect place to persist state that concerns only one or a few pages."
> "Remix's loader functions run in parallel for faster execution. However, their concurrent nature also dictates that we must secure each loader function."
> "Both loader and action functions are accessible over the internet and must be treated and secured like API endpoints."

### Preguntas para explorar

- Como se compara createCookieSessionStorage con JWT para auth?
- El patron de requireUserId en cada loader — escala bien o hay forma de centralizarlo?
- Como manejar roles y permisos ademas de auth basica?
- Search params vs React Context para estado de UI — cuando usar cual?

### Conexiones con experiencia previa

- El patron de requireUserId en cada loader es similar a middleware en Express/Fastify
- createCookieSessionStorage es similar a express-session pero integrado
- useRouteLoaderData('root') es similar a React Context pero con tipado inferido
- El debounced search con useSubmit es similar a patrones con React Query + input search

---

## Capitulo 10 — Working with File Uploads

### Conceptos clave

1. **Multipart form data:**
   - `encType="multipart/form-data"` en el Form para adjuntar archivos
   - `request.formData()` carga TODO en memoria (peligroso para archivos grandes)
   - `unstable_parseMultipartFormData(request, uploadHandler)` — stream, no carga en memoria
   - Solo cambiar a multipart cuando sea necesario (delete sigue siendo url-encoded)

2. **Remix upload handlers:**
   - `unstable_createFileUploadHandler()` — escribe archivos al filesystem
     - `directory`, `avoidFileConflicts`, `maxFileSize`
   - `unstable_createMemoryUploadHandler()` — maneja campos no-file en memoria
   - `unstable_composeUploadHandlers()` — compone handlers: primero intenta con file, fallback a memory
   - `UploadHandler` type — interfaz para custom handlers

3. **Streaming vs memory:**
   - Archivos grandes NO deben cargarse en memoria
   - Remix upload handlers procesan en chunks (streaming)
   - Default max file size: 30MB
   - Configurable via `maxFileSize` en `unstable_createFileUploadHandler`

4. **Splat routes (wildcard):**
   - `dashboard.expenses.$id.attachments.$.tsx` → `/dashboard/expenses/:id/attachments/*`
   - `params['*']` captura el resto del path
   - Util para servir archivos con paths variables

5. **Proteccion de archivos:**
   - NO guardar en `public/` (accesible publicamente)
   - Guardar en `attachments/` fuera de public
   - Resource route con `requireUserId()` + query por `id_userId`
   - `buildFileResponse()` con `Content-Disposition: attachment`
   - Limpiar archivos al eliminar expense/income

6. **Third-party storage:**
   - Para produccion: AWS S3, Cloudinary, etc.
   - Custom upload handler que streamea al provider
   - El handler devuelve la URL del archivo en el provider

### Citas para recordar

> "It is important to remember that files in the public folder are publicly accessible over the internet."
> "We must ensure that private user data is protected by authorization code."
> "Remix's upload handler primitives let you create custom handlers for different third-party services."

### Preguntas para explorar

- Como implementar un upload handler para S3?
- Como manejar progreso de upload en el cliente?
- Que pasa con archivos huerfanos si falla la transaccion de DB?
- Como limitar tipos de archivo permitidos?

### Conexiones con experiencia previa

- El patron de splat routes es similar a catch-all routes en Next.js `[...slug]`
- `unstable_composeUploadHandlers` es similar a middleware composition
- La proteccion de archivos via resource route es similar a patrones de presigned URLs en S3
- El cleanup de archivos al eliminar es similar a cascade deletes en DB

---

## Capitulo 11 — Optimistic UI

### Conceptos clave

1. **Que es Optimistic UI:**
   - Aplicar el cambio en UI ANTES de recibir confirmacion del server
   - Mejora la percepcion de velocidad (snappy)
   - Riesgo: rollbacks si la mutation falla
   - Tradeoff: complejidad vs percepcion de velocidad

2. **Cuando usar optimistic UI:**
   - Mutaciones con baja tasa de error
   - Acciones donde el feedback instantaneo importa (delete, likes, toggles)
   - NO cuando necesitas un id del server para acciones posteriores (create)
   - Evaluar: ?la complejidad extra vale la pena?

3. **Remix facilita optimistic UI porque:**
   - Revalidation automatica post-action (siempre sincronizado)
   - `navigation.formData` — acceso a datos del form en progreso
   - `fetcher.formData` — lo mismo pero para useFetcher
   - `fetcher.data` — action data del fetcher (para errores)
   - ErrorBoundary como fallback si algo sale mal
   - Sin estado React adicional (no useState, no useReducer)

4. **Patrones de optimistic UI en Remix:**
   - **Delete de lista:** `if (isSubmitting) return null` — oculta el item inmediatamente
   - **Upload de attachment:** mostrar Attachment component aunque el upload no haya terminado
   - **Remove de attachment:** ocultar Attachment y mostrar file input inmediatamente
   - **Update de form:** no deshabilitar el boton de submit (permite updates consecutivos)

5. **Manejo de errores en optimistic UI:**
   - `fetcher.data?.success === false` para detectar fallo
   - Estilo condicional (text-red-600) para senialar rollback
   - No mostrar ErrorBoundary si podemos dar feedback inline
   - El usuario puede reintentar inmediatamente

6. **navigation.formData vs fetcher.formData:**
   - `navigation.formData` — datos del form global (Form component)
   - `fetcher.formData` — datos del form aislado (useFetcher.Form)
   - Ambos contienen los valores del form en progreso
   - `undefined` si no hay submission activa

### Citas para recordar

> "Optimistic UI is a pattern that's used to provide instant feedback to users while waiting for an execution to resolve."
> "Remix automatically updates loader data after a mutation, keeping the client and server in sync."
> "Remix's primitives, such as useNavigation and useFetcher, allow us to read pending submission data without adding custom React states."

### Preguntas para explorar

- Como manejar optimistic updates con validacion server-side compleja?
- Que pasa si el usuario navega antes de que termine la mutation?
- Como implementar optimistic create cuando necesitas el id del server?
- El patron de `if (isSubmitting) return null` — que pasa con lectores de pantalla?

### Conexiones con experiencia previa

- El patron de optimistic UI en Remix es similar a React Query `onMutate` + `onError` rollback
- `navigation.formData` es similar a `useFormState` pero del framework
- La revalidation automatica elimina la necesidad de `invalidateQueries` manual
- El patron de ocultar items en delete es similar a patrones con `useOptimistic` hook de React 19

---

## Capitulo 12 — Caching Strategies

### Conceptos clave

1. **Headers route module API:**
   - `headers` export en cualquier route module
   - Se ejecuta SOLO en el server, despues de todos los loaders
   - Recibe: `parentsHeaders`, `errorHeaders`, `actionHeaders`, `loaderHeaders`
   - Remix usa el headers export MAS PROFUNDO disponible
   - Permite mergear headers de padres e hijos

2. **Cache-Control directives:**
   - `public` — puede cachearse en shared caches (CDN, proxies)
   - `private` — solo en cache del browser (no CDN)
   - `max-age=<seconds>` — tiempo maximo de cache
   - `no-cache` — debe revalidar con el server antes de usar cache
   - `no-store` — no cachear nada (ni siquiera para back/forward)
   - `immutable` — el contenido nunca cambia (solo con hash en filename)
   - `max-age=31536000, immutable` — 1 ano, tipico de assets con hash

3. **ETags (Entity Tags):**
   - `ETag` header con identificador unico del recurso
   - Cliente envia `If-None-Match` con el ETag previo
   - Server responde `304 Not Modified` si el recurso no cambio
   - Ventaja: permite auth check en el server antes de decidir si servir cache
   - Desventaja: igual hay roundtrip al server (solo se ahorra el body)

4. **Estrategias de caching:**
   - **Publicas (sin auth):** `public, max-age=3600` — CDN, 1 hora
   - **Privadas (con auth):** `no-cache, private` — siempre revalidar
   - **Assets estaticos:** `public, max-age=31536000, immutable` — Remix lo hace automatico
   - **Archivos de usuario:** `private, max-age=31536000, immutable` + ETag
   - **Sin cache:** `no-store` — datos sensibles o muy dinamicos

5. **Remix built-in caching:**
   - Todos los JS bundles tienen hash en filename
   - Cache-Control: `public, max-age=31536000, immutable`
   - Assets de links export tambien
   - Nunca hay dos archivos con mismo nombre y diferente contenido

6. **In-memory caching:**
   - Solo viable en long-running servers (no serverless/edge)
   - Alternativa: Redis para serverless/edge
   - Util cuando DB queries son lentas
   - Requiere logica de invalidacion manual
   - En BeeRich con SQLite no es necesario (queries de ms)

7. **Seguridad en caching:**
   - NO cachear datos de usuario en shared caches
   - ETag permite auth check antes de servir cache
   - `private` evita que CDN cachee datos sensibles
   - Cuidado con caches en computadoras publicas

### Citas para recordar

> "There are only two hard things in computer science: cache invalidation and naming things."
> "Caching effectiveness increases the closer the cache is to the users."
> "Remix provides a thin abstraction layer on top of the web platform and eases the usage of HTTP caching strategies."

### Preguntas para explorar

- Como implementar `stale-while-revalidate` en Remix?
- ETag vs Last-Modified — cual es mejor para que caso?
- Como integrar Redis como cache layer en Remix?
- Como testear caching en desarrollo local?

### Conexiones con experiencia previa

- El patron de headers function es similar a middleware para HTTP headers
- ETag + 304 es el mismo patron que en cualquier API REST
- Remix built-in caching (hash + immutable) es el mismo approach que Vite
- `no-cache` vs `no-store` es una distincion importante que muchos devs ignoran

---

## Capitulo 13 — Deferring Loader Data

### Conceptos clave

1. **Server-side data fetching vs client-side:**
   - Server-side: 2 roundtrips (HTML + assets) para LCP
   - Client-side SPA: 4 roundtrips (HTML + JS + fetch + assets)
   - Remix aplane el waterfall moviendo data fetching al server
   - Problema: un loader lento bloquea todo el render inicial

2. **defer function:**
   - `defer({ data, promise })` en lugar de `json()`
   - Acepta Promises sin resolver
   - Stream al cliente via HTTP streaming + React streaming
   - Requiere `renderToPipeableStream` en entry.server.tsx
   - No soportado en todos los runtimes (serverless tradicional no)

3. **Await component + Suspense:**
   - `<Await resolve={promise}>{(resolved) => <Component />}</Await>`
   - `<Suspense fallback="Loading...">` alrededor de Await
   - `errorElement` prop para errores del promise
   - `useDeferredValue` hook alternativo para acceder datos

4. **Optimizacion de orden de queries:**
   - Iniciar la query lenta PRIMERO (sin await)
   - Despues ejecutar queries rapidas con await
   - La query lenta arranca antes, aunque se resuelva despues

5. **Tradeoffs de defer:**
   - Pro: initial page load mas rapido
   - Contra: introduce loading spinners (pending UI)
   - Contra: layout shifts cuando se resuelve
   - Contra: crawlers pueden no ver el contenido diferido
   - Es un LEVER, no una solucion universal

6. **Requisitos tecnicos:**
   - HTTP streaming soportado por el runtime
   - `renderToPipeableStream` en entry.server.tsx
   - `npx remix reveal` para generar entry.server si no existe
   - PrismaPromise necesita `.then()` para convertirse a Promise nativa

### Citas para recordar

> "Remix provides levers so that we can optimize the user experience based on our app's requirements."
> "When considering defer, it is important to remember that deferred data loading may also degrade the user experience by adding a pending UI."
> "Remix flattens the request waterfall by moving the data fetching to the server."

### Preguntas para explorar

- Como afecta defer a SEO y crawlers?
- defer vs client-side fetch — cuando usar cual?
- Como testear streaming en desarrollo?
- Que pasa si el promise nunca se resuelve?

### Conexiones con experiencia previa

- El patron de defer + Await es similar a React Query `suspense: true`
- HTTP streaming es el mismo mecanismo que usa Next.js con streaming SSR
- El tradeoff de defer (velocidad vs pending UI) es similar a lazy loading de imagenes
- PrismaPromise → Promise con `.then()` es un detalle importante de Prisma

### Conceptos clave

1. **Meta tags:**
   - `meta` export en cualquier route module
   - `MetaFunction` tipada con `typeof loader`
   - Remix usa el meta export MAS CERCANO (nested overrides parent)
   - `Meta` component en `<head>` inyecta los meta tags
   - Meta function se ejecuta en server (SSR) y cliente
   - `data` puede ser `undefined` si hay error → siempre checkear con `?.`
   - `matches` array para acceder loader data de otras rutas activas
   - Tipado: `MetaFunction<typeof loader, { root: typeof rootLoader }>`

2. **Links (recursos externos):**
   - `links` export en cualquier route module
   - `LinksFunction` devuelve array de objetos link
   - `Links` component en `<head>` inyecta los links
   - Nested links se UNMOUNT al salir de la ruta (scoped stylesheets!)
   - Prefetching: Remix fetchea loader data + JS bundle primero, despues links en paralelo
   - Ejemplos: Google Fonts, stylesheets, preconnect

3. **Static assets:**
   - `public/` folder servido por el web server (Express.js en BeeRich)
   - Remix NO sirve static files — es responsabilidad del server
   - `express.static('public', { maxAge: '1h' })` en server.js
   - Ideal para: favicon, robots.txt, sitemap.xml
   - Imagenes: mejor usar CDN/servicio especializado (unpic-img)

4. **Resource routes para assets:**
   - Cualquier ruta sin componente = resource route
   - `loader()` puede devolver `new Response(content, { headers })`
   - `[.txt]` en filename escapa el punto para rutas como `/robots.txt`
   - Util para: generar PDFs, imagenes, texto, JSON dinamicamente
   - Permite auth checks antes de servir el asset

5. **Route-scoped stylesheets:**
   - Importar CSS en route module: `import styles from '~/styles/foo.css'`
   - Exportar via `links` function
   - Remix solo carga el CSS cuando la ruta esta activa
   - Se descarga al navegar fuera de la ruta

### Citas para recordar

> "Meta functions run on the client, the server, and on error."
> "Remix will always use the closest meta function export and ignore all other meta function exports higher up in the route hierarchy."
> "Remix is not a web server but an HTTP request handler."

### Preguntas para explorar

- Como se compara el meta system de Remix con Next.js `generateMetadata`?
- El patron de resource routes para assets — como escala para PDFs generados?
- Scoped stylesheets vs CSS Modules — cual es mejor para que caso?
- Como integrar unpic-img con Remix para optimizacion de imagenes?

### Conexiones con experiencia previa

- El patron de `matches` para acceder loader data de otras rutas es similar a React Context pero con tipado
- Resource routes son similares a API routes en Next.js
- Scoped stylesheets via links export es similar a CSS Modules pero declarativo
- El bracket notation `[.txt]` es similar a route groups en Next.js
