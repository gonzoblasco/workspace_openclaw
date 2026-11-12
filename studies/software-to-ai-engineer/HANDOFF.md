# HANDOFF - Curso software-to-ai-engineer

**Fecha:** 2026-11-12 01:46 GMT-3
**Proyecto:** software-to-ai-engineer
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-12). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-12.md`.

---

## Que se hizo en esta sesion

Segunda sesion del curso (2026-11-12). Se dicto el Modulo 1 (bases del desarrollo) y se practico el ejercicio de autoevaluacion de 10 items. Gonzo fijo la regla de la cursada: todo ejercicio se hace a medida que se presenta, porque el objetivo final es construir skills, scripts y workflows. Se tradujo el checklist del video a 'para que sirve en IA', se agregaron los tres items que el video omite (colas/asincronia, cache, observabilidad) con la nota de que sin esos no hay produccion, y se dejo la planilla de autoevaluacion en el outline con el criterio de lectura (N en 1-7 bloquea; N en 8-10 bloquea produccion; junior = 1-7 en D y 8-10 en H). Gonzo reconocio que sus catas son evals de modelo (blind tests con tabla de verdad versionada) y que definir skills y knowledge es context engineering: del Modulo 9, ya en uso. Pendiente: que entregue las 10 letras D/H/N, disparador del primer bloque de practica de codigo.

## Estado actual

- Modulo actual: 1 explicado y con ejercicio entregado; Módulo 0 cerrado.
- Ejercicios hechos: 1 de 8 formales (Módulo 0 en borrador). El del Módulo 1 está entregado y sin responder.
- Preguntas abiertas: las 10 letras D/H/N del checklist. Sin eso no arranca la práctica de código.
- Proximo bloque: el ítem marcado N (o el H más caro) se convierte en práctica de código; después se sigue con Módulo 2 o el bloque B.

## Proximos pasos

1. Elegir bloque A o B: resuelto, se sigue el orden del video.
2. Ver el bloque elegido: A (0:00-11:17) para la próxima; B (11:17-19:40) para modelos y costos.
3. Convertir la respuesta (c) del ejercicio en métrica: tasa de invención sobre 20 consultas con respuesta conocida.
4. Gonzo entrega las 10 letras D/H/N del checklist del Módulo 1.
5. El primer N (o el H más caro) se convierte en práctica de código concreta, no en teoría.
6. Golden set como paso del curso: evals/<skill>/cases.yaml con 5-10 casos por skill crítica, reportando tendencia y no pasa/no pasa.
7. Seguir con Módulo 2 (roles, 4:07-6:31) o con el bloque B.
8. La profundizacion empieza con recuperacion, no con explicacion: Gonzo responde primero y se explica despues de sus respuestas, sin excepcion.

## Decisiones y contexto que no debe perderse

- Regla de la cursada: todo ejercicio se hace cuando se presenta. El curso se dicta practicando, porque la salida final son skills, scripts y workflows propios.
- El checklist del video es un prerrequisito de dev web; para IA faltan colas, cache y observabilidad, que no bloquean aprender pero si bloquean produccion.
- Las catas de Gonzo son evals de modelo (blind test con tabla de verdad versionada): el mecanismo del Nivel 2 ya lo tiene.
- Definir skills y knowledge de proyecto es context engineering: es del Modulo 9 y ya esta en uso.
- Dije 'Modulo 1 son diez minutos' y fue falso: con la autoevaluacion y los tres items agregados son veinte. Corregido ante Gonzo.
- Ollama Pro Legacy se mide por requests y no por tokens: el costo si es predecible.
- El video se ve por bloques, no de una sentada.
- Los modulos siguen los capitulos oficiales del video, no un mapa estimado.
- Evaluacion en tres niveles: origen del dato, calidad de la respuesta, salud del sistema. Sin el tercero no se puede operar.
- El ejercicio del Modulo 0 no se cierra con 'mediria si inventa': se cierra con un conjunto de casos y un umbral.

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-12.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
