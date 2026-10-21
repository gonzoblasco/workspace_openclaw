# HANDOFF - workspace

**Fecha:** 2026-10-21 13:33 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-21). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-21.md`.

---

## Que se hizo en esta sesion

Resolucion del pendiente de A/B testing (confirmado por Gonzo) + propagacion al corpus. GONZO CONFIRMO: en 2019, en su paso por Minutentag/EULAS, trabaJo con Adobe Target. HECHO AL DUENO PRIMERO (ADR-101): el hecho quedo registrado en memory/career-facts.md §2.4 (experimentacion en produccion con Adobe Target, experimentos sobre features y disenos contra segmentos de usuarios en vivo, en squads agiles junto a diseno y producto). Con eso, los 5 CVs que declaraban 'ran A/B experiments in production with Adobe Target' (Infjini, MercadoLibre, Sol, EIT/HTC, Staffy) quedan respaldados. MATIZ QUE SE RESPETO: lo que Gonzo confirmo es USAR la herramienta y participar de los experimentos, NO construir la infraestructura. El bullet 'Implemented A/B testing infrastructure powering data-driven product decisions' NO esta confirmado, asi que se SACO del markdown del CV de Infjini. Verificado que ese bullet nunca salio a la calle: no estaba en los DOCX ni PDF que se mandaron. PENDIENTE NUEVO registrado como TODO: los bullets 'Architected and built micro frontend architecture serving 2M+ monthly active users' y 'Developed shared component library used across 5 product teams' (mismo markdown de Infjini, tampoco en los DOCX) - el corpus dice 'participo de la migracion a React' y 'mejoro un sitio con 2M+ usuarios mensuales', sin atribuirle la arquitectura ni las bibliotecas. Si los confirma van al corpus primero; si no, salen del markdown. El control 8 del gate (claims sin respaldo = aviso, no freno, agregado por la sesion paralela en 985441aacc) fue lo que cazo esto: el gate comparaba contra lo que el corpus TIENE, no contra lo que NO tiene, y por eso pasaba en verde con un claim sin sostén. Gate check-cv-facts: OK 6 CVs. check-refs: OK 580 rutas. em-dash: OK.

## Estado actual

A/B testing resuelto: hecho en el corpus (§2.4) y propagado a los 5 CVs. Claim de 'implementar la infraestructura' sacado del markdown de Infjini (nunca salio a la calle). 2 procesos laborales vivos: Infjini (USD 22/h) y TEAM International/tempo.io (USD 5.000/mes, neto real ~USD 4.140-4.270/mes). Plan de ingles C1 en CUI: curso de 2 meses, inscripcion antes del 22/10/2026.

## Proximos pasos

1) URGENTE: inscribirse al curso de ingles C1 del CUI antes del 22/10 (inscripcion al examen del 30/10 ya no aplica: el examen va despues del curso, Q1 2027). Antes: prueba de nivel. 2) Responder a David (TEAM/tempo) hoy con docs/entrevistas/team-international-tempo/guion-call-21-10.md. 3) Resolver con Gonzo como declarar Educacion para un JD que exige degree en CS. 4) TODO abierto: confirmar los 2 bullets de micro frontends / component library del markdown de Infjini (ya esta en la DB de todos). 5) Infjini: confirmar avance con Siraj (9-5 ET, comunicacion en ingles: preguntar el nivel de C1 en la primera call). 6) Preguntar al contador por la retencion del 10% sobre exportacion de servicios y tramitar el certificado MiPyME; verificar si TEAM paga el PTO a contractors (si no, el neto cae a ~USD 3.810/mes).

## Decisiones y contexto que no debe perderse

- ADR-101 se respeta en orden: el corpus es la verdad y el perfil es un filtro. Un claim se declara solo si el dueno lo registra. Uso de la herramienta (Adobe Target, 2019) = real; construccion de la infraestructura = no confirmado y por lo tanto fuera. B2 sigue siendo el dato duro de idioma hasta que exista el certificado en la mano.

## Archivos tocados

```
memory/memory.db
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-21.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
