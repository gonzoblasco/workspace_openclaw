---
name: "regression-net"
metadata:
  category: "Hermes SDD"
  tags:
    - tests
    - regresion
    - mutacion
    - pipeline-c
    - minimax
description: "Red de tests de regresion del Pipeline C: convierte cada finding de B en un test ejecutable y valida la suite por mutacion. Se dispara SOLO si B reporto findings o antes de deploy, nunca preventiva. Gate: toda mutacion sembrada debe ser detectada."
user-invocable: true
---

# Skill: regression-net - Pipeline C

> **Que hace:** convierte los findings del revisor B en tests que fallan si el bug vuelve.
> **Que NO hace:** no arregla el bug (eso es A), no revisa (eso es B), no opina de diseño.

## Trigger (y anti-trigger)

| Se dispara | NO se dispara |
|---|---|
| B reporto **al menos un finding** | no hubo review de B |
| Cierre de unidad antes de deploy | la unidad es documental (sin codigo) |
| A termino un rework que cerro findings | "por si acaso" / preventiva |

**La regla que define el rol:** *todo finding de B tiene que terminar como un test de C.*
Si un finding no se convirtio en test, se perdio dos veces - se midio el 2026-10-26: el rework
cubrio 7 de 9 findings y el que se escapo tampoco quedo como test.

## Input

1. Artefacto **corregido por A** (no el original)
2. Reporte de B con los findings (lista con severidad y evidencia)
3. El spec / criterios de aceptacion

## Modelo

`sessions_spawn(model: "ollama/minimax-m3.1-flash:cloud")`

MiniMax M3.1 Flash: 17/40 wins absolutos en la cata de 8 roles (2026-10-20), y es el titular del
slot C segun el router (`model-router.sh model pipeline_abc`).
**A ≠ B ≠ C obligatorio**: si C corre con el mismo modelo que A o B, no es una tercera red.

## Procedimiento

### 1. Un test por finding

Para cada finding del reporte de B, escribir **uno o mas tests** que:

- **Fallen contra el codigo original** (el que tenia el bug) - sin esto, el test no prueba nada
- **Pasen contra el codigo corregido**
- Tengan nombre que diga **que invariante** protegen, no "test_bug_3"

### 2. Tests de invariante, no de implementacion

El error clasico: testear *como* esta escrito el codigo. Si A refactoriza, el test rompe sin que
haya bug. Testear **la promesa**:

```python
# MAL: acoplado a la implementacion
assert cache._internal_list is not result

# BIEN: la promesa del docstring
result.append({"x": 1})
assert len(cache._internal_list) == 0, "devolver una copia, no la lista interna"
```

### 3. Gate de mutacion (obligatorio, no opcional)

Sembrar mutaciones deliberadas y verificar que la suite las caza:

| Mutacion | Debe detectarla |
|---|---|
| Invertir una comparacion (`<=` → `<`) | ✅ |
| Cambiar `return list(x)` → `return x` | ✅ |
| Invertir un signo en un calculo de edad/TTL | ✅ |
| Quitar una validacion de borde | ✅ |

**Si una mutacion sobrevive, la unidad NO se puede declarar `done`.**

```bash
# el seed_bugs.py del bench sirve tal cual como sembrador de mutaciones
python3 bench/seed_bugs.py <copia_del_artefacto>
pytest -q   # DEBE fallar. Si pasa, la red tiene un agujero.
```

### 4. Reporte

```markdown
## RED DE TESTS - <unidad>

| Finding de B | Test creado | Falla con el bug? | Pasa corregido? |
|---|---|---|---|
| BUG-1 per_page=0 no lanza | test_per_page_zero_raises | ✅ | ✅ |

## MUTACIONES
| Mutacion | Detectada |
|---|---|
| `<=` → `<` en filter_by_date | ✅ |
| `return list(data)` → `return data` | ✅ |

## SUITE FINAL
<paste de pytest -q>

## VEREDICTO
CERRADA (todas las mutaciones detectadas) | ABIERTA (N mutaciones sobreviven)
```

## Reglas duras

- **No corrige codigo de produccion.** Si un test falla, reporta a A; no parchea.
- **No borra tests de A.** Si un test de A miente (pasa aunque el codigo este mal), lo **reporta**;
  corregirlo es de A.
- **Un finding sin test = unidad abierta.** Sin excepciones.
- **No inventa cobertura.** Si el finding era inobservable (p.ej. timing), lo declara
  "no testeable con este harness" en vez de escribir un test que no prueba nada.

## Integracion con el tracker

```bash
scripts/pipeline-track.sh review U2      # B termino
# -> corre esta skill
scripts/pipeline-track.sh done U2        # solo si el gate de mutacion paso
```
