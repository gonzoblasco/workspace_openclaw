# OSS-TRACKER.md - Open Source Contributions Tracker

> Generado desde memory/memory.db (tabla contributions). Fuente de verdad: la DB.
> Regenerar con: ./scripts/memory-db.sh export-oss

## Estado actual

| Métrica | Valor |
|---------|-------|
| PRs abiertos | 18 |
| PRs mergeados | 6 |
| PRs cerrados sin merge | 19 |
| Colaboraciones no-codigo | 6 |
| Repos con contribuciones | 19 |

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

| **Issue** | [#10220](https://github.com/adobe/react-spectrum/issues/10220) | fix(react-aria): only announce combobox section changes to VoiceOver |
| **Nuestro PR** | [#10503](https://github.com/adobe/react-spectrum/pull/10503) | **open** |
| **Contexto** | - | Gate del announcement effect a solo cambios de seccion. Maintainer LFDanLu dio luz verde 24/08. 218 + 41 tests pass. Comentado en issue. |

| **Issue** | [https://github.com/adobe/react-spectrum/issues/9687](a11y) | fix: expose input styling on RAC Checkbox and Radio (inputClassName/inputStyle) |
| **Nuestro PR** | [10517](https://github.com/adobe/react-spectrum/pull/10517) | **open** |
| **Contexto** | - | 9687 |

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

| **Issue** | [#3654](https://github.com/facebook/astryx/issues/3654) | CERRADO 28/08 por ownership (no por calidad). PR aprobado 2x por cixzhang (27/08) tras limpiar scripts + regenerar tokens.doc.mjs. Cierre: issue #3654 ya asignado a @rubyycheung y programa coordinado en #4475 (a11y + design ownership). Leccion: chequear si el issue ya esta ASIGNADO (no solo abierto) antes de abrir PR en astryx. Audit y metodologia quedaron documentados en la conversacion. |
| **Nuestro PR** | [#4022](https://github.com/facebook/astryx/pull/4022) | **closed** |

| **Issue** | [#4994]() | Cerrado 23/08 sin merge. Diagnostico correcto (bug a11y critico axe), pero eligieron PR #5107 con aria-hidden: presentation no permite aria-orientation que Divider siempre escribe, trade aria-required-children por aria-allowed-attr (critica x2). Maintainer invita a seguir contribuyendo. |
| **Nuestro PR** | [#5344]() | **closed** |

| **Issue** | [#4912](https://github.com/facebook/astryx/issues/4912) | MERGED 24/08. build-storybook fallaba con no merge base en PRs viejos (fetch-depth 50). Fix: two-dot diff fallback en analyze-pr.js. Resuelve #4912. Merge commit 152e956. |
| **Nuestro PR** | [#4914](https://github.com/facebook/astryx/pull/4914) | **merged** |
| **Contexto** | - | Abierto 11 Ago. Aprobado por cixzhang 24/08 (los 5 findings del review del 12/08 fueron addressados). FOLLOW-UP sugerido por cixzhang: --deepen=200 solo cubre ~250 commits atras, y 55 de 122 PRs stale estan mas atras - valdria un segundo deepen. |

| **Issue** | [#5049](https://github.com/facebook/astryx/issues/5049) | MERGED 24/08. HoverCard con label expone rich card como dialog popup (no como descripcion). Trigger ahora usa aria-haspopup=dialog + aria-controls (gateado en open state, como DateInput) + aria-expanded sincronizado. useHoverCard expone id e isOpen; describedBy queda como alias deprecado. Sin label mantiene aria-describedby (role=group). Merge commit f4d494c. 38 tests pass, a11y audit sin violaciones. |
| **Nuestro PR** | [#5419](https://github.com/facebook/astryx/pull/5419) | **merged** |
| **Contexto** | - | Abierto 24/08. Review de cixzhang con 3 comentarios, todos addressados: label en el hook template, merge (no overwrite) de atributos popup existentes del trigger, y gating de aria-controls en open state. Re-review y merge el mismo dia. Commits 52262da7 + c1603cad. |

| **Issue** | [#5476](https://github.com/facebook/astryx/issues/5476) | MERGED 26/08. TreeList forward BaseProps: aria-label/aria-labelledby al <ul role=tree>, header visible gana, role despues del rest. Bug a11y: tree sin header no podia nombrarse. |
| **Nuestro PR** | [#5493](https://github.com/facebook/astryx/pull/5493) | **merged** |
| **Contexto** | - | Abierto 25/08. 3 reviews de cixzhang (2 CHANGES_REQUESTED + 1 APPROVED): acotar a TreeList (List va en #5288), aria-label al ul no al div, header visible gana sobre caller aria-labelledby. Merge 26/08. Es a11y -> dispara post LinkedIn nicho a11y. |

### facebook/docusaurus

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#11332](https://github.com/facebook/docusaurus/issues/11332) | fix(theme-classic): announce page title on route change for screen readers |
| **Nuestro PR** | [#12387](https://github.com/facebook/docusaurus/pull/12387) | **open** |
| **Contexto** | - | Focus management: pasa el titulo del Layout al SkipToContent y lo anuncia en route change. WestonThayer valido el enfoque. 116 + 51 tests pass. Comentado en issue. |

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
| **Issue** | [#5548](https://github.com/mui/base-ui/issues/5548) | MERGED 24/08. [combobox][menu][select] Move aria-orientation to the role owners. Grid Combobox/Autocomplete emitian aria-orientation=horizontal pero el role grid no lo soporta. Fix: mover aria-orientation a los role owners, omitirlo en grid/presentation, preservando navegacion. 7 archivos +69 -4 con tests de regresion. Aprobado por atomiks. Resuelve #5548. |
| **Nuestro PR** | [#5551]() | **merged** |
| **Contexto** | - | El Codex bot (20/08) senalo P1: omitir orientation rompia la navegacion horizontal del grid. Gonzo lo addresso separando la orientacion de navegacion del atributo ARIA (strip aria-orientation de listProps en grid). Buen ejemplo de atender feedback de bot con solucion correcta. |

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

| **Issue** | [https://github.com/shadcn-ui/ui/issues/11125](collab) | Publicado comment reactivacion en issue #11125 (issuecomment-5473908810) como autor del fix: cerre compatibilidad con PR gemelo #11223 (doneumark) + senale cuello de botella de 3 semanas sin re-review. PR #11465 sigue OPEN, REVIEW_REQUIRED. |
| **Nuestro PR** | [11465](https://github.com/shadcn-ui/ui/pull/11465) | **open** |
| **Contexto** | - | 11125 |

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

## Colaboraciones no-codigo

> Contribuciones donde el aporte de Gonzo fue comentario, review, audit o diagnostico (no un PR con merge a su nombre). Impacto real via PRs de otros o conversaciones.

| Repo | Eslabón | Detalle |
|------|---------|---------|
| NousResearch/hermes-agent | [#38072](https://github.com/NousResearch/hermes-agent/issues/38072) | COLABORACION NO-CODIGO. Re-audit de a11y publicado como comentario (24/08): verifico contra main actual que findings siguen vivos (#3,#4,#5,#6) y cuales se mitigaron (#1 mejorado, #2 resuelto). Comentario issuecomment-5393570919. |
| facebook/astryx | [#3764](https://github.com/facebook/astryx/issues/3764) | COLABORACION NO-CODIGO. Selector typeahead: el diagnostico/audit de Gonzo fue la base, el fix llego a main via PR de otro autor (merged 11/08). Impacto real sin merge a nombre de Gonzo. |
| facebook/astryx | [#5107](https://github.com/facebook/astryx/pull/5107) | COLABORACION NO-CODIGO. Dividers/Selector a11y: el trabajo de Gonzo (PR #5344, cerrado sin merge) fue la base, el fix llego a main via PR de otro autor (merged 23/08). Diagnostico de Gonzo fue el punto de partida. |
| facebook/astryx | [#4157](https://github.com/facebook/astryx/pull/4157) | COLABORACION NO-CODIGO. Avatar status labels: el trabajo de Gonzo fue la base, el fix llego a main via PR de otro autor (merged 24/07). |
| facebook/astryx | [#5034](https://github.com/facebook/astryx/pull/5034) | COLABORACION NO-CODIGO. Avatar status label via context: fix llego a main via PR de otro autor (merged 22/08). Composicion via AvatarStatusLabelContext. |
| facebook/astryx | [#3654](https://github.com/facebook/astryx/issues/3654) | COLABORACION NO-CODIGO. Contrast tokens WCAG: el diagnostico de Gonzo (PR #4022) fue la base; PR #3677 de otro autor quedo CLOSED sin merge pero el trabajo influyo. El #4022 de Gonzo CERRADO 28/08 por ownership (issue #3654 asignado a @rubyycheung, programa #4475) - aprobado 2x por cixzhang pero cerrado por coordinacion a11y+design. |
