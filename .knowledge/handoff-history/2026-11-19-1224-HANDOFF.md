# HANDOFF - workspace

**Fecha:** 2026-11-19 12:24 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-19). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-19.md`.

---
## Que se hizo en esta sesion

### 2026-11-19 12:24
Sesion larga de gobierno + ejecucion: roadmap de 5 tareas, cerrado entero.

1) Roadmap (`docs/challenges/roadmap-next-5.md`) con problemas previstos por tarea. Al final, tres de esas predicciones fueron falsas y los dos defectos mas caros no estaban en la lista.

2) Tarea 1 (pins): ya estaban puestos; solo se corrigio la descripcion del repo localdoc-agent, que insinuaba una submission al challenge que nunca existio.

3) Tarea 2 (rename agente-local-amigo -> localdoc-agent): un rename tiene ~7 capas (directorio, remoto, distribucion, lockfile, slug en estado, artefactos de entorno, prosa). Se habian hecho 4. El review encontro 5 defectos reales: pyproject y uv.lock con el nombre viejo, slug del programa del Planner distinto del nombre de archivo, "10 tests" repetido en dos archivos cuando habia 25, y el prompt del venv. Correccion de Gonzo: "Lucia" es una persona de ejemplo del enunciado, no un cliente; se marco como tal en el programa y el HANDOFF, y se verifico que ningun artefacto publico la presente como real.

4) Tarea 3 (privacidad): en localdoc-agent y field-notes se agrego un probe con `sys.addaudithook` que corre en subproceso, falla ante cualquier socket no-loopback y tiene CONTROL POSITIVO (se conecta a example.com a proposito; si el hook no lo ve, el test falla). Se agrego guard de bind (exit 2 en 0.0.0.0) y un wipe real: el boton "Delete everything" borraba el indice y dejaba `data/private/` con los originales, ademas de -wal/-shm. El probe se colgo y el cuelgue fue el hallazgo: con un modelo ausente es el demonio de Ollama el que va al registry, fuera del alcance de Python. Se documento el limite en ambos README. Tests: localdoc-agent 33, field-notes 14.

5) Tarea 4 (bilingue): tres ensayos reescritos al espanol (no traducidos), feed sin duplicados (19 -> 15 -> 16), indice con una fila por pieza, y guard nuevo: un par con una sola mitad ahora rompe el build (antes fallaba en silencio y P4.3 decia que estaba cubierto).

6) Tarea 5 (articulo): `the-review-that-invented-a-bug` / `la-revision-que-invento-un-bug`, publicados y verificados en vivo con hreflang completo. La primera linea casi lleva un dato falso: se iba a escribir "113 caracteres truncados" de memoria; medido contra git eran 19.889 en el commit (111 por debajo del cap) y 20.131 en el arbol (131 por encima).

7) Layout y cache: el indice mostraba dos filas por pieza ("En espanol" + "Tambien en espanol"); ahora es una fila con link a la otra version. Al migrar el CSS se rompio `.entries` (home) porque solo se migro `.index-list`: mismo grid, dos listas, una sola migrada. Gonzo seguia viendolo roto por `max-age=600` de Pages: se agrego versionado del CSS por hash de contenido.

8) Auditoria de performance y a11y: skip link existia pero no movia el foco (faltaba tabindex="-1"); chip sin affordance de link; favicon ausente generaba un 404 y bajaba Best Practices. Lighthouse en produccion: 99/100/100/100 (el punto que falta es el max-age=600 de Pages sobre las fuentes, no configurable).

### 2026-11-19 02:02
Verificacion definitiva del OAuth de gh en orgs de terceros: comentarios reales en shadcn-ui#11757 (7000227192) y meta/astryx#4652 (7000228285) publicados con exito. OAuth-first confirmado con evidencia, no solo probes.

### 2026-11-19 02:02
Verificacion definitiva del OAuth de gh en orgs de terceros: comentarios reales en shadcn-ui#11757 (7000227192) y meta/astryx#4652 (7000228285) publicados con exito, confirmando que OAuth-first es correcto y que el fine-grained no puede comentar en repos ajenos.

### 2026-11-19 00:59
Diagnostico y reparacion de credenciales de GitHub tras revocar Gonzo todos los PAT classic. (1) Se cayo una sola cosa: el MCP, con 401 Bad credentials sobre un github_pat_ revocado en secrets/github-token. El resto sano: gh CLI, SSH, push HTTPS via helper de gh en los 7 projects, admin en los 8 repos, ningun workflow con GH_PAT. (2) Verifique que el OAuth de gh sirve para el MCP (get_me OK) y reescribi ~/.openclaw/bin/github-mcp-launch para resolver el token dinamicamente, con fallo ruidoso en vez de 401 silencioso. (3) Limpieza medida a pedido de Gonzo: trash del token revocado, su backup y el launcher viejo; secrets/ quedo vacio y el slot del PAT sigue existiendo por contrato. (4) Gonzo provisiono un PAT fine-grained: 81 repos, push en los propios, pull en shadcn-ui, radix-ui, TanStack, meta (Actions/issues/pulls/contents/commits 200), gists y orgs OK. (5) Hallazgo importante: el fine-grained NO puede comentar en repos publicos ajenos (403 Resource not accessible en shadcn-ui#11757 y astryx#4652), mientras el OAuth de gh si pasa la autorizacion en esas 4 orgs; inverti la precedencia del launcher a OAuth-first con el PAT como fallback. Prueba usada: POST de comment con body vacio (422 = autorizado, 403 = bloqueado), sin efecto lateral. (6) Notifications: la API solo acepta classic PAT con scope notifications; en fine-grained no existe la casilla, queda afuera por decision.

### 2026-11-18 22:15
Cierre de la segunda parte de la sesion: infraestructura del MCP de GitHub y credenciales. (1) Se restauro el binario del MCP oficial github-mcp-server v2.2.0 (Darwin_arm64) en ~/.openclaw/bin/github-mcp via OPS, con dictamen APLICA CON CAMBIOS y limites duros respetados. Verifique la cadena de custodia por mi cuenta porque OPS reporto mal el checksum: el archivo oficial hashea el TARBALL (5e46b05b...), no el binario; tarball contra oficial OK, binario extraido contra instalado OK (11608433...). OPS habia comparado el hash del binario contra el archivo del tarball, que da distinto siempre. Funcional: 53 tools, get_me autentica, list_notifications responde. (2) Se registro el MCP como server del gateway (mcp.servers.github) via config.set, porque openclaw mcp set/add fallan con 'This operation requires exclusive offline state ownership' mientras el gateway corre. Token fuera del config: launcher ~/.openclaw/bin/github-mcp-launch (700) que lee el PAT del archivo 600 y lo exporta. (3) Bug propio encontrado y corregido: el binario necesita el subcomando 'stdio' en args; sin el imprime la ayuda y sale con exit 0, y el gateway lo veia como 'Connection closed'. Corregido con args=[stdio] y verificado con handshake real (starting server version=2.2.0, readOnly=false). (4) Hallazgo de seguridad: el token guardado no era el public_repo pedido sino un PAT con admin:enterprise, admin:org, delete_repo, workflow, user. Se reemplazo por un fine-grained github_pat_ que Gonzo paso por chat. Verificado: identidad gonzoblasco, lectura OK en meta/astryx y shadcn-ui/ui, wrapper OK. PERO la escritura FALLA: 'Resource not accessible by personal access token (addComment)'. Diagnostico: el fine-grained no tiene el repo en su allowlist con escritura (repository access en 'only select' o Issues en Read en vez de Read and write). No se puede distinguir de una aprobacion de org pendiente con el mensaje actual; el mensaje tipico de aprobacion de org es distinto. (5) Se cancelo el comentario de seguimiento en astryx#4652 por pedido de Gonzo; draft borrado, nada publicado. Pendiente critico: el PAT ancho (ghp_) sigue VIVO en la cuenta de GitHub aunque se borro la copia del disco, porque borrar el archivo no lo revoca. Hay que revocarlo en settings/tokens. Y el token vigente es de facto read-only hasta que se corrija su permiso de Issues.

Estado de los hilos al cierre: ariakit#4058 cerrado (fix en 0.4.43); astryx#7871 mergeado en v0.7.12; astryx#4690 abierto y en conflicto, sin comentar por decision; astryx#4652 abierto con nuestra medicion DOM publicada; shadcn#11757 abierto con nuestro comentario publicado.

## Estado actual

5/5 tareas del roadmap cerradas. a11y-portfolio desplegado y verificado: Lighthouse 99/100/100/100. localdoc-agent 33 tests, field-notes 14. Sindicacion a DEV.to pendiente: la clave existe en el store pero el proxy de egress del gateway esta deshabilitado (401), y el payload esta listo en docs/challenges/articles/.

### Estado previo (heredado)

MCP operativo OAuth-first verificado con 2 comentarios reales. PAT fallback. Notifications sin soporte en fine-grained.

### Estado previo (heredado)

MCP de GitHub operativo con OAuth-first verificado con comentarios reales en 2 orgs (shadcn, meta). PAT fine-grained como fallback. Notifications sigue sin soporte en fine-grained.

### Estado previo (heredado)

MCP de GitHub operativo con OAuth-first; PAT fine-grained guardado como fallback (600). Falta la prueba definitiva con un comentario real en una org de terceros.

### Estado previo (heredado)

MCP de GitHub operativo (binario + server registrado con args stdio). Credencial vigente fine-grained sin permiso de escritura; PAT ancho sin revocar.

### Estado previo (heredado)

dreams-rotate.py cubre los 8 diarios y la rotacion esta al dia (103 activas, 0 desfasadas). Tests 13/13. Commit aeae49319d pusheado, CI verde. Workspace limpio, main == origin/main.

### Estado previo (heredado)

Cuatro notificaciones revisadas; dos comentarios publicados (astryx#4652, shadcn#11757); PAT de escritura restaurado.

### Estado previo (heredado)

Render del libro en curso (chapters 1/17). Voz fijada en ADR-116: Chatterbox clonando assets/voces/baritono-jazz (100-104 Hz, 11.400 Hz, entona). Registro de voces por nombre operativo.

### Estado previo (heredado)

Revertido y limpio. Retirados: scripts/scripts-inventory.py, la clave scripts_inventory de settings, el bloque del pre-commit y las 3 lineas falsas del CHANGELOG. ADR-113 reescrito como Status: Rejected con el motivo tecnico y agregado al indice (check-adr-integrity OK, 70 ADRs). Sobrevive el inventario medido en tmp/scripts_inventory_raw.json. Errores propios durante la limpieza: se borro agents/kanam-planner/agents/ creyendo que era basura de esta sesion cuando contenia caesar3-clone-f2-f3.json trackeado; restaurado con git checkout y verificado.

### Estado previo (heredado)

ADR-114 aceptado; commit local sin push

### Estado previo (heredado)

El Descenso: bitacora cerrada en sus decisiones estructurales (Decision 0 y Decision 1 escritas y con escena). Cuatro fragmentos de prosa en docs/stories/el_descenso/borradores.md (1 original, 1b reescrito, 3 sirenas, 4 cocina). Sin manuscrito ni outline todavia. Audio profundo entregado.

v0.1. Cuatro skills ejecutables reales + surface-alignment-audit procedimental. Suites 60/60. audit-surface corre y emite report.html+json.

### Estado previo (heredado)

Conversacion de Medallia auditada y declarada borrable sin perdida (kit ya esta en repo, sin cron atado). Infjini/Disney: ABIERTO - fecha sin coordinar, sin contacto humano desde 26/10. Gonzo lo declaro 'cerrado' verbalmente; el tracker lo tiene abierto por su propio revert del 16/11. Tracker sin editar: falta decision explicita sobre marcarlo con nota de inactividad.

### Estado previo (heredado)

Research cerrado con fuentes; integracion NO ejecutada. Gateway sin provider google configurado (solo el perfil auth en modo api_key). Sin key creada, sin cambio de modelo primario, sin diff de config aplicado.

### Estado previo (heredado)

docs/claims/ operativo con 25 claims y gate en el pre-commit. settings con una sola clave de asignacion de modelos (model_by_agent), managed-blocks.py escribe en una y retire-aliases borra copias. ADR-090 documenta la correccion estructural. Tres CI en verde. Vault de memory-wiki sin uso, conservado como archivo.

### Estado previo (heredado)

Tres artefactos escritos y commiteados; esperando la respuesta de los socios.

### Estado previo (heredado)

Migración congelada en Fase 5 hasta el 2026-12-01 (quota Gemini Starter agotada; Ollama Pro activo hasta 2026-11-30). OpenClaw sigue siendo el entorno operativo maestro y Kanam sigue trabajando normal acá.

### Estado previo (heredado)

CV final entregado y enviado por Gonzo. Llamada con Agustín Bermúdez acordada para mañana 16/11.

### Estado previo (heredado)

Material listo, no enviado: falta el OK de Gonzo para mandar el mensaje y el CV.

### Estado previo (heredado)

Error de carga de la skill evidence-hunter resuelto; frontmatter válido.

### Estado previo (heredado)

Modulo 0 dado y verificado. Research de Vane auditado contra fuente: dos papers leidos, el resto marcado. Modulo 1 no empezado. Sin linea base grabada todavia.

### Estado previo (heredado)

Lab local operativo y versionado sin secretos. Curso en modulo 4. Instancia arriba.

### Estado previo (heredado)

Sesion cerrada. Clase commiteada; nada pendiente de esta sesion. Otras sesiones concurrentes montaron godot-3d-rpg-curso, godot-2d-platformer-beginners y creative-web-threejs-blender en la misma franja horaria.

### Estado previo (heredado)

- Estado: sesion cerrada; clase y gate retirados por pedido. Cambio propio pendiente de commit: solo el borrado de la linea del README.
- Modulo actual: n/a (curso retirado).
- Ejercicios hechos: n/a.
- Preguntas abiertas: ninguna del curso.
- Proximo bloque: n/a.

### Estado previo (heredado)

Workspace limpio salvo esos dos scripts ajenos. Clase n8n cerrada y commiteada.

### Estado previo (heredado)

ADR-112 aceptado y commiteado; gateway en tailnet; CVs de Feltsense y Mercado Libre corregidos y regenerados (ML en 2 paginas); gate de CV extendido.

### Estado previo (heredado)

v0.1. Cuatro skills ejecutables reales + surface-alignment-audit procedimental. Suites 60/60. audit-surface corre y emite report.html+json.

### Estado previo (heredado)

Conversacion de Medallia auditada y declarada borrable sin perdida (kit ya esta en repo, sin cron atado). Infjini/Disney: ABIERTO - fecha sin coordinar, sin contacto humano desde 26/10. Gonzo lo declaro 'cerrado' verbalmente; el tracker lo tiene abierto por su propio revert del 16/11. Tracker sin editar: falta decision explicita sobre marcarlo con nota de inactividad.

### Estado previo (heredado)

Research cerrado con fuentes; integracion NO ejecutada. Gateway sin provider google configurado (solo el perfil auth en modo api_key). Sin key creada, sin cambio de modelo primario, sin diff de config aplicado.

### Estado previo (heredado)

docs/claims/ operativo con 25 claims y gate en el pre-commit. settings con una sola clave de asignacion de modelos (model_by_agent), managed-blocks.py escribe en una y retire-aliases borra copias. ADR-090 documenta la correccion estructural. Tres CI en verde. Vault de memory-wiki sin uso, conservado como archivo.

### Estado previo (heredado)

Tres artefactos escritos y commiteados; esperando la respuesta de los socios.

### Estado previo (heredado)

Migración congelada en Fase 5 hasta el 2026-12-01 (quota Gemini Starter agotada; Ollama Pro activo hasta 2026-11-30). OpenClaw sigue siendo el entorno operativo maestro y Kanam sigue trabajando normal acá.

### Estado previo (heredado)

CV final entregado y enviado por Gonzo. Llamada con Agustín Bermúdez acordada para mañana 16/11.

### Estado previo (heredado)

Material listo, no enviado: falta el OK de Gonzo para mandar el mensaje y el CV.

### Estado previo (heredado)

Error de carga de la skill evidence-hunter resuelto; frontmatter válido.

### Estado previo (heredado)

Modulo 0 dado y verificado. Research de Vane auditado contra fuente: dos papers leidos, el resto marcado. Modulo 1 no empezado. Sin linea base grabada todavia.

### Estado previo (heredado)

Lab local operativo y versionado sin secretos. Curso en modulo 4. Instancia arriba.

### Estado previo (heredado)

Sesion cerrada. Clase commiteada; nada pendiente de esta sesion. Otras sesiones concurrentes montaron godot-3d-rpg-curso, godot-2d-platformer-beginners y creative-web-threejs-blender en la misma franja horaria.

### Estado previo (heredado)

- Estado: sesion cerrada; clase y gate retirados por pedido. Cambio propio pendiente de commit: solo el borrado de la linea del README.
- Modulo actual: n/a (curso retirado).
- Ejercicios hechos: n/a.
- Preguntas abiertas: ninguna del curso.
- Proximo bloque: n/a.

### Estado previo (heredado)

Workspace limpio salvo esos dos scripts ajenos. Clase n8n cerrada y commiteada.

### Estado previo (heredado)

ADR-112 aceptado y commiteado; gateway en tailnet; CVs de Feltsense y Mercado Libre corregidos y regenerados (ML en 2 paginas); gate de CV extendido.

## Proximos pasos

1) DEV.to: pedir a OPS habilitar el egress proxy para dev.to, o recibir la clave en el momento. 2) Decidir si el articulo se recorta (1.569 palabras vs 800-1.200 de la skill). 3) Verificar mobile con viewport real: Chrome headless no lo cambia y la captura a 390px no prueba nada. 4) Queda sin commitear .knowledge/handoff-history de otra sesion (2 borrados, 2 nuevos): no es de esta sesion.

### Pendientes heredados (sin cambios)

1. Retomar Critic T3.3 o ABYA YALA segun Gonzo.

### Pendientes heredados (sin cambios)

1. Nada pendiente en credenciales. Retomar programa Critic o ABYA YALA segun decida Gonzo.

### Pendientes heredados (sin cambios)

1) Confirmar con un comentario real que el OAuth ya no choca con OAuth App restrictions en shadcn-ui/radix-ui/TanStack/meta. 2) Si falla, generar un classic PAT con public_repo solo para esa operacion. 3) Push de los commits del workspace.

### Pendientes heredados (sin cambios)

1) Revocar el PAT classic ghp_ de hoy en settings/tokens: tiene admin:enterprise y delete_repo y borrar el archivo NO lo revoca. 2) Corregir el fine-grained: repository access con meta/astryx y shadcn-ui/ui, permiso Issues Read and write; si sigue fallando, aprobar el token desde la org. 3) Comentario de seguimiento pendiente en astryx#4652 (opcional, cancelado hoy). 4) Decidir si se borran forks/astryx y forks/astryx-demo con trash.

### Pendientes heredados (sin cambios)

1) OPS: instalar la guarda de forks/astryx con scripts/check-foreign-knowledge.py --install; mientras falte, cualquier commit del workspace la necesita en --no-verify. 2) Opcional: que --check marque como fuera de rotacion un diario nuevo sin marcadores (hoy solo avisa por stderr el script, y el --check no lo ve). 3) Opcional cosmetico: un mes 100% rotado deja un --- colgando en el archivo de historia. 4) Borrar /tmp/dreams-backup-2026-11-18.tar.gz cuando ya no haga falta.

### Pendientes heredados (sin cambios)

1. Decidir limpieza de forks/astryx y forks/astryx-demo (trash o conservar); opcional: restaurar el MCP de GitHub (binario + egressProxy) via OPS; astryx#4690 sigue esperando rebase ajeno.

### Pendientes heredados (sin cambios)

1) Dejar terminar scripts/render-libro-baritono.sh (~10 h, log en /tmp/render-baritono.log) y auditar cada capitulo: cola, duracion contra el texto, y las rafagas de siseo. 2) Gonzo menciono que quedan 'un par de errores' en el audio: pedirle el timestamp y el capitulo antes de tocar el pipeline. 3) Borrar el symlink de compatibilidad docs/stories/las_tres_sabanas/audio/voz/referencia-baritono-4st.wav cuando el render termine, y sacar --ref del script de batch para que use --voz. 4) Escuchar capitulo 1 completo antes de dar la voz por cerrada. 5) Si el resultado pide mas actuacion, evaluar exaggeration por registro (deuda declarada en ADR-116).

### Pendientes heredados (sin cambios)

1) Decidir si la tabla de scripts se retoma con un mecanismo nuevo (script que escribe entre marcadores propios y compara contra su propia salida) o queda archivada. El patron managed de ADR-055 NO sirve para contenido libre. 2) Revisar los 9 huerfanos con Gonzo, empezando por record_entity.py (sistema de entidades sin uso, proposito recuperable). 3) Los 6 scripts de la Cata de Harnesses se pueden archivar cuando haya decision.

### Pendientes heredados (sin cambios)

1. Resolver ADR-113 (fila de indice) para que el pre-commit vuelva a verde. Commitear CHANGELOG.md cuando la sesion que lo reescribio lo cierre. Evaluar push del commit e29bc386c8.

### Pendientes heredados (sin cambios)

1) El Descenso: decidir quien es el cuerpo del garaje en el Presente Oscuro. Es la ultima decision grande: define de que se arrepiente Julian y con que cierra la novela. Despues de eso corresponde outline y capitulo 1.
1) Una .kanam/pipeline.config.yaml por producto: es el bloqueo real (4 pendientes, 0 con config), sin eso el gate no audita nada. 2) Auth en el oracle (requires_auth). 3) Baselines por producto (C.2). 4) JUnit queda RECHAZADO hasta que exista un CI que corra el oracle.
3. ### Pendientes heredados (sin cambios)
1) Decidir con Gonzo si Infjini/Disney se marca 'sin actividad desde 26/10, ventana vencida, sigue solo si Siraj escribe' en docs/entrevistas/_general/job-search-tracker.md; 2) Borrar esta conversacion (sin perdida); 3) El gap real del proceso es ingles hablado: el plan del CUI hasta el 22/12 sigue, con o sin Disney.
5. ### Pendientes heredados (sin cambios)
1) Gonzo crea la key en aistudio.google.com/apikey con su cuenta. 2) Brief a kanam-ops con el diff: cargar key via openclaw models auth paste-api-key --provider google, definir modelos google/gemini-3.8-flash y google/gemini-3.5-flash-lite, dejar openrouter de fallback, y actualizar ADR-090 mas el bloque managed model-operativo. 3) Validar una sesion real con Flash-Lite en free tier antes de habilitar billing. 4) Si funciona, prepago de 5 USD y aplicar el credito mensual de 10 del plan.
7. ### Pendientes heredados (sin cambios)
1) Evaluar si el claim layer escala: sumar topics (career facts ya existe en prosa en memory/career-facts.md, estado de todos por proyecto) o quedarse en los tres criticos. 2) La skill memory-wiki-vault fue reescrita por el skill review a default repo-first: revisarla para que no mande a revivir el plugin retirado. 3) El vault tiene 13 paginas stale por missing updatedAt del import de hermes-sdd; si nunca se usa, decidir si se borra o se deja como archivo. 4) Considerar si el mismo formato de claims aplica a .knowledge/HANDOFF de proyectos.
9. ### Pendientes heredados (sin cambios)
1. Respuesta de los socios sobre el brief. Llamada con Agustin (EFISAT) el 2026-11-16. Si aprueban, el trabajo pasa por Planner y despues por DEV. Al dia 20 del piloto se acuerda el mantenimiento y al dia 30 se transfiere la titularidad.
11. ### Pendientes heredados (sin cambios)
1) 2026-12-01: activar Google AI Pro y retomar Fase 5 final (sesión de prueba real en Gemini). 2) Decisión pendiente: laptop MacBook Air consume solo MD/HANDOFF, sin memory.db (evita split-brain SQLite). 3) Formalizar Vane como deprecado (desplazado por Gemini cloud + image-generator nativo) con un ADR corto cuando se haga el corte a Google AI Pro.
13. ### Pendientes heredados (sin cambios)
1. Preparar la llamada del 16/11: 3 preguntas clave (dolor de mantenimiento, tareas manuales, equipo propio o tercerizado). Si responde, no poner precio en la primera charla.
15. ### Pendientes heredados (sin cambios)
1. Enviar mensaje.md (versión WhatsApp) cuando Gonzo confirme; completar el placeholder [nombre del vínculo]; si responde, agendar 20 minutos.
17. ### Pendientes heredados (sin cambios)
1. Continuar con las tareas de Kanam Critic o workspace general.
19. ### Pendientes heredados (sin cambios)
1. Elegir camino: (a) linea base grabada de «contame sobre vos» en ingles, (b) Modulo 1.1 auditoria de LinkedIn, (c) plan de 4 semanas ajustado. Recomendacion de Kanam: linea base primero.
2. Commit local de `studies/entrevistas-tecnicas/` (research/ + ejercicio-0-gonzo.md).
3. Push cuando Gonzo lo autorice.
4. Deuda: leer Brooks (2014) y McCarthy & Goffin (2004) para cerrar las dos citas sin verificar; sin esas, no enseñar sus tamanos de efecto.
5. HEREDADOS (sin cambios):
1. Gonzo hace 3.A (tipo number vs campo ausente en el IF). Luego modulo 4: dos Google Sheets como tools de un agente. Si se muda a VPS, el endpoint de Ollama cambia de host.docker.internal al host destino.
7. ### Pendientes heredados (sin cambios)
1. Decidir si cute-room-portfolio-3d se estudia: modulos 1 y 2 para escena, modulo 8 (baking) es el que justifica el curso. En reinos-de-la-frontera: convertir PNG a WebP cuando exista pipeline web y decidir si se retira assets/quaternius/_download/.
9. ### Pendientes heredados (sin cambios)
10. ### PENDIENTE - servicio del gateway: `partial import` (registrado 2026-11-10 20:54)
11. **Estado:** el gateway esta sano y estable (pid 63535, uptime > 2h, loopback 200, https 200, escuchando solo en 127.0.0.1 y [::1]). Lo que NO esta resuelto es la definicion del servicio:
12. ```
13. launchctl print gui/501/ai.openclaw.gateway
14. properties = partial import | keepalive | runatload | inferred program
15. ```
16. Consecuencia: la proxima actualizacion de OpenClaw puede negarse a activar el servicio (`service-ownership-changed`). No rompe la operacion hoy; rompe un update futuro.
17. **Plan acordado (no ejecutado):**
1. Correr `/opt/homebrew/bin/openclaw gateway install --force` **con PATH seteado** y ruta absoluta.
- El intento del 2026-11-10 fallo porque `launchctl submit` ejecuta con `PATH=/usr/bin:/bin:/usr/sbin:/sbin` y `openclaw` vive en `/opt/homebrew/bin`: 363 corridas con `openclaw: command not found`, mas un bucle de SIGTERMs de 3 horas.
2. Verificar que `properties` deje de decir `partial import`.
3. Si `bootstrap` sigue devolviendo EIO (`Bootstrap failed: 5: Input/output error`), usar `sudo` - el propio error pide privilegios: *"Try re-running the command as root for richer errors"*.
22. **Regla de disparo:** el humano corre la palabra clave **`nuevamente`** cuando vuelva a aparecer un mensaje extraño o quiera retomar este plan. Al escucharla, retomar este pendiente y no otro.
23. **Por que no se ejecuto ahora:** el ultimo intento a ciegas costo tres horas de inestabilidad. Se hace con Gonzo frente a la maquina o cuando el gateway pueda caerse sin costo.
24. ---
1. Retomar studies/n8n-ai-automations cuando Gonzo elija el primer workflow real a implementar (modulos 3/6/11 son el mismo patron). Pendientes de otra sesion: integracion de assets CC0 en projects/edad-de-los-reinos.
26. ### Pendientes heredados (sin cambios)
1) Verificar contra GitHub las 19 referencias de CVs historicos que no estan en el corpus y agregarlas a career-facts 5.2.1. 2) Limpiar las carreras universitarias de los 5 CVs historicos (EIT/HTC, Mercor, Sol, TEMPO) - son de otras sesiones. 3) Confirmar con Gonzo que el iPad quedo operativo con ws://100.126.255.95:18789. 4) Watchdog de canales: el timeout del trigger sigue sin resolver si se repite.
47. ### Pendientes heredados (sin cambios)
1. Gonzo hace 3.A (tipo number vs campo ausente en el IF). Luego modulo 4: dos Google Sheets como tools de un agente. Si se muda a VPS, el endpoint de Ollama cambia de host.docker.internal al host destino.
49. ### Pendientes heredados (sin cambios)
1. Decidir si cute-room-portfolio-3d se estudia: modulos 1 y 2 para escena, modulo 8 (baking) es el que justifica el curso. En reinos-de-la-frontera: convertir PNG a WebP cuando exista pipeline web y decidir si se retira assets/quaternius/_download/.
51. ### Pendientes heredados (sin cambios)
52. ### PENDIENTE - servicio del gateway: `partial import` (registrado 2026-11-10 20:54)
53. **Estado:** el gateway esta sano y estable (pid 63535, uptime > 2h, loopback 200, https 200, escuchando solo en 127.0.0.1 y [::1]). Lo que NO esta resuelto es la definicion del servicio:
54. ```
55. launchctl print gui/501/ai.openclaw.gateway
56. properties = partial import | keepalive | runatload | inferred program
57. ```
58. Consecuencia: la proxima actualizacion de OpenClaw puede negarse a activar el servicio (`service-ownership-changed`). No rompe la operacion hoy; rompe un update futuro.
59. **Plan acordado (no ejecutado):**
1. Correr `/opt/homebrew/bin/openclaw gateway install --force` **con PATH seteado** y ruta absoluta.
- El intento del 2026-11-10 fallo porque `launchctl submit` ejecuta con `PATH=/usr/bin:/bin:/usr/sbin:/sbin` y `openclaw` vive en `/opt/homebrew/bin`: 363 corridas con `openclaw: command not found`, mas un bucle de SIGTERMs de 3 horas.
2. Verificar que `properties` deje de decir `partial import`.
3. Si `bootstrap` sigue devolviendo EIO (`Bootstrap failed: 5: Input/output error`), usar `sudo` - el propio error pide privilegios: *"Try re-running the command as root for richer errors"*.
64. **Regla de disparo:** el humano corre la palabra clave **`nuevamente`** cuando vuelva a aparecer un mensaje extraño o quiera retomar este plan. Al escucharla, retomar este pendiente y no otro.
65. **Por que no se ejecuto ahora:** el ultimo intento a ciegas costo tres horas de inestabilidad. Se hace con Gonzo frente a la maquina o cuando el gateway pueda caerse sin costo.
66. ---
1. Retomar studies/n8n-ai-automations cuando Gonzo elija el primer workflow real a implementar (modulos 3/6/11 son el mismo patron). Pendientes de otra sesion: integracion de assets CC0 en projects/edad-de-los-reinos.
68. ### Pendientes heredados (sin cambios)
1) Verificar contra GitHub las 19 referencias de CVs historicos que no estan en el corpus y agregarlas a career-facts 5.2.1. 2) Limpiar las carreras universitarias de los 5 CVs historicos (EIT/HTC, Mercor, Sol, TEMPO) - son de otras sesiones. 3) Confirmar con Gonzo que el iPad quedo operativo con ws://100.126.255.95:18789. 4) Watchdog de canales: el timeout del trigger sigue sin resolver si se repite.

### Pendientes heredados (sin cambios)

1) Una .kanam/pipeline.config.yaml por producto: es el bloqueo real (4 pendientes, 0 con config), sin eso el gate no audita nada. 2) Auth en el oracle (requires_auth). 3) Baselines por producto (C.2). 4) JUnit queda RECHAZADO hasta que exista un CI que corra el oracle.

### Pendientes heredados (sin cambios)

1) Decidir con Gonzo si Infjini/Disney se marca 'sin actividad desde 26/10, ventana vencida, sigue solo si Siraj escribe' en docs/entrevistas/_general/job-search-tracker.md; 2) Borrar esta conversacion (sin perdida); 3) El gap real del proceso es ingles hablado: el plan del CUI hasta el 22/12 sigue, con o sin Disney.

### Pendientes heredados (sin cambios)

1) Gonzo crea la key en aistudio.google.com/apikey con su cuenta. 2) Brief a kanam-ops con el diff: cargar key via openclaw models auth paste-api-key --provider google, definir modelos google/gemini-3.8-flash y google/gemini-3.5-flash-lite, dejar openrouter de fallback, y actualizar ADR-090 mas el bloque managed model-operativo. 3) Validar una sesion real con Flash-Lite en free tier antes de habilitar billing. 4) Si funciona, prepago de 5 USD y aplicar el credito mensual de 10 del plan.

### Pendientes heredados (sin cambios)

1) Evaluar si el claim layer escala: sumar topics (career facts ya existe en prosa en memory/career-facts.md, estado de todos por proyecto) o quedarse en los tres criticos. 2) La skill memory-wiki-vault fue reescrita por el skill review a default repo-first: revisarla para que no mande a revivir el plugin retirado. 3) El vault tiene 13 paginas stale por missing updatedAt del import de hermes-sdd; si nunca se usa, decidir si se borra o se deja como archivo. 4) Considerar si el mismo formato de claims aplica a .knowledge/HANDOFF de proyectos.

### Pendientes heredados (sin cambios)

1. Respuesta de los socios sobre el brief. Llamada con Agustin (EFISAT) el 2026-11-16. Si aprueban, el trabajo pasa por Planner y despues por DEV. Al dia 20 del piloto se acuerda el mantenimiento y al dia 30 se transfiere la titularidad.

### Pendientes heredados (sin cambios)

1) 2026-12-01: activar Google AI Pro y retomar Fase 5 final (sesión de prueba real en Gemini). 2) Decisión pendiente: laptop MacBook Air consume solo MD/HANDOFF, sin memory.db (evita split-brain SQLite). 3) Formalizar Vane como deprecado (desplazado por Gemini cloud + image-generator nativo) con un ADR corto cuando se haga el corte a Google AI Pro.

### Pendientes heredados (sin cambios)

1. Preparar la llamada del 16/11: 3 preguntas clave (dolor de mantenimiento, tareas manuales, equipo propio o tercerizado). Si responde, no poner precio en la primera charla.

### Pendientes heredados (sin cambios)

1. Enviar mensaje.md (versión WhatsApp) cuando Gonzo confirme; completar el placeholder [nombre del vínculo]; si responde, agendar 20 minutos.

### Pendientes heredados (sin cambios)

1. Continuar con las tareas de Kanam Critic o workspace general.

### Pendientes heredados (sin cambios)

1. Elegir camino: (a) linea base grabada de «contame sobre vos» en ingles, (b) Modulo 1.1 auditoria de LinkedIn, (c) plan de 4 semanas ajustado. Recomendacion de Kanam: linea base primero.
2. Commit local de `studies/entrevistas-tecnicas/` (research/ + ejercicio-0-gonzo.md).
3. Push cuando Gonzo lo autorice.
4. Deuda: leer Brooks (2014) y McCarthy & Goffin (2004) para cerrar las dos citas sin verificar; sin esas, no enseñar sus tamanos de efecto.
5. HEREDADOS (sin cambios):
1. Gonzo hace 3.A (tipo number vs campo ausente en el IF). Luego modulo 4: dos Google Sheets como tools de un agente. Si se muda a VPS, el endpoint de Ollama cambia de host.docker.internal al host destino.
7. ### Pendientes heredados (sin cambios)
1. Decidir si cute-room-portfolio-3d se estudia: modulos 1 y 2 para escena, modulo 8 (baking) es el que justifica el curso. En reinos-de-la-frontera: convertir PNG a WebP cuando exista pipeline web y decidir si se retira assets/quaternius/_download/.
9. ### Pendientes heredados (sin cambios)
10. ### PENDIENTE - servicio del gateway: `partial import` (registrado 2026-11-10 20:54)
11. **Estado:** el gateway esta sano y estable (pid 63535, uptime > 2h, loopback 200, https 200, escuchando solo en 127.0.0.1 y [::1]). Lo que NO esta resuelto es la definicion del servicio:
12. ```
13. launchctl print gui/501/ai.openclaw.gateway
14. properties = partial import | keepalive | runatload | inferred program
15. ```
16. Consecuencia: la proxima actualizacion de OpenClaw puede negarse a activar el servicio (`service-ownership-changed`). No rompe la operacion hoy; rompe un update futuro.
17. **Plan acordado (no ejecutado):**
1. Correr `/opt/homebrew/bin/openclaw gateway install --force` **con PATH seteado** y ruta absoluta.
- El intento del 2026-11-10 fallo porque `launchctl submit` ejecuta con `PATH=/usr/bin:/bin:/usr/sbin:/sbin` y `openclaw` vive en `/opt/homebrew/bin`: 363 corridas con `openclaw: command not found`, mas un bucle de SIGTERMs de 3 horas.
2. Verificar que `properties` deje de decir `partial import`.
3. Si `bootstrap` sigue devolviendo EIO (`Bootstrap failed: 5: Input/output error`), usar `sudo` - el propio error pide privilegios: *"Try re-running the command as root for richer errors"*.
22. **Regla de disparo:** el humano corre la palabra clave **`nuevamente`** cuando vuelva a aparecer un mensaje extraño o quiera retomar este plan. Al escucharla, retomar este pendiente y no otro.
23. **Por que no se ejecuto ahora:** el ultimo intento a ciegas costo tres horas de inestabilidad. Se hace con Gonzo frente a la maquina o cuando el gateway pueda caerse sin costo.
24. ---
1. Retomar studies/n8n-ai-automations cuando Gonzo elija el primer workflow real a implementar (modulos 3/6/11 son el mismo patron). Pendientes de otra sesion: integracion de assets CC0 en projects/edad-de-los-reinos.
26. ### Pendientes heredados (sin cambios)
1) Verificar contra GitHub las 19 referencias de CVs historicos que no estan en el corpus y agregarlas a career-facts 5.2.1. 2) Limpiar las carreras universitarias de los 5 CVs historicos (EIT/HTC, Mercor, Sol, TEMPO) - son de otras sesiones. 3) Confirmar con Gonzo que el iPad quedo operativo con ws://100.126.255.95:18789. 4) Watchdog de canales: el timeout del trigger sigue sin resolver si se repite.

### Pendientes heredados (sin cambios)

1. Gonzo hace 3.A (tipo number vs campo ausente en el IF). Luego modulo 4: dos Google Sheets como tools de un agente. Si se muda a VPS, el endpoint de Ollama cambia de host.docker.internal al host destino.

### Pendientes heredados (sin cambios)

1. Decidir si cute-room-portfolio-3d se estudia: modulos 1 y 2 para escena, modulo 8 (baking) es el que justifica el curso. En reinos-de-la-frontera: convertir PNG a WebP cuando exista pipeline web y decidir si se retira assets/quaternius/_download/.

### Pendientes heredados (sin cambios)

### PENDIENTE - servicio del gateway: `partial import` (registrado 2026-11-10 20:54)

**Estado:** el gateway esta sano y estable (pid 63535, uptime > 2h, loopback 200, https 200, escuchando solo en 127.0.0.1 y [::1]). Lo que NO esta resuelto es la definicion del servicio:

```
launchctl print gui/501/ai.openclaw.gateway
  properties = partial import | keepalive | runatload | inferred program
```

Consecuencia: la proxima actualizacion de OpenClaw puede negarse a activar el servicio (`service-ownership-changed`). No rompe la operacion hoy; rompe un update futuro.

**Plan acordado (no ejecutado):**

1. Correr `/opt/homebrew/bin/openclaw gateway install --force` **con PATH seteado** y ruta absoluta.
   - El intento del 2026-11-10 fallo porque `launchctl submit` ejecuta con `PATH=/usr/bin:/bin:/usr/sbin:/sbin` y `openclaw` vive en `/opt/homebrew/bin`: 363 corridas con `openclaw: command not found`, mas un bucle de SIGTERMs de 3 horas.
2. Verificar que `properties` deje de decir `partial import`.
3. Si `bootstrap` sigue devolviendo EIO (`Bootstrap failed: 5: Input/output error`), usar `sudo` — el propio error pide privilegios: *"Try re-running the command as root for richer errors"*.

**Regla de disparo:** el humano corre la palabra clave **`nuevamente`** cuando vuelva a aparecer un mensaje extraño o quiera retomar este plan. Al escucharla, retomar este pendiente y no otro.

**Por que no se ejecuto ahora:** el ultimo intento a ciegas costo tres horas de inestabilidad. Se hace con Gonzo frente a la maquina o cuando el gateway pueda caerse sin costo.

---

1. Retomar studies/n8n-ai-automations cuando Gonzo elija el primer workflow real a implementar (modulos 3/6/11 son el mismo patron). Pendientes de otra sesion: integracion de assets CC0 en projects/edad-de-los-reinos.

### Pendientes heredados (sin cambios)

1) Verificar contra GitHub las 19 referencias de CVs historicos que no estan en el corpus y agregarlas a career-facts 5.2.1. 2) Limpiar las carreras universitarias de los 5 CVs historicos (EIT/HTC, Mercor, Sol, TEMPO) - son de otras sesiones. 3) Confirmar con Gonzo que el iPad quedo operativo con ws://100.126.255.95:18789. 4) Watchdog de canales: el timeout del trigger sigue sin resolver si se repite.

## Decisiones y contexto que no debe perderse

- No minificar CSS: un minificador conservador ahorra 526 B gzip sobre 3.789; no paga el riesgo ni la dependencia. No subsetear fuentes: son variables y el subset de glifos baja solo 5%, el peso esta en las tablas de variacion. Una fila por pieza en el indice: la traduccion es una vista, no una pieza. Versionar assets por hash de contenido: un cambio solo de CSS era invisible para cualquiera con cache. Tesis del articulo: la evidencia confirma el sintoma, no la explicacion que le colgas encima.

### Heredadas (sin cambios)

- OAuth-first por evidencia de comentarios reales.

### Heredadas (sin cambios)

- OAuth-first confirmado con evidencia de comentarios reales, no solo probes.

### Heredadas (sin cambios)

- Precedencia OAuth-first por evidencia de alcance, no por preferencia: el fine-grained pierde en repos ajenos. Cleanup activo pero medido: se borra lo que no sirve, con trash.

### Heredadas (sin cambios)

- Credencial de escritura: PAT en archivo 600 + launcher 700, nunca en openclaw.json. El binario del github-mcp-server necesita 'stdio' explicito en args. Los checksums oficiales hashean el tarball, no el binario: la cadena de custodia se verifica en dos pasos. Lectura y escritura son permisos distintos: un token que lee las dos orgs puede no escribir en ninguna, y el mensaje de error no distingue allowlist de aprobacion de org.

### Heredadas (sin cambios)

- La skill growing-doc-retention no estaba sin usar: es de instalacion y su valor es el mecanismo corriendo, no la invocacion. La leccion que si sirve es su paso 4 (el gate va donde el doc vive) y su corolario nuevo: cuando un doc pasa a existir N veces (un DREAMS.md por agente), el gate tiene que ENUMERAR las instancias o queda verde sobre archivos que crecen solos. No se abrio ADR: la politica de rotacion mensual es de 2026-10-06; esto es cobertura de la misma politica, no una decision nueva.

### Heredadas (sin cambios)

- Escribir con PAT en ~/.openclaw/secrets/github-token, no con el OAuth de gh: la restriccion de la org es del OAuth App. Medir componentes renderizados, no tokens: el paquete publicado y el source de main divergen (matcha y chocolate cambiaron color-text-green). No comentar en PRs aprobados y trabados en rebase cuando el follow-up ya esta rastreado.

### Heredadas (sin cambios)

- ADR-116 (reemplaza ADR-115, archivado): la voz es Chatterbox con clonacion desde una referencia baritona de 100 Hz. Una voz es un directorio en assets/voces/<nombre>/ con referencia.wav, el texto que la genero y voz.json con los valores medidos; el script la resuelve por nombre. No se aplican los tres registros de Kokoro al motor vigente: Chatterbox entona solo y sumar variacion por tramo multiplica las costuras. Leccion de metodo: las tres primeras voces se eligieron con una muestra de una frase sin dialogo ni preguntas; una frase suelta no prueba un narrador.

### Heredadas (sin cambios)

- growing-doc-retention no deja ideas pendientes de adaptar: deja la leccion de los dos errores de diagnostico (el archivo gigante no implica rotacion rota; la ventana se elige por ritmo real del repo). El patron managed solo soporta valores escalares interpolados, no contenido libre: guardar una tabla como setting no genera bloque. La verificacion de un artefacto generado se hace con grep/test en el archivo, nunca leyendo el stdout del generador.

### Heredadas (sin cambios)

- Pagos: sin proveedor obligatorio, eleccion por proyecto (ADR-114 supersede ADR-042)

### Heredadas (sin cambios)

- Decision 0 (18/11): Julian ve al padre esconder la navaja; cuando llega la policia el ya la movio y nunca se lo dice. El padre se lo atribuye a la suerte. La suerte del padre es el hijo.
- Decision 1 (18/11): la primera vez que usa la navaja es contra el padre, en la cocina, sin sangre: la abre sobre la mesa y le dice "no hables mas de ella". Quince anos.
- Estructura: Opcion B, el aula como ancla y detonante, no como inicio.
- La navaja es el arma del homicidio de la madre. El padre esta libre y Julian lo cuida: amor, miedo y custodia en el mismo gesto.
- JUnit no se implementa: no hay consumidor (surface-audit.yml corre solo el stage estático; la única mención de junit era un ejemplo escrito por mí en octubre). Una casilla vacía no es razón para construir. El token brand-primary/blanco es decisión del dueño del DS, no mía.
- ### Heredadas (sin cambios)
- Un proceso con ventana prometida vencida y 21 dias de silencio NO se cierra automaticamente: el 16/11 ya se cerro por silencio y Gonzo lo revirtio en 4 minutos. La distincion que vale es 'sin noticias' (no hay respuesta) vs 'aun no coordinamos' (depende de coordinar). Cerrar un proceso es de Gonzo, no de la regla de 10 dias. Ademas: nunca inferir el cliente de un bench (Infojini -> Disney, no Medallia) sin fuente; Brighthire es la grabadora, no la empresa contratante.
- ### Heredadas (sin cambios)
- Google AI Pro no da API incluida; da 10 USD/mes de credito Cloud (prepago 5 obligatorio) y cuota solo en superficies Google. Antigravity OAuth con OpenClaw es breach de terms: prohibido, se usa API key. 3.8 Flash es el workhorse elegido; Hydrogen descartado por caro (2x). OpenRouter queda en B del pipeline A/B como veedor independiente. Mix por rol: Flash en CORE/dev, Flash-Lite en auditor/mind/studio. Arrancar gratis con Flash-Lite, pagar cuando el volumen lo exija.
- ### Heredadas (sin cambios)
- La idea de memory-wiki se conserva, el vehiculo no: claim + evidencia + status + confidence vive en docs/claims/ dentro del repo, versionado, con gate propio. Un detector que nunca dispara es indistinguible de uno ausente: --negative en cada gate nuevo. Un dato, un dueno: tres claves con el mismo valor siguen siendo tres duenos, se retira la copia en vez de vigilarla. Un gate que falla por un archivo ajeno es un gate que enseña a usar --no-verify: se corrige la causa, no se saltea.
- ### Heredadas (sin cambios)
- Producto enlatado, no servicio por hora. Un deploy por cliente (single-tenant). Next.js + Supabase con RLS y exclusion constraint de Postgres para impedir solapamiento. La solicitud de invitado retiene el lugar 48 horas. La titularidad se transfiere despues de acordar el mantenimiento, nunca antes.
- ### Heredadas (sin cambios)
- Coexistencia temporal sana: OpenClaw = maestro; Antigravity = espejo de solo lectura hasta activar Pro. En la laptop Air: NO sincronizar memory.db, solo markdown derivado (dailies, HANDOFFs, career-facts, ADRs) y lo que deba persistir va por HANDOFF a la Mini. Vane queda sin sentido funcional al perder Ollama Pro y ganar Gemini Notebook.
- ### Heredadas (sin cambios)
- Sin titulo de ingeniero; liderazgos tono bajo; sin carreras universitarias; EY es frontend, no full stack; CV corto y la profundidad va a la llamada.
- ### Heredadas (sin cambios)
- Sin título de ingeniero; liderazgos tono bajo; OSS dentro del CV; formación sin universidades (career-facts 7-bis).
- ### Heredadas (sin cambios)
- Se corrigió sintaxis YAML en agents/kanam-critic/skills/evidence-hunter/SKILL.md eliminando un paréntesis de cierre fuera de comillas.
- ### Heredadas (sin cambios)
- El research externo se audita leyendo la fuente, no se adopta por plausible. Aprobar una cita sin abrir el paper es el mismo error que citar un README como especificacion.
- Reappraisal no reduce el estres subjetivo: cambia fisiologia y atencion. Ensenarlo como «calmate» es falso.
- Acento leve penaliza credibilidad por fluidez y el oyente puede corregirlo si lo nota; acento fuerte no. La palanca practica es fluidez del contenido, no borrar el acento.
- No hay literatura que sostenga «rechazo por ansiedad» como criterio formal en examenes de conducir; se rechaza por errores observables.
- Vane devuelve borradores: lo que la clase cita tiene que estar leido.
- HEREDADAS (sin cambios):
- Fallback unico local por decision de Gonzo: 'el fallback no puede ser otro modelo en la nube'. Primario deepseek y no beam: dejo de ser gratuito y su calidad ya estaba descartada por ADR-105 (3/4 bugs, auto-aprobacion con defecto vivo). Ninguna carrera universitaria va a CV ni ATS (regla 2026-11-04). Una referencia de CV se verifica abriendo el hilo en GitHub, no contra el corpus.
- ### Heredadas (sin cambios)
- Fallback unico local por decision de Gonzo: 'el fallback no puede ser otro modelo en la nube'. Primario deepseek y no beam: dejo de ser gratuito y su calidad ya estaba descartada por ADR-105 (3/4 bugs, auto-aprobacion con defecto vivo). Ninguna carrera universitaria va a CV ni ATS (regla 2026-11-04). Una referencia de CV se verifica abriendo el hilo en GitHub, no contra el corpus.

### Heredadas (sin cambios)

- JUnit no se implementa: no hay consumidor (surface-audit.yml corre solo el stage estático; la única mención de junit era un ejemplo escrito por mí en octubre). Una casilla vacía no es razón para construir. El token brand-primary/blanco es decisión del dueño del DS, no mía.

### Heredadas (sin cambios)

- Un proceso con ventana prometida vencida y 21 dias de silencio NO se cierra automaticamente: el 16/11 ya se cerro por silencio y Gonzo lo revirtio en 4 minutos. La distincion que vale es 'sin noticias' (no hay respuesta) vs 'aun no coordinamos' (depende de coordinar). Cerrar un proceso es de Gonzo, no de la regla de 10 dias. Ademas: nunca inferir el cliente de un bench (Infojini -> Disney, no Medallia) sin fuente; Brighthire es la grabadora, no la empresa contratante.

### Heredadas (sin cambios)

- Google AI Pro no da API incluida; da 10 USD/mes de credito Cloud (prepago 5 obligatorio) y cuota solo en superficies Google. Antigravity OAuth con OpenClaw es breach de terms: prohibido, se usa API key. 3.8 Flash es el workhorse elegido; Hydrogen descartado por caro (2x). OpenRouter queda en B del pipeline A/B como veedor independiente. Mix por rol: Flash en CORE/dev, Flash-Lite en auditor/mind/studio. Arrancar gratis con Flash-Lite, pagar cuando el volumen lo exija.

### Heredadas (sin cambios)

- La idea de memory-wiki se conserva, el vehiculo no: claim + evidencia + status + confidence vive en docs/claims/ dentro del repo, versionado, con gate propio. Un detector que nunca dispara es indistinguible de uno ausente: --negative en cada gate nuevo. Un dato, un dueno: tres claves con el mismo valor siguen siendo tres duenos, se retira la copia en vez de vigilarla. Un gate que falla por un archivo ajeno es un gate que enseña a usar --no-verify: se corrige la causa, no se saltea.

### Heredadas (sin cambios)

- Producto enlatado, no servicio por hora. Un deploy por cliente (single-tenant). Next.js + Supabase con RLS y exclusion constraint de Postgres para impedir solapamiento. La solicitud de invitado retiene el lugar 48 horas. La titularidad se transfiere despues de acordar el mantenimiento, nunca antes.

### Heredadas (sin cambios)

- Coexistencia temporal sana: OpenClaw = maestro; Antigravity = espejo de solo lectura hasta activar Pro. En la laptop Air: NO sincronizar memory.db, solo markdown derivado (dailies, HANDOFFs, career-facts, ADRs) y lo que deba persistir va por HANDOFF a la Mini. Vane queda sin sentido funcional al perder Ollama Pro y ganar Gemini Notebook.

### Heredadas (sin cambios)

- Sin titulo de ingeniero; liderazgos tono bajo; sin carreras universitarias; EY es frontend, no full stack; CV corto y la profundidad va a la llamada.

### Heredadas (sin cambios)

- Sin título de ingeniero; liderazgos tono bajo; OSS dentro del CV; formación sin universidades (career-facts 7-bis).

### Heredadas (sin cambios)

- Se corrigió sintaxis YAML en agents/kanam-critic/skills/evidence-hunter/SKILL.md eliminando un paréntesis de cierre fuera de comillas.

### Heredadas (sin cambios)

- El research externo se audita leyendo la fuente, no se adopta por plausible. Aprobar una cita sin abrir el paper es el mismo error que citar un README como especificacion.
- Reappraisal no reduce el estres subjetivo: cambia fisiologia y atencion. Ensenarlo como «calmate» es falso.
- Acento leve penaliza credibilidad por fluidez y el oyente puede corregirlo si lo nota; acento fuerte no. La palanca practica es fluidez del contenido, no borrar el acento.
- No hay literatura que sostenga «rechazo por ansiedad» como criterio formal en examenes de conducir; se rechaza por errores observables.
- Vane devuelve borradores: lo que la clase cita tiene que estar leido.
- HEREDADAS (sin cambios):
- Fallback unico local por decision de Gonzo: 'el fallback no puede ser otro modelo en la nube'. Primario deepseek y no beam: dejo de ser gratuito y su calidad ya estaba descartada por ADR-105 (3/4 bugs, auto-aprobacion con defecto vivo). Ninguna carrera universitaria va a CV ni ATS (regla 2026-11-04). Una referencia de CV se verifica abriendo el hilo en GitHub, no contra el corpus.

### Heredadas (sin cambios)

- Fallback unico local por decision de Gonzo: 'el fallback no puede ser otro modelo en la nube'. Primario deepseek y no beam: dejo de ser gratuito y su calidad ya estaba descartada por ADR-105 (3/4 bugs, auto-aprobacion con defecto vivo). Ninguna carrera universitaria va a CV ni ATS (regla 2026-11-04). Una referencia de CV se verifica abriendo el hilo en GitHub, no contra el corpus.

## Archivos tocados

```
memory/2026-11-19.md
.knowledge/HANDOFF.md
.knowledge/SESSIONS.md
.knowledge/handoff-history/2026-11-17-0857-HANDOFF.md
skills/github/SKILL.md
agents/kanam-mind/briefs/2026-11-18-birdid-offline-feasibility.md
agents/kanam-ops/scripts/gateway-channels-watch-trigger.js
agents/kanam-ops/tests/test_ops_scripts.py
memory/2026-11-18.md
memory/memory.db
scripts/pipeline-queue.sh
docs/CHANGELOG.md
docs/adr/README.md
docs/archive/CHANGELOG-archive.md
docs/stories/el_descenso/historia_descenso.md
memory/2026-11-17.md
agents/kanam-auditor/LEARNINGS.md
agents/kanam-auditor/MEMORY.md
agents/kanam-auditor/ROADMAP.md
memory/devto/2026-W47.md
.knowledge/handoff-history/2026-11-09-1700-HANDOFF.md
memory/2026-11-15.md
docs/entrevistas/_general/job-search-tracker.md
memory/career-facts.md
agents/kanam-critic/skills/evidence-hunter/SKILL.md
studies/ai-agents-for-beginners/m1-llm-en-10-lineas.md
.knowledge/handoff-history/2026-11-06-1805-2-HANDOFF.md
.knowledge/handoff-history/2026-11-06-1805-HANDOFF.md
studies/sql-full-course/HANDOFF.md
studies/sql-full-course/SESSIONS.md
memory/2026-11-12.md
studies/dsa-mega-course/HANDOFF.md
studies/godot-2d-platformer-beginners/HANDOFF.md
studies/godot-2d-platformer-beginners/SESSIONS.md
studies/godot-3d-rpg-curso/HANDOFF.md
studies/godot-3d-rpg-curso/PROGRESO.md
studies/godot-3d-rpg-curso/SESSIONS.md
studies/README.md
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-19.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*

## What This Is

OpenClaw personal workspace

## Tech Stack

OpenClaw, AI-assisted dev

## Current Goal

Manage Gonzo's projects, memory, and daily work

## Where I Left Off

v0.4 cerrada: dev-pipeline.yml corre 11 suites, gate de skills, rutas, copias de dash, docs del rol y roadmap del rol. runs.db persiste corridas y weekly cuenta por semana ISO. Una corrida real completa (task #5) registrada. Los cuatro ejecutables de medicion (metrics_scan, dep_inventory, compat_matrix, bench_compare) verificados contra repos reales.

## Next Steps

1. Usar el pipeline en el proximo trabajo real que asigne CORE, sin evidencia declarada a mano, para probar v0.5 con un cambio que pueda fallar
2. Medir demanda real desde sesiones y memoria a las dos semanas (hito 5.4 quedo con una sola corrida, no mide uso)
3. Decidir si se limpian las 91 skills de otros roles sin verificacion y las 87 rutas ambiguas fuera del arbol de dev

## Blockers

- La corrida #5 tardo 0s y verify solo corrio tests que ya pasaban: el pipeline no se probo contra un cambio que pueda fallar de formas interesantes
- La metrica de demanda tiene una sola corrida: no mide uso todavia

## Decisions Made

| Decision | Why | Date |
|----------|-----|------|
| Los gates de CI se acotan al arbol de kanam-dev, no al workspace | docs_sync da 409 desalineaciones y check-roadmaps falla por studio; bloquear por deuda ajena empuja al --no-verify, que es peor que no tener gate | 2026-11-10 |
| El registro en runs.db es best-effort: si falla, el pipeline sigue | Un fallo de telemetria no puede tumbar un pipeline que ya hizo el trabajo; se avisa por stderr, no se calla | 2026-11-10 |
| runs.db inserta una vez y actualiza la misma fila en cada guardado | El runner guarda por estacion para poder retomar; insert-only dejaba una corrida que murio a mitad marcada como completo para siempre | 2026-11-10 |
| audit y docs_sync detectan Python sin manifiesto por los test_*.php presentes, incluidos los de bin/ | El rol no tiene pyproject ni package.json y el pipeline no podia verificar su propio repo | 2026-11-10 |
| Un 0 de unittest discover es error de medicion, no realidad: 0 | El cero significa que no busco donde estan los tests; aceptarlo como conteo real es un falso positivo del verificador | 2026-11-10 |

## Session History

### 2026-08-02 - Configured session-context on workspace
**Left off:** Showing usage example to Gonzo
### 2026-08-02 - Testing session-context save
**Left off:** Writing save.mjs script
### 2026-11-06 - Sesion de demanda de Kanam DEV: diagnostico (el cuello era invocacion, no skills), construccion de la superficie de pipeline completa y cierre del roadmap v0.2.
_1971 commits, 114 files changed_
**Left off:** Superficie del pipeline terminada y commiteada: intake (S1), despachador kanam-dev con 8 subcomandos, runner con plantillas y resume, slice-commit, docs-sync y handoff gate. 134 tests verdes. Skill kanam-dev-surface registrada. Roadmap v0.2 commiteado con indice y tracking sincronizados.
### 2026-11-10 - Auditoria de la ventana de cambio de modelo (beam a deepseek), correccion de los defectos medidos, U4 completo con cuatro ejecutables, runs.db (hitos 5.1-5.5) y CI del rol (v0.4). De 134 a 254 tests.
_61 commits, 165 files changed_
**Left off:** v0.4 cerrada: dev-pipeline.yml corre 11 suites, gate de skills, rutas, copias de dash, docs del rol y roadmap del rol. runs.db persiste corridas y weekly cuenta por semana ISO. Una corrida real completa (task #5) registrada. Los cuatro ejecutables de medicion (metrics_scan, dep_inventory, compat_matrix, bench_compare) verificados contra repos reales.
