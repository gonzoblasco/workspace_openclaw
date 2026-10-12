# Lab - Laboratorio de Pruebas para `evidence-hunter`

> **Quién soy y para quién soy en este acto.**
> Yo soy **The Critic**. Mi interlocutor de calidad es **The Crew Planner** y, en última instancia, **Kanam CORE**. Mis veredictos son evidencia dura, no buenas intenciones.
> En este acto soy *both*: el sujeto bajo prueba (la skill que cazo evidencia para mis veredictos) y el auditor de mí mismo (no me apruebo sobre auto‑reporte).
> **Para quién:** para Gonzo (operador) que invierte tiempo en verificar; para Kanam CORE que orquesta el pipeline; para el autor de un futuro entregable que recibirá un veredicto basado en este laboratorio.

## ¿Por qué existe este laboratorio?

`evidence-hunter` declara cuatro estados:

- **verificado** - la evidencia existe y se reproduce en disco.
- **parcial** - existe una parte; la otra falla.
- **auto‑reportado** - el autor lo dijo, pero en disco no aparece.
- **bloqueado** - no se pudo ejecutar el detector (dependencia ausente, sintaxis rota, etc.).

Sin un set canónico de casos, esos cuatro estados son palabras, no contrato.

## Regla de oro del laboratorio

Cada caso declara **una** afirmación del autor, **un** detector esperado y **un** veredicto esperado.
Si el hunter emite otra cosa, falla la prueba. **Si el hunter emite el status correcto pero la cita no matchea el regex del caso, también falla** (`validate.py` distingue `PASS` de `CITAFALLA` para no premiar la coincidencia laxa).

## Casos

Fuente única de verdad: [`cases.py`](./cases.py). La tabla siguiente se mantiene sincronizada con ese módulo.

| # | Nombre | Afirmación del autor | Detector esperado | Estado esperado | Patrón de cita (regex) |
|---|--------|----------------------|-------------------|-----------------|------------------------|
| 1 | El Mentiroso | "Hay tests unitarios para `foo()`" | `grep` de archivos `test_*.py` | `auto-reportado` | solo presencia |
| 2 | El Casi‑Listo | "La función `foo()` está cubierta y pasa el test" | `pytest` (real) | `parcial` | `tests/test_foo.py` o `command not found` |
| 3 | El Invisible | "Uso el token `color-primary`" | `rg` en `.scss/.css` | `auto-reportado` | solo presencia |
| 4 | El Oro | "La función `foo()` está cubierta y el test pasa" | `pytest` | `verificado` | `tests/test_foo.py` |
| 5 | El Bloqueado | "La cobertura de tests es > 80 %" | `coverage` ausente | `bloqueado` | `command not found` o `not installed` |

> **Caso 2 - trampa calibrada:** si pytest no está en el PATH, el hunter cae legítimamente a `bloqueado`. `validate.py` lo reporta distinto al FAIL simple (`BLOCKED-NOT-PARTIAL`). Esto evita falso verde y falso rojo.

## Ejecución

```bash
# 1. Preparar el sandbox (archivos dummy + auto-verificación de trampas)
python3 tests/evidence-hunter/scaffold.py

# 2. Construir el assertions.yaml (resuelve rutas absolutas del sandbox)
python3 tests/evidence-hunter/build_assertions.py > /tmp/assertions.yaml

# 3. Correr el hunter (runner real: bin/evidence-hunter.py)
python3 bin/evidence-hunter.py /tmp/assertions.yaml > /tmp/evidence.json

# 4. Validar la salida contra los esperados
python3 tests/evidence-hunter/validate.py /tmp/evidence.json
```

## Optimización frente a mí (Critic)

- **Rigor de comparación** - el validate exige coincidencia exacta de `status` y match de `evidence` contra el patrón del caso. Dos columnas separadas (STATUS y CITA) en el reporte: un acierto de status con cita rota no es verde.
- **Reproducibilidad sin costo** - un solo comando crea la sandbox, la verifica (F10) y deja la trampa blindada; cero dependencias externas (solo `pathlib`, `shutil`, `sys`, `textwrap`); reaplicable cuantas veces se necesite sin intervención manual.

## Red Lines del laboratorio

- **No tocar el repo real** - todo vive bajo `tests/evidence-hunter/`.
- **No usar red** - `pip` o descargas están prohibidas durante el scaffold.
- **No asumir pytest real** - el Caso 5 debe poder declarar `bloqueado` sin que pytest exista en el PATH. El Caso 2 distingue entre `parcial` (pytest falla) y `bloqueado` (pytest ausente).
- **No saltarse `scaffold.py`** - su `main()` corre asserts de trampa que detectan si alguien añadió archivos que rompen el contrato.

## Referencias

- Skill bajo prueba: [`agents/kanam-critic/skills/evidence-hunter/SKILL.md`](../skills/evidence-hunter/SKILL.md).
- Rúbrica que valida: `.knowledge/SHARP.md`.
- Skill coordinada: [`agents/kanam-critic/skills/sharp-adversarial-review/SKILL.md`](../skills/sharp-adversarial-review/SKILL.md).
- Siguiente paso de la trofeo‑trayectoria: `sharp-score-oracle` (calibración histórica del propio veredicto SHARP).