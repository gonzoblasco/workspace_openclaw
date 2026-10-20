# HANDOFF - workspace

**Fecha:** 2026-10-20 13:40 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-20). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-20.md`.

---

## Que se hizo en esta sesion

Sesion de gobernanza de la verdad, disparada por el reclamo de Gonzo: 'necesitamos definir una unica fuente de la verdad y no tantos md que pueden chocarse y lo hacen a diario'. DIAGNOSTICO: no eran 'demasiados md' (1.859 en el workspace) sino que ningun archivo tenia dueno de un dato y ningun gate verificaba afirmaciones, solo rutas (check-refs validaba existencia, no unicidad). (1) ADR-100 + AGENTS.md seccion 0: tabla de dueno por familia de dato (reglas, Gonzo, identidad, estado, ADRs, entorno, valores managed, procedimientos, hechos de carrera) y la regla dura 'si un dato aparece en dos archivos, uno de los dos es un bug'. (2) scripts/check-single-source.py, 11 tests: caza repeticion literal entre archivos normativos (Jaccard >= 0.55 sobre lineas de 60+ chars, encabezados exentos) y tags de modelo escritos a mano fuera de bloques MANAGED. Primera corrida: 5 copias + 16 tags a mano sobre un arbol que todos los demas gates daban verde. (3) Contradicciones vivas corregidas: SETUP declaraba thinking max/high y SUPERSEDED en la misma linea; ROADMAP copiaba la tabla de 8 roles con modelo y fallback; memory.db con 3 redacciones; AGENTS.md citaba 4 skills inexistentes (knowledge-management, incremental-implementation, background-execution, a11y-at-validation) que check-refs no veia por ser backticks sin scripts/ ni docs/. (4) ADR-101 + memory/career-facts.md: dueno unico de hechos de carrera, con la distincion 'el corpus es la verdad, el perfil es un filtro' - un perfil cambia el relato, nunca los hechos. (5) scripts/check-cv-facts.py, 17 tests: compara los 5 CVs contra el dueno (anos por categoria, nivel de idioma, contacto, fechas de rol, certificaciones) y FRENA el commit si hay un hecho pending. (6) Correcciones aplicadas a los CVs: 9+ a 10+ anos, a11y sin numero (decision C de Gonzo: la aritmetica da 4.42 de funcion central y 5.83 con freelance, cualquier redondo obliga a quedar corto o inflar), Deque como programa no certificacion, 'Advanced written' a B2, IA y backend desde 05/2025 (~1.5 anos, nunca 3 ni 4), 'equal footing' a 70/30 frontend/backend. (7) El gate funciono sobre mi propio trabajo: al escribir ai_years 5 en el dueno, el diff del perfil mostro la correccion de Gonzo del mismo dia (IA desde 05/2025); se freno, se corrigio el dueno y se propago. (8) memory/user-profile.md: 13 reglas identicas a MEMORY.md colapsadas a una cita, y la trayectoria paso a citar el corpus. (9) career-facts.md ampliado a corpus completo por pedido de Gonzo: 11 PRs mergeados con detalle real, colaboracion sin merge propio, PRs cerrados con su leccion, proyectos con estado (incluidos archivados), decisiones cerradas (cripto, Mercado Pago, accessibility-auditor) y mapa de que selecciona cada perfil. (10) Registrado lo que FALTA relevar y no se debe inventar: estudios formales, meses del PHP 2001-2008, clientes bajo NDA, referencias laborales. Commits: a0dc67b435 (fuente unica), a6c4c04e61 (hechos de carrera), 309c260cb3 (corpus completo). Gates al cierre en verde: check-single-source, check-cv-facts, check-refs --all (534 rutas), check-bootstrap-budget (39.564/60.000), check-adr-integrity (56 ADRs), suite pytest completa.

## Estado actual

Gobernanza de la verdad operativa y verificada por gates. ADR-100 y ADR-101 aceptados. Dos gates nuevos corriendo sin condicion en pre-commit y CI, con 28 tests entre ambos. Los 5 CVs convergen a un solo juego de hechos; la unica divergencia admitida entre perfiles es el relato. El corpus de carrera esta completo salvo cuatro datos que Gonzo debe aportar.

## Proximos pasos

1) Gonzo aporta los cuatro faltantes de career-facts.md seccion 11: estudios formales, meses del PHP 2001-2008, clientes bajo NDA, referencias laborales. 2) Deuda declarada: un hecho agregado al corpus pero no propagado a ningun CV es deuda silenciosa, porque el gate ve lo que el CV declara y no lo que el corpus olvido usar; con 3 CVs activos no duele, con 10 si. 3) Deuda declarada en ADR-101: AGENTS-DETALLE solapa 29% de vocabulario con AGENTS.md y crece; SKILLS-INDEX no tiene generador y su fecha puede mentir. 4) memory/2026-10-19.md quedo con cambios sin commitear de otra sesion, no se toco.

## Decisiones y contexto que no debe perderse

- ADR-100: cada dato tiene un dueno declarado en AGENTS.md seccion 0 y la segunda copia es un bug, sin excepcion por conveniencia (la excusa 'el subagente solo recibe AGENTS.md' quedo invertida: si un dato tiene que estar ahi, ese es su dueno). ADR-101: el corpus es la verdad y el perfil es un filtro; una contradiccion se frena en el momento, se decide y se corrige el dueno, no se acumula. Decision de Gonzo sobre a11y: opcion C, sacar el numero y nombrar los roles (Super7UI y EY), porque un redondo se desmonta con una resta y los hechos no.

## Archivos tocados

```
memory/2026-10-19.md
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-20.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
