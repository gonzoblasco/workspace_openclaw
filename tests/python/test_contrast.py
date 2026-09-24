"""Tests for scripts/check-contrast.py - el guardia de contraste de kanam-os.

Por que existen: el contraste de la app se reviso a mano UNA vez (2026-09-24,
tras el reporte de Gonzo "quedo muy oscuro"). Una revision manual no protege
nada, y ademas la auditoria de ese dia estaba ROTA: comparaba claves con `--`
contra claves sin `--`, asi que nunca encontraba un par y reportaba "0 fallas".

El test central es `test_detecta_la_paleta_vieja`: prueba que el chequeo PUEDE
fallar. Un check que no puede fallar no verifica nada.
"""
import importlib.util
import re
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


def set_var(css, nombre, valor):
    """Cambia el valor de una variable de :root por NOMBRE, no por valor viejo.

    Atar el test a un hex concreto lo vuelve fragil: al iluminar la paleta dos
    tests empezaron a fallar no porque la logica se rompiera, sino porque el
    literal que buscaban ya no existia. Buscar por nombre mantiene el test
    valido para cualquier paleta.
    """
    nuevo, n = re.subn(
        rf"(--{nombre}:\s*)#[0-9a-fA-F]{{6}}", rf"\g<1>{valor}", css
    )
    assert n == 1, f"no se encontro --{nombre} en :root ({n} matches)"
    return nuevo


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


def test_detecta_la_paleta_vieja(tmp_path):
    """CRITICO: el chequeo tiene que FALLAR con un borde de control ilegible.

    El borde de un control necesita 3:1 (WCAG 1.4.11). Si este test pasara, el
    check seria ciego, que fue exactamente el bug de la auditoria manual del
    2026-09-24. Se busca por NOMBRE de variable, no por el hex viejo: atarlo a
    un literal hacia que el test se rompiera al cambiar la paleta.
    """
    css = CSS.read_text(encoding="utf-8")
    viejo = set_var(css, "border-control", "#24302d")
    f = tmp_path / "viejo.css"
    f.write_text(viejo, encoding="utf-8")
    m = cc()
    assert m.check(f) == 1, "el check NO detecto el borde de control por debajo de 3:1"


def test_detecta_texto_ilegible(tmp_path):
    css = CSS.read_text(encoding="utf-8")
    malo = set_var(css, "muted", "#2a3330")
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


# --- colores hardcodeados fuera de :root ---
# El guardia original solo leia :root, y asi se le escaparon tres colores con
# falla real, dos de ellos en CONTROLES (.btn-warn, .chip-clear). Escribir un
# hex a mano esquiva una validacion que solo mira las variables.

def test_encuentra_hardcodeados():
    m = cc()
    hard = m.find_hardcoded(CSS.read_text(encoding="utf-8"))
    assert hard, "no encontro ningun hex hardcodeado (hay 6 reales)"
    props = {p for _, p, _ in hard}
    assert "color" in props and "border-color" in props


def test_detecta_borde_hardcodeado_ilegible(tmp_path):
    """CRITICO: .btn-warn y .chip-clear son CONTROLES con hex a mano.

    Tenian #5c4715: 1.24:1 sobre panel-2 cuando 1.4.11 pide 3:1. El guardia
    original no lo veia porque solo leia :root.
    """
    css = CSS.read_text(encoding="utf-8")
    viejo = css.replace("border-color: #ad922d;", "border-color: #5c4715;")
    assert viejo != css, "no se pudo construir el caso"
    f = tmp_path / "hard.css"
    f.write_text(viejo, encoding="utf-8")
    m = cc()
    assert m.check(f) == 1, "el guardia NO detecto el control con borde ilegible"


def test_detecta_texto_hardcodeado_ilegible(tmp_path):
    css = CSS.read_text(encoding="utf-8")
    viejo = css.replace("color: #cba0fc;", "color: #c084fc;")
    f = tmp_path / "txt.css"
    f.write_text(viejo, encoding="utf-8")
    m = cc()
    assert m.check(f) == 1, "el guardia NO detecto el texto violeta por debajo de AA"


def test_hardcodeados_actuales_pasan():
    """Los 6 hex actuales cumplen su umbral."""
    m = cc()
    V = m.read_vars(CSS.read_text(encoding="utf-8"))
    for sel, prop, val in m.find_hardcoded(CSS.read_text(encoding="utf-8")):
        umbral = 4.5 if prop == "color" else 3.0
        peor = min(m.contrast(val, V[s]) for s in m.SURFACES)
        assert peor >= umbral, f"{sel} {prop} {val}: {peor:.2f} < {umbral}"


def test_la_paleta_nueva_es_mas_clara_que_la_vieja():
    """El reporte fue 'demasiado oscuro': la correccion tiene que iluminar.

    Gonzo lo reporto DOS veces. El primer intento subio bg de L* 4.0 a 6.6 y
    volvio a ser 'demasiado oscuro': 2.6 puntos no se perciben. Este test fija
    que el fondo este en el rango de un tema oscuro real (L* >= 12), no en
    negro casi puro.
    """
    m = cc()
    V = m.read_vars(CSS.read_text(encoding="utf-8"))

    def lstar(h):
        v = m.luminance(h)
        return 116 * (v ** (1 / 3)) - 16 if v > 0.008856 else 903.3 * v

    for superficie in ("bg", "panel", "panel-2"):
        L = lstar(V[superficie])
        assert L >= 12, f"{superficie} L* {L:.1f}: sigue demasiado oscuro para el reporte"
