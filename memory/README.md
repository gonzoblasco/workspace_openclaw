# memory/ - Mapa de la memoria

La memoria del workspace. **Fuente de verdad: `memory.db`** (SQLite); los `.md` son vistas legibles y notas curadas.

## Contrato del tooling (no mover, no renombrar)

| Ruta | Quien la espera ahi |
|---|---|
| `memory/<YYYY-MM-DD>.md` | `scripts/memory-end-session.py` (escribe), `scripts/memory-catalog-v2.py` (lee, solo `*.md` de la raiz, no recursivo) |
| `memory/memory.db` | Todos los scripts (`MEMORY_DB`) |
| `memory/todos.md`, `memory/inbox.md` | `scripts/memory-db.sh export-todos/export-inbox` (regeneran en la raiz) |
| `memory/archive/dailies/`, `memory/archive/sessions/` | skill `knowledge-management` (archivado) |

**El daily del dia vive en la raiz.** Los viejos se archivan (DB + `archive/dailies/`).

## Estructura

```
memory/
├── memory.db              # fuente de verdad (DB-first)
├── YYYY-MM-DD.md          # daily vigente (raiz por contrato)
├── todos.md  inbox.md     # vistas generadas desde la DB (raiz por contrato)
├── user-profile.md        # perfil de Gonzo (referenciado por USER.md)
├── user-interests.md      # intereses, para curaduria
│
├── archive/
│   ├── dailies/           # dailies consolidados (YYYY-MM-DD.md)
│   └── sessions/          # logs de sesion con hora (YYYY-MM-DD-HHMM.md)
├── handoffs/              # HANDOFF-YYYY-MM-DD-<tema>.md
├── notes/                 # notas tematicas (batallas, cata-k-esimo,
│                          #   portfolio-curation, novel-pitch, conversation_summary)
├── recipes/               # recetas
├── tech-notes/            # notas tecnicas sueltas
├── _templates/            # plantillas (YYYY-MM-DD.md)
├── dreaming/  .dreams/    # estado de dreaming (gitignored)
└── export/                # chunks derivados regenerables (gitignored)
```

## Convenciones de nombre

- **Dailies:** `YYYY-MM-DD.md` (uno por dia, en la raiz).
- **Logs de sesion:** `YYYY-MM-DD-HHMM.md` (automaticos de OpenClaw, gitignored). El sufijo `-N` de desempate tambien se ignora.
- **Handoffs:** `HANDOFF-YYYY-MM-DD-<tema>.md`.
- **Guion:** guion comun `-` siempre, nunca em dash.

## Regla de mantenimiento

Cuando llegue un archivo nuevo suelto a la raiz, va a la subcarpeta que le corresponde segun su tipo (handoff, nota, receta, sesion). La raiz queda solo con lo que el tooling espera ahi.
