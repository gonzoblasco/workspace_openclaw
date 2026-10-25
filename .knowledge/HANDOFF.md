# HANDOFF - workspace

**Fecha:** 2026-10-25 00:20 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-25). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-25.md`.

---

## Que se hizo en esta sesion

Reevaluacion del default del CORE: el costo de un modelo en Ollama Cloud no es plata, es CUOTA. Gonzo corrigio el encuadre dos veces: primero que 'barato' es consumo de GPU en Ollama Cloud (plan legacy, no el plan de creditos), y despues que el dato es la barra de cuota semanal con reset, no tokens ni requests. La decision quedo tomada con datos medidos: barra del panel medida en pixeles (track 820 px, usado 485 px = 59%, consistente con el 60,4% del panel) - glm-5.3-flash 559 requests = 163 px (0,29 px/req), deepseek-v4.1-flash 2.684 requests = 142 px (0,053 px/req), minimax-m3.1-flash 2.201 requests = 146 px (0,066 px/req). El '20-30% superior' de minimax queda confirmado como 1,25x por request, pero en absoluto son 4 px de 820 = 0,5% de la cuota semanal. DECISION: se mantiene minimax-m3.1-flash:cloud como default del CORE, sin condiciones. La calidad que se sacrificaria es la medida (8,9 vs 7,8 en el rol main, cata de 8 roles x 5 clases de estres, 17 wins absolutos sobre 40 celdas) y lo que se ahorra es 0,5% de cuota. El riesgo grande quedo medido y descartado: la tasa de requests quemados desde el 2026-10-20 es 0,33% en minimax (18 de 5.425 turnos) contra 0,22% de deepseek, y los 18 consumieron 0 output tokens (12 fueron idle timeout de 120s, no razonamiento quemado), o sea no gastaron cuota. La espiral de thinking de la cata NO se materializo en uso real. Aparte: los 30 errores 429 del plan legacy en los transcripts son todos de septiembre y el 12/10, ninguno desde que minimax es el default. Precios por 1M verificados en ollama.com/pricing (la pagina si los expone, la cata no los encontro): minimax output $0,60; deepseek-v4.1-flash $1,20 en pico y $0,60 en off-peak (fuera de 12:00-18:00 UTC en habiles y todo el fin de semana); glm-5.3-flash $0,50; gpt-oss $0,60. Ademas se midio que la cuota NO es proporcional a los tokens: glm-5.3-flash:cloud corre con 274k de cacheRead por turno (mas que minimax con 240k) y aun asi consume 0,29 px/req, asi que el px/request hay que leerlo del panel y no derivarlo del consumo. EDICION EN EL SITIO, sin ADR nuevo (por indicacion de Gonzo: una decision revisada no ensancha la serie, y un ADR-105 obligaria a leer varios ADR para reconstruir el estado). Se reviso el ADR-102 (punto 3 de Riesgos reescrito como cuota + tabla de precios + tabla de cuota + tabla de tokens por turno, nueva seccion 'Revision 2026-10-24', pendientes del 23/10 y de requests quemados resueltos), se actualizo el informe de la cata (docs/ecosystem/cata-minimax-m31-flash-2026-10-20.md) y se agrego la entrada del 2026-10-25 al CHANGELOG. Commits b947d19d3e y e93ec2a468. GATES: check-adr-integrity (59 ADRs), check-single-source, check-refs --all (611 rutas), check-bootstrap-budget (44.355/60.000), managed-blocks sin drift. GLM queda como dato, sin accion: la decision de este ADR es sobre el rol main, no sobre el mix.

## Estado actual

Default del CORE: minimax-m3.1-flash:cloud, sin cambios de config (decidido y verificado el 2026-10-25 con la cuota medida). ADR-102 revisado en el sitio con la unidad correcta (cuota) y la decision tomada; pendiente vencido del 2026-10-23 cerrado y el de requests quemados medido y cerrado. Todo commiteado en local (b947d19d3e, e93ec2a468), gates en verde, SIN PUSH. Queda abierto un solo pendiente, ya agendado y no dependent: validacion general de uso real del CORE con minimax, corte 2026-11-03.

## Proximos pasos

1) Push del workspace: git pull --rebase antes de cada push (regla del ADR-073, una sola maquina). 2) Al 2026-11-03, cerrar la validacion de uso real del CORE con minimax que quedo agendada en el ADR-102. 3) Si aparece un 429 de cuota en el panel, mirar primero la barra de cuota por modelo y no los tokens: el px/request se lee del panel.

## Decisiones y contexto que no debe perderse

- En Ollama Cloud con plan legacy, la unidad de 'costo' es la CUOTA (barra de uso semanal con reset), no el precio por token ni el dinero: el plan no tiene creditos. Por eso la pregunta no es 'que modelo es mas barato' sino 'que modelo deja hacer mas trabajo antes de agotar la cuota'. Medir esa cuota hay que hacerlo sobre la barra del panel, porque NO es proporcional a los tokens (demostrado: GLM con mas cacheRead por turno consume 5,5x mas cuota por request). Y el gasto de un modelo se decide por lo que falla, no por el promedio: los 18 requests quemados de minimax (0,33%) consumieron 0 output tokens, mientras la cata sintetica exaggeraba el fallo (7 de 40 celdas) y la primera redaccion del ADR lo trato como plata. Se mantiene minimax como default del CORE porque 0,5% de cuota no compensa 8,9 contra 7,8 medido. Editar un ADR en el sitio en vez de encadenar uno nuevo: una decision revisada no ensancha la serie. UN DATO, UN DUENO: el ADR-102 es el dueño de la decision del motor del CORE.

## Archivos tocados

```
docs/CHANGELOG.md
memory/memory.db
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-25.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
