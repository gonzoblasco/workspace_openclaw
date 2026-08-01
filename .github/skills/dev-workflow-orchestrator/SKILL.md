---
name: "dev-workflow-orchestrator"
description: "Orquestador de pipelines de desarrollo estandarizados multi-workflow"
---

# dev-workflow-orchestrator

## Descripción
Orquestador que define y ejecuta pipelines de desarrollo estandarizados. No reemplaza las skills individuales, las orquesta en el orden correcto con handoffs explícitos. 7 workflows predefinidos.

## Workflows

### 1. New Feature (Full)
```
User → (@researcher)* → @architect → @builder → [@validator + @tester] (PARALLEL) → @scribe
```

### 2. Bug Fix (Quick)
```
User → @builder → [@validator + @tester] (PARALLEL) → done
```

### 3. API Change (Critical)
```
User → (@researcher)* → @architect → @api-guardian → @builder → [@validator + @tester] (PARALLEL) → @scribe
```

### 4. Refactoring
```
User → @architect → @builder → [@validator + @tester] (PARALLEL) → done
```

### 5. Release
```
User → @scribe → @github-manager
```

### 6. Process Issue
```
User → @github-manager (loads issue) → Orchestrator (analyzes) → Appropriate workflow
```

### 7. Research
```
User → @researcher → Report
```

## Handoff Matrix
| Agent | Receives from | Passes to |
|-------|---------------|-----------|
| @researcher | User/Orchestrator | @architect |
| @architect | User/@researcher | @api-guardian or @builder |
| @api-guardian | @architect | @builder |
| @builder | @architect/@api-guardian | @validator AND @tester (PARALLEL) |
| @validator | @builder | SYNC POINT |
| @tester | @builder | SYNC POINT |
| @scribe | Both gates approved | @github-manager (for release) |

## 10 Golden Rules
1. **Version-First** — Determinar versión target ANTES de empezar
2. **@researcher for Unknown Tech** — Investigar tecnologías nuevas antes de decidir
3. **@architect is the Gate** — No feature sin decisión de arquitectura
4. **@api-guardian MANDATORY for API changes** — Sin excepciones
5. **Dual Quality Gates** — @validator AND @tester deben pasar
6. **No Skipping** — Cada agente en el workflow debe ejecutarse
7. **Reports versionados** — Todos los reportes bajo reports/v[X.X.X]/
8. **Nunca pushear sin permiso** — Aplica a TODOS los agentes
9. **CHANGELOG antes del push** — Siempre actualizar
10. **Decisiones documentadas** — Cada trade-off debe registrarse

## Notas
- Orquesta skills existentes, no las reemplaza
- Handoffs explícitos eliminan ambigüedad
- Quality gates paralelos para velocidad
