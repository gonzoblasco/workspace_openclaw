# ADR-084: Registros de sesion - un solo lugar, fuera del gate, con historia congelada

**Fecha:** 2026-09-29
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** auditoria Nivel 2 del workspace; quedaron tres pendientes de decision (`docs/conversations/`, `docs/history/`, `scripts/ui-measure.mjs`)
**Relacionado:** ADR-056 (guardas del pre-commit), ADR-073 (skills por rol), ADR-098 (proyectos en `projects/`), ADR-083 (frontera de roles)

---

## Contexto

El workspace guardaba "registros de conversacion" en **dos directorios** sin criterio que los separara:

- `docs/conversations/` (2 archivos, ambos del **mismo evento**: la sesion kanam-lab del 2026-09-16). Uno decia "Registro permanente", el otro "Archivo de conversacion". Eran **dos redacciones del mismo hecho**, con formato distinto y sin ninguna relacion entre si salvo la fecha.
- `docs/history/` (1 archivo, 2026-09-21). Mismo genero, carpeta distinta, sin ninguna regla que explicara por que estaba ahi y no en `conversations/`.

Tres problemas concretos, y ninguno es cosmetico:

1. **Dos casas para lo mismo.** Quien busca un registro tiene que adivinar la carpeta. El nombre `docs/history/` ademas era ambiguo: nacio de renombrar `docs/archives/` (reorg 2026-09-28), y `history` sugiere "historia del repo", no "registros de sesion".
2. **Duplicacion del mismo evento.** Los dos archivos del 09-16 dicen lo mismo con otras palabras. Un duplicado no es redundancia: es divergencia futura (se edita uno, el otro miente).
3. **Una entrada muerta en el gate.** `scripts/check-refs.py` tenia `SKIP_DIRS = ("docs/archives/", "docs/history/", "docs/conversations/")`. `docs/archives/` **ya no existe** desde el rename del 09-28. La lista nombraba un fantasma, y de paso cubria `docs/history/` (que si existe) por una razon que nadie habia escrito.

Ademas, el contenido de estos archivos **envejece en silencio**: el registro del 09-16 describe la eliminacion de dos tabs de `kanam-lab`, y el proyecto hoy los volvio a tener (commit `4587022`, 2026-09-29). Un registro asi no es una promesa sobre el arbol actual: es una **foto de un momento**.

---

## Decision

**Los registros de sesion viven en un solo lugar (`docs/records/`), son inmutables, y el gate no los escanea.**

1. **Un solo directorio.** `docs/records/`. Se eliminan `docs/conversations/` y `docs/history/`. Un registro que no sabe donde ir no es un registro: es un archivo perdido.
2. **Formato de nombre unico:** `YYYY-MM-DD-<tema>.md`. El tema describe el evento, no la carpeta de origen.
3. **Historia congelada: no se reescribe.** `docs/records/` entra en `SKIP_DIRS`. Un registro se lee como se escribio; corregirle un guion o un link roto lo falsifica. **El mismo criterio de ADR-056**, aplicado al directorio que si existe (no al fantasma `docs/archives/`).
4. **Sin duplicados.** Dos redacciones del mismo evento se **consolidan en un archivo** (se conserva la union, no se elige una y se tira la otra). La consolidacion es la unica reescritura permitida, y se hace una vez, al archivarlos.
5. **En `docs/records/` no se cita algo que no existe.** La inmutabilidad no exime de la regla de ADR-056: si el texto afirmaba un hecho hoy falso (los tabs eliminados que volvieron), **eso se registra en el archivo** como nota de desactualizacion, no se corrige el texto original ni se lo deja mentir sin aviso.

### Sobre `scripts/ui-measure.mjs`

**Se muda a la skill que lo posee** (`agents/kanam-dev/skills/cross-engine-css-measurement/scripts/`). Era un script huerfano en `scripts/`: nacio como one-shot del proyecto `kanam-story-bible` y no lo citaba nadie (solo se autocitaba en su comentario de uso). Un script de medicion de geometria pertenece a la skill de medicion de geometria, no a la raiz de tooling del workspace. El `ui-shot.mjs` especifico del proyecto ya queda donde estaba: el proyecto tiene su version, la skill se queda con la general.

---

## Consecuencias

### Positivas
- **Una sola puerta** para los registros de sesion, con un nombre que dice lo que es.
- **`SKIP_DIRS` deja de nombrar un fantasma.** Era una lista con una entrada muerta: el tipo de pudricon que el propio ADR-056 existe para atrapar, aplicado al checker que ese ADR introdujo.
- **El script de medicion tiene duenio.** Una skill que mide geometria provee su propio instrumento; el workspace deja de acumular huerfanos en `scripts/`.
- **La desactualizacion se declara.** Un registro del 09-16 que hoy ya no refleja el proyecto lo dice en una linea, en vez de mentir por omision.

### Negativas
- **Consolidar pierde la separacion por autor.** Aceptado: los dos archivos del 09-16 eran la misma sesion contada dos veces; separarlos no aportaba nada.
- **`docs/records/` no se verifica.** Aceptado por diseno: es historia. Si un registro necesita links vivos, no es un registro, es documentacion viva y va a `docs/`.

### Lo que NO cambia
- El gate sigue escaneando todo lo demas con markdown (ADR-056 intacto).
- La regla del guion comun sigue retirada (ADR-082); el hook sigue corriendo, pero aca no aplica porque no se reescribe historia.

---

## Alternativas consideradas

1. **Dejar `docs/conversations/` y renombrar solo `docs/history/`.** Rechazado: mantiene dos casas y el nombre `conversations` no cubre registros que no son conversacion (una sesion de autopsia, un postmortem).
2. **Borrar los tres archivos.** Rechazado: son el unico registro de esas sesiones; la memoria (`memory/archive/dailies/`) no cubre la remocion de tabs ni el detalle de la skill `kanam-lab-profile`. Se conserva consolidado.
3. **Conservar los duplicados.** Rechazado: divergen con el primer edit.
4. **Dejar `ui-measure.mjs` en `scripts/` "por si acaso".** Rechazado: es la logica que acumula huerfanos. Tiene duenio claro.

---

## Implementacion

| Pieza | Path |
|---|---|
| Registros consolidados | `docs/records/YYYY-MM-DD-<tema>.md` |
| Gate | `scripts/check-refs.py` (`SKIP_DIRS`) |
| Script con duenio | `agents/kanam-dev/skills/cross-engine-css-measurement/scripts/ui-measure.mjs` |

## Referencias

- ADR-056: las guardas del pre-commit y por que la historia no se chequea
- ADR-073: el ciclo de skills vive en `agents/<rol>/skills/`
- `memory/2026-09-29.md`: la auditoria Nivel 2 que dejo estos tres pendientes
