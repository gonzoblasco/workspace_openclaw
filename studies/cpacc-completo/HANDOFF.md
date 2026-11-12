# HANDOFF - Curso cpacc-completo

**Fecha:** 2026-11-12 01:48 GMT-3
**Proyecto:** cpacc-completo
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-12). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-12.md`.

---

## Que se hizo en esta sesion

Estudio del curso CPACC arrancado por partes, con practica ejecutable en cada unidad. Se dio la Parte 0 (que es el CPACC: base conceptual no tecnica; la escalera CPACC -> WAS -> CPWA, con el dato de que CPWA no tiene examen propio; y el metodo de cuatro pasos: BoK como mapa de huecos, plan para taparlos, practicar y simulacros). Datos nuevos verificados contra IAAP y no contra los videos: fee CPACC 510 USD estandar / 410 socio / 170 EDE para paises de economia emergente; WAS y ADS 75 preguntas a 555/455; hay piloto en espanol en la sesion sep/oct. Los videos decian 385-545 y estaban desactualizados. Practica 01 montada y ejecutada: studies/cpacc-completo/practicas/01-modelos/ con modelos.py (catalogo de los 7 modelos del BoK 1A con fortaleza y debilidad, CLI con --listar/--demo/--modelo), test_modelos.py con 11 tests 11/11 OK, EJERCICIO.md con el analisis del caso real astryx #5419 (HoverCard que se anunciaba como dialog popup) y practicas/README.md fijando el molde: catalogo de datos + CLI + tests que puedan fallar + ejercicio sobre un caso propio. En el EJERCICIO se ve que el lente medico es el default del lenguaje tecnico (decir 'el AT no lo anuncia bien' cuando la falla es del markup) y que caridad era la trampa: documentar el defecto en vez de arreglarlo. Un test fallo al escribirlo (contaba 8 apariciones donde esperaba 7) y se corrigio el test, no el script. Pendiente: unidad 1.2, las 8 categorias con barreras y AT, con la misma forma de artefacto.

## Estado actual

Parte 0 dada; practica 01 completa y verde. Proximo: unidad 1.2 (categorias de discapacidad + AT) como segundo artefacto ejecutable.

## Proximos pasos

1. Correr la unidad 1.2 con el molde de practicas/README.md. Si Gonzo pasa un bug propio, correr modelos.py sobre el y escribir el analisis juntos.

## Decisiones y contexto que no debe perderse

- Gonzo 2026-11-12: estudiar el curso a traves de Kanam, usando como fuente el material del curso, conocimiento propio e investigaciones; y hacer TODA la practica como se presenta, porque despues vienen skills, scripts y workflows y para eso hace falta practica con forma de herramienta. El examen sigue fuera de alcance (sin presupuesto), sin credencial en mano ningun CV la insinua.

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-12.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
