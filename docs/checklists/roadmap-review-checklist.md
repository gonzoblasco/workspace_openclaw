# Checklist: Revision del ROADMAP

> Procedimiento para revisar `docs/ROADMAP.md` contra fuentes reales. Nace 2026-09-14, despues de que el documento durmiera 17 dias con los 11 items en verde y 22 acciones abiertas abajo.

**Por que existe:** el ROADMAP no falla por falta de contenido, falla por marcar verde sin evidencia. El commit del 28/08 se llama *"complete roadmap - all items green"* y no correspondia. Este checklist evita repetirlo.

**Regla madre:** la revision se hace **contra fuentes reales** (git, GitHub, filesystem, logs, DB), nunca contra lo que creemos recordar. Si un item no se puede verificar con una fuente, queda 🟡, no 🟢.

---

## Cuando correrlo

- Al cerrar una sesion que toco infraestructura, pipeline, portfolio o estrategia.
- Semanal, si no hubo sesion que lo tocara.

## Pasos

### 1. Inventario
Listar todos los `[ ]` y los estados (🔴/🟡/🟢) del documento. Para cada uno, anotar **la fuente que lo probaria**.

### 2. Verificar item por item (fuente -> veredicto)
Cada item cae en exactamente una de estas categorias:

| Veredicto | Que hacer |
|---|---|
| **Hecho** | Tachar `[x]` con la evidencia y la fecha entre parentesis. |
| **Pendiente** | Dejar `[ ]`. Si es tarea concreta y fechada, moverla a `memory/memory.db` (`todos`) y dejar aca solo el estado de la capa. |
| **Obsoleto** | Borrar (no tachar). Un item fechado que ya paso no es deuda, es ruido. |
| **Regla** | Sacarlo de los checkboxes y escribirlo como regla operativa. Las reglas no se tachan. |
| **Restriccion cerrada** | Sacarlo de los checkboxes. Una decision cerrada por ADR no es accion pendiente. |

### 3. Fuentes por item (que mirar, no que recordar)
- **Estado de repo / trackeo:** `git status --short`, `git ls-files`, `git check-ignore -v`.
- **Archivos archivados:** `gh repo view <owner>/<repo> --json isArchived`.
- **Hooks / tooling:** listar `projects/*/.git/hooks/pre-commit` y buscar `simple-git-hooks` en los `package.json`.
- **Infra / reinicios:** `wc -c AGENTS.md MEMORY.md` (limite bootstrap 20.000), `~/.openclaw/logs/gateway-restart.log`, `~/.openclaw/logs/stability/`.
- **Proyectos / anclas:** `projects/*/.knowledge/ADR-*.md`, `docs/NORTH.md`.
- **Busqueda laboral:** `docs/entrevistas/job-search-tracker.md` (unica tabla de procesos).
- **Cadencia de posts:** `ls -1 docs/linkedin/` con fechas de modificacion.

### 4. Recalcular estados
Un item solo puede estar 🟢 si su **señal de listo** esta verificada. Si la señal no se corrio, es 🟡 aunque "ande bien". Si hay evidencia de regresion, 🔴.

### 5. Reconciliar la tabla de prioridad
La tabla del final debe coincidir con los encabezados de cada seccion. Si no coinciden, el documento miente.

### 6. Cerrar
- Actualizar la linea `Ultima revision: YYYY-MM-DD` del encabezado.
- Dejar en el daily una linea con el delta (cuantos items cerraron, cuantos se abrieron, que estado cambio).

---

## Antipatrones (vistos en carne propia)

- **Marcar 🟢 por optimismo.** El 28/08 se pusieron los 11 en verde sin correr las señales de listo. Resultado: 17 dias de falso verde.
- **Usar el ROADMAP como backlog.** Los items fechados del 31/08 (reintentar assessment, manejar aviso de OpenSistemas) vencieron y quedaron ahi. El backlog va a la DB.
- **Confiar en el estado del encabezado.** Los encabezados decian 🟢 mientras abajo habia 22 acciones abiertas. Siempre gana la evidencia del filesystem, no el emoji.
- **Revisar de memoria.** Si no se abrio la fuente, no es una revision: es una reescritura de lo que creiamos.

---

## Relacion con otros documentos

- `docs/NORTH.md` - el "para que" de largo plazo. El ROADMAP no lo redefine.
- `memory/memory.db` (`todos`, espejo `memory/todos.md`) - las tareas concretas y fechadas.
- `docs/ROADMAP.md` - que decisiones tomamos y en que estado esta cada capa.
- `docs/ROADMAPS.md` - el **Roadmap de Roadmaps**: el indice de madurez de los 7 roles.
- `docs/checklists/roadmap-authoring-guide.md` - el estandar de formato de un roadmap de rol.
- `docs/adr/` - las decisiones cerradas. Si un item del ROADMAP contradice un ADR, gana el ADR.

---

## Variante: revisar un ROADMAP de rol

> Anadida 2026-10-07, junto con `docs/ROADMAPS.md`. Los roadmaps de rol (`agents/<rol>/ROADMAP.md`)
> se revisan con la misma regla madre -contra fuentes reales- pero con un foco distinto: no
> "que capa esta estable", sino **"la version declarada no miente"**.

**Cuando correrla:** al cerrar una sesion que toco el roadmap de un rol, la tabla de `docs/ROADMAPS.md`,
un cambio de capacidad del rol, o cuando el guard lo marque.

### Pasos

1. **Correr el guard (barato, primero):** `python3 scripts/check-roadmaps.py`. Verifica existencia,
   encabezado, secciones, marcador de proyecto y **coherencia de version** contra el indice.
   Si falla, ahi esta el trabajo.
2. **Verificar el retrato (seccion 2):** cada fila de la tabla capacidad->estado se prueba contra
   el filesystem, el codigo o el runtime del rol. Un `✅` sin fuente es un falso verde.
3. **Verificar el salto de version:** si el rol declara una version nueva, su **criterio de listo**
   tiene que estar cumplido con evidencia reproducible. Un numero editado no es un salto.
4. **Reconciliar el indice:** la version del archivo del rol y la fila de la tabla en
   `docs/ROADMAPS.md` deben coincidir. Cuando discrepan, **gana el archivo del rol** (la evidencia)
   y se corrige el indice.
5. **Cerrar:** actualizar `Ultima revision:` dentro del roadmap del rol, y dejar el delta en el daily.

### Antipatrones propios de los roadmaps de rol

- **Marcar verde por optimismo.** El retrato no es una promesa de lo que el rol hara: es un espejo
  de lo que el rol **es hoy**, probado contra su arbol.
- **Editar el numero sin ganarselo.** v0.1 es el default; cada salto pide su senal de listo.
- **Dejar que el indice derive del archivo.** La tabla de `docs/ROADMAPS.md` no manda: es un espejo
  que hay que corregir cuando el archivo cambia.
- **Copiar el formato sin el criterio.** Las 7 secciones son el esqueleto; lo que vale es que cada
  hito haya pasado por "¿esto desbloquea algo?".
