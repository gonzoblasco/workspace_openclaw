# CONTRIBUTING.md — Playbook de Open Source

**Estrategia de Gonzo para conseguir trabajo como dev Next.js senior fullstack через visibilidad open source**

---

## Perfil que se vende

Gonzo no es "un dev que sabe React". El diferenciador es:

1. **Metodología IA-asistida own** — trabaja con un sistema completo de IA como infraestructura: sesiones por proyecto, memoria persistente, handoffs, subagentes, skill workshop. No usa IA como chat, la usa como copiloto metodológico. La mayoría de los devs no saben hacer esto.
2. **Stack opinado, no por default** — cura herramientas (CSN: OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG). Decide por criterio, no por convención heredada.
3. **Accesibilidad como especialización activa** — no es checkbox, es ventaja competitiva. Tiene proyectos dedicados y busca trabajos donde sea central.
4. **Fullstack real** — React/TS frontend, Supabase/Edge Functions backend, DB, billing, tooling, scaffolding.
5. **Documenta decisiones, no solo código** — AGENTS.md, ROADMAP, ADRs. Eso es senior sin título.

**El pitch:** *"Soy un dev fullstack que construyó un sistema de trabajo con IA propio, con stack opinado y docs de decisiones. Tengo PRs mergeados que lo demuestran."*

Un repositorio con PRs mergeados en shadcn/ui, TanStack, o Vercel vale más que cualquier take-home test.

---

## Filosofía

- No contribuir por contribuir. Buscar proyectos donde Gonzo ya usa o conoce el dominio — eso da velocidad y calidad.
- PRs chicos, bien hechos, semánticos, con tests. Mejor 3 PRs sólidos que 10 PRs de typo.
- En inglés siempre que el repo sea internacional.
- Commits semánticos (`feat`, `fix`, `test`, `docs`, `refactor`).
- Un PR por issue/feature. No mezclar concerns.
- Si el repo tiene CONTRIBUTING.md, leerlo antes de tocar nada.
- **Cada PR es evidencia de la metodología**: commits limpios, descripción clara, tests, referencias al issue. El PR mismo demuestra que sabés trabajar con IA como copiloto.

## Cómo pedirle a una sesión nueva que trabaje en un repo externo

### Prompt base (copiar y adaptar)

> Quiero trabajar como contributor en un proyecto open source. Te paso el contexto:
>
> - **Repo:** github.com/[org]/[repo]
> - **Issue:** #[n] — [título del issue]
> - **Fork:** github.com/gonzoblasco/[repo] (forkear si no existe)
> - **Clonar en:** `projects/[repo]`
>
> 1. Leé el CONTRIBUTING.md del repo y su estructura de plugins/sistema
> 2. Leé el issue y los comentarios del maintainer
> 3. Implementá el cambio siguiendo sus convenciones
> 4. Verificá build, lint, tests
> 5. Commits semánticos, un PR por issue
> 6. Abrí el PR referenciando el issue

### Archivo de contexto por repo

Cada repo donde contribuimos tiene su propio `HANDOFF.md` en `projects/[repo]/HANDOFF.md` con:
- Qué se hizo hasta ahora
- Qué PRs están abiertos
- Qué sigue en el plan
- Estructura del repo para referencia

## Reglas de oro

1. **Forkear primero, clonar después.** Remote `origin` = upstream, `fork` = el tuyo.
2. **Branch naming:** `feature/[issue]-[descripcion-corta]` o `fix/[issue]-[descripcion]`
3. **Un PR por issue.** Si el cambio es grande, partir en PRs chicos.
4. **Tests.** Si el repo tiene tests, el PR incluye tests. Si no tiene, igual escribirlos.
5. **No romper CI.** Si el CI falla por algo del repo (no nuestro), mencionarlo en el PR pero no bloquear.
6. **Descripción del PR:** qué hace, por qué, cómo se verificó, qué falta. En inglés.
7. **Paciencia.** Los maintainers tienen vidas. Esperar 1-2 semanas antes de hacer follow-up.

---

## Pipeline de repos objetivos

### En progreso

| Repo | Issue | PR | Estado |
|------|-------|-----|--------|
| akd-io/create-next-stack | #262 Bun | [#280](https://github.com/akd-io/create-next-stack/pull/280) | Esperando review |
| akd-io/create-next-stack | #224 Vitest | — | Plan, en ~2 semanas |
| akd-io/create-next-stack | #249 Supabase | — | Plan, después de Vitest |
| akd-io/create-next-stack | #268 Auth.js + ShadCN | — | Plan |
| akd-io/create-next-stack | #272 Architecture review | — | Plan (el golazo) |

### Tier 1 — Alta visibilidad, activos, alineados con el perfil (atacar primero)

| Repo | ⭐ | Actividad (30d) | Por qué encaja |
|------|-----|-----------------|----------------|
| **shadcn-ui/ui** | 119k | 50 issues activos | Lo usa en SoporteML. 15 bugs abiertos esta semana, muchos de UI/accesibilidad — justo su especialización. "Merged in shadcn/ui" = visibilidad enorme. |
| **TanStack/router** | 14.8k | 50 issues activos | Lo usa en kanamai, reactiva, umbrawriter. 8 enhancement issues recientes. #918 (Accessibility) y #4901 (Link external links) son factibles. |
| **TanStack/query** | 50k | 19 issues activos | Lo usa en todos lados. #2712 (ErrorBoundary retry on mount) y #9681 (DevTools isolation) son issues reales, alcanzables. |
| **vercel/ai** | 25.5k | 50 issues activos | AI SDK de Vercel. 1729 issues abiertos. Mucho scope. Empresa contratan mucho desde este ecosistema. |
| **payloadcms/payload** | 43.5k | 50 issues activos | CMS fullstack Next.js. Stack muy parecido al suyo. Mucha superficie de bugs. |

### Tier 2 — Buenos pero más esfuerzo o menos actividad

| Repo | ⭐ | Por qué |
|------|-----|---------|
| **vercel/next.js** | 79k+ | 10 good first issues. El repo emblemático. Un PR mergeado = CV por sí solo. Review largo, alta dificultad. |
| **t3-oss/create-t3-app** | 29k | Issues recientes sobre Bun, Prisma, Biome — cosas que conoce. #2185 (clipboard copy a11y) es su intersección. Último push dic 2025, menos activo. |
| **biomejs/biome** | 25.4k | Lo usa en CSN. Muy activo. Pero el dominio es tooling interno (parser/linter), menos fullstack. |
| **shuding/nextra** | 13.8k | Docs framework sobre Next.js. 5 help wanted issues. Actividad moderada. |

### Tier 3 — Interesantes pero fríos ahora

| Repo | Por qué no ahora |
|------|-----------------|
| nextjs/saas-starter | Sin actividad en 30 días |
| pacocoursey/next-themes | Sin actividad en 30 días |
| vercel/commerce | 1 issue activo en 30 días |
| ixartz/SaaS-Boilerplate | 1 issue activo |

### Candidatos futuros (cuando el Tier 1 avance)

- **supabase/supabase** — docs, examples, bugs en JS client. Lo usa diario. #6435 (good first issue: newlines in SMS OTP) está disponible.
- **openai/openai-node** — SDK que usa en varios proyectos
- **vitest-dev/vitest** — lo usa en CSN, podría contribuir docs o bugs

---

## Plan de ataque (próximas 2 semanas)

### Semana 1 — shadcn-ui/ui (accesibilidad + UI)

Priorizar bugs de accesibilidad — es su especialización y hay 15 abiertos esta semana:

| Issue | Descripción | Por qué |
|-------|-------------|---------|
| #11157 | Input OTP: keyboard navigation causes unwanted layout shift | Accesibilidad + UX. Chico, claro. |
| #11104 | SidebarProvider registers global Cmd+B shortcut without opt-out | Accesibilidad (teclado), bug claro. |
| #11159 | Calendar Range: third click doesn't reset start date | UX bug, componente conocido. |

### Semana 2 — TanStack/router o TanStack/query

Elegir uno:
- **TanStack/router** #918 (Accessibility) o #4901 (Link external links)
- **TanStack/query** #2712 (ErrorBoundary retry) o #9681 (DevTools isolation)

### En paralelo — akd-io/create-next-stack

Seguir el plan existente: Vitest → Supabase → Auth.js. El PR #280 debería tener review pronto.

---

## Criterios para elegir nuevos repos

1. **Gonzo ya usa el proyecto** — conoce el dominio, no arranca de cero
2. **Repo activo** — maintainers que responden, issues actualizados en los últimos 30 días
3. **Issues alcanzables** — `good first issue`, `help wanted`, o bugs/enhancement sin assignee
4. **Categorías donde Gonzo es fuerte:** React, Next.js, TypeScript, Supabase, tooling/scaffolding, accesibilidad, AI SDKs
5. **Tamaño del repo** — no contribuir a React core de entrada; proyectos medianos donde un PR se nota
6. **Valor de visibilidad** — ¿el repo lo miran recruiters/empresas del ecosistema donde quiere trabajar?

---

## Tracking

El estado de cada repo se guarda en:
- `projects/[repo]/HANDOFF.md` — estado detallado por repo
- `projects/PROYECTOS.md` — sección "Colaboración externa" con tabla resumen
- `memory/YYYY-MM-DD.md` — diario de cada sesión
- `MEMORY.md` — contexto de largo plazo

## Sesiones por proyecto

Una sesión de OpenClaw por repo externo. Al arrancar:
1. Leer `projects/[repo]/HANDOFF.md`
2. Leer el issue objetivo
3. Clonar/fetche el repo si no está
4. Trabajar siguiendo las reglas de oro

Al cerrar:
1. Actualizar `HANDOFF.md` del repo
2. Actualizar `memory/YYYY-MM-DD.md`
3. Commit + push del workspace