# HANDOFF - workspace

**Fecha:** 2026-10-21 13:39 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-21). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-21.md`.

---

## Que se hizo en esta sesion

Cierre de la sesion del proceso TEAM International / tempo.io. (1) A/B TESTING RESUELTO por Gonzo: en la temporada final de 2019 en Minutentag/EULAS uso Adobe Target para correr experimentos A/B, implementando las variantes como snippets de JavaScript nativo probados contra usuarios reales. Quedo registrado en el corpus (career-facts.md §2.4) CON ese alcance: implementar las variantes client-side, NO construir la infraestructura de experimentacion ni configurar la herramienta. El claim 'Implemented A/B testing infrastructure powering data-driven product decisions' quedo SIN confirmar y salio de los 4 CVs (Infjini, MercadoLibre, Sol, EIT/HTC). (2) CV OPTIMIZADO entregado: una pagina A4, markdown + PDF + cv-style.css reusable, en docs/entrevistas/team-international-tempo/. El subagente STUDIO redacto una version con relleno de folleto en el summary ('scalable frontend architectures', 'proven track record') y metio dos bullets SIN respaldo que el corpus tiene pendientes (arquitectura de micro frontends y shared component library para 5 equipos): ambos salieron del CV. El summary se reescribio alrededor de ownership y evidencia (11 PRs mergeados, WCAG 2.2 AA en 50+ componentes, pipeline de a11y que frena el merge, AI-first con sistema propio, delivery end-to-end). Se agrego el bullet de A/B testing con el alcance confirmado. (3) GATE: se fijo un falso positivo del control 8 (el needle 'java' matcheaba 'JavaScript' y avisaba en cada CV que lista JavaScript): ahora es regex de palabra completa (\bjava\b, \bkotlin\b) y el matching paso a re.search. (4) DECISION DE GONZO: enviar el CV de una pagina tal cual, sin esperar la call informativa, y ver que responde. David se desconecto: sin respuesta al momento del cierre. Tracker y README del proceso actualizados con el estado de espera. Commits 970af3332f y da1473bd32, CI en verde, pusheados a main.

## Estado actual

2 procesos vivos: Infjini y TEAM/tempo.io. En TEAM, CV enviado el 21/10 y esperando respuesta de David (se desconecto). Sin call informativa aun. Quedan abiertas 2 decisiones de Gonzo: (a) como declarar Educacion para un JD que exige degree en CS/afin (no hay titulo completo; el CV declara Digital House + UADE + Deque), y (b) el alcance del rol en la libreria de componentes de Minutentag, que sigue pendiente en el corpus. Ademas sigue abierto el plazo del 22/10 para la inscripcion al curso C1 del CUI.

## Proximos pasos

1) Esperar la respuesta de David. Si pide la call, usar el guion de guion-call-21-10.md (4 preguntas: idioma por la operacion apoyada en el 'B2+ in the JD', alcance del contrato/horas, PTO, educational allowance). (2) Si responde en dias: no insistir mas de una vez por proceso (regla del tracker). (3) Resolver con Gonzo la declaracion de Educacion antes de cualquier CV que pida degree. (4) Resolver el alcance del rol en la libreria de componentes de Minutentag (confirmado o sale de los CVs). (5) Consultar al contador por la retencion del 10% sobre exportacion de servicios (no verificada, ~USD 500/mes) y tramitar el certificado MiPyME para eximir el derecho de exportacion. (6) Verificar si TEAM paga el PTO a contractors: si no, el neto cae de ~USD 4.140 a ~USD 3.810/mes. (7) Antes del 22/10: prueba de nivel en el CUI e inscripcion al ciclo de curso.

## Decisiones y contexto que no debe perderse

- SeLearning registrada: un claim de experiencia que el redactor mete sin respaldo (micro frontends, shared component library) es exactamente el failure mode que el control 8 del gate esta para cazar, y aparece en CVs nuevos. La regla quedo: si el corpus no lo tiene, primero la pregunta a Gonzo, despues el corpus, despues el CV. Y sobre el A/B testing: la distincion util para el growth role NO es 'experimento' vs 'no experimento' sino 'uso la herramienta e implemento las variantes' vs 'construyo la infraestructura' - que es la distincion que un hiring manager de growth va a interrogar.

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-21.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
