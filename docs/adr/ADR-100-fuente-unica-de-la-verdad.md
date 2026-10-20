# ADR-100: Fuente única de la verdad - un dato, un dueño, y un gate que lo verifica

**Fecha:** 2026-10-20
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** workspace - "necesitamos definir una unica fuente de la verdad y no tantos md que pueden chocarse y lo hacen a diario"
**Relacionado:** ADR-055 (bloques managed), ADR-065 (DB-first vs doc-only), ADR-083 (una regla sin guarda se viola sola), ADR-092 (ventana del CHANGELOG)

---

## Contexto

La queja de Gonzo no era estética. El 2026-10-20 el workspace tenía 1.859 archivos markdown y, más importante, **ningún archivo tenía dueño de un dato**. Los gates existentes verificaban que las rutas citadas existieran (`check-refs.py`), que los ADRs estuvieran indexados y que los valores repetidos se propagaran (`managed-blocks.py`), pero **nada** verificaba que una afirmación viviera en un solo lugar.

Resultado medido ese mismo día, antes de escribir una línea de código:

| Contradicción viva | Archivo | Archivo |
|---|---|---|
| "Kanam en thinking **max**, agentes A/B en **high**" vs. "thinking global `off`" | `docs/SETUP.md` | `AGENTS.md` (bloque managed) |
| El mismo archivo declara la política **vigente y SUPERSEDED en la misma frase** | `docs/SETUP.md:27` | (mismo archivo) |
| Tabla completa de 8 roles con modelo y fallback | `docs/ROADMAP.md` | `AGENTS.md` (bloque managed) |
| Estados de `soporteml` con distinto nivel de detalle | `docs/NORTH.md` | `MEMORY.md` + `ROADMAP.md` |
| `memory.db` como fuente de verdad, 3 redacciones distintas | `AGENTS.md` | `docs/SETUP.md` + `docs/ROADMAP.md` |
| Lucide, Stripe, pre-commit, validación UI repetidos | `AGENTS.md` | `MEMORY.md`, `docs/learnings/*` |
| 4 skills citadas como "las más usadas" que **no existían** | `AGENTS.md:100` | (no existian) |

Ese último caso es el que midió el costo real: `knowledge-management`, `incremental-implementation`, `background-execution` y `a11y-at-validation` no existían en `skills/` ni en `agents/*/skills/`. `check-refs.py` no las veía porque no eran rutas, eran backticks sin `scripts/` o `docs/`. La instrucción era inequívoca y apuntaba a la nada.

El patrón de fondo: **un dato que se repite no tiene dueño, y lo que no tiene dueño lo edita cualquiera**. La memoria del sistema no fallaba por falta de documentación - fallaba por exceso de copias.

## Decisión

### 1. Un dueño declarado por familia de dato

Vive en `AGENTS.md`, sección 0, porque es la única guía que **todos** los subagentes reciben:

| Dato | Dueño |
|---|---|
| Reglas duras (cómo actúo) | `AGENTS.md` |
| Quién es Gonzo y cómo hablarle | `USER.md` |
| Quién soy | `SOUL.md` + `IDENTITY.md` |
| Estado y hechos vigentes | `MEMORY.md` |
| Por qué se decidió | `docs/adr/` (append-only) |
| Entorno (máquinas, modelos, scripts) | `docs/SETUP.md` |
| Valores repetidos (modelos, pipeline) | `memory.db` → bloques managed |
| Procedimiento de una tarea | `skills/<slug>/SKILL.md` |

Los demás archivos **citan**, no repiten.

### 2. La segunda copia es un bug, no una convención

No hay excepción "por conveniencia" ni "porque el subagente solo recibe AGENTS.md". Esta última era la excusa que había justificado duplicar modelos en cuatro archivos. Si un dato tiene que estar en `AGENTS.md` porque los subagentes no ven otra cosa, entonces **ese es su dueño** y los demás lo citan - no al revés.

Consecuencia práctica: `docs/ROADMAP.md` dejó de tener la tabla de 8 roles con modelo y fallback. Mide **estado**, no declara asignaciones. `MEMORY.md` dejó de repetir iconos, pagos y pre-commit: los cita.

### 3. Enforcement: `scripts/check-single-source.py`

Una regla sin guarda se viola sola (ADR-083). El gate corre **sin condición** en pre-commit y en CI, porque la duplicación nace de una edición en cualquier archivo normativo, no de un pathspec predecible.

Verifica dos clases:

**a) Repetición literal.** Una línea normativa (≥60 chars) que aparece en dos archivos normativos con similitud Jaccard ≥ 0.55. Los títulos quedan exentos: un encabezado es el **nombre** de la regla, no la regla, y citarlo es como nombrar un archivo.

**b) Modelo fuera de casa.** Los tags de modelo (`nombre:cloud`, `gemma4:e4b-mlx`) se declaran en `memory.db` y se propagan a los bloques `MANAGED`. Un tag escrito a mano en un archivo normativo es una copia que el propagador no puede corregir. Dueños: `AGENTS.md` (solo entre marcadores) y `docs/SETUP.md` (el **catálogo** de modelos instalados es su dato, distinto de la asignación por rol). La historia -benchmarks, decisiones superadas- se marca con `<!-- modelo: historico -->`.

### 4. Lo que el gate NO hace

No compara contra la DB ni contra ADRs. Un ADR es registro histórico y puede decir lo que decía la política en su fecha; el estado vigente vive en `MEMORY.md` y en los bloques managed. Tampoco entra a `memory/` ni a `docs/archive/`: la historia congelada se lee como se escribió.

## Consecuencias

### Positivas
- El drift deja de depender de que alguien compare archivos a mano. El 2026-10-20 el gate cazó **5 copias y 16 tags escritos a mano** en su primera corrida, sobre un árbol que todos los demás gates daban verde.
- Las skills fantasma no vuelven: citar una skill que no existe ahora es una ruta rota visible para `check-refs.py --all`, y la lista de "más usadas" se corrigió a skills reales.
- La sección 0 de `AGENTS.md` es la respuesta directa a "¿dónde vive este dato?" sin abrir cinco archivos.

### Negativas
- **Un dato nuevo exige decidir el dueño antes de escribirlo.** Es fricción deliberada: es la que faltaba.
- El umbral 0.55 puede marcar dos reglas parecidas pero distintas como duplicadas. El escape es redactar una con el dueño y citar en la otra, que es el comportamiento que se busca.
- Los tags de modelo escritos a mano requieren disciplina de marcado para la historia. Sin la marca, el gate bloquea.

### Deuda declarada
- `docs/AGENTS-DETALLE.md` solapa 29% de vocabulario con `AGENTS.md`. El gate no lo caza porque el detalle **amplía** en vez de repetir, pero el solapamiento es real y crece. El to-do de refactor de `AGENTS.md` (en `memory/todos.md`) sigue abierto.
- `SKILLS-INDEX.md` no tiene generador: se actualiza a mano y su fecha declarada puede mentir. Candidato a gate propio.
