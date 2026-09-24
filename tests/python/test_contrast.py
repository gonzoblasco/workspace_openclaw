"""Tests for scripts/check-contrast.py - el guardia de contraste de kanam-os.

Por que existen: el contraste de la app se reviso a mano UNA vez (2026-09-24,
tras el reporte de Gonzo "quedo muy oscuro"). Una revision manual no protege
nada, y ademas la auditoria de ese dia estaba ROTA: comparaba claves con `--`
contra claves sin `--`, asi que nunca encontraba un par y reportaba "0 fallas".

El test central es `test_detecta_la_paleta_vieja`: prueba que el chequeo PUEDE
fallar. Un check que no puede fallar no verifica nada.
"""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
CSS = ROOT / "projects" / "kanam-os" / "app" / "globals.css"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cc():
    return load("check_contrast", "scripts/check-contrast.py")


# --- la matematica de WCAG ---

def test_contraste_blanco_negro_es_21():
    m = cc()
    assert round(m.contrast("#ffffff", "#000000"), 0) == 21


def test_contraste_identico_es_1():
    m = cc()
    assert m.contrast("#4ade80", "#4ade80") == 1.0


def test_contraste_es_simetrico():
    m = cc()
    assert m.contrast("#101614", "#e6ece9") == m.contrast("#e6ece9", "#101614")


# --- el chequeo contra el CSS real ---

def test_paleta_actual_pasa():
    """La paleta de kanam-os cumple WCAG AA en los pares declarados."""
    m = cc()
    assert m.check(CSS) == 0


def test_detecta_la_paleta_vieja(tmp_path):
    """CRITICO: el chequeo tiene que FALLAR con la paleta que tenia fallas.

    La version vieja tenia el borde de control en #24302d: 1.31:1 sobre panel,
    cuando WCAG 1.4.11 pide 3:1 para el limite de un componente de UI. Si este
    test pasara, el check seria ciego (que fue exactamente el bug de la
    auditoria manual del 2026-09-24).
    """
    css = CSS.read_text(encoding="utf-8")
    viejo = css.replace("--border-control: #66766f;", "--border-control: #24302d;")
    assert viejo != css, "no se pudo construir la paleta vieja"
    f = tmp_path / "viejo.css"
    f.write_text(viejo, encoding="utf-8")
    m = cc()
    assert m.check(f) == 1, "el check NO detecto el borde de control por debajo de 3:1"


def test_detecta_falta_de_foco_visible(tmp_path):
    """Quitar las reglas de foco debe fallar 2.4.7.

    El reemplazo tiene que ELIMINAR el token, no contenerlo: renombrar
    `focus-visible` a `focus-visible-x` dejaba el substring intacto y el check
    seguia viendolo (el mismo error de verificacion ciega que este archivo
    previene). Se reemplaza la palabra completa por un token distinto.
    """
    css = CSS.read_text(encoding="utf-8")
    sin_foco = css.replace("focus-visible", "focus").replace(":focus {", ":nada {")
    assert "focus-visible" not in sin_foco, "el reemplazo no elimino el token"
    f = tmp_path / "sinfoco.css"
    f.write_text(sin_foco, encoding="utf-8")
    m = cc()
    assert m.check(f) == 1, "el check NO detecto la ausencia de indicador de foco"


def test_detecta_texto_ilegible(tmp_path):
    css = CSS.read_text(encoding="utf-8")
    malo = css.replace("--muted: #93a29d;", "--muted: #2a3330;")
    f = tmp_path / "malo.css"
    f.write_text(malo, encoding="utf-8")
    m = cc()
    assert m.check(f) == 1, "el check NO detecto texto muted ilegible"


def test_falla_si_no_hay_root(tmp_path):
    f = tmp_path / "vacio.css"
    f.write_text("body { color: red; }\n", encoding="utf-8")
    m = cc()
    try:
        m.check(f)
        raise AssertionError("deberia fallar sin bloque :root")
    except SystemExit:
        pass


# --- la propiedad que une el check con el CSS real ---

def test_variables_esperadas_existen():
    """El check depende de estas variables: si desaparecen, es un error."""
    m = cc()
    V = m.read_vars(CSS.read_text(encoding="utf-8"))
    for nombre in ("bg", "panel", "panel-2", "border-control", "text", "muted", "accent"):
        assert nombre in V, f"falta --{nombre} en :root"


def test_no_hay_outline_none_sin_reemplazo():
    """`outline: none` sin :focus-visible deja el teclado a ciegas (2.4.7)."""
    css = CSS.read_text(encoding="utf-8")
    assert "focus-visible" in css, "no hay indicador de foco"
