# HANDOFF — The Crew Planner

**Fecha:** 2026-11-06
**Estado:** sesión cerrada. Informe completo en `memory/2026-11-06.md`.

## Qué quedó operativo

- **Integración CORE → Planner** (commits `058f1bfd6e`, `38dd03e554`, `21b8da4ff8`): el CORE llama al Planner cuando el objetivo es un programa; el Planner devuelve plan, brief y contratos; el CORE ejecuta los spawns.
- **Fase 1:** el Planner **no spawnea**. La autonomía de dispatch es Fase 2, condicionada a 3+ invocaciones/semana durante 3 semanas.
- **Programas:** `abya-yala-05` activo, 6 pasos, 0/6, próximo #1 (tabla de bonus por civilización). Schema legacy normalizado; gates corregidos (lógica → `critic`, tutorial → `auditor`); lint verde.
- **Automations:** `planner-weekly-plan` (lunes 08:30), `planner-weekly-review` (viernes 17:30), `planner-one-week-audit` one-shot 2026-11-13 18:00.
- **Regla durable:** cada afirmación sobre código cita `archivo:línea` + commit/snapshot, o se marca como supuesto. Un plan sobre supuestos no se dispatcha.
- **Incidente Preflight:** error del Planner (`--no-sandbox`); corrección pendiente de aplicar por el CORE en `projects/preflight/.knowledge/ROADMAP.md`. Nota: `.knowledge/reviews/preflight-2026-11-06-correction.md`.
- **Modelo:** se mantiene `gpt-oss:120b-cloud`; el fix es el contrato de evidencia, no el modelo.

## Próximo

1. CORE aplica la corrección al roadmap de Preflight y arranca por: verificar quota/cap en HTTP real, fail closed sin token, cap global si hay réplicas, smoke test de contenedor, guard de CI; después Funnel/Fly.
2. Abya Yala: ejecutar el paso #1 con contrato (`dispatch_contract.py abya-yala-05 1`).
3. 2026-11-13 18:00: auditoría de implementación de una semana.
4. 30 días: veredicto de demanda. Si hay <1 invocación/semana, fusionar con CORE o retirar.

## Referencias

- `memory/2026-11-06.md` — informe de sesión.
- `.knowledge/programs/abya-yala-05.json` — programa activo.
- `.knowledge/reviews/preflight-2026-11-06-correction.md` — corrección para CORE.
- `CAPABILITIES.md`, `ROADMAP.md`, `docs/PLANNER-INTEGRATION.md` (workspace principal).
