# Fixture de la cata 2026-11-16 (suite oculta versionada)

Comparación de 5 modelos cloud sobre 3 tareas, con dos tandas de razonamiento
(`low` y `off`). Este directorio es el activo reproducible: suite, evaluador,
referencia correcta y versiones defectuosas.

## Archivos

| Archivo | Qué es |
|---|---|
| `tasks.json` | Los 3 enunciados, verbatim, con su versión. |
| `evaluate.py` | El evaluador con los asserts ocultos + `--selftest`. |
| `reference/` | Soluciones correctas escritas a mano (deben dar PASS). |
| `defective/` | Versiones con defectos conocidos (deben dar FAIL). |
| `run_cata.py` | Runner: misma vía, nonce anti-cache, auto-escalado de `num_predict`. |
| `analyze.py` | Agregación por modelo/tanda y clasificación del modo de salida. |
| `probe.py`, `probe2.py` | Sondas de la perilla de razonamiento (la 1ra quedó invalidada por cache). |
| `work/` | Salidas crudas y thinking por celda. |
| `results.json` | Resultado por celda. |

## Uso

```bash
python3 evaluate.py --selftest          # valida en las dos direcciones
python3 run_cata.py                     # corre la cata (28 celdas)
python3 analyze.py                      # tabla agregada
```

## Cuándo revisar los asserts

- **T1**: si cambia la convención de tramos (inclusivo/exclusivo) o el tamaño máximo.
- **T2**: si cambia la regla de redondeo (hoy: un solo redondeo al total).
- **T3**: depende del CSV embebido en el enunciado; si se edita `tasks.json`, recalcular
  el total (235.74) y las filas excluidas (id 3 duplicado, fila EUR, fila fuera de Q3).

Si un assert se vuelve dudoso, se corrige el assert y se re-corre `--selftest`; **no** se
interpreta el fallo como defecto del modelo hasta que la referencia vuelva a dar PASS y la
defectuosa FAIL.
