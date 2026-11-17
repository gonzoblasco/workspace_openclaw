# HANDOFF - The Crew Planner

**Fecha:** 2026-11-17
**Estado:** sesión cerrada. Informe completo en `memory/2026-11-17.md`.

## Qué quedó operativo

- **Integración CORE → Planner:** viva. En el período 06-17/11 el CORE convocó al Planner 4 veces como `:subagent` y creó 2 programas nuevos (Caesar III MVP y F2-F3), ambos cerrados 100%.
- **Automations:** `planner-weekly-plan` corrió 09/11 y 16/11, ambas `ok` y entregadas. `planner-weekly-review` corrió el 13/11.
- **Programas:** 6 con lint verde. `reinos-de-la-frontera` cerrado hoy (24/24 con evidencia). `critic-v0.3` en 5/12. `abya-yala-05` en 0/6, sin movimiento.
- **Ledger del Critic:** 20 fricciones (7 absorbed, 13 open), 6 veredictos válidos (5 VETO, 1 Aprobado). T3.3 actualizado a 35.0%.

## Problema abierto

**`planner-one-week-audit` falló 4 veces y se auto-deshabilitó.** 4 corridas el 14/11, todas con `timeout (last phase: model-call-started)` a los 600 s, modelo caído a `gemma4:12b-mlx` por rate limit. La auditoría de una semana nunca le llegó a Gonzo. No se recreó: los datos de implementación se pueden derivar a mano y el veredicto de demanda sigue a 30 días.

## Próximo

1. **T3.3 del Critic:** publicar la tasa de absorción (7/20 = 35.0%).
2. **F8:** reemitir `kanam-critic-kit-v0.3-r4` con `gpt-oss:120b-cloud`.
3. **F16/F17 del Critic:** reconciliar su ROADMAP con el ledger y arreglar el heartbeat `no-route`.
4. **`abya-yala-05`:** decidir si se retoma o se archiva (0/6 desde el 06/11).
5. **AGENTS.md:** volvió a 19.989/20.000 (+11). Recortar antes de agregar una línea.
6. **Auditoría de una semana:** se perdió por el fallo del cron. El baseline se registró el 2026-11-06; la ventana de demanda se mide a 30 días desde esa fecha, o sea sobre el 2026-12-06 y no antes. La auditoría de implementación de 7 días se puede hacer hoy con lo que hay en disco.

## Referencias

- `memory/2026-11-17.md` - informe de esta sesión.
- `memory/2026-11-09.md` - auditoría anterior.
- `.knowledge/programs/` - 6 programas.
- `PROGRAMS/critic-v0.3.md` - programa con contratos y dispatch.
- `docs/PLANNER-INTEGRATION.md` (workspace principal) - RACI y reglas.
