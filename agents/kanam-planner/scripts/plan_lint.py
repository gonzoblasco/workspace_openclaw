#!/usr/bin/env python3
"""Gate de validacion de planes de programa.

Wrapper del comando `lint` de program_plan.py para que el CORE pueda correr
`plan_lint.py` sin recordar la subcomanda.
"""

import os
import sys
from pathlib import Path

SCRIPT = Path(__file__).with_name("program_plan.py")
os.execv(sys.executable, [sys.executable, str(SCRIPT), "lint", *sys.argv[1:]])
