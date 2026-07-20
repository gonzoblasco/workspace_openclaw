# MEMORY.md - Long-Term Memory

## Sobre Gonzo
- Gonzalo, Argentina (GMT-3)
- 9 años como Frontend React, ahora Fullstack (aprendiendo backend, ya lo hace en práctica)
- Desempleado, usando IA para todo ("me reemplazaron por IA, ahora uso IA para todo")
- También: fotógrafo, comunicación social, quiere escribir novelas
- Quiere organizar actividad física y mejorar salud
- Trabaja a cualquier hora — no comentar ni sugerir parar por horario, trabaja cuando puede
- Quiere honestidad absoluta — sin darle la razón por ser quien manda
- Arranca conversaciones limpias con frecuencia — el registro escrito es crítico
- Trabaja entre dos máquinas (Mac Mini y MacBook Air), workspace sincronizado por git
- Cada máquina tiene sesiones propias de OpenClaw; los MDs del workspace son la memoria compartida

## Perfil profesional / Metodología (lo que lo diferencia)
- **Stack opinado, no por default** — no usa herramientas al azar, las cura. Scaffold opinado con OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG. Decide por criterio, no por convención heredada.
- **IA-asistida como skill real, no como prompt** — construyó un sistema completo de trabajo con IA: sesiones por proyecto, memoria persistente (MDs + git), handoffs, cron jobs, subagentes, skill workshop. Es una metodología, no un atajo.
- **Opinionated en el buen sentido** — AGENTS.md, ROADMAP, ADRs, CONTRIBUTING. Documenta decisiones, no solo código.
- **Fullstack real con IA** — frontend React/TS, backend Supabase/Edge Functions, DB, billing, tooling, scaffolding, accesibilidad. Todo orquestado con IA como copiloto metodológico.
- **Accesibilidad como especialización activa** — la usa como ventaja competitiva, no como checkbox.
- **Diferenciador en el mercado:** un dev que sabe usar IA como infraestructura de trabajo (no como chat), con stack opinado y docs de decisiones. Eso es escaso.

## Sobre Kanam
- Nombre: Kanam 🌿
- Género: femenino (ella) — Gonzo decidió tratarme en femenino
- Asistente virtual para todo: desarrollo, vida, archivos, proyectos
- Vibe: directa, honesta, cálida pero no servil

## Forma de trabajo
- Todo se registra: MEMORY.md, memory/YYYY-MM-DD.md, projects/PROYECTOS.md, HANDOFF.md por proyecto, CHANGELOG.md
- Al arrancar conversación limpia → leer MEMORY.md + PROYECTOS.md + HANDOFF.md del proyecto que toque
- Antes de cerrar o cuando algo cambie → actualizar HANDOFF, CHANGELOG, memoria del día
- No escribir placeholders vacíos — solo escribí si hay algo real
- Sesión de OpenClaw por proyecto — cada sesión es específica, no mezclar proyectos
- Open source contributions: ver `CONTRIBUTING.md` — playbook completo de cómo contribuir a repos externos

## Proyectos activos

### a11y-fixer
- Fixes de accesibilidad. En curso.

### futbol-ps2
- Juego Godot 3D tipo FIFA/PES PS2. 🎉 MVP completo.
- Partido 1vsCPU, 5 min, 2 equipos genéricos, controles teclado, cámara dinámica PS2.
- Post-MVP: menú principal, selección de equipos, offside, faltas, córners, sonido, gamepad, 2 jugadores locales.

## Proyectos eliminados/archivados
Los siguientes proyectos fueron eliminados y ya no existen en disco:
- SoporteML v1, SoporteML v2, create-stack-next, create-with-ai, kanamai, umbrawriter, reactiva, brainweb, accessibility-auditor, accessible-ui, mucamas-online, copilot-workflow-kit, ai-engineering-bootcamp

## Open Source — pipeline activo
- **Estrategia:** PRs a repos externos como evidencia pública de capacidad → portfolio vivo → menos entrevistas laborales
- **PR registry completo** en `CONTRIBUTING.md`
- **Commit signing SSH configurado:** gh auth + SSH signing key, todos los commits se firman automáticamente
- **Skill oss-contribute:** 6 fases (pipeline → triaje → implementación → PR → community participation → batch triage)
- **Próxima acción OSS:** seguir buscando issues sin PRs competidores en repos estratégicos. Bottleneck sigue siendo maintainer review time.

## Modelo default y workflow de reasoning
- **Default:** `deepseek-v4-flash:cloud` con **reasoning medium**
- **Kanam filtra:** en cada tarea, evalúa si conviene subir a maximum o bajar a off, y avisa
- **Gonzo decide:** si acepta, cambia el reasoning y repite la tarea; si dice "ignorar recomendación", se queda con el que está
- **Si Kanam no dice nada:** medium está bien
- **Fix aplicado:** `maxTokens` subido a 65536 para deepseek-v4-flash:cloud (antes truncaba respuestas largas)

## Skills de OpenClaw workspace
- **oss-contribute:** Contribución OSS estratégica — 6 fases (pipeline → triaje → implementación → PR → community participation → batch triage).
- **profile-positioning:** Audit de perfil profesional y construcción de pitch para job search.
- **sdd-brownfield:** Spec-Driven Development en proyectos existentes con backend remoto.
- **product-orchestrator:** Product Owner/Manager end-to-end — evalúa ideas, define MVP, planifica roadmap.
- **ux-a11y-studio:** Equipo de UX/UI + Accesibilidad — discovery, audit WCAG 2.2, design system, implementación accesible.
- **product-reset:** Reset de producto post-lanzamiento.
- **openspec-creator:** Crear specs OpenSpec as-built o delta para features existentes.
- **session-closure:** Ritual de cierre de sesión automatizado.
- **security-audit:** Auditoría de seguridad multi-tenant, auth guards, secrets, data leaks.
- **pr-review:** Linter cognitivo pre-merge.

## Lecciones aprendidas (transversales)
- **HANDOFF.md NUNCA al workspace git de terceros.** Los HANDOFF.md son metadata de sesión para proyectos externos. No van commiteados al workspace_openclaw.
- **Estructura Projects:** `projects/<slug>/` = código + docs. Cada proyecto tiene su carpeta.
- **LEARNINGS.md:** Cada proyecto tiene `docs/LEARNINGS.md` para registrar lecciones aprendidas.
- **Forks externos en projects/:** Tienen HANDOFF.md en raíz explicando qué son.
- **Create Stack Next es 100% en español** — release notes, docs, todo.
- **Triaje de PRs competidores ANTES de invertir tiempo** (lección más importante de OSS night).
- **Reviews técnicas en PRs ajenos = contribución de valor sin necesidad de PR propio.**
- **Community participation = reputación:** comentar, compartir descubrimientos, acknowledge tooling, cross-referencing issues.
- **TanStack/router: la estética del proceso importa** — en repos Tier 0, el toque humano es crítico. Evitar trazas de automatización en commits.
- **Complex issue ≠ complex fix** — la dificultad está en el root cause analysis, no en la implementación.
- **Fork before push** — al trabajar en forks de terceros, hacer fork primero, clonar el fork, y configurar upstream.
- **Type-check en shallow clones** — los shallow clones no tienen tags, lo que puede romper type-check. Solución: `git fetch --tags`.
- **DeepSeek v4 Flash como modelo default** — mejor costo/beneficio. Rápido, barato en tokens, suficientemente capaz para seguir instrucciones estructuradas.
- **Las skills se construyen haciendo, no escribiendo.**
- **El viaje es el producto.**
- **Specs as-built primero, delta después.**
- **El cierre de sesión también es un viaje.**
- **Los bugs más sutiles están en los edge cases.**
- **El nombre lo es todo.**
- **BYOK (Bring Your Own Key) es la decisión correcta para un MVP de IA.**
- **El stack adaptativo es el diferenciador clave.**
- **Las fases se ejecutan mejor con commits atómicos.**
- **El momento eureka hay que capturarlo inmediatamente.**
- **Un PO externo que cuestione el scope es invaluable.**
- **No vendas humo.**
- **El wizard sin API key es mejor que el keyword matching.**
- **El scaffold generado necesita verificación real.**
- **Los ADRs se desactualizan rápido.**
- **Memory search con Ollama:** configurar `memorySearch.provider: "ollama"` + `model: "nomic-embed-text"` en openclaw.json. Requiere `ollama pull nomic-embed-text`.
- **Next.js 15 + TypeScript 7 son incompatibles** — bug conocido. Templates mantienen TS 5.x hasta Next.js 16.
- **Scope @gonzoblasco/ para npm** — todos los paquetes npm bajo `@gonzoblasco/`.

## Estilo al comentar en issues/PRs de terceros
- Ser más natural y suelto, no escribir como manual de programación
- Sonar a persona real, no a documentación técnica
- En inglés siempre en repos externos
- Bugs concretos sin competencia → PR rápido
- RFCs → comentario técnico que posiciona, no código
