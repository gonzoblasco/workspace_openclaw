#!/usr/bin/env python3
"""Guard de roadmaps de rol (docs/ROADMAPS.md, 2026-10-07).

Por que existe: el 2026-10-07 se descubrio que 5 de 7 roles del ecosistema NO
tenian ROADMAP.md y nada lo detectaba. Una regla sin guarda se viola sola
(ADR-083). Este guard convierte "cada rol tiene su mapa de madurez" en algo
verificable: existencia, forma y coherencia de version.

Que verifica, por cada rol listado en REQUIRED_ROLES:
  1. EXISTENCIA  - agents/<rol>/ROADMAP.md existe.
  2. ENCABEZADO  - declara la version actual con el formato del estandar.
  3. SECCIONES   - tiene al menos MIN_SECTIONS secciones '## ' (las 7 del
                   estandar; se tolera que el encabezado no sea '## ').
  4. MARCADOR    - cierra con la linea de proyecto del workspace.
  5. COHERENCIA  - la version declarada coincide con la fila del rol en la
                   tabla "El mapa de madurez" de docs/ROADMAPS.md, Y con la
                   fila del rol en docs/roadmap-tracking.json (la tabla de
                   seguimiento que el CI nombra). Si cualquiera de las tres
                   vistas no dicen lo mismo, hay drift.

Uso:
  python3 scripts/check-roadmaps.py            # reporte legible, exit 1 si falla
  python3 scripts/check-roadmaps.py --quiet    # solo exit code
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

ROADMAPS_INDEX = REPO / "docs" / "ROADMAPS.md"
TRACKING_INDEX = REPO / "docs" / "roadmap-tracking.json"

# Roles del ecosistema que DEBEN tener roadmap de rol. Kanam CORE (main) tiene
# el suyo a nivel de sistema (docs/ROADMAP.md), no de rol; el agente bundled
# `openclaw` queda fuera de alcance. Actualizar esta lista cuando se sume un rol.
REQUIRED_ROLES = [
    "kanam-auditor",
    "kanam-critic",
    "kanam-dev",
    "kanam-mind",
    "kanam-ops",
    "kanam-planner",
    "kanam-studio",
]

MIN_SECTIONS = 6  # las 7 del estandar, con tolerancia a que la 1 (encabezado) no sea '## '

VERSION_RE = re.compile(r"Versi[oó]n actual:?\**\s*\**\s*(v?\d+\.\d+)", re.IGNORECASE)
PROJECT_MARKER = "<!-- project: github.com/gonzoblasco/workspace_openclaw -->"


def version_in(text: str) -> str | None:
    m = VERSION_RE.search(text)
    return m.group(1) if m else None


def index_versions(index_text: str) -> dict[str, str]:
    """Extrae {rol: version} de las filas de la tabla del mapa de madurez.

    Las filas tienen la forma:
      | **kanam-dev** (...) | ... | v0.1 | ... |
    Devuelve solo las filas cuyo nombre de rol aparece en negrita.
    """
    found: dict[str, str] = {}
    for line in index_text.splitlines():
        # fila de rol: contiene '**kanam-<algo>**'
        m_role = re.search(r"\*\*(kanam-[a-z]+)\*\*", line)
        if not m_role:
            continue
        role = m_role.group(1)
        # la primera version 'vX.Y' de la fila es la declarada
        m_ver = re.search(r"\bv?\d+\.\d+\b", line.split("|")[-3] if line.count("|") >= 3 else line)
        if not m_ver:
            m_ver = re.search(r"\bv?0\.\d+\b", line)
        if m_ver:
            found[role] = m_ver.group(0).lstrip("v")
    return found


def tracking_versions() -> dict[str, str]:
    """{rol: version} desde docs/roadmap-tracking.json (la tabla de seguimiento).

    El CI nombra este archivo como la tabla de seguimiento que el guard verifica.
    Hasta el 2026-10-12 el guard no lo leia: verificaba solo contra la tabla de
    docs/ROADMAPS.md, asi que el .json podia derivar en silencio (y derivo: decia
    v0.1 para kanam-critic cuando la realidad ya era v0.2). Leerlo cierra la
    promesa del comentario del CI y la brecha de la segunda verdad.
    """
    if not TRACKING_INDEX.exists():
        return {}
    try:
        data = json.loads(TRACKING_INDEX.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}
    out: dict[str, str] = {}
    for role, meta in data.items():
        if isinstance(meta, dict) and "version" in meta:
            out[role] = str(meta["version"]).lstrip("v")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    ok = True
    lines: list[str] = []

    index_text = ROADMAPS_INDEX.read_text(encoding="utf-8") if ROADMAPS_INDEX.exists() else ""
    if not ROADMAPS_INDEX.exists():
        ok = False
        lines.append(f"FALTA el indice {ROADMAPS_INDEX.relative_to(REPO)}")
    idx = index_versions(index_text)

    tver = tracking_versions()
    if not TRACKING_INDEX.exists():
        ok = False
        lines.append(f"FALTA la tabla de seguimiento {TRACKING_INDEX.relative_to(REPO)}")
    elif not tver:
        ok = False
        lines.append(f"la tabla de seguimiento {TRACKING_INDEX.relative_to(REPO)} no parsea")

    for role in REQUIRED_ROLES:
        path = REPO / "agents" / role / "ROADMAP.md"
        rel = path.relative_to(REPO)
        if not path.exists():
            ok = False
            lines.append(f"❌ {role}: no existe {rel}")
            continue

        text = path.read_text(encoding="utf-8")
        problems: list[str] = []

        ver = version_in(text)
        if not ver:
            problems.append("sin linea 'Version actual' con formato del estandar")

        if text.count("\n## ") + (1 if text.startswith("## ") else 0) < MIN_SECTIONS:
            problems.append(f"menos de {MIN_SECTIONS} secciones '## '")

        if PROJECT_MARKER not in text:
            problems.append("sin marcador de proyecto")

        if ver:
            v_norm = ver.lstrip("v")
            idx_ver = idx.get(role)
            if idx_ver and idx_ver != v_norm:
                problems.append(
                    f"drift de version: archivo dice v{v_norm}, indice dice v{idx_ver}"
                )
            t_ver = tver.get(role)
            if t_ver and t_ver != v_norm:
                problems.append(
                    f"drift vs tabla de seguimiento: archivo dice v{v_norm}, "
                    f"roadmap-tracking.json dice v{t_ver}"
                )

        if problems:
            ok = False
            lines.append(f"❌ {role}: " + "; ".join(problems))
        else:
            lines.append(f"✅ {role}: v{ver.lstrip('v')}")

    if not args.quiet:
        print("Guard de roadmaps de rol (docs/ROADMAPS.md)")
        for ln in lines:
            print("  " + ln)
        print(f"  {len(REQUIRED_ROLES) - sum(1 for l in lines if l.startswith('❌'))}/{len(REQUIRED_ROLES)} roles OK")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
