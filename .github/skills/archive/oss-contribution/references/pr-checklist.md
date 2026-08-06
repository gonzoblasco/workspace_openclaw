# PR Checklist — OSS Contribution Reference

Checklist para PRs a repositorios externos.

## Pre-PR

- [ ] Fork creado desde el repo original (no clonar directo)
- [ ] Branch con nombre descriptivo: `fix/issue-123`, `feat/add-x`
- [ ] Upstream configurado: `git remote add upstream <original-url>`
- [ ] Sin cambios de formato/whitespace no relacionados
- [ ] Sin cambios a archivos no relacionados
- [ ] Commits firmados con SSH
- [ ] Sin trazas de automatización en commits (repos Tier 0)

## PR Description

```markdown
## Description

[Clear, human description of what this PR does and why]

## Related Issue

Closes #123

## Testing

- [ ] Added tests
- [ ] Existing tests pass
- [ ] Manual testing done

## Screenshots (if applicable)

[Only if UI changes]
```

## Post-PR

- [ ] Responder a comments de maintainers dentro de 24h
- [ ] Si piden cambios, hacerlos rápido
- [ ] Si el PR se cierra, aprender y seguir
- [ ] Actualizar CONTRIBUTING.md si el PR se mergea

## PR Description Tone

| Repo Tier | Tone |
|---|---|
| **Tier 0** | Natural, humano, sin automatización visible |
| **Tier 1** | Profesional pero relajado |
| **Tier 2** | Cualquiera, es nuestro repo |

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Tier Ranking](./tier-ranking.md) — Clasificación de repos
- [Community Guidelines](./community-guidelines.md) — Reglas de interacción
