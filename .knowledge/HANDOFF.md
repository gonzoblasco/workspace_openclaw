# HANDOFF - workspace

**Fecha:** 2026-11-04 22:15 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-04). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-04.md`.

---

## Que se hizo en esta sesion

CONTEXTO LEGAL (Expte. 15.533, Juzgado de Familia de Diamante, Visconti). Se leyeron integras las 17 fojas de la demanda por privacion de responsabilidad parental notificada el 03/11 a las 19:59 (traslado 12 dias, vence ~13/11) y la presentacion que la actora hizo una o dos semanas antes. Se produjeron tres documentos en ~/Documents/familia-vicente/: explicacion en castellano, notas de contestacion para la Dra. Betania Bolzan y modelo de programa de revinculacion con intermediario imparcial. HALLAZGO CENTRAL del ultimo tramo: la jueza no rechazo la propuesta de revinculacion, la dejo "como previo a evaluar" y le pidio a la Lic. ... dos preguntas: si es etica y tecnicamente compatible ser terapeuta individual de uno de los progenitores y conductor de la revinculacion, y si el vinculo terapeutico previo compromete la objetividad y la independencia. Ese es exactamente el punto que el modelo que prepare ya marcaba como exclusion (parte IV: el intermediario "no puede ser el terapeuta de ninguno de los progenitores"). La respuesta honesta a las dos preguntas es "no", y contestarla asi no debilita la posicion: permite que Zarate siga como terapeuta de Gonzo y que el proceso lo conduzca un profesional neutral de la lista del juzgado o del ETI. La notificacion del requerimiento a Zarate esta a cargo de Gonzo segun el propio escrito. Datos a favor que el informe de Zarate ya aporta y no se estaban usando: Gonzo estuvo al cuidado de su sobrina de 3 anos, dos veces por semana, en casa y en espacios publicos. Flancos: la frase sobre "solo se respondio uno de los tantos mensajes" es inverificable; y el escrito representa a Gonzo "en representacion de mi hijo Vicente", lo que afirma la responsabilidad parental que la demanda quiere quitarle.

## Estado actual

DOS FRENTES ABIERTOS. (a) LEGAL: demanda por privacion de responsabilidad parental (Expte. 15.533) notificada el 03/11, traslado vence ~13/11; en manos de la Dra. Betania Bolzan, con tres documentos preparados en ~/Documents/familia-vicente/. La jueza no rechazo la propuesta de revinculacion: la dejo 'como previo a evaluar' y pidio dos respuestas antes de decidir. (b) SISTEMA: allowlist de 24 modelos (21 cloud + 3 locales reales); studio en deepseek-v4.1-flash y planner en gpt-oss, ambos con gemma4:12b-mlx de fallback; ADR-090 coherente con config y DB. Estructura del workspace: projects/ (4), services/vane, oss/facebook-astryx, _workbench/onwheels; forks/ y clones/ vacios.

## Proximos pasos

1) LEGAL URGENTE: responder el requerimiento de la jueza sobre el rol del profesional. La respuesta honesta a las dos preguntas es 'no' (un terapeuta de parte no puede conducir la revinculacion), y va acompanada de una presentacion nueva que pida un conductor neutral de la lista del juzgado o del ETI. Coordinar con Betania antes de que nadie firme. 2) LEGAL: notificar el requerimiento al Lic. Zarate, a cargo de Gonzo segun el propio escrito. 3) LEGAL: contestar el traslado del 15.533 antes del ~13/11; corregir antes la frase del escrito de 2026 sobre las entrevistas del NAF (Moreyra reconoce haber citado al progenitor al encuadre inicial). 4) LEGAL: obtener constancias de la cuenta judicial 12.172 (desarma la acusacion de alimentos) y la resolucion de archivo del legajo penal 011.099 del 22/10/2022. 5) HEREDADO (2026-11-04 21:58): tarea discriminante de calidad: el recall saturo dos veces (8 de 8 modelos encontraron los 4 bugs); falta un prompt con clase 'premisa falsa' que discrimine. 6) HEREDADO (2026-11-04 21:58): TODO id 97 - auditoria de ADRs y configuracion general: inventario de definiciones duplicadas, un dueno por definicion, resolver ADRs huerfanos (el de STUDIO esta fuera de docs/adr), unificar las claves duplicadas de settings y gate que falle cuando dos fuentes vigentes discrepen. 7) HEREDADO (2026-11-04 16:10): seguimiento de Talent Connect (sin respuesta; segunda puntada si pasan 7-10 dias). 8) HEREDADO (2026-11-04 16:10): prep de la entrevista inicial con IA del aviso, si avanzan. 9) HEREDADO (2026-11-04 16:10): NO hay adaptador de Teamtailor en skills/job-application/scripts/ats/ (solo ashby, lever, eightfold, greenhouse). 10) HEREDADO (2026-11-04 16:10): los otros CVs (mural, mercor, team-international, code-evaluator) siguen con el conteo viejo de PRs. 11) HEREDADO (2026-11-04 16:10): deteccion de trabajo sin registrar en session-end.sh, con ADR propio. 12) HEREDADO (2026-11-04 16:10): modelo multi-proyecto, tambien con ADR. 13) HEREDADO (2026-11-04 16:10): GitHub Actions a Node 24 (checkout@v5, setup-node@v5, setup-python@v6) antes de la migracion a Ubuntu 26 del 19/10/2026. 14) Cuando aparezca un clon nuevo en forks/ para un PR, correr check-foreign-knowledge.py --install en un paso.

## Decisiones y contexto que no debe perderse

1) LEGAL (HOY 2026-11-04): el conductor de la revinculacion no puede ser el terapeuta de ninguna de las partes ni del nino. El modelo preparado ya lo excluia en su parte IV con el nombre incluido, y la propuesta presentada propuso a ese mismo profesional. Contestar 'no' a las dos preguntas de la jueza FORTALECE la posicion: el terapeuta sigue en su rol y el proceso lo conduce un neutral. 2) LEGAL (HOY): no se discute el Expte. 11.972 (medida autosatisfactiva por redes) porque esta firme y discutirlo debilita. No se niega el episodio de febrero 2024: se ataca la atribucion de autoria via pericia con observacion de la diada. 3) SISTEMA (2026-11-03): una excepcion es un olor a clasificacion equivocada. Si un repo necesita una exencion para cumplir una regla, el que esta mal es la carpeta (vane: forks/ -> services/). Un git checkout de comprobacion ESCRIBE, no lee. No inferir el estado de un hilo de memoria: correr pr-thread-brief.sh. 4) HEREDADAS (2026-11-04 21:58): (a) studio corre deepseek-v4.1-flash y planner se queda en gpt-oss; los dos con gemma4:12b-mlx. El fallback tiene que EXISTIR y ser barato. (b) Un ADR se corrige en el lugar, no se superpone con uno nuevo: ensanchar la serie obliga a leer varios ADR para reconstruir el estado. (c) Ante dos fuentes vigentes que se contradicen gana la que tiene evidencia medida, no la mas reciente. (d) Los modelos en desuso se purgan en dos capas: lista estatica y catalogo del picker. (e) El dato de la DB se busca por CONTENIDO en todas las tablas, no por el nombre de la clave. (f) Pipeline C, Auditoria de camino y Redaccion con Voz se resuelven como SKILLS con override de modelo por sessions_spawn, no como agentes con identidad: el test de tres condiciones no lo justifica y el bootstrap cuesta 1500-2800 tok/turno. (g) path-audit se dispara en CADA minor release (Gonzo acepta el costo: le encontro mejoras reales). (h) Kimi K3.1 Pro queda como convocado para auditoria de camino y redaccion decisiva, nunca titular de rol fijo (14-22x deepseek por request). (i) Con plan Legacy el costo se mide en cuota de GPU y slots de concurrencia, nunca en precio por token. 5) HEREDADAS (2026-11-04 16:10): En un CV no se ponen conteos de PRs ni carreras universitarias incompletas; la colaboracion si es material de CV (nunca de post); Figma y GraphQL no se declaran porque no son hechos del corpus. En la memoria, el dato crudo se versiona y el indice derivado se regenera (ADR-108). En la limpieza de scripts, huerfano no es lo mismo que prescindible. El cierre de sesion NO se canta sin commit, push y CI verde verificado.

## Cerrados en esta sesion

- commit de las 3 skills (path-audit, regression-net, voz-gonzo) y su gate
- purga de la allowlist de modelos (minimax-m2.7, mistral-large-3, nemotron-3-nano)
- cambios de rol de planner y studio
- el restart del picker no hizo falta: Gonzo confirmo que ve los modelos nuevos
- el chequeo de si el .knowledge de preflight habia quedado atras se resolvio como no-problema

## Archivos tocados

```
.knowledge/HANDOFF.md
.knowledge/SESSIONS.md
.knowledge/handoff-history/2026-10-27-1321-2-HANDOFF.md
.knowledge/handoff-history/2026-10-27-1636-HANDOFF.md
.knowledge/handoff-history/2026-10-27-1704-HANDOFF.md
.knowledge/handoff-history/2026-10-28-1810-HANDOFF.md
.knowledge/handoff-history/2026-10-28-1923-HANDOFF.md
.knowledge/handoff-history/2026-10-28-2131-HANDOFF.md
.knowledge/handoff-history/2026-11-04-2159-2-HANDOFF.md
memory/2026-11-04.md
memory/memory.db
scripts/session-handoff.py
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-04.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
