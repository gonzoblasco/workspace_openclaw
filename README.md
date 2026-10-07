# README.md - Workspace de Kanam

> Repo **privado**. Es el punto de entrada del workspace: un **router**, no una copia.
> Cuando algo cambia, se cambia en su fuente; acá solo se apunta. Si un dato se repite
> de otro archivo, nace desincronizado (ya pasó con `AGENTS.md` y con el mirror `.github/skills/`).

## Qué es esto

Workspace de trabajo de Kanam sobre OpenClaw, que vive **solo en la Mac Mini** (desde la migración a arquitectura multi-agente, ADR-073). No es una superficie pública ni un producto: es el espacio de trabajo, la memoria y las decisiones de la colaboración entre Gonzo y Kanam.

## Puntos de entrada (empezá por acá)

| Si necesitás... | Andá a | Qué es |
|---|---|---|
| Cómo se comporta el agente | [`AGENTS.md`](./AGENTS.md) | Reglas de conducta (no personalidad) |
| Detalle ampliado de esas reglas | [`docs/AGENTS-DETALLE.md`](./docs/AGENTS-DETALLE.md) | OSS, pipeline, triple git, sanitización, cleanup, verify-before-push |
| Entorno, máquinas, modelos, scripts | [`docs/SETUP.md`](./docs/SETUP.md) | Cheat sheet de entorno |
| Personalidad y voz | [`SOUL.md`](./SOUL.md), [`IDENTITY.md`](./IDENTITY.md) | Principios y quién es Kanam |
| Perfil de Gonzo | [`USER.md`](./USER.md) | Preferencias y reglas de interacción |
| Memoria de largo plazo | [`MEMORY.md`](./MEMORY.md) | Memorias curadas (solo main session) |
| Mapa y contrato de la memoria | [`memory/README.md`](./memory/README.md) | Estructura de `memory/`, retención, tooling |
| Decisiones de arquitectura | [`docs/adr/`](./docs/adr/) | ADRs aceptados (86 archivos) |
| Skills disponibles | [`SKILLS-INDEX.md`](./SKILLS-INDEX.md) | Índice de las 78 skills activas |
| Contribuir a OSS | [`CONTRIBUTING.md`](./CONTRIBUTING.md) | Estrategia y reglas de PRs |
| Cambios estructurales | [`CHANGELOG.md`](./CHANGELOG.md) | Registro histórico del workspace |
| Registros de sesión (historia) | [`docs/records/`](./docs/records/) | Fotos inmutables de sesiones pasadas (ADR-084), no documentación viva |
| Trabajo en curso y próximo | [`docs/ROADMAP.md`](./docs/ROADMAP.md), [`memory/todos.md`](./memory/todos.md) | Roadmap (capas + la ruta) y pendientes |
| Operación del gateway | [`docs/gateway-operations.md`](./docs/gateway-operations.md) | Servicios y rutinas del gateway |

## Mapa de nivel 1

| Ruta | Qué es |
|---|---|
| [`agents/`](./agents/) | Los 4 roles de agente (dev, mind, ops, studio), cada uno con su `AGENTS.md`, identidad, skills y plantillas |
| [`skills/`](./skills/) | Skills activas del workspace (36) |
| [`docs/`](./docs/) | Documentación: ADRs, arquitectura, checklists, entrevistas, linkedin, pipeline, stories, cpacc, records, entre otras |
| [`memory/`](./memory/) | Memoria: `memory.db` (fuente de verdad) + vistas `.md` + archivo |
| [`scripts/`](./scripts/) | Tooling del workspace (memoria, refs, ADRs, pipeline, gateway) |
| [`studies/`](./studies/) | Estudios internos (p. ej. narrative-engineering) |
| [`design/`](./design/) | Tokens y assets de diseño |
| [`media/`](./media/) | Media de entrada de sesiones |
| [`prompts/`](./prompts/), [`tests/`](./tests/) | Prompts y suites de test (bash, node, python) |
| `sandbox/` | Pruebas temporales aisladas (gitignored) |

### Carpetas invisibles

| Ruta | Qué es |
|---|---|
| [`.knowledge/`](./.knowledge/) | Conocimiento de sesión del workspace: `BRIEF.md`, `STATUS.md`, `HANDOFF.md`, catálogo de skills |
| [`.openclaw/`](./.openclaw/) | Superficies de discovery del gateway (`portals.json`) |
| `.data/`, `.clawhub/` | Estado local del tooling (gitignored) |
| `.github/` | CI (`skills-ci.yml`) |

## Contexto de bootstrap

OpenClaw carga un subconjunto de archivos como *Project Context* en cada arranque, con caps fijos: `USER.md` a 4.000 chars y `AGENTS.md` a 20.000. Por eso `AGENTS.md` empuja el detalle a `docs/AGENTS-DETALLE.md` y el entorno a `docs/SETUP.md`: no es duplicación, es recorte por presupuesto de contexto. Los subagentes reciben `AGENTS.md`, no `MEMORY.md`.

## Contrato del worktree

- **No se versiona:** `.env` y variantes, tokens, `*.db` (excepto `memory/memory.db`), `node_modules/`, memoria cruda de sesión, estado local de dreaming.
- **Los proyectos viven en `~/projects/`** (fuera de este worktree): ver [`docs/adr/ADR-075-proyectos-viven-en-home-projects.md`](./docs/adr/ADR-075-proyectos-viven-en-home-projects.md). El workspace ya no es responsable de la memoria de proyecto.
- Un gitlink o submodule es **solo un puntero**: quitar la referencia nunca borra datos locales.

## Flujo de trabajo

- **Commits atómicos**, en inglés, formato `type(#issue): descripcion`.
- **`git pull --rebase` antes de cada push.**
- **Esperar el CI** y que todos los checks pasen antes de dar algo por cerrado.
- **Pre-commit hooks:** enforcer de guion, `check-refs.py` (rutas y links vivos), `check-adr-integrity.py`. Omitir con `SKIP_SIMPLE_GIT_HOOKS=1`.
- **Docs vivas:** CHANGELOG para cambios estructurales, daily en `memory/`, handoffs en `memory/handoffs/`.

## Máquinas

- **Una sola máquina activa: la Mac Mini.** Corre el gateway 24/7. El workspace vive acá y no se sincroniza con otra computadora (ADR-073).
- La MacBook Air quedó **fuera del flujo**; si alguna vez se la reconecta, ver ADR-085.

## Mantenimiento

```bash
python3 scripts/check-refs.py --all      # rutas y links citados en los docs
python3 scripts/check-adr-integrity.py   # corpus de ADRs vs indice
./scripts/test-skills.sh                 # integridad de las skills
```

Todos corren también en el pre-commit. Si agregás un doc de entrada con links, sumalo a `DEFAULTS` en [`scripts/check-refs.py`](./scripts/check-refs.py): un doc que nadie escanea se rompe en silencio.

---

_Última revisión: 2026-09-29._
