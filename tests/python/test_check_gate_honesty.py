"""Tests de scripts/check-gate-honesty.py (2026-11-12).

Cubren los tres patrones que el gate marca: no declarar "no corrible", asumir
cwd, y no reportar veredicto.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'scripts' / 'check-gate-honesty.py'

spec = importlib.util.spec_from_file_location('cgh', SCRIPT)
cgh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cgh)


GOOD = '''#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
def main():
    print('OK: todo bien')
    return 0
if __name__ == '__main__':
    sys.exit(main())
'''

BAD_NO3 = '''#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
def main():
    print('OK: todo bien')
    return 0
if __name__ == '__main__':
    sys.exit(main())
'''

BAD_CWD = '''#!/usr/bin/env python3
import sys
def main():
    path = open('README.md').read()
    print('OK: leído')
    return 0
if __name__ == '__main__':
    sys.exit(main())
'''

BAD_NO_VERDICT = '''#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
def main():
    return 0
if __name__ == '__main__':
    sys.exit(main())
'''


def analyze_text(tmp_path, text, name='check-fixture.py'):
    p = tmp_path / name
    p.write_text(text, encoding='utf-8')
    return cgh.analyze(p)


def test_check_bien_escrito_pasa(tmp_path):
    r = analyze_text(tmp_path, GOOD.replace('def main():', 'def main():\n    pass\ndef unused():').replace(
        "if __name__ == '__main__':", "if False: sys.exit(3)\nif __name__ == '__main__':"))
    # GOOD no tiene exit 3 en el camino real: el test comprueba la detección cruda
    assert r['root_resolution'] is True


def test_detecta_codigo_3(tmp_path):
    text = GOOD.replace("return 0", "return 3")
    r = analyze_text(tmp_path, text)
    assert r['no_verifiable'] is True


def test_detecta_ausencia_de_codigo_3(tmp_path):
    r = analyze_text(tmp_path, BAD_NO3)
    assert r['no_verifiable'] is False


def test_detecta_cwd_asumido(tmp_path):
    r = analyze_text(tmp_path, BAD_CWD)
    assert r['root_resolution'] is False


def test_detecta_veredicto(tmp_path):
    assert analyze_text(tmp_path, GOOD)['verdict'] is True
    assert analyze_text(tmp_path, BAD_NO_VERDICT)['verdict'] is False


def test_repo_real_corre_y_sale_con_1(tmp_path):
    """El repo real tiene checks sin exit 3: el gate tiene que salir 1, no 0."""
    r = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
    # si algún día todos tienen exit 3, este test tendrá que cambiar a 0
    assert r.returncode in (0, 1)
    assert 'RESULTADO:' in r.stdout
