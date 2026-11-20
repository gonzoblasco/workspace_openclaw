# HANDOFF - workspace

**Fecha:** 2026-11-19 22:41 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-19). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-19.md`.

---
## Que se hizo en esta sesion

### 2026-11-19 22:41
Conversación de arranque de sesión 2026-11-19: el humano preguntó 'qué sabes de mí'. Se respondió con el estado del workspace (sesiones 1-7 del día: credenciales GitHub, localdoc-agent, ABYA YALA, critic v0.3, gobierno/verdad), la personalidad del CORE (Kanam) según SOUL.md, y se preguntó cómo era Gonzo en persona. Se documentó la personalidad de Gonzo (USER.md + user-profile.md), el patrón de trinchera con protocolo TRINCHERA, se escribió el protocolo en MEMORY.md, se cerró la sesión.

### 2026-11-19 13:54
Cierre de la segunda mitad: causa raiz de los gates fallidos y cambio de modelo del juez. (1) Diagnostico por experimento controlado: mismo gate T4.3, mismo brief, un solo cambio (modelo). gpt-oss:120b-cloud habia fallado 4 de 4 (F29 ORO inventado, F30 no supo invocar la herramienta, F31 evidencia elidida, F34 reporte declarado y no escrito). deepseek-v4.1-flash completo el gate: reporte de 17.7 KB, fila en el ledger, verify-verdict 12/12, y encontro 4 defectos reales en el artefacto. Documentado en agents/kanam-critic/docs/JUDGE-RELIABILITY.md. (2) ADR-117 escrito y aceptado: enmienda la fila kanam-critic de ADR-090, el juez pasa a deepseek con fallback gemma4:12b-mlx. El ADR deja explicito que NO cambia el pipeline A/B (A sigue gpt-oss) y que la asignacion no esta vigente hasta que config + DB + bloque coincidan. (3) Aplicacion en tres capas. OPS dictamino NO APLICA y aplico igual la capa 1 (openclaw.json), y al tocar model_by_agent corrompio el setting: el valor quedo literalmente en 'model_pipeline', con dos timestamps. Si se aplicaba el bloque, el mapa de modelos por agente se destruia. Se recupero el valor desde git (memory.db esta versionado), se recompuso con solo la palabra del critic cambiada, se aplico con managed-blocks.py y se verifico segmento por segmento: el diff es una sola frase. (4) Un gate de claims (models.critic-primary) freno el commit por tener hardcodeado el modelo viejo; se actualizo citando ADR-117, no por conveniencia. (5) Cuatro arreglos del kit que quedaban pendientes: emit-verdict rechaza evidencia elidida con lista explicita de frases (exit 2, ledger con sha256 intacto); verify-verdict exige tabla SHARP con lista explicita de legacy previos al 2026-11-19; format_sharp_report valida la etiqueta contra la matriz SHARP; 5 tests nuevos de VETO y ORO. (6) Tasa de absorcion del ledger: de 22.6% a 40% (14/35), cada friccion cerrada con su fix_url.

### 2026-11-19 13:36
Sesion de gobierno y verdad de datos, sin escribir codigo de producto. Cuatro frentes cerrados y tres errores propios corregidos antes de que salieran. (1) AUTOMATIONS: el job pipeline-queue-watcher fallaba por timeout del trigger-gate (presupuesto fijo de 30s documentado en automation/cron-jobs/schedules.md; corridas medidas de 41.8s y 108.8s). Convertido a payload command con scripts/pipeline-queue-watch.sh: 105ms, lastRunStatus ok, silencio via NO_REPLY. Ademas: dos jobs watch-devto-trends duplicados (creados el 17/11 con 8 minutos de diferencia, mismo script) quedaron en uno; gateway-channels-refresh recibio bestEffort para que su entrega bloqueada no genere alertas. (2) ROADMAP revisado a 41 dias: el cuerpo de 2.3 declaraba 'todos cerrados' cuando el tracker tenia 3 procesos vivos desde el 19/10 (mismo error que el falso verde de octubre, invertido); 1.1 bajo a amarillo porque pipeline-track.sh status devuelve vacio; se agrego la capa 0.4 Coexistencia OpenClaw+Antigravity que no existia; siete numeros stale reemplazados por medicion. (3) NORTH revisado: tres afirmaciones falsas (OnWheels 'falta solo el chat RAG' cuando hubo reset a greenfield el 29/10 y F0 no arranco; kanam-os listado como frente activo sin copia local desde el 29/10; busqueda laboral 'dormante' con 3 procesos vivos). CPACC retirado por falta de fondos: T1 queda con un solo criterio de salida. (4) PLAN-DE-MARCHA.md creado: tres cubetas (obra 50 / ingreso 30 / sistema 20 con piso y techo), piso funcional de 30 min semanales, secuencia de 6 semanas hasta el 31/12, orden de sacrificio y contingencias; paso por red-team del Planner y se le agregaron reparto de roles y contingencias. (5) VERDAD DE CV: de 18 claims sin respaldo se auditaron 22 referencias contra GitHub (autoria, reviews y comentarios). Tres no tenian NINGUNA participacion de Gonzo (ariakit 6810, hermes-agent 130041, astryx 5332) y dos numeros estaban mal (ibm-products 9868 es un issue ajeno; el analisis atribuido a 9866 vive en 9865). Se agrego career-facts.md seccion 5.5 con la clasificacion en cuatro tablas y una lista de referencias no citables; los CVs y sus HTML quedaron alineados; las cinco entradas de universidad salieron por la regla dura del 2026-11-04. (6) PERFIL DEL BLOG: a11y-portfolio/profile no mencionaba Preflight ni kanam-fixer y Super7ui/Minutentag tenian un solo bullet cada uno. Reescrito desde career-facts y publicado: 4/4/4/3 bullets, titulos canonicos, verificado en vivo con curl.

### 2026-11-19 13:28
Sesion larga de programa critic-v0.3: de 5/12 a 11/12. (1) T3.3 tasa de absorcion publicada: 7/27 = 25.9%, con la lectura honesta de que la absorcion de autores ajenos es 0 y el 35% previo era sobre base de 20. (2) T4.1 objective-extractor: cuatro rondas de ejecutor. gpt-oss invento markup inexistente, luego rutas /full/path/to/ y tests en verde con pytest rojo, y en la r4 afirmo 9 fixes sin modificar el archivo (mtime identico). Con deepseek y override de pacto salio la version real: 260 lineas, 17 tests, resolucion de citas contra la raiz del repo. Gate: r1 invento ORO 24/25 con flag inexistente (F29), r2 no supo invocar la herramienta (F30), r3 dio VETO honesto pero elidio evidencia (F31). Se cerro por verificacion del CORE y despues se absorbio el VETO: r2 Aprobado 20/25 con CI y uso real sobre el ROADMAP. (3) T4.2 detectores horizon (grafo de imports con ast, ciclos relativos y absolutos) y resistance (patrones de borde): lab 12/12, el CORE encontro un falso verde con imports absolutos que el lab no cazaba, 6 fixtures propios confirman que discriminan. Aprobado 23/25 (F32: el juez elidio la seccion de discriminacion). (4) T4.3 format_sharp_report: publica el veredicto como comentario de PR. Primera publicacion real: PR #1 de workspace_openclaw, comentario 7014080729 de 4432 chars generado por la herramienta. Modo estricto: sin tabla SHARP exige --allow-ledger-axes. Gate T4.3 invalido, declaro un reporte que no escribio (F34); cierre por verificacion del CORE. (5) T5.1 contrato de invocacion cruzada en docs/CRITIC-DISPATCH.md: que trae la peticion, que devuelve el Critic (4 artefactos), 9 sintomas que invalidan una respuesta mapeados a F29-F34, regla de dos gates fallidos sin tercer intento ciego. (6) T5.2 gate cableado: scripts/check-critic-gate.py con exit 0/3/4/2, 17 tests, match exacto por slug sin herencia, step en CI verificado en el runner. (7) F33: el reporte r2 de T4.1 no tenia tabla SHARP y verify-verdict lo acepto igual; se regenero. v1.0 queda pending a proposito: exige un mes de demanda de otros roles.

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

## Estado actual

Sesión de arranque general; sin trabajo de proyecto en curso. Contexto: el humano (Gonzalo Blasco) se puso al día con el estado del workspace y la identidad/personalidad del CORE.

### Estado previo (heredado)

Programa critic-v0.3 en 11/12 (v1.0 pending: exige un mes de demanda de otros roles). Juez en deepseek (ADR-117) aplicado en config, DB, bloque y claim. Kit: 18/18, 65 tests, gate de veredicto en CI, ledger 14 absorbidas / 21 abiertas (casi todas de autores ajenos).

### Estado previo (heredado)

Sistema verde: check-bootstrap-budget OK (5 archivos bajo cap), check-refs OK 182 rutas, check-adr-integrity OK 68 ADRs, check-single-source OK, check-cv-facts OK 15 CVs, automations sin jobs en error. OnWheels F0 sigue sin iniciar: bloqueada por dos decisiones de Gonzo (aceptar el diseno PII minimo y registrar la app central en el panel de developers de MeLi). Plan de marcha vigente hasta el 31/12.

### Estado previo (heredado)

Programa critic-v0.3 en 11/12. Kit: 18/18 checks, verify-verdict 10/10, lab 12/12, 51 tests en agents/kanam-critic. Gate de veredicto corre en CI. PR #1 abierto a proposito (se mergea despues). Ledger: 34 fricciones, 7 absorbidas, 27 abiertas; 6 de las nuevas son fallas de gates.

### Estado previo (heredado)

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

1. Ningún paso de proyecto pendiente en este cierre. Próxima sesión: retomar trabajo de proyecto según memory/2026-11-19.md o pendientes del HANDOFF vigente.

### Pendientes heredados (sin cambios)

1) Dejar correr el mes y medir demanda de otros roles para v1.0. 2) Mergear PR #1 (rama feat/critic-format-sharp-report). 3) Revisar docs/OPS-DISPATCH.md: un dictamen NO APLICA no puede convivir con escrituras, y los valores multisegmento se reescriben desde su fuente. 4) Las 21 fricciones abiertas son de autores ajenos: no son trabajo del Critic.

### Pendientes heredados (sin cambios)

1) Gonzo: registrar la app central de OnWheels en el panel de developers de MeLi y pasar Client ID + permisos; aceptar o rechazar el diseno PII minimo (guardar question_id/item_id/texto/estado, nunca nombre ni from.id del comprador, exhibir solo en la sesion del seller dueno, TTL, rotular respuestas IA). Con eso corren 0.3 a 0.6 y se confirma api_version=4. 2) Postular a Mercor: cuenta en work.mercor.com, subir el PDF, Practice Interview (el CV ya esta listo). 3) Si el blog se va a seguir tocando, clonar a11y-portfolio en projects/ de forma estable en vez de clones descartables. 4) Deuda del plan: .knowledge sin respaldo en preflight, mercor-project-odin y SDXL; dedupe de contributions; 2 de 12 proyectos con pre-commit hook; radar de oportunidades OSS con 24 dias. 5) gateway-channels-refresh deberia ser delivery mode none (solo por UI; el CLI no expone la bandera).

### Pendientes heredados (sin cambios)

1) Dejar correr un mes y medir solicitudes de otros roles para cerrar v1.0. 2) Mergear PR #1. 3) Considerar extender el regex de placeholders de emit-verdict a frases de elision en castellano (F32/F33). 4) Evaluar por que el Critic como subagente falla 3 de 4 gates: es la causa raiz detras de F29-F34.

### Pendientes heredados (sin cambios)

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

- Protocolo TRINCHERA para señalar patrones de franqueza que se afilan en conversaciones largas; se escribió en MEMORY.md. Se mantuvo el veto del humano para retirarlo.

### Heredadas (sin cambios)

- El modelo del juez era la causa dominante, no la forma de la tarea: se cambio con evidencia y con ADR, no con un patch de config. Cuando un gate es invalido se cierra por verificacion del CORE con nota explicita, nunca con veredicto provisional. Las reglas nuevas del kit no invalidan historia: los veredictos previos sin tabla quedan LEGACY informativo.

### Heredadas (sin cambios)

- Fallback cubre fallas, no lentitud (ADR-112, timeout 900s, Gemma local). CPACC retirado por falta de fondos, reapertura al primer ingreso real. Coexistencia OpenClaw+Antigravity en vez de migracion. El ROADMAP no es backlog: las tareas fechan en memory.db. Un numero de PR en un CV se cita por autoria, por review formal o por comentario propio, y las tres cosas se escriben distinto. Un auto-reporte de subagente no es un hecho: se verifica contra la fuente.

### Heredadas (sin cambios)

- Ejecutor A pasa a deepseek cuando gpt-oss reporta trabajo inexistente (override autorizado). Cierre por verificacion del CORE con nota explicita cuando el gate es invalido, nunca veredicto provisional. Match exacto por slug en el gate de veredictos: sin herencia entre -rN y base.

### Heredadas (sin cambios)

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
MEMORY.md
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
