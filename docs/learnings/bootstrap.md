# Learnings - bootstrap

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## El cap de bootstrap se mide en caracteres UTF-16, no en bytes

El runtime de OpenClaw trunca EN SILENCIO los archivos de bootstrap (AGENTS/MEMORY/USER/SOUL/IDENTITY) al superar su cap. Caps (OpenClaw 2026.9.8, dist/bootstrap-*.mjs): 20.000 por archivo, 4.000 fijo para USER.md, 60.000 total. Mide .length de JS = unidades UTF-16, NO bytes: wc -c sobreestima en espanol por los acentos y da un margen falso (USER.md: 3.976 bytes vs 3.933 real -> margen 24 vs 67). Gate: scripts/check-bootstrap-budget.py (pre-commit sin condicion + CI). Leccion de fondo: una regla de gobernanza sin guarda se viola sola (USER.md se habia arreglado el 14/09 y regreso a 4.582).

---

