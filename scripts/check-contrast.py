#!/usr/bin/env python3
"""
check-contrast.py - Verifica contraste WCAG 2.1 de la paleta de kanam-os.

Por que existe: el contraste se reviso UNA VEZ a mano (2026-09-24, tras el
reporte de Gonzo "quedo muy oscuro, no se si cumple accesibilidad"). Una
revision a mano no protege nada: el proximo cambio de color vuelve a romperlo
sin que nadie note. Esto lo convierte en un chequeo que falla ruidosamente.

Y hay un motivo mas concreto: en las auditorias manuales de ese dia el script
comparaba claves con `--` contra claves sin `--`, asi que NUNCA encontraba un
par y reportaba "0 fallas". Un chequeo que no puede fallar no verifica nada.
Aca los pares se extraen del CSS real y el script falla con exit 1.

Que revisa:
  1. Texto normal sobre cada superficie: >= 4.5:1 (AA).
  2. Borde de CONTROL (`--border-control`): >= 3:1 sobre las 3 superficies.
     WCAG 1.4.11 lo exige para el limite de un componente de UI.
  3. Indicador de foco: >= 3:1 sobre las 3 superficies (1.4.11 + 2.4.7).
  4. Que el foco NO sea `outline: none` sin reemplazo: eso anula 2.4.7.

Uso:
    python3 scripts/check-contrast.py [ruta/globals.css]

Salida: una linea por par y exit 1 si alguna falla.
"""
import re
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
DEFAULT_CSS = WS / "projects" / "kanam-os" / "app" / "globals.css"

# Superficies de fondo del tema, de mas oscura a mas clara.
SURFACES = ("bg", "panel", "panel-2")
# Texto que debe leerse como cuerpo de texto.
TEXT_ROLES = ("text", "muted")


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


def read_vars(css):
    """Las variables de color de :root, con la clave SIN los guiones.

    El `--` se saca aca y no en cada uso: comparar `--bg` contra `bg` es
    exactamente el bug que hacia que la auditoria previa no encontrara nada.
    """
    m = re.search(r":root\s*\{(.*?)\}", css, re.S)
    if not m:
        raise SystemExit("ERROR: no encontre el bloque :root en el CSS")
    variables = dict(re.findall(r"--([a-z0-9-]+):\s*(#[0-9a-fA-F]{6})", m.group(1)))
    if not variables:
        raise SystemExit("ERROR: :root no tiene variables de color")
    return variables


def check(css_path):
    css = Path(css_path).read_text(encoding="utf-8")
    V = read_vars(css)
    fallas = []

    def need(name):
        if name not in V:
            raise SystemExit(f"ERROR: falta la variable --{name} en :root")
        return V[name]

    for s in SURFACES:
        need(s)
    need("border-control")
    need("accent")

    print(f"Chequeo de contraste: {css_path}")

    print("\n  Texto (AA exige 4.5:1)")
    for role in TEXT_ROLES:
        if role not in V:
            continue
        for s in SURFACES:
            r = contrast(V[role], V[s])
            ok = r >= 4.5
            if not ok:
                fallas.append(f"{role} sobre {s}: {r:.2f} (necesita 4.5)")
            print(f"    {'OK  ' if ok else 'FALLA'}  {role:8} sobre {s:8} {r:5.2f}:1")

    print("\n  Borde de control (1.4.11 exige 3:1)")
    for s in SURFACES:
        r = contrast(V["border-control"], V[s])
        ok = r >= 3
        if not ok:
            fallas.append(f"border-control sobre {s}: {r:.2f} (necesita 3)")
        print(f"    {'OK  ' if ok else 'FALLA'}  {V['border-control']} sobre {s:8} {r:5.2f}:1")

    print("\n  Indicador de foco (1.4.11 + 2.4.7 exigen 3:1)")
    for s in SURFACES:
        r = contrast(V["accent"], V[s])
        ok = r >= 3
        if not ok:
            fallas.append(f"accent (foco) sobre {s}: {r:.2f} (necesita 3)")
        print(f"    {'OK  ' if ok else 'FALLA'}  accent sobre {s:8} {r:5.2f}:1")

    # 2.4.7: quitar el outline sin dar otro indicador deja el teclado a ciegas.
    print("\n  Foco visible (2.4.7)")
    hay_focus_visible = "focus-visible" in css
    outline_none = re.findall(r"outline:\s*none", css)
    if not hay_focus_visible:
        fallas.append("no hay reglas :focus-visible: el teclado no tiene indicador")
        print("    FALLA  no hay ninguna regla :focus-visible")
    else:
        print(f"    OK     hay reglas :focus-visible ({css.count('focus-visible')} usos)")
    if outline_none:
        print(f"    nota   {len(outline_none)} regla(s) con `outline: none`")
        if not hay_focus_visible:
            fallas.append("`outline: none` sin reemplazo de foco visible")

    print()
    if fallas:
        print(f"FALLA: {len(fallas)} problema(s) de contraste")
        for f in fallas:
            print(f"  - {f}")
        return 1
    print("OK: contraste WCAG AA en todos los pares declarados.")
    return 0


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSS
    sys.exit(check(target))
