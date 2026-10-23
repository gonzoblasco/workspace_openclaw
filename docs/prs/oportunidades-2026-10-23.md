# Radar de oportunidades OSS - 2026-10-23

> Busqueda de material de post, **PRs y reviews por separado**, en repos de 1er y 2do nivel.
> Todo lo de abajo esta **verificado contra GitHub el 2026-10-23** (API): comments, assignees y
> PRs que referencian el issue. Un candidato sin PR que lo reclame y sin review humano NO es libre
> de verdad: hay que releer el hilo antes de tocarlo.
>
> **Regla que gobierna esto:** `memory/user-profile.md` - "Contribucion combinada por ticket:
> priorizar ayudar a mergear PRs existentes (review con sustancia, verificacion contra main,
> destrabar CI, rescatar tests de regresion) sobre abrir PR propio competitivo; usar codigo cuando
> hace falta, en servicio del merge ajeno o del fix no reclamado."

**Criterio de tier usado aca:**

| Tier | Que significa | Repos |
|---|---|---|
| **1** | 1er nivel (>9k stars), donde el merge ya tiene visibilidad | shadcn-ui/ui, mui/material-ui, chakra-ui, mantine, vercel/ai, microsoft/fluentui, radix-ui/primitives, adobe/react-spectrum, tanstack/router, facebook/astryx, mui/base-ui, carbon-design-system/carbon |
| **2** | 2do nivel o sub-marca, donde ya hay contribucion propia | carbon-design-system/ibm-products, vercel/ai, tanstack/router, colinhacks/zod, payloadcms/payload, shuding/nextra, t3-oss/create-t3-app |

---

## 1. PRs propias de Gonzo que estan paradas

Lo mas rentable primero: esto ya es material con resultado atribuible y **ya se puede postear**
si el PR se destraba (o, si Gonzo decide, si el PR se cierra con el trabajo atribuido).

| PR | Estado medido | Antiguedad sin actividad | Comentarios | Reviews |
|---|---|---|---|---|
| `t3-oss/create-t3-app#2243` - fix(www): add accessible label to clipboard copy button | open, not draft | creado 30/07, upd 30/07 (**~3 meses parado**) | 2 | 0 |
| `t3-oss/create-t3-app#2240` - fix(prettier): add .prettierignore to exclude generated Prisma client | open, not draft | creado 15/07, upd 30/07 (**~2,5 meses**) | 2 | 0 |
| `adobe/react-spectrum#10517` - fix: align screen reader focus indicator with RAC Checkbox and Radio | open, not draft | creado 27/08, upd 18/10 (**activo**) | 13 | 33 |

**Medido, no supuesto:** `#2243` y `#2240` tienen **0 review comments**. No es "waiting for review" del
maintainer: no hay nadie mirando. Es trabajo en curso sin contraparte. `#10517` esta vivo: 33
review comments y actividad hace 5 dias. **No se toca.**

**Lo que esto significa:** son PRs **a11y** (etiqueta accesible en un boton de copiar) en un repo
donde Gonzo ya tiene track record. Destrabarlos es exactamente la regla de la skill: "priorizar
ayudar a mergear PRs existentes sobre abrir PR propio competitivo". Y es post en ingles (materia
a11y) con resultado atribuible.

---

## 2. Issues a11y LIBRES (nadie los reclamo)

Criterio: 0 comentarios, sin assignee, y **ningun PR que los referencie** (verificado por timeline).

### `mui/material-ui` - 4 issues "Assess WCAG 2.2 conformance"

Repo de primer nivel, issues de una ola de auditoria **sin ningun comentario**. Los 4 comparten la
misma forma y el mismo tracking issue (`mui/material-ui#49260`, "Wave 4, lower risk"):

| Issue | Componente | Comments | PRs que lo referencian |
|---|---|---|---|
| [`#49444`](https://github.com/mui/material-ui/issues/49444) | CardActionArea | 0 | ninguno |
| [`#49445`](https://github.com/mui/material-ui/issues/49445) | AppBar | 0 | ninguno |
| [`#49446`](https://github.com/mui/material-ui/issues/49446) | SpeedDial | 0 | ninguno |
| [`#49447`](https://github.com/mui/material-ui/issues/49447) | ImageList | 1 | ninguno |

**El scope esta escrito en el issue, y es replicable:** (1) tests de axe y fixtures en
`packages/mui-material/test/regressions/a11y/fixtures/`, (2) escribir
`packages/mui-material/src/<Componente>/accessibility.md`, (3) inscribirlo en la suite CSS-dependent,
(4) correr `pnpm a11y:scorecard` (el script existe: `scripts/a11yScorecard/index.mjs`). El issue dice
explicitamente el patron: *"Write each check in the report as numbered Manual testing steps, as in
`Button/accessibility.md`"*.

**La plantilla ya existe y se puede copiar:** hay 12 `accessibility.md` en el repo
(`packages/mui-material/src/{Accordion,AccordionSummary,Avatar,Button,Checkbox,CircularProgress,LinearProgress,Radio,RadioGroup,Switch,TextField}/accessibility.md`),
y la carpeta de fixtures ya tiene 5 (`accordion`, `avatars`, `buttons`, `progress`, `toggle-button`).
**El trabajo es deriesgo bajo y puramente acotado: no hay que inventar el formato.**

**Por que es buena oportunidad:** el trabajo es **documental y de tests, no de logica de componentes**
- es exactamente el tipo de aporte que Gonzo ya hace bien, es de riesgo bajo, y produce un resultado
atribuible y trazable (un PR mergeado en un repo de 99k stars). Ademas la plantilla ya esta escrita
en el repo: hay 12 `accessibility.md` de componentes que dan el patron, y la carpeta de fixtures ya
tiene 5 entradas.

**Antes de arrancar:** leer el tracking issue `#49260` completo y la issue padre de la ola. 4 issues
parecen una ola coordenada, y hay que ver si hay una convencion que este revisor debe respetar.

### `mui/base-ui#5794` - iPhone VoiceOver closes entire menu after last submenu item

- 0 comentarios, sin assignee, **ningun PR lo referencia**.
- Labels: `component: menu`, `type: bug`, `accessibility`, `browser: Safari`.
- Repo de 11k stars donde Gonzo ya mergeo (`mui/base-ui#5551`).

Candidato a **reproduccion + diagnostico primero** (regla de Gonzo: "bugs concretos sin
competencia: no asumir simplicidad"). Es un bug de VoiceOver en iPhone: el caso mas caro de
reproducir sin hardware, asi que el contribution posible es el analisis y el test, no el fix.

---

## 3. Issues a11y que NO son libres (ya hay trabajo en curso)

Documentado para **no pisar**. Esta es la parte que la regla de "nunca piso" exige.

| Issue | Por que esta tomado |
|---|---|
| `facebook/astryx#7856` Spinner announces itself | **10 PRs** lo referencian (7870, 7910, 7920, 7930, 7939, 7940, 7942, 7948, 7950, 7954, 7956) |
| `facebook/astryx#7860` EmptyState live region | 2 PRs (7892, 7910) |
| `facebook/astryx#7819` Lab components render native disabled | 3 PRs (7820, 7903, 7909) |
| `facebook/astryx#7863` Comments (lab) live regions | 1 PR (7902) |
| `facebook/astryx#7853` Toast two live owners | 1 PR (7871) |
| `adobe/react-spectrum#9556` Incorrect aria-posinset for Pickers | 4 PRs (9013, 10487, 10554, 10711) |
| `adobe/react-spectrum#9687` SR focus indicator misaligned | PR 10517 (**es de Gonzo**) |
| `adobe/react-spectrum#9737` Invalid accessible label for menu list | 2 PRs + 7 comentarios |
| `mui/material-ui#49511` Clickable always assigned to component | asignado a `silviuaavram`, label `status: waiting for author` |
| `mui/material-ui#49477` Follow-ups from Wave 1 | `status: waiting for maintainer`, 4 issues hijas |
| `mui/base-ui#5519` Combobox popup state during exit animations | 2 PRs (5537, 48823) |

---

## 4. Candidatas a REVIEW (PRs abiertas con senal a11y, sin review de humano)

Se busca: PR abierta, senal a11y en el titulo, **sin ningun review de humano** (verificado con
`/reviews`), y que no sea de Gonzo. La oportunidad es dejar un review con sustancia: un detalle
tecnico con criterio, verificando el diff contra main.

| PR | Repo | Creada | Reviews | Archivos | Comments |
|---|---|---|---|---|---|
| [`#10803`](https://github.com/adobe/react-spectrum/pull/10803) fix(button): support `aria-keyshortcuts` | adobe/react-spectrum (1er nivel) | 18/10 | **0** | 5 | 0 |
| [`#6047`](https://github.com/mui/base-ui/pull/6047) [dialog] Return focus inside the parent modal when a nested trigger is rendered | mui/base-ui | 21/10 | **0** | 2 | 3 |
| [`#4222`](https://github.com/radix-ui/primitives/pull/4222) focus-scope: Treat a native radio group as one tab stop | radix-ui/primitives | 18/10 | **0** | 3 | 1 |
| [`#4227`](https://github.com/radix-ui/primitives/pull/4227) [FocusScope] Preserve focus trapping across Suspense | radix-ui/primitives | 19/10 | **0** | 5 | 0 |
| [`#7906`](https://github.com/facebook/astryx/pull/7906) fix(core): make disabled Button focusable via aria-disabled | facebook/astryx | 22/10 | **0** | - | - |

**Descartadas de este lote** (ya tienen review humano): `carbon#23819` (review de `adamalston`),
`carbon#23762` (review de `amal-k-joy`). La regla es no agregar ruido donde el maintainer ya esta.

**Criterio para review con sustancia, no un "se ve bien":** leer el diff, verificar el comportamiento
contra la spec ARIA correspondiente, y confirmar que el fix no rompe el caso borde. Si el PR esta
atascado en CI o en un test, destrabarlo vale mas que opinar.

---

## 5. Tier 2 - lo que se midio y NO hay

Medido el 2026-10-23, con la API de GitHub:

| Repo | Issues con label `accessibility` abiertos |
|---|---|
| `carbon-design-system/ibm-products` | **0** |
| `vercel/ai` | **0** |
| `tanstack/router` | **0** |
| `colinhacks/zod` | **0** |
| `payloadcms/payload` | **0** |

**Por que 0 y no "no hay material":** el label no existe o no se usa. `carbon-design-system/carbon`
no tiene `accessibility`: usa labels granulares por tecnologia de asistencia:

| Label | Issues abiertos |
|---|---|
| `a11y: JAWS` | 56 |
| `a11y: VoiceOver` | 33 |
| `a11y: NVDA` | 2 |
| `a11y: high contrast mode` | 3 |
| `a11y: TalkBack` | 0 |

**Consecuencia:** el tier 2 de a11y **no tiene un backlog de issues abiertos**. La oportunidad de
tier 2 no es "encontrar un issue de a11y": es (a) **destrabar las 2 PRs propias paradas de
`create-t3-app`**, que es donde Gonzo tiene la contribucion y el PR, o (b) revisar en el tier 2
donde el volumen de PRs a11y es alto pero la gente no da review (`shuding/nextra`, 47 PRs abiertas
y 45 sin actividad; `t3-oss/create-t3-app`, 53 y 49).

---

## 6. Lo que este radar NO es

- **No es una lista de tareas.** Es un radar: cambia el lunes. La fecha de cada dato es la de la
  medicion (2026-10-23), y hay que re-validar antes de actuar.
- **No autoriza nada.** Todo lo que salga de aca va al filtro de "nunca piso" y a la regla de
  "un post por resultado atribuible".
- **No reemplaza la busqueda manual dentro del repo.** Cada repo tiene su propia convencion
  (el `Button/accessibility.md` de material-ui, el `AST-0xx` de astryx). El radar no la adivina.
