# ADR-008 — Cookie Session Auth Pattern

**Fecha:** 2026-08-05
**Contexto:** Capitulo 8 de "Full Stack Web Development with Remix"
**Fuente:** Andre Landgraf / Remix team

## Decision

Adoptar el patron de autenticacion basado en `createCookieSessionStorage` con `requireUserId()` en cada loader y action protegido, y `useRouteLoaderData` para acceso global al usuario.

## Detalle

### Componentes del patron

1. **Session storage** (`session.server.ts`):
   - `createCookieSessionStorage({ cookie: { name, secrets, httpOnly, secure, sameSite, maxAge } })`
   - `getSession(request.headers.get('Cookie'))` — leer session del request
   - `commitSession(session)` — serializar a cookie value
   - `destroySession(session)` — eliminar cookie

2. **Helper functions** (`session.server.ts`):
   - `getUserSession(request)` — obtiene session object
   - `getUserId(request)` — retorna userId o null
   - `getUser(request)` — retorna user object (sin password) o null
   - `requireUserId(request)` — throw redirect a /login si no autenticado
   - `createUserSession(user)` — setea cookie con userId
   - `logout(request)` — destroy session + redirect a login

3. **Proteccion de rutas:**
   ```ts
   export async function loader({ request }: LoaderFunctionArgs) {
     const userId = await requireUserId(request);
     // ... query con userId filter
   }
   ```

4. **Acceso global al usuario:**
   - Loader en `root.tsx` devuelve `{ user }`
   - Hook `useUser()` via `useRouteLoaderData<typeof loader>('root')`
   - Archivo en `app/modules/session.ts` (sin .server! — se usa en cliente)

### Reglas de seguridad

1. Llamar `requireUserId()` en CADA loader y action de rutas protegidas
2. Filtrar TODAS las queries por `userId` (un usuario no debe ver datos de otro)
3. No exponer password en queries (`select: { id: true, name: true }`)
4. `httpOnly: true` para evitar XSS
5. `SESSION_SECRET` en .env, nunca hardcodeado
6. Thrown redirect NO necesita ErrorBoundary (es un redirect, no un error)

### Flujo completo

```
Register/Login:
  form → action() → registerUser/loginUser() → createUserSession(user)
  → redirect('/dashboard') con Set-Cookie header

Pagina protegida:
  request con Cookie header → loader() → requireUserId() → userId
  → query con where: { userId } → render

Logout:
  form POST a /logout → action() → logout(request) → destroySession()
  → redirect('/login') con Set-Cookie: maxAge=0
```

## Consecuencias

**Positivas:**
- Auth integrado en el framework (sin librerias externas)
- Cookie httpOnly + signed = seguro contra XSS
- Cada loader/action es un endpoint independiente y seguro
- Acceso global al usuario sin prop drilling ni Context

**Negativas:**
- requireUserId() en cada loader = repetitivo (no hay middleware global)
- Cookies tienen limite de tamaño (solo userId, no datos pesados)
- No hay refresh tokens ni token rotation out of the box
- La session expira con la cookie (30 dias por defecto)

## Notas

Este patron es especifico de Remix pero el concepto de cookie-session auth es universal. La principal diferencia con JWT es que la session se almacena del lado del server (en la cookie firmada) y no hay token que el cliente pueda inspeccionar.
