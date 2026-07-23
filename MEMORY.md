# MEMORY.md — Long-Term Memory

## Sobre Gonzo

- Gonzalo, Argentina (GMT-3)
- 9 años Frontend React, ahora Fullstack real (React/TS, Supabase/Edge Functions, DB, billing, tooling)
- Desempleado, usando IA para todo
- También: fotógrafo, comunicación social, quiere escribir novelas
- Quiere organizar actividad física y mejorar salud
- Trabaja a cualquier hora — no comentar ni sugerir parar
- Quiere honestidad absoluta — sin darle la razón por ser quien manda
- Arranca conversaciones limpias con frecuencia — el registro escrito es crítico
- Trabaja entre Mac Mini y MacBook Air, workspace sincronizado por git
- Diferenciador: IA como infraestructura de trabajo (no como chat), stack opinado, docs de decisiones

## Metodología

- Stack opinado: OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG. Decide por criterio, no por convención.
- Sesión de OpenClaw por proyecto. No mezclar.
- Todo se registra: MEMORY.md, memory/YYYY-MM-DD.md, HANDOFF.md, CHANGELOG.md
- Los aprendizajes detallados van en `docs/LEARNINGS.md`, no acá.

## Proyectos activos

### a11y-fixer
- Fixes de accesibilidad. En curso, Fase 1 (MVP) en definición.

### create-stack-next
- Scaffolder opinado para Next.js 15. Publicado en npm. Diferenciación real vs create-next-app.
- **Estado:** vivo, no tocar. Necesita evolución, no reset.

### workflow-kit
- Portable AI agent workflow skills. Publicado en npm. Uso diario.
- **Estado:** vivo, no tocar. Evoluciona naturalmente.

### soporteml
- CRM multi-tenant para vendedores de Mercado Libre con IA. EL-1 a EL-5 completos.
- **Estado:** técnicamente completo. Si no tiene uso activo, reconsiderar archivado.

### ai-engineering-bootcamp
- 10 niveles, 23 proyectos hands-on de AI-assisted development.
- **Estado:** estructura completa, contenido todo en Pending. No es reset, es proyecto de contenido por escribir.

## Proyectos candidatos a reset (desde idea con workflows)

### antigravity-developer-stack (prioridad #1)
- 30+ patrones y playbooks de ingeniería con IA. Contenido valioso, estructura monolítica.
- **Problema:** nombre críptico, mezcla demasiadas cosas, difícil de mantener coherente.
- **Plan:** reset con product discovery + build scaffold → skill de OpenClaw o docs site.

### accessible-ui
- Headless component library (Combobox, Modal, Tabs). Espacio saturado (Radix, Ariakit, React Aria).
- **Plan:** reset con angle único (agent-friendly o generativo) o archivar.

### accessibility-auditor
- Plataforma de auditoría WCAG con Playwright + axe-core. Competitivo, sin diferenciación fuerte.
- **Plan:** reset como API-first o CI tool, o archivar.

### create-with-ai
- Generador de apps con IA tipo Lovable pero local. Mercado hipercompetitivo.
- **Plan:** reset con angle más específico o archivar.

## Repos archivados / eliminados

- **futbol-ps2** → eliminado (MVP completo, descartado)
- **copilot-skills** → archivado (reemplazado por workflow-kit)
- **chatgpt-project-architect** → archivado (absorbido por AGDS)
- **0001** → eliminar o archivar (sin propósito)
- **prueba_minecraft_claude_code** → eliminar o archivar (experimento abandonado)

## Open Source

- **Estrategia:** PRs a repos externos como portfolio vivo → menos entrevistas
- **PR registry completo** en `CONTRIBUTING.md`
- **Commit signing SSH configurado**
- **Bottleneck:** maintainer review time

## Modelo default

- **Default:** `deepseek-v4-flash:cloud` con **reasoning medium**
- Kanam evalúa cada tarea y recomienda subir a maximum o bajar a off. Gonzo decide.
- Si Kanam no dice nada: medium está bien.

## Workflows disponibles (skills del workspace)

| Workflow | Reemplaza | Para qué |
|---|---|---|
| `accessibility-studio` | a11y-system-designer, ux-a11y-studio | Diseño y validación de accesibilidad |
| `build-scaffold` | 5 skills de scaffold | Scaffolding y construcción de proyectos |
| `debug-investigation` | — | Investigación sistemática de bugs hasta causa raíz |
| `dependency-management` | — | Evaluación, actualización y gobernanza de dependencias |
| `engineering-governance` | — | Evolución continua del AI Engineering OS |
| `incident-response` | — | Gestión estructurada de incidentes en producción |
| `knowledge-management` | — | Gobernanza y sincronización de la base de conocimiento |
| `narrative-content` | story-planning, story-writing | Planificación y escritura de ficción |
| `observability` | — | Instrumentación, métricas, tracing y análisis del sistema |
| `oss-contribution` | oss-contribute, sdd-brownfield | Contribución estratégica a OSS |
| `performance-optimization` | — | Análisis, profiling y optimización sistemática |
| `pre-deploy-qa` | — | Validación pre-deploy (build, rutas, SEO, API, performance) |
| `product-discovery` | 4 skills de producto | Idea → definición de producto. Fase 0 dividida en 0.1 (Brainstorming, GLM 5.2) y 0.2 (Arquitectura, Kimi K2.7). |
| `release-management` | — | Planificación, coordinación y ejecución de releases |
| `research-spike` | — | Investigación técnica para reducir incertidumbre |
| `review-quality` | pr-review, po-review, security-audit | Revisión pre-merge y auditoría |
| `session-lifecycle` | 4 skills de sesión | Ciclo de vida completo de sesión |
| `task-execution` | — | Ejecución de tareas: planificar, implementar, verificar, PR |
| `tech-docs` | adr-framework, adr-sync | Documentación técnica |
| `vibe-code-cleanup` | — | Limpieza de código generado por IA/vibe coding |

> **Nota:** `ai-agent-setup` se movió a `docs/reference/ai-agent-setup.md` — es referencia conceptual, no skill operativa.

## Lecciones aprendidas (resumen)

Lo esencial. El detalle está en `docs/LEARNINGS.md`.

- **Triaje de PRs competidores ANTES de invertir tiempo** — la lección más cara.
- **Complex issue ≠ complex fix** — la dificultad está en el root cause, no en la implementación.
- **Fork before push** — al trabajar en forks de terceros, fork primero, clonar el fork, configurar upstream.
- **Type-check en shallow clones** — no tienen tags. Solución: `git fetch --tags`.
- **Repos Tier 0 (shadcn/ui, TanStack, Vercel):** evitar trazas de automatización. Descripción humana.
- **Reviews técnicas en PRs ajenos = contribución de valor sin PR propio.**
- **Community participation = reputación:** comentar, compartir, cross-referencing.
- **HANDOFF.md nunca al workspace git de terceros** — es metadata de sesión, no va al repo externo.
- **Next.js 15 + TypeScript 7 son incompatibles** — templates mantienen TS 5.x hasta Next.js 16.
- **Scope @gonzoblasco/ para npm.**
- **Las skills se construyen haciendo, no escribiendo.**
- **Specs as-built primero, delta después.**
- **El scaffold generado necesita verificación real.**
- **Los ADRs se desactualizan rápido.**
- **El truncamiento no es del modelo, es de maxTokens sin configurar.**
- **Reasoning maximum no es más texto, es mejor texto** — como code reviewer, no generador.
- **Algunos workflows no se configuran en el gateway, se acuerdan en conversación y se registran.**
- **Inventario periódico de repos** — hacer cada N meses para detectar zombies, candidatos a reset, y mantener el portfolio limpio.
- **No todo lo incompleto necesita reset** — distinguir entre proyectos que necesitan redefinición (reset) y proyectos que necesitan iteración (evolución).
- **El vehículo importa tanto como el contenido** — AGDS tiene contenido valioso pero estructura wrong. A veces el problema no es la idea sino cómo se empaqueta.
- **Proyectos de contenido ≠ proyectos de software** — ai-engineering-bootcamp no necesita código, necesita escritura. El approach es diferente.
- **Biome se autoformatea — correr `npx biome check --write .` post-scaffold** — si no, el primer CI falla porque Biome lintea su propio `biome.json`.
- **shadcn/ui + Biome = ignorar `src/components/ui/*`** — los componentes de shadcn generan falsos positivos de a11y. Agregar al `files.ignore` de `biome.json` desde el día 1.
- **Setup de proyecto nuevo: git init + .knowledge/ + .gitignore + submodule** — hacer todo de una, no post-hoc.
- **Pattern-Keys (`area.symptom`) para deduplicar aprendizajes** — adoptado de self-improving-agent. Opcional pero recomendado para entradas recurrentes.
- **Recurrence-Count >= 3 en 30 días + 2 tareas → promover a SOUL/TOOLS/AGENTS** — si algo pasa 3 veces, no es accidente, es falta de memoria institucional.
- **IDs LRN-YYYYMMDD-XXX para referencias cruzadas** — opcional, útil cuando LEARNINGS.md crece.
- **No instalar skills que pisan 80%+ de lo que ya tenemos** — robar ideas, integrarlas como convención propia.
- **Learning Signals en AGENTS.md** — frases gatillo que disparan logging automático (correcciones, preferencias, patrones).
- **Self-Reflection post-tarea** — después de tareas significativas, evaluar con CONTEXT/REFLECTION/LESSON.
- **Conflict Resolution** — específico > general, reciente > antiguo, ambiguo → preguntar.
- **Common Traps** — aprender del silencio, promover rápido, leer todo, compactar borrando.
- **WAL Protocol** — escribir antes de responder. Si hay correcciones/preferencias/decisiones → STOP, WRITE, THEN respond.
- **Working Buffer** — loggear exchanges cuando el contexto está al ~60%+.
- **Compaction Recovery** — protocolo de recuperación post-compactación (buffer → daily notes → search).
- **Relentless Resourcefulness** — probar 5-10 approaches antes de decir "no puedo".
- **Verify Implementation** — no reportar "done" si solo cambiaste texto, no mecanismo.
- **Confidence Tagging** — 🟢/🟡/🔴 en recomendaciones según calidad de datos.
- **Self-Reflection con BIASES DETECTED** — identificar sesgos cognitivos en retrospectiva.
- **Evaluación multidimensional** — framework con pesos para evaluar workflows/skills/proyectos.
- **Gate dimension** — una dimensión crítica puede vetar todo (ej: seguridad).
- **Tiered verification (L0-L3)** — nivel de verificación según alcance del cambio.
- **Auto-rollback on regression** — si una mejora empeora las cosas, revertir.
- **DREAMS.md** — consolidación programada de memoria cada ~7 días.
- **Structured Escalation** — handoff estructurado cuando estoy stuck (BLOQUEO/CAUSA/INTENTOS/NECESITO/ALTERNATIVA).
- **Growth Loops** — 4 ciclos de mejora continua: Curiosidad, Patrones, Expansión, Resultados.
- **Handoff estructurado entre subagentes** — qué se hizo, dónde están los artifacts, cómo verificar, issues conocidos, qué sigue.
- **Productividad adaptada a ADHD** — una cosa a la vez, inbox capture, overload triage, rutinas de inicio/cierre, sin culpa.

## Estilo en issues/PRs de terceros

- Natural y suelto, no como manual de programación
- Sonar a persona real, no a documentación técnica
- En inglés siempre en repos externos
- Bugs concretos sin competencia → PR rápido
- RFCs → comentario técnico que posiciona, no código
