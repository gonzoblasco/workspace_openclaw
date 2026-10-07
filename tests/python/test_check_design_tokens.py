"""Tests para scripts/check-design-tokens.py - el guardia de contraste del design system.

Por que existen: el principio no negociable #1 del design system ("contraste
verificado, no sentido") era FALSO - ninguna herramienta medía el contraste de los
tokens, y las matrices `$contrast` eran numeros escritos a mano nunca verificados.
Un guardia que no puede fallar no verifica nada (leccion de check-contrast.py).

Los tests cubren:
  - la matematica de contraste (valores WCAG conocidos);
  - que el guardia DETECTA un par roto (se siembra el defecto en un contexto falso);
  - que los bordes DECORATIVOS no son falso positivo (no se exigen);
  - que el sistema real pasa.
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CHECKER = ROOT / "scripts" / "check-design-tokens.py"


def load():
    spec = importlib.util.spec_from_file_location("check_design_tokens", CHECKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- matematica de contraste: valores WCAG conocidos ---

def test_contrast_white_on_black_is_21():
    mod = load()
    assert abs(mod.contrast("#FFFFFF", "#000000") - 21.0) < 0.01


def test_contrast_same_color_is_1():
    mod = load()
    assert abs(mod.contrast("#123456", "#123456") - 1.0) < 0.01


def test_contrast_known_teal():
    # #0d9488 sobre blanco: 3.74 (el valor real del bug: fallaba 4.5 como texto).
    mod = load()
    assert abs(mod.contrast("#0d9488", "#FFFFFF") - 3.74) < 0.05


# --- el guardia PUEDE fallar (se siembra el defecto) ---

def test_flags_a_broken_text_pair():
    mod = load()
    # Un tema fabricado con texto muted ilegible sobre blanco (dict aplanado,
    # como lo entrega theme_contexts).
    sem = {"text.muted": "#cccccc", "surface.base": "#FFFFFF"}
    failures, _, _ = mod.check_theme("fake", {}, sem, {})
    assert any(f[0] == "text.muted" for f in failures), failures


def test_passes_a_good_pair():
    mod = load()
    sem = {"text.muted": "#555555", "surface.base": "#FFFFFF"}
    failures, _, _ = mod.check_theme("fake", {}, sem, {})
    assert failures == []


# --- los bordes decorativos NO se exigen (evita falso positivo) ---

def test_decorative_border_is_not_in_the_required_pairs():
    mod = load()
    required = {p[0] for p in mod.TEXT_PAIRS + mod.GRAPHIC_PAIRS}
    assert "border.subtle" not in required
    assert "border.base" not in required
    # border.strong SI (puede delimitar un componente).
    assert "border.strong" in required


# --- el sistema real pasa (tras la correccion 2026-10-06) ---

def test_real_system_passes():
    mod = load()
    for name, prim, sem0, tover in mod.theme_contexts():
        failures, _, _ = mod.check_theme(name, prim, sem0, tover)
        assert failures == [], (name, failures)


# --- la matriz declarada existe y tiene numeros, no prosa vacia ---

def test_dark_theme_exists_and_passes():
    """El tema oscuro (agregado 2026-10-06 para migrar kanam-os) existe y cumple."""
    mod = load()
    names = [n for n, *_ in mod.theme_contexts()]
    assert "dark" in names, names
    for name, prim, sem0, tover in mod.theme_contexts():
        if name == "dark":
            failures, _, _ = mod.check_theme(name, prim, sem0, tover)
            assert failures == [], failures


def test_base_declares_contrast():
    data = json.loads((ROOT / "design" / "tokens" / "kanam.tokens.json").read_text(encoding="utf-8"))
    assert "$contrast" in data, "el sistema base debe declarar su matriz (antes no lo hacia)"
    assert len(data["$contrast"]) >= 4
