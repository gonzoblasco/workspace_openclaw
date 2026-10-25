"""Reproduccion minima del bug: invalidate() sobre una clave VENCIDA.

La entrada murio por TTL. Spec 4: invalidate devuelve True solo si existia;
spec 6: solo las entradas vivas cuentan. Una clave vencida no existe, luego
invalidate debe devolver False.
Nota: no llamar len() antes, porque __len__ purga y enmascara el bug.
"""
from cache import ResilientCache


class C:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


clock = C()
cache = ResilientCache(ttl_seconds=5, max_entries=10, clock=clock)
cache.get_or_fetch("a", lambda: 1)
clock.t += 6  # 'a' vencio
result = cache.invalidate("a")
print("invalidate('a') sobre clave vencida =", result, "<- esperado False")
assert result is False, "BUG: clave vencida reportada como existente"
