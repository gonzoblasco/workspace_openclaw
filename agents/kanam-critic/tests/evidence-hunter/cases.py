#!/usr/bin/env python3
"""
cases.py — Fuente ÚNICA de verdad para los 10 casos del laboratorio.

Cualquier cambio en la lista de casos (descripciones, fuentes esperadas,
estados, citas) vive acá. Los otros archivos (`scaffold.py`,
`build_assertions.py`, `validate.py`, `README.md`‑tabla) consumen este módulo.

Diseño:
  - Cada caso es un dataclass inmutable para evitar mutaciones accidentales.
  - El campo `evidence_pattern` es una regex opcional. Si está presente,
    `validate.py` exige que `details[i].evidence` matchee; si no está, solo
    exige que el campo exista y no sea None (cita mínima).
  - `status_esperado` es uno de: verificado | parcial | auto-reportado | bloqueado.

Regla:
  - Si añades un caso, todos los archivos lo ven automáticamente.
  - Si cambias un caso, el README‑tabla debe regenerarse manualmente
    (es texto, no se puede auto‑generar en runtime).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Case:
    id: int
    name: str
    description: str
    source: str
    expected_status: str
    detector: str
    evidence_pattern: str | None  # regex opcional; None = solo exige presencia.


# Tabla canónica. Cualquier divergencia con el README debe corregirse
# simultáneamente en ambos lugares — este archivo es la fuente.
CASES: list[Case] = [
    Case(
        id=0,
        name="El Mentiroso",
        description="Hay tests unitarios para foo()",
        source="case1_mentiro/foo.py",
        expected_status="auto-reportado",
        detector="grep de archivos test_*.py",
        evidence_pattern=None,
    ),
    Case(
        id=1,
        name="El Casi-Listo",
        description="La función foo() está cubierta y pasa el test",
        source="case2_casi_listo/foo.py",
        expected_status="parcial",
        detector="ejecución real de pytest",
        # Acepta tanto la ruta del test fallido (parcial real) como el
        # mensaje "command not found" cuando pytest no existe (bloqueado).
        # `validate.py` distingue ambos por el status, no por la cita.
        evidence_pattern=r"(test_foo\.py|command not found|No such file)",
    ),
    Case(
        id=2,
        name="El Invisible",
        description="Uso el token color-primary",
        source="case3_invisible/styles.scss",
        expected_status="auto-reportado",
        detector="rg en .scss/.css",
        evidence_pattern=None,
    ),
    Case(
        id=3,
        name="El Oro",
        description="La función foo() está cubierta y el test pasa",
        source="case4_oro/tests/test_foo.py",
        expected_status="verificado",
        detector="pytest",
        # La cita debe apuntar al test que pasa.
        evidence_pattern=r"tests/test_?foo\.py",
    ),
    Case(
        id=4,
        name="El Bloqueado",
        description="La cobertura de tests es > 80 %",
        source="case5_bloqueado/bar.py",
        expected_status="bloqueado",
        detector="coverage ausente",
        # El patrón acepta la RAZÓN HONESTA del bloqueo, no una frase fabricada
        # para satisfacerlo. El detector declara por qué no puede medir:
        # la herramienta ausente (PATH/venv) o el detector sin implementar.
        evidence_pattern=r"(PATH|venv|no se puede medir|no implementado|TODO)",
    ),
    Case(
        id=5,
        name="El Token Malinterpretado",
        description="El kit usa el token de diseño kana-critical en sus estilos",
        source="case6_token_malinterpretado/styles.scss",
        expected_status="auto-reportado",
        detector="extracción de token + rg en .scss/.css",
        # Trampa del 2026-11-06: el detector tomaba la preposición 'de' como
        # token, lo buscaba con rg y lo encontraba en cualquier lado del repo:
        # devolvía `verificado` con una cita que no probaba nada. El archivo de
        # este caso contiene 'de' a propósito (para que la ruta ingenua dé
        # verificado) pero NO contiene el token real: el estado honesto es
        # auto-reportado.
        evidence_pattern=r"(kana-critical|no aparece)",
    ),
    Case(
        id=6,
        name="Horizon — Ciclo Invisible",
        description="No hay imports circulares entre los modulos del paquete pkg",
        source="case7_horizon_ciclo/pkg",
        expected_status="auto-reportado",
        detector="ast: grafo de imports + DFS de ciclos",
        # Trampa: cada `import` suelto parece inocente; un grep de 'import' no
        # ve el ciclo alpha -> beta -> alpha. Solo el grafo lo muestra.
        evidence_pattern=r"\.py:\d+ .*ciclo",
    ),
    Case(
        id=7,
        name="Resistance — Solo Camino Feliz",
        description="Los casos borde estan cubiertos",
        source="case8_resistance_feliz/tests/test_calc.py",
        expected_status="auto-reportado",
        detector="patrones declarativos de caso borde",
        evidence_pattern=r"(camino feliz|sin casos borde|sin tests)",
    ),
    Case(
        id=8,
        name="Resistance — Borde Real",
        description="Los casos borde estan cubiertos",
        source="case9_resistance_borde/tests/test_calc.py",
        expected_status="verificado",
        detector="patrones declarativos de caso borde",
        # Contraparte del caso 7: pytest.raises + parametrize son dos patrones
        # distintos. Sin este caso, un detector que siempre devuelve
        # auto-reportado pasaria la trampa sin medir nada.
        evidence_pattern=r"test_.*\.py:\d+",
    ),
    Case(
        id=9,
        name="Horizon — Paquete Limpio",
        description="No hay imports circulares entre los modulos del paquete pkg",
        source="case10_horizon_limpio/pkg",
        expected_status="verificado",
        detector="ast: grafo de imports + DFS de ciclos",
        # Contraparte del caso 6: mismo texto, grafo aciclico.
        evidence_pattern=r"\.py:\d+ .*sin ciclos",
    ),
    Case(
        id=10,
        name="Horizon — Ciclo por Imports Absolutos",
        description="No hay imports circulares entre los modulos del paquete pkg",
        source="case11_horizon_ciclo_abs",
        expected_status="auto-reportado",
        detector="ast: grafo de imports + DFS de ciclos",
        # Trampa T4.2-r2: el ciclo se escribe con imports ABSOLUTOS
        # (`from pkg import beta`), el estilo mas comun. El detector solo
        # resolvia relativos y devolvia "modulo sin imports internos":
        # fabricaba evidencia a favor de una afirmacion falsa.
        evidence_pattern=r"\.py:\d+ .*ciclo",
    ),
    Case(
        id=11,
        name="Horizon — Absolutos Limpio",
        description="No hay imports circulares entre los modulos del paquete pkg",
        source="case12_horizon_limpio_abs",
        expected_status="verificado",
        detector="ast: grafo de imports + DFS de ciclos",
        # Contraparte del caso 10: imports absolutos resueltos contra el
        # indice y grafo aciclico. Sin este caso, un detector que devolviera
        # siempre auto-reportado (o bloqueado) pasaria la trampa sin medir.
        evidence_pattern=r"\.py:\d+ .*sin ciclos",
    ),
]
