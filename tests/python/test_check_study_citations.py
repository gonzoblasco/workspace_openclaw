"""Tests de scripts/check-study-citations.py (promovido el 2026-11-12).

Cubren los tres modos de error que el gate encontró durante la cursada, más los
casos que hoy NO debe dar verde (código 3) y el arreglo por tabla de offsets.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'scripts' / 'check-study-citations.py'

spec = importlib.util.spec_from_file_location('csc', SCRIPT)
csc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(csc)


TRANSCRIPT = """\
[0:00:00] This course from Harvard University explores the concepts and algorithms
[0:06:04] Where you're trying to slide the tiles in order to make sure all the numbers
[0:06:20] But there are similar problems that you can frame in other ways.
"""


def run_cli(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                          capture_output=True, text=True)


@pytest.fixture
def class_dir(tmp_path):
    d = tmp_path / 'clase'
    d.mkdir()
    (d / 'transcripcion.md').write_text(TRANSCRIPT, encoding='utf-8')
    return d


def test_cita_correcta_pasa(class_dir):
    (class_dir / 'outline.md').write_text(
        'Texto: "But there are similar problems that you can frame" (0:06:20)\n',
        encoding='utf-8')
    r = run_cli(class_dir)
    assert r.returncode == 0, r.stdout + r.stderr
    assert 'PASA' in r.stdout


def test_cita_parafraseada_falla(class_dir):
    (class_dir / 'outline.md').write_text(
        'Texto: "pero hay problemas parecidos que podes enmarcar" (0:06:20)\n',
        encoding='utf-8')
    r = run_cli(class_dir)
    assert r.returncode == 1
    assert 'cita no encontrada' in r.stdout


def test_timestamp_corrido_falla(class_dir):
    (class_dir / 'outline.md').write_text(
        'Texto: "But there are similar problems that you can frame" (0:06:04)\n',
        encoding='utf-8')
    r = run_cli(class_dir)
    assert r.returncode == 1
    assert 'timestamp fuera de su bloque' in r.stdout


def test_cita_que_cruza_bloques_usa_el_inicio(class_dir):
    # cita que empieza en 0:06:04 y termina en el bloque siguiente
    (class_dir / 'outline.md').write_text(
        'Texto: "all the numbers [0:06:20] But there are similar problems" (0:06:04)\n',
        encoding='utf-8')
    # la cita no existe literal: el `[0:06:20]` está en medio
    r = run_cli(class_dir)
    assert r.returncode == 1


def test_fix_corrige_por_tabla_de_offsets(class_dir):
    outline = class_dir / 'outline.md'
    outline.write_text(
        'Texto: "But there are similar problems that you can frame" (0:06:04)\n',
        encoding='utf-8')
    r = run_cli(class_dir, '--fix')
    assert r.returncode == 0, r.stdout + r.stderr
    assert '(0:06:20)' in outline.read_text(encoding='utf-8')


def test_sin_citas_es_no_corrible(class_dir):
    (class_dir / 'outline.md').write_text('Sin citas acá.\n', encoding='utf-8')
    r = run_cli(class_dir)
    assert r.returncode == 3


def test_sin_transcripcion_es_no_corrible(tmp_path):
    d = tmp_path / 'clase'
    d.mkdir()
    (d / 'outline.md').write_text('"algo largo aqui" (0:00:01)\n', encoding='utf-8')
    r = run_cli(d)
    assert r.returncode == 3


def test_index_usa_texto_sin_timestamps():
    """El offset no cuenta el `[h:mm:ss]` del bloque: si contara, adelanta un cue."""
    cues = csc.parse_cues(TRANSCRIPT)
    index = csc.build_index(cues)
    joined = csc.normalize(' '.join(csc.strip_cue(l) for _, _, l in cues))
    pos = joined.find(csc.normalize('But there are similar problems'))
    found = csc.locate(index, pos)
    assert found[1] == '0:06:20'
