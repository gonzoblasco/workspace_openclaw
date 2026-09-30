# ADR-056: Guardas de gobernanza en el pre-commit - guion comun y rutas citadas

**Fecha:** 2026-09-22
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** auditoria #2 tras ADR-055; la regla del guion comun y las rutas citadas se cumplian solo dentro de `skills/`
**Relacionado:** ADR-055 (bloques managed), ADR-038 (docs narrativos), ADR-054 (kanam-os), ADR-084 (registros de sesion: reemplaza la lista de directorios historicos)

---

## Contexto

Dos reglas duras del workspace se verificaban solo en una parte del repo:

1. **Guion comun siempre** (`AGENTS.md`, "Reglas de oro"). El chequeo vive en `scripts/test-skills.sh`, que recorre **unicamente `$SKILLS_DIR`**. Los `docs/` nunca se miraban.
2. **Las rutas citadas deberian existir.** No habia ningun chequeo. `docs/AGENTS-DETALLE.md` citaba `scripts/pr-thread-brief.sh` como la **"verificacion mecanica"** de la regla de atribucion por login, y **ese script nunca existio en git** (`git log --all` vacio).

El costo de lo primero, medido: **44 en dash y 2 em dash acumulados en 8 archivos de docs**, violando una regla declarada. El costo de lo segundo es peor y no es cosmetico: una regla que **dice** tener respaldo mecanico sin tenerlo es peor que una regla sin respaldo, porque induce a confiar en un chequeo que nadie corre. Esa regla existe justamente por un error real (astryx #4690: el `CHANGES_REQUESTED` de un maintainer se reporto como nuestro por proximidad de contexto).

El patron detras de los dos: **la regla se aplico a la superficie que se estaba mirando en ese momento, no a la que la regla nombra.**

---

## Decision

**El pre-commit verifica guion comun y rutas citadas sobre TODO markdown staged, no solo sobre `skills/`.**

```sh
MD_CHANGED=$(echo "$CHANGED" | grep -E '\.md$' || true)
if [ -n "$MD_CHANGED" ]; then
  # 1) guion largo -> abort (sobre el contenido STAGED, no el del disco)
  # 2) rutas citadas -> check-refs.py --all
fi
```

Tres decisiones concretas dentro de esto:

1. **Se chequea el contenido staged** (`git show ":$f"`), no el del disco. Es lo que se commitea; chequear el disco deja pasar el caso de archivo editado y no re-agregado.
2. **`scripts/check-refs.py` ignora los directorios historicos.** Una ruta rota ahi es un dato del pasado, no una promesa vigente. Corregir historia la falsifica. **Nota (ADR-084, 2026-09-29):** la lista original nombraba `docs/archives/` y `docs/conversations/`; hoy es un unico directorio, `docs/records/`. El criterio no cambio, solo su lista.
3. **Los chequeos baratos corren siempre; los caros siguen acotados.** Guion y refs son dos procesos de Python sobre archivos staged: baratos. La suite completa (bats + pytest, ~40s) sigue disparandose solo cuando cambian `skills/` o `scripts/`.

### Lo que NO se chequea, a proposito

- **U+2011 (guion no separable).** La regla nombra U+2013/U+2014. U+2011 aparece en rangos tipo `1-5`, donde es separador de rango, no puntuacion. Marcarlo daria falsos positivos en todo rango de paginas.
- **`\n` literales.** Se corrigieron los de `cpacc-improvements.md`, pero no se agrego un chequeo: distinguir un escape real de un ejemplo de codigo exige parsear markdown, y el falso positivo costaria mas que el caso.

---

## Consecuencias

### Positivas
- **La regla del guion deja de tener una zona ciega.** Era una regla dura con un agujero del tamano de `docs/`, y la evidencia (44 violaciones) muestra que el agujero se usaba.
- **Las rutas citadas dejan de mentir.** `scripts/pr-thread-brief.sh` ahora existe y hace lo que el doc prometia.
- **Guardas probadas en negativo.** Un guard que nunca falla no se distingue de un guard ausente. Ambas rutas se probaron abortando de verdad (en dash y ruta rota, con archivos temporales).

### Negativas
- **El commit se puede bloquear por un guion en un doc.** Aceptado: es la regla que Gonzo ya declaro, y el arreglo es un `sed`.
- **`check-refs.py --all` recorre `docs/` en cada commit con markdown.** Medido: 133 rutas, imperceptible.
- **Una referencia legitima a un archivo que todavia no existe se bloquea.** Aceptado: se agrega el archivo, o se deja de citar. Un doc que promete algo inexistente es el bug.

---

## Alternativas consideradas

1. **Extender `test-skills.sh` a todo el repo.** Es un script atado a la estructura de skills (frontmatter, links entre skills); forzarlo a recorrer `docs/` mezcla dos responsabilidades. Rechazado: se prefirio un checker propio (`check-refs.py`) con su propia semantica.
2. **Chequear el disco en vez del staged.** Deja pasar el archivo editado despues del `git add`. Rechazado.
3. **Chequear tambien los historicos.** Convertiria el archivo historico en un documento que se reescribe a si mismo. Rechazado.
4. **Un hook que arregle en vez de avisar.** Un hook que edita lo que estas por commitear sorprende y puede romper trabajo ajeno. Rechazado: aborta y dice donde.

---

## Implementacion

| Pieza | Path |
|---|---|
| Checker de rutas | `scripts/check-refs.py` (`--all` incluye `docs/**`; `SKIP_DIRS` = `docs/records/`, ADR-084) |
| Script que respalda la regla | `scripts/pr-thread-brief.sh` |
| Tests | `tests/python/test_check_refs.py` (11) |
| Hook | `scripts/pre-commit.template` (+ instalado en `.git/hooks/pre-commit`) |

## Referencias

- `docs/AGENTS-DETALLE.md`: regla de atribucion por login (2026-09-22)
- ADR-055: el otro mecanismo que convierte una regla declarada en una verificada
- Leccion de la clase de bug: una regla verificada solo en la superficie que se estaba mirando deja el resto del repo sin verificar, y la evidencia de que se usa el agujero esta en el repo mismo
