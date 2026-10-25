# Caso 1 - `resilient_cache`

Módulo `cache.py`, stdlib only, type hints y docstrings en funciones públicas.

## API
- `class ResilientCache`:
  - `__init__(self, ttl_seconds: float, max_entries: int = 128, clock: Callable[[], float] = time.monotonic)`
  - `get_or_fetch(self, key: str, fetcher: Callable[[], T]) -> T`
  - `invalidate(self, key: str) -> bool`
  - `clear(self) -> None`
  - `__len__(self) -> int`

## Comportamiento requerido
1. `get_or_fetch` devuelve el valor cacheado si la entrada no venció.
2. Si venció o no existe, llama a `fetcher()`, guarda el resultado y lo devuelve.
3. El reloj es inyectable: **nunca** llamar a `time.time()` ni `time.monotonic()` dentro de la lógica; solo a través de `self._clock()`.
4. `invalidate(key)` borra la entrada y devuelve `True` si existía, `False` si no.
5. `clear()` vacía todo.
6. `len(cache)` es la cantidad de entradas vivas.
7. LRU: al superar `max_entries` se descarta la entrada menos recientemente usada.
8. **Reentrada**: si dos llamadas concurrentes piden la misma clave y ambas son miss, el `fetcher` se invoca **una sola vez** y ambas reciben el mismo resultado.
9. Una excepción en `fetcher` **no** deja la clave cacheada (ni un valor parcial), y el error se propaga.
10. Thread-safe.

## Criterios de aceptación
- Ninguna llamada a `time.*` fuera del `clock` inyectado (verificable por lectura).
- La reentrada produce 1 sola llamada al `fetcher` bajo concurrencia.
- Una excepción del `fetcher` no deja entrada en el caché.
- LRU: con `max_entries=2`, insertar 3 claves deja viva la más reciente y la segunda-más-reciente.
