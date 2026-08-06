---
name: "release-management"
metadata:
  category: "Workflow"
  tags:
    - release
    - deploy
    - versionado
description: "Workflow de Release Management: planificación, coordinación y ejecución de releases hacia producción. Gestiona estrategias de despliegue, versionado, comunicación y rollback."
user-invocable: false
---

# Workflow: Release Management

## Propósito

Coordinar la liberación de nuevas versiones hacia producción de forma segura, predecible y repetible.

No valida calidad.

Eso pertenece a `pre-deploy-qa`.

No desarrolla features.

No corrige bugs.

Su responsabilidad comienza cuando el software ya está listo para ser liberado.

---

# Filosofía

> Shipping is a business decision, not a Git command.

Una release no es un deploy.

Una release es poner una capacidad nueva en manos de los usuarios.

---

# Relación con otros workflows

Antes

↓

review-quality

↓

pre-deploy-qa

↓

release-management

↓

observability

↓

incident-response (si ocurre)

---

# Cuándo usarlo

- release a producción
- release interna
- beta
- canary
- hotfix
- rollback
- milestone importante

---

# Estrategias de Release

Ver [estrategias de release](./references/strategies.md).

---

# Fases

## 1. Release Planning

Definir:

Versión

Objetivo

Scope

Features incluidas

Features excluidas

Riesgos

Rollback plan

---

## 2. Readiness Review

Verificar:

QA aprobado

Build estable

Tests verdes

Documentación actualizada

CHANGELOG listo

ADRs sincronizados

No continuar si falta alguno.

---

## 3. Versioning

Aplicar SemVer.

Major

Minor

Patch

Crear tag.

Verificar consistencia.

---

## 4. Deployment Strategy

Elegir estrategia.

Responder:

¿Canary?

¿Blue/Green?

¿Rolling?

¿Feature Flags?

¿Release completa?

Justificar decisión.

---

## 5. Communication

Preparar:

Release Notes

Cambios visibles

Breaking Changes

Migraciones necesarias

Stakeholders afectados

Soporte

---

## 6. Release Execution

Coordinar:

Deploy

Monitoreo

Validaciones rápidas

Smoke Tests

No modificar código durante esta fase.

---

## 7. Post Release Verification

Verificar:

Métricas

Errores

Latencia

Logs

Health Checks

Feedback temprano

No cerrar la release inmediatamente.

---

## 8. Release Closure

Actualizar:

CHANGELOG

STATUS

Versiones

Release Notes

Lecciones aprendidas

Cerrar release.

---

# Outputs

RELEASE_PLAN.md

RELEASE_NOTES.md

Release Checklist

Rollback Plan

Tag SemVer

Release Report

---

# Helper Scripts

Scripts en `skills/release-management/scripts/`:

| Script | Uso |
|---|---|
| `release-check.sh --version <semver>` | Verifica build, tests, CHANGELOG con version, tag no existente, y sin cambios sin commitear. Usar en la fase 2 (Readiness Review). |
| `update-changelog.sh` | Inserta una entrada `[Unreleased]` en CHANGELOG.md. Usar cuando se cierra un epic o feature. |
| `generate-release-notes.sh` | Genera notas de release desde commits/tags. Usar en la fase 5 (Communication). |

Tambien ver [close-epic.sh](../task-execution/scripts/close-epic.sh) en Task Execution para cerrar epics con tag y STATUS.

---

# Checklist

Ver [release checklist](./references/checklist.md).

---

# Decisiones

Puede:

✔ recomendar estrategia

✔ generar release notes

✔ preparar rollback

✔ coordinar checklist

✔ generar plan

Nunca:

✖ saltar QA

✖ desplegar sin rollback

✖ ignorar métricas

✖ modificar código

---

# Integración

Si la release falla

↓

incident-response

Si aparecen métricas preocupantes

↓

observability

Si la release termina correctamente

↓

session-lifecycle

↓

engineering-governance (en retrospectivas importantes)

---

# Principios

Releases pequeñas son más seguras que releases enormes.

Cada release debe poder revertirse.

La comunicación es parte de la release.

El deploy termina cuando el sistema está estable, no cuando termina el pipeline.

Cada release debe dejar evidencia suficiente para reconstruir qué cambió y por qué.

## Related Skills

- [Dependency Management](../dependency-management): Para gestionar dependencias en la release
- [Task Execution](../task-execution): Para implementar features incluidas en la release