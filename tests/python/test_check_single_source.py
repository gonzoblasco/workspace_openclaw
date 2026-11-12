"""Tests de scripts/check-single-source.py (2026-11-12).

Este gate corre en CADA commit y no tenía un solo caso de test: si dejara de
detectar una segunda copia, nada lo diría. Estos tests lo prueban contra un
árbol temporal con archivos normativos controlados.

Lo que cubren:
  1. Una línea idéntica en dos archivos normativos se detecta como duplicado.
  2. Una línea distinta no.
  3. Un título markdown repetido NO cuenta (ALLOW): es el nombre, no la regla.
  4. Las líneas cortas (< MIN_CHARS) no cuentan: son rótulos.
  5. Un tag de modelo escrito a mano fuera de MANAGED se detecta.
  6. Sin archivos normativos, el gate devuelve 3 y no 0.
"""
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'scripts' / 'check-single-source.py'

spec = importlib.util.spec_from_file_location('css', SCRIPT)
css = importlib.util.module_from_spec(spec)
spec.loader.exec_module(css)


REGLON = ('Nunca se corre un comando destructivo sin preguntar antes, '
          'y siempre se prefiere trash antes que rm.')


def write_tree(tmp_path, files):
    for rel, text in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')


def test_detecta_linea_duplicada(tmp_path):
    write_tree(tmp_path, {
        'AGENTS.md': f'# Reglas\n\n{REGLON}\n',
        'MEMORY.md': f'# Estado\n\n{REGLON}\n',
    })
    dups = css.find_duplicates(tmp_path)
    assert len(dups) == 1
    fa, na, fb, nb, score, sa, sb = dups[0]
    assert {fa, fb} == {'AGENTS.md', 'MEMORY.md'}
    assert score >= css.THRESHOLD


def test_no_detecta_lineas_distintas(tmp_path):
    write_tree(tmp_path, {
        'AGENTS.md': f'# Reglas\n\n{REGLON}\n',
        'MEMORY.md': '# Estado\n\nLos gates del pre-commit tardan dos segundos y '
                     'corren en cada commit del repositorio.\n',
    })
    assert css.find_duplicates(tmp_path) == []


def test_titulo_repetido_no_cuenta(tmp_path):
    write_tree(tmp_path, {
        'AGENTS.md': '# Las mismas reglas\n\n## La sección de verificación obligatoria\n',
        'MEMORY.md': '# Otro\n\n## La sección de verificación obligatoria\n',
    })
    assert css.find_duplicates(tmp_path) == []


def test_linea_corta_no_cuenta(tmp_path):
    write_tree(tmp_path, {
        'AGENTS.md': '# Reglas\n\nNo correr rm.\n',
        'MEMORY.md': '# Estado\n\nNo correr rm.\n',
    })
    assert css.find_duplicates(tmp_path) == []


def test_detecta_modelo_a_mano(tmp_path):
    # MODEL_TAG exige el tag entre backticks y con la forma `modelo:cloud`
    write_tree(tmp_path, {
        'AGENTS.md': '# Reglas\n\nEl primario de este agente es '
                     '`deepseek-v4.1-flash:cloud` y corre en la Mac Mini.\n',
    })
    # sin bloque MANAGED, el tag de modelo está a mano
    stray = css.find_stray_models(tmp_path)
    assert stray, 'un tag de modelo fuera de MANAGED tiene que detectarse'


def test_modelo_dentro_de_managed_no_cuenta(tmp_path):
    write_tree(tmp_path, {
        'AGENTS.md': '# Reglas\n\n<!-- BEGIN MANAGED:sintetico -->\n'
                     'El primario es `deepseek-v4.1-flash:cloud`.\n'
                     '<!-- END MANAGED:sintetico -->\n',
    })
    assert css.find_stray_models(tmp_path) == []


def test_sin_normativos_devuelve_3(tmp_path):
    rc = css.main([str(tmp_path)])
    assert rc == 3


def test_arbol_real_no_tiene_duplicados():
    """Contra el repo real: hoy no hay segundas copias. Si aparece una, este test avisa."""
    assert css.find_duplicates(ROOT) == []
