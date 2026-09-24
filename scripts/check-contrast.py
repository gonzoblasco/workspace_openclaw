#!/usr/bin/env python3
"""
check-contrast.py - Verifica contraste WCAG 2.1 de TODOS los temas de kanam-os.

Por que existe: el contraste se reviso UNA VEZ a mano (2026-09-24, tras el
reporte de Gonzo "quedo muy oscuro, no se si cumple accesibilidad"). Una
revision a mano no protege nada: el proximo cambio de color vuelve a romperlo
sin que nadie note. Esto lo convierte en un chequeo que falla ruidosamente.

Y hay un motivo mas concreto: en las auditorias manuales de ese dia el script
comparaba claves con `--` contra claves sin `--`, asi que NUNCA encontraba un
par y reportaba "0 fallas". Un chequeo que no puede fallar no verifica nada.
Aca los pares se extraen del CSS real y el script falla con exit 1.

Cubre los DOS temas (dark y light). Revisar solo uno es un agujero: al agregar
el tema claro el mismo verde del oscuro daba ~1.5:1 sobre blanco, ilegible.

Que revisa, por tema:
  1. Texto de cuerpo (`text`, `muted`) sobre las 3 superficies: >= 4.5:1 (AA).
  2. Texto de estado (`warn`, `info`, `danger`, `badge-comment-text`): >= 4.5.
     Se usan como texto en badges y botones, no como decoracion.
  3. `accent` como texto: >= 4.5 (tags, badge-merged).
  4. Bordes de CONTROL (`border-control`, `accent-dim` y los `badge-*-border`):
     >= 3:1. WCAG 1.4.11 lo exige para el limite de un componente de UI.
  5. Hex HARDCODEADOS fuera de los bloques de tema: mismo umbral segun su rol.
     Escribir un color a mano esquiva una validacion que solo mira variables,
     y asi se escaparon seis, dos de ellos en controles.
  6. Que existan reglas `:focus-visible` (2.4.7: teclado a ciegas sin ellas).

Uso:
    python3 scripts/check-contrast.py [ruta/globals.css]

Salida: una seccion por tema y exit 1 si alguna falla.
"""
import re
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
DEFAULT_CSS = WS / "projects" / "kanam-os" / "app" / "globals.css"

# Superficies de fondo del tema, de mas oscura a mas clara.
SURFACES = ("bg", "panel", "panel-2")
# Texto de cuerpo.
TEXT_ROLES = ("text", "muted")
# Texto de estado (badges, botones): se lee, no decora.
STATUS_TEXT = ("warn", "info", "danger", "badge-comment-text")
# `accent` se usa como texto en tags y badge-merged.
ACCENT_TEXT = ("accent",)
# Bordes que delimitan un control o un estado: 1.4.11 pide 3:1.
BORDER_ROLES = (
    "border-control",
    "accent-dim",
    "badge-info-border",
    "badge-warn-border",
    "badge-comment-border",
)
# El tema por defecto vive en `:root`.
DEFAULT_THEME = "dark"


def srgb(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * srgb(r) + 0.7152 * srgb(g) + 0.0722 * srgb(b)


def contrast(fg, bg):
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def lstar(hex_color):
    """Claridad perceptual (CIE L*): 0 = negro, 100 = blanco.

    Se usa para distinguir "tema oscuro" de "negro casi puro": el bg original
    estaba en L* 4.0 y se veia como un pozo. Un tema oscuro real vive en 8-20.
    """
    v = luminance(hex_color)
    return 116 * (v ** (1 / 3)) - 16 if v > 0.008856 else 903.3 * v


def block_spans(css):
    """(selector, inicio, fin) de los bloques de primer nivel, en el CSS ORIGINAL.

    Recorre caracter a caracter con conciencia de comentarios, asi los offsets
    son validos para el texto tal cual viene. La version anterior limpiaba los
    comentarios ANTES de contar y despues aplicaba los offsets al texto sin
    limpiar: los indices quedaban corridos y una mutacion de prueba cambiaba
    la variable equivocada (o ninguna). Se descubrio porque un test de
    mutacion dejo de detectar el cambio que inyectaba.

    Devuelve offsets en vez de strings para que quien mute el CSS pueda
    reemplazar en el lugar correcto sin volver a parsear.
    """
    spans = []
    profundidad = 0
    sel_inicio = 0
    cuerpo_inicio = 0
    i = 0
    n = len(css)
    while i < n:
        # Saltar comentarios: pueden contener llaves y desalinear el conteo.
        if css.startswith("/*", i):
            j = css.find("*/", i + 2)
            i = n if j < 0 else j + 2
            continue
        ch = css[i]
        if ch == "{":
            profundidad += 1
            if profundidad == 1:
                cuerpo_inicio = i + 1
        elif ch == "}":
            profundidad -= 1
            if profundidad == 0:
                sel = css[sel_inicio:i].split("{")[0].strip()
                spans.append((sel, cuerpo_inicio, i))
                sel_inicio = i + 1
        i += 1
    return spans


def iter_top_blocks(css):
    """Bloques de primer nivel (selector, cuerpo), ignorando los anidados.

    Los @media contienen bloques adentro, asi que un regex simple los confunde
    y puede atribuirle variables de color al selector equivocado. `block_spans`
    los recorre por profundidad: solo interesa el nivel 0.
    """
    return [(sel, css[ini:fin]) for sel, ini, fin in block_spans(css)]


def theme_of(selector):
    """Nombre de tema del selector, o None si no define uno.

    `:root` define el tema por defecto; `[data-theme="X"]` define el suyo.
    Un selector como `:root, [data-theme="dark"]` cae en el mismo tema: es el
    patron que usa el CSS para "default + explicito".
    """
    m = re.search(r"\[data-theme=[\"']([a-z]+)[\"']\]", selector)
    if m:
        return m.group(1)
    return DEFAULT_THEME if ":root" in selector else None


def read_themes(css):
    """Todos los temas del CSS: {nombre: {variable: hex}}."""
    temas = {}
    for sel, cuerpo in iter_top_blocks(css):
        nombre = theme_of(sel)
        if nombre is None:
            continue
        variables = dict(re.findall(r"--([a-z0-9-]+):\s*(#[0-9a-fA-F]{6})", cuerpo))
        if variables:
            temas[nombre] = variables
    return temas


def read_vars(css):
    """Variables del tema por defecto, con la clave SIN los guiones.

    El `--` se saca aca y no en cada uso: comparar `--bg` contra `bg` es
    exactamente el bug que hacia que la auditoria previa no encontrara nada.
    """
    temas = read_themes(css)
    if DEFAULT_THEME not in temas:
        raise SystemExit("ERROR: no encontre el bloque :root en el CSS")
    return temas[DEFAULT_THEME]


def find_hardcoded(css):
    """Colores hex escritos a mano fuera de los bloques de tema, con su rol.

    Devuelve (selector, propiedad, valor). Solo mira `color` y `border-color`:
    son los que tienen umbral WCAG. Un hex en un `background` decorativo o en
    `.bar > span` (barra de progreso, sin texto encima) no aplica.

    Existe porque el guardia original solo leia :root, y asi se le escaparon
    seis colores con falla real, dos de ellos en CONTROLES. Escribir un color
    a mano esquiva cualquier validacion que solo mire las variables.
    """
    hallados = []
    for sel, props in iter_top_blocks(css):
        if theme_of(sel) is not None:
            continue
        for h in re.findall(r"(?<![\w-])color:\s*(#[0-9a-fA-F]{6})", props):
            hallados.append((sel.splitlines()[-1].strip(), "color", h))
        for h in re.findall(r"border-color:\s*(#[0-9a-fA-F]{6})", props):
            hallados.append((sel.splitlines()[-1].strip(), "border-color", h))
    return hallados


def check_theme(nombre, V, fallas):
    """Revisa un tema y agrega sus problemas a `fallas`."""

    def par(rol, etiqueta, umbral):
        for s in SURFACES:
            if rol not in V:
                continue
            r = contrast(V[rol], V[s])
            ok = r >= umbral
            if not ok:
                fallas.append(f"[{nombre}] {etiqueta} sobre {s}: {r:.2f} (necesita {umbral})")
            print(f"    {'OK  ' if ok else 'FALLA'}  {etiqueta:20} sobre {s:8} {r:5.2f}:1")

    print(f"\n  Tema '{nombre}'")
    print(f"    superficies: bg {V.get('bg','?')} (L* {lstar(V['bg']):.1f})  "
          f"panel {V.get('panel','?')}  panel-2 {V.get('panel-2','?')}")

    print("    -- texto (AA exige 4.5) --")
    for rol in TEXT_ROLES:
        par(rol, rol, 4.5)
    for rol in ACCENT_TEXT:
        par(rol, f"{rol} (tag)", 4.5)
    for rol in STATUS_TEXT:
        if rol in V:
            par(rol, rol, 4.5)

    print("    -- bordes de control y estado (1.4.11 exige 3) --")
    for rol in BORDER_ROLES:
        if rol in V:
            par(rol, rol, 3.0)


def check(css_path):
    css = Path(css_path).read_text(encoding="utf-8")
    temas = read_themes(css)
    if not temas:
        raise SystemExit("ERROR: no encontre ningun bloque de tema en el CSS")
    if DEFAULT_THEME not in temas:
        raise SystemExit(f"ERROR: falta el tema por defecto ({DEFAULT_THEME}) en :root")

    fallas = []
    print(f"Chequeo de contraste: {css_path}")
    print(f"  temas encontrados: {', '.join(sorted(temas))}")

    for nombre in sorted(temas):
        V = temas[nombre]
        for s in SURFACES:
            if s not in V:
                raise SystemExit(f"ERROR: el tema '{nombre}' no define --{s}")
        check_theme(nombre, V, fallas)

    # Hex HARDCODEADOS fuera de los temas.
    #
    # La primera version de este script solo leia :root, y asi se le escaparon
    # .badge-open (#1e3a5f = 1.24:1), .btn-warn y .chip-clear (#5c4715 =
    # 1.60:1). Dos de esos son CONTROLES: incumplian 1.4.11 sin que el guardia
    # lo viera. Un color escrito a mano esquiva una validacion que solo mira
    # las variables.
    hard = find_hardcoded(css)
    if hard:
        print("\n  Colores hardcodeados fuera de los temas")
        for sel, prop, val in hard:
            umbral = 4.5 if prop == "color" else 3.0
            peores = {t: min((contrast(val, V[s]), s) for s in SURFACES) for t, V in temas.items()}
            malos = {t: p for t, p in peores.items() if p[0] < umbral}
            for t, (r, s) in malos.items():
                fallas.append(
                    f"[{t}] {sel} {prop} {val}: {r:.2f} sobre {s} (necesita {umbral})"
                )
            peor_t, (peor_r, peor_s) = min(peores.items(), key=lambda kv: kv[1][0])
            marca = "FALLA" if malos else "OK  "
            print(
                f"    {marca}  {sel:22} {prop:12} {val}  "
                f"peor [{peor_t}] {peor_r:5.2f}:1 sobre {peor_s} (min {umbral})"
            )

    # 2.4.7: quitar el outline sin dar otro indicador deja el teclado a ciegas.
    print("\n  Foco visible (2.4.7)")
    hay_focus_visible = "focus-visible" in css
    if not hay_focus_visible:
        fallas.append("no hay reglas :focus-visible: el teclado no tiene indicador")
        print("    FALLA  no hay ninguna regla :focus-visible")
    else:
        print(f"    OK     hay reglas :focus-visible ({css.count('focus-visible')} usos)")

    print()
    if fallas:
        print(f"FALLA: {len(fallas)} problema(s) de contraste")
        for f in fallas:
            print(f"  - {f}")
        return 1
    print("OK: contraste WCAG AA en todos los pares de todos los temas.")
    return 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSS
    sys.exit(check(target))
