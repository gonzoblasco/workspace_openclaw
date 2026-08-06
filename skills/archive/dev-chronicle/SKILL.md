---
name: "dev-chronicle"
description: "Narrativas de trabajo dev desde git, sesiones y memoria"
---

# dev-chronicle

## Descripción
Genera narrativas en prosa del trabajo del developer leyendo git history, session transcripts de OpenClaw y memory files. Formatos: daily chronicles, weekly rollups, standups, portfolio write-ups. Enfocado en decisiones y approaches rechazados, no solo tareas completadas.

## Cuándo usarlo
- Para escribir standup notes a partir de commits del día anterior
- Para revisar cambios de dirección y pivotes de la semana
- Para generar un case study de portfolio a partir de un proyecto terminado
- Para capturar qué se descartó o rechazó durante un día de trabajo
- Para resumir un sprint para una update de equipo

## Workflow
1. Especificar el período (día, semana, sprint, proyecto completo)
2. Especificar el formato (daily, weekly, standup, portfolio)
3. Ejecutar dev-chronicle
4. Revisar la narrativa generada
5. Publicar o archivar según corresponda

## Tooling relacionado

| Skill / Script | Uso |
|---|---|
| `release-management/scripts/generate-release-notes.sh` | Genera notas de release desde commits/tags. Usar para portfolio write-ups y sprints. |
| `tech-docs/scripts/update-changelog.sh` | Inserta `[Unreleased]` en CHANGELOG.md. Usar cuando la narrativa derive en un release. |
| `session-lifecycle/scripts/session-end.sh` | Genera cierre de sesión que alimenta las daily chronicles. |
| `github/scripts/pr-batch-check.sh` | Lista PRs abiertos/mergeados para enriquecer el contexto. |

## Notas
- Sintetiza git history + session transcripts + memory files
- No requiere API keys externas
- El foco en decisiones y approaches rechazados es valioso para retrospectivas
