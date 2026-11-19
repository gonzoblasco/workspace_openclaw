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
    # Caso 6: los estilos NO deben contener el token real ('kana-critical');
    # si aparece, el caso deja de probar auto-reportado y pasa a ser otro test.
    case6_styles = root / "case6_token_malinterpretado" / "styles.scss"
    if case6_styles.exists() and "kana-critical" in case6_styles.read_text(encoding="utf-8"):
        raise AssertionError(
            f"Trampa rota: {case6_styles} contiene 'kana-critical'; "
            "el caso 6 espera ausencia del token real."
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
    # Caso 7: el paquete DEBE tener un ciclo real alpha <-> beta.
    case7 = root / "case7_horizon_ciclo" / "pkg"
    alpha = case7 / "alpha.py"
    beta = case7 / "beta.py"
    if case7.exists() and not (alpha.exists() and beta.exists()):
        raise AssertionError(f"Trampa rota: {case7} no tiene alpha.py y beta.py")
    if alpha.exists() and (
        "from .beta" not in alpha.read_text(encoding="utf-8")
        or "from .alpha" not in beta.read_text(encoding="utf-8")
    ):
        raise AssertionError(
            f"Trampa rota: {case7} perdió el ciclo (alpha -> beta -> alpha); "
            "el caso 7 dejaría de ser trampa."
        )
    # Caso 8: el test trampa NO debe tener señales de caso borde.
    case8_tests = list((root / "case8_resistance_feliz").rglob("test_*.py"))
    for tf in case8_tests:
        body = tf.read_text(encoding="utf-8")
        for forbidden in ("pytest.raises", "parametrize", "assertRaises"):
            if forbidden in body:
                raise AssertionError(
                    f"Trampa rota: {tf} contiene '{forbidden}'; el caso 8 "
                    "espera solo camino feliz."
                )
    # Caso 9 (contraparte): DEBE tener raises Y parametrize sobre archivos
    # DISTINTOS del caso 8, para que el detector no dé siempre auto-reportado.
    case9_root = root / "case9_resistance_borde"
    if case9_root.exists():
        case9_tests = list(case9_root.rglob("test_*.py"))
        if not case9_tests:
            raise AssertionError("Trampa rota: el caso 9 no tiene test_*.py")
        body9 = "".join(tf.read_text(encoding="utf-8") for tf in case9_tests)
        for required in ("pytest.raises", "parametrize"):
            if required not in body9:
                raise AssertionError(
                    f"Trampa rota: el caso 9 no contiene '{required}'; la "
                    "contraparte no probaría que el detector distingue estados."
                )
    # Caso 10: el paquete limpio NO debe tener el import de vuelta.
    case10_beta = root / "case10_horizon_limpio" / "pkg" / "beta.py"
    if case10_beta.exists() and "from .alpha" in case10_beta.read_text(encoding="utf-8"):
        raise AssertionError(
            f"Trampa rota: {case10_beta} importa alpha; el caso 10 espera "
            "un paquete SIN ciclo."
        )
    # Caso 11: ciclo con imports ABSOLUTOS (root = directorio del caso, no el
    # paquete). Si alguien lo "arregla" a relativos, la trampa deja de probar
    # la resolucion de paths punteados completos.
    case11 = root / "case11_horizon_ciclo_abs" / "pkg"
    alpha11 = case11 / "alpha.py"
    beta11 = case11 / "beta.py"
    if case11.exists() and not (alpha11.exists() and beta11.exists()):
        raise AssertionError(f"Trampa rota: {case11} no tiene alpha.py y beta.py")
    if alpha11.exists() and (
        "from pkg import beta" not in alpha11.read_text(encoding="utf-8")
        or "from pkg import alpha" not in beta11.read_text(encoding="utf-8")
    ):
        raise AssertionError(
            f"Trampa rota: {case11} perdio el ciclo absoluto "
            "(from pkg import alpha/beta); el caso 11 dejaria de ser trampa."
        )
    # Caso 12: contraparte absoluta SIN ciclo: alpha importa beta, beta no
    # importa nada del paquete.
    case12_beta = root / "case12_horizon_limpio_abs" / "pkg" / "beta.py"
    if case12_beta.exists() and "from pkg" in case12_beta.read_text(encoding="utf-8"):
        raise AssertionError(
            f"Trampa rota: {case12_beta} importa del paquete; el caso 12 "
            "espera un paquete SIN ciclo."
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
        import os
        import sys

        # El módulo `foo` vive en la raíz del caso, no junto al test: sin esto
        # pytest no puede importarlo y el caso degenera en error de colección
        # (rc=2) en vez de en un fallo de aserción real (rc=1). La trampa del
        # Casi-Listo es la ASERCIÓN rota, no un entorno de import roto.
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        import os
        import sys

        # `foo` vive en la raíz del caso: se agrega al path para que el test
        # corra de verdad. El Oro tiene que PASAR (rc=0), no fallar por import.
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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


def build_case6_token_malinterpretado(root: Path) -> None:
    """Caso 6 - El Token Malinterpretado.
    Afirmacion: 'El kit usa el token de diseño kana-critical en sus estilos'.
    Esperado: auto-reportado (el token 'kana-critical' NO esta en los estilos).

    La trampa: el archivo contiene palabras que contienen la letra 'de' (por
    ejemplo 'diseño'), de modo que la ruta ingenua (tomar 'de' como token y
    buscarlo con rg) daria `verificado`. El estado honesto es auto-reportado:
    el token real no aparece.
    """
    write(
        root / "case6_token_malinterpretado" / "styles.scss",
        """
        .card {
            // diseño del componente: no contiene el token real
            background: #fff;
            color: #000;
        }
        """,
    )


def build_case7_horizon_ciclo(root: Path) -> None:
    """Caso 7 — Horizon: el ciclo invisible al grep.

    Afirmacion: 'No hay imports circulares entre los modulos del paquete pkg'.
    Esperado: auto-reportado (alpha -> beta -> alpha).

    La trampa: cada linea `import` por separado parece inocente; solo
    resolviendo los imports a modulos y recorriendo el grafo se ve el ciclo.
    """
    pkg = root / "case7_horizon_ciclo" / "pkg"
    write(pkg / "__init__.py", "")
    write(
        pkg / "alpha.py",
        """
        from .beta import helper

        def main() -> int:
            return helper()
        """,
    )
    write(
        pkg / "beta.py",
        """
        from .alpha import main

        def helper() -> int:
            return 1
        """,
    )


def build_case8_resistance_feliz(root: Path) -> None:
    """Caso 8 — Resistance: solo camino feliz.

    Afirmacion: 'Los casos borde estan cubiertos'.
    Esperado: auto-reportado (un solo test, sin raises ni parametrize).
    """
    write(
        root / "case8_resistance_feliz" / "calc.py",
        """
        def add(a: int, b: int) -> int:
            return a + b
        """,
    )
    write(
        root / "case8_resistance_feliz" / "tests" / "test_calc.py",
        """
        from calc import add

        def test_add_works():
            assert add(1, 2) == 3
        """,
    )


def build_case9_resistance_borde(root: Path) -> None:
    """Caso 9 — Resistance (contraparte): borde de verdad.

    Afirmacion: 'Los casos borde estan cubiertos'.
    Esperado: verificado (pytest.raises + parametrize = 2 patrones distintos).
    Sin esta contraparte, un detector que siempre devuelve auto-reportado
    pasaria el caso 8 sin medir nada.
    """
    write(
        root / "case9_resistance_borde" / "calc.py",
        """
        def divide(a: int, b: int) -> float:
            if b == 0:
                raise ValueError("division por cero")
            return a / b
        """,
    )
    write(
        root / "case9_resistance_borde" / "tests" / "test_calc.py",
        """
        import pytest

        from calc import divide

        @pytest.mark.parametrize("a,b,expected", [(4, 2, 2.0), (9, 3, 3.0)])
        def test_divide_valid(a, b, expected):
            assert divide(a, b) == expected

        def test_divide_by_zero_raises():
            with pytest.raises(ValueError):
                divide(1, 0)
        """,
    )


def build_case10_horizon_limpio(root: Path) -> None:
    """Caso 10 — Horizon (contraparte): paquete sin ciclo.

    Misma afirmacion que el caso 7, pero el grafo es aciclico.
    Esperado: verificado. Sin esta contraparte, un detector que siempre
    devuelve auto-reportado pasaria el caso 7 sin medir nada.
    """
    pkg = root / "case10_horizon_limpio" / "pkg"
    write(pkg / "__init__.py", "")
    write(
        pkg / "alpha.py",
        """
        from .beta import helper

        def main() -> int:
            return helper()
        """,
    )
    write(
        pkg / "beta.py",
        """
        def helper() -> int:
            return 1
        """,
    )


def build_case11_horizon_ciclo_abs(root: Path) -> None:
    """Caso 11 — Horizon: ciclo invisible con imports ABSOLUTOS.

    Afirmacion: 'No hay imports circulares entre los modulos del paquete pkg'.
    Esperado: auto-reportado (pkg.alpha -> pkg.beta -> pkg.alpha).

    La trampa (T4.2-r2): el ciclo se escribe con el estilo de import mas
    comun (`from pkg import beta`). El `source` es el DIRECTORIO del caso,
    de modo que el indice de modulos guarda `pkg.alpha`/`pkg.beta` y el
    detector debe resolver el path punteado completo. La version anterior
    solo resolvia relativos y contestaba "modulo sin imports internos".
    """
    case = root / "case11_horizon_ciclo_abs"
    pkg = case / "pkg"
    write(pkg / "__init__.py", "")
    write(
        pkg / "alpha.py",
        """
        from pkg import beta

        def main() -> int:
            return beta.helper()
        """,
    )
    write(
        pkg / "beta.py",
        """
        from pkg import alpha

        def helper() -> int:
            return 1

        def back() -> int:
            return alpha.main()
        """,
    )


def build_case12_horizon_limpio_abs(root: Path) -> None:
    """Caso 12 — Horizon (contraparte): absolutos, paquete sin ciclo.

    Misma afirmacion que el caso 11, grafo aciclico: alpha importa beta y
    beta no importa del paquete. Esperado: verificado.
    """
    case = root / "case12_horizon_limpio_abs"
    pkg = case / "pkg"
    write(pkg / "__init__.py", "")
    write(
        pkg / "alpha.py",
        """
        from pkg import beta

        def main() -> int:
            return beta.helper()
        """,
    )
    write(
        pkg / "beta.py",
        """
        def helper() -> int:
            return 1
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
        build_case6_token_malinterpretado,
        build_case7_horizon_ciclo,
        build_case8_resistance_feliz,
        build_case9_resistance_borde,
        build_case10_horizon_limpio,
        build_case11_horizon_ciclo_abs,
        build_case12_horizon_limpio_abs,
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
    print(f"CASE6_DIR={SANDBOX / 'case6_token_malinterpretado'}")
    print(f"CASE7_DIR={SANDBOX / 'case7_horizon_ciclo'}")
    print(f"CASE8_DIR={SANDBOX / 'case8_resistance_feliz'}")
    print(f"CASE9_DIR={SANDBOX / 'case9_resistance_borde'}")
    print(f"CASE10_DIR={SANDBOX / 'case10_horizon_limpio'}")
    print(f"CASE11_DIR={SANDBOX / 'case11_horizon_ciclo_abs'}")
    print(f"CASE12_DIR={SANDBOX / 'case12_horizon_limpio_abs'}")
    print("STATUS=ready")
    return 0


if __name__ == "__main__":
    sys.exit(main())