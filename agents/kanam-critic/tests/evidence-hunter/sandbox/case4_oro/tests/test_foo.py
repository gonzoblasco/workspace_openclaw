import sys
import os
# Ensure the parent directory (containing foo.py) is on the import path.
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from foo import foo

def test_foo_returns_42():
    assert foo() == 42
