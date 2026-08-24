# OSS-TRACKER.md - Open Source Contributions Tracker

> Generado desde memory/memory.db (tabla contributions). Fuente de verdad: la DB.
> Regenerar con: ./scripts/memory-db.sh export-oss

## Estado actual

| Métrica | Valor |
|---------|-------|
| PRs abiertos | 16 |
| PRs mergeados | 3 |
| PRs cerrados sin merge | 18 |
| Repos con PRs | 18 |

## PR Registry

### NousResearch/hermes-agent

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#38072](https://github.com/NousResearch/hermes-agent/issues/38072) | Issue OPEN de a11y del Desktop renderer (apps/desktop). Audit de andrea9292 (03/06): 6 findings. Gonzo comento 05/08 ofreciendose a trabajar. RE-AUDIT publicado por Gonzo 24/08 contra main actual: #3 nested-interactive VIGENTE (reclamado por elchic00), #5 sin h1/landmarks VIGENTE, #4 contraste VIGENTE, #6 hit targets VIGENTE, #1 aria-hidden-focus MEJORADO (invisible+pointer-events-none), #2 resize separator RESUELTO (ya no es focusable). Comentario: issuecomment-5393570919. |
| **Nuestro PR** | []() | **open** |
| **Contexto** | - | Colaborativo, no competitivo: elchic00 reclamo el finding #3 (24/08) y tiene PR en curso - NO abrir PR para eso. Gonzo aporto re-audit verificando que findings siguen vivos tras refactor a tree/renderer/. Ofrecio ayudar a revisar el fix del #3 o tomar el #5. |

### Nutlope/hallmark

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#22](https://github.com/Nutlope/hallmark/issues/22) | Cerrado 22/08 por inactividad (1 mes sin review del maintainer). Branch eliminado. Comentario de cierre publicado. |
| **Nuestro PR** | [#32](https://github.com/Nutlope/hallmark/pull/32) | **closed** |
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

### adobe/react-spectrum

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | fix(react-aria): aria-posinset global across sections en listbox. Agosto. |
| **Nuestro PR** | [#10487]() | **open** |

### carbon-design-system/carbon

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | ComposedModal: add aria-describedby prop support. Agosto, sin review. |
| **Nuestro PR** | [#22887]() | **open** |

### colinhacks/zod

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#6220](https://github.com/colinhacks/zod/issues/6220) | Cerrado (verificado 22/08 - el PR ya no estaba abierto). |
| **Nuestro PR** | [#6222](https://github.com/colinhacks/zod/pull/6222) | **closed** |
| **Contexto** | - | Abierto 22 Jul. Security fix (prototype pollution defense preservado). |

### facebook/astryx

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#4143](https://github.com/facebook/astryx/issues/4143) | Cerrado 22/08 por redundante: main absorbió el fix vía #4157 (default label por variante) y #5034 (composición vía AvatarStatusLabelContext). Comentario de cierre publicado agradeciendo a imdreamrunner. Lección: verificar contra main antes de force-pushear rebases viejos. |
| **Nuestro PR** | [#4298](https://github.com/facebook/astryx/pull/4298) | **closed** |
| **Contexto** | - | Gonzo abrió #4218 primero (icon+label). humbertovirtudes sugirió converger con #4157 por ser base más sólida. PR #4218 cerrado, contenido migrado a #4298. |

| **Issue** | [#4421](https://github.com/facebook/astryx/issues/4421) | MERGED 23/08. Non-color indicator (font-weight semibold) en current breadcrumb. Aprobado por cixzhang. Resuelve #4421 (WCAG 1.4.1 Use of Color). |
| **Nuestro PR** | [#4605](https://github.com/facebook/astryx/pull/4605) | **merged** |
| **Contexto** | - | Abierto 31 Jul. WCAG 1.4.1 fix. |

| **Issue** | [#4450](https://github.com/facebook/astryx/issues/4450) | Cerrado (verificado 22/08 - el PR ya no estaba abierto). |
| **Nuestro PR** | [#4604](https://github.com/facebook/astryx/pull/4604) | **closed** |
| **Contexto** | - | Abierto 31 Jul. Tiene conflictos con main. |

| **Issue** | [#3654]() | WCAG 2.1 AA contrast failures en core color tokens. CHANGES_REQUESTED (ernestt), trabajado 22/08. Solo border-emphasized tras revert de disabled. |
| **Nuestro PR** | [#4022]() | **open** |

| **Issue** | [#4994]() | Cerrado 23/08 sin merge. Diagnostico correcto (bug a11y critico axe), pero eligieron PR #5107 con aria-hidden: presentation no permite aria-orientation que Divider siempre escribe, trade aria-required-children por aria-allowed-attr (critica x2). Maintainer invita a seguir contribuyendo. |
| **Nuestro PR** | [#5344]() | **closed** |

| **Issue** | [#4912](https://github.com/facebook/astryx/issues/4912) | MERGED 24/08. build-storybook fallaba con no merge base en PRs viejos (fetch-depth 50). Fix: two-dot diff fallback en analyze-pr.js. Resuelve #4912. Merge commit 152e956. |
| **Nuestro PR** | [#4914](https://github.com/facebook/astryx/pull/4914) | **merged** |
| **Contexto** | - | Abierto 11 Ago. Aprobado por cixzhang 24/08 (los 5 findings del review del 12/08 fueron addressados). FOLLOW-UP sugerido por cixzhang: --deepen=200 solo cubre ~250 commits atras, y 55 de 122 PRs stale estan mas atras - valdria un segundo deepen. |

### google/skills

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | Cerrado 22/08 por Gonzo (decisión propia). |
| **Nuestro PR** | [#196](https://github.com/google/skills/pull/196) | **closed** |

### ibelick/ui-skills

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | Cerrado 22/08 por inactividad (1 mes sin review del maintainer). Branch eliminado. Comentario de cierre publicado. |
| **Nuestro PR** | [#37](https://github.com/ibelick/ui-skills/pull/37) | **closed** |
| **Contexto** | - | Abierto 16 Jul. |

### mui/base-ui

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | [combobox] Remove invalid aria-orientation from grid role. Agosto. |
| **Nuestro PR** | [#5551]() | **open** |

### mui/material-ui

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#48990](https://github.com/mui/material-ui/issues/48990) | MERGED 24/08. [docs][templates] Remove focusable links from hidden carousel slides. WCAG 4.1.2 aria-hidden-focus: el carousel (react-swipeable-views) esconde slides inactivos con aria-hidden pero el link Go to store seguia focusable. Fix: tabIndex={-1} en slides inactivos (1 archivo, +1 -0). Aprobado por silviuaavram. Resuelve #48990 (cerrado COMPLETED). |
| **Nuestro PR** | [#49003]() | **merged** |
| **Contexto** | - | Abierto en agosto. PR de docs (templates). Merge 06:44 UTC 24/08. |

### payloadcms/payload

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | Cerrado 22/08 por inactividad (1 mes sin review del maintainer). Branch eliminado. Comentario de cierre publicado. |
| **Nuestro PR** | [#17413](https://github.com/payloadcms/payload/pull/17413) | **closed** |

| **Issue** | - | Cerrado 22/08 por inactividad (1 mes sin review del maintainer). Branch eliminado. Comentario de cierre publicado. |
| **Nuestro PR** | [#17342](https://github.com/payloadcms/payload/pull/17342) | **closed** |

### radix-ui/primitives

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | Cerrado 22/08 por inactividad (1 mes sin review del maintainer). Branch eliminado. Comentario de cierre publicado. |
| **Nuestro PR** | [#4053](https://github.com/radix-ui/primitives/pull/4053) | **closed** |

| **Issue** | [#3636](https://github.com/radix-ui/primitives/issues/3636) | Cerrado 22/08 por inactividad (1 mes sin review del maintainer). Branch eliminado. Comentario de cierre publicado. |
| **Nuestro PR** | [#4067](https://github.com/radix-ui/primitives/pull/4067) | **closed** |
| **Contexto** | - | Abierto 22 Jul. Accesibilidad. |

| **Issue** | [#3640](https://github.com/radix-ui/primitives/issues/3640) | Cerrado 22/08 por inactividad (1 mes sin review del maintainer). Branch eliminado. Comentario de cierre publicado. |
| **Nuestro PR** | [#4066](https://github.com/radix-ui/primitives/pull/4066) | **closed** |
| **Contexto** | - | Abierto 22 Jul. W3C APG pattern compliance. |

| **Issue** | [#3619](https://github.com/radix-ui/primitives/issues/3619) | Cerrado 22/08 por inactividad (1 mes sin review del maintainer). Branch eliminado. Comentario de cierre publicado. |
| **Nuestro PR** | [#4065](https://github.com/radix-ui/primitives/pull/4065) | **closed** |
| **Contexto** | - | Abierto 22 Jul. |

| **Issue** | - | Select: announce option position/total para screen readers. Agosto. |
| **Nuestro PR** | [#4109]() | **open** |

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

| **Issue** | [#11465]() | fix(react): drain released tail spacer tras scroll manual. Agosto. |
| **Nuestro PR** | [#11465]() | **open** |

### shuding/nextra

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | Cerrado 22/08 por inactividad (1 mes sin review del maintainer). Branch eliminado. Comentario de cierre publicado. |
| **Nuestro PR** | [#5029](https://github.com/shuding/nextra/pull/5029) | **closed** |

### swiftlang/swift-testing

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#686](https://github.com/swiftlang/swift-testing/issues/686) | Documentar patrón de .serialized en suites anidadas. CLOSED (no merged). harlanhaskins dijo que la guía quedaría obsoleta con el proposal de serialización. Hold hasta que avance el proposal. |
| **Nuestro PR** | [#1813](https://github.com/swiftlang/swift-testing/pull/1813) | **closed** |

### t3-oss/create-t3-app

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | Cerrado 22/08 por consolidación de PRs (tooling genérico sin reviews, 1 mes). Branch eliminado. |
| **Nuestro PR** | [#2239](https://github.com/t3-oss/create-t3-app/pull/2239) | **closed** |

| **Issue** | - | .prettierignore para generated Prisma. MERGEABLE, 1 review. |
| **Nuestro PR** | [#2240](https://github.com/t3-oss/create-t3-app/pull/2240) | **open** |
| **Contexto** | - | Abierto 15 Jul. Complementario a #2239. |

| **Issue** | - | Cerrado 22/08 por consolidación de PRs (tooling genérico sin reviews, 1 mes). Branch eliminado. |
| **Nuestro PR** | [#2244](https://github.com/t3-oss/create-t3-app/pull/2244) | **closed** |
| **Contexto** | - | Abierto 30 Jul. |

| **Issue** | [#2185](https://github.com/t3-oss/create-t3-app/issues/2185) | aria-label en clipboard button. MERGEABLE, sin reviews. |
| **Nuestro PR** | [#2243](https://github.com/t3-oss/create-t3-app/pull/2243) | **open** |
| **Contexto** | - | Abierto 30 Jul. WCAG 4.1.2 fix. |

### vercel/ai

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | warn when reasoning tokens spent. Review bot de Vercel addressado. Squash 22 Jul. |
| **Nuestro PR** | [#17274](https://github.com/vercel/ai/pull/17274) | **waiting_review** |

