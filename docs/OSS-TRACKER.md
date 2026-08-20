# OSS-TRACKER.md - Open Source Contributions Tracker

> Generado desde memory/memory.db (tabla contributions). Fuente de verdad: la DB.
> Regenerar con: ./scripts/memory-db.sh export-oss

## Estado actual

| Métrica | Valor |
|---------|-------|
| PRs abiertos | 28 |
| PRs mergeados | 0 |
| PRs cerrados sin merge | 2 |
| Repos con PRs | 17 |

> Aportes 2026-08-20: PRs nuevos react-spectrum #10487 (posinset sections) + base-ui #5551 (aria-orientation grid) + mui #49003 (docs carousel) + 4 comentarios técnicos a11y. Repos nuevos: adobe/react-spectrum, mui/material-ui, mui/base-ui.

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

| **Issue** | [#4421](https://github.com/facebook/astryx/issues/4421) | Non-color indicator (font-weight) en current breadcrumb. MERGEABLE, sin reviews. |
| **Nuestro PR** | [#4605](https://github.com/facebook/astryx/pull/4605) | **open** |
| **Contexto** | - | Abierto 31 Jul. WCAG 1.4.1 fix. |

| **Issue** | [#4450](https://github.com/facebook/astryx/issues/4450) | aria-labelledby en Selector trigger. CONFLICTING, sin reviews. |
| **Nuestro PR** | [#4604](https://github.com/facebook/astryx/pull/4604) | **open** |
| **Contexto** | - | Abierto 31 Jul. Tiene conflictos con main. |

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

### vercel/ai

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | - | warn when reasoning tokens spent. Review bot de Vercel addressado. Squash 22 Jul. |
| **Nuestro PR** | [#17274](https://github.com/vercel/ai/pull/17274) | **waiting_review** |

### adobe/react-spectrum (NUEVO 2026-08-20)

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#9556](https://github.com/adobe/react-spectrum/issues/9556) | aria-posinset incorrecto en Pickers con Sections (regresión v1→S2). PR: posinset global consistente con setsize. Fix en useOption + useMenuItem. |
| **Nuestro PR** | [#10487](https://github.com/adobe/react-spectrum/pull/10487) | **open** - MERGEABLE. fix(react-aria): make aria-posinset global across sections. Helper compartido utils/posinset.ts + test. |

| **Issue** | [#10326](https://github.com/adobe/react-spectrum/issues/10326) | Autocomplete: VoiceOver no anuncia opción enfocada. Comentario: portar el live announcer de ComboBox a useAutocomplete. Oferta de PR. |
| **Comentario** | [comentario](https://github.com/adobe/react-spectrum/issues/10326#issuecomment-5359548673) | Confirmado: useAutocomplete sin live announcer, ComboBox sí. Fix = extraer helper compartido. |

| **Issue** | [#10220](https://github.com/adobe/react-spectrum/issues/10220) | Combobox solo anuncia nombre con VoiceOver. Comentario: gate el announcement solo a cambios de sección (preserva secciones, no interrumpe anuncio nativo por item). Oferta de PR. |
| **Comentario** | [comentario](https://github.com/adobe/react-spectrum/issues/10220#issuecomment-5359551331) | Solución intermedia: no descartar todo el effect, solo anunciar en isGroupChange. |

### mui/material-ui (NUEVO 2026-08-20)

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#48990](https://github.com/mui/material-ui/issues/48990) | docs: aria-hidden contiene focusable en templates carousel (WCAG 4.1.2). PR con tabIndex condicional en slides inactivas. |
| **Nuestro PR** | [#49003](https://github.com/mui/material-ui/pull/49003) | **open** - MERGEABLE. [docs][templates] Remove focusable links from hidden carousel slides. |

| **Issue** | [#47892](https://github.com/mui/material-ui/issues/47892) | dialog: Narrator lee main page detrás del modal. Comentario técnico: Modal no aplica aria-hidden al contenido exterior (a diferencia de react-spectrum/radix). Oferta de PR. |
| **Comentario** | [comentario](https://github.com/mui/material-ui/issues/47892#issuecomment-5359555501) | Root cause: focus trap sin aria-hidden del contenido externo. |

### mui/base-ui (NUEVO 2026-08-20)

| Eslabón | Link | Detalle |
|---------|------|---------|
| **Issue** | [#5548](https://github.com/mui/base-ui/issues/5548) | grid renderiza aria-orientation inválido (rol grid no lo soporta, axe aria-allowed-attr). Fix: no pasar orientation a useListNavigation cuando grid activo. Afecta Combobox + Autocomplete (reusa AriaCombobox). |
| **Nuestro PR** | [#5551](https://github.com/mui/base-ui/pull/5551) | **open** - MERGEABLE. [combobox] Remove invalid aria-orientation from grid role. |

