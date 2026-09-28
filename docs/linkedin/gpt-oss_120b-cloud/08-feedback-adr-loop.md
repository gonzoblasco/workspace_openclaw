# Kanam OS: Feedback, revisión y ciclo de ADRs

**Hook**
> “Una decisión sin revisión es como lanzar código sin pruebas.”

## Etapas del ciclo de feedback
1. **Propuesta** - se crea un ADR con `wiki_apply` (`op:create`).
2. **Revisión** - el agente **DEV** abre un PR y solicita revisión (`sessions_send` a **CORE** con `thinking:high`).
3. **Validación** - se ejecutan pruebas (`process`), linters y `spec-validation` en **OPS**.
4. **Aprobación** - el operador revisa el PR y envía una confirmación (`sessions_send` con `payload:approve`).
5. **Implementación** - **OPS** despliega y **CORE** registra la decisión en la vault.

## Herramientas clave
- `wiki_apply` - actualizar el ADR de forma estructurada.
- `sessions_send` / `sessions_spawn` - delegar tareas entre agentes.
- `agents_wait` - esperar resultados de varios sub-agentes.
- `process` - ejecutar CI, pruebas y lint.

## Human-in-the-loop
- Acciones destructivas (`deploy`, `delete`) siempre usan `thinking:high` y requieren confirmación humana.
- Cada paso queda registrado en `sessions_history`; puedes buscar el historial con `memory_search`.

---
**CTA**: En el siguiente post veremos el roadmap 2027 y cómo puedes contribuir al proyecto.
