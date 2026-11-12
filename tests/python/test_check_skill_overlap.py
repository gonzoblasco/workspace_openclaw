"""Tests de scripts/check-skill-overlap.py (2026-11-12).

Lo que se prueba no es la detección de overlap (necesita Ollama): es que el
caché de embeddings y la normalización por pares no cambien el resultado, y que
el check NO dé verde cuando no puede correr.
"""
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'scripts' / 'check-skill-overlap.py'

spec = importlib.util.spec_from_file_location('cso', SCRIPT)
cso = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cso)


def make_items():
    def it(name):
        return {'name': name, 'description': 'x' * 5}
    return [
        (it('a'), [1.0, 0.0, 0.0]),
        (it('b'), [1.0, 0.0, 0.0]),      # idéntico a 'a'
        (it('c'), [0.0, 1.0, 0.0]),      # ortogonal a 'a' y 'b'
    ]


def test_cosine_pairs_encuentra_el_par_identico():
    pairs = cso.cosine_pairs(make_items(), 0.9)
    assert len(pairs) == 1
    sim, a, b = pairs[0]
    assert {a, b} == {'a', 'b'}
    assert abs(sim - 1.0) < 1e-12


def test_cosine_pairs_ignora_vectores_vacios():
    items = [(i, v) for i, v in make_items()]
    items.append(({'name': 'vacio', 'description': ''}, []))
    pairs = cso.cosine_pairs(items, 0.9)
    assert all('vacio' not in (a, b) for _, a, b in pairs)


def test_cosine_legacy_coincide_con_pairs():
    """La función vieja y la nueva tienen que dar lo mismo: el refactor no cambia semántica."""
    items = make_items()
    a, b = items[0], items[1]
    legacy = cso.cosine(a[1], b[1])
    nuevo = cso.cosine_pairs([a, b], 0.0)[0][0]
    assert abs(legacy - nuevo) < 1e-12


def test_text_key_estable():
    assert cso.text_key('hola') == cso.text_key('hola')
    assert cso.text_key('hola') != cso.text_key('hola2')


def test_text_key_ignora_lo_que_embed_trunca():
    """embed() usa text[:500]: el hash tiene que cubrir exactamente eso."""
    base = 'x' * 500
    assert cso.text_key(base + 'A') == cso.text_key(base + 'B')


def test_cache_roundtrip(tmp_path, monkeypatch):
    cache = tmp_path / 'cache.json'
    monkeypatch.setenv('OPENCLAW_SKILL_OVERLAP_CACHE', str(cache))
    cso.CACHE_PATH = str(cache)
    cso.save_cache({'k': [1.0, 2.0]})
    assert cso.load_cache() == {'k': [1.0, 2.0]}


def test_cache_de_otro_modelo_se_descarta(tmp_path, monkeypatch):
    cache = tmp_path / 'cache.json'
    monkeypatch.setenv('OPENCLAW_SKILL_OVERLAP_CACHE', str(cache))
    cso.CACHE_PATH = str(cache)
    cache.write_text('{"model": "otro-modelo", "vectors": {"k": [1.0]}}', encoding='utf-8')
    assert cso.load_cache() == {}


def test_sin_catalogo_es_no_corrible(monkeypatch):
    """Si el runtime no responde, el check NO puede dar verde."""
    monkeypatch.setattr(cso, 'load_catalog', lambda: None)
    rc = cso.main([])
    assert rc == 3


def test_catalogo_chico_es_no_corrible(monkeypatch):
    monkeypatch.setattr(cso, 'load_catalog', lambda: [{'name': 'solo', 'description': 'x'}])
    rc = cso.main([])
    assert rc == 3
