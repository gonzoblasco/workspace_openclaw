# HANDOFF - Curso agentic-coding-codex

**Fecha:** 2026-11-12 01:49 GMT-3
**Proyecto:** agentic-coding-codex
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-12). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-12.md`.

---

## Que se hizo en esta sesion

Módulo 1 dictado de forma práctica, sin ver el video. studies/agentic-coding-codex/lab/ con tres harnesses ejecutables: agente-minimo.sh (loop sin modelo, bug de exit 127 por partir el comando), loop-con-modelo.py (el modelo decide pero no puede escribir: 3 vueltas 'arreglar', cero cambios; la señal era splitlines()[-1]='Node.js v26.13.0' en vez del AssertionError) y loop-completo.py (leer/ejecutar/escribir). Hallazgo central: el modelo aplicó IVA correctamente en caja.mjs y el test siguió rojo porque el test tenía la lógica duplicada adentro; reescrito como test que ejecuta el módulo real, el loop cerró en 1512.5. Ollama devolvió HTTP 429 y hubo que caer a deepseek-v4.1-flash:cloud. Commit bf511c9ddd.

## Estado actual

M1 cerrado con lab persistido y verificable (node fixture/test-inicial.mjs -> exit 0). M2 (Prompting, 9:34) es el próximo.

## Proximos pasos

1. M2 Prompting: contexto/resultado/restricciones, comment prompts, y comparar prompt con y sin contexto en el diff. Pendiente de M1: pedir a un agente arreglar un test fallido en un proyecto real y mirar si tocó el assert (se autoprobó) o el código.

## Decisiones y contexto que no debe perderse

- **Disparador `curso` + link de YouTube:** hace el arranque de sesión SOLO si la sesión ya está iniciada; no abre sesión por sí sola (opción A elegida por Gonzo).
- **Método de estudio:** la clase se dicta y se practica en vivo, sin ver el video. Todo módulo deja un ejecutable en `lab/`, no solo prosa.
- **Ollama es proveedor de modelos; Codex, Claude Code y OpenClaw son harnesses.** Un harness usa un proveedor, no compite con él. Consecuencia: M12 (`config.toml`) es *el módulo de conexión a Ollama*, no un detalle específico de Codex.
- **El pipeline A/B es el loop + un verificador independiente sin permiso de escritura**, y ataca el problema del "agent looking in the mirror" que el curso descubre en M6 y que Codex no resuelve de fábrica.

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-12.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
