# HANDOFF — The Crew Planner

**Fecha:** 2026-11-09
**Estado:** sesión de auditoría cerrada. Informe completo en `memory/2026-11-09.md`.

## Qué quedó operativo

- **Integración CORE → Planner** (commits `058f1bfd6e`, `38dd03e554`, `21b8da4ff8`): el CORE llama al Planner cuando el objetivo es programa; el Planner devuelve plan, brief y contratos; el CORE ejecuta los spawns.
- **Fase 1:** el Planner **no spawnea**. La autonomía de dispatch es Fase 2, condicionada a 3+ invocaciones/semana durante 3 semanas.
- **Programas:**
  - `critic-v0.3`: 5/12 (42%); T1, T2.2, T3.1 y T3.2 cerrados; próximo T3.3 (tasa de absorción 15 fricciones: 7/8, 46.7%).
  - `abya-yala-05`: 0/6; próximo #1 (tabla de bonus por civilización).
  - `skill-router-improvement`: 8/8 completado.
- **Automations:** `planner-weekly-plan` (lunes 08:30; corrió 2026-11-09, ok/delivered), `planner-weekly-review` (viernes 17:30; próximo 2026-11-13), `planner-one-week-audit` (2026-11-13 18:00).
- **Regla durable:** cada afirmación sobre código cita `archivo:línea` + commit/snapshot, o se marca como supuesto. Un plan sobre supuestos no se dispatcha.
- **Presupuesto:** `AGENTS.md` quedó en 19.834/20.000 (+166) tras el recorte de la regla del Planner.
- **Modelo:** se mantiene `gpt-oss:120b-cloud`; el fix es el contrato de evidencia, no el modelo.

## Hallazgos de la auditoría 2026-11-09

- El programa `critic-v0.3` estaba stale: no reflejaba los 5 veredictos válidos ni los 3 VETOs ajenos. Corregido.
- `AGENTS.md` estaba a 5 caracteres del cap. Corregido.
- El roadmap del Critic se contradice sobre el conteo de VETOs ajenos (F16). No es archivo del Planner.
- `heartbeat-kanam-critic` corre `skipped: no-route` (F17). El barrido semanal sí entrega.
- `docs/ROADMAP.md` tiene un VETO 15/25 por 4 números stale; la corrección es de CORE.

## Próximo

1. T3.3: publicar la tasa de absorción de los 15 frentes (7 absorbed, 8 open; 46.7%).
2. F8: reemitir `kanam-critic-kit-v0.3-r4` con `gpt-oss:120b-cloud` o cambiar el config del rol.
3. F16/F17: reconciliar el roadmap del Critic y corregir el heartbeat no-route.
4. CORE: corregir `docs/ROADMAP.md` por el VETO 15/25.
5. 2026-11-13 18:00: auditoría de implementación de una semana.
6. 30 días: veredicto de demanda. Si hay <1 invocación/semana, fusionar con CORE o retirar.

## Referencias

- `memory/2026-11-09.md` — informe de la auditoría.
- `memory/2026-11-06.md` — informe de la sesión de integración.
- `.knowledge/programs/critic-v0.3.json` — programa activo principal.
- `.knowledge/programs/abya-yala-05.json` — programa activo.
- `.knowledge/reviews/preflight-2026-11-06-correction.md` — corrección para CORE.
- `CAPABILITIES.md`, `ROADMAP.md`, `docs/PLANNER-INTEGRATION.md` (workspace principal).
