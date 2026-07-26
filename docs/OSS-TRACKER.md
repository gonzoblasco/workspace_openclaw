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

### radix-ui/primitives

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | Select inside Dialog focus freeze |
| **Nuestro PR** | [#4053](https://github.com/radix-ui/primitives/pull/4053) | Sin review humano, sin CI. Changeset agregado 23 Jul |
| **Estado** | ⏳ Esperando review | — |

### TanStack/router

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | [#7787](https://github.com/TanStack/router/issues/7787) | loaderDeps serializer falla con circular refs |
| **Nuestro PR** | [#7834](https://github.com/TanStack/router/pull/7834) | safeStringify approach. CI verde, sin issues |
| **Estado** | ⏳ Esperando review | — |

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | MatchInner throw undefined on cleared loadPromise |
| **Nuestro PR** | [#7861](https://github.com/TanStack/router/pull/7861) | CodeRabbit issues addressados 23 Jul. CI verde |
| **Estado** | ⏳ Esperando review | — |

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
| **Nuestro PR** | [#11187](https://github.com/shadcn-ui/ui/pull/11187) | Bloqueado por Vercel deploy |
| **Estado** | ⏳ Esperando | — |

### t3-oss/create-t3-app

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | biome ignore generated files |
| **Nuestro PR** | [#2239](https://github.com/t3-oss/create-t3-app/pull/2239) | CI verde, changeset listo, Vercel ready |
| **Estado** | ⏳ Esperando review | — |

### shuding/nextra

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | select modal={false} |
| **Nuestro PR** | [#5029](https://github.com/shuding/nextra/pull/5029) | UNSTABLE es falso positivo, branch actualizado |
| **Estado** | ⏳ Esperando review | — |

### payloadcms/payload

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | duplicate latest=true version rows |
| **Nuestro PR** | [#17413](https://github.com/payloadcms/payload/pull/17413) | **Review humano de sviat-barbutsa** (21 Jul). Fix addressado. BLOCKED (falta CI de payload) |
| **Estado** | ⏳ Esperando maintainer | — |

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | lexical blocks stale form state |
| **Nuestro PR** | [#17342](https://github.com/payloadcms/payload/pull/17342) | Sin review humano. Sin CI. BLOCKED |
| **Estado** | ⏳ Esperando | — |

### google/skills

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | — | verify-revision-state recipe for Skill Registry |
| **Nuestro PR** | [#196](https://github.com/google/skills/pull/196) | Abierto 23 Jul |
| **Estado** | ⏳ Esperando review | — |

### swiftlang/swift-testing

| Eslabón | Link | Detalle |
|---------|------|--------|
| **Issue** | [#686](https://github.com/swiftlang/swift-testing/issues/686) | Documentar patrón de `.serialized` en suites anidadas |
| **Nuestro PR** | [#1813](https://github.com/swiftlang/swift-testing/pull/1813) | Nueva sección "Serializing suites across multiple files" en Parallelization.md |
| **Estado** | ⏳ Esperando review | — |

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

| Repo | ⭐ | Actividad (30d) | Por qué encaja |
|------|-----|-----------------|----------------|
| **facebook/astryx** | — | Muy activo | Design system de Meta. PR #4298 abierto (default a11y labels). Accesibilidad = especialización de Gonzo. Review de humbertovirtudes ya iniciado. |
| **shadcn-ui/ui** | 119k | 50 issues activos | Lo usa en SoporteML. 2 PRs abiertos (#11179, #11180). Issues se cubren rápido — verificar sin PRs antes de atacar. |
| **TanStack/router** | 14.8k | 50 issues activos | Lo usa en kanamai, reactiva, umbrawriter. PR #7818 abierto (loaderDeps serializer). 8 issues sin PRs disponibles. |
| **TanStack/query** | 50k | 19 issues activos | Lo usa en todos lados. Reviews técnicas dejadas en PRs #11036 y #10994. Issues muy competidos (3-4 PRs por issue). |
| **vercel/ai** | 25.5k | 50 issues activos | AI SDK de Vercel. 1729 issues abiertos. 3 reviews técnicas dejadas en PRs existentes. Mucho scope para PR propio. |
| **payloadcms/payload** | 43.5k | 50 issues activos | CMS fullstack Next.js. Stack muy parecido. Mucha superficie de bugs. |

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
| google/skills | [#196](https://github.com/google/skills/pull/196) abierto, esperando review |

### Candidatos futuros

- **supabase/supabase** — docs, examples, bugs en JS client. Lo usa diario. #6435 (good first issue: newlines in SMS OTP) disponible.
- **openai/openai-node** — SDK que usa en varios proyectos
- **vitest-dev/vitest** — lo usa en CSN, podría contribuir docs o bugs

---

## Estado actual — Plan de ataque

### Semana 1-2 — shadcn-ui/ui + TanStack/router + create-next-stack ✅ HECHO

| Issue | PR | Estado |
|-------|-----|--------|
| shadcn #11157 Input OTP layout shift | [#11179](https://github.com/shadcn-ui/ui/pull/11179) | Abierto, esperando review + Vercel deploy |
| shadcn #11161 MessageScroller footer flicker | [#11180](https://github.com/shadcn-ui/ui/pull/11180) | Abierto, esperando review + Vercel deploy |
| shadcn #11104 Sidebar Cmd+B | Descartado | 4 PRs competidores, saturado |
| TanStack/router #7787 loaderDeps serializer | [#7834](https://github.com/TanStack/router/pull/7834) | Abierto, safeStringify approach (reemplaza #7818 cerrado) |

### Semana 2-3 — Payload + Radix + TanStack fixes ✅ HECHO

| Acción | PR | Detalle |
|--------|-----|--------|
| Changeset agregado | radix-ui #4053 | .changeset/slick-emus-show.md pusheado 23 Jul |
| CodeRabbit fixes | TanStack/router #7861 | getDerivedStateFromProps + pending-promise guards pusheados 23 Jul |
| Rebase verificado | nextra #5029 | Branch actualizado con main, UNSTABLE es falso positivo |
| Estado documentado | payload #17413 | Review de sviat addressado, esperando maintainer |

### Próximos pasos

1. **Esperar reviews** de todos los PRs (1-2 semanas desde última actividad)
2. **facebook/astryx #4298** — recién abierto 24 Jul, esperar review de @humbertovirtudes. Si en 7 días no hay movimiento, follow-up.
3. **payloadcms/payload #17413** — el más cercano al merge. Si en 7 días no hay movimiento, considerar follow-up comment
4. **shadcn-ui/ui ×3** — si en 14 días no hay actividad, hacer follow-up comment amigable
5. **No abrir nuevos PRs** hasta que al menos uno de los existentes reciba review humano. El bottleneck es maintainer review, no producción de código.
