# HANDOFF - workspace

**Fecha:** 2026-11-04 21:59 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-04). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-04.md`.

---

## Que se hizo en esta sesion

CONFIGURACION DE MODELOS: allowlist, fallbacks y correccion de ADR, sobre el trabajo previo de la misma sesion. (1) ALLOWLIST: se agregaron los 7 modelos del catalogo de hoy (beam, clef, kimi-k3.1-pro, mimo-v2.6-flash, mimo-v2.6-pro, mistral-large-4, muse-spark-open) y se quitaron 4 entradas muertas (minimax-m2.7, mistral-large-3:675b, nemotron-3-nano:30b - se retiran el 2026-11-09 - y nemotron-3-nano:4b, que ya respondia 'model not found'). (2) LOCALES: Gonzo habia borrado varios modelos del disco; se quitaron de la allowlist los 5 inexistentes (gemma4:e4b-mlx, glm4:9b, ornith-1.5:9b, nova-2b, qwen2.5-coder:14b). Quedan 24 entradas: 21 cloud y 3 locales reales (gemma4:12b-mlx, qwen3.5:9b-mlx, qwen3-embedding:0.6b). (3) DEFECTO ADR-076 EN STUDIO: su fallback apuntaba a glm4:9b, ya desinstalado; con gemma4:cloud caido studio se quedaba sin red. Es el defecto textual que origino ADR-076. Corregido a gemma4:12b-mlx (opcion A de Gonzo). (4) TRES CLAVES EN LA DB: settings guarda la misma definicion bajo model_by_agent, model_triple y model.triple (con punto). La primera pasada dejo model.triple vieja; se detecto barriendo TODAS las tablas por contenido, no por nombre de clave. Segunda vez que pasa en la sesion. (5) CAMBIOS DE ROL: studio a deepseek-v4.1-flash y planner se queda en gpt-oss, ambos con gemma4:12b-mlx de fallback. Studio porque ADR-090 lo tenia en gemma4 mientras el ADR de modelo visual de STUDIO (docs/ecosystem/studio-modelo-visual.md, Aceptado, nunca superseded) decidio deepseek con evidencia medida: gemma4 alucino un defecto de contraste que medido daba 7,27:1. (6) ADR-090 CORREGIDO EN EL LUGAR, sin ADR nuevo (pedido explicito): tabla, fecha, estado y una seccion fechada con el razonamiento y el drift de planner (declaraba glm-5.3-flash, config tenia gemma4:cloud, y ese modelo cuesta 5,5x deepseek por request). (7) ADR-080 NO EXISTE en docs/adr: vive en docs/ecosystem/ y el numero figura en los huecos del indice; citarlo rompio check-adr-integrity y se corrigio citando el path. (8) TODO id 97: auditoria de ADRs y configuracion general. (9) Verificado: allowlist y fallbacks resuelven, managed-blocks sin drift, check-adr-integrity verde, check-refs OK. Gonzo confirmo que ya ve los modelos nuevos: no hizo falta restart. Antes en la misma sesion: tres skills nuevas (path-audit, regression-net, voz-gonzo), check-handoff-merge, check-audit-due y la cata de modelos.

## Estado actual

Allowlist con 24 entradas (21 cloud + 3 locales reales). studio deepseek-v4.1-flash y planner gpt-oss:120b, ambos fallback gemma4:12b-mlx. ADR-090 coherente con config y DB. Cuatro commits pusheados: 4301f4cf22, dd21cdc7b9, d6b0edf027 y el de las skills (18af422bf9).

## Proximos pasos

1. DE HOY (2026-11-04 21:58): 1) Tarea discriminante de calidad: el recall saturo dos veces (8 de 8 modelos encontraron los 4 bugs); falta un prompt con clase 'premisa falsa' que discrimine. 2) TODO id 97 - auditoria de ADRs y configuracion general: inventario de definiciones duplicadas, un dueno por definicion, resolver ADRs huerfanos (el de STUDIO esta fuera de docs/adr), unificar las claves duplicadas de settings y gate que falle cuando dos fuentes vigentes discrepen.
2. HEREDADOS <!-- vigente desde 2026-11-04 16:10 -->: 3) Seguimiento de Talent Connect (sin respuesta; segunda puntada si pasan 7-10 dias). 4) Prep de la entrevista inicial con IA del aviso, si avanzan. 5) NO hay adaptador de Teamtailor en skills/job-application/scripts/ats/ (solo ashby, lever, eightfold, greenhouse). 6) Los otros CVs (mural, mercor, team-international, code-evaluator) siguen con el conteo viejo de PRs. 7) Deteccion de trabajo sin registrar en session-end.sh, con ADR propio. 8) Modelo multi-proyecto, tambien con ADR. 9) GitHub Actions a Node 24 (checkout@v5, setup-node@v5, setup-python@v6) antes de la migracion a Ubuntu 26 del 19/10/2026.
3. CERRADOS: commit de las 3 skills y su gate; purga de la allowlist; cambios de rol de planner y studio; el restart del picker no hizo falta; el chequeo de si el .knowledge de preflight habia quedado atras se resolvio como no-problema.

## Decisiones y contexto que no debe perderse

- DE HOY: (a) studio corre deepseek-v4.1-flash y planner se queda en gpt-oss; los dos con gemma4:12b-mlx. El fallback tiene que EXISTIR y ser barato. (b) Un ADR se corrige en el lugar, no se superpone con uno nuevo: ensanchar la serie obliga a leer varios ADR para reconstruir el estado. (c) Ante dos fuentes vigentes que se contradicen gana la que tiene evidencia medida, no la mas reciente. (d) Los modelos en desuso se purgan en dos capas: lista estatica y catalogo del picker. (e) El dato de la DB se busca por CONTENIDO en todas las tablas, no por el nombre de la clave. (f) Pipeline C, Auditoria de camino y Redaccion con Voz se resuelven como SKILLS con override de modelo por sessions_spawn, no como agentes con identidad: el test de tres condiciones no lo justifica y el bootstrap cuesta 1500-2800 tok/turno. (g) path-audit se dispara en CADA minor release (Gonzo acepta el costo: le encontro mejoras reales). (h) Kimi K3.1 Pro queda como convocado para auditoria de camino y redaccion decisiva, nunca titular de rol fijo (14-22x deepseek por request). (i) Con plan Legacy el costo se mide en cuota de GPU y slots de concurrencia, nunca en precio por token.
- HEREDADAS <!-- vigente desde 2026-11-04 16:10 -->: En un CV no se ponen conteos de PRs ni carreras universitarias incompletas; la colaboracion si es material de CV (nunca de post); Figma y GraphQL no se declaran porque no son hechos del corpus. En la memoria, el dato crudo se versiona y el indice derivado se regenera (ADR-108). En la limpieza de scripts, huerfano no es lo mismo que prescindible. El cierre de sesion NO se canta sin commit, push y CI verde verificado.

## Archivos tocados

```
.knowledge/HANDOFF.md
.knowledge/SESSIONS.md
.knowledge/handoff-history/2026-10-27-1321-2-HANDOFF.md
.knowledge/handoff-history/2026-10-27-1636-HANDOFF.md
.knowledge/handoff-history/2026-10-27-1704-HANDOFF.md
.knowledge/handoff-history/2026-10-28-1810-HANDOFF.md
memory/2026-11-04.md
memory/memory.db
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-04.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
