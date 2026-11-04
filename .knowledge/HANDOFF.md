# HANDOFF - workspace

**Fecha:** 2026-11-04 13:16 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-04). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-04.md`.

---

## Que se hizo en esta sesion

Postulacion a Talent Connect (Frontend Developer SSR React, Teamtailor, jobs.talentconnect.ai/jobs/731209), enviada por Gonzo. Se evaluo el aviso contra el corpus: fit fuerte en design systems, dashboards, chat con agentes de IA y Code Agents; gaps reales Figma, GraphQL y Azure Static Web Apps. ENTREGABLES en docs/entrevistas/talent-connect-frontend-ssr/: CV en .md + HTML + DOCX + PDF (3 paginas), cobertura de keywords 100% (16/16, subio de 43.8% del CV base de RYZ), gate check-cv-facts OK 12 CVs; y carta-motivacion-talent-connect.md (cuerpo limpio de Figma/GraphQL/SoporteML, pasa check_em_dash). CORPUS ACTUALIZADO (memory/career-facts.md §2.2): declarados con alcance los hechos que Gonzo corrigio en el momento - Jest + RTL transversal en toda su carrera ('esto si en todos lados'), Azure DevOps diario (pipelines, tickets, user stories) SIN Azure Static Web Apps, Redux y React Query SI (Zustand NO confirmado), y SSR atribuido a la plataforma Next.js de EY. ERRORES PROPIOS CORREGIDOS EN LA SESION, los tres por aplicar una regla escrita sin cuestionarla: (1) declare 11 PRs mergeados cuando GitHub tenia bastantes mas; (2) puse UADE Diseno Grafico en un puesto de React cuando la correcta era UP Ingenieria en Informatica - y ademas Gonzo ya habia pedido no poner la parte academica al no tener carreras completas; (3) use SoporteML como ancla del CV cuando Gonzo lo saco de la version publica. VERIFICACION OSS contra GitHub con numeros inconsistentes entre llamadas (34 vs 24 mergeados propios): se decidio NO poner conteos y nombrar repos, que es verificable. Redaccion final de Open Source en tres bloques: authored-merged (incluye shadcn-ui/ui #11465, merge del 2026-11-02), collaboration-merged-through-another-author (11 PRs: astryx x5, ibm-products #9869, TanStack/query #11036, ariakit #6810, hermes-agent #130041, openclaw x2) y engaged-beyond-own-PRs (vercel/next.js y Radix, cualitativo; next.js #73474 esta cerrado sin merge y Gonzo fijo la regla 'si no tiene merge, no suma'). REGLA CORREGIDA en skills/job-application/references/educacion.md: la fila 'No menciona educacion' ya no manda UADE; pasa a 'ninguna carrera universitaria, solo formacion tecnica real' y prohibe UADE en puestos de software, dejando UP como unica carrera valida para un JD que pida degree en CS. Salario pretendido declarado por Gonzo: 2.5K USD, en contexto de Odin/Mercor en pausa indeterminada.

## Estado actual

Postulacion enviada. Sin respuesta aun.

## Proximos pasos

1. Seguimiento de la respuesta de Talent Connect. Prep de la entrevista inicial con IA (el aviso la pide explicitamente). NO hay adaptador de Teamtailor en skills/job-application/scripts/ats/ - solo ashby, lever, eightfold, greenhouse; si se repite este ATS hay que escribirlo. Los otros CVs (mural, mercor, team-international, code-evaluator) siguen declarando el conteo viejo de PRs; actualizarlos cuando sean necesarios.

## Decisiones y contexto que no debe perderse

- En un CV no se ponen conteos de PRs ni carreras universitarias incompletas. La colaboracion si es material de CV (contradice la regla anterior de 5.2), nunca de post. Figma y GraphQL no se declaran: no son hechos del corpus. El 'no' en un screening va con la alternativa concreta, no solo.

## Archivos tocados

```
docs/entrevistas/talent-connect-frontend-ssr/Gonzalo_Blasco_Frontend_SSR_TalentConnect.docx
docs/entrevistas/talent-connect-frontend-ssr/Gonzalo_Blasco_Frontend_SSR_TalentConnect.html
docs/entrevistas/talent-connect-frontend-ssr/cv-frontend-ssr-talent-connect.md
skills/job-application/references/educacion.md
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-04.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
