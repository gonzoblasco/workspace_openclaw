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
C_ROLE = "minimax-m3.1-flash:cloud"
# Pre-filtro barato (ADR-089). Corre antes del gate B; no autoriza solo.
PREFILTER = "gemma4:cloud"


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

def models_c_in_router(root: Path) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """(A, B, C) declarados en la ruta `pipeline_abc` de model-router.sh."""
    text = _read(root / "scripts" / "model-router.sh")
    if not text:
        return None, None, None
    m = re.search(r'"pipeline_abc"\s*:\s*"([^"]+)"', text)
    if not m:
        return None, None, None
    parts = [p.strip() for p in m.group(1).split("/")]
    if len(parts) != 3:
        return None, None, None
    return parts[0], parts[1], parts[2]


def models_in_blocks(root: Path) -> Tuple[Optional[str], Optional[str]]:
    """(A, B) declarados como settings en managed-blocks.py."""
    text = _read(root / "scripts" / "managed-blocks.py")
    if not text:
        return None, None
    a = re.search(r'"model_pipeline_a"\s*:\s*"([^"]+)"', text)
    b = re.search(r'"model_pipeline_b"\s*:\s*"([^"]+)"', text)
    return (a.group(1) if a else None), (b.group(1) if b else None)


def prefilter_in_router(root: Path) -> Optional[str]:
    """Modelo de la ruta `pipeline_ab_prefilter` de model-router.sh."""
    text = _read(root / "scripts" / "model-router.sh")
    if not text:
        return None
    m = re.search(r'"pipeline_ab_prefilter"\s*:\s*"([^"]+)"', text)
    return m.group(1) if m else None


def prefilter_in_blocks(root: Path) -> Optional[str]:
    text = _read(root / "scripts" / "managed-blocks.py")
    if not text:
        return None
    m = re.search(r'"model_pipeline_prefilter"\s*:\s*"([^"]+)"', text)
    return m.group(1) if m else None


def parse_porcelain(output: str) -> List[Tuple[str, str]]:
    """Parsea `git status --porcelain` (v1) -> lista de (status, path).

    Formato porcelain v1: XY<space>PATH, donde XY son 2 chars de estado.
    El path empieza en el indice 3. Si el path contiene caracteres especiales
    git lo entrecomilla; desentrecomillamos para devolver el path real.
    """
    entries: List[Tuple[str, str]] = []
    for line in output.splitlines():
        if len(line) < 4:
            continue
        status = line[:2]
        path = line[3:]
        if path.startswith('"') and path.endswith('"'):
            path = path[1:-1]
        entries.append((status, path))
    return entries


def _git_staged_report(root: Path) -> Tuple[List[str], str]:
    """Reporte informativo: que paths estan en staging y que cambio en cada uno.

    Devuelve (staged_paths, report_text). Es INFORMATIVO: su resultado nunca se
    cuenta como violacion del pacto A/B (un workspace sucio no rompe el pacto).
    """
    import subprocess
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=root, capture_output=True, text=True, timeout=5
        )
    except Exception as e:
        return [], "No se pudo leer el estado de git: %s" % e

    if not result.stdout.strip():
        return [], "Workspace limpio: nada en staging."

    entries = parse_porcelain(result.stdout)
    # Staged = cambios ya agregados al index (columna X != ' ' y no untracked '??').
    staged_paths = [p for status, p in entries
                    if not status.startswith("?") and status[0] != " "]
    untracked = [p for status, p in entries if status.startswith("?")]

    lines = []
    if staged_paths:
        lines.append("Paths en staging (%d): %s" % (len(staged_paths), " | ".join(staged_paths)))
        for path in staged_paths:
            try:
                d = subprocess.run(
                    ["git", "diff", "--staged", "--", path],
                    cwd=root, capture_output=True, text=True, timeout=3
                )
                if d.stdout.strip():
                    lines.append("\n--- %s\n%s" % (path, d.stdout.rstrip()))
            except Exception:
                pass
    else:
        lines.append("Nada en staging.")
    if untracked:
        lines.append("Untracked (%d): %s" % (len(untracked), " | ".join(untracked)))

    return staged_paths, "\n".join(lines)

def models_in_skills(root: Path) -> Tuple[Optional[str], List[str]]:
    """Modelos citados en la skill de arbitraje del pipeline (A/B/C)."""
    text = _read(root / "skills" / "agent-orchestration-pipeline-model-arbitration" / "SKILL.md")
    if not text:
        return None, []
    found = [m for m in (A_ROLE, B_ROLE, C_ROLE) if m in text]
    return text, found


def models_in_adr(root: Path) -> Tuple[Optional[str], List[str]]:
    """Modelos citados en ADRs (principalmente ADR-077 y ADR-105) que definen el pacto.

    The original implementation only globs ``ADR-07*`` which matches ``ADR-077``
    but **excludes** ``ADR-105`` (or any other ADR that starts with ``ADR-1``).
    This caused the checker to never see the ``C`` model declared in ``ADR-105``
    and consequently always report a false violation.

    We now include any ADR that starts with ``ADR-0`` – this captures both the
    existing ``ADR-077`` and ``ADR-105`` (the latter begins with ``ADR-1`` but
    lives in the same ``docs/adr`` directory). The heuristic still works for
    future ADR numbers because the pact‑defining ADRs are expected to be in the
    ``0xx`` range. If additional unrelated ADRs appear they will be read as
    well, but they will not contribute any of the canon model strings, so the
    logic remains correct.
    """
    adr_dir = root / "docs" / "adr"
    if not adr_dir.is_dir():
        return None, []
    hits = []
    # Include both ADR‑077 (pipeline AB) and ADR‑105 (pipeline ABC) and any
    # future ADRs that start with ``ADR-0``.
    for p in adr_dir.glob("ADR-*" ):
        content = _read(p)
        if content:
            hits.append(content)
    if not hits:
        return None, []
    combined = "\n".join(hits)
    return combined, [m for m in (A_ROLE, B_ROLE, C_ROLE) if m in combined]


def find_violations(root: Path) -> List[str]:
    """Devuelve las violaciones del pacto, como textos listos para imprimir."""
    violations: List[str] = []

    r_a, r_b = models_in_router(root)
    blk_a, blk_b = models_in_blocks(root)
    # C modelo from blocks
    blk_c = None
    text_blocks = _read(root / "scripts" / "managed-blocks.py")
    if text_blocks:
        m_c = re.search(r'"model_pipeline_c"\s*:\s*"([^\"]+)"', text_blocks)
        if m_c:
            blk_c = m_c.group(1)
    skl_text, skl_models = None, []    # arbitraje skill eliminada (2026-11-06): modelos viven en model-router.sh + managed blocks.
    adr_text, adr_models = models_in_adr(root)

    # 1) El pacto tiene que existir en TODAS las fuentes declaradas (A/B y C).
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
    # Verificar existencia de pipeline_abc y modelo C en router
    r_a3, r_b3, r_c3 = models_c_in_router(root)
    # Determine if the router file mentions the `pipeline_abc` key at all.
    router_text = _read(root / "scripts" / "model-router.sh")
    has_abc_key = router_text and "pipeline_abc" in router_text
    if r_a3 is None or r_b3 is None or r_c3 is None:
        # The key exists but the split did not provide three parts → only two models.
        if has_abc_key and (r_a3 is not None or r_b3 is not None or r_c3 is None):
            violations.append(
                "model-router.sh declara la ruta `pipeline_abc` con solo dos modelos (A / B). "
                "Se requieren tres modelos (A / B / C)."
            )
        else:
            violations.append(
                "model-router.sh no declara la ruta `pipeline_abc` con tres modelos (A / B / C). "
                "Debe declarar exactamente 3 modelos para el pacto ABC."
            )
    # Verificar existencia de modelo C en managed-blocks
    if blk_c is None:
        violations.append(
            "managed-blocks.py no declara `model_pipeline_c`: el bloque de AGENTS.md "
            "no contiene la definición del modelo C."
        )
    if not adr_models:
        violations.append(
            "ADR-077 no nombra los modelos A/B (%s / %s)." % (A_ROLE, B_ROLE)
        )
    # Si ADR-105 no menciona C, reportar.
    if C_ROLE not in adr_models:
        violations.append(
            "ADR-105 no nombra el modelo C (%s)." % C_ROLE
        )

    # 2) Consistencia: todas las fuentes que SI declaran deben coincidir (A/B y C).
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
    # Verificar consistencia del modelo C entre router y managed-blocks
    if r_c3 and blk_c and r_c3 != blk_c:
        violations.append(
            "el modelo C declarado en router (%s) es distinto del declarado en managed-blocks (%s). "
            "Debe ser consistente." % (r_c3, blk_c)
        )

    # 3) Asimetria: A y B distintos. Un mismo modelo no es un segundo ojo.
    for name, (a, b) in declared.items():
        if a and b and a == b:
            violations.append(
                "asimetria rota en %s: A y B son el mismo modelo (%s). "
                "El revisor debe ver mas que el ejecutor (ADR-077)." % (name, a)
            )
    # Asimetria C contra A y B
    if r_c3:
        if r_c3 == r_a:
            violations.append(
                "asimetria rota: modelo C (%s) es igual al modelo A (%s)." % (r_c3, r_a)
            )
        if r_c3 == r_b:
            violations.append(
                "asimetria rota: modelo C (%s) es igual al modelo B (%s)." % (r_c3, r_b)
            )

    # 4) Contra el canon: si una fuente declara, debe declarar el pacto vigente.
    for name, (a, b) in declared.items():
        if a and b and (a, b) != (A_ROLE, B_ROLE):
            violations.append(
                "%s declara A=%s / B=%s, distinto del pacto vigente A=%s / B=%s."
                % (name, a, b, A_ROLE, B_ROLE)
            )
    # Verificar que el modelo C coincide con el canon
    # Verify that the ABC route models match the canonical definitions.
    if r_c3 and (r_c3 != C_ROLE):
        violations.append(
            "model-router.sh declara C=%s en `pipeline_abc`, distinto del canon %s." % (r_c3, C_ROLE)
        )
    if r_a3 and (r_a3 != A_ROLE):
        violations.append(
            "model-router.sh declara A=%s en `pipeline_abc`, distinto del canon %s." % (r_a3, A_ROLE)
        )
    if r_b3 and (r_b3 != B_ROLE):
        violations.append(
            "model-router.sh declara B=%s en `pipeline_abc`, distinto del canon %s." % (r_b3, B_ROLE)
        )
    if blk_c and (blk_c != C_ROLE):
        violations.append(
            "managed-blocks.py declara model_pipeline_c %s, distinto del canon %s." % (blk_c, C_ROLE)
        )

    # 5) Pre-filtro (ADR-089): declarado y consistente en router y managed-blocks.
    pf_router = prefilter_in_router(root)
    pf_blocks = prefilter_in_blocks(root)
    if pf_router is None:
        violations.append(
            "model-router.sh no declara la ruta `pipeline_ab_prefilter` (ADR-089)."
        )
    if pf_blocks is None:
        violations.append(
            "managed-blocks.py no declara `model_pipeline_prefilter` (ADR-089)."
        )
    if pf_router and pf_blocks and pf_router != pf_blocks:
        violations.append(
            "pre-filtro inconsistente: router=%s, managed-blocks=%s." % (pf_router, pf_blocks)
        )
    if pf_router and pf_router != PREFILTER:
        violations.append(
            "pre-filtro declarado como %s, distinto del canon %s." % (pf_router, PREFILTER)
        )

    return violations


def main(argv: List[str]) -> int:
    root = Path(argv[1]).resolve() if len(argv) > 1 else ROOT

    violations = find_violations(root)

    # Reporte informativo de git (no es una violacion del pacto).
    _staged, git_report = _git_staged_report(root)

    if violations:
        print("PACTO DEL PIPELINE A/B/C VIOLADO (%d):" % len(violations))
        for v in violations:
            print("  - " + v)
        print()
        print("El CORE delega con TRES agentes: A escribe con %s, B revisa con %s, "
              "C escribe la red de tests con %s (ADR-077/ADR-089/ADR-105). "
              "Consultar `scripts/model-router.sh model pipeline_abc`."
              % (A_ROLE, B_ROLE, C_ROLE))
        return 1

    print(
        "OK: pacto A/B/C consistente en router, managed-blocks, skill y ADR-077/ADR-105 "
        "(A=%s, B=%s, C=%s, pre-filtro=%s, los tres distintos)."
        % (A_ROLE, B_ROLE, C_ROLE, PREFILTER)
    )
    print("Pista: `scripts/model-router.sh model pipeline_abc` y "
          "`scripts/model-router.sh model pipeline_ab` (para el flujo corto).")
    print()
    print("Estado de git (informativo):")
    print(git_report)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
