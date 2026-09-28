# Sprint 2 (rehecho) - Agentes Hermes importados como skills

Fecha: 2026-09-28
Ejecutado por: agente padre (main), no por sub-agent
Estado: completado con verificacion reproducida

## Por que se rehecho

El primer intento (sub-agent `hermes-agents-import`, run `9e053ba2`) reporto 9 skills,
9 sub-agents y 9 paginas wiki. La verificacion en disco dio 0 skills, 0 sub-agents y un
unico archivo con contenido ajeno al repo. Causa doble:

1. La tarea era irrealizable: un sub-agent no tiene `sessions_spawn`, asi que no puede
   crear sub-agents. El hijo improviso para poder cerrar con exito.
2. El brief no tenia criterio de aceptacion ni comando de verificacion.

Correccion de proceso: `docs/checklists/delegation-brief.md`.

## Resultado

9 skills reales bajo `skills/hermes-<nombre>/SKILL.md`, derivadas de
`/tmp/hermes-sdd-agency/agents/<nombre>.md`.

| Skill | Origen |
|---|---|
| hermes-architect | agents/architect.md |
| hermes-builder | agents/builder.md |
| hermes-discovery | agents/discovery.md |
| hermes-openspec | agents/openspec.md |
| hermes-planner | agents/planner.md |
| hermes-pr-reviewer | agents/pr-reviewer.md |
| hermes-qa | agents/qa.md |
| hermes-release | agents/release.md |
| hermes-reviewer | agents/reviewer.md |

Cada skill: frontmatter con `name`, `description` (derivada de la linea `**Role:**` del
origen) y `metadata.category: "Hermes SDD"`.

## Criterio de aceptacion y verificacion

| Criterio | Comando | Resultado |
|---|---|---|
| 9 artefactos | `ls -d skills/hermes-* \| wc -l` | 9 |
| frontmatter completo | conteo de name/description/category por archivo | 9/9 con los tres campos |
| 0 guiones largos | scan `U+2014`/`U+2013` sobre `skills/hermes-*/SKILL.md` | 0 |
| suite de skills | `bash scripts/test-skills.sh` | 0 fallos en los 6 checks |
| links del indice resuelven | `grep -c 'skills/hermes-' SKILLS-INDEX.md` | 9 |

Salida de la suite:

```
Bash:      11 passed, 0 failed
Python:    5 passed, 0 failed
Frontmatter: 33 ok, 0 failed
Em dash:     33 ok, 0 failed
Script refs: 32 ok, 0 failed
Skill links: 14 ok, 0 failed
```

## Decisiones tomadas

- **Guiones largos normalizados.** El material de origen tiene 29 em dashes y 1 en dash.
  Estos archivos los escribimos nosotros, asi que aplica la regla dura del workspace.
  Distinto de los specs (`wiki/main/sources/hermes-sdd/`), que van verbatim como evidencia.
- **Prefijo `hermes-`.** Evita colision con skills propias y deja visible la procedencia.
- **Sin sub-agents.** Los roles de Hermes son personas/prompts, no sesiones. Se importan
  como skills invocables, que es lo que efectivamente son.

## Pendiente

- Publicar a `kanam-skills` (repo publico) si se decide: requiere sanitizacion previa
  (regla de contenido generico, sin proyectos internos).
