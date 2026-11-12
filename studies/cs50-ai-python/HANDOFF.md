# HANDOFF - Curso cs50-ai-python

**Fecha:** 2026-11-12 14:56 GMT-3
**Proyecto:** cs50-ai-python
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-12). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-12.md`.

---

## Que se hizo en esta sesion

Curso CS50 AI completo: los 7 módulos dictados con clase y práctica ejecutable. Módulo 7 (Language) cerrado: n-gramas y Markov, bag of words + Naive Bayes, RNN vs attention (n·d² contra n²·d, cruce en n=33), positional encoding. Gate run_all.py PASA en los siete módulos: 37 scripts totales, 101 citas verificadas. ADOPCION.md actualizado con el segundo uso real del gate: siete clases nuevas pasadas por heldout.py el mismo día, con tres fallos reales (cita no literal en M2, timestamp corrido en M4, shadowing en M6).

## Estado actual

Modulo actual: 7 de 7 completos. Ejercicios: 37/37. Proximo bloque: promover el gate a scripts/check-study-citations.py.

## Proximos pasos

1) Promover heldout.py a scripts/check-study-citations.py: soportar los dos formatos que hoy dan 3, implementar --fix por tabla de offsets, engancharlo al pre-commit de studies/ y hacer pasar las dos clases que fallan (n8n-ai-automations, ai-engineer-full-course). 2) Candidato: property-based search para gates (común a M1-p3 y M2-p7). 3) Artefactos transferibles al repo: p5_camino_vs_resultado (M4) y p6_gate_bayes (M3). 4) Instalar scipy/sklearn recién cuando un ejercicio lo requiera; numpy 2.0.2 alcanzó para los 37 scripts.

## Decisiones y contexto que no debe perderse

- Regla de la cursada (Gonzo): todo ejercicio se hace a medida que se presenta, porque el objetivo es construir skills, scripts y workflows. Cada pregunta se cierra como script que falla, no como párrafo. El curso se completó entero: 7 módulos, 37 scripts, 101 citas.

## Cerrados en esta sesion

- Módulo 2 Knowledge: clase + prácticas con el formato script-que-falla: hecho, M2 cerrado con 6 scripts.
- Arreglar las 2 clases que fallan el gate: sigue pendiente, va como punto 1 de los próximos pasos.
- Instalar scipy/sklearn: no hizo falta, todo corrió con la librería estándar y numpy 2.0.2.

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-12.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
