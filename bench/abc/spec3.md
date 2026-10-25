# Caso 3 - `rate_limiter`

Módulo `ratelimit.py`, stdlib only, type hints y docstrings en funciones públicas.

## API
- `class TokenBucket`:
  - `__init__(self, capacity: float, refill_per_second: float, clock: Callable[[], float] = time.monotonic)`
  - `allow(self, cost: float = 1.0) -> bool` - consume `cost` tokens si hay; devuelve si se permitió.
  - `available(self) -> float` - tokens disponibles ahora.
  - `reset(self) -> None`

## Comportamiento requerido
1. Arranca **lleno**: `available() == capacity`.
2. `allow()` consume `cost` tokens y devuelve `True` si había suficientes; si no había, devuelve `False` y **no** consume nada.
3. Los tokens se recargan a `refill_per_second` tokens por segundo, de forma fraccionaria, según el reloj inyectado.
4. El refills se calculan con el reloj inyectado: **nunca** llamar `time.*` directamente.
5. `cost` mayor que `capacity` → `allow` devuelve `False` para siempre, sin excepción.
6. `cost <= 0` → `ValueError`.
7. **Reloj que retrocede**: si `clock()` devuelve un valor menor al último visto, el limitador NO debe crear tokens extra ni quedar en estado inconsistente.
8. `reset()` vuelve a llenar el bucket y reinicia el reloj interno.

## Criterios de aceptación
- Con `capacity=3`: tres `allow()` dan `True`, el cuarto `False`.
- Con `refill_per_second=1.0`: tras 1.0s de reloj, hay 1 token disponible.
- Con `refill_per_second=0.5`: tras 0.5s hay 0.5 token; `allow(cost=0.5)` da `True`.
- `cost=0` lanza `ValueError`; `cost=999` da `False` y no lanza.
- Tras `reset()`, `available() == capacity`.
