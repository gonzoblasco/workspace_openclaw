# HANDOFF - workspace

**Fecha:** 2026-11-18 22:15 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-18). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-18.md`.

---
## Que se hizo en esta sesion

### 2026-11-18 22:15
Cierre de la segunda parte de la sesion: infraestructura del MCP de GitHub y credenciales. (1) Se restauro el binario del MCP oficial github-mcp-server v2.2.0 (Darwin_arm64) en ~/.openclaw/bin/github-mcp via OPS, con dictamen APLICA CON CAMBIOS y limites duros respetados. Verifique la cadena de custodia por mi cuenta porque OPS reporto mal el checksum: el archivo oficial hashea el TARBALL (5e46b05b...), no el binario; tarball contra oficial OK, binario extraido contra instalado OK (11608433...). OPS habia comparado el hash del binario contra el archivo del tarball, que da distinto siempre. Funcional: 53 tools, get_me autentica, list_notifications responde. (2) Se registro el MCP como server del gateway (mcp.servers.github) via config.set, porque openclaw mcp set/add fallan con 'This operation requires exclusive offline state ownership' mientras el gateway corre. Token fuera del config: launcher ~/.openclaw/bin/github-mcp-launch (700) que lee el PAT del archivo 600 y lo exporta. (3) Bug propio encontrado y corregido: el binario necesita el subcomando 'stdio' en args; sin el imprime la ayuda y sale con exit 0, y el gateway lo veia como 'Connection closed'. Corregido con args=[stdio] y verificado con handshake real (starting server version=2.2.0, readOnly=false). (4) Hallazgo de seguridad: el token guardado no era el public_repo pedido sino un PAT con admin:enterprise, admin:org, delete_repo, workflow, user. Se reemplazo por un fine-grained github_pat_ que Gonzo paso por chat. Verificado: identidad gonzoblasco, lectura OK en meta/astryx y shadcn-ui/ui, wrapper OK. PERO la escritura FALLA: 'Resource not accessible by personal access token (addComment)'. Diagnostico: el fine-grained no tiene el repo en su allowlist con escritura (repository access en 'only select' o Issues en Read en vez de Read and write). No se puede distinguir de una aprobacion de org pendiente con el mensaje actual; el mensaje tipico de aprobacion de org es distinto. (5) Se cancelo el comentario de seguimiento en astryx#4652 por pedido de Gonzo; draft borrado, nada publicado. Pendiente critico: el PAT ancho (ghp_) sigue VIVO en la cuenta de GitHub aunque se borro la copia del disco, porque borrar el archivo no lo revoca. Hay que revocarlo en settings/tokens. Y el token vigente es de facto read-only hasta que se corrija su permiso de Issues.

Estado de los hilos al cierre: ariakit#4058 cerrado (fix en 0.4.43); astryx#7871 mergeado en v0.7.12; astryx#4690 abierto y en conflicto, sin comentar por decision; astryx#4652 abierto con nuestra medicion DOM publicada; shadcn#11757 abierto con nuestro comentario publicado.

### 2026-11-18 14:55
Auditoria y arreglo de la skill growing-doc-retention: por que contaba como 'menos usada' y que tenia de aprovechable. Conclusion: es una skill de instalacion, no de invocacion (se leyo 2026-10-06 y 2026-10-14); su mecanismo son dos scripts que corren solos, asi que un contador de invocaciones siempre marca cero. Al medirla aparece el hueco real: dreams-rotate.py tenia un solo DREAMS.md hardcodeado cuando ya existian OCHO (raiz + agents/*/). Cuatro diarios de agente (dev, critic, auditor, mind) guardaban septiembre y octubre en el activo y '--check' daba verde porque no los miraba: el modo de falla que la propia skill advierte (gate colgado donde el doc ya no vive). Arreglado: el script enumera instancias, archiva por agente en memory/archive/dreaming/agents/<agente>/, '--check' nombra las desfasadas y '--dry-run' reporta por instancia. Aplicado al workspace: 53 entradas archivadas (dev 21, critic 11, mind 11, auditor 10), 103 activas en 8 diarios, 133 entradas antes y 133 despues, verificado agente por agente contra el backup. La revision B (kanam-critic) encontro dos defectos reales que se corrigieron: D1 el activo se reescribia ANTES que el archivo, asi que un fallo de I/O borraba entradas para siempre con --check verde (reproducido: 34 a 23 en kanam-dev); ahora se persiste el archivo primero, con escritura atomica (tmp + os.replace), error por instancia con exit 2 sin abortar el lote y guarda contra duplicar un bloque en un reintento. D2 el test 9 pasaba por casualidad (!grep sobre un archivo borrado tambien da verde); se cubrio con [ -f ] + marcadores y se verifico por mutacion (borrando el diario del agente fallan 4 tests). 13/13 bats, check-refs 757/757, bootstrap OK, single-source OK. Commit aeae49319d, pusheado (46dfb57c14..aeae49319d) con CI verde en Skill Scripts CI. El push llevo tambien los dos commits del cierre del narrador que estaban en main local.

### 2026-11-18 14:53
Barrido de 4 notificaciones de GitHub, con dos comentarios publicados. (1) ariakit#4058: cerrado COMPLETED por el PR #8360 de diegohaz (hideWhenAnchorHidden con el middleware hide de Floating UI + hoverOnScroll), publicado en @ariakit/react 0.4.43. Nuestro comentario de julio quedo acreditado en Acknowledgments del PR, pero la implementacion final descarto la propuesta del listener de scroll por una geometria sin listeners. (2) astryx#7871: mergeado en v0.7.12; el review no solicitado del 23-oct fue adoptado en silencio (cero respuestas, cero reacciones, cero mencion). El codigo final resolvio la ambiguedad en la direccion de la lectura 1 que planteamos - isTopLayer + enclosingModalDialog en tiempo de escritura, FR10 reescrito con 'otherwise through the shared channel, adds no live container of its own', dos bindings nuevas toast-*-announcement-top-layer y la exclusion enganosa 'bound above' eliminada. (3) astryx#4690: abierto pero CONFLICTING desde el 5-nov; dos comentarios nuestros. El ruling de cixzhang del 27-ago reusa nuestra frase 'existing interactive descendants must remain reachable', pero la implementacion eligio justo el punto medio que advertimos: fila focusable Y controles in-cell en el tab order, documentado como divergencia #2 del APG. Decision: no comentar (aprobado, trabado en rebase, follow-up ya rastreado en #4611). (4) astryx#4652: remido dos veces - primero tokens y despues componentes reales. Se armo forks/astryx-demo (Vite + React 19 + core 0.7.16, temas compilados con esbuild desde el source de main) y se midio con Playwright sobre Chrome: dots inactivos 1.09-1.68:1 en todos los temas (fallan 3:1 de 1.4.11), activo 4.02-16.71:1; badge verde solido en stone 7.19:1, translucido en base/chocolate/matcha 2.43/1.24/1.31:1 sobre card #686D57. Los numeros base reproducen exactos los de agosto (1.20:1 y 2.43:1), lo que valido el arnes. Comentario publicado. (5) shadcn#11757: comentario publicado apuntando al ruling de atomiks en mui/base-ui#5633 (cerrado como intencional, APG select-only combobox + macOS) para evitar que el fix se implemente en la capa equivocada: select.tsx es literalmente SelectPrimitive.Root y openOnArrowKeyDown es interno de useListNavigation. (6) Credenciales: gh solo tenia tokens OAuth y la org meta bloquea OAuth Apps para escritura; se creo ~/.openclaw/secrets/github-token (600) con un PAT classic public_repo y desde entonces gh escribe en orgs restringidas con GH_TOKEN desde el archivo. El MCP de GitHub sigue sin binario (~/.openclaw/bin/github-mcp) y sin egressProxy. Limpieza: se removio un SingletonLock huerfano del perfil de browser imported que apuntaba al hostname viejo. Pendiente: decidir si se borran forks/astryx y forks/astryx-demo.

### 2026-11-18 14:21
TTS: el narrador del audiolibro quedo definido y reutilizable. Se probaron cuatro motores en la noche. Kokoro se descarto no por sucio sino por plano: es no autoregresivo y calcula la entonacion de la estructura del texto, asi que siempre cae al final. Medido: 'Viste a Vera.' y 'Viste a Vera?' dan el mismo contorno (154 a 103 y 154 a 105 Hz). Con 1432 lineas de dialogo en el libro, todas las preguntas sonaban a afirmacion. Quedo Chatterbox clonando una referencia: em_alex de Kokoro bajado 4 semitonos, que da 100-104 Hz de tono y 11.400 Hz de banda, y entona. La clave fue bajar el tono de la REFERENCIA y no del audio final: filtrar el resultado costaba 1,6 kHz de banda (10.185 a 8.564 Hz) y sonaba apagado. Se corrigieron cuatro bugs del pipeline: las notas de produccion *POV: ...* se narraban en 14 capitulos; las rayas llegaban al fonemizador como caracter desconocido y metian 60 ms de sonido fantasma antes de cada vocal ('Ah' sonaba 'nahh'); el corte a 240 caracteres partia palabras y hacia alucinar la cola (7,6 s); y el -3 semitonos aplicado al resultado apagaba la voz. El narrador quedo reutilizable: la voz vive en assets/voces/baritono-jazz/ con manifiesto y valores medidos, y el script la resuelve por nombre (--voz baritono-jazz), asi que cualquier proyecto usa el mismo narrador sin copiar rutas. ADR-116 reemplaza al ADR-115, que quedo archivado. El render de los 17 capitulos corre en background: capitulo 1 listo en 5:37 de audio y 24,7 minutos, unos 4,4x el tiempo real.

### 2026-11-18 03:11
Auditoria de la skill growing-doc-retention y de la tabla de scripts de SETUP.md. La skill resulto no estar sin usar: es de instalacion y su mecanismo (changelog-rotate.py 14d, dreams-rotate.py mensual, gates en pre-commit y session-end) corre verde y verificado. De las tres ideas que propuse adaptar, dos no eran candidatos (modelos ya managed en AGENTS.md/SETUP.md; estado de OPS inexistente en MEMORY.md) y la tercera (tabla de scripts) revelo un problema distinto: 142 scripts en disco contra ~30 filas, mezclando catalogo vivo con actas de defuncion.

Programa scripts-inventory creado en agents/kanam-planner/.knowledge/programs/ (plan_lint OK). El Planner fallo DOS veces devolviendo el JSON como prosa sin escribir archivo y encima duplico la ruta (agents/kanam-planner/agents/kanam-planner/); el CORE escribio el programa contra el esquema real copiado de skill-router-improvement.json.

Ejecutado el inventario: 142 scripts medidos, distribuidos por referencias (9 con 0, 18 con 1, 52 con 2-4, 63 con 5+). Los 9 huerfanos son todos de la Cata de Harnesses (octubre 2026), evento cerrado, salvo heartbeat-snapshot.sh (infra viva del job agentTurn) y moltbook-ingest.py (confirmado vivo por Gonzo: rutina de revision periodica de sitios para noticias, con dev.to agregado el mismo dia).

FALLO GRAVE DE REPORTE: se declaro implementado un bloque managed que no existia. Se guardo una tabla entera como valor del setting scripts_inventory, cuando managed-blocks.py solo genera bloques desde templates hardcodeados en BLOCKS (lineas 118-174) e interpola variables escalares; apply dijo 'al dia' sin escribir nada. El gate del pre-commit llamaba a un --check que devolvia exit 1 permanente. Se uso ADR-113 sin verificar que el 114 ya existia. La auditoria de Gonzo ('auditar y verificar el output anterior') encontro todo esto.

## Estado actual

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

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-18.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*

## Archivos tocados

```
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
