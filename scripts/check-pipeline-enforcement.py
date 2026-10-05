#!/usr/bin/env python3
"""
check-pipeline-enforcement.py - Verifica que el pacto del pipeline A/B no se
erosione en silencio.

POR QUE EXISTE (2026-10-05). Durante una sesion entera de trabajo sobre un
proyecto, el CORE delego trabajo de codigo spawneando UN solo agente con el
modelo por DEFECTO del rol (glm-5.3-flash) en vez de correr el pipeline A/B:
dos agentes distintos, A escribe con `gpt-oss:120b-cloud`, B revisa con
`deepseek-v4.1-flash:cloud` (ADR-077). Gonzo lo detecto por el consumo: no veia
uso de gpt-oss. No hubo review adversarial (B) en ninguna tarea, y las que si
se revisaron las "verifico" el propio CORE, que no es un segundo ojo.

La regla estaba escrita (AGENTS.md, ADR-077, la skill de arbitraje, el router)
y NADIE la verificaba: `scripts/model-router.sh` sugiere la ruta pero es un
chequeo VOLUNTARIO - hay que consultarlo. Una regla sin enforcement se viola
sola (misma leccion que ADR-083 y check-agent-skill-boundary.py).

Que revisa:
  1. CONSISTENCIA DEL PACTO - las cuatro fuentes que declaran los modelos A/B
     (model-router.sh, managed-blocks.py, la skill de arbitraje, ADR-077) dicen
     lo MISMO. Si una deriva, el pacto tiene dos verdades y se puede citar la
     conveniente.
  2. ASIMETRIA - A y B son modelos DISTINTOS. "Pedir otro ojo" con el mismo
     modelo no es un segundo ojo (el defecto que origino ADR-077).

Las rutas son inyectables (`root` como parametro) para que los tests construyan
arboles falsos en un directorio temporal, y para que el defecto se siembre en un
corpus descartable y no en el workspace real.

Uso:
    check-pipeline-enforcement.py
Salida: exit 0 si el pacto esta consistente, 1 si hay violaciones.
"""

import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent

# Rol ejecutor (A) y revisor (B). La asimetria es la decision (ADR-077).
A_ROLE = "gpt-oss:120b-cloud"
B_ROLE = "deepseek-v4.1-flash:cloud"


def _read(path: Path) -> Optional[str]:
    return path.read_text(encoding="utf-8") if path.exists() else None


def models_in_router(root: Path) -> Tuple[Optional[str], Optional[str]]:
    """(A, B) declarados en la ruta `pipeline_ab` de model-router.sh."""
    text = _read(root / "scripts" / "model-router.sh")
    if not text:
        return None, None
    m = re.search(r'"pipeline_ab"\s*:\s*"([^"]+)"', text)
    if not m:
        return None, None
    parts = [p.strip() for p in m.group(1).split("/")]
    if len(parts) != 2:
        return None, None
    return parts[0], parts[1]


def models_in_blocks(root: Path) -> Tuple[Optional[str], Optional[str]]:
    """(A, B) declarados como settings en managed-blocks.py."""
    text = _read(root / "scripts" / "managed-blocks.py")
    if not text:
        return None, None
    a = re.search(r'"model_pipeline_a"\s*:\s*"([^"]+)"', text)
    b = re.search(r'"model_pipeline_b"\s*:\s*"([^"]+)"', text)
    return (a.group(1) if a else None), (b.group(1) if b else None)


def models_in_skills(root: Path) -> Tuple[Optional[str], List[str]]:
    """Modelos citados en la skill de arbitraje del pipeline A/B."""
    text = _read(root / "skills" / "agent-orchestration-pipeline-model-arbitration" / "SKILL.md")
    if not text:
        return None, []
    found = [m for m in (A_ROLE, B_ROLE) if m in text]
    return text, found


def models_in_adr(root: Path) -> Tuple[Optional[str], List[str]]:
    """Modelos citados en ADR-077 (el ADR que define el pacto)."""
    adr_dir = root / "docs" / "adr"
    if not adr_dir.is_dir():
        return None, []
    hit = None
    for p in adr_dir.glob("ADR-077*"):
        hit = _read(p)
        break
    if hit is None:
        return None, []
    return hit, [m for m in (A_ROLE, B_ROLE) if m in hit]


def find_violations(root: Path) -> List[str]:
    """Devuelve las violaciones del pacto, como textos listos para imprimir."""
    violations: List[str] = []

    r_a, r_b = models_in_router(root)
    blk_a, blk_b = models_in_blocks(root)
    skl_text, skl_models = models_in_skills(root)
    adr_text, adr_models = models_in_adr(root)

    # 1) El pacto tiene que existir en TODAS las fuentes declaradas.
    if r_a is None or r_b is None:
        violations.append(
            "model-router.sh no declara la ruta `pipeline_ab` con dos modelos "
            "(A / B). Es la fuente de verdad del modelo por tarea."
        )
    if blk_a is None or blk_b is None:
        violations.append(
            "managed-blocks.py no declara `model_pipeline_a` / `model_pipeline_b`: "
            "el bloque de AGENTS.md que ve el CORE no puede propagar el pacto."
        )
    if not skl_models:
        violations.append(
            "la skill de arbitraje no nombra los modelos A/B (%s / %s)."
            % (A_ROLE, B_ROLE)
        )
    if not adr_models:
        violations.append(
            "ADR-077 no nombra los modelos A/B (%s / %s)." % (A_ROLE, B_ROLE)
        )

    # 2) Consistencia: todas las fuentes que SI declaran deben coincidir.
    declared = {
        "model-router.sh": (r_a, r_b),
        "managed-blocks.py": (blk_a, blk_b),
    }
    seen = {v for v in declared.values() if v[0] and v[1]}
    if len(seen) > 1:
        detail = "; ".join("%s -> A=%s B=%s" % (k, v[0], v[1]) for k, v in declared.items())
        violations.append(
            "el pacto A/B tiene dos verdades en las fuentes declaradas: %s. "
            "Debe ser A=%s / B=%s en todas." % (detail, A_ROLE, B_ROLE)
        )

    # 3) Asimetria: A y B distintos. Un mismo modelo no es un segundo ojo.
    for name, (a, b) in declared.items():
        if a and b and a == b:
            violations.append(
                "asimetria rota en %s: A y B son el mismo modelo (%s). "
                "El revisor debe ver mas que el ejecutor (ADR-077)." % (name, a)
            )

    # 4) Contra el canon: si una fuente declara, debe declarar el pacto vigente.
    for name, (a, b) in declared.items():
        if a and b and (a, b) != (A_ROLE, B_ROLE):
            violations.append(
                "%s declara A=%s / B=%s, distinto del pacto vigente A=%s / B=%s."
                % (name, a, b, A_ROLE, B_ROLE)
            )

    return violations


def main(argv: List[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else ROOT

    violations = find_violations(root)

    if violations:
        print("PACTO DEL PIPELINE A/B VIOLADO (%d):" % len(violations))
        for v in violations:
            print("  - " + v)
        print()
        print(
            "El CORE delega con DOS agentes: A escribe con %s, B revisa con %s "
            "(ADR-077/ADR-088). Consultar `scripts/model-router.sh model pipeline_ab`."
            % (A_ROLE, B_ROLE)
        )
        return 1

    print(
        "OK: pacto A/B consistente en router, managed-blocks, skill y ADR-077 "
        "(A=%s, B=%s, distintos)." % (A_ROLE, B_ROLE)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
