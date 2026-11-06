# HANDOFF - workspace

**Fecha:** 2026-11-05 22:58 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-05). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-05.md`.

---

## Que se hizo en esta sesion

Hebrus retirado tras evaluacion empirica: compila limpio (make -j8 metal, EXIT=0), corre Qwen3.6-35B-A3B en guarded SSD a prefill 8.61 t/s y generation 7.79 t/s en M4 de 24 GiB, sin swap nuevo. Pero el modelo NO entra en RAM (19.37 GiB vs 17.76 de working set) y DeepSeek V4 Flash exige 64 GiB (ds4_ssd.c:584). Se borro forks/hebrus completo (19 GB, trash). forks/ queda vacia.

## Estado actual

Hebrus retirado, forks/ vacia, sin cambios de config. DeepSeek local bloqueado por hardware (piso 64 GiB de memoria unificada).

## Proximos pasos


1) 1. Verificar la deteccion de estancamiento de llm.sh contra un cuelgue reproducible. 2) LEGAL URGENTE: responder el requerimiento de la jueza sobre el rol del profesional. La respuesta honesta a las dos preguntas es 'no' (un terapeuta de parte no puede conducir la revinculacion), y va acompanada de una presentacion nueva que pida un conductor neutral de la lista del juzgado o del ETI. Coordinar con Betania antes de que nadie firme. 3) LEGAL: notificar el requerimiento al Lic. Zarate, a cargo de Gonzo segun el propio escrito. 4) LEGAL: contestar el traslado del 15.533 antes del ~13/11; corregir antes la frase del escrito de 2026 sobre las entrevistas del NAF (Moreyra reconoce haber citado al progenitor al encuadre inicial). 5) LEGAL: obtener constancias de la cuenta judicial 12.172 (desarma la acusacion de alimentos) y la resolucion de archivo del legajo penal 011.099 del 22/10/2022. 6) HEREDADO (2026-11-04 21:58): tarea discriminante de calidad: el recall saturo dos veces (8 de 8 modelos encontraron los 4 bugs); falta un prompt con clase 'premisa falsa' que discrimine. 7) HEREDADO (2026-11-04 21:58): TODO id 97 - auditoria de ADRs y configuracion general: inventario de definiciones duplicadas, un dueno por definicion, resolver ADRs huerfanos (el de STUDIO esta fuera de docs/adr), unificar las claves duplicadas de settings y gate que falle cuando dos fuentes vigentes discrepen. 8) HEREDADO (2026-11-04 16:10): seguimiento de Talent Connect (sin respuesta; segunda puntada si pasan 7-10 dias). 9) HEREDADO (2026-11-04 16:10): prep de la entrevista inicial con IA del aviso, si avanzan. 10) HEREDADO (2026-11-04 16:10): NO hay adaptador de Teamtailor en skills/job-application/scripts/ats/ (solo ashby, lever, eightfold, greenhouse). 11) HEREDADO (2026-11-04 16:10): los otros CVs (mural, mercor, team-international, code-evaluator) siguen con el conteo viejo de PRs. 12) HEREDADO (2026-11-04 16:10): deteccion de trabajo sin registrar en session-end.sh, con ADR propio. 13) HEREDADO (2026-11-04 16:10): modelo multi-proyecto, tambien con ADR. 14) HEREDADO (2026-11-04 16:10): GitHub Actions a Node 24 (checkout@v5, setup-node@v5, setup-python@v6) antes de la migracion a Ubuntu 26 del 19/10/2026. 15) Cuando aparezca un clon nuevo en forks/ para un PR, correr check-foreign-knowledge.py --install en un paso. 16) Si aparece una maquina con >=64 GiB de memoria unificada, el experimento Hebrus se repite en una tarde: clonar forks/, make -j8 metal, download_model.sh deepseek-v2, correr con AUTO.

## Decisiones y contexto que no debe perderse


1) LEGAL (HOY 2026-11-04): el conductor de la revinculacion no puede ser el terapeuta de ninguna de las partes ni del nino. El modelo preparado ya lo excluia en su parte IV con el nombre incluido, y la propuesta presentada propuso a ese mismo profesional. Contestar 'no' a las dos preguntas de la jueza FORTALECE la posicion: el terapeuta sigue en su rol y el proceso lo conduce un neutral. 2) LEGAL (HOY): no se discute el Expte. 11.972 (medida autosatisfactiva por redes) porque esta firme y discutirlo debilita. No se niega el episodio de febrero 2024: se ataca la atribucion de autoria via pericia con observacion de la diada. 3) SISTEMA (2026-11-03): una excepcion es un olor a clasificacion equivocada. Si un repo necesita una exencion para cumplir una regla, el que esta mal es la carpeta (vane: forks/ -> services/). Un git checkout de comprobacion ESCRIBE, no lee. No inferir el estado de un hilo de memoria: correr pr-thread-brief.sh. 4) HEREDADAS (2026-11-04 21:58): (a) studio corre deepseek-v4.1-flash y planner se queda en gpt-oss; los dos con gemma4:12b-mlx. El fallback tiene que EXISTIR y ser barato. (b) Un ADR se corrige en el lugar, no se superpone con uno nuevo: ensanchar la serie obliga a leer varios ADR para reconstruir el estado. (c) Ante dos fuentes vigentes que se contradicen gana la que tiene evidencia medida, no la mas reciente. (d) Los modelos en desuso se purgan en dos capas: lista estatica y catalogo del picker. (e) El dato de la DB se busca por CONTENIDO en todas las tablas, no por el nombre de la clave. (f) Pipeline C, Auditoria de camino y Redaccion con Voz se resuelven como SKILLS con override de modelo por sessions_spawn, no como agentes con identidad: el test de tres condiciones no lo justifica y el bootstrap cuesta 1500-2800 tok/turno. (g) path-audit se dispara en CADA minor release (Gonzo acepta el costo: le encontro mejoras reales). (h) Kimi K3.1 Pro queda como convocado para auditoria de camino y redaccion decisiva, nunca titular de rol fijo (14-22x deepseek por request). (i) Con plan Legacy el costo se mide en cuota de GPU y slots de concurrencia, nunca en precio por token. 5) HEREDADAS (2026-11-04 16:10): En un CV no se ponen conteos de PRs ni carreras universitarias incompletas; la colaboracion si es material de CV (nunca de post); Figma y GraphQL no se declaran porque no son hechos del corpus. En la memoria, el dato crudo se versiona y el indice derivado se regenera (ADR-108). En la limpieza de scripts, huerfano no es lo mismo que prescindible. El cierre de sesion NO se canta sin commit, push y CI verde verificado. 6) VEREDICTO HEBRUS (2026-11-05): funciona pero no conviene en 24 GiB. Compila limpio y corre Qwen3.6-35B-A3B en guarded SSD a prefill 8.61 t/s y generation 7.79 t/s en el M4, sin swap nuevo. El motivo del retiro no es la velocidad: el modelo NO entra en RAM (19.37 GiB vs 17.76 de working set) y DeepSeek V4 Flash exige 64 GiB (ds4_ssd.c:584). Un proceso de ~20 GB que no cabe compite de forma permanente con el gateway, Ollama y los 6.5/8 GB de swap ya en uso. Se borro forks/hebrus (19 GB, trash); forks/ queda vacia.

## Archivos tocados

```
memory/2026-11-05.md
memory/memory.db
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-05.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
