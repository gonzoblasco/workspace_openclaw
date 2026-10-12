#!/usr/bin/env python3
"""
cases.py — Fuente ÚNICA de verdad para los 5 casos del laboratorio.

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
]