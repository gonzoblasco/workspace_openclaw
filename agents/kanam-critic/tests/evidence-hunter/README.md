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
| 5 | El Bloqueado | "La cobertura de tests es > 80 %" | `coverage` | `bloqueado` | `PATH` / `venv` / `no se puede medir` |
| 6 | El Token Malinterpretado | "El kit usa el token de diseño `kana-critical`" | extracción de token + `rg` | `auto-reportado` | `kana-critical` o `no aparece` |
| 7 | Horizon — Ciclo Invisible | "No hay imports circulares entre los modulos del paquete `pkg`" | `ast`: grafo de imports + DFS | `auto-reportado` | `.py:linea … ciclo` |
| 8 | Resistance — Solo Camino Feliz | "Los casos borde estan cubiertos" | patrones declarativos de borde | `auto-reportado` | `camino feliz` / `sin casos borde` |
| 9 | Resistance — Borde Real | "Los casos borde estan cubiertos" | patrones declarativos de borde | `verificado` | `test_*.py:linea` |
| 10 | Horizon — Paquete Limpio | "No hay imports circulares entre los modulos del paquete `pkg`" | `ast`: grafo de imports + DFS | `verificado` | `.py:linea … sin ciclos` |
| 11 | Horizon — Ciclo por Imports Absolutos | "No hay imports circulares entre los modulos del paquete `pkg`" | `ast`: grafo de imports + DFS | `auto-reportado` | `.py:linea … ciclo` |
| 12 | Horizon — Absolutos Limpio | "No hay imports circulares entre los modulos del paquete `pkg`" | `ast`: grafo de imports + DFS | `verificado` | `.py:linea … sin ciclos` |

> **Caso 2 - trampa calibrada:** si pytest no está en el PATH, el hunter cae legítimamente a `bloqueado`. `validate.py` lo reporta distinto al FAIL simple (`BLOCKED-NOT-PARTIAL`). Esto evita falso verde y falso rojo.

> **Casos 7–10 (T4.2) — pares trampa/contraparte.** Cada detector nuevo entra con
> **un caso que lo falsifica** y **un caso que prueba que mide algo**:
> - Horizon: el caso 7 tiene un ciclo real `alpha -> beta -> alpha` que un `grep import`
>   no ve (cada línea suelta parece inocente). El caso 10 repite la misma afirmación
>   sobre un grafo acíclico y debe dar `verificado`. Sin el caso 10, un detector que
>   devolviera siempre `auto-reportado` pasaría la trampa sin medir nada.
> - Horizon absolutos (T4.2‑r2): el caso 11 es el mismo ciclo escrito con imports
>   absolutos (`from pkg import beta`) y `source` apuntando al **directorio** del
>   caso, no al paquete. El detector sólo resolvía relativos y devolvía
>   "modulo sin imports internos" sobre un paquete con ciclo: falso verde. El caso
>   12 es su contraparte acíclica. Además, un import no resoluble ya no se cuenta
>   como "sin imports": el `evidence` declara `N externos/no resueltos`, y si
>   **todos** los imports quedan sin resolver el estado es `bloqueado` (un grafo
>   vacío no prueba ausencia de ciclos).
> - Resistance: el caso 8 tiene un solo test de camino feliz. El caso 9 tiene
>   `pytest.raises` + `parametrize` (dos patrones distintos) y debe dar `verificado`.
>   Misma lógica: la contraparte es lo que impide el detector de un solo estado.

> **Colección de pytest.** `tests/pytest.ini` excluye `sandbox/` del *recursado*
> (`norecursedirs`): los fixtures repiten basenames (`test_foo.py`) y uno está roto
> a propósito (Caso 2). `norecursedirs` no bloquea archivos pasados explícitamente,
> así que el hunter sigue corriendo `pytest <archivo>` sobre cada caso.

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