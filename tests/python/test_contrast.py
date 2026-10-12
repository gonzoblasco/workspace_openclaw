"""Tests for scripts/check-contrast.py - el guardia de contraste de kanam-os.

Por que existen: el contraste se reviso a mano UNA vez (2026-09-24, tras el
reporte de Gonzo "quedo muy oscuro"). Una revision manual no protege nada, y
ademas la auditoria de ese dia estaba ROTA: comparaba claves con `--` contra
claves sin `--`, asi que nunca encontraba un par y reportaba "0 fallas".

Los tests que importan son los que prueban que el chequeo PUEDE fallar. Un
check que no puede fallar no verifica nada.

Cubren los DOS temas: al agregar el tema claro, el mismo verde del oscuro daba
~1.5:1 sobre blanco. Un guardia que solo mira un tema deja ese agujero abierto.

SOBRE EL FIXTURE (2026-09-24): estos tests leian `projects/kanam-os/app/globals.css`
directamente. El workspace NO versiona el codigo de los proyectos (solo
`projects/<slug>/.knowledge/`), asi que ese archivo existe en la maquina de
desarrollo pero NUNCA en CI: 12 tests pasaban local y fallaban en CI desde
cualquier otra maquina. La causa era el entorno, no la logica del guard.

Ahora la base es `fixtures/kanam-os-themes.css`, siempre disponible. Prueba el
CONTRATO del guard (que puede fallar, y con que umbrales). La paleta REAL se
guarda donde vive la paleta: en el repo kanam-os, que es el unico que puede ver
su `globals.css`. Ver ADR-066.
"""
import importlib.util
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
# El fixture es la base de todos los tests: el contrato de temas, no la paleta.
CSS = Path(__file__).resolve().parent / "fixtures" / "kanam-os-themes.css"
# La paleta real solo existe donde el repo del proyecto esta clonado (no en CI).
CSS_REAL = ROOT / "projects" / "kanam-os" / "app" / "globals.css"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cc():
    return load("check_contrast", "scripts/check-contrast.py")


def leer_css():
    return CSS.read_text(encoding="utf-8")


# --- helpers de mutacion ---------------------------------------------------
#
# Se busca por NOMBRE de variable, nunca por el hex viejo: atar el test a un
# literal hace que se rompa al cambiar la paleta, no por logica sino porque el
# valor buscado ya no existe. Eso paso dos veces el 2026-09-24.


def set_var(css, nombre, valor):
    """Reemplaza una variable en TODOS los temas. Devuelve (css, n)."""
    nuevo, n = re.subn(
        rf"(--{nombre}:\s*)#[0-9a-fA-F]{{6}}", rf"\g<1>{valor}", css
    )
    assert n >= 1, f"no se encontro --{nombre} en el CSS"
    return nuevo, n


def in_theme(css, tema, nombre, valor):
    """Reemplaza una variable SOLO dentro del bloque de un tema.

    Hace falta porque cada variable aparece una vez por tema (2 en total): un
    `re.subn` global cambiaria las dos y el test no probaria nada.

    Usa `block_spans` del propio guardia, que devuelve offsets validos para el
    CSS ORIGINAL. La version anterior limpiaba los comentarios antes de contar
    llaves y despues aplicaba esos offsets al texto sin limpiar: quedaban
    corridos y el reemplazo caia en el lugar equivocado (o en ninguno). Se
    detecto porque el test de mutacion del tema claro dio "OK" cuando tenia
    que fallar.
    """
    for sel, ini, fin in cc().block_spans(css):
        if cc().theme_of(sel) != tema:
            continue
        nuevo_cuerpo, n = re.subn(
            rf"(--{nombre}:\s*)#[0-9a-fA-F]{{6}}", rf"\g<1>{valor}", css[ini:fin]
        )
        assert n == 1, f"--{nombre} no esta en el tema {tema} ({n} matches)"
        return css[:ini] + nuevo_cuerpo + css[fin:]
    raise AssertionError(f"no encontre el tema {tema}")


# --- la matematica de WCAG ---

def test_contraste_blanco_negro_es_21():
    m = cc()
    assert round(m.contrast("#ffffff", "#000000"), 0) == 21


def test_contraste_identico_es_1():
    m = cc()
    assert m.contrast("#6ee7a0", "#6ee7a0") == 1.0


def test_contraste_es_simetrico():
    m = cc()
    a = m.contrast("#222d29", "#f0f4f2")
    b = m.contrast("#f0f4f2", "#222d29")
    assert a == b


# --- el chequeo contra el CSS real ---

def test_paleta_del_fixture_pasa():
    """El contrato de temas (los DOS) cumple WCAG AA en todos los pares.

    Es una paleta concreta y valida: si el guard fallara contra ella, cualquier
    test de mutacion de abajo seria ambiguo (no se sabria si detecta la
    mutacion o si el guard falla de entrada).
    """
    m = cc()
    assert m.check(CSS) == 0


def test_encuentra_los_dos_temas():
    m = cc()
    temas = m.read_themes(leer_css())
    assert "dark" in temas, "falta el tema oscuro"
    assert "light" in temas, "falta el tema claro"


def test_cada_tema_define_las_variables_clave():
    """Un tema incompleto heredaria la variable del otro y se veria mal."""
    m = cc()
    temas = m.read_themes(leer_css())
    claves = ("bg", "panel", "panel-2", "border", "border-control",
              "text", "muted", "accent", "accent-dim")
    for nombre, V in temas.items():
        faltan = [k for k in claves if k not in V]
        assert not faltan, f"al tema '{nombre}' le faltan: {faltan}"


# --- los tests que prueban que el chequeo PUEDE fallar ---

def test_detecta_borde_de_control_ilegible(tmp_path):
    """CRITICO: el borde de un control necesita 3:1 (WCAG 1.4.11).

    Se inyecta el valor de la paleta original (#24302d = 1.31:1 sobre panel).
    Si este test pasara, el check seria ciego, que fue exactamente el bug de la
    auditoria manual del 2026-09-24.
    """
    css, _ = set_var(leer_css(), "border-control", "#24302d")
    f = tmp_path / "viejo.css"
    f.write_text(css, encoding="utf-8")
    m = cc()
    assert m.check(f) == 1, "el check NO detecto el borde de control por debajo de 3:1"


def test_detecta_texto_ilegible(tmp_path):
    css, _ = set_var(leer_css(), "muted", "#2a3330")
    f = tmp_path / "malo.css"
    f.write_text(css, encoding="utf-8")
    m = cc()
    assert m.check(f) == 1, "el check NO detecto texto muted ilegible"


def test_detecta_falta_de_foco_visible(tmp_path):
    """Quitar las reglas de foco debe fallar 2.4.7.

    El reemplazo tiene que ELIMINAR el token, no contenerlo: renombrar
    `focus-visible` a `focus-visible-x` dejaba el substring intacto y el check
    seguia viendolo (el mismo error de verificacion ciega que este archivo
    previene).
    """
    sin_foco = leer_css().replace("focus-visible", "focus").replace(":focus {", ":nada {")
    assert "focus-visible" not in sin_foco, "el reemplazo no elimino el token"
    f = tmp_path / "sinfoco.css"
    f.write_text(sin_foco, encoding="utf-8")
    m = cc()
    assert m.check(f) == 1, "el check NO detecto la ausencia de indicador de foco"


def test_detecta_color_hardcodeado_ilegible(tmp_path):
    """Un hex a mano esquiva una validacion que solo mira las variables.

    Asi se escaparon seis colores reales, dos de ellos en CONTROLES
    (.btn-warn y .chip-clear en 1.24:1). El caso se construye de forma
    SINTETICA: ya no hay hardcodeados en el CSS, pero el guardia tiene que
    seguir detectandolos si alguien agrega uno.
    """
    css = leer_css() + "\n\n.prueba-borde {\n  border-color: #5c4715;\n}\n"
    f = tmp_path / "hard.css"
    f.write_text(css, encoding="utf-8")
    m = cc()
    assert m.check(f) == 1, "el guardia NO detecto un borde hardcodeado ilegible"


def test_detecta_texto_hardcodeado_ilegible(tmp_path):
    css = leer_css() + "\n\n.prueba-texto {\n  color: #c084fc;\n}\n"
    f = tmp_path / "hard2.css"
    f.write_text(css, encoding="utf-8")
    m = cc()
    assert m.check(f) == 1, "el guardia NO detecto un texto hardcodeado bajo AA"


def test_hardcodeado_legible_no_falla(tmp_path):
    """La contraprueba: un hardcodeado que SI cumple no debe romper el check.

    Sin esto, el test anterior pasaria igual si el guardia fallara ante
    CUALQUIER hardcodeado, cumpliera o no.

    El color se eligio midiendo: un hardcodeado se evalua contra los DOS temas,
    asi que tiene que cumplir en ambos. Recorriendo los grises, el unico que
    llega a 3:1 en oscuro y claro es #888888 (min 3.07). Ese limite no es
    casualidad: es la razon de que cada tema tenga su propia paleta en vez de
    compartir colores fijos.
    """
    css = leer_css() + "\n\n.prueba-ok {\n  border-color: #888888;\n}\n"
    f = tmp_path / "ok.css"
    f.write_text(css, encoding="utf-8")
    m = cc()
    assert m.check(f) == 0, "el guardia rechazo un color hardcodeado que si cumple"


# --- el tema claro en particular ---

def test_tema_claro_no_reusa_los_colores_del_oscuro(tmp_path):
    """CRITICO para el tema claro: no es una inversion del oscuro.

    Si el tema claro heredara el accent del oscuro (#6ee7a0), sobre fondo
    blanco daria ~1.5:1: ilegible. Este test pone el accent oscuro en el tema
    claro y exige que el guardia lo detecte.
    """
    css = leer_css()
    oscuro = cc().read_themes(css)["dark"]["accent"]
    claro = in_theme(css, "light", "accent", oscuro)
    f = tmp_path / "claro-roto.css"
    f.write_text(claro, encoding="utf-8")
    m = cc()
    assert m.check(f) == 1, (
        f"el guardia NO detecto el accent {oscuro} del tema oscuro aplicado al tema claro"
    )


def test_tema_claro_es_claro_y_oscuro_es_oscuro():
    """Las superficies tienen que estar del lado correcto del espectro.

    Gonzo reporto DOS veces que la app estaba 'demasiado oscura'. El primer
    ajuste subio el bg de L* 4.0 a 6.6 y no se percibio: 2.6 puntos no se
    notan. Este test fija que el tema oscuro este en el rango de un tema oscuro
    real (L* >= 12) y que el claro sea efectivamente claro.
    """
    m = cc()
    temas = m.read_themes(leer_css())
    L = {t: m.lstar(V["bg"]) for t, V in temas.items()}
    assert L["dark"] >= 12, f"tema oscuro demasiado oscuro: L* {L['dark']:.1f}"
    assert L["light"] >= 90, f"tema claro no es claro: L* {L['light']:.1f}"
    assert L["light"] > L["dark"] + 60, f"los temas no se distinguen: {L}"


def test_ambos_temas_tienen_foco_visible():
    """El indicador de foco no es opcional en ninguno de los dos."""
    css = leer_css()
    assert "focus-visible" in css, "no hay indicador de foco"
    # El outline usa --accent, que cada tema define: no hay hex fijo que se
    # olvide de actualizar.
    assert "outline: 2px solid var(--accent)" in css, (
        "el foco no usa --accent: al cambiar de tema quedaria con el color viejo"
    )


# --- anti-deriva: el fixture contra la paleta real ---


def _css_var_names(css: str) -> set[str]:
    """Nombres de variables declaradas (--foo:) en un CSS."""
    return set(re.findall(r"--([a-z0-9-]+)\s*:", css))


@pytest.mark.skipif(
    not CSS_REAL.exists(),
    reason="el repo kanam-os no esta clonado: la paleta real no existe aca (normal en CI)",
)
def test_fixture_no_deriva_del_css_real():
    """En la maquina que SI tiene el proyecto, el fixture no puede quedar viejo.

    kanam-os resuelve sus TEMAS por `@import` (public/kanam.css -> :root claro,
    public/dark.css -> [data-theme=dark]) y expone los ROLES que este guard
    consume como ALIAS declarados en el propio `globals.css`
    (`--bg: var(--k-surface-base)`, ...).

    Por eso el contrato a comparar es la CAPA DE ALIAS del globals.css, no los
    valores `--k-*` resueltos: el fixture documenta los alias que el guard lee,
    y si el CSS real deja de declarar un rol, el guard quedaria CIEGO en ese
    par. La version anterior leia los temas resueltos; al pasar kanam-os a
    `@import` devolvia `{}` y se "resolvio" con un skipif que lo desactivaba
    SIEMPRE (el @import nunca desaparece) - una guarda que no puede fallar.
    """
    m = cc()
    roles = (
        set(m.SURFACES)
        | set(m.TEXT_ROLES)
        | set(m.STATUS_TEXT)
        | set(m.ACCENT_TEXT)
        | set(m.BORDER_ROLES)
    )
    real = _css_var_names(CSS_REAL.read_text(encoding="utf-8"))
    fixture = _css_var_names(leer_css())
    faltan_real = sorted(roles - real)
    faltan_fixture = sorted(roles - fixture)
    assert not faltan_real, (
        f"el CSS real ya no declara roles que la guarda lee: {faltan_real}"
    )
    assert not faltan_fixture, (
        f"al fixture le faltan roles que la guarda lee: {faltan_fixture}"
    )
    sobra = sorted(fixture - real)
    assert not sobra, (
        f"el fixture declara variables que el CSS real no define: {sobra}"
    )
