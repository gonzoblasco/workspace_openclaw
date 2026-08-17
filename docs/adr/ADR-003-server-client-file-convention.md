# ADR-003 - Server/Client file naming convention como contrato explicito con el tooling

**Status:** Aceptado
**Origen:** remix-book ADR-002
**Fecha:** 2026-08-05

## Contexto

En proyectos fullstack con un solo codebase, el codigo se compila en dos bundles (server y client). El tooling puede inferir que codigo pertenece a cada uno mediante tree shaking, pero hay casos donde la inferencia no es suficiente o donde se necesita claridad explicita.

Alternativas consideradas:
1. **Dynamic imports condicionales** (`if (typeof window === 'undefined')`) - fragil, no evita que el codigo llegue al bundle equivocado.
2. **Separacion fisica de carpetas** (`server/` y `client/`) - mas rigido, rompe co-location.
3. **Comentarios/marcadores** - no verificables por el compilador.

## Decision

Adoptar naming convention como contrato explicito con el tooling para separar codigo que debe ejecutarse exclusivamente en un entorno:

- **`.server.ts`** - el archivo solo se incluye en el server bundle. Nunca llega al cliente. Ideal para: acceso a DB, API tokens, secrets, logica de negocio sensible.
- **`.client.ts`** - el archivo solo se incluye en el client bundle. Nunca se ejecuta en el server. Ideal para: librerias que dependen de `window`, `navigator`, `document`, o APIs del browser.

**Reglas:**
- Los route modules NO pueden usar esta convencion porque contienen codigo de ambos entornos.
- El naming es parte del contrato con el compilador, no solo documentacion.

## Consecuencias

### Positivas
- Seguridad: codigo sensible nunca llega al cliente.
- Claridad: cualquier dev sabe al instante donde corre cada archivo.
- Verificable por el compilador (error si se importa `.server` en cliente).
- Mantiene co-location (el archivo vive cerca de donde se usa).

### Negativas
- No aplicable a route modules (hay que usar otros mecanismos).
- Puede llevar a duplicacion si no se disena bien la separacion de concerns.
- Depende del soporte del framework (no es portable a cualquier stack).

## Notas

Este patron se origino en Remix pero el concepto es transferible: **usar naming convention como contrato explicito con el tooling, no solo como documentacion**. Cualquier framework que compile a server + client bundles puede adoptar una convencion similar.
