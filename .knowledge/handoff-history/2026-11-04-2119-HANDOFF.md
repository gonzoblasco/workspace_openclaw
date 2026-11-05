# HANDOFF - workspace

**Fecha:** 2026-11-04 21:19 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-04). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-04.md`.

---

## Que se hizo en esta sesion

CATA DE MODELOS OLLAMA CLOUD Y TRES SKILLS NUEVAS. (1) CATALOGO: la lista cloud son 24 modelos y no 20: la pagina carga por HTMX con scroll infinito (hx-trigger=revealed), asi que web_fetch y curl devuelven solo los primeros 20. Faltaban gpt-oss, deepseek-v4-pro, kimi-k2.6 y mistral-large-3. (2) RETIROS: nemotron-3-nano:30b, mistral-large-3 y minimax-m2.7 se retiran el 2026-11-09. El aviso vive en el MAIL y en usage settings, nunca en la ficha del modelo. (3) ENCUADRE: con plan Legacy el costo no es precio por token sino cuota de GPU y slots de concurrencia (tres, y el 429 es por cuenta, no por modelo). Kanam armo tablas de precio por token antes de corregir el eje. (4) CATA DE 9 MODELOS sobre un artefacto con 4 bugs sembrados: 8 de 8 encontraron los 4, o sea recall SATURADO que no rankea calidad. Consumo 48 requests y ~47k tokens. ERROR PROPIO CORREGIDO EN LA SESION: deepseek y minimax devolvieron 0 content con num_predict=8192 y parecia el modo de fallo de minimax; era el TOPE de tokens, no el modelo. Con 24000 los dos dieron 4 de 4. Leccion: num_predict minimo 16000 en toda cata futura. Dato: con tope suficiente deepseek gasto MAS tokens que minimax (9161 contra 7953) en esa tarea. (5) CATA DISCRIMINANTE K3.1 Pro contra DeepSeek en tres tareas sin codigo (planificacion, auditoria de camino, creativo): los marcadores volvieron a saturar (4 de 4), el juicio fue por lectura. DeepSeek gano planificacion (unico que dio un umbral accionable: ~15% de barra por dia con corte a 85-90%) y auditoria (encontro lo que Kimi no vio: el SSRF guard solo prueba los casos listados, y uso el caso gpt-oss como contraejemplo de prompt model-agnostic). Kimi gano creativo: 'me hubiera gustado otro resultado' contra 'me rechazaron', no cede el sujeto. Costo casi identico (1386 contra 1336 tokens). Conclusion: DeepSeek para lo operativo, Kimi para el matiz. (6) CUOTA MEDIDA EN PIXELES sobre capturas del panel: barra semanal 933 px para 4484 requests (0,065 px/req) y barra de sesion 937 px para 287 requests (0,49 px/req). Un request de K3.1 son 7 px, el 4,7% de la sesion; la estimacion previa de 'casi 10%' era el doble de la real. Las dos ventanas no dan el mismo px/req porque una request no cuesta lo mismo que otra, asi que el costo se expresa como rango: 14 a 22 veces deepseek. (7) LICENCIA DE MUSE verificada: la restriccion de USD 20M aplica solo a Model-as-a-Service; el uso interno no tiene restriccion. Unica obligacion: mostrar 'Built with Muse Spark Open' en la UI de un producto. (8) TEST DE TRES CONDICIONES para decidir agente contra skill (acumula contexto propio, mandato recurrente, modelo distinto al CORE): ningun candidato paso las tres. Pipeline C, Auditoria de camino y Redaccion con Voz quedan como SKILLS; Triage ni eso, es gemma4 con un prompt corto. Costo de un agente medido: 1500 a 2800 tokens por turno solo de bootstrap. (9) TRES SKILLS CREADAS Y PROBADAS: skills/path-audit (auditoria de CAMINO en CADA minor release, no lee codigo, sale a .knowledge/AUDIT.md con afirmaciones-no-probadas), skills/regression-net (Pipeline C: un test por finding de B y gate de mutacion obligatorio, toda mutacion detectada o la unidad queda abierta) y skills/voz-gonzo (lee docs/voz-gonzo.md como fuente unica mas gate ejecutable check-voz.py: cero violaciones en un texto limpio y ocho en uno sucio). Mas scripts/check-audit-due.py, que compara minor a minor y marca 'fix (no aplica)' en la linea 0.0.x. SKILLS-INDEX actualizado y check-refs en verde con 692 rutas. (10) FRENO POR CONTRADICCION: PreFlight declaraba tres versiones distintas (package.json 0.2.0, STATUS.md 0.1.0, y Gonzo dijo 0.6). Gonzo aclaro que estaba trabajando sin guardar sesion y que no era problema de Kanam; tema cerrado, queda pendiente que el numero de version tenga un solo dueno. (11) ERROR PROPIO DE CIERRE, corregido en la sesion: al regenerar este HANDOFF la primera vez SOBRESCRIBI en vez de FUSIONAR, y se perdieron 8 pendientes heredados de la sesion de las 16:10. La regla ya estaba escrita en session-close-handoff (paso 3: leer el vigente, clasificar en sigue-vivo/hecho/cambio, fusionar en los flags). Re-hecho con los heredados conservados y marcados con su origen.

## Estado actual

Skills curadas y sin commitear (git status: SKILLS-INDEX.md modificado + 4 entradas nuevas sin trackear). Cata documentada en docs/ecosystem/cata-catalogo-ollama-cloud-2026-11-04.md. CI verde en los tres commits del dia 2026-11-04 (9a0c619d8c, 32671c04fa, ac3317a73c) <!-- vigente desde 2026-11-04 16:10 -->.

## Proximos pasos

1. DE HOY (2026-11-04 21:18): 1) Purgar minimax-m2.7, mistral-large-3 y nemotron-3-nano:30b de modelPolicy.allow ANTES del 2026-11-09 (se retiran). 2) Cambios de rol propuestos: planner y studio a deepseek-v4.1-flash. 3) Commitear las 3 skills + check-audit-due.py cuando Gonzo lo autorice. 4) Tarea discriminante de calidad pendiente: el recall saturo dos veces seguidas, falta un prompt con clase 'premisa falsa'.
2. HEREDADOS <!-- vigente desde 2026-11-04 16:10 -->: 5) Seguimiento de Talent Connect (sin respuesta; segunda puntada si pasan 7-10 dias). 6) Prep de la entrevista inicial con IA del aviso, si avanzan. 7) NO hay adaptador de Teamtailor en skills/job-application/scripts/ats/ (solo ashby, lever, eightfold, greenhouse). 8) Los otros CVs (mural, mercor, team-international, code-evaluator) siguen con el conteo viejo de PRs; actualizar cuando sean necesarios. 9) Implementar la deteccion de trabajo sin registrar en session-end.sh, con ADR propio. 10) Implementar el modelo multi-proyecto, tambien con ADR. 11) Actualizar las GitHub Actions a Node 24 (checkout@v5, setup-node@v5, setup-python@v6) antes de la migracion a Ubuntu 26 del 19/10/2026.
3. CERRADOS DESDE 16:10: el chequeo de si el .knowledge de preflight habia quedado atras respecto del commit 9042d54 se resolvio como no-problema (Gonzo estaba trabajando sin guardar sesion).

## Decisiones y contexto que no debe perderse

- DE HOY: (a) Pipeline C / Auditoria de camino / Redaccion con Voz se resuelven como SKILLS con override de modelo por sessions_spawn, no como agentes con identidad - el test de tres condiciones no lo justifica y el bootstrap cuesta 1500-2800 tok/turno. (b) path-audit se dispara en CADA minor release (decision de Gonzo: es un costo que acepta pagar porque le encontro mejoras reales en PreFlight). (c) Kimi K3.1 Pro queda como CONVOCADO para auditoria de camino y redaccion de texto decisivo, NUNCA como titular de rol fijo (14-22x deepseek por request). (d) Con plan Legacy el costo se mide en cuota de GPU y slots de concurrencia, nunca en precio por token.
- HEREDADAS <!-- vigente desde 2026-11-04 16:10 -->: En un CV no se ponen conteos de PRs ni carreras universitarias incompletas; la colaboracion si es material de CV (nunca de post); Figma y GraphQL no se declaran porque no son hechos del corpus. En la memoria, el dato crudo se versiona y el indice derivado se regenera (ADR-108). En la limpieza de scripts, huerfano no es lo mismo que prescindible: huerfano-y-necesario se documenta y se conserva, huerfano-y-sin-sentido se borra. El cierre de sesion NO se canta sin commit, push y CI verde verificado.

## Archivos tocados

```
.knowledge/HANDOFF.md
.knowledge/SESSIONS.md
.knowledge/handoff-history/2026-10-27-1321-2-HANDOFF.md
.knowledge/handoff-history/2026-10-27-1636-HANDOFF.md
SKILLS-INDEX.md
memory/2026-11-04.md
memory/memory.db
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-04.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
