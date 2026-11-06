#!/usr/bin/env python3
"""Wrapper local del session_plan.py del workspace principal.

El Planner tiene su propio `.knowledge/` y su propio plan de rol. El script
real vive una sola vez en el workspace principal; este wrapper solo fija
`SESSION_PLAN_PATH` al estado del rol y delega, para no duplicar la fuente
de verdad ni mezclar el plan del CORE con el del Planner.
"""

import os
import sys
from pathlib import Path

ROLE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROLE_ROOT.parents[1]
MAIN_SCRIPT = WORKSPACE / "scripts" / "session_plan.py"

os.environ.setdefault(
    "SESSION_PLAN_PATH",
    str(ROLE_ROOT / ".knowledge" / "session_plan.json"),
)

if not MAIN_SCRIPT.exists():
    raise SystemExit(f"No encuentro el script principal: {MAIN_SCRIPT}")

os.execv(sys.executable, [sys.executable, str(MAIN_SCRIPT), *sys.argv[1:]])
