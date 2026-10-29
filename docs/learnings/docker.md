# Learnings - docker

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## yarn add en el stage final de un Dockerfile rompe las versiones del build

En un Dockerfile multi-stage, si el stage final hace `yarn add <pkg>` SIN tener yarn.lock copiado (solo se copiaron public/, .next/static y .next/standalone), yarn re-resuelve TODO a la ultima version semver. En el caso de Vane eso subio `next` de 16.2.2 (la fijada en yarn.lock, con la que se construyo la app) a 16.4.2. La 16.4.2 exige .next/server/preview-props.json, un manifest que la 16.2.2 no genera -> ENOENT y crash loop del container. Arreglo: COPY --from=builder el paquete exacto (playwright/playwright-core) y llamar al CLI directo (node ./node_modules/playwright/cli.js install). Regla: en el stage final nunca agregar dependencias; copiar las que el builder ya instalo con el lockfile.

**Tags:** docker,yarn,nextjs,version-drift,playwright

---

## Next standalone bindea a process.env.HOSTNAME, que en Docker es el ID del container

El server.js de Next.js standalone hace `process.env.HOSTNAME || '0.0.0.0'`. En Docker, la variable HOSTNAME viene seteada al ID del container, asi que Next bindeaba al hostname (http://<id>:3000) en vez de a 0.0.0.0. Sintoma: el healthcheck contra http://localhost:3000 falla con exit=7 (connection refused) aunque la app responda bien desde el host via el puerto mapeado. Arreglo: setear `HOSTNAME: '0.0.0.0'` en el environment del compose. Aplica a cualquier Next standalone en Docker.

**Tags:** docker,nextjs,healthcheck,hostname,networking

---

## Onyx: para exponer solo Ollama Cloud, el criterio es remote_host, no el tag

En Onyx (onyx-dot-app/onyx), el provider LLM "Ollama" no distingue cloud de local: el endpoint /api/admin/llm/ollama/available-models devuelve TODO lo que expone el daemon, y el sufijo ":cloud" del tag NO es criterio suficiente (gpt-oss:120b-cloud y mistral-large-3:675b-cloud son cloud sin ese sufijo, y nemotron-3-nano:30b-cloud tambien). La fuente de verdad es el campo remote_host de GET /api/tags en el daemon. Para exponer solo cloud hay que filtrar por ese campo al construir model_configurations del provider. El filtro por sufijo deja pasar o deja fuera modelos segun como se nombren, y el error es silencioso: el chat sigue funcionando y uno cree que esta todo bien.

**Tags:** docker,ollama,cloud,onyx,provider

---

## El prompt del writer de Vane Filtraba el razonamiento del modelo a la respuesta final

Salida real de Vane (chat b140e38e, 2026-10-21) filtro el monologo interno del modelo dentro de la respuesta final: 'We need sentence citations. The last clause Chinese accidental-avoid', un fragmento en chino, y palabras pegadas ('bidireccionalconflictiva', 'laarchitecture', 'unainterpretacion', 'utilizando'): 12 ocurrencias. CAUSA: el writer prompt (src/lib/prompts/search/writer.ts) exigia 'every sentence must include at least one citation, even when inferred' SIN ninguna regla sobre que no puede contener la salida; bajo esa presion el modelo narra sus decisiones de citacion. FIX: seccion 'Output hygiene' (solo la respuesta final, un solo idioma, sin palabras pegadas, sin anglicismos cuando hay palabra espanola, corregir defectos en silencio, omitir en vez de inventar) + aclarar que la cita se pega al hecho y nunca es clausula propia. VERIFICADO por A/B con la misma query y el mismo historial: 12 leaks antes, 0 despues, 50 fuentes. REGLA GENERAL: cuando un modelo se filtra a si mismo, la causa suele estar en el prompt que lo presiona, no en el modelo.

**Tags:** ollama,vane,prompts,writer,leak,calidad-salida

---

## Un watcher que miente es peor que un watcher que no existe: el pgrep por ruta no matchea un worker con cwd

El 2026-10-28 el watcher de la cata de harnesses (scripts/watch-docker-cata.sh) dio un FALSO POSITIVO: aviso 'la cata ya no tiene corridas y Docker sigue abierto' mientras la cata estaba corriendo y sana. La causa: el patron pgrep -f 'cata-harnesses-2026-10-27/runner.py' nunca matchea, porque el runner se lanza como 'python runner.py' con cwd en el directorio de la cata, y pgrep -f matchea contra el argv, no contra el cwd. El pgrep devolvia vacio, el watcher concl 'no hay corridas' y disparaba. QUE HACER: (1) el patron del pgrep tiene que ser el NOMBRE del script ('runner\.py'), y la pertenencia se resuelve por el cwd del proceso con 'lsof -a -p <pid> -d cwd -Fn | grep -qx n<dir esperado>'. (2) Un pgrep que devuelve vacio NO prueba que el trabajo termino: prueba que el patron esta mal. (3) Probar el watcher en las DOS ramas: con el trabajo vivo (no debe disparar) y con un stub que simula Docker abierto y sin trabajo (debe disparar). (4) El aviso se repitio cada 7 minutos: un watcher sin cooldown es ruido, se agrego un sello de 1 hora que se borra cuando Docker se cierra o arranca la cata.

**Tags:** docker,verificacion,cata,watcher,pgrep,cwd,falso-positivo,cooldown

---

