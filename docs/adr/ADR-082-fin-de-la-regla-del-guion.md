# ADR-082: La regla del guion comun deja de ser obligatoria

**Fecha:** 2026-09-29
**Estado:** Aceptado
**Decisores:** Gonzo (definicion explicita)
**Origen:** sesion 2026-09-29 - Gonzo: *"quiero quitar la regla de los guiones, creo ya tenemos una evolucion y una robustez para tener identidad propia, dejemos de perder tiempo y recursos revisando los guiones"*
**Relacionado:** ADR-056 (guardas de gobernanza en el pre-commit), ADR-071 (hyphen enforcement)
**Supersede:** la regla del guion comun en `USER.md`, `MEMORY.md`, `AGENTS.md`, `CONTRIBUTING.md` y los archivos de instruccion de los agentes

---

## Contexto

La regla del guion comun (`-` siempre, nunca em dash U+2014 ni en dash U+2013) nacio de un error real: el 2026-08-22 se escapo un em dash en el body del PR astryx #5344 y Gonzo lo corrigio a mano. La leccion de entonces fue que una regla escrita en memoria no alcanza: hace falta un mecanismo. Ese mecanismo es `scripts/check_em_dash.py`, la seccion de `CONTRIBUTING.md` y el guard del pre-commit.

En los meses siguientes la regla se consolido, se institucionalizo (ADR-056, ADR-071) y se le puso un techo de mantenimiento: 225 archivos historicos con guiones largos en `memory/`, exclusiones por rename, excepciones por proyecto (la novela) y un enforcer de portabilidad dudosa. La disciplina se sostuvo, pero el costo creciente es de mantenimiento del aparato, no del objetivo original.

## Decision

**La regla del guion comun deja de ser una regla obligatoria del workspace.**

1. **Se retira la regla declarada** de `USER.md`, `MEMORY.md`, `AGENTS.md`, `CONTRIBUTING.md` y de los archivos de instruccion de los cuatro agentes (`kanam-mind`, `kanam-dev`, `kanam-ops`, `kanam-studio`), junto con su eco en skills y docs de metodo.

2. **Se retira la obligacion de escanear.** El scan manual con `scripts/check_em_dash.py` deja de ser un paso previo obligatorio a publicar.

3. **El aparato mecanico no se desarma ahora.** El hook del pre-commit, `scripts/check_em_dash.py`, `scripts/hyphen_enforcer.sh` y `scripts/test-skills.sh` se conservan tal como estan: siguen corriendo y no molestan. Desarmarlos es una tarea aparte, con su propia verificacion, no un efecto colateral de esta decision.

4. **Los proyectos actuales no se tocan.** No hay barrido retroactivo: lo que ya existe en los proyectos se deja como esta.

5. **No es una decision hacia atras.** Los PRs y comentarios ya publicados no se reeditan. La regla se retira hacia adelante.

## Consecuencias

* **A favor:** deja de consumir atencion y tokens en una revision que el objetivo original (evitar un guion idiomatico en textos largos en ingles) ya no justifica; el mecanismo que la hacia cumplir sigue en pie.
* **En contra (aceptado):** sin la regla declarada, los textos nuevos pueden volver a traer em dashes. Es el trade-off explicito: identidad propia por encima del cosmético.
* **Vigencia del mecanismo:** mientras el hook siga activo, un markdown staged con em dash todavia puede bloquear el commit del workspace. Es una consecuencia tecnica, no una regla vigente; quien la padezca decide si desarma el check en su tarea.

## Notas

* **No es una reversion de ADR-056/ADR-071 de un plumazo.** Esos ADRs describen guardas que hoy siguen existiendo en el codigo. Este ADR retira la *obligacion de estilo*, no la implementacion. Si mas adelante se desarman los scripts, corresponde un ADR que los supersede explicitamente.
* **La excepcion de la novela** (`docs/stories/quienes_quedan/`, raya U+2014 como raya de dialogo) queda sin objeto como excepcion, pero no se toca el manuscrito.
