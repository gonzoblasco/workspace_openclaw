# DEFINITION.md — Kanam Workflow Kit

> Phase 2 — Product Definition
> Fecha: 2026-07-15

> **Nota sobre naming:** El proyecto actual se llama `--copilot-skills`. Para el producto uso "Kanam Workflow Kit" como placeholder — decidimos el nombre definitivo después.

## MVP Scope

### Core value
Un kit de skills reutilizables para AI-assisted development que se instala en cualquier proyecto con un comando. Define workflows de commit, PR, review, auditoría de seguridad, y cierre de epics.

### In scope (MVP)
1. **11 skills existentes** — refinados, con frontmatter YAML estándar, documentación clara
2. **CLI de instalación** — `npx @kanam/workflow-kit init` que copia los skills al proyecto
3. **README.md** — qué es, cómo se usa, cómo se adapta
4. **Docs de cada skill** — propósito, precondiciones, pasos, validación
5. **Compatibilidad explícita** — Claude Code, Codex, Cursor, OpenClaw
6. **Repo público en GitHub** — bajo la organización Kanam

### Out of scope (post-MVP)
- Interfaz gráfica — post-MVP
- Skills generados por IA (auto-generación de skills) — post-MVP
- Marketplace de skills comunitarios — post-MVP
- Integración con CI/CD — post-MVP

### Explicit non-goals
- No es un framework de agentes (como LangChain, CrewAI)
- No reemplaza skills nativos de Claude Code
- No es un producto SaaS

## User Personas

### Persona 1: El dev solitario con IA
- **Quién:** Desarrollador fullstack, 25-40 años
- **Context:** Usa Claude Code o Codex para codificar, pero cada sesión arranca de cero
- **Necesita:** Skills pre-hechos que definan cómo commitear, revisar, auditar
- **Éxito:** Corre `npx @kanam/workflow-kit init` y tiene un workflow completo en 5 segundos

### Persona 2: El equipo que estandariza
- **Quién:** Tech lead o founder técnico, 30-45 años
- **Context:** El equipo usa IA pero cada uno la usa distinto — commits inconsistentes, sin review, sin auditoría
- **Necesita:** Un estándar portable que todos puedan copiar a sus proyectos
- **Éxito:** Todos los proyectos del equipo tienen los mismos skills, mismos gates, mismo formato de commit

## User Flows

### Flow 1: Instalación
- **Trigger:** Dev corre `npx @kanam/workflow-kit init`
- **Steps:**
  1. CLI pregunta: "¿Qué skills querés instalar?" (default: todos)
  2. CLI pregunta: "¿Cuáles son los scopes de tu proyecto?" (para commit)
  3. CLI copia los skills seleccionados a `.agents/skills/`
  4. CLI genera `.env.local.example` si aplica
- **Outcome:** Skills instalados y listos para usar
- **Error:** Directorio `.agents/skills/` ya existe → preguntar si sobrescribir

### Flow 2: Usar un skill (commit)
- **Trigger:** Dev escribe `/commit` en el chat del agente
- **Steps:**
  1. Agente lee `.agents/skills/commit/SKILL.md`
  2. Sigue los pasos: revisar staged, elegir tipo, determinar scope, escribir mensaje
  3. Crea el commit con formato Conventional Commits
- **Outcome:** Commit formateado correctamente
- **Error:** No hay cambios staged → mensaje "No hay cambios para commitear"

### Flow 3: Security audit
- **Trigger:** Dev escribe `/security-audit` o cierra un epic
- **Steps:**
  1. Agente lee `.agents/skills/security-audit/SKILL.md`
  2. Revisa: fugas multi-tenancy, auth guards, secrets, data leaks
  3. Genera reporte de hallazgos
- **Outcome:** Reporte de seguridad con estado PASS/FAIL
- **Error:** Hallazgos críticos → bloquea cierre de epic

## Success Metrics

1. **GitHub stars** — 50+ en 3 meses
2. **npm downloads** — 100+ en 3 meses
3. **Issues/PRs de la comunidad** — señal de uso real
4. **Proyectos que lo adoptan** — al menos create-stack-next y brainweb
