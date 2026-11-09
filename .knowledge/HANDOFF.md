# HANDOFF - Workspace

**Fecha:** 2026-11-09 15:21 GMT-3
**Proyecto:** Workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-09). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-09.md`.

---

## Que se hizo en esta sesion

Re-evaluación de la clase `studies/entrevistas-tecnicas/` (charla de Nerdearla Chile 2026, Tatiana Rodríguez) con `deepseek-v4.1-flash`, a pedido de Gonzo. Se auditó el outline v1 contra la transcripción ASR y las fuentes oficiales (NERDflix, perfil de speaker, Frontiers 2025) y se aplicó una v2: identidad corregida (el ASR decía «Diana»; es Tatiana Rodríguez / @tatanomada), claim del horario documentado (estudio de 104.552 exámenes orales: pico 11-13 h, no 2 p.m.), orden 1.5/1.6 alineado al video, mapa temporal reconstruido, condición del correo de cierre agregada, glosario de ASR en el transcript y ejemplos de LinkedIn. Se creó `AUDIT-2026-11-09.md`. Los claims del 85 % (HackerRank) y 40 % (práctica deliberada) no tienen fuente localizable: quedan como afirmaciones de la speaker, no como estadísticas.

## Estado actual

Clase v2 y auditoría listas en `studies/entrevistas-tecnicas/`; transcript con glosario; README actualizado. Cambios locales sin commit. Pendiente: estudiar la clase (Módulo 0/1) y decidir si se reemplazan los porcentajes sin fuente.

## Proximos pasos

1. Estudiar la clase v2 con Gonzo: Módulo 0 (marco) y Módulo 1.1 (auditoría de LinkedIn).
2. Commit local de `studies/README.md`, `studies/entrevistas-tecnicas/outline.md`, `transcripcion.md` y `AUDIT-2026-11-09.md`.
3. Push cuando Gonzo lo autorice.
4. Deuda de la clase: verificar contra audio el nombre de la speaker; reemplazar o sacar los claims del 85 % y 40 % si la clase se publica; identificar «Qway»/«PNP» o dejarlos marcados como ASR dudoso.
5. HEREDADOS (del cierre 2026-11-08; sin cambios):
0) CERRAR E3.3 con un cambio real de config de bajo riesgo: pre-flight a OPS, veredicto registrado, aplicacion con backup y evidencia real. Sin eso el entregable sigue abierto. 0-bis) AGENTS.md a 8 chars del cap: mover texto a docs/ antes de cualquier adicion. 0-ter) Resolver el drift de version de kanam-critic y kanam-studio para que el pre-commit vuelva a verde y no haya que usar --no-verify. 0-quater) Push de los dos commits de esta sesion (git pull --rebase + push) cuando Gonzo lo autorice. 1) 1. Verificar la deteccion de estancamiento de llm.sh contra un cuelgue reproducible. 2) LEGAL URGENTE: responder el requerimiento de la jueza sobre el rol del profesional. La respuesta honesta a las dos preguntas es 'no' (un terapeuta de parte no puede conducir la revinculacion), y va acompanada de una presentacion nueva que pida un conductor neutral de la lista del juzgado o del ETI. Coordinar con Betania antes de que nadie firme. 3) LEGAL: notificar el requerimiento al Lic. Zarate, a cargo de Gonzo segun el propio escrito. 4) LEGAL: contestar el traslado del 15.533 antes del ~13/11; corregir antes la frase del escrito de 2026 sobre las entrevistas del NAF (Moreyra reconoce haber citado al progenitor al encuadre inicial). 5) LEGAL: obtener constancias de la cuenta judicial 12.172 (desarma la acusacion de alimentos) y la resolucion de archivo del legajo penal 011.099 del 22/10/2022. 6) HEREDADO (2026-11-04 21:58): tarea discriminante de calidad: el recall saturo dos veces (8 de 8 modelos encontraron los 4 bugs); falta un prompt con clase 'premisa falsa' que discrimine. 7) HEREDADO (2026-11-04 21:58): TODO id 97 - auditoria de ADRs y configuracion general: inventario de definiciones duplicadas, un dueno por definicion, resolver ADRs huerfanos (el de STUDIO esta fuera de docs/adr), unificar las claves duplicadas de settings y gate que falle cuando dos fuentes vigentes discrepen. 8) HEREDADO (2026-11-04 16:10): seguimiento de Talent Connect (sin respuesta; segunda puntada si pasan 7-10 dias). 9) HEREDADO (2026-11-04 16:10): prep de la entrevista inicial con IA del aviso, si avanzan. 10) HEREDADO (2026-11-04 16:10): NO hay adaptador de Teamtailor en skills/job-application/scripts/ats/ (solo ashby, lever, eightfold, greenhouse). 11) HEREDADO (2026-11-04 16:10): los otros CVs (mural, mercor, team-international, code-evaluator) siguen con el conteo viejo de PRs. 12) HEREDADO (2026-11-04 16:10): deteccion de trabajo sin registrar en session-end.sh, con ADR propio. 13) HEREDADO (2026-11-04 16:10): modelo multi-proyecto, tambien con ADR. 14) HEREDADO (2026-11-04 16:10): GitHub Actions a Node 24 (checkout@v5, setup-node@v5, setup-python@v6) antes de la migracion a Ubuntu 26 del 19/10/2026. 15) Cuando aparezca un clon nuevo en forks/ para un PR, correr check-foreign-knowledge.py --install en un paso. 16) Si aparece una maquina con >=64 GiB de memoria unificada, el experimento Hebrus se repite en una tarde: clonar forks/, make -j8 metal, download_model.sh deepseek-v2, correr con AUTO. 17) Interna.work (2026-11-06): esperar respuesta de talents@interna.work hasta el 2026-11-11; si no hay respuesta sustantiva o solo mandan un link a formulario, cerrar en el tracker sin recontacto. 18) Infjini/Disney: fijar por escrito con Siraj la fecha y el formato de la entrevista de noviembre. 19) abya-yala: el roadmap 0.5 sigue sin aprobar; el gate abierto es la decision del arquero dominado.
20) REA (2026-11-06): evaluado y no adoptado. Si se retoma, el caso util es TypeScript con source maps, no un bundle webpack minificado; la decompilacion nativa exige Hopper o Ghidra y ninguno esta instalado (doctor reporta ambos ausentes).
3. NUEVO (sesion 2026-11-08 - Feltsense AI Engineer):
0) Aprobar o pedir cambios al CV y formulario Ashby; luego OK explicito para Submit Application (nada sale sin ok).
1) Confirmar numero salarial objetivo para la llamada (rango puesto 60-110k USD; referencia historica 85-95k).
2) Confirmar titulo de header del CV ('AI Engineer - Agent Systems, LLM Backends').
3) Tras envio del formulario: agregar fila en docs/entrevistas/_general/job-search-tracker.md y actualizar CV final.
4) Commit/push del workspace (docs + cv + real-browser.mjs + cambios).

## Decisiones y contexto que no debe perderse

- La clase ya existía; el pedido fue re-evaluarla con el modelo presente, no recrearla. Se auditó contra la fuente, no se re-transcribió.
- El ASR no es autoridad para nombres propios: «Diana» en 28.0 s es un error; la identidad oficial es Tatiana Rodríguez (@tatanomada), confirmada por NERDflix y el perfil de speaker de Nerdearla.
- El claim del horario se corrige con evidencia: Frontiers 2025 (104.552 exámenes orales) muestra pico 11-13 h y caída en los extremos; no sostiene el «2 p.m.» exacto ni equipara exámenes orales con entrevistas laborales.
- Los porcentajes sin fuente (85 % HackerRank, 40 % práctica deliberada) se mantienen etiquetados como claims; no se usan como estadísticas.
- Los cambios quedan en local; el push requiere OK explícito de Gonzo.
- HEREDADAS (del cierre 2026-11-08; sin cambios):
- que no debe perderse
0) PRE-FLIGHT DE OPS (2026-11-06): desde `c2a020b7dc`, ningun cambio de config, canales, plugins, automatizaciones ni credenciales se aplica sin veredicto previo de OPS (APLICA / NO APLICA / APLICA CON CAMBIOS). Adoptado como regla operativa del CORE, no como cambio de sustrato: tocar AGENTS.md no pasa por OPS. El limite de aprobacion no se delega: restart, borrado o produccion exigen OK explicito de Gonzo. 0-bis) El pre-flight NO cierra E3.3 por si solo: el criterio es el primer veredicto real en el change log, no la regla escrita. 0-ter) El texto externo que paso Gonzo se verifico contra el repo antes de adoptarlo; el documento citaba a OPS pero no tenia el paso de dry-run. 0-quater) Un archivo de otra sesion que aparece en `git status` se lee como contexto y no se commitea, aunque sea tentador ordenar el arbol. 0-quinquies) Ante un pre-commit rojo por archivos ajenos, se documenta la causa y se usa `--no-verify`; no se arreglan roadmaps de otros roles. 1) LEGAL (HOY 2026-11-04): el conductor de la revinculacion no puede ser el terapeuta de ninguna de las partes ni del nino. El modelo preparado ya lo excluia en su parte IV con el nombre incluido, y la propuesta presentada propuso a ese mismo profesional. Contestar 'no' a las dos preguntas de la jueza FORTALECE la posicion: el terapeuta sigue en su rol y el proceso lo conduce un neutral. 2) LEGAL (HOY): no se discute el Expte. 11.972 (medida autosatisfactiva por redes) porque esta firme y discutirlo debilita. No se niega el episodio de febrero 2024: se ataca la atribucion de autoria via pericia con observacion de la diada. 3) SISTEMA (2026-11-03): una excepcion es un olor a clasificacion equivocada. Si un repo necesita una exencion para cumplir una regla, el que esta mal es la carpeta (vane: forks/ -> services/). Un git checkout de comprobacion ESCRIBE, no lee. No inferir el estado de un hilo de memoria: correr pr-thread-brief.sh. 4) HEREDADAS (2026-11-04 21:58): (a) studio corre deepseek-v4.1-flash y planner se queda en gpt-oss; los dos con gemma4:12b-mlx. El fallback tiene que EXISTIR y ser barato. (b) Un ADR se corrige en el lugar, no se superpone con uno nuevo: ensanchar la serie obliga a leer varios ADR para reconstruir el estado. (c) Ante dos fuentes vigentes que se contradicen gana la que tiene evidencia medida, no la mas reciente. (d) Los modelos en desuso se purgan en dos capas: lista estatica y catalogo del picker. (e) El dato de la DB se busca por CONTENIDO en todas las tablas, no por el nombre de la clave. (f) Pipeline C, Auditoria de camino y Redaccion con Voz se resuelven como SKILLS con override de modelo por sessions_spawn, no como agentes con identidad: el test de tres condiciones no lo justifica y el bootstrap cuesta 1500-2800 tok/turno. (g) path-audit se dispara en CADA minor release (Gonzo acepta el costo: le encontro mejoras reales). (h) Kimi K3.1 Pro queda como convocado para auditoria de camino y redaccion decisiva, nunca titular de rol fijo (14-22x deepseek por request). (i) Con plan Legacy el costo se mide en cuota de GPU y slots de concurrencia, nunca en precio por token. 5) HEREDADAS (2026-11-04 16:10): En un CV no se ponen conteos de PRs ni carreras universitarias incompletas; la colaboracion si es material de CV (nunca de post); Figma y GraphQL no se declaran porque no son hechos del corpus. En la memoria, el dato crudo se versiona y el indice derivado se regenera (ADR-108). En la limpieza de scripts, huerfano no es lo mismo que prescindible. El cierre de sesion NO se canta sin commit, push y CI verde verificado. 6) VEREDICTO HEBRUS (2026-11-05): funciona pero no conviene en 24 GiB. Compila limpio y corre Qwen3.6-35B-A3B en guarded SSD a prefill 8.61 t/s y generation 7.79 t/s en el M4, sin swap nuevo. El motivo del retiro no es la velocidad: el modelo NO entra en RAM (19.37 GiB vs 17.76 de working set) y DeepSeek V4 Flash exige 64 GiB (ds4_ssd.c:584). Un proceso de ~20 GB que no cabe compite de forma permanente con el gateway, Ollama y los 6.5/8 GB de swap ya en uso. Se borro forks/hebrus (19 GB, trash); forks/ queda vacia. 7) OUTREACH (2026-11-06): contestar cold outreach sin links ni adjuntos no tiene riesgo tecnico; el costo real es que la respuesta califica el lead. El plazo para cerrar lo fija la claim publicada del remitente (24-48 business hours), no una espera indefinida. Un pago 'por entregable aprobado' exige criterio de aprobacion escrito antes de aceptar, y un cliente sin nombre no es una oferta.
8) REA (2026-11-06): repo morluto/rea verificado como genuino en cinco capas (repo, owner, npm con attestations SLSA, tarball con hash coincidente, cero hooks y cero canal de exfiltracion) y util solo para inventariar bundles ajenos: sobre un bundle minificado devuelve estructura, no comportamiento (0,9% de las relaciones describen calls/awaits/returns). Un repo genuino y una herramienta que nos sirve son dos preguntas distintas.
- NUEVO (2026-11-08):
- Educacion omitida en CV para este JD porque no pide degree; solo formacion/Training (Digital House bootcamp 2018 + Deque programa 2021), segun references/educacion.md y correccion de Gonzo.
- La seccion de contribuciones no-code (reviews/comentarios/diagnosticos) debe ir justo debajo de los PR mergeados en el CV.
- Form ATS Ashby de Feltsense AI Engineer preparado y verificado, con reemplazo de CV corregido; submit no realizado (requiere OK explicito).
- Adaptador real-browser.mjs se corrigio para usar Playwright de projects/kanam-fixer en vez de a11y-fixer archivado.

## Archivos tocados

```
docs/CHANGELOG.md
docs/archive/CHANGELOG-archive.md
studies/README.md
studies/entrevistas-tecnicas/outline.md
studies/entrevistas-tecnicas/transcripcion.md
studies/entrevistas-tecnicas/AUDIT-2026-11-09.md
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-09.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
