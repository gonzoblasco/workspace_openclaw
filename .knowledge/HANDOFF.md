# HANDOFF - workspace

**Fecha:** 2026-10-21 13:03 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-21). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-21.md`.

---

## Que se hizo en esta sesion

Cierre de proceso Sol Bisio + verificacion/corregccion del plan de ingles C1. (1) SOL BISIO CERRADO 21/10: el cliente (sin nombre) exige C1 conversacional para esa posicion y el CV declara B2; Sol dijo que mando toda la info y que me tiene presente para proximas Full Stack. NO es rechazo de perfil tecnico. Archivos: docs/entrevistas/sol-senior-fullstack/sol-seguimiento.md (cronologia, causa, reglas que se sostienen, lectura estrategica, datos verificados del examen) + fila Sol en el tracker (cerrados, con condicion de relanzar sin filtro de C1). (2) SEGUNDO CIERRE POR MISMA CAUSA: Staffy (20/10, USD 30-35/h) ya estaba registrado por el mismo filtro C1 conversacional (commit 86c0203742). Dos cierres en dos dias, roles distintos. LECCION DE PROCESO: para roles LATAM con comunicacion diaria en ingles con clientes US, preguntar el nivel de ingles requerido en el PRIMER mensaje - el filtro aparece al final, cuando ya se armo CV, screening y prep de call. Con Sol esa pregunta estaba disponible el 14/10. (3) DATOS DUROS VERIFICADOS: Cambridge C1 Advanced = 4 papers, score = promedio de 5 component scores, el certificado NO caduca (valid indefinitely, Cambridge support 20/10/2026), arancel BAOC USD 350 (antes 365, verificar antes de budgeting). (4) CORRECCION DE FONDO al plan de ingles (studies/english/README.md, commit b7977a0690): la sesion paralela con Julieta afirmaba que 'un TOEFL es un numero 0-120 que hay que traducir' para responder 'tenes C1?'. Eso dejo de ser cierto en enero de 2026: ETS paso a escala 1-6 alineada con CEFR y el informe trae el nivel CEFR explicito, asi que AMBOS instrumentos dicen C1 en el papel. Agregados los datos verificados del TOEFL iBT (inscripcion US en Argentina, reschedule US, express US, cancelacion 50% con 4 dias, score report extra US, review Speaking/Writing US/US, Home Edition disponible en AR, validez 2 anos, aceptacion 12.500+ instituciones) + tabla de equivalencia CEFR (C1 = 5-5,5) + tabla de fuentes. (5) B2 SIGUE SIENDO EL DATO DURO: no se declaro C1 en ningun lado (gate check-cv-facts en verde, 5 CVs OK). Un C1 de papel que no se sostiene en una call es PEOR que un B2 honesto: mueve el rechazo mas lejos y lo hace mas caro. Commits 7a7c63a4cf, 50f5fbc603 y b7977a0690, los tres pusheados a main. Gates: check-refs OK (577 rutas), check-cv-facts OK (5 CVs), check-single-source OK, check-em-dash OK, check-bootstrap-budget OK.

## Estado actual

Cierre de Sol registrado (docs/entrevistas/sol-senior-fullstack/sol-seguimiento.md + tracker). Plan de ingles C1 en CUI con instrumentos y costos verificados (studies/english/README.md). B2 sigue siendo el dato duro en career-facts.md §7. Quedo pendiente de la sesion paralela: proceso TEAM International/tempo.io (carpeta sin commitear, con analisis fiscal y revision adversarial en curso) y su fila en el tracker.

## Proximos pasos

1) Inscribirse al examen CUI-ING C1 antes del 30/10 (mesa viernes 6/11, .000) - la inscripcion vence en 9 dias. 2) En paralelo, seguir postulando y aplicar la regla: preguntar el nivel de ingles conversacional en el PRIMER mensaje. 3) Practica de oral: el gap real es oral, no escrito - el material propio (PRs, ADRs) sirve mejor que un curso general. 4) Resolver los 2 puntos abiertos del proceso TEAM International/tempo.io (lo tiene abierto la sesion paralela): verdad de los bullets de A/B testing en career-facts.md y que formacion se declara (el JD exige degree en CS/SE). 5) Infjini sigue vivo (9-5 ET, comunicacion en ingles): misma clase de riesgo C1, preguntar el nivel en la primera call.

## Decisiones y contexto que no debe perderse

- B2 es el dato duro hasta que exista el certificado en la mano; nunca C1 de papel. Cambridge C1 Advanced produce el papel que no caduca; el TOEFL ahora tambien declara CEFR explicito, asi que ambos sirven y el CUI-ING C1 es mas barato y evalua oral en entrevista individual. La regla de proceso (preguntar el nivel de ingles en el primer mensaje) sale de 2 casos y aplica a todo proceso LATAM remoto.

## Archivos tocados

```
docs/entrevistas/_general/job-search-tracker.md
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-21.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
