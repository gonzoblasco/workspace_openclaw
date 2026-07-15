# ROADMAP.md — Kanam Workflow Kit

> Phase 3 — Product Roadmap
> Fecha: 2026-07-15

## Phase breakdown

### Phase 1: Refinar skills existentes — ~1 día
- **Goal:** Todos los skills con frontmatter YAML estándar, documentación clara, sin errores
- **Deliverable:** 11 skills pulidos y consistentes
- **Tasks:**
  1. Agregar frontmatter YAML a todos los skills (name, description, version)
  2. Revisar que todos tengan: Propósito, Precondiciones, Pasos, Validación
  3. Estandarizar formato de títulos y secciones
  4. Verificar que los {{FILL}} estén en los skills correctos
- **Skill:** agent-dispatcher

### Phase 2: CLI de instalación — ~1 día
- **Goal:** `npx @kanam/workflow-kit init` funcional
- **Deliverable:** Paquete npm publicado
- **Tasks:**
  1. Crear package.json para el CLI
  2. Script de init que copia skills y pregunta scopes
  3. Publicar en npm
- **Skill:** agent-dispatcher

### Phase 3: Docs + README — ~0.5 días
- **Goal:** Documentación completa del kit
- **Deliverable:** README.md, docs de cada skill, guía de adaptación
- **Tasks:**
  1. README.md con: qué es, quick start, skills list, cómo adaptar
  2. Guía de compatibilidad por agente (Claude Code, Codex, Cursor, OpenClaw)
  3. Ejemplo de uso end-to-end
- **Skill:** agent-dispatcher

### Phase 4: Repo público + branding — ~0.5 días
- **Goal:** Repo en GitHub con branding Kanam
- **Deliverable:** Repo público, LICENSE, CI básico
- **Tasks:**
  1. Crear repo `kanamai/workflow-kit` (o similar)
  2. Agregar LICENSE (MIT)
  3. Agregar GitHub Actions para lint de markdown
  4. Push initial commit
- **Skill:** agent-dispatcher

### Post-MVP
- Skills comunitarios (PRs de otros devs)
- Integración con create-stack-next como template opcional
- Versión en inglés para alcance global

## Skill mapping

| Phase | Skill | Why |
|---|---|---|
| 1. Refinar skills | agent-dispatcher | Editar 11 archivos markdown |
| 2. CLI | agent-dispatcher | Crear paquete npm simple |
| 3. Docs | agent-dispatcher | Documentación |
| 4. Repo | agent-dispatcher | Git + CI |

## Risk register

| Riesgo | Impacto | Probabilidad | Mitigación |
|---|---|---|---|
| addyosmani/agent-skills ya cubre esto | Medio | Alta | Diferenciarse en workflow completo + security-audit + agnosticismo |
| Poca adopción del CLI | Medio | Media | Promocionar en comunidades dev tooling |
| Skills muy específicos de Gonzo | Medio | Media | Los {{FILL}} permiten adaptación |
