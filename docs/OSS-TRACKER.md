# OSS-TRACKER.md - Open Source Contributions Tracker

> Generado desde memory/memory.db (tabla contributions). Fuente de verdad: la DB.
> Regenerar con: ./scripts/memory-db.sh export-oss

## Estado actual

| Métrica | Valor |
|---------|-------|
| PRs abiertos | 27 |
| PRs mergeados | 0 |
| PRs cerrados sin merge | 2 |
| Repos con PRs | 15 |

## PR Registry

### Nutlope/hallmark

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#22](https://github.com/Nutlope/hallmark/issues/22) | Use native skills directory. MERGEABLE, sin reviews. |
| **Nuestro PR** | [#32](https://github.com/Nutlope/hallmark/pull/32) | **open** |
| **Contexto** | - | Abierto 16 Jul. |

### TanStack/router

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#7787](https://github.com/TanStack/router/issues/7787) | safeStringify approach. CI verde, sin issues. |
| **Nuestro PR** | [#7834](https://github.com/TanStack/router/pull/7834) | **waiting_review** |

| **Issue** | - | MatchInner throw undefined on cleared loadPromise. CLOSED (no merged). schiller-manuel dijo que #7805 lo arreglará properly. |
| **Nuestro PR** | [#7861](https://github.com/TanStack/router/pull/7861) | **closed** |

| **Issue** | [#7873](https://github.com/TanStack/router/issues/7873) | Skip console.log para AbortError. Sin reviews. |
| **Nuestro PR** | [#7878](https://github.com/TanStack/router/pull/7878) | **open** |
| **Contexto** | - | Abierto 22 Jul. |

### colinhacks/zod

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#6220](https://github.com/colinhacks/zod/issues/6220) | Report __proto__ como unrecognized. MERGEABLE, sin reviews. |
| **Nuestro PR** | [#6222](https://github.com/colinhacks/zod/pull/6222) | **open** |
| **Contexto** | - | Abierto 22 Jul. Security fix (prototype pollution defense preservado). |

### facebook/astryx

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#4143](https://github.com/facebook/astryx/issues/4143) | Default accessible labels (Online/Away/Busy). Esperando review de @humbertovirtudes. |
| **Nuestro PR** | [#4298](https://github.com/facebook/astryx/pull/4298) | **open** |
| **Contexto** | - | Gonzo abrió #4218 primero (icon+label). humbertovirtudes sugirió converger con #4157 por ser base más sólida. PR #4218 cerrado, contenido migrado a #4298. |

| **Issue** | [#4421](https://github.com/facebook/astryx/issues/4421) | Non-color indicator (font-weight) en current breadcrumb. **MERGEABLE, scope limpio, respaldado por auditoría #5332.** Sin reviews. |
| **Nuestro PR** | [#4605](https://github.com/facebook/astryx/pull/4605) | **open** |
| **Contexto** | - | Abierto 31 Jul. WCAG 1.4.1 fix. **22/08: audit #5332 (Breadcrumbs) cita este PR como la fix canónica de B8 y no lo toca para no pisarlo. Scope limpiado (se sacaron los commits de #3654 que ya viven en #4022). Rebaseado sobre upstream/main. Comment publicado pidiendo review citando el respaldo.** |

| **Issue** | [#3654](https://github.com/facebook/astryx/issues/3654) | Contraste WCAG 2.1 AA en tokens core. **Reactivado 22/08: body actualizado (solo border-emphasized tras revert de disabled), comment con @ernestt, MERGEABLE.** |
| **Nuestro PR** | [#4022](https://github.com/facebook/astryx/pull/4022) | **open** |
| **Contexto** | - | Abierto 16 Jul. ernestt pidió CHANGES_REQUESTED (disabled tokens exentos bajo SC 1.4.3). Gonzalo revirtió text/icon-disabled, quedó solo border-emphasized (borde activo, SC 1.4.11). Quedó dormido 3 semanas en CHANGES_REQUESTED. 22/08: body actualizado + comment citando auditoría #5332 + @ernestt. Falta re-review humano. |

| **Issue** | [#4450](https://github.com/facebook/astryx/issues/4450) | aria-labelledby en Selector trigger. CONFLICTING, sin reviews. |
| **Nuestro PR** | [#4604](https://github.com/facebook/astryx/pull/4604) | **open** |
| **Contexto** | - | Abierto 31 Jul. Tiene conflictos con main. |

| **Issue** | [#4994](https://github.com/facebook/astryx/issues/4994) | Divider role=separator dentro de role=listbox (crítico axe). **PR nuevo 22/08, MERGEABLE, CI corriendo.** |
| **Nuestro PR** | [#5344](https://github.com/facebook/astryx/pull/5344) | **open** |
| **Contexto** | - | 22/08: detectado en scan a11y recurrente. Bug crítico axe aria-required-children (WCAG 1.3.1/4.1.2). Fix: dividers dentro del listbox pasan a role=presentation; Divider acepta role override. Fix en Selector + MultiSelector + tests + changeset. **Candidato a PR propio de a11y (no competía por issues tomados).** |

### google/skills

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | verify-revision-state recipe for Skill Registry. CLA check falló (primera contribución a Google). Re-triggered 23 Jul. |
| **Nuestro PR** | [#196](https://github.com/google/skills/pull/196) | **waiting_review** |

### ibelick/ui-skills

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | WCAG 2.2 coverage. Sin reviews. |
| **Nuestro PR** | [#37](https://github.com/ibelick/ui-skills/pull/37) | **open** |
| **Contexto** | - | Abierto 16 Jul. |

### openclaw/openclaw

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#127212](https://github.com/openclaw/openclaw/issues/127212) | expose active split pane to assistive tech (aria-current=true en pane activo). Cierra #127212. Sin cambio visual. Nace de feedback de gonzoblasco en #126714. Tests: aria-current migra tras pointerdown. |
| **Nuestro PR** | [#127213](https://github.com/openclaw/openclaw/pull/127213) | **open** |
| **Contexto** | - | Maintainer convirtio feedback de a11y en PR con tests. Portfolio vivo. |

### payloadcms/payload

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | duplicate latest=true version rows. Review humano de sviat-barbutsa (21 Jul). Fix addressado. Follow-up 31 Jul. |
| **Nuestro PR** | [#17413](https://github.com/payloadcms/payload/pull/17413) | **waiting_review** |

| **Issue** | - | lexical blocks stale form state. Sin review humano. Follow-up bump 31 Jul. |
| **Nuestro PR** | [#17342](https://github.com/payloadcms/payload/pull/17342) | **waiting_review** |

### radix-ui/primitives

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | Select inside Dialog focus freeze. Sin review humano, sin CI. Changeset agregado 23 Jul. |
| **Nuestro PR** | [#4053](https://github.com/radix-ui/primitives/pull/4053) | **waiting_review** |

| **Issue** | [#3636](https://github.com/radix-ui/primitives/issues/3636) | aria-activedescendant + aria-selected fix. Sin reviews. |
| **Nuestro PR** | [#4067](https://github.com/radix-ui/primitives/pull/4067) | **open** |
| **Contexto** | - | Abierto 22 Jul. Accesibilidad. |

| **Issue** | [#3640](https://github.com/radix-ui/primitives/issues/3640) | ArrowUp handling en DropdownMenu. Sin reviews. |
| **Nuestro PR** | [#4066](https://github.com/radix-ui/primitives/pull/4066) | **open** |
| **Contexto** | - | Abierto 22 Jul. W3C APG pattern compliance. |

| **Issue** | [#3619](https://github.com/radix-ui/primitives/issues/3619) | Blur handler para commit. Sin reviews. |
| **Nuestro PR** | [#4065](https://github.com/radix-ui/primitives/pull/4065) | **open** |
| **Contexto** | - | Abierto 22 Jul. |

### shadcn-ui/ui

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#11157](https://github.com/shadcn-ui/ui/issues/11157) | InputOTP slot transition layout shift. Bloqueado por Vercel deploy (necesita autorización team shadcn-pro). |
| **Nuestro PR** | [#11179](https://github.com/shadcn-ui/ui/pull/11179) | **waiting_review** |

| **Issue** | [#11161](https://github.com/shadcn-ui/ui/issues/11161) | MessageScroller footer flicker. Bloqueado por Vercel deploy. |
| **Nuestro PR** | [#11180](https://github.com/shadcn-ui/ui/pull/11180) | **waiting_review** |

| **Issue** | - | remove scrollbar-none from table. Bloqueado por Vercel deploy. barisgirismen comentó (25 Jul) que el fix es correcto y complementario a #11291. |
| **Nuestro PR** | [#11187](https://github.com/shadcn-ui/ui/pull/11187) | **waiting_review** |

| **Issue** | [#11157](https://github.com/shadcn-ui/ui/issues/11157) | Prevent layout shift on keyboard nav. 1 review (CodeRabbit). |
| **Nuestro PR** | [#11198](https://github.com/shadcn-ui/ui/pull/11198) | **open** |
| **Contexto** | - | Abierto 16 Jul. Approach alternativo a #11179. |

### shuding/nextra

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | select modal={false}. UNSTABLE es falso positivo, branch actualizado. Follow-up check-in 31 Jul. |
| **Nuestro PR** | [#5029](https://github.com/shuding/nextra/pull/5029) | **waiting_review** |

### swiftlang/swift-testing

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#686](https://github.com/swiftlang/swift-testing/issues/686) | Documentar patrón de .serialized en suites anidadas. CLOSED (no merged). harlanhaskins dijo que la guía quedaría obsoleta con el proposal de serialización. Hold hasta que avance el proposal. |
| **Nuestro PR** | [#1813](https://github.com/swiftlang/swift-testing/pull/1813) | **closed** |

### t3-oss/create-t3-app

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | biome ignore generated files. CI verde, changeset listo, Vercel ready. Follow-up bump 31 Jul. |
| **Nuestro PR** | [#2239](https://github.com/t3-oss/create-t3-app/pull/2239) | **waiting_review** |

| **Issue** | - | .prettierignore para generated Prisma. MERGEABLE, 1 review. |
| **Nuestro PR** | [#2240](https://github.com/t3-oss/create-t3-app/pull/2240) | **open** |
| **Contexto** | - | Abierto 15 Jul. Complementario a #2239. |

| **Issue** | - | Fix table prefix placeholder. MERGEABLE, sin reviews. |
| **Nuestro PR** | [#2244](https://github.com/t3-oss/create-t3-app/pull/2244) | **open** |
| **Contexto** | - | Abierto 30 Jul. |

| **Issue** | [#2185](https://github.com/t3-oss/create-t3-app/issues/2185) | aria-label en clipboard button. MERGEABLE, sin reviews. |
| **Nuestro PR** | [#2243](https://github.com/t3-oss/create-t3-app/pull/2243) | **open** |
| **Contexto** | - | Abierto 30 Jul. WCAG 4.1.2 fix. |

### trekhleb/javascript-algorithms

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#2057](https://github.com/trekhleb/javascript-algorithms/issues/2057) | Return ordered cycle path array instead of parent mapping in detectUndirectedCycle. APPROVED por m-coder567 (Milan Parmar) + COMMENTED positivo por daltino (Dalton Whyte). MERGEABLE, 587 tests. |
| **Nuestro PR** | [#2198](https://github.com/trekhleb/javascript-algorithms/pull/2198) | **open** |
| **Contexto** | - | Repo EDUCATIVO (algoritmos y estructuras de datos con explicaciones, para preparacion de entrevistas). Los PRs son contribuciones de aprendizaje, no fixes de produccion. 100+ PRs abiertos es la naturaleza del repo (popular, muchos contributors). El maintainer mergea en batches a su ritmo, sin urgencia. PR bien hecho, aprobado, mergeable. Se agradecio a los reviewers por nombre (Milan y Dalton). |

### vercel/ai

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | warn when reasoning tokens spent. Review bot de Vercel addressado. Squash 22 Jul. |
| **Nuestro PR** | [#17274](https://github.com/vercel/ai/pull/17274) | **waiting_review** |

