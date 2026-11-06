#!/usr/bin/env python3
"""Regression net for skill-router catalog matching (step 2 of skill-router-improvement).

Exit 0 only if every case finds its expected skill within TOP_N (3).
Exit 1 otherwise. Prints a table per case."""

import importlib.util, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
MOD = os.path.join(HERE, "skill-router.py")
spec = importlib.util.spec_from_file_location("skill_router", MOD)
sr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sr)

TOP = 3

# (query, expected_skill_name, note)
CASES = [
    ("aplicar a una oferta de trabajo", "job-offer-veracity-check", "oferta real? veracidad"),
    ("verificar los claims del CV contra los hechos vigentes", "career-claim-provenance", "veracidad de claims"),
    ("es una oferta real o phishing", "job-offer-veracity-check", "veracidad de oferta"),
    ("escribir y probar una nueva feature", "spec-draft-creation", "specs"),
    ("verificar contraste de UI", "ui-contrast-audit", "a11y"),
    ("cargar un PDF y extraer texto", "pdf-tool", "pdf"),
    ("guardar sesion y memoria", "session-close-handoff", "session"),
    ("escribir un ADR", "adr-archiving", "docs"),
    ("revisar un PR de OSS", "pr-review-response", "pr review"),
    ("crear un proyecto nuevo", "project-root-placement", "proyectos"),
]

fail = 0
print(f"{'case'.ljust(46)} {'expected'.ljust(30)} {'rank'}")
print("-" * 86)
for q, exp, note in CASES:
    merged = sr.suggest(q, 10)
    names = [r[4]["name"] for r in merged]
    rank = names.index(exp) + 1 if exp in names else None
    top = names[:TOP]
    ok = rank is not None and rank <= TOP
    status = "OK" if ok else "FAIL"
    if not ok:
        fail += 1
    print(f"{status:4} {q.ljust(46)[:46]} {exp.ljust(30)} {rank if rank else '-'}   (top: {', '.join(names[:TOP])})")

print("-" * 86)
print(f"{len(CASES) - fail}/{len(CASES)} passed")
sys.exit(0 if fail == 0 else 1)
