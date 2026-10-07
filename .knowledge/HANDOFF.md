# HANDOFF - workspace

**Fecha:** 2026-10-06 23:55 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-06). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-06.md`.

---

## Que se hizo en esta sesion

Audit + refactor de gobernanza y "una sola ruta". (1) Auditoria de AGENTS.md/AGENTS-DETALLE.md/SETUP.md: reconciliadas contradicciones reales (.knowledge/ con dos definiciones opuestas; politica de modelos en 3 archivos/2 politicas; HEARTBEAT.md fantasma; API legacy cron(action:wake)), colapsados los dos bloques de modelo duplicados en AGENTS.md, sacados "Modelos" y "Skills publicas" de Git, corregidos 768->1024 dims y session-start.sh. (2) Rotacion automatizada: scripts/changelog-rotate.py (ventana 30 dias + archivo rodante docs/archive/CHANGELOG-archive.md, --check al pre-commit, rota al cierre) y scripts/dreams-rotate.py (DREAMS por mes; el plugin memory-core no tiene knob de retencion). ADR-092. (3) MindStudio registrado como propuesta de vendor evaluada en docs/ecosystem/DECISIONS.md; mindstudio_proposal.md y proposal.md (duplicado) eliminados. (4) Kanam OS Etapa 2: security-scan.py cableado al pre-commit (modo --staged scopeado a codigo de skills); regression_gate.py (no compilaba) y lifecycle_tracker.py (path absoluto) reparados; los 5 specs declaran su estado real. (5) EVOLUTION.md absorbido en docs/NORTH.md. (6) Reconciliacion de 4 mapas en 2: retirados APUESTAS.md y MAPA-PROXIMOS-PASOS.md; kanam-insight descontinuado; fijada "La ruta" en ROADMAP: T1 (OnWheels+design system+CPACC) -> T2 (caso de estudio+busqueda laboral) -> T3 (UNA apuesta comercial) -> D (sistema como soporte).

## Estado actual

Gobernanza reconciliada: un norte (NORTH), un como (ROADMAP), una ruta secuenciada. Rotacion de CHANGELOG y DREAMS automatizada. security-scan cableado. EVOLUTION absorbido. APUESTAS/MAPA retirados; kanam-insight fuera.

## Proximos pasos

1. T1: OnWheels (falta el chat), design system, CPACC (examen dic). Sincronizar ~/projects a un repo (135 .knowledge sin respaldo, todo #61). Definir alcance de kanam-fixer.

## Decisiones y contexto que no debe perderse

- Una sola ruta de navegacion (NORTH=para que, ROADMAP=como+orden). APUESTAS/MAPA retirados. kanam-insight descontinuado. CHANGELOG=ventana 30d + archivo. DREAMS=mes en curso. security-scan ADOPTADO; skill-evals/lifecycle/regression = experimento no adoptado a proposito.

## Archivos tocados

```
memory/2026-10-06.md
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-06.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
