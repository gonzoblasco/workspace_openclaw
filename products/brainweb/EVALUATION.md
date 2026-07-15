# EVALUATION.md — BrainWeb

> Phase 1 — Product Evaluation
> Fecha: 2026-07-15

## Problem

La gente acumula información dispersa: links, notas, ideas, snippets. Las herramientas existentes o son pesadas (Notion), requieren apps nativas (Obsidian), o tienen curvas de aprendizaje altas (Logseq, Roam). No hay una opción **web-first, open source, self-hostable** que sea simple, visual (graph view), y que funcione como un "segundo cerebro" liviano.

## Audience

- **Usuarios de PKM** que quieren control de sus datos (self-hosted)
- **Devs** que prefieren una web app a una app nativa
- **Geeks de la productividad** que quieren algo liviano y visual
- **Gente que usa Obsidian pero quiere acceso web** (no app de escritorio)
- Tamaño: nicho dentro de nicho. No son millones, pero hay comunidad activa (cientos de miles en foros de PKM)

## Existing solutions

| Herramienta | Tipo | Open Source | Self-hosted | Web-first | Graph view |
|---|---|---|---|---|---|
| Obsidian | App nativa | ❌ (core cerrado) | ❌ | ❌ | ✅ |
| Logseq | App nativa | ✅ | ❌ (P2P local) | ❌ | ✅ |
| Notion | Web app | ❌ | ❌ | ✅ | ❌ |
| Roam Research | Web app | ❌ | ❌ | ✅ | ✅ |
| Capacities | Web app | ❌ | ❌ | ✅ | ❌ |
| Tana | Web app | ❌ | ❌ | ✅ | ❌ |
| Heptabase | App nativa | ❌ | ❌ | ❌ | ✅ (canvas) |
| Anytype | App nativa | ✅ | ❌ (P2P) | ❌ | ✅ |
| SiYuan | Web app | ✅ | ✅ | ✅ | ✅ |
| GitNodes | Web app | ✅ | ✅ (Git) | ✅ | ✅ |

**Gap analysis:** SiYuan y GitNodes existen pero son proyectos chicos. SiYuan es chino con UI en inglés medio. GitNodes usa Git como source of truth (interesante pero opinado). **Ninguno** tiene el approach de "web app simple + self-hosted con Supabase + graph view SVG" que brainweb ya tiene esbozado.

## Differentiation

BrainWeb se diferencia por:
1. **Web-first + self-hosted** — corre en cualquier lado con Supabase, no requiere app nativa
2. **Graph view SVG nativo** — ya implementado, visual y rápido
3. **Simple por diseño** — no es un clon de Notion, es un bloc de notas con superpoderes
4. **Stack moderno** — React 19 + TanStack Start + Tailwind v4, fácil de extender
5. **Open source real** — no es open core, es código abierto completo

## Revenue model

**Opción A: SaaS freemium**
- Free: hasta 100 notas, self-hosted manual
- Pro ($5/mes): notas ilimitadas, sync multi-dispositivo, AI features
- Competitivo vs Obsidian Sync ($5/mes) y Notion ($10/mes)

**Opción B: Open source + donations / GitHub Sponsors**
- Sin ingresos directos, pero construye portfolio y reputación
- Alinea con la estrategia de Gonzo de PRs y visibilidad

**Opción C: Self-hosted premium**
- Código gratis, pero guía de deploy + soporte = pago único ($20-50)
- Modelo tipo Dokploy / Coolify

**Recomendación:** Arrancar con Opción B (open source + sponsors) y evolucionar a Opción A si hay tracción. No tiene sentido meter billing desde el día 1 en un mercado saturado.

## Technical feasibility

- **¿Se puede construir?** Sí, ya hay un MVP funcional en localStorage
- **Lo que falta:** backend (Supabase), auth, sync multi-dispositivo, deploy
- **Stack actual:** TanStack Start + React 19 + Tailwind v4 + shadcn/ui
- **Stack target:** mismo frontend + Supabase (auth + DB + realtime)
- **Complejidad:** moderada (CRUD + auth + graph view + sync)
- **Dependencias externas:** Supabase (gratuito hasta cierto punto)
- **Tiempo estimado MVP:** 2-3 semanas (una persona, sesiones intermitentes)

## Strategic fit

- **¿Fit con objetivos de Gonzo?** Sí — es un proyecto público que muestra capacidad técnica fullstack + UI/UX + open source
- **¿Fit con ecosistema Kanam?** Indirecto — no es un producto Kanam, pero usa el mismo stack y metodología
- **¿Sinergia con otros proyectos?** Podría integrarse con create-stack-next como template de PKM app
- **Opportunity cost:** cada hora en brainweb es una hora que no va a SoporteML v2 (prioridad #1) o UmbraWriter (prioridad #2)

## Risks

| Riesgo | Impacto | Probabilidad | Mitigación |
|---|---|---|---|
| Mercado saturado | Alto | Alta | Diferenciarse en nicho web-first + self-hosted + simple |
| Nadie lo usa | Medio | Media | Hacerlo open source desde el día 1, comunidad primero |
| Obsidian saca web app | Alto | Baja | Obsidian es nativo por filosofía, improbable |
| Gonzo pierde interés | Medio | Media | Definir MVP chico (2 semanas), no proyecto eterno |
| Competencia con SoporteML v2 | Medio | Alta | Priorizar explícitamente: brainweb es proyecto de portfolio, no de ingresos |

## Verdict: 🟡 GO WITH CAVEATS

### Conditions
1. **No compite con SoporteML v2** — brainweb se construye en tiempo muerto o como proyecto paralelo, no reemplaza la prioridad #1
2. **MVP ultra-chico** — no intentar competir feature a feature con Obsidian. El MVP es: web app con backend, auth, notas markdown, tags, graph view. Eso es todo.
3. **Open source first** — no pensar en monetización hasta que haya tracción real
4. **Tiempo límite: 2 semanas** para MVP funcional deployado. Si no está, se congela.

### Recommendation
Brainweb tiene potencial como **proyecto open source de portfolio** que muestra:
- Fullstack React/TS + Supabase
- UI/UX cuidada (graph view SVG, editor markdown)
- Open source real con comunidad

No es un producto para vivir de él (al menos no ahora). Pero es un proyecto que:
- Se ve bien en GitHub
- Es demostrable en entrevistas
- Usa el stack que Gonzo ya domina
- Tiene código base que ya funciona (solo falta backend)

**Propuesta:** Convertir brainweb en un open source tool self-hosted, gratis, con GitHub Sponsors. Si en 6 meses tiene 100+ stars y gente usándolo, reevaluar si vale la pena meterle SaaS.
