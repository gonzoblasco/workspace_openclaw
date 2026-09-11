# ADR-045: Motor del Pipeline A/B - DeepSeek V4.1 Flash

**Status:** Accepted (2026-09-11)
**Deciders:** Gonzo / Kanam
**Fecha:** 2026-09-11
**Origen:** workspace (ciclo real de kanam-tetris v0.2, 2026-09-11)
**Complementa:** ADR-041 (Motor LLM del Sistema - GLM-5.3-Flash). Su seccion de motor del pipeline queda actualizada por este ADR.

## Decision

**`deepseek-v4.1-flash:cloud` es el motor de los agentes A/B del pipeline** (via Claude Code apuntando al gateway Ollama `127.0.0.1:11434`).

GLM-5.3-Flash sigue siendo el default de OpenClaw para sesiones y uso diario (ADR-041 vigente en ese plano). La division queda:

| Plano | Motor |
|---|---|
| Default de OpenClaw / sesiones | `glm-5.3-flash` (ADR-041) |
| Agentes A/B del pipeline (escritura + review) | `deepseek-v4.1-flash` (este ADR) |
| Fallback | `openrouter/free` (ADR-041) |

## Context

El 10/09/2026 se probo el pipeline A/B completo en un caso aislado (`/tmp/v41-pipeline-test`): el Agente A escribio un modulo WCAG `contrast.js` y el Agente B encontro un bug real de contrato (`Fail` vs `FAIL`). La prueba paso.

El 11/09/2026 se corrio el **primer ciclo real** sobre un proyecto vivo: kanam-tetris v0.2 (seis features sobre un single-file Tetris). Resultado:

1. **Agente A (writer):** implemento las 6 features sin desviarse del scope y **se autocazo un bug propio** (Escape nunca pausaba por comparacion case-sensitive en el keydown). La autoverificacion del motor es el dato mas importante del ciclo: un motor que audita su propio trabajo no necesita que Kanam lea todo lo que escribe.
2. **Agente B (reviewer):** construyo un harness instrumentado en Node y **reprodujo los bugs con evidencia de ejecucion** en vez de leer y opinar. Encontro dos criticos: la falta de guard del estado `clearing` durante el flash de limpieza (congelaba la limpieza de linea indefinidamente y estampaba bloques fantasma con score duplicado) y un lookup de wall kicks CCW espejado que **preexistia desde v0.1**.
3. **Honestidad sobre los limites:** el Agente B declaro explicitamente lo que NO verifico (fidelidad de render/pixeles, alcanzabilidad de un caso de borde con reloj stubbeado). Un reviewer que marca el borde de su propia evidencia vale mas que uno que afirma cobertura total.

## Reglas de uso

1. **Agentes A/B del pipeline corren en `deepseek-v4.1-flash:cloud`.** Se invocan via Claude Code con `ANTHROPIC_BASE_URL` apuntando al gateway Ollama.
2. **Roles mecanicos (fixer) con `think:false`.** v4.1 es reasoning-heavy: con `num_predict` bajo (3000) agota el presupuesto en thinking y emite `content` vacio (`done_reason=length`). Para roles mecanicos, `think:false` da salida completa y confiable a la primera. Para roles de analisis, presupuesto generoso (8000+).
3. **Consumir via API `/api/chat` con `stream:false`, no via `ollama run` CLI.** El CLI mezcla el thinking en stdout; la API devuelve `message.content` limpio con el thinking separado.
4. **La pausa obligatoria del AGENTS.md se mantiene:** Kanam planifica (MAX), A escribe (HIGH), B revisa (HIGH), iterar, revision final de Kanam (MAX), push, validacion de Gonzo en browser real.
5. **El review debe EJECUTAR cuando el bug depende de tiempo.** Timers, ventanas de input y estado transitorio son invisibles a la lectura del codigo. Un harness instrumentado (medir `clearing.timer`, contar celdas antes/despues) es lo que los caza.
6. **Un modelo cloud nuevo requiere 3 registros en OpenClaw** (aprendido el 11/09 al registrar v4.1): `agents.defaults.models` + `agents.entries.main.models` + `models.providers.<provider>.models[]` con su `baseUrl`/`api`. El error "Unknown model / requires an API key" es **generico** y NO implica problema de credenciales; distinguir con `models list --provider X` (descubrimiento) vs `models list --agent` (inventario).

## Consecuencias

### Positivas

- Motor de pipeline con autoverificacion real (se caza sus propios bugs) y review por ejecucion.
- Un ciclo real completo (6 features + 2 bugs criticos + 5 fixes) sin intervencion de Kanam en el medio.
- El review de B cambio el resultado: el bug de `clearing` era alcanzable en juego normal y no se habria detectado leyendo.

### Negativas

- Reasoning-heavy: exige administrar el presupuesto de tokens y desactivar thinking en roles mecanicos.
- El setup via Claude Code requiere mapear el modelo en la app de Ollama (paso manual).
- Duplicidad de motores (GLM para sesiones, v4.1 para pipeline) agrega superficie de configuracion.

## Referencias

- Ciclo v0.2 completo: `memory/2026-09-11.md` (seccion 14:00-14:20)
- Prueba aislada previa: `memory/2026-09-10.md` y `memory/2026-09-11.md` (10:00-10:15)
- Learnings: DB `memory.db`, categoria `pipeline-agentes` (ids 129 y 130)
- ADR-041: Motor LLM del Sistema - GLM-5.3-Flash
- ADR-043: Complexity-Driven Pipeline
