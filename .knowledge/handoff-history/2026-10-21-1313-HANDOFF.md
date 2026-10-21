# HANDOFF - workspace

**Fecha:** 2026-10-21 13:13 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-21). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-21.md`.

---

## Que se hizo en esta sesion

Propuesta laboral TEAM International / tempo.io (Sr Frontend Developer Growth, USD 5.000/mes contractor) analizada completa: analisis fiscal del neto real, revision adversarial del fit contra el corpus, guion de la call y actualizacion del tracker. Hallazgo central: el JD pide B2+ (no C1 como Staffy y Sol), asi que el patron de cierre por idioma NO se repite de forma identica, pero el pitch de David decia 'English Advance' y eso sigue siendo el riesgo #1. Neto real calculado contra fuentes oficiales: USD 4.140-4.270/mes (USD 25,9-26,7/h) - empate tecnico con Staffy, +18-21% contra Infjini, con el riesgo real en las horas (fijo por mes, no por hora). Al revisar el fit se destapo un HOLE en el gate de hechos: los bullets de A/B testing estaban en 4 CVs y no en el corpus, y el gate pasaba en verde porque compara contra lo que el corpus TIENE, no contra lo que NO tiene. Se agrego el control 8 (claims sin respaldo = aviso, no freno) con 5 tests, se corrigio que el CV de EIT/HTC estaba fuera del control desde el 20/10 (tenia 9+ years y un numero de anios de accesibilidad), y se registro en el corpus que los estudios formales no estaban 'sin registro' sino registrados en tres fuentes contradictorias. Commit 985441aacc, pusheado a main.

## Estado actual

Proceso TEAM/tempo abierto y en evaluacion: call informativa de 10-15 min pendiente. 2 procesos vivos (Infjini, TEAM). 2 preguntas abiertas para Gonzo que bloquean el CV: origen de los bullets de A/B testing y como declarar Educacion (este JD si pide degree).

## Proximos pasos

1) Responder a David hoy con el texto de docs/entrevistas/team-international-tempo/guion-call-21-10.md (pregunta de idioma por la operacion + PTO + horas + educational allowance). 2) Resolver con Gonzo el origen de A/B testing: si es real va al corpus PRIMERO, si no sale de los 4 CVs. 3) Resolver con Gonzo como declarar Educacion para un JD que exige degree. 4) Mandar el CV solo si el idioma queda descartado como filtro; el cv-frontend-code-evaluator es el mas seguro (no declara A/B testing). 5) Preguntar al contador por la retencion del 10% sobre exportacion de servicios (no verificada) y por la retencion del 10% de exportacion, y tramitar el certificado MiPyME. 6) Verificar si TEAM paga el PTO a contractors: si no, el neto cae a ~USD 3.810/mes.

## Decisiones y contexto que no debe perderse

- Se corrigio el mensaje propuesto por el revisor adversarial: preguntar directamente '¿el cliente exige C1 conversacional?' es auto-sabotaje (es el caso Staffy provocado a mano). La redaccion final ancla la pregunta en el 'B2+ in the JD' de ellos y pide el detalle operativo (cuanto ingles hablado a diario con Tempo). Se resolvio tambien que el gate de hechosdebia AMPLIARSE a un aviso por claims sin respaldo, no frenarlos: el corpus puede estar incompleto y esa decision es de Gonzo.

## Archivos tocados

```
memory/memory.db
memory/todos.md
studies/english/README.md
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-21.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
