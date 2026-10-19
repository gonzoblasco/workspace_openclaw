# ADR-010: Server/Client File Convention - Naming como Contrato con el Tooling

**Status:** Accepted  
**Deciders:** Gonzo / Kanam  
**Fecha:** 2026-08-05  
**Actualizado:** 2026-10-15  
**Origen:** remix-book ADR-002

## Contexto

En proyectos fullstack con single codebase, el código compila en dos bundles (server y client). El tooling puede inferir qué código pertenece a cada uno via tree shaking, pero hay casos donde la inferencia no basta o se necesita claridad explícita.

**Alternativas consideradas y descartadas:**
1. **Dynamic imports condicionales** (`if (typeof window === 'undefined')`) - frágil, no evita que código llegue al bundle equivocado
2. **Separación física de carpetas** (`server/` y `client/`) - más rígido, rompe co-location
3. **Comentarios/marcadores** - no verificables por el compilador

## Decisión

Adoptar **naming convention como contrato explícito con el tooling** para separar código que debe ejecutarse exclusivamente en un entorno:

| Convención | Uso | Ejemplos |
|------------|-----|----------|
| **`.server.ts`** | Solo server bundle. Nunca llega al cliente. | Acceso a DB, API tokens, secrets, lógica de negocio sensible |
| **`.client.ts`** | Solo client bundle. Nunca se ejecuta en server. | Librerías que dependen de `window`, `navigator`, `document`, APIs del browser |

**Reglas:**
- **Route modules NO usan esta convención** - contienen código de ambos entornos
- El naming es **parte del contrato con el compilador**, no solo documentación
- El archivo vive cerca de donde se usa (co-location mantenida)

## Consecuencias

| Positivas | Negativas |
|-----------|-----------|
| **Seguridad**: código sensible nunca llega al cliente | No aplicable a route modules (otros mecanismos) |
| **Claridad**: cualquier dev sabe al instante dónde corre cada archivo | Posible duplicación si no se diseña bien separación de concerns |
| **Verificable por compilador** (error si importa `.server` en cliente) | Depende de soporte del framework (no portable a cualquier stack) |
| **Mantiene co-location** | |

## Stack Actual (2026-10)

| Framework | Soporte | Configuración |
|-----------|---------|---------------|
| **Vite + React** | Via `vite-plugin-server-client` o manual | `build.rollupOptions.output.manualChunks` |
| **Next.js (App Router)** | Nativo (`'use client'`, `'use server'`) | Convención oficial preferida sobre naming |
| **Remix** | Nativo (`.server.ts`, `.client.ts`) | Origen de esta convención |

> **Nota 2026-10:** En proyectos Next.js modernos, se prefiere la directiva `'use client'` / `'use server'` oficial. Esta convención (.server.ts/.client.ts) sigue vigente para proyectos Vite/Remix y como patrón conceptual: **naming como contrato verificable con tooling**.

## Ejemplo Práctico

```
features/auth/
├── auth.server.ts      // DB access, password hashing, session creation
├── auth.client.ts      // useAuth hook, client-side redirects
├── auth.types.ts       // Shared types (no suffix = shared)
└── auth.test.ts        // Tests import both as needed
```

## Referencias

- [ADR-009](./ADR-009-primitives-conventions-levers.md): Primitives/Conventions/Levers - esto es una **Convention** que actúa como **Lever** de seguridad
- [ADR-011](./ADR-011-nextjs-fullstack-platform.md): Next.js platform decision
- [ADR-020](./ADR-020-vite-default-bundler.md): Vite como bundler default

---

*Actualizado 2026-10-15: nota sobre Next.js App Router, tabla de stack actual*