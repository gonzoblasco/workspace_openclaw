# Release Checklist — Referencia

## Antes de la Release

### QA y Calidad
- [ ] QA aprobado
- [ ] Build estable (CI verde)
- [ ] Tests unitarios pasan
- [ ] Tests de integración pasan
- [ ] Tests E2E pasan (si aplica)
- [ ] Sin vulnerabilidades críticas abiertas

### Documentación
- [ ] CHANGELOG actualizado con cambios visibles
- [ ] ADRs sincronizados (si hubo cambios arquitectónicos)
- [ ] Release Notes preparadas
- [ ] Documentación de migración lista (si aplica)

### Técnico
- [ ] Version SemVer definido
- [ ] Tag creado
- [ ] Rollback plan documentado
- [ ] Feature flags verificados (si aplica)
- [ ] Dependencias actualizadas y compatibles

## Durante la Release

- [ ] Deploy iniciado
- [ ] Smoke tests pasan post-deploy
- [ ] Health checks verdes
- [ ] Métricas baseline estables
- [ ] Alertas sin disparos anormales

## Después de la Release

- [ ] Monitoreo activo por 30 min mínimo
- [ ] Feedback de early adopters (si aplica)
- [ ] CHANGELOG finalizado con fecha de release
- [ ] Release Notes publicadas
- [ ] Lecciones aprendidas registradas
- [ ] Release cerrada en tracker

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Strategies](./strategies.md) — Estrategias de release
