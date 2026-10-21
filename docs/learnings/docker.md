# Learnings - docker

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## yarn add en el stage final de un Dockerfile rompe las versiones del build

En un Dockerfile multi-stage, si el stage final hace `yarn add <pkg>` SIN tener yarn.lock copiado (solo se copiaron public/, .next/static y .next/standalone), yarn re-resuelve TODO a la ultima version semver. En el caso de Vane eso subio `next` de 16.2.2 (la fijada en yarn.lock, con la que se construyo la app) a 16.4.2. La 16.4.2 exige .next/server/preview-props.json, un manifest que la 16.2.2 no genera -> ENOENT y crash loop del container. Arreglo: COPY --from=builder el paquete exacto (playwright/playwright-core) y llamar al CLI directo (node ./node_modules/playwright/cli.js install). Regla: en el stage final nunca agregar dependencias; copiar las que el builder ya instalo con el lockfile.

---

## Next standalone bindea a process.env.HOSTNAME, que en Docker es el ID del container

El server.js de Next.js standalone hace `process.env.HOSTNAME || '0.0.0.0'`. En Docker, la variable HOSTNAME viene seteada al ID del container, asi que Next bindeaba al hostname (http://<id>:3000) en vez de a 0.0.0.0. Sintoma: el healthcheck contra http://localhost:3000 falla con exit=7 (connection refused) aunque la app responda bien desde el host via el puerto mapeado. Arreglo: setear `HOSTNAME: '0.0.0.0'` en el environment del compose. Aplica a cualquier Next standalone en Docker.

---

## bolt.diy: el SSR corre bajo workerd, no Node - Docker no alcanza al host

bolt.diy usa cloudflare({ viteEnvironment: { name: 'ssr' } }) en vite.config.ts: el runtime del servidor es el binario workerd, no Node. Dentro de un contenedor workerd NO logra salir a la red del gateway de Docker (error propio: 'Network connection lost', mientras Node dariá 'fetch failed'). Descartes: no es DNS (resuelve 192.168.65.254 + fdc4:f303:9324::254), no es IPv6 (ENETUNREACH, pero IPv4 cruda tampoco funciona), no es CORS (Ollama responde Access-Control-Allow-Origin OK). En macOS workerd alcanza 127.0.0.1 sin problema, asi que el modo nativo funciona. Ademas: la imagen prebuilt upstream (ghcr.io/stackblitz-labs/bolt.diy) muere con 'vite: not found', y el target production del Dockerfile tiene el mismo bug porque 'pnpm prune --prod' se lleva vite (que es devDependency) mientras el CMD arranca 'vite preview'. <!-- project: github.com/gonzoblasco/workspace_openclaw -->

---

## Onyx: para exponer solo Ollama Cloud, el criterio es remote_host, no el tag

En Onyx (onyx-dot-app/onyx), el provider LLM "Ollama" no distingue cloud de local: el endpoint /api/admin/llm/ollama/available-models devuelve TODO lo que expone el daemon, y el sufijo ":cloud" del tag NO es criterio suficiente (gpt-oss:120b-cloud y mistral-large-3:675b-cloud son cloud sin ese sufijo, y nemotron-3-nano:30b-cloud tambien). La fuente de verdad es el campo remote_host de GET /api/tags en el daemon. Para exponer solo cloud hay que filtrar por ese campo al construir model_configurations del provider. El filtro por sufijo deja pasar o deja fuera modelos segun como se nombren, y el error es silencioso: el chat sigue funcionando y uno cree que esta todo bien.

---

