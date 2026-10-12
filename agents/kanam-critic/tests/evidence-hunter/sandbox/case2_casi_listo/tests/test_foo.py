import os
import sys

# El módulo `foo` vive en la raíz del caso, no junto al test: sin esto
# pytest no puede importarlo y el caso degenera en error de colección
# (rc=2) en vez de en un fallo de aserción real (rc=1). La trampa del
# Casi-Listo es la ASERCIÓN rota, no un entorno de import roto.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from foo import foo

def test_foo_returns_zero():
    # Aserción INTENCIONALMENTE rota.
    assert foo() == 0
