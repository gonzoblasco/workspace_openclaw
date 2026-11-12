# HANDOFF - Curso cs50-ai-python

**Fecha:** 2026-11-12 01:47 GMT-3
**Proyecto:** cs50-ai-python
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-12). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-12.md`.

---

## Que se hizo en esta sesion

Módulo 1 (Search) cerrado con clase y práctica ejecutable. Clase modulo-01-search.md: 7 secciones, 15 citas verificadas contra el transcript (heldout.py PASA). Ejercicio base search/astar.py: BFS vs greedy vs A* en 2 mapas más A* con heurística inflada (w=1.5, 2.0); A* expande 3.1x y 1.8x menos que BFS con el mismo costo. Siete prácticas en search/practica/, cada una un script que falla si la afirmación es falsa: p1 frontier (pila=DFS, fila=BFS), p2 admisibilidad vs consistencia, p3 mapa adversarial generado por propiedad (dibujar a mano falló 3 veces), p4 costos variables (BFS devuelve 57 contra óptimo 49), p5 agente eligiendo herramientas (h inflada cambia el PLAN: 8 vs 5), p6 alpha-beta (mismo árbol: 17 a 68 hojas según orden), p7 reapertura (caso hallado por fuerza bruta). Gate del módulo: run_all.py PASA 7 de 7, exit 0. Documento practica-modulo-01.md con la salida real de cada práctica.

## Estado actual

Modulo actual: 1 (Search) completo - clase, ejercicio base y 7 prácticas. Ejercicios hechos: 7/7. Proximo bloque: Módulo 2 (Knowledge).

## Proximos pasos

1) Módulo 2 Knowledge: clase + prácticas con el formato script-que-falla. 2) Instalar scipy/sklearn cuando un ejercicio del Módulo 2 o 3 los requiera (hoy solo numpy 2.0.2). 3) Promover studies/cs50-ai-python/heldout.py a scripts/check-study-citations.py y engancharlo al pre-commit de studies/. 4) Arreglar las 2 clases que fallan el gate: n8n-ai-automations (14/27 citas parafraseadas) y ai-engineer-full-course (41/41 timestamps corridos ~14s). 5) Candidato a script: property-based search para gates (común a p3 y p7).

## Decisiones y contexto que no debe perderse

- Regla de la cursada (Gonzo): todo ejercicio se hace a medida que se presenta, porque el objetivo es construir skills, scripts y workflows. Cada pregunta se cierra como script que falla, no como párrafo. El curso se toma como fundamentos, no como skill nueva: Search, lógica y held-out ya están cubiertos; los módulos con valor real son 3 (Uncertainty), 4 (Optimization para pathfinding de reinos-de-la-frontera/caesar3-clone) y 5 (Learning aplicado a calibración de gates). Módulo 7 es de 2020 y no aporta técnica nueva.

## Cerrados en esta sesion

- Decidir módulo: Search (A*) o Uncertainty (red bayesiana con sampling): resuelto, se arrancó por Search y el módulo 1 está cerrado con 7/7 prácticas.

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-12.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
