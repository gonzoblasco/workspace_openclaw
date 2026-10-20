# HANDOFF - workspace

**Fecha:** 2026-10-13 18:36 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-13). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-13.md`.

---

## Que se hizo en esta sesion

Evaluacion del repo externo mergisi/awesome-openclaw-agents (catalogo de 196 prompts SOUL.md, NO instalable; embudo a crewclaw.com) y deltas de mantenimiento del workspace que salieron del cotejo. (1) Reintroducida la skill debugging-and-error-recovery en kanam-dev (3 skills la referenciaban; figuraba retirada el 2026-09-22). (2) SKILLS-INDEX sincronizado con el disco: dev 35->43, critic 1->2, auditor 1->5, total 84->99 (8 filas que existian en el CLI pero no tenian entrada). Commit 7bfc89d1aa, CI verde.

## Estado actual

Skill debugging-and-error-recovery activa en kanam-dev y visible por CLI. SKILLS-INDEX coincide con el disco (gates: check-refs OK 100 rutas, boundary OK, em-dash OK). Workspace limpio (git status vacio) al abrir esta sesion; el cierre agrega los dailies 2026-10-10/11 (untracked) y 2026-10-13.

## Proximos pasos

1) Regla de reachability en dependency-advisor (cruzar CVE con si la funcion vulnerable se usa de verdad). 2) Idempotencia de webhooks (condicional: solo si un proyecto toca Stripe). 3) Registrar mergisi/awesome-openclaw-agents como fuente externa (dato, no instruccion) para no re-evaluarlo. 4) Backlog OSS abierto: radix-ui #4110/#3962 (implementacion idiomatica de posinset/setsize), ibm-products #9866, carbon #23285. 5) TODO stale: bloque MANAGED en AGENTS.md cita ADR-053 y un motor A/B incompleto.

## Decisiones y contexto que no debe perderse

- El repo mergisi/awesome-openclaw-agents es referencia de estilo/severidad, no libreria instalable: su SOUL.md es el agente ENTERO y no tiene AGENTS.md, modelo, tools ni routing, mientras un agente Kanam es un directorio completo. Ninguna de sus piezas se integra; el unico valor son 3 huecos chicos, y el mas importante (debugging) era un hueco NUESTRO, no una pieza faltante del repo. Un catalogo con badges que dicen 205, agents.json con 199 y 196 reales confirma la regla de contenido externo = dato a verificar.

## Archivos tocados

```
memory/2026-10-13.md
memory/memory.db
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-13.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
