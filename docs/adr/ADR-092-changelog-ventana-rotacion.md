# ADR-092: El CHANGELOG vive en una ventana activa de ~30 días, con rotación automatizada

**Fecha:** 2026-10-06
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** sesión 2026-10-06 - Gonzo: *"habría que crear un script para automatizar la redacción del changelog... que lo obligue a mostrar solo los últimos 30 días o sino archivarlo... así nunca cavilemos a quedar desfasados"*
**Relacionado:** ADR-055 (bloques managed desde la DB), ADR-056 (guardas de gobernanza en el pre-commit), ADR-065 (DB-first vs doc-only), ADR-082 (fin de la regla del guion)

---

## Contexto

`CHANGELOG.md` creció de forma append-only desde el inicio del workspace: **310 KB, 2.829 líneas, ~186 entradas desde julio**. El log de dreaming (`DREAMS.md`) sufría el mismo problema. Ningún humano lo lee entero; el archivo activo deja de orientar y pasa a ser un depósito.

La primera poda se hizo a mano el 2026-10-06: se movió a `docs/archive/` todo lo anterior al 2026-09-06 (hoy en `docs/archive/CHANGELOG-archive.md`). El CHANGELOG activo quedó en **108 entradas (2026-09-09 → 2026-10-06)**, y el archivo con las **78 restantes**.

Pero una poda manual no resuelve el problema: en 30 días hay que acordarse de nuevo. **El objetivo no es el tamaño, es que nunca quede desfasado sin que nos demos cuenta.** Una regla sin enforcement se viola sola (ADR-083): si la rotación depende de la memoria, vuelve el mismo depósito.

## Decisión

**El `CHANGELOG.md` activo contiene solo las entradas de los últimos ~30 días; lo anterior vive archivado. La rotación la automatiza `scripts/changelog-rotate.py`.**

1. **Ventana activa:** 30 días por defecto (`--days N` configurable). El corte lo fija la fecha de hoy menos N días. Las entradas se ordenan por fecha descendente, estables dentro del mismo día.

2. **Archivo rodante único:** `docs/archive/CHANGELOG-archive.md`. Acumula la historia; **nunca se pierde una entrada**. No hay nombres con fecha que decidir: al archivar, lo viejo se suma al archivo.

3. **Header generado:** el script reescribe el encabezado del activo (corte vigente + link al archivo) y el del archivo. **Nadie lo edita a mano**: es el mismo patrón de bloques administrados de ADR-055, aplicado a un doc en vez de a la DB.

4. **Idempotente:** correrlo dos veces no cambia nada la segunda. Escribe solo si el contenido difiere, así normaliza el header (self-heal) sin ruido.

5. **Enforcement en dos puntos, con disparadores distintos:**
   - **pre-commit (`--check`):** si `CHANGELOG.md` está staged fuera de la ventana, el commit **falla** con la instrucción de rotar. Corre **solo cuando el propio CHANGELOG.md está staged** - no bloquea commits ajenos por un archivo que nadie tocó.
   - **cierre de sesión:** `session-end.sh` corre la rotación sin flags. La ventana se cierra en cada sesión, no "alguna vez".

6. **El activo se puede reconstruir desde cero.** Cuando arrastre hipótesis refutadas (como pasó con `NORTH.md`/`ROADMAP.md`), se reescribe el activo y lo viejo queda en el archivo. La rotación es mecánica; la reconstrucción es editorial y sigue siendo decisión humana.

## Consecuencias

- **A favor:** el activo siempre refleja ~30 días, sin depender de que alguien se acuerde. El ruido deja de acumularse en la superficie que se lee. El archivo conserva la historia sin costo de lectura.
- **A favor:** el mecanismo es determinista y testeado (`tests/python/test_changelog_rotate.py`): split, ventana, idempotencia, acumulación sin duplicados, orden, exit codes de `--check`.
- **Aceptado:** el archivo crece sin límite. Es el precio de no perder historia; su lectura no es obligatoria y no compite con el activo.
- **Nota:** `DREAMS.md` se rotó a mano por mes el mismo día (a `memory/archive/dreaming/`). Es estado local gitignored del plugin de dreaming; automatizar *su* rotación es una tarea aparte, con su propio runner.
- **Historia congelada:** los bloques rotados conservan los guiones largos y las rutas de la época (un ADR luego renombrado, por ejemplo). `docs/archive/` queda excluido de la regla del guion (hook) y de `check-refs.py`, con la misma política que `docs/records/` (ADR-084/ADR-082): se lee como se escribió.

## Alternativas

- **Solo poda manual:** rechazada - ya se hizo una vez y el problema vuelve en 30 días.
- **Borrar lo viejo en vez de archivar:** rechazada - la historia es trazabilidad; el costo de guardarla es nulo.
- **Archivo por rango de fecha (`CHANGELOG-pre-YYYY-MM.md`):** rechazada como mecanismo primario - obliga a decidir nombres y multiplica archivos. Se usó una vez para la migración manual; el mecanismo automatizado usa un archivo rodante único.
- **Rotalo por tamaño en vez de por fecha:** rechazada - "30 días" es una ventana temporal legible; el tamaño es una consecuencia, no el criterio.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
