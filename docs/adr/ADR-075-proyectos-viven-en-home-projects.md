# ADR-075: Los proyectos viven en `~/projects`, fuera del worktree del workspace

**Fecha:** 2026-09-27
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** sesion de recuperacion 2026-09-27 - el movimiento a `~/projects` no estaba documentado en ningun ADR y el workspace conservaba el arbol viejo como bajas sin commitear
**Relacionado:** ADR-073 (arquitectura multi-agente), ADR-056 (guardas de gobernanza), ADR-066 (los guardias no leen codigo de proyecto)

---

## Contexto

Hasta 2026-09-25 los proyectos vivian en `workspace/projects/<slug>/`. El git del workspace trackeaba **solo su `.knowledge/`** (memoria), mediante el bloque del `.gitignore` que ignora todo `projects/` salvo `projects/*/.knowledge/`. El codigo de cada proyecto vivia en su propio repo de GitHub, y en el agregado privado `projects_openclaw`.

El **2026-09-26**, durante la migracion multi-agente (ADR-073), los proyectos se movieron a `~/projects/`, fuera del worktree del workspace. Verificado en disco y en git:

- `~/projects/` existe desde 2026-09-26 14:54, con 32 directorios de proyecto.
- `workspace/projects/` **ya no existe en disco**.
- El git del workspace conserva **143 archivos** del arbol viejo (casi todos `.knowledge/`) como bajas sin commitear.
- De esos 143, **135 tienen copia identica o equivalente en `~/projects`**; 8 no tienen copia (ver Consecuencias).

El movimiento no quedo registrado en ningun ADR, ni se actualizaron `AGENTS.md` ni `.gitignore`, que siguen describiendo la ubicacion vieja.

## Decision

**La ubicacion de trabajo de los proyectos es `~/projects/<slug>/`, fuera del workspace.**

> **SUPERSEDED por ADR-098 (2026-10-08): "Los proyectos vuelven al workspace, y `cwd` separa el hogar del agente de su zona de trabajo".** Los proyectos vuelven a `<workspace>/projects/` (dentro del árbol del gateway); `~/projects` pasa a ser un symlink a `~/.openclaw/workspace/projects`. El cuerpo de este ADR describe el estado de 2026-09-27 y se conserva como registro histórico. **Leer ADR-098 para el estado vigente.**

- El codigo del proyecto y su `.knowledge/` conviven en `~/projects/<slug>/`.
- **11 de los 32 proyectos** tienen su propio repo git en `~/projects/<slug>/.git`; la mayoria excluye su `.knowledge/` via `.git/info/exclude`.
- El workspace (`~/.openclaw/workspace`) **deja de hospedar el arbol `projects/`**.

Esta decision **documenta el estado actual**; formaliza lo que ya es de hecho, para que el workspace deje de arrastrar el arbol viejo y las reglas dejen de describir una ruta que ya no existe.

### La memoria de proyecto (el `.knowledge/`) es parte del proyecto

Gonzo, 2026-09-27: *"el `.knowledge` ya no viaja, es parte de cada proyecto... o sea, va con el proyecto... al mover los proyectos del workspace ya quito su responsabilidad"*.

Esto cierra la pregunta que quedaba abierta: el workspace **no** es responsable de la memoria de proyecto. El `.knowledge/` vive dentro de `~/projects/<slug>/` y viaja con el proyecto, en el repo del proyecto. No se re-tracking en el workspace, ni se mueve al agregado como mecanismo primario, ni se centraliza en la DB de vectores.

**Pendiente operativo (backlog, todo #61):** sincronizar los proyectos a un repo nuevo. Diferido a proposito por Gonzo. Hoy 135 archivos `.knowledge/` viven solo en disco, sin respaldo en git - el respaldo llega con esa sincronizacion.

## Consecuencias

### Positivas
- Un solo lugar para el codigo y la memoria de cada proyecto.
- El workspace deja de cargar el arbol de proyectos: menos ruido de untracked y menos superficie para barridos accidentales (el mismo barrido que se llevo `memory.db` arrastro estas bajas).

### Negativas / pendientes
- **El workspace ya no trackea `.knowledge/`** (por diseno, ver Decision). La memoria de proyecto es del proyecto y viaja con el. Hoy la mayoria de los repos de proyecto excluyen su `.knowledge/` y `~/projects` no es repo, asi que esa memoria vive solo en disco: el respaldo llega con la sincronizacion del todo #61.
- **`AGENTS.md` y `.gitignore` actualizados en la misma sesion.** `AGENTS.md` ahora describe `~/projects` y aclara que el workspace ya no trackea `.knowledge/`; el `.gitignore` reemplaza el bloque muerto de `projects/` por una sola regla de ignorado.
- **8 archivos `.knowledge/` sin copia en `~/projects`** (siguen solo en HEAD): 6 de `kanam-solitaires` (hoy dividido en `kanam-solitaires-v1` / `kanam-solitaries-v2`) y 2 de slugs sin carpeta (`workspace-general`, `workspace`). Recuperables desde git (`git show HEAD:<path>`).
- **Las 143 bajas del arbol `projects/`** del workspace son el arbol viejo, ahora redundante: se commitearon como limpieza legitima.
- **`aggregate-sync.sh` actualizado.** Resolvia `PROJECTS_DIR="${WORKSPACE_DIR}/projects"`; ahora apunta a `~/projects` (override con `PROJECTS_DIR`) y falla con un mensaje que incluye como inicializar el agregado.

## Notas
- El movimiento ocurrio junto con la migracion de skills a `agents/<rol>/` (ADR-073). Ambos comparten el mismo origen y el mismo problema: se aplicaron a medias, sin cerrar el estado en git ni actualizar las reglas.
- Antes de este ADR, `~/projects` ya era un directorio con proyectos sueltos (algunos desde 2026-09-08). Lo que decide este ADR no es su creacion, sino que **pasa a ser la ubicacion oficial**, en reemplazo de `workspace/projects/`.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
