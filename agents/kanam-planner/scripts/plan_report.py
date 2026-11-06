#!/usr/bin/env python3
"""Reporte de programas y alertas.

Wrapper del comando `report` de program_plan.py.
"""

import os
import sys
from pathlib import Path

SCRIPT = Path(__file__).with_name("program_plan.py")
os.execv(sys.executable, [sys.executable, str(SCRIPT), "report", *sys.argv[1:]])
