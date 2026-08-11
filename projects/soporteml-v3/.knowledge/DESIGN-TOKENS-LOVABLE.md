# SoporteML v3 — Especificación de Design Tokens

Referencia técnica para implementar el design system de la nueva versión.
Todos los valores se expresan como triplete HSL sin `hsl()` (formato de variable CSS
compatible con Tailwind: `--token: H S% L%;` y uso `hsl(var(--token))`).

Base heredada de v1: `src/index.css` (`:root` y `.dark`).
Marca: amarillo Mercado Libre `45 93% 47%`.

---

## 1. Tokens semánticos faltantes

### 1.1 `--primary-muted`

| | Claro | Oscuro |
|---|---|---|
| Valor | `45 93% 92%` | `45 60% 16%` |
| Foreground asociado | `--primary-strong` | `--primary-strong` |

- **Propósito:** fondo suave de marca. Reemplaza el patrón `bg-primary/15` cuando se
  necesita un fondo estable y predecible sobre cualquier superficie (el alpha se
  comporta distinto sobre `card` vs `background`).
- **Dónde se usa:** chip/filtro activo en Inbox, item activo del sidebar,
  fondo del avatar de empresa en el CompanySwitcher, fondo del badge "IA" en el
  copiloto, celda seleccionada en tablas, fondo de `Tabs` activo variante soft.
- **Nunca:** como fondo de botón primario (eso es `--primary`), ni con texto
  `--primary-foreground` encima.

### 1.2 `--primary-strong`

| | Claro | Oscuro |
|---|---|---|
| Valor | `38 92% 30%` | `45 93% 62%` |

- **Propósito:** texto e íconos de marca con contraste AA. El amarillo
  `45 93% 47%` sobre fondo claro da ~1.9:1 y **no** puede usarse para texto.
  `--primary-strong` en claro llega a ≥ 4.5:1 sobre `--background` y sobre
  `--primary-muted`.
- **Dónde se usa:** texto del chip activo, label del item activo del sidebar,
  íconos de marca, links de marca, número de KPI destacado, texto sobre
  `--primary-muted`, `Button variant="link"` de marca.
- **Nunca:** como fondo de superficie grande.

### 1.3 `--informative`

| | Claro | Oscuro |
|---|---|---|
| `--informative` | `212 92% 45%` | `212 92% 60%` |
| `--informative-foreground` | `0 0% 100%` | `222 28% 7%` |

- **Propósito:** cuarto estado del sistema junto a success / warning / destructive.
  Comunica información neutral, no acción ni riesgo.
- **Dónde se usa:** `Alert` informativo, banners de sistema ("Sincronizando con
  Mercado Libre…"), badge "Auto‑IA", tooltip de ayuda, estados `pending` neutros,
  toast `info`.
- **Regla:** nunca se usa para éxito ni para advertencia; si el mensaje pide una
  acción del usuario, usar `warning`.

### 1.4 `--surface-active`

| | Claro | Oscuro |
|---|---|---|
| `--surface-hover` (ya existe en v1) | `220 14% 93%` | `220 18% 18%` |
| `--surface-active` | `220 14% 88%` | `220 18% 22%` |

- **Propósito:** estado `:active` (pressed) de superficies e interactivos
  secundarios. Un escalón más marcado que `--surface-hover`, siempre en la misma
  dirección: más oscuro en tema claro, más claro en tema oscuro.
- **Dónde se usa:** `Button variant="outline" | "secondary" | "ghost"` en `:active`,
  filas de tabla al presionar, items de lista del Inbox, items del sidebar,
  `DropdownMenuItem` presionado, `ToggleGroup`.
- **Combinar con:** `active:scale-[0.98]` en botones; en filas de tabla solo cambio
  de fondo (sin scale).

### 1.5 Otros tokens semánticos que la guía usa y no estaban listados

| Token | Claro | Oscuro | Propósito / uso |
|---|---|---|---|
| `--success-muted` | `150 55% 92%` | `150 45% 14%` | Fondo suave de estados OK (badge "Respondida", banda de SLA cumplido) |
| `--warning-muted` | `38 92% 92%` | `38 60% 15%` | Fondo suave de "Por vencer", SLA en riesgo |
| `--destructive-muted` | `0 84% 95%` | `0 50% 16%` | Fondo suave de "SLA vencido", errores no bloqueantes |
| `--informative-muted` | `212 92% 94%` | `212 60% 16%` | Fondo suave de banners informativos y badge Auto‑IA |
| `--success-strong` | `150 65% 26%` | `150 60% 55%` | Texto/ícono sobre `--success-muted` (AA) |
| `--warning-strong` | `30 90% 30%` | `38 92% 62%` | Texto/ícono sobre `--warning-muted` (AA) |
| `--destructive-strong` | `0 72% 40%` | `0 80% 70%` | Texto/ícono sobre `--destructive-muted` (AA) |
| `--informative-strong` | `212 92% 34%` | `212 92% 70%` | Texto/ícono sobre `--informative-muted` (AA) |
| `--surface-raised` | `0 0% 100%` | `222 24% 13%` | Superficie por encima de `card` (popover anidado, drawer interno) |
| `--surface-sunken` | `220 20% 94%` | `222 30% 5%` | Fondo hundido: contenedor de lista, code block, zona de scroll |
| `--overlay` | `220 25% 12% / 0.45` | `222 40% 2% / 0.6` | Backdrop de Dialog / Sheet |
| `--focus-ring` | `45 93% 40%` | `45 93% 55%` | Anillo de foco visible; deriva de marca pero con contraste ≥ 3:1 contra el fondo |
| `--border-strong` | `220 13% 76%` | `220 18% 28%` | Bordes de inputs con foco, separadores de tabla con jerarquía |
| `--chart-1..5` | `45 93% 47%`, `212 92% 45%`, `150 60% 40%`, `280 60% 50%`, `25 85% 45%` | `45 93% 55%`, `212 92% 60%`, `150 60% 48%`, `280 60% 62%`, `25 85% 58%` | Series de gráficos en Analytics |
| Badges de categoría | ver §4.4 | ver §4.4 | Precio / Stock / Técnico / Envío / Garantía |

---

## 2. Regla de estado: fondo 12–15% + texto 100%

**Sí es una regla global**, y aplica a los cinco estados semánticos:
`primary`, `success`, `warning`, `destructive`, `informative`.

### Cómo se aplica

- **Variante soft (por defecto en la app):** fondo = color base al **12–15%** de
  opacidad (`bg-success/15`) o, preferentemente en v3, el token `*-muted`
  precalculado. Texto e ícono = **100%** de opacidad, pero usando la variante
  `*-strong`, no el color base, para garantizar AA.
- **Borde opcional:** mismo color base al 25–30% (`border-success/30`) cuando el
  elemento necesita separarse de la superficie (alerts, callouts).
- **Regla de oro:** *el color base nunca se usa como texto sobre su propio fondo
  al 15%*. En tema claro el amarillo, el verde y el naranja no pasan AA. Por eso
  existen los tokens `*-strong`.

### Por qué tokens y no alpha

`bg-success/15` se compone contra la superficie subyacente; sobre `card`
(`0 0% 100%`) y sobre `muted` (`220 14% 94%`) el resultado difiere. Los tokens
`*-muted` son opacos y se ven idénticos en cualquier contexto. **En v3 preferir
`bg-success-muted` sobre `bg-success/15`.** El alpha queda permitido solo para
overlays temporales (hover sobre una fila ya coloreada, highlight de búsqueda).

### Excepciones (fondo sólido, texto `*-foreground`)

1. **Badge de conteo / notificación** (campana, contador de no leídas):
   `bg-destructive text-destructive-foreground`, sólido, porque debe leerse a
   tamaño micro y a distancia.
2. **Botón primario y botón destructivo:** `bg-primary text-primary-foreground`,
   `bg-destructive text-destructive-foreground`.
3. **Toast destructivo** y diálogos de confirmación de borrado: fondo sólido.
4. **Indicadores de estado tipo "dot"** (punto de conexión MeLi, online/offline):
   círculo sólido de 8px del color base al 100%, sin fondo suave.
5. **Barras de progreso y series de gráfico:** color base al 100%.
6. **Badges de categoría de pregunta:** mantienen el patrón soft de v1
   (`bg-badge-precio/15 text-badge-precio`) → en v3 migran a
   `bg-badge-precio-muted text-badge-precio-strong`.

Regla resumida: **soft por defecto, sólido solo cuando el elemento es una acción
principal, una alarma, o es demasiado pequeño para leerse en soft.**

---

## 3. Escala tipográfica

Fuente única: **Inter** (400 / 500 / 600 / 700). Números de métricas con
`font-variant-numeric: tabular-nums`.

| Nivel | Tamaño | Line-height | Weight | Letter-spacing | Clases Tailwind | Contexto |
|---|---|---|---|---|---|---|
| **Display** | 36px / 2.25rem | 40px (1.11) | 700 | -0.02em | `text-4xl font-bold tracking-tight` | Solo landing y pantallas de bienvenida. No usar dentro del CRM |
| **H1** | 30px / 1.875rem | 36px (1.2) | 600 | -0.02em | `text-3xl font-semibold tracking-tight` | Título de página (uno por ruta): "Inbox", "Clientes", "Analytics" |
| **H2** | 24px / 1.5rem | 32px (1.33) | 600 | -0.01em | `text-2xl font-semibold tracking-tight` | Título de sección mayor, encabezado de drawer / dialog |
| **H3** | 18px / 1.125rem | 28px (1.55) | 600 | -0.01em | `text-lg font-semibold` | Encabezado de card, título de grupo de preguntas, título de artículo KB |
| **H4 / Subhead** | 16px / 1rem | 24px (1.5) | 600 | 0 | `text-base font-semibold` | Subtítulo dentro de card, nombre de cliente en el detalle |
| **Body** | 14px / 0.875rem | 20px (1.43) | 400 | 0 | `text-sm` | Texto principal de la app: preguntas, respuestas, contenido de tablas |
| **Body strong** | 14px | 20px | 500 | 0 | `text-sm font-medium` | Énfasis dentro de body, celda de tabla con jerarquía, item de lista activo |
| **Small** | 13px / 0.8125rem | 18px (1.38) | 400 | 0 | `text-[0.8125rem] leading-[1.125rem]` | Texto secundario denso: descripciones auxiliares, helper text de formulario |
| **Caption** | 12px / 0.75rem | 16px (1.33) | 400 | 0 | `text-xs text-muted-foreground` | Metadata: timestamps, "hace 3 h", contadores, footer de card |
| **Label** | 12px / 0.75rem | 16px | 500 | 0.01em | `text-xs font-medium` | Label de campo de formulario, encabezado de columna de tabla |
| **Micro** | 11px / 0.6875rem | 14px (1.27) | 500 | 0.01em | `text-[0.6875rem] leading-[0.875rem] font-medium` | Texto dentro de badges y chips, contador de notificaciones |
| **Overline** | 11px / 0.6875rem | 14px | 600 | 0.08em, `uppercase` | `text-[0.6875rem] font-semibold uppercase tracking-[0.08em] text-muted-foreground` | Encabezado de grupo del sidebar, separador de sección en listas ("Hoy", "Ayer") |
| **Metric** | 24–30px | 1.1 | 600 | -0.02em | `text-2xl font-semibold tabular-nums tracking-tight` | Números de KPI en Dashboard y Analytics |
| **Mono / código** | 13px | 20px | 400 | 0 | `font-mono text-[0.8125rem]` | IDs de MeLi, item_id, payloads en el panel de debug |

Reglas de aplicación:

- Un solo **H1** por ruta; el resto desciende sin saltar niveles.
- En texto largo (artículo de KB, respuesta extensa) usar `leading-relaxed`;
  en tablas y listas densas, `leading-snug` o `leading-normal`.
- Nunca `font-bold` por debajo de 14px: usar `font-medium` o `font-semibold`.
- Ancho de línea de lectura ≤ 72 caracteres (`max-w-[65ch]`).
- No usar `tracking-*` fuera de los valores de esta tabla.

---

## 4. Paleta completa de tokens de color — v3

### 4.1 Base / superficies

| Token | Claro | Oscuro |
|---|---|---|
| `--background` | `220 20% 97%` | `222 28% 7%` |
| `--foreground` | `220 20% 10%` | `210 20% 92%` |
| `--card` | `0 0% 100%` | `222 24% 10%` |
| `--card-foreground` | `220 20% 10%` | `210 20% 92%` |
| `--popover` | `0 0% 100%` | `222 24% 10%` |
| `--popover-foreground` | `220 20% 10%` | `210 20% 92%` |
| `--muted` | `220 14% 94%` | `220 18% 14%` |
| `--muted-foreground` | `220 10% 46%` | `215 15% 55%` |
| `--accent` | `220 14% 90%` | `220 18% 16%` |
| `--accent-foreground` | `220 20% 10%` | `210 20% 92%` |
| `--secondary` | `220 14% 90%` | `220 18% 16%` |
| `--secondary-foreground` | `220 20% 10%` | `210 20% 85%` |
| `--surface-hover` | `220 14% 93%` | `220 18% 18%` |
| `--surface-active` | `220 14% 88%` | `220 18% 22%` |
| `--surface-raised` | `0 0% 100%` | `222 24% 13%` |
| `--surface-sunken` | `220 20% 94%` | `222 30% 5%` |
| `--overlay` | `220 25% 12% / 0.45` | `222 40% 2% / 0.6` |
| `--glass` | `0 0% 100% / 0.6` | `222 24% 10% / 0.6` |

### 4.2 Marca y foco

| Token | Claro | Oscuro |
|---|---|---|
| `--primary` | `45 93% 47%` | `45 93% 47%` |
| `--primary-foreground` | `220 20% 10%` | `222 28% 7%` |
| `--primary-muted` | `45 93% 92%` | `45 60% 16%` |
| `--primary-strong` | `38 92% 30%` | `45 93% 62%` |
| `--ring` | `45 93% 47%` | `45 93% 47%` |
| `--focus-ring` | `45 93% 40%` | `45 93% 55%` |
| `--glow-primary` | `45 93% 47% / 0.1` | `45 93% 47% / 0.15` |

### 4.3 Estados semánticos

| Token | Claro | Oscuro |
|---|---|---|
| `--success` | `150 60% 40%` | `150 60% 45%` |
| `--success-foreground` | `0 0% 100%` | `0 0% 100%` |
| `--success-muted` | `150 55% 92%` | `150 45% 14%` |
| `--success-strong` | `150 65% 26%` | `150 60% 55%` |
| `--warning` | `38 92% 50%` | `38 92% 50%` |
| `--warning-foreground` | `220 20% 10%` | `222 28% 7%` |
| `--warning-muted` | `38 92% 92%` | `38 60% 15%` |
| `--warning-strong` | `30 90% 30%` | `38 92% 62%` |
| `--destructive` | `0 84% 60%` | `0 62% 50%` |
| `--destructive-foreground` | `0 0% 100%` | `0 0% 100%` |
| `--destructive-muted` | `0 84% 95%` | `0 50% 16%` |
| `--destructive-strong` | `0 72% 40%` | `0 80% 70%` |
| `--informative` | `212 92% 45%` | `212 92% 60%` |
| `--informative-foreground` | `0 0% 100%` | `222 28% 7%` |
| `--informative-muted` | `212 92% 94%` | `212 60% 16%` |
| `--informative-strong` | `212 92% 34%` | `212 92% 70%` |

### 4.4 Badges de categoría de pregunta

| Token | Claro | Oscuro | Muted claro | Muted oscuro | Strong claro | Strong oscuro |
|---|---|---|---|---|---|---|
| `--badge-precio` | `200 80% 45%` | `200 80% 55%` | `200 80% 94%` | `200 55% 16%` | `200 85% 30%` | `200 80% 68%` |
| `--badge-stock` | `150 60% 35%` | `150 60% 45%` | `150 55% 93%` | `150 45% 14%` | `150 65% 24%` | `150 60% 58%` |
| `--badge-tecnico` | `280 60% 50%` | `280 60% 60%` | `280 60% 95%` | `280 40% 18%` | `280 60% 38%` | `280 65% 74%` |
| `--badge-envio` | `25 85% 45%` | `25 85% 55%` | `25 85% 93%` | `25 55% 16%` | `25 90% 32%` | `25 85% 66%` |
| `--badge-garantia` | `340 65% 45%` | `340 65% 55%` | `340 65% 95%` | `340 45% 17%` | `340 70% 35%` | `340 70% 70%` |

### 4.5 Bordes

| Token | Claro | Oscuro |
|---|---|---|
| `--border` | `220 13% 87%` | `220 18% 18%` |
| `--border-strong` | `220 13% 76%` | `220 18% 28%` |
| `--input` | `220 13% 87%` | `220 18% 18%` |

### 4.6 Sidebar

| Token | Claro | Oscuro |
|---|---|---|
| `--sidebar-background` | `220 20% 95%` | `222 28% 5%` |
| `--sidebar-foreground` | `220 10% 30%` | `215 15% 60%` |
| `--sidebar-primary` | `45 93% 47%` | `45 93% 47%` |
| `--sidebar-primary-foreground` | `220 20% 10%` | `222 28% 7%` |
| `--sidebar-accent` | `220 14% 90%` | `220 18% 12%` |
| `--sidebar-accent-foreground` | `220 20% 10%` | `210 20% 85%` |
| `--sidebar-border` | `220 13% 87%` | `220 18% 14%` |
| `--sidebar-ring` | `45 93% 47%` | `45 93% 47%` |

### 4.7 Gráficos

`--chart-1` … `--chart-5` según la tabla de §1.5. Orden de asignación fijo para
que una misma serie mantenga el color entre pantallas.

### 4.8 Radio y elevación

| Token | Valor |
|---|---|
| `--radius` | `0.5rem` (lg); md = `calc(--radius - 2px)`; sm = `calc(--radius - 4px)` |
| `--shadow-sm` | `0 1px 2px hsl(220 20% 10% / 0.06)` — cards |
| `--shadow-md` | `0 4px 12px hsl(220 20% 10% / 0.08)` — popover, dropdown |
| `--shadow-lg` | `0 12px 32px hsl(220 20% 10% / 0.12)` — dialog, sheet |

En tema oscuro las sombras se reducen a la mitad de opacidad y la elevación se
comunica principalmente con `--surface-raised` y `--border`.

---

## 5. Reglas de uso y contraste

### 5.1 Mapa token → componente

| Componente / estado | Fondo | Texto / ícono | Borde |
|---|---|---|---|
| Botón primario | `primary` | `primary-foreground` | — |
| Botón primario hover | `primary` @ 90% luminancia (`hover:brightness-95`) | `primary-foreground` | — |
| Botón secundario / outline | `card` | `foreground` | `border` |
| Botón secundario hover | `surface-hover` | `foreground` | `border-strong` |
| Botón secundario active | `surface-active` | `foreground` | `border-strong` |
| Botón ghost hover / active | `surface-hover` / `surface-active` | `foreground` | — |
| Botón destructivo | `destructive` | `destructive-foreground` | — |
| Chip / filtro inactivo | `muted` | `muted-foreground` | `border` |
| Chip / filtro activo | `primary-muted` | `primary-strong` | `primary` @ 30% |
| Sidebar item inactivo | transparente | `sidebar-foreground` | — |
| Sidebar item hover | `sidebar-accent` | `sidebar-accent-foreground` | — |
| Sidebar item activo | `primary-muted` | `primary-strong` | barra izquierda `primary` 2px |
| Badge categoría | `badge-*-muted` | `badge-*-strong` | — |
| Estado pregunta: respondida | `success-muted` | `success-strong` | — |
| Estado pregunta: por vencer | `warning-muted` | `warning-strong` | — |
| Estado pregunta: SLA vencido | `destructive-muted` | `destructive-strong` | — |
| Estado pregunta: auto‑IA / sincronizando | `informative-muted` | `informative-strong` | — |
| Contador de notificaciones | `destructive` | `destructive-foreground` | — |
| Punto de conexión MeLi | `success` / `destructive` sólido 8px | — | — |
| Alert informativo | `informative-muted` | `foreground` + ícono `informative-strong` | `informative` @ 30% |
| Input normal / foco / error | `card` | `foreground` | `input` / `focus-ring` / `destructive` |
| Fila de tabla hover / seleccionada | `surface-hover` / `primary-muted` | `foreground` | — |
| Dialog / Sheet backdrop | `overlay` | — | — |
| Skeleton | `muted` con pulse | — | — |

### 5.2 Reglas de contraste (WCAG AA)

1. **Texto normal ≥ 4.5:1**, texto ≥ 18.66px o ≥ 14px bold ≥ 3:1.
   Todos los pares `*-strong` sobre `*-muted` y sobre `background`/`card`
   cumplen ≥ 4.5:1 en ambos temas.
2. **El amarillo de marca nunca es texto sobre fondo claro.** Usar
   `--primary-strong`. `--primary` solo como fondo (con
   `--primary-foreground` oscuro encima, ratio ≈ 8:1) o como acento gráfico.
3. **Elementos no textuales ≥ 3:1**: bordes de input, anillos de foco,
   íconos que transmiten información, límites de gráficos. Por eso
   `--focus-ring` es más oscuro que `--primary` en tema claro.
4. **Nunca color como único portador de significado.** Todo estado lleva
   además texto o ícono: "Vencido" + ícono de reloj, no solo el punto rojo.
5. **`--muted-foreground` solo para texto no esencial** (metadata, captions).
   Cumple 4.5:1 sobre `background` pero no debe usarse para contenido crítico
   ni para labels de formulario.
6. **Foco siempre visible:** `focus-visible:ring-2 ring-[hsl(var(--focus-ring))]
   ring-offset-2 ring-offset-background`. Prohibido `outline: none` sin
   reemplazo.
7. **Disabled:** `opacity-50` + `cursor-not-allowed`. Se acepta que no cumpla
   AA (excepción explícita de WCAG para controles inactivos), pero el estado
   debe comunicarse también por texto o tooltip.
8. **Tema oscuro:** los `*-muted` oscuros son de baja luminancia (14–18%) para
   no brillar; los `*-strong` suben a 55–70% de luminancia. Verificar cada par
   con contraste real, no por simetría con el tema claro.

### 5.3 Prohibiciones

- Colores hex inline, clases arbitrarias de Tailwind (`bg-gray-100`,
  `text-blue-500`), `bg-white` / `text-black`.
- Introducir un color nuevo sin agregarlo antes como variable en `:root` y
  `.dark` y mapearlo en `tailwind.config.ts`.
- Usar `bg-<estado>/15` en v3 cuando existe el token `*-muted` equivalente.
- Gradientes decorativos fuera de `text-gradient` (marca) en la landing.

---

## 6. Snippet de implementación

```css
:root {
  /* marca */
  --primary: 45 93% 47%;
  --primary-foreground: 220 20% 10%;
  --primary-muted: 45 93% 92%;
  --primary-strong: 38 92% 30%;
  --focus-ring: 45 93% 40%;

  /* estados */
  --informative: 212 92% 45%;
  --informative-foreground: 0 0% 100%;
  --informative-muted: 212 92% 94%;
  --informative-strong: 212 92% 34%;
  /* … success / warning / destructive con el mismo patrón de 4 variantes */

  /* superficies */
  --surface-hover: 220 14% 93%;
  --surface-active: 220 14% 88%;
  --surface-raised: 0 0% 100%;
  --surface-sunken: 220 20% 94%;
  --border-strong: 220 13% 76%;
}

.dark {
  --primary-muted: 45 60% 16%;
  --primary-strong: 45 93% 62%;
  --focus-ring: 45 93% 55%;
  --informative: 212 92% 60%;
  --informative-foreground: 222 28% 7%;
  --informative-muted: 212 60% 16%;
  --informative-strong: 212 92% 70%;
  --surface-hover: 220 18% 18%;
  --surface-active: 220 18% 22%;
  --surface-raised: 222 24% 13%;
  --surface-sunken: 222 30% 5%;
  --border-strong: 220 18% 28%;
}
```

```ts
// tailwind.config.ts → theme.extend.colors
primary: {
  DEFAULT: "hsl(var(--primary))",
  foreground: "hsl(var(--primary-foreground))",
  muted: "hsl(var(--primary-muted))",
  strong: "hsl(var(--primary-strong))",
},
informative: {
  DEFAULT: "hsl(var(--informative))",
  foreground: "hsl(var(--informative-foreground))",
  muted: "hsl(var(--informative-muted))",
  strong: "hsl(var(--informative-strong))",
},
surface: {
  hover: "hsl(var(--surface-hover))",
  active: "hsl(var(--surface-active))",
  raised: "hsl(var(--surface-raised))",
  sunken: "hsl(var(--surface-sunken))",
},
```

---

## 7. Secciones no aplicables

- **Tokens de tipografía multi‑familia:** No aplica. SoporteML usa una sola
  familia (Inter); no hay token de fuente secundaria ni serif.
- **Modo alto contraste dedicado:** No aplica en v3. El tema oscuro ya cumple AA;
  si se agrega, debe ser un tercer bloque `.hc` con los `*-strong` reforzados.
