import os
import sys

# `foo` vive en la raíz del caso: se agrega al path para que el test
# corra de verdad. El Oro tiene que PASAR (rc=0), no fallar por import.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from foo import foo

def test_foo_returns_42():
    assert foo() == 42
