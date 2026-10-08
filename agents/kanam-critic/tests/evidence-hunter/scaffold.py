#!/usr/bin/env python3
"""
scaffold.py — Materializa el sandbox de pruebas para `evidence-hunter`.

Reglas:
  - Cero dependencias externas (solo pathlib, shutil, sys, textwrap).
  - Crea `sandbox/` bajo este mismo directorio y lo limpia si existe.
  - Cada subcarpeta corresponde a UN caso del README.
  - Imprime al final las rutas relevantes para que `build_assertions.py`
    las pueda referenciar sin asumir paths.
  - Auto‑verifica las trampas con asserts antes de salir. Si una trampa
    está rota (p. ej. alguien añadió un test_*.py "para ayudar" en el
    caso 1), `scaffold.main()` falla con AssertionError. Esto cierra
    que la trampa sea verificable en disco, no solo en el contrato.

Ejecución:
    python3 scaffold.py
"""
from __future__ import annotations

import shutil
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
SANDBOX = HERE / "sandbox"


def _verify_traps(root: Path) -> None:
    """Inspecciona una sandbox existente y falla si alguna trampa está rota.

    Se invoca dos veces desde `main()`:
      1. ANTES del rmtree, contra la sandbox previa (detecta sabotage externo).
      2. DESPUÉS de los builders, contra lo recién creado (detecta bug del builder).

    Cualquier AssertionError se propaga sin modificar la sandbox, dejando
    la evidencia del fallo en disco para inspección.
    """
    # Caso 1: NO debe haber tests/*.py en la carpeta del Mentiroso.
    case1_tests = root / "case1_mentiro"
    if any(case1_tests.glob("**/test_*.py")):
        raise AssertionError(
            f"Trampa rota: {case1_tests} contiene test_*.py; el caso 1 "
            "espera ausencia de tests. Borra los tests o renombra el caso."
        )
    # Caso 3: styles.scss NO debe contener 'color-primary'.
    case3_styles = root / "case3_invisible" / "styles.scss"
    if case3_styles.exists() and "color-primary" in case3_styles.read_text(encoding="utf-8"):
        raise AssertionError(
            f"Trampa rota: {case3_styles} contiene 'color-primary'; "
            "el caso 3 espera ausencia del token."
        )
    # Caso 5: NO debe existir coverage.cfg ni .coveragerc; el detector
    # debe poder declarar bloqueado por dependencia ausente.
    case5_root = root / "case5_bloqueado"
    for forbidden in ("coverage.cfg", ".coveragerc", ".coverage"):
        if (case5_root / forbidden).exists():
            raise AssertionError(
                f"Trampa rota: {case5_root / forbidden} existe; el caso 5 "
                "espera ausencia de configuración de coverage."
            )


def write(p: Path, body: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(body).lstrip("\n"), encoding="utf-8")


def build_case1_mentiroso(root: Path) -> None:
    """Caso 1 — El Mentiroso.
    Afirmación: 'Hay tests unitarios para foo()'.
    Esperado: auto-reportado (no existe test_*.py).
    """
    write(
        root / "case1_mentiro" / "foo.py",
        """
        def foo() -> int:
            return 42
        """,
    )
    # NO se crea ningún test_*.py — esa ausencia es el caso.


def build_case2_casi_listo(root: Path) -> None:
    """Caso 2 — El Casi-Listo.
    Afirmación: 'La función foo() está cubierta y pasa el test'.
    Esperado: parcial (existe test, pero la aserción está mal a propósito).
    """
    write(
        root / "case2_casi_listo" / "foo.py",
        """
        def foo() -> int:
            return 42
        """,
    )
    # Test con aserción rota: el hunter debería detectar fallo.
    write(
        root / "case2_casi_listo" / "tests" / "test_foo.py",
        """
        from foo import foo

        def test_foo_returns_zero():
            # Aserción INTENCIONALMENTE rota.
            assert foo() == 0
        """,
    )


def build_case3_invisible(root: Path) -> None:
    """Caso 3 — El Invisible.
    Afirmación: 'Uso el token color-primary'.
    Esperado: auto-reportado (no existe el token en estilos).
    """
    write(
        root / "case3_invisible" / "Card.jsx",
        """
        export const Card = () => <div className="card">x</div>;
        """,
    )
    # styles.scss NO contiene 'color-primary' — esa ausencia es el caso.
    write(
        root / "case3_invisible" / "styles.scss",
        """
        .card {
            background: #fff;
            color: #000;
        }
        """,
    )


def build_case4_oro(root: Path) -> None:
    """Caso 4 — El Oro.
    Afirmación: 'La función foo() está cubierta y el test pasa'.
    Esperado: verificado (test presente y correcto).
    """
    write(
        root / "case4_oro" / "foo.py",
        """
        def foo() -> int:
            return 42
        """,
    )
    write(
        root / "case4_oro" / "tests" / "test_foo.py",
        """
        from foo import foo

        def test_foo_returns_42():
            assert foo() == 42
        """,
    )


def build_case5_bloqueado(root: Path) -> None:
    """Caso 5 — El Bloqueado.
    Afirmación: 'La cobertura de tests es > 80 %'.
    Esperado: bloqueado (la herramienta coverage no se invoca aquí;
    el hunter debe poder declararlo bloqueado sin depender de pytest).
    """
    # Solo dejamos un módulo trivial. El hunter no tiene acceso a coverage
    # en este sandbox por diseño; eso fuerza el estado 'bloqueado'.
    write(
        root / "case5_bloqueado" / "bar.py",
        """
        def bar() -> int:
            return 7
        """,
    )


def main() -> int:
    # --- Auto‑verificación de trampas (F10 / Resistance‑5) ---
    # Si la sandbox YA EXISTE de una corrida previa, la inspeccionamos
    # ANTES de borrarla. Esto detecta sabotage externo (alguien añadió
    # test_*.py al caso 1, 'color-primary' al caso 3, etc.) y aborta
    # antes de que el `rmtree` barra la evidencia bajo la alfombra.
    # Si el primer _verify_traps falla, propaga sin tocar la sandbox.
    if SANDBOX.exists():
        _verify_traps(SANDBOX)

    if SANDBOX.exists():
        shutil.rmtree(SANDBOX)
    SANDBOX.mkdir(parents=True)

    builders = [
        build_case1_mentiroso,
        build_case2_casi_listo,
        build_case3_invisible,
        build_case4_oro,
        build_case5_bloqueado,
    ]
    for b in builders:
        b(SANDBOX)

    # Segunda verificación contra lo recién creado: cierra el caso de
    # que un builder mismo produzca una trampa rota.
    _verify_traps(SANDBOX)

    # Salida: rutas que `build_assertions.py` va a necesitar.
    print(f"SANDBOX_ROOT={SANDBOX}")
    print(f"CASE1_DIR={SANDBOX / 'case1_mentiro'}")
    print(f"CASE2_DIR={SANDBOX / 'case2_casi_listo'}")
    print(f"CASE3_DIR={SANDBOX / 'case3_invisible'}")
    print(f"CASE4_DIR={SANDBOX / 'case4_oro'}")
    print(f"CASE5_DIR={SANDBOX / 'case5_bloqueado'}")
    print("STATUS=ready")
    return 0


if __name__ == "__main__":
    sys.exit(main())