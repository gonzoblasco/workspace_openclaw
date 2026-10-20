# Learnings - docker

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## yarn add en el stage final de un Dockerfile rompe las versiones del build

En un Dockerfile multi-stage, si el stage final hace `yarn add <pkg>` SIN tener yarn.lock copiado (solo se copiaron public/, .next/static y .next/standalone), yarn re-resuelve TODO a la ultima version semver. En el caso de Vane eso subio `next` de 16.2.2 (la fijada en yarn.lock, con la que se construyo la app) a 16.4.2. La 16.4.2 exige .next/server/preview-props.json, un manifest que la 16.2.2 no genera -> ENOENT y crash loop del container. Arreglo: COPY --from=builder el paquete exacto (playwright/playwright-core) y llamar al CLI directo (node ./node_modules/playwright/cli.js install). Regla: en el stage final nunca agregar dependencias; copiar las que el builder ya instalo con el lockfile.

---

## Next standalone bindea a process.env.HOSTNAME, que en Docker es el ID del container

El server.js de Next.js standalone hace `process.env.HOSTNAME || '0.0.0.0'`. En Docker, la variable HOSTNAME viene seteada al ID del container, asi que Next bindeaba al hostname (http://<id>:3000) en vez de a 0.0.0.0. Sintoma: el healthcheck contra http://localhost:3000 falla con exit=7 (connection refused) aunque la app responda bien desde el host via el puerto mapeado. Arreglo: setear `HOSTNAME: '0.0.0.0'` en el environment del compose. Aplica a cualquier Next standalone en Docker.

---

