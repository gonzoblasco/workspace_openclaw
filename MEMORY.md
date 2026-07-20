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

### futbol-ps2
- Juego Godot 3D tipo FIFA/PES PS2. 🎉 MVP completo.
- Post-MVP: menú principal, selección de equipos, offside, faltas, córners, sonido, gamepad, 2 jugadores locales.

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
| `workflow-accessibility-studio` | a11y-system-designer, ux-a11y-studio | Diseño y validación de accesibilidad |
| `workflow-build-scaffold` | 5 skills de scaffold | Scaffolding y construcción de proyectos |
| `workflow-narrative-content` | story-planning, story-writing | Planificación y escritura de ficción |
| `workflow-oss-contribution` | oss-contribute, sdd-brownfield | Contribución estratégica a OSS |
| `workflow-product-discovery` | 4 skills de producto | Idea → definición de producto |
| `workflow-review-quality` | pr-review, po-review, security-audit | Revisión pre-merge y auditoría |
| `workflow-session-lifecycle` | 4 skills de sesión | Ciclo de vida completo de sesión |
| `workflow-tech-docs` | adr-framework, adr-sync | Documentación técnica |

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

## Estilo en issues/PRs de terceros

- Natural y suelto, no como manual de programación
- Sonar a persona real, no a documentación técnica
- En inglés siempre en repos externos
- Bugs concretos sin competencia → PR rápido
- RFCs → comentario técnico que posiciona, no código
