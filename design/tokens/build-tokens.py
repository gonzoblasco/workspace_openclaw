#!/usr/bin/env python3
"""
build-tokens.py - Kanam Design System token builder.

Resuelve las referencias {capa.clave} de los tokens JSON y genera CSS
utilizable (una hoja por contexto: sistema base + cada tema de producto).

Uso:
  python3 design/tokens/build-tokens.py

Salida (por contexto):
  design/tokens/dist/kanam.css          sistema base Kanam (:root)
  design/tokens/dist/<tema>.css         scope [data-theme="<tema>"] (apps multi-tema)
  design/tokens/dist/<tema>.root.css    scope :root (apps de un solo tema, ej. Gradio)
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
SYS = ROOT / "kanam.tokens.json"
THEMES = [
    ("plaza", ROOT / "themes" / "plaza.tokens.json"),
    ("terrario", ROOT / "themes" / "terrario.tokens.json"),
    # dark es el eje de MODO (oscuro/claro), no de marca: hoy comparte el
    # atributo data-theme con plaza/terrario por simpleza. El sistema base
    # kanam.css ES el modo claro.
    ("dark", ROOT / "themes" / "dark.tokens.json"),
]

REF = re.compile(r"\{([a-zA-Z0-9_.]+)\}")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def flatten(node, prefix=""):
    """Aplana el arbol a {path: valor} sin las claves de metadata ($...)."""
    out = {}
    if not isinstance(node, dict):
        return {prefix: node}
    for k, v in node.items():
        if k.startswith("$"):
            continue
        path = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            out.update(flatten(v, path))
        else:
            out[path] = v
    return out


def resolve(value, primitives, semantic, depth=0):
    """Resuelve {refs} en cadena. `primitive.*` mira primitivas; el resto, semanticas."""
    if not isinstance(value, str) or "{" not in value or depth > 8:
        return value

    def sub(m):
        key = m.group(1)
        if key.startswith("primitive."):
            target = primitives.get(key[len("primitive."):])
        else:
            target = semantic.get(key)
        if target is None:
            return m.group(0)  # deja la ref sin resolver (se ve el error, no se esconde)
        return resolve(target, primitives, semantic, depth + 1)

    return REF.sub(sub, value)


def css_name(path):
    """semantic.brand.primary -> --k-brand-primary"""
    return "--k-" + path.replace(".", "-")


def build():
    DIST.mkdir(parents=True, exist_ok=True)
    system = load(SYS)
    prim_flat = flatten(system.get("primitive", {}))
    sem_flat = flatten(system.get("semantic", {}))

    written = []

    # 1) Sistema base Kanam
    lines = [
        "/* KANAM DESIGN SYSTEM - generado por build-tokens.py. NO editar a mano. */",
        "/* Fuente de verdad: design/tokens/kanam.tokens.json */",
        ":root {",
    ]
    for path, val in sem_flat.items():
        resolved = resolve(val, prim_flat, sem_flat)
        lines.append(f"  {css_name(path)}: {resolved};")
    lines.append("}")
    (DIST / "kanam.css").write_text("\n".join(lines) + "\n", encoding="utf-8")
    written.append(("kanam.css", len(sem_flat)))

    # 2) Temas: override de la capa semantica, en dos variantes de scope.
    #    - [data-theme="x"]: apps multi-tema (cambian el tema en runtime).
    #    - :root:            apps de un solo tema que no controlan el atributo del root (Gradio).
    for name, path_json in THEMES:
        theme = load(path_json)
        t_flat = flatten(theme.get("semantic", {}))
        body = []
        for path, val in t_flat.items():
            resolved = resolve(val, prim_flat, {**sem_flat, **t_flat})
            body.append(f"  {css_name(path)}: {resolved};")
        header = [
            f"/* TEMA {name.upper()} - generado por build-tokens.py. NO editar a mano. */",
            f"/* Fuente: design/tokens/themes/{name}.tokens.json (extiende el sistema Kanam) */",
        ]
        (DIST / f"{name}.css").write_text(
            "\n".join(header + [f'[data-theme="{name}"] {{'] + body + ["}"]) + "\n",
            encoding="utf-8",
        )
        written.append((f"{name}.css", len(t_flat)))
        (DIST / f"{name}.root.css").write_text(
            "\n".join(
                header
                + [f"/* scope :root - para apps de un solo tema (consumir junto a kanam.css) */"]
                + [":root {"]
                + body
                + ["}"]
            )
            + "\n",
            encoding="utf-8",
        )
        written.append((f"{name}.root.css", len(t_flat)))

    for fname, n in written:
        print(f"  {fname}: {n} tokens")
    print(f"OK: {len(written)} hojas generadas en {DIST}")

    # Verificacion: ninguna ref sin resolver en la salida.
    unresolved = []
    for f in DIST.glob("*.css"):
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if "{" in line and "}" in line and "--k-" in line:
                unresolved.append(f"{f.name}:{i}: {line.strip()}")
    if unresolved:
        print(f"AVISO: {len(unresolved)} referencias sin resolver:")
        for u in unresolved[:5]:
            print("  ", u)
        raise SystemExit(1)
    print("Verificacion: todas las referencias resueltas.")


if __name__ == "__main__":
    build()
