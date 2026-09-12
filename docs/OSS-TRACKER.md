# OSS-TRACKER.md - Open Source Contributions Tracker

> Generado desde memory/memory.db (tabla contributions). Fuente de verdad: la DB.
> Regenerar con: ./scripts/memory-db.sh export-oss

## Estado actual

| Métrica | Valor |
|---------|-------|
| PRs abiertos | 19 |
| PRs mergeados | 7 |
| PRs cerrados sin merge | 22 |
| Colaboraciones no-codigo | 15 |
| Repos con contribuciones | 22 |

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
| **Nuestro PR** | [#10487]() | **closed** |

| **Issue** | [#10220](https://github.com/adobe/react-spectrum/issues/10220) | fix(react-aria): only announce combobox section changes to VoiceOver |
| **Nuestro PR** | [#10503](https://github.com/adobe/react-spectrum/pull/10503) | **open** |
| **Contexto** | - | Gate del announcement effect a solo cambios de seccion. Maintainer LFDanLu dio luz verde 24/08. 218 + 41 tests pass. Comentado en issue. |

| **Issue** | [https://github.com/adobe/react-spectrum/issues/9687](a11y) | fix: expose input styling on RAC Checkbox and Radio (inputClassName/inputStyle) |
| **Nuestro PR** | [10517](https://github.com/adobe/react-spectrum/pull/10517) | **open** |
| **Contexto** | - | 9687 |

| **Issue** | [10554](https://github.com/adobe/react-spectrum/issues/9556) | Test-only PR: regression for global aria-posinset across sections. Merged 2026-09-09 by yihuiliao. Draft LinkedIn: docs/linkedin/react-spectrum-aria-posinset.md |
| **Nuestro PR** | [10554](https://github.com/adobe/react-spectrum/pull/10554) | **merged** |

### carbon-design-system/carbon

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | ComposedModal: add aria-describedby prop support. Agosto, sin review. |
| **Nuestro PR** | [#22887]() | **open** |

### carbon-design-system/ibm-products

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [9864](https://github.com/carbon-design-system/ibm-products/issues/9864) | PR #9878 (2026-09-09). CreateFullPage: getActiveStep en useCreateComponentFocus buscaba pasos sin ancestro [inert] pero los steps se ocultan solo con display:none (__step--hidden-step). Devolvia siempre el paso 1 oculto, .focus() no-op, foco se perdia al Skip to main content. Regression v2.44. Fix: querySelector directo de la clase __step--visible-step (blockClass compuesto de CreateFullPage resuelve a __step__step--visible-step en el DOM real). Test de regresion: falla sin fix (timeout), pasa con fix; suite 28/28. Issue fresco (creado 08/09), root cause reportado por el autor, verificado contra main antes de actuar. Pipeline T=8: Agente A escribio, Kanam reviso y corrigio (fixture con inputs reales + selector compuesto). |
| **Nuestro PR** | [9878](https://github.com/carbon-design-system/ibm-products/pull/9878) | **open** |

| **Issue** | [9839](https://github.com/carbon-design-system/ibm-products/issues/9839) | PR #9879 (2026-09-09). Datagrid sortable headers anunciados como toggle buttons: el boton sort en useSortableColumns.tsx seteaba aria-pressed (true/false), VoiceOver lo anuncia como toggle sin direccion. aria-sort ya existe en el th via getAriaSortValue (DatagridHeaderRow). Verificado que @carbon/react DataTable TableHeader NO usa aria-pressed (outlier de Datagrid). Fix: remover aria-pressed + helper getAriaPressedValue sin uso. Test de regresion: falla en main (aria-pressed=false presente), pasa con fix; suite Datagrid 47/48 (1 skipped pre-existente). T=6 trivial: Kanam solo, sin Agente A. Issue 25/08 (15 dias), sin asignar, sin PRs cruzados. |
| **Nuestro PR** | [9879](https://github.com/carbon-design-system/ibm-products/pull/9879) | **open** |

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

| **Issue** | [https://github.com/mui/base-ui/issues/5633](1) | Comentario analitico en #5633 (Select: flechas con dropdown cerrado). RESOLUCION (2026-09-04): atomiks (maintainer) cerro el issue como by-design - Base UI sigue el select nativo de macOS + patron APG select-only combobox. ArrowDown en select cerrado abre el menu (spec-compliant); typeahead que commitea cerrado tambien es comportamiento macOS. La convencion Windows (ciclar con flechas) es diferencia de plataforma, no bug. Sugirio tecnica hover (estilo Photoshop) como alternativa UX. Nuestro analisis fue validado en sustancia (atomiks cubrio el punto del typeahead). No hay PR que abrir. |
| **Nuestro PR** | [-](https://github.com/mui/base-ui/issues/5633) | **closed** |
| **Contexto** | - | https://github.com/mui/base-ui/issues/5633 |

### mui/material-ui

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#48990](https://github.com/mui/material-ui/issues/48990) | MERGED 24/08. [docs][templates] Remove focusable links from hidden carousel slides. WCAG 4.1.2 aria-hidden-focus: el carousel (react-swipeable-views) esconde slides inactivos con aria-hidden pero el link Go to store seguia focusable. Fix: tabIndex={-1} en slides inactivos (1 archivo, +1 -0). Aprobado por silviuaavram. Resuelve #48990 (cerrado COMPLETED). |
| **Nuestro PR** | [#49003]() | **merged** |
| **Contexto** | - | Abierto en agosto. PR de docs (templates). Merge 06:44 UTC 24/08. |

### openclaw/openclaw

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [126876](https://github.com/openclaw/openclaw/issues/126876) | Comentario tecnico en issue #126876 (audit 13 barreras screen reader). Aporte sin duplicar al bot: (1) tabla de plugins list persiste aun con stdout piped - verbose/json son los unicos escapes y no estan enmarcados como camino accesible; (2) modo plain automatico no es implementable (no hay deteccion portable de SR desde stdout) - el contrato viable es flag global explicito hermano de --no-color; (3) seam tecnico: loadHumanListModules aislaria el renderer de lineas etiquetadas sin tocar cold-imports. |
| **Nuestro PR** | [comment-126876](https://github.com/openclaw/openclaw/issues/126876#issuecomment-5642289378) | **active** |
| **Contexto** | - | openclaw/openclaw |

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

| **Issue** | [https://github.com/shadcn-ui/ui/issues/11757](0) | Comentario analitico en #11757 (Select: flechas con dropdown cerrado). RESOLUCION (2026-09-05): el fix pertenece upstream en mui/base-ui, donde atomiks cerro #5633 como by-design (macOS + APG). Issue de shadcn queda abierto pero efectivamente muerto - nadie va a fixear algo declarado intencional. Ultimo comentario (shahharis98) se retira del tema. No hay accion posible. |
| **Nuestro PR** | [-](https://github.com/shadcn-ui/ui/issues/11757) | **closed** |
| **Contexto** | - | https://github.com/shadcn-ui/ui/issues/11757 |

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
| adobe/react-spectrum | [#9556](https://github.com/adobe/react-spectrum/issues/9556) | PR PROPIO CERRADO 02/09 como innecesario (decision documentada). Fix de #9556 (aria-posinset global en secciones): el helper getPosInSet hacia DOBLE CONTEO (item.index en react-stately ya es global 0,1,2,3 - verificado empiricamente; sumaba index+1 + items de secciones precedentes = 5 en vez de 3). El codigo ORIGINAL ya produce posinset global correcto (test nuevo pasa contra main sin el fix). Bug de #9556 ya resuelto upstream por #9615 (merged Feb 2026, co-autor snowystinger). CI rojo (lint, s2-docs, test, test-16/17/18) consistente con el doble conteo. snowystinger pidio arreglar + evidencia de SR testing humano (politica AI-assisted de Adobe). Cierre con analisis completo (issuecomment-5510672207) + oferta de PR test-only con el test de regresion. Leccion: verificar contra main ANTES de abrir PR cuando el issue es viejo. |
| adobe/react-spectrum | [#10220](https://github.com/adobe/react-spectrum/issues/10220) | PR PROPIO (fix #10220, combobox announcements section-gate). 02/09: snowystinger senalo CI rojo + pidio evidencia de SR testing humano (politica AI-assisted). Fix: SearchAutocomplete.test.js (usa useComboBox internamente) tenia asserts del comportamiento viejo - actualizados al section-gated (commit 322a9543b, pusheado). A diferencia del #10487, este fix NO esta roto: el gate es direccion valida, ComboBox.test.js ya estaba actualizado, solo faltaba SearchAutocomplete. Comment honesto (issuecomment-5510942540): sin acceso a VoiceOver real, gate conservador, verificacion final requiere humano con Mac. Pendiente: CI + re-review. |
| adobe/react-spectrum | [#9556](https://github.com/adobe/react-spectrum/issues/9556) | PR TEST-ONLY (ofrecido en cierre del #10487): regression test de aria-posinset global across sections en virtualized menu. Pasa contra main (4/4 verificado local). Sin cambios de produccion. Referenciado en el comment de cierre del #10487 (issuecomment-5511145812). |
| carbon-design-system/carbon | [16031](https://github.com/carbon-design-system/carbon/issues/16031) | Verificacion de issue resuelto via #22751 (9/09). Confirmacion posterior de wkeese (maintainer, issuecomment-5610416004): botones ya no anidados, URL nueva del storybook validada. Aporte validado por maintainer sin interaccion adicional de nuestra parte. |
| carbon-design-system/ibm-products | [9868](https://github.com/carbon-design-system/ibm-products/issues/9868) | Review de PR ajeno (9/09): verificado diff contra Tearsheet legacy y source de Carbon (ComposedModal Layer level=0, ModalBody Layer interno). Approach correcto. 2 señales: pérdida de hasScrollingContentProps (role=region/tabIndex) y narrow variant con $background vs $layer del legacy. Nota sobre light mode identico por token design. Comment: issuecomment-5609797683 |
| carbon-design-system/ibm-products | [9866](https://github.com/carbon-design-system/ibm-products/issues/9866) | Analisis cruzado cluster React 19 (9/09): #9865/#9866/#9867 + carbon #23285, todos de snicolas-ibm. Verificado a nivel source: los 4 derivan estado durante commit (setState sincrono desde layout/passive effects o render body); React 19 acumula nestedUpdateCount en flush sincrono. Fix directions por hook. Nota: getInitialSize de useResizeObserver probablemente redundante (ResizeObserver dispara entry inicial en observe). Comment: issuecomment-5609873985 |
| facebook/astryx | [#3764](https://github.com/facebook/astryx/issues/3764) | COLABORACION NO-CODIGO. Selector typeahead: el diagnostico/audit de Gonzo fue la base, el fix llego a main via PR de otro autor (merged 11/08). Impacto real sin merge a nombre de Gonzo. |
| facebook/astryx | [#5107](https://github.com/facebook/astryx/pull/5107) | COLABORACION NO-CODIGO. Dividers/Selector a11y: el trabajo de Gonzo (PR #5344, cerrado sin merge) fue la base, el fix llego a main via PR de otro autor (merged 23/08). Diagnostico de Gonzo fue el punto de partida. |
| facebook/astryx | [#4157](https://github.com/facebook/astryx/pull/4157) | COLABORACION NO-CODIGO. Avatar status labels: el trabajo de Gonzo fue la base, el fix llego a main via PR de otro autor (merged 24/07). |
| facebook/astryx | [#5034](https://github.com/facebook/astryx/pull/5034) | COLABORACION NO-CODIGO. Avatar status label via context: fix llego a main via PR de otro autor (merged 22/08). Composicion via AvatarStatusLabelContext. |
| facebook/astryx | [#3654](https://github.com/facebook/astryx/issues/3654) | COLABORACION NO-CODIGO. Contrast tokens WCAG: el diagnostico de Gonzo (PR #4022) fue la base; PR #3677 de otro autor quedo CLOSED sin merge pero el trabajo influyo. El #4022 de Gonzo CERRADO 28/08 por ownership (issue #3654 asignado a @rubyycheung, programa #4475) - aprobado 2x por cixzhang pero cerrado por coordinacion a11y+design. |
| facebook/astryx | [#3349](https://github.com/facebook/astryx/issues/3349) | COLABORACION NO-CODIGO. RFC InfoTip: unico feedback sustantivo (16/07). Argumento Option A (standalone InfoTip) sobre B, propuse patron toggletip (tap abre, Escape/2do tap cierra) y aria-describedby al elemento explicado, ofreci implementacion/tests. ISSUE CERRADO 01/09 como COMPLETED por rubyycheung: #3355 (merged 08/07) implemento InfoTip en lab con button+aria-label+hover/focus+Escape; #5248 (merged 21/08) agrego touchTrigger=tap (tap abre/cierra); #4408 (AKnassa, cerrado sin merge) aporto el diagnostico de tap que entro via #5248. Option A y comportamiento toggletip coincidieron con lo implementado; aria-describedby NO se implemento. PR #3355 se mergeo 8 dias ANTES del comment, sin causalidad directa. |
| facebook/astryx | [#4777](https://github.com/facebook/astryx/issues/4777) | COLABORACION NO-CODIGO. Avatar status a11y: ISSUE CERRADO 02/09 como FIXED por cixzhang con CREDITO EXPLICITO a Gonzo: 'the parent-reads-child framing is what made this fixable, and the follow-up discussion about the interactive <a>/<button> branches shaped the answer'. Fix en main via #5034 (cixzhang, merged 22/08): AvatarStatusDot reporta label via ref compartido en commit phase (sin render extra, sin API change, sin breaking change). Tests cubren el ejemplo del issue (wrapper arbitrario, nesting depth, decorative avatar). Nota: label cae en commit phase, SSR lleva el nombre plano hasta hydration. Aportes de Gonzo: comment 07/08 (3 opciones, empuje a opcion 3 con spike AT), comment 10/08 (sibling del root en vez de role=group para ramas interactivas - la forma que se implemento). |
| vercel/next.js | [73474](https://github.com/vercel/next.js/issues/73474) | Comentario de diagnostico (16/07) en issue de Loading.tsx/Suspense que no funcionan en 2do load. Separo 3 escenarios confluidos: A) Antivirus/proxy (Kaspersky cachea text/html y text/x-component), B) Streaming roto en prod por reverse proxy (X-Accel-Buffering), C) await antes de Suspense como clue de flush de boundaries sin async work en el parent. CERRADO 02/09 por marcoshernanz como 'downstream response buffering, not a Next.js failure' - confirma el diagnostico A/B. Mi comentario estructuro el analisis que el maintainer valido al cerrar. |
