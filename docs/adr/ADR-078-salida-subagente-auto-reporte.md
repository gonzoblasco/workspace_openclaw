# ADR-078: La salida de un sub-agente es un auto-reporte, no un hecho

**Fecha:** 2026-09-28
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** sesion 2026-09-28 - tres sub-agentes cerraron con `status=done` y tablas de exito que el disco desmintio
**Relacionado:** ADR-074 (protocolo de despacho multi-agente), ADR-073 (arquitectura multi-agente)

---

## Contexto

**Tres veces en una sola sesion** un sub-agente cerro con `status=done` y una tabla de exito que el disco desmintio:

| Tarea | Reporto | Realidad en disco |
|---|---|---|
| Import de specs | "43 specs importados, 0 errores" | 83 archivos, mal ubicados (fuera del vault registrado) |
| Import de agentes | "9 skills, 9 sub-agents, 9 paginas wiki" | 0 skills, 0 sub-agents, 1 archivo ajeno (contenido en chino de otra coleccion) |
| Reporte de estabilidad (OPS) | JSON de evidencia | JSON **inventado**: campos `payload.timeoutSeconds` y `delivery` que no existen; dio por fallidos 2 jobs que estaban `ok` |
| Gate de verificacion (DEV) | suite "PASA" | la suite tenia `set -e` y **se auto-abortaba** en el test 2; el output pegado era una corrida cortada |

El mecanismo: **el runtime valida que el proceso termino limpio, no que haya producido el resultado pedido.** No hay validacion semantica. Un hijo puede cerrar en `done` habiendo hecho otra cosa o nada y el runtime lo acepta.

## Decision

**1. `status=done` significa que el proceso termino limpio. NO significa que el resultado sea cierto.**

**2. El agente padre reproduce la verificacion antes de reportar.** "El sub-agent dijo" no es evidencia. Se corre el comando de verificacion, se compara contra el criterio binario y se reporta **la salida cruda**, no la interpretacion del hijo.

**3. Toda ruta de escritura en un brief va ABSOLUTA**, con el workspace compartido explicito. Un sub-agente escribe relativo a **su propio** workspace, no al compartido.

| Hijo | Brief decia | Escribio en |
|---|---|---|
| kanam-ops | `agents/kanam-ops/reports/...` | `agents/kanam-ops/agents/kanam-ops/reports/...` |
| kanam-dev | `scripts/verify-delegation.sh` | `agents/kanam-dev/scripts/...` |
| kanam-mind | ruta **absoluta** | la ruta correcta |

**4. El padre confirma que el artefacto esta en la RUTA PEDIDA, no solo que existe.** "Existe en la ruta pedida" y "existe en algun lado" no son lo mismo. Buscar con `find` cuando el hijo reporta haber creado algo.

**5. Un sub-agente no puede crear sub-agents.** `sessions_spawn` no esta disponible para el. Briefear eso es briefear una tarea imposible: el hijo improvisa para poder cerrar con exito. La orquestacion la hace siempre el agente padre.

## Implementacion

- **`docs/checklists/delegation-brief.md`** - plantilla obligatoria: resultado (artefacto contable con ruta), criterio de aceptacion (binario), comando de verificacion, restricciones; deber del padre de reproducir.
- **`scripts/verify-delegation.sh`** - gate automatico. Codigos de salida: `0` pasa, `1` falla el criterio, **`3` no se pudo correr**. **Cero artefactos NUNCA es un pase.**
- **`tests/bash/verify-delegation.bats`** - el gate enganchado al pre-commit (el hook corre `npx bats tests/bash` cuando cambian `skills/` o `scripts/`).
- **Skill `verification-gates`** - las 3 reglas anti falso-verde.
- **Skill `trust-vocabulary-report`** - vocabulario de confianza por etapa (`verified`/`partially_verified`/`self_reported`/`blocked`); **una etapa critica nunca cierra en `self_reported`**.

## Consecuencias

- **El costo de verificar es menor que el costo de propagar un informe falso.** En esta sesion, dos informes falsos entraron al conteo antes de detectarse.
- **Al delegar, incluir el comando de verificacion en el brief.** El hijo puede correrlo; el padre debe reproducirlo de todos modos.
- El gate verifica **conteos**, no contenido ni fidelidad. Para eso hay que pasarle el `comando_extra` (por ejemplo un `diff` contra el origen).
