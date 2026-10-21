# Learnings - vite

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## 504 Outdated Optimize Dep: pre-bundlear los imports dinamicos en optimizeDeps.include

Cuando un import dinamico (import()) no esta en optimizeDeps.include de vite.config.ts, el scanner de deps no lo ve antes que el browser: Vite lo descubre en runtime, re-empaqueta TODO el cache de deps optimizados y el browser sigue pidiendo las URLs viejas -> cadena de 504 (Outdated Optimize Dep) en todos los entrypoints de cliente. Sintoma: errores 504 en consola del browser + en el log '[vite] (client) dependencies optimized: ... / optimized dependencies changed. reloading'. Fix: agregar el paquete al array optimizeDeps.include y borrar node_modules/.vite (quedan los hashes viejos). Caso bolt.diy: app/lib/runtime/projectFileValidation.ts importa prettier/standalone + prettier/plugins/{babel,typescript,estree} y llega al cliente via projectMcp -> Chat.client.tsx; app/utils/performance-monitor.ts importa web-vitals. Ojo con node-fetch: es node-only y su archivo (app/lib/fetch.ts) no tiene importadores, no va al bundle del browser. El propio upstream ya lo anticipa en el comentario de vite.config.ts: 'Pre-bundle them up front to avoid invalidating optimized URLs on the first page load (504 Outdated Optimize Dep)'. <!-- project: github.com/gonzoblasco/workspace_openclaw -->

---

