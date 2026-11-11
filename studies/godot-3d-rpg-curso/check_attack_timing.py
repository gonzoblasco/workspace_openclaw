#!/usr/bin/env python3
"""check_attack_timing.py - el golpe cae en el tick que toca, no antes.

Falla cuando aparece una ventana de inicio de ataque (windup) en la que el que
pega puede moverse o cambiar de objetivo ANTES de que el golpe se resuelva.

El curso (Módulo 5, «Changing States» / «Player Damaging Monsters») enseña a
enmarcar el golpe: el `Area3D` del arma se habilita en el frame exacto del
impacto y se deshabilita inmediatamente después. En simulacion por ticks el
equivalente es no resolver el dano en el mismo tick en que se decide atacar,
sino reservar un windup y cancelarlo si el atacante se mueve o retargetea.

Uso:
    python3 check_attack_timing.py projects/reinos-de-la-frontera
"""
import re
import sys
from pathlib import Path

WINDUP_FIELDS = ("windup_ticks", "attack_windup", "windup")


def load(target: Path) -> str:
    f = target / "sim" / "sim_state.gd"
    if not f.exists():
        print(f"SKIP: no existe {f}")
        raise SystemExit(0)
    return f.read_text(encoding="utf-8")


def main() -> int:
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    src = load(target)

    # Localizar el bloque de resolucion de ataque.
    m = re.search(r"Within range: attempt attack if cooldown ready\.(.*?)# Process projectile",
                  src, re.S)
    if not m:
        print(f"FAIL: no se encontro el bloque de resolucion de ataque en {target}")
        return 1
    block = m.group(1)

    failures = []

    # 1. El dano se aplica dentro del mismo bloque condicional que decide atacar,
    #    sin un windup intermedio.
    decides_attack = "if ent.attack_timer <= 0:" in block
    applies_damage = "hp = max(0," in block
    has_windup = any(f in src for f in WINDUP_FIELDS)

    if decides_attack and applies_damage and not has_windup:
        failures.append(
            "El dano se resuelve en el mismo tick que se decide atacar "
            "(sin windup). Un atacante que se mueve en el tick siguiente ya "
            "hizo dano igual."
        )

    # 2. Cancelacion: si hay windup declarado, tiene que existir su cancelacion
    #    cuando el atacante deja el objetivo o se mueve.
    if has_windup:
        has_cancel = bool(re.search(
            r"windup(_ticks)?\s*=\s*-?1|attack_windup\s*=\s*0", src))
        if not has_cancel:
            failures.append(
                "Hay un campo de windup pero ningun sitio lo cancele: el golpe "
                "se resuelve aunque el atacante haya cambiado de objetivo."
            )

    if failures:
        print("FAIL: la ventana de ataque no esta enmarcada")
        for f in failures:
            print(f"  - {f}")
        return 1

    print("OK: el golpe se resuelve en una ventana declarada y cancelable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
