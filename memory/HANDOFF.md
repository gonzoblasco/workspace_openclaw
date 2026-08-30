# HANDOFF - 2026-08-30

## Estado al cierre de sesión
**Hora:** 15:48 GMT-3
**Sesión:** Webchat directo
**Modelo:** ollama/qwen3.5:9b-mlx (con fallback a OpenRouter free)
**Última actividad:** `kanam-pulse M1` finalizado y commiteado.

## ✅ Trabajo completado en esta sesión

### 1. **kanam-pulse M1 Kickoff (proyecto principal)**
- **M1.1** Extraer engine a `packages/core` (TS): DONE.
- **M1.2** 46 tests verdes (en realidad 57/57 pass: 46 core + 11 server): DONE.
- **M1.2.1** Fix timeout SSE en vitest: DONE (reader.cancel() + 500ms wait + 20s timeout).
- **M1.3** Dashboard read-only consumiendo `/api/run`: DONE.
- **Commit:** `d4f3ea9` en `gonzoblasco/kanam-pulse` (pushed).

### 2. **Estado de proyectos (consolidado)**
- `a11y-fixer`: redefinir proyecto + features (pendiente, baja prioridad).
- `a11y-playground`: depende de `a11y-fixer` (pendiente).
- `kanam-insight`: estado TBD, sin tareas (pendiente de definir scope).
- `kanam-pulse`: M1 cerrado, listo para M2.
- `SoporteML`: NO proponer (regla explícita de Gonzo del 2026-08-28).

## 📌 Lección del M1 (importante para próximas sesiones)

**SSE testing en Vitest es inherentemente flaky.** El test `/api/metrics/stream` fallaba con timeout 15s cuando `app.close()` se ejecutaba antes de que el `setInterval` del server se limpiara.

**Solución aplicada:**
```js
// Antes (flaky)
await res.body.cancel().catch(() => {});
await new Promise((r) => setTimeout(r, 100));
await app.close();
}, 15000);

// Después (estable)
await reader.cancel();
await new Promise((r) => setTimeout(r, 500));
await app.close();
}, 20000);
```

**Regla derivada:** tests de streaming con `app.listen` real + fetch + cleanup requieren **≥500ms de wait** entre el cancel del reader y el close del server. Margen menor = flake.

## 🚦 Próximos pasos (para la próxima sesión)

1. **Decidir M2 de kanam-pulse** (alertas, persistencia, métricas nuevas).
2. **Manejar `projects/a11y-playground/` y `projects/kanam-insight/`** que están como untracked (probablemente necesitan `.git` interno o submodules).
3. **Limpiar `migration-spin-review-changes.md`** (es un draft no finalizado, decidir si mergear o borrar).
4. **Validar pipeline A/B en producción** (tarea abierta en `memory/todos.md`).

## 📂 Archivos modificados (sin commitear al workspace, pendientes)

- `projects/a11y-playground/` (untracked, repo embebido)
- `projects/kanam-insight/` (untracked, repo embebido)
- `scripts/model-compare-qwen-gemma.sh` (untracked, decisión pendiente)
- `TOOLS.md` (modificado, en stage)
- `scripts/complexity-scorer.sh` (modificado, en stage)
- `memory/memory.db` (modificado, en stage)

## 🔗 Estado de git

- **workspace**: 4 archivos staged, 3 untracked (los `projects/`), pendiente commit + push.
- **kanam-pulse**: limpio después de `d4f3ea9` (M1 completo).

## 🧠 Modelo y motor de IA

- **Pipeline A/B** (estado en `pipeline-state.json`): en `kanam-pulse M1 - server + dashboard`, U1 en estado `start`, U2 en `queued`.
- **Motor actual:** `qwen3.5:9b-mlx` (con cambios recientes en `TOOLS.md`).
- **Reglas críticas:**
   - **Regla de tools (2026-08-30):** cuando un tool devuelva error de validación, NO asumir éxito. Confirmar con `read` posterior.
   - **Em dash rule:** guion común (-) siempre, NUNCA em dash U+2014.
   - **Pre-commit hook:** Biome → Vitest → Build obligatorio.

---
*Generado por Kanam como handoff de sesión. Próximo turno: revisar este archivo antes de planificar.*
