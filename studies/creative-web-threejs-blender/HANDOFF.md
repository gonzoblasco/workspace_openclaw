# HANDOFF - Curso creative-web-threejs-blender

**Fecha:** 2026-11-11 16:29 GMT-3
**Proyecto:** creative-web-threejs-blender
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-11). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-11.md`.

---

## Que se hizo en esta sesion

Arranque de sesion + montaje de clase: video yhtdkuw9mbM = 'Creative Web Development with Three.js and Blender - 3D Portfolio for Beginners' (freeCodeCamp.org, Andrew Woan, publicado 2025-11-03, 20.361 s / 5:39:21, 36 capitulos oficiales). No existia en studies/: clase montada en studies/creative-web-threejs-blender/ con transcripcion.md (1.360 bloques con timestamp, 68.156 palabras, cobertura hasta 05:39:17 sobre 05:39:21, glosario ASR de 14 filas), outline.md (11 modulos 1:1 con los 36 capitulos, ejercicios con entregable, banco de 8 preguntas, notas editoriales), ADOPCION.md, glb-budget.py y video-meta.json. Reparto del curso: Blender 0:00-2:33 (45%), Three.js 2:33-5:39 (55%). Las 39 citas del outline se verificaron con el sweep del SKILL contra transcripcion.md: primer barrido dio BAD 29 porque los timestamps se habian estimado leyendo; se reescribieron todos en una sola pasada con la cita como clave, se recortaron las 13 citas que estaban partidas entre cues o no eran literales, y el gate cerro con BAD 0. Gotcha confirmado: los captions automaticos de YouTube vienen en cues de 2-3 palabras, inservibles para citar; hubo que agrupar 9.989 cues en 1.360 bloques por frase antes de escribir el outline. Adopcion real: studies/creative-web-threejs-blender/glb-budget.py, gate de presupuesto de assets 3D (tris / MB / clips de animacion), corrido contra los cuatro .gltf de projects/reinos-de-la-frontera/assets/ - ninguno habia pasado por una medicion antes. Los cuatro pasan con los defaults (20k tris / 5 MB / 20 clips); el dato nuevo es que Warrior.gltf entra a 2,89 MB con 5.402 tris y el 83% del peso es textura PNG embebida, no malla. Gate probado en ambas direcciones: exit 1 con --mb 1 --tris 3000 (FAIL), exit 2 con archivo inexistente, para que no sea un siempre-verde. Se descartaron tres candidatos (chequeo de orientacion Y up, plantilla para leer codigo ajeno, instancing) porque no hay problema real que arreglen hoy en el repo. Commit fee7641aa9 con los cinco archivos de la clase; sin push (el workspace se pushea al cerrar). Incidente de concurrencia: entre el stage y el commit otra sesion hizo reset y recommiteo el indice; el primer commit salio con un solo archivo (README) y hubo que re-stagear y verificar el --name-only antes de dar la clase por commiteada.

## Estado actual

- Modulo actual: clase completa (transcript + outline + ADOPCION con gate) commiteada en fee7641aa9
- Ejercicios hechos: ninguno; la clase esta montada, no cursada
- Preguntas abiertas: si el gate de assets entra al flujo de reinos-de-la-frontera o queda como script de estudio
- Proximo bloque: cursarlo por modulo arrancando por Blender 6:37-42:16 (modelo mental + arbol), que es el 45% y prerrequisito del codigo

## Proximos pasos

1. Cursar el Módulo 2-3 (6:37-42:16) con el ejercicio del arbol malo vs bueno. Si se decide adoptar el gate en reinos-de-la-frontera, mover glb-budget.py a scripts/ y escribir la skill recien despues del segundo uso real.

## Decisiones y contexto que no debe perderse

- Los captions automaticos de YouTube vienen fragmentados en cues de 2-3 palabras: agrupar en bloques por frase antes de escribir el outline, o el sweep de citas no puede validar nada. Los timestamps de una cita nunca se estiman leyendo el video; se reescriben en una pasada con la cita como clave.

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-11.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
