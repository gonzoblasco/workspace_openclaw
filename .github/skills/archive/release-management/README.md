# Release Management

Coordinación de releases a producción.

## ¿Para qué sirve?

Para **coordinar la liberación de nuevas versiones** a producción de forma segura, predecible y repetible. No valida calidad (eso es pre-deploy-qa), no desarrolla features. Su responsabilidad empieza cuando el software ya está listo para ser liberado.

**Filosofía:** Shipping is a business decision, not a Git command.

## ¿Cuándo usarlo?

- Release a producción
- Beta o canary
- Hotfix
- Rollback
- Milestone importante

## ¿Cómo se usa?

### Workflow completo

1. **Release Planning** — versión, objetivo, scope, riesgos, rollback plan
2. **Readiness Review** — QA aprobado, build estable, tests verdes, CHANGELOG listo
3. **Versioning** — SemVer, crear tag
4. **Deployment Strategy** — canary, blue/green, rolling, feature flags
5. **Communication** — release notes, breaking changes, stakeholders
6. **Release Execution** — deploy, monitoreo, smoke tests
7. **Post Release Verification** — métricas, errores, latencia, logs
8. **Release Closure** — CHANGELOG, STATUS, lessons learned

### Scripts útiles

```bash
# Generar release notes
./scripts/generate-release-notes.sh --version 1.2.0 --name "Auth overhaul"

# Verificar readiness
./scripts/release-check.sh --version 1.2.0
```

## Referencias

| Archivo | Qué contiene |
|---|---|
| `references/strategies.md` | Estrategias de release |
| `references/checklist.md` | Release checklist |
| `references/release-communication.md` | Templates: release notes, rollback plan |

## Skills relacionadas

- [Dependency Management](../dependency-management) — Para gestionar dependencias en la release
- [Task Execution](../task-execution) — Para implementar features incluidas en la release
