# Ground truth - bench head-to-head de revisores

> [!CAUTION]
> **Este archivo NO debe estar en el working directory de un agente revisor B.**
> Si lo ve, el benchmark deja de medir recall y pasa a medir lectura de_comentarios.

Artefacto: implementacion escrita por **A = `gpt-oss:120b-cloud`** a partir de
`bench/base/task_spec.md`. Luego se le sembraron 4 bugs con `bench/seed_bugs.py`.

Reproducir:

```bash
for b in b-deepseek b-beam b-minimax; do
  mkdir -p bench/$b
  cp bench/base/reports.py bench/base/test_reports.py bench/base/task_spec.md bench/$b/
  python3 bench/seed_bugs.py bench/$b
done
```

## Bugs sembrados (4)

| id | Donde | Que rompe | Severidad | Visible en los tests de A? |
|---|---|---|---|---|
| BUG-1 | `paginate` | `per_page <= 0` paso a `per_page < 0` -> `per_page=0` ya NO lanza `ValueError`. Viola el criterio "per_page invalido (0, negativo o no int) lanza ValueError" y ademas `items[start:0]` devuelve lista vacia en vez de error. | ALTO | **Si** - `test_invalid_per_page_raises` falla |
| BUG-2 | `filter_by_date` | `<= until_date` paso a `< until_date` -> el limite `until` es **exclusivo**. Viola el criterio "filter_by_date es inclusivo en since y en until". | ALTO | **Si** - `test_inclusive_bounds` y `test_datetime_inputs` fallan |
| BUG-3 | `cached_reports` | `age = (now - cached_at)` paso a `age = (cached_at - now)` -> la edad es siempre negativa -> `age <= ttl_seconds` siempre es True -> **el cache nunca expira**. Viola "cached_reports no devuelve un valor cacheado mas viejo que ttl_seconds". | CRITICO | **No** - los tests de A comparan datos iguales, asi que pasan igual |
| BUG-4 | `cached_reports` | `return list(data)` paso a `return data` -> se devuelve **la lista interna del cache**. Un caller que la mute la corrompe y el cache queda contaminado. Viola la promesa de "devolver una copia" del docstring. | MEDIO | **No** - ningun test muta el resultado |

## Debilidades de los tests de A (no son bugs sembrados, pero son findings reales)

- `test_cache_miss_after_ttl` **no verifica que haya habido un fetch nuevo**: compara
  `first == later` y como el FakeSession devuelve siempre los mismos datos, el test
  pasa aunque el cache nunca expire.
- `test_cache_hit_within_ttl` tampoco verifica que NO hubo fetch en el segundo call.
- `fetch_reports` no tiene test propio (el `AttributeError` por sesion sin `fetch`).
- No hay test de `per_page` no-int (el criterio lo menciona explicitamente).
- No hay test de `filter_by_date` con `since`/`until` como `datetime` mezclado con `date`.
- No hay test de `summarize` con `amount` ausente (solo con amount invalido tipo string).

## Metrica

- **Recall** = bugs sembrados encontrados / 4
- **Precision** = bugs reportados que estan en el ground truth / bugs reportados
- Los findings extra (debilidades de tests) se cuentan aparte: son validos si el B
  los reporta con evidencia ejecutable.

## Resultados medidos (2026-10-25, Ollama 0.40.11, Mac Mini)

| Revisor B | Recall | Bugs reportados | Hallazgos extra | Duracion | Veredicto |
|---|---|---|---|---|---|
| `deepseek-v4.1-flash:cloud` | **4/4** | 9 | si | 52s | RECHAZADO |
| `minimax-m3.1-flash:cloud` | **4/4** | 10 | si | 180s | RECHAZADO |
| `beam:cloud` | **3/4** | 3 | **no** | 17s | **APROBADO (incorrecto)** |

`beam` **no corrigio BUG-4** (sigue con `return data` en la linea del hit) y no lo
reporto. Su veredicto "APROBADO" fue incorrecto: el cache sigue contaminable.
El resto de los tres dejaron la suite verde sin relajar ningun assert original.

Verificacion del recall: `python3 bench/verify_recall.py`.
