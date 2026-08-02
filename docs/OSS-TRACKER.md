# OSS-TRACKER.md — Open Source Contributions Tracker

Registro completo de contribuciones a repos externos. Cada entrada captura la cadena completa: issue → PR de tercero → nuestro aporte → nuestro PR → estado.

## Estrategia

- PRs a repos externos como portfolio vivo → menos entrevistas
- PR registry completo acá abajo
- Commit signing SSH configurado
- **Bottleneck:** maintainer review time

---

## PR Registry — Cadena Completa

**Formato estándar:**

```
#### repo-org/repo-name

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | #[n] | Título del issue |
| **PR de tercero** | #[n] (autor) | Qué hizo → **ESTADO** (MERGED/OPEN/CLOSED) |
| **Nuestro aporte** | [Comment](url) | Qué dijimos, qué nos pidieron |
| **Nuestro PR** | #[n] | Qué hace → **ESTADO** |
| **Contexto** | — | Cómo llegamos acá, decisiones, bifurcaciones |
```

Si no hay issue o PR de tercero, se omite ese eslabón. El contexto es obligatorio.

---

### facebook/astryx

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | [#4143](https://github.com/facebook/astryx/issues/4143) | AvatarStatusDot solo usa color para transmitir estado (WCAG 1.4.1) |
| **PR de tercero** | [#4157](https://github.com/facebook/astryx/pull/4157) (AKnassa) | Shapes por variante (filled/ring/minus) → **MERGED** 24 Jul |
| **Nuestro aporte** | [Comment](https://github.com/facebook/astryx/pull/4157#issuecomment-5072292534) | Ofrecimos converger #4218 con #4157. @humbertovirtudes sugirió PR separado |
| **Nuestro PR** | [#4298](https://github.com/facebook/astryx/pull/4298) | Default accessible labels ("Online"/"Away"/"Busy") → **OPEN**, esperando review de @humbertovirtudes |
| **Contexto** | — | Gonzo abrió #4218 primero (icon+label). humbertovirtudes sugirió converger con #4157 por ser base más sólida. PR #4218 cerrado, contenido migrado a #4298. |

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | [#4421](https://github.com/facebook/astryx/issues/4421) | Breadcrumb current item solo usa color para distinguirse |
| **Nuestro PR** | [#4605](https://github.com/facebook/astryx/pull/4605) | Non-color indicator (font-weight) en current breadcrumb → **OPEN**, MERGEABLE, sin reviews |
| **Contexto** | — | Abierto 31 Jul. WCAG 1.4.1 fix. |

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | [#4450](https://github.com/facebook/astryx/issues/4450) | Selector trigger sin accessible name |
| **Nuestro PR** | [#4604](https://github.com/facebook/astryx/pull/4604) | aria-labelledby en Selector trigger → **OPEN**, CONFLICTING, sin reviews |
| **Contexto** | — | Abierto 31 Jul. Tiene conflictos con main. |

### radix-ui/primitives

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | Select inside Dialog focus freeze |
| **Nuestro PR** | [#4053](https://github.com/radix-ui/primitives/pull/4053) | Sin review humano, sin CI. Changeset agregado 23 Jul |
| **Estado** | ⏳ Esperando review | — |

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | [#3636](https://github.com/radix-ui/primitives/issues/3636) | Select: aria-activedescendant y aria-selected fixes |
| **Nuestro PR** | [#4067](https://github.com/radix-ui/primitives/pull/4067) | aria-activedescendant + aria-selected fix → **OPEN**, sin reviews |
| **Contexto** | — | Abierto 22 Jul. Accesibilidad. |

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | [#3640](https://github.com/radix-ui/primitives/issues/3640) | DropdownMenu: ArrowUp debe abrir y focus último item |
| **Nuestro PR** | [#4066](https://github.com/radix-ui/primitives/pull/4066) | ArrowUp handling en DropdownMenu → **OPEN**, sin reviews |
| **Contexto** | — | Abierto 22 Jul. W3C APG pattern compliance. |

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | [#3619](https://github.com/radix-ui/primitives/issues/3619) | Slider: commit value on blur después de keyboard nav |
| **Nuestro PR** | [#4065](https://github.com/radix-ui/primitives/pull/4065) | Blur handler para commit → **OPEN**, sin reviews |
| **Contexto** | — | Abierto 22 Jul. |

### TanStack/router

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | [#7787](https://github.com/TanStack/router/issues/7787) | loaderDeps serializer falla con circular refs |
| **Nuestro PR** | [#7834](https://github.com/TanStack/router/pull/7834) | safeStringify approach. CI verde, sin issues |
| **Estado** | ⏳ Esperando review | — |

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | MatchInner throw undefined on cleared loadPromise |
| **Nuestro PR** | [#7861](https://github.com/TanStack/router/pull/7861) | **CLOSED** (no merged). schiller-manuel dijo que #7805 lo arreglará "properly" |
| **Estado** | ❌ Cerrado sin merge | — |

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | [#7873](https://github.com/TanStack/router/issues/7873) | serverFnFetcher loggea AbortError en consola |
| **Nuestro PR** | [#7878](https://github.com/TanStack/router/pull/7878) | Skip console.log para AbortError → **OPEN**, sin reviews |
| **Contexto** | — | Abierto 22 Jul. |

### vercel/ai

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | warn when reasoning tokens spent |
| **Nuestro PR** | [#17274](https://github.com/vercel/ai/pull/17274) | Review bot de Vercel addressado. Squash 22 Jul |
| **Estado** | ⏳ Esperando review humano | — |

### shadcn-ui/ui

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | [#11157](https://github.com/shadcn-ui/ui/issues/11157) | InputOTP slot transition layout shift |
| **Nuestro PR** | [#11179](https://github.com/shadcn-ui/ui/pull/11179) | Bloqueado por Vercel deploy (necesita autorización team shadcn-pro) |
| **Estado** | ⏳ Esperando | — |

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | [#11161](https://github.com/shadcn-ui/ui/issues/11161) | MessageScroller footer flicker |
| **Nuestro PR** | [#11180](https://github.com/shadcn-ui/ui/pull/11180) | Bloqueado por Vercel deploy |
| **Estado** | ⏳ Esperando | — |

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | remove scrollbar-none from table |
| **Nuestro PR** | [#11187](https://github.com/shadcn-ui/ui/pull/11187) | Bloqueado por Vercel deploy. barisgirismen comentó (25 Jul) que el fix es correcto y complementario a #11291 |
| **Estado** | ⏳ Esperando | — |

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | [#11157](https://github.com/shadcn-ui/ui/issues/11157) | InputOTP slot transition layout shift (mismo issue, approach alternativo) |
| **Nuestro PR** | [#11198](https://github.com/shadcn-ui/ui/pull/11198) | Prevent layout shift on keyboard nav → **OPEN**, 1 review (CodeRabbit) |
| **Contexto** | — | Abierto 16 Jul. Approach alternativo a #11179. |

### t3-oss/create-t3-app

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | biome ignore generated files |
| **Nuestro PR** | [#2239](https://github.com/t3-oss/create-t3-app/pull/2239) | CI verde, changeset listo, Vercel ready. Follow-up bump 31 Jul |
| **Estado** | ⏳ Esperando review | — |

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | prettier ignore generated Prisma client |
| **Nuestro PR** | [#2240](https://github.com/t3-oss/create-t3-app/pull/2240) | .prettierignore para generated Prisma → **OPEN**, MERGEABLE, 1 review |
| **Contexto** | — | Abierto 15 Jul. Complementario a #2239. |

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | Better Auth + Drizzle + PostgreSQL table prefix |
| **Nuestro PR** | [#2244](https://github.com/t3-oss/create-t3-app/pull/2244) | Fix table prefix placeholder → **OPEN**, MERGEABLE, sin reviews |
| **Contexto** | — | Abierto 30 Jul. |

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | [#2185](https://github.com/t3-oss/create-t3-app/issues/2185) | Clipboard copy button sin accessible label |
| **Nuestro PR** | [#2243](https://github.com/t3-oss/create-t3-app/pull/2243) | aria-label en clipboard button → **OPEN**, MERGEABLE, sin reviews |
| **Contexto** | — | Abierto 30 Jul. WCAG 4.1.2 fix. |

### shuding/nextra

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | select modal={false} |
| **Nuestro PR** | [#5029](https://github.com/shuding/nextra/pull/5029) | UNSTABLE es falso positivo, branch actualizado. Follow-up check-in 31 Jul |
| **Estado** | ⏳ Esperando review | — |

### payloadcms/payload

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | duplicate latest=true version rows |
| **Nuestro PR** | [#17413](https://github.com/payloadcms/payload/pull/17413) | **Review humano de sviat-barbutsa** (21 Jul). Fix addressado. Follow-up 31 Jul |
| **Estado** | ⏳ Esperando maintainer | — |

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | lexical blocks stale form state |
| **Nuestro PR** | [#17342](https://github.com/payloadcms/payload/pull/17342) | Sin review humano. Follow-up bump 31 Jul |
| **Estado** | ⏳ Esperando | — |

### google/skills

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | verify-revision-state recipe for Skill Registry |
| **Nuestro PR** | [#196](https://github.com/google/skills/pull/196) | CLA check falló (primera contribución a Google). Re-triggered 23 Jul |
| **Estado** | ⏳ Esperando CLA + review | — |

### swiftlang/swift-testing

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | [#686](https://github.com/swiftlang/swift-testing/issues/686) | Documentar patrón de `.serialized` en suites anidadas |
| **Nuestro PR** | [#1813](https://github.com/swiftlang/swift-testing/pull/1813) | **CLOSED** (no merged). harlanhaskins dijo que la guía quedaría obsoleta con el proposal de serialización. Gonzo cerró y dejó seguimiento. |
| **Estado** | ❌ Cerrado — hold hasta que avance el proposal | — |

### colinhacks/zod

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | [#6220](https://github.com/colinhacks/zod/issues/6220) | __proto__ no reportado como unrecognized key en strict mode |
| **Nuestro PR** | [#6222](https://github.com/colinhacks/zod/pull/6222) | Report __proto__ como unrecognized → **OPEN**, MERGEABLE, sin reviews |
| **Contexto** | — | Abierto 22 Jul. Security fix (prototype pollution defense preservado). |

### Nutlope/hallmark

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | [#22](https://github.com/Nutlope/hallmark/issues/22) | Cursor install instructions misleading |
| **Nuestro PR** | [#32](https://github.com/Nutlope/hallmark/pull/32) | Use native skills directory → **OPEN**, MERGEABLE, sin reviews |
| **Contexto** | — | Abierto 16 Jul. |

### ibelick/ui-skills

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | Improve fixing-accessibility skill |
| **Nuestro PR** | [#37](https://github.com/ibelick/ui-skills/pull/37) | WCAG 2.2 coverage → **OPEN**, sin reviews |
| **Contexto** | — | Abierto 16 Jul. |

---

## Reviews técnicas (sin PR propio)

| Repo | PR | Issue | Aporte |
|------|-----|-------|--------|
| TanStack/query | [#11036](https://github.com/TanStack/query/pull/11036) | [#10924](https://github.com/TanStack/query/issues/10924) | Floating promise, cleanup |
| TanStack/query | [#10994](https://github.com/TanStack/query/pull/10994) | [#10924](https://github.com/TanStack/query/issues/10924) | Análisis comparativo |
| vercel/ai | [#14983](https://github.com/vercel/ai/pull/14983) | [#12687](https://github.com/vercel/ai/issues/12687) | Test coverage gap |
| vercel/ai | [#13577](https://github.com/vercel/ai/pull/13577) | [#13506](https://github.com/vercel/ai/issues/13506) | Breaking change analysis |
| vercel/ai | [#12800](https://github.com/vercel/ai/pull/12800) | [#12799](https://github.com/vercel/ai/issues/12799) | RFC compliance, product/version separator |

---

## Clasificación de repos

### Tier 1 — Alta visibilidad, activos, alineados con el perfil

| Repo | ⭐ | PRs activos | Por qué encaja |
|------|-----|-------------|----------------|
| **facebook/astryx** | — | 3 | Design system de Meta. 3 PRs abiertos (#4298, #4605, #4604). Accesibilidad = especialización de Gonzo. Review de humbertovirtudes ya iniciado en #4298. |
| **radix-ui/primitives** | 16.5k | 4 | 4 PRs abiertos (#4053, #4065, #4066, #4067). Accesibilidad y UX. |
| **shadcn-ui/ui** | 119k | 4 | 4 PRs abiertos (#11179, #11180, #11187, #11198). Todos bloqueados por Vercel deploy. |
| **TanStack/router** | 14.8k | 2 | 2 PRs abiertos (#7834, #7878). 1 cerrado sin merge (#7861). |
| **t3-oss/create-t3-app** | 29k | 4 | 4 PRs abiertos (#2239, #2240, #2243, #2244). 2 con follow-up bump. |
| **payloadcms/payload** | 43.5k | 2 | 2 PRs abiertos (#17413, #17342). #17413 con review humano. Follow-ups hechos. |
| **vercel/ai** | 25.5k | 1 | 1 PR abierto (#17274). Review bot addressado. |

### Tier 2 — Buenos pero más esfuerzo o menos actividad

| Repo | ⭐ | PRs | Por qué |
|------|-----|-----|---------|
| **colinhacks/zod** | 38k | 1 | #6222 abierto. Security fix. |
| **shuding/nextra** | 13.8k | 1 | #5029 abierto. Follow-up check-in hecho. |
| **Nutlope/hallmark** | — | 1 | #32 abierto. Cursor install fix. |
| **ibelick/ui-skills** | — | 1 | #37 abierto. WCAG 2.2 skill. |
| **google/skills** | — | 1 | #196 abierto. CLA pendiente. |

### Tier 3 — Interesantes pero fríos ahora

| Repo | Por qué no ahora |
|------|-----------------|
| nextjs/saas-starter | Sin actividad en 30 días |
| pacocoursey/next-themes | Sin actividad en 30 días |
| vercel/commerce | 1 issue activo en 30 días |
| swiftlang/swift-testing | #1813 cerrado, esperando proposal |

### Candidatos futuros

- **supabase/supabase** — docs, examples, bugs en JS client. Lo usa diario.
- **openai/openai-node** — SDK que usa en varios proyectos
- **vitest-dev/vitest** — lo usa en CSN, podría contribuir docs o bugs

---

## Estado actual — Dashboard

### Totales

| Métrica | Valor |
|---------|-------|
| **PRs abiertos totales** | 24 |
| **PRs con review humano** | 2 (payload #17413, t3 #2240) |
| **PRs mergeados** | 0 |
| **PRs cerrados sin merge** | 2 (#7861, #1813) |
| **Repos con PRs activos** | 11 |
| **Follow-ups enviados (31 Jul)** | 4 (t3 #2239, nextra #5029, payload #17413, payload #17342) |

### Próximos pasos

1. **Esperar respuestas** a los follow-ups del 31 Jul (t3, nextra, payload ×2)
2. **astryx #4604** — resolver conflictos con main
3. **google/skills #196** — verificar estado del CLA
4. **No abrir nuevos PRs** hasta que al menos uno reciba review humano. El bottleneck sigue siendo maintainer review time.
5. **Próximo check:** 7-9 Ago si no hay movimiento antes
