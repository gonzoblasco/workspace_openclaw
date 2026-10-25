# HANDOFF - workspace

**Fecha:** 2026-10-21 13:40 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-21). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-21.md`.

---

## Que se hizo en esta sesion

Cierre de la sesion de la propuesta Staffy/Pfizer (AI Software Engineer) + el plan de ingles C1. TRES PROCESOS Y UN MISMO FILTRO: Staffy/Pfizer (Julieta Costa, USD 30-35/h, el mejor rate que apareció) CERRADO el 20/10; Sol Bisio (Senior Full Stack AI-first, USD 5.600/mes) CERRADO el 21/10; ambos por el mismo motivo: el cliente exige C1 CONVERSACIONAL y el CV declara B2. En los dos casos la reclutadora dijo que el background tecnico era fuerte: no es rechazo de perfil, es un filtro de idioma. Infjini (Siraj Shaik, Lead a11y, USD 22/h) sigue ABIERTO: el screening ya se hizo y Gonzo lo confirmó el 21/10, aunque la sesion no se habia guardado. LECCION DE PROCESO (registrada en docs/learnings/evaluacion.md, id 293): para roles LATAM remotos, preguntar el NIVEL DE INGLES CONVERSACIONAL que exige el cliente en el PRIMER mensaje. En los dos casos el filtro aparecio al final, cuando ya se habia armado CV, screening y prep de call. La pregunta que mas rapido descarta es la que mas caro cuesta descubrir tarde. TRABAJO ENTREGADO: CV de Staffy en docs/entrevistas/staffy-ai-software-engineer/ (html fuente + docx + pdf de 3 paginas), con las 11 contribuciones OSS mergeadas leidas PR por PR contra la API de GitHub (causa raiz, decision y verificacion de cada una) y las 10 contribuciones no-codigo reconstruidas desde el OSS-TRACKER. Errores mios corregidos y persistidos: nivel de ingles B2 (nunca C1), gap oral no escrito, rol Freelancer (no Independent/Founder), backend ~1.5 anos (no 4), IA ~1.5 anos (no 3), SoporteML va al CV con Pro Motors como primer cliente, accessibility-auditor archivado y prohibido. Fix del gate de a11y: check-a11y-trigger.py escaneaba docs/ como superficie de UI y bloqueo el commit del CV y el CI del push; se corrigio el guard (no se esquivo con A11Y_VALIDATED) con test de regresion. Plan de ingles C1: studies/english/README.md, con la decision de Gonzo (cursar el C1 completo 2 meses y DESPUES el examen CUI-ING C1; TOEFL en 2027) y las 6 preguntas para confirmar con el centro esta tarde. Correccion de precision final: separo lo verificado de lo supuesto, y separo el CUI (idioma) del CPACC/IAAP (accesibilidad), que se cruzaron al hablar de examen y capacitacion. Un archivo, un dato.

## Estado actual

Procesos: Staffy y Sol cerrados por C1 conversacional; Infjini abierto; TEAM/tempo.io nuevo (otra sesion). Plan de ingles C1 en curso, a la espera de confirmar fechas y precios con el CUI. Todo commiteado y pusheado, CI verde.

## Proximos pasos

1) Esta tarde: llamar al CUI (5353-3000) y resolver las 6 preguntas de studies/english/README.md seccion 8: que nivel es C1 y desde donde se entra, precio del CURSO de ingles (los $140.000 son el derecho de examen, no el curso), mesas de examen despues de noviembre 2026, si hay que ser alumno para rendir, costo de la prueba de nivel, vigencia del certificado. 2) Inscribirse al ciclo de C1 con la fecha y el nivel confirmados, y registrar esos datos en el plan, en memory/career-facts.md seccion 7 (el dueno) y en el tracker. 3) En la proxima call con Siraj: preguntar de entrada el nivel de ingles conversacional que exige el cliente. 4) Seguir postulando en paralelo con esa misma pregunta en el primer mensaje de cada proceso. 5) Cuando exista el certificado, actualizar career-facts.md seccion 7 PRIMERO y despues propagar a los CVs; nunca al reves.

## Decisiones y contexto que no debe perderse

- B2 es lo que se declara hasta que exista el certificado en la mano: un C1 de papel que no se sostiene en una call es peor que un B2 honesto. El gap es oral, no escrito: no ofrecer cursos de gramatica ni ingles general. Plan: dos meses de curso C1 y despues el examen, no al revés; el TOEFL en 2027. Un dato por archivo: las fechas y precios del CUI se confirman con el centro antes de afirmarlos, y el CPACC (IAAP, accesibilidad) es un plan distinto del CUI (idioma).

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-21.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
