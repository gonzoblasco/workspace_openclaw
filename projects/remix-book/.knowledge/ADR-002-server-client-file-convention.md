# ADR-002 — Server/Client File Naming Convention (`.server.ts` / `.client.ts`)

**Fecha:** 2026-08-05
**Contexto:** Capítulo 2 de "Full Stack Web Development with Remix"
**Fuente:** Andre Landgraf / Remix team

## Decisión

Adoptar la convención de naming `.server.ts` y `.client.ts` para separar explícitamente código que debe ejecutarse exclusivamente en un entorno, en proyectos fullstack con un solo código base.

## Detalle

Remix compila el código en dos bundles (server y client) usando tree shaking para inferir qué código pertenece a cada uno. Sin embargo, hay casos donde la inferencia no es suficiente o donde se necesita claridad explícita:

- **`.server.ts`** — el archivo solo se incluye en el server bundle. Nunca llega al cliente. Ideal para: acceso a DB, API tokens, secrets, lógica de negocio sensible.
- **`.client.ts`** — el archivo solo se incluye en el client bundle. Nunca se ejecuta en el server. Ideal para: librerías que dependen de `window`, `navigator`, `document`, o APIs del browser.

**Reglas:**
- Los route modules (`app/routes/`) NO pueden usar esta convención porque contienen código de ambos entornos (loader/action en server, componente en cliente).
- Los entry points (`entry.server.tsx`, `entry.client.tsx`) ya siguen esta convención por defecto.
- El naming es parte del contrato con el compilador, no solo documentación.

## Alternativas consideradas

1. **Dynamic imports condicionales** — `if (typeof window === 'undefined')` — frágil, no evita que el código llegue al bundle equivocado.
2. **Separación física de carpetas** — `server/` y `client/` — más rígido, rompe co-location.
3. **Comentarios/marcadores** — no verificables por el compilador.

## Consecuencias

**Positivas:**
- Seguridad: código sensible nunca llega al cliente
- Claridad: cualquier dev sabe al instante dónde corre cada archivo
- Verificable por el compilador (error si se importa `.server` en cliente)
- Mantiene co-location (el archivo vive cerca de donde se usa)

**Negativas:**
- No aplicable a route modules (hay que usar otros mecanismos)
- Puede llevar a duplicación si no se diseña bien la separación de concerns
- Depende del soporte del framework (no es portable a cualquier stack)

## Notas

Este patrón es específico de Remix pero el concepto es transferible: usar naming convention como contrato explícito con el tooling, no solo como documentación.
