"""Tests de scripts/check-handoff-merge.py (2026-11-12).

El gate existe porque una sesión pisó 8 pendientes de otra al regenerar el
HANDOFF. No tenía tests: si dejara de detectar la pérdida, nada lo diría.

Cubren:
  1. Un pendiente que desaparece sin declararse -> falla (exit 1).
  2. El mismo pendiente en el bloque CERRADOS -> pasa.
  3. --closed con el texto del item -> pasa.
  4. Un HANDOFF nuevo que agrega items no falla.
  5. Sin archivos, error de uso (2), no verde.

GOTCHA del fixture: el gate matchea el título de sección por SUBSTRING y ya
lowercased. "Próximos pasos" con tilde NO contiene "proximo", así que la sección
se saltea en silencio y el test pasa por la razón equivocada. Las fixtures usan
"Proximos pasos" sin tilde. Es una limitación del gate, no del test: un HANDOFF
con títulos acentuados puede quedar fuera del chequeo de pendientes. Cazado
escribiendo estos tests (2026-11-12).
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'scripts' / 'check-handoff-merge.py'

PREV = """# HANDOFF - workspace

## Proximos pasos

- Promover el gate de citas a scripts/check-study-citations.py
- Arreglar las dos clases que fallan el gate de citas

## Decisiones

- El curso se toma como fundamento, no como skill nueva
"""

NEW_WITHOUT = """# HANDOFF - workspace

## Proximos pasos

- Arreglar las dos clases que fallan el gate de citas

## Decisiones

- El curso se toma como fundamento, no como skill nueva
"""

NEW_WITH_CLOSED = """# HANDOFF - workspace

## Proximos pasos

- Arreglar las dos clases que fallan el gate de citas

## CERRADOS

- Promover el gate de citas a scripts/check-study-citations.py

## Decisiones

- El curso se toma como fundamento, no como skill nueva
"""


def run(tmp_path, new_text, prev_text=PREV, *extra):
    prev = tmp_path / 'prev.md'
    new = tmp_path / 'new.md'
    prev.write_text(prev_text, encoding='utf-8')
    new.write_text(new_text, encoding='utf-8')
    return subprocess.run(
        [sys.executable, str(SCRIPT), '--new', str(new), '--prev', str(prev), *extra],
        capture_output=True, text=True)


def test_pendiente_perdido_falla(tmp_path):
    # El gate compara coverage: una palabra del item viejo que sigue en el nuevo
    # alcanza para "conservado". Para probar la pérdida, el item tiene que
    # desaparecer ENTERO, no sólo acortarse.
    prev = PREV.replace(
        '- Arreglar las dos clases que fallan el gate de citas',
        '- Verificar el portal de IAAP antes de la fecha de cierre')
    r = run(tmp_path, NEW_WITHOUT, prev)
    assert r.returncode == 1
    out = (r.stdout + r.stderr).lower()
    assert 'promover' in out


def test_pendiente_declarado_en_cerrados_pasa(tmp_path):
    r = run(tmp_path, NEW_WITH_CLOSED)
    assert r.returncode == 0, r.stdout + r.stderr


def test_closed_por_flag_pasa(tmp_path):
    r = run(tmp_path, NEW_WITHOUT, PREV, '--closed',
            'Promover el gate de citas a scripts/check-study-citations.py')
    assert r.returncode == 0, r.stdout + r.stderr


def test_handoff_que_agrega_no_falla(tmp_path):
    extra = NEW_WITH_CLOSED.replace(
        '## Decisiones', '- Un pendiente nuevo que la sesión agregó\n\n## Decisiones')
    r = run(tmp_path, extra)
    assert r.returncode == 0, r.stdout + r.stderr


def test_sin_archivos_es_error_de_uso(tmp_path):
    # Sin --new el gate cae al default `.knowledge/HANDOFF.md`; si no existe,
    # tiene que fallar (2 o 3), nunca devolver verde.
    r = subprocess.run([sys.executable, str(SCRIPT), '--new', 'no-existe.md'],
                       capture_output=True, text=True, cwd=str(tmp_path))
    assert r.returncode != 0
