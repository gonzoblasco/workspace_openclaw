# project-closure

> Cierra un proyecto de forma completa e inmortaliza su conocimiento en ADR + DB + skill.

## Propósito

Cuando un proyecto queda terminado, no basta con un commit. Hay que **capturar la decisión, el aprendizaje y el estado** en los tres lugares donde persiste la memoria institucional: un ADR (decisión), la base de datos (sessions + learnings), y la documentación de la skill asociada. Todo reproducible con un script.

## Cuándo usarla

- Gonzo dice "cerremos el proyecto", "documentemos X", "que quede immortlizado".
- Un proyecto alcanza su criterio de éxito y no habrá más iteración.
- Una serie de sesiones cierra un ciclo (ej. un sistema nuevo).

**Importante:** "cerrar proyecto" ≠ "separarse del workspace". Es documentar el trabajo de forma durable, no abandonar la relación de trabajo. El conocimiento queda accesible para futuras sesiones.

## Workflow de cierre

```
Proyecto terminado
    │
    ▼
┌─────────────────────────────────────────────┐
│ 1. Identificar qué se cierra y su alcance    │
│    (¿es un proyecto? ¿un sistema? ¿una fase?)│
└─────────────────┬───────────────────────────┘
                  │
    ┌─────────────▼─────────────┐
    │ 2. Escribir el ADR        │  docs/adr/ADR-XXX-<slug>.md
    │    (decisión + racional + │  Formato: Status/Decision/Consecuencias/Alternativas
    │    validación)            │
    └─────────────┬─────────────┘
                  │
    ┌─────────────▼─────────────┐
    │ 3. Registrar en DB        │  memory.db:
    │    - daily_notes (summary)│  sessions_relacional (T-score, modelo, thinking)
    │    - sessions_relacional  │  learnings (si hay lección nueva)
    └─────────────┬─────────────┘
                  │
    ┌─────────────▼─────────────┐
    │ 4. Skill + script          │  skills/<slug>/SKILL.md
    │    para hacerlo reproducible│  + scripts/project-closure.sh
    └─────────────┬─────────────┘
                  │
    ┌─────────────▼─────────────┐
    │ 5. Commit + push + daily   │  workspace commit, mirror de skills, daily actualizado
    └───────────────────────────┘
```

## Step-by-step

### 1. Identificar el cierre

Antes de escribir nada, **clarificar el alcance** con Gonzo:
- ¿Se cierra el proyecto completo o solo una fase/sistema?
- ¿Cuál es la decisión más importante que quedar documentada?

**No asumir:** un "cierre" puede ser existencial (todo el workspace) o puntual (un sistema). Confirmar antes de gastar esfuerzo.

### 2. Escribir el ADR

Numero el próximo ADR (`ls docs/adr/` y +1). Formato (ver `ADR-043` como ejemplo):
- **Status / Deciders / Fecha / Origen**
- **Contexto:** el problema que motivó la decisión.
- **Decision:** qué se decidió, conciso y accionable.
- **Implementación:** archivos y componentes.
- **Consecuencias:** positivas y limitaciones.
- **Alternativas:** qué se descartó y por qué.
- **Validación:** evidencia empírica de que la decisión es correcta.

### 3. Registrar en la DB

Usar Python + sqlite3 sobre `memory/memory.db`:

```sql
-- daily_notes: resumen del cierre (type='daily')
INSERT INTO daily_notes (date, type, content, source_file, created_at) VALUES (...);

-- sessions_relacional: con complexity score si aplica
INSERT INTO sessions_relacional (date, title, tags, complexity_score, model_used,
  thinking_level, summary, content_bare, created_at) VALUES (...);

-- learnings: si hay una lección nueva y durable
INSERT INTO learnings (category, title, content, tags, created_at, updated_at) VALUES (...);
```

### 4. Crear skill + script de cierre

La skill documenta el workflow (este archivo). El script automatiza:

```bash
./scripts/project-closure.sh --name "<slug>" --title "<título>" \
  --summary "<resumen>" --complexity <T-score> --model "<modelo>" \
  --create-adr --tag "pipeline,cierre" [--learning]
```

Qué hace el script:
1. Crea el ADR con el template.
2. Registra en `daily_notes` + `sessions_relacional` (+ `learnings` opcional).
3. Devuelve el resumen para el daily markdown.

### 5. Commit final

- Commit del workspace con el ADR + script + skill.
- Mirror de skills (`rsync` a `.github/skills/`).
- Push con `--rebase`.

## Reglas clave

1. **ADR = decisión inmutable.** Lo documentado no se re-abre salvo evidencia nueva.
2. **Referencia ≠ proyecto.** Al des-trackear/limpiar, nunca borrar datos locales (`.env`, `*.db`, uploads). `git rm --cached` preserva el archivo en disco.
3. **Cierre ≠ abandono.** El conocimiento queda en ADR + DB para retomarlo. La relación de trabajo continúa.
4. **Confirmar alcance antes.** Un cierre existencial vs puntual son trabajos muy distintos.
5. **Todo reproducible.** El script `project-closure.sh` debe dejar el cierre repetible, no manual.

## Status

- Version: 1.0.0
- Created: 2026-08-31
- Depends on: `scripts/project-closure.sh`, `memory/memory.db`, `docs/adr/`
