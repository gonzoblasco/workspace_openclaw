# SoporteML - Guía de Diseño (Design Guide) - Generada por Lovable

> **Fuente:** Respuesta de Lovable al prompt `prompts/PROMPT-GUIA-DISENO.md` (2026-08-07).
> **Estado:** ES LA FUENTE DE VERDAD de identidad visual para v3. Define lo que v3 DEBE ser.
> **Relación con otros docs:**
> - `DESIGN-GUIDE.md` (armada desde v1) = lo que YA existe. Referencia de lo actual.
> - `UI-DESIGN-SKILL.md` = estándar de implementación (el CÓMO).
> - Esta guía = la identidad visual objetivo (el QUÉ debe ser v3).
> **Pendiente:** cruzar esta guía contra `DESIGN-GUIDE.md` y el skill para reconciliar tokens nuevos (ver notas al final).

---

# SoporteML — Guía de Diseño (Design Guide)

> Referencia de identidad visual y marca para la interfaz de SoporteML.
> No cubre implementación técnica (ver skill `ui-design-engineer`).

---

## 1. Marca y personalidad

### Posicionamiento visual
SoporteML es un **centro de control**, no un panel de marketing. La interfaz debe sentirse como una cabina bien ordenada: densa en información pero calma, con jerarquía evidente y cero ruido decorativo. El usuario entra a resolver preguntas de compradores rápido, muchas veces desde el celular y bajo presión de tiempo (SLA).

### Atributos de marca
| Atributo | Se ve como | No se ve como |
|---|---|---|
| **Confiable** | Superficies neutras, datos siempre visibles, estados explícitos | Gradientes, ilustraciones genéricas, "wow" visual |
| **Rápida** | Transiciones 150–250 ms, skeletons inmediatos, densidad alta | Animaciones de entrada largas, carruseles, parallax |
| **Cercana** | Copy en vos rioplatense, empty states que orientan | Jerga técnica, tono corporativo frío |
| **Asistida por IA** | Acentos sutiles y etiquetas claras de "sugerido por IA" | Púrpuras "AI", brillos, efectos mágicos |
| **Profesional** | Un solo color de acento, tipografía consistente | Múltiples colores de marca compitiendo |

### Regla de oro
**El color se gana, no se regala.** El 90% de la pantalla es neutra. El amarillo de marca y los colores de estado aparecen solo donde hay una acción o una señal que exige atención.

---

## 2. Paleta de color

Todos los valores en **HSL** (formato `H S% L%`), pensados para tokens semánticos.

### 2.1 Color primario de marca

**Amarillo dorado Mercado Libre-adjacent** — `hsl(45 93% 47%)` · `#E8B004`

Es un color de alta luminancia: **nunca** se usa para texto sobre fondo claro. Su rol es *superficie de acción* (botón primario, indicador activo, foco).

| Token | Claro | Oscuro | Uso |
|---|---|---|---|
| `--primary` | `45 93% 47%` | `45 93% 47%` | Botón primario, item activo, ring de foco |
| `--primary-foreground` | `220 20% 10%` | `222 28% 7%` | Texto sobre primario (siempre oscuro) |
| `--primary-muted` | `45 93% 47% / 0.12` | `45 93% 47% / 0.16` | Fondos suaves, chips activos |
| `--primary-strong` | `42 90% 38%` | `45 95% 60%` | Texto/íconos "marca" cuando se necesita contraste AA |

> **Contraste:** el amarillo puro tiene ~1.9:1 contra blanco. Para texto de marca sobre fondo claro usar `--primary-strong` (`hsl(42 90% 38%)`, ~4.6:1). Sobre fondo oscuro usar `hsl(45 95% 60%)`.

### 2.2 Neutros (la base real de la app)

**Tema claro** — grises con tinte azulado frío, evita el beige que "ensucia" junto al amarillo.

| Token | Valor | Uso |
|---|---|---|
| `--background` | `220 20% 97%` | Fondo de app (nunca blanco puro: reduce fatiga en jornadas largas) |
| `--card` | `0 0% 100%` | Superficies elevadas: cards, tablas, popovers |
| `--muted` | `220 14% 94%` | Fondos de secciones, filas alternas, chips inertes |
| `--accent` | `220 14% 90%` | Hover de filas y de items de navegación |
| `--border` | `220 13% 87%` | Bordes de 1px, divisores |
| `--foreground` | `220 20% 10%` | Texto principal |
| `--muted-foreground` | `220 10% 46%` | Texto secundario, timestamps, placeholders |

**Tema oscuro** — azul-carbón, no negro puro. Evita el "smearing" en OLED y permite jerarquía por elevación.

| Token | Valor | Uso |
|---|---|---|
| `--background` | `222 28% 7%` | Fondo de app |
| `--card` | `222 24% 10%` | Superficie elevada |
| `--muted` | `220 18% 14%` | Secciones, filas alternas |
| `--accent` | `220 18% 16%` | Hover |
| `--border` | `220 18% 18%` | Bordes |
| `--foreground` | `210 20% 92%` | Texto principal (nunca blanco puro) |
| `--muted-foreground` | `215 15% 55%` | Texto secundario |

### 2.3 Sidebar (superficie diferenciada)

La navegación es un plano distinto al contenido: en claro es **más oscura** que el fondo, en oscuro es **más oscura** todavía. Esto ancla la app visualmente.

| Token | Claro | Oscuro |
|---|---|---|
| `--sidebar-background` | `220 20% 95%` | `222 28% 5%` |
| `--sidebar-foreground` | `220 10% 30%` | `215 15% 60%` |
| `--sidebar-accent` | `220 14% 90%` | `220 18% 12%` |
| `--sidebar-border` | `220 13% 87%` | `220 18% 14%` |

### 2.4 Colores de estado

Nunca se usan como decoración. Cada uno significa exactamente una cosa.

| Estado | Claro | Oscuro | Significado | Aplicación |
|---|---|---|---|---|
| **Éxito** | `150 60% 40%` | `150 60% 45%` | Publicado, respondido, conectado | Badge, ícono check, toast |
| **Advertencia** | `38 92% 50%` | `38 92% 50%` | SLA por vencer, revisión sugerida, confianza IA baja | Badge, borde izquierdo de fila |
| **Error / Destructivo** | `0 84% 60%` | `0 62% 50%` | SLA vencido, falla de publicación, desconexión | Badge, botón destructivo, toast |
| **Informativo** | `210 90% 48%` | `210 90% 60%` | Estado neutro del sistema, tips | Banner, tooltip |

**Regla de aplicación de estado:** fondo al 12–15% de opacidad + texto/ícono al 100% del color. Nunca fondo sólido saturado con texto blanco, salvo en botones destructivos y toasts.

```
Badge de error:   bg: color / 0.15    text: color    border: color / 0.25
Botón destructivo: bg: color sólido   text: destructive-foreground
```

### 2.5 Distribución de color en pantalla (regla 60/30/10)

- **60%** neutros de fondo (`background`, `card`)
- **30%** neutros de estructura y texto (`border`, `muted`, `foreground`)
- **10%** color con intención: primario (acciones), estados (señales), badges de categoría (clasificación)

---

## 3. Tipografía

### Familia
**Inter** (pesos 300–800) — variable, excelente legibilidad en tamaños chicos, números tabulares nativos. Fallback: `system-ui, -apple-system, sans-serif`.

Para datos numéricos usar la feature `tabular-nums` (`font-variant-numeric: tabular-nums`) en tablas, contadores y métricas: evita el "baile" de dígitos en actualizaciones en tiempo real.

### Escala tipográfica

| Rol | Tamaño / Line-height | Peso | Tracking | Uso |
|---|---|---|---|---|
| **Display** | 32 / 38 px | 700 | -0.02em | Solo landing y estados de bienvenida. No en la app. |
| **H1 — Título de página** | 24 / 30 px | 600 | -0.015em | "Bandeja de entrada", "Analytics" |
| **H2 — Sección** | 18 / 26 px | 600 | -0.01em | Bloques dentro de una página, títulos de drawer |
| **H3 — Subsección / Card** | 15 / 22 px | 600 | 0 | Encabezado de card, título de grupo |
| **Body** | 14 / 21 px | 400 | 0 | Texto base de la app: preguntas, respuestas, celdas |
| **Body medium** | 14 / 21 px | 500 | 0 | Énfasis dentro de body, labels de formulario |
| **Small** | 13 / 19 px | 400 | 0 | Texto secundario denso, descripciones de campo |
| **Caption** | 12 / 16 px | 400 | 0 | Timestamps, metadatos, ayuda de campo |
| **Micro** | 11 / 14 px | 500 | 0.02em | Badges, chips, contadores |
| **Overline** | 11 / 14 px | 600 | 0.08em, UPPERCASE | Encabezados de tabla, agrupadores de sidebar |

### Datos numéricos (KPIs y métricas)

| Rol | Tamaño | Peso | Notas |
|---|---|---|---|
| **Métrica hero** | 30 / 34 px | 700 | `tabular-nums`, tracking -0.02em |
| **Métrica card** | 22 / 26 px | 600 | `tabular-nums` |
| **Número en tabla** | 14 px | 500 | `tabular-nums`, alineado a la derecha |
| **Delta / variación** | 12 px | 600 | Color de estado (éxito/error), con flecha ▲▼ |

### Reglas
- Máximo **3 pesos por pantalla** (típicamente 400 / 500 / 600).
- Nunca texto justificado. Nunca texto centrado en interfaces densas — solo en empty states y diálogos.
- Ancho máximo de bloques de lectura: **68 caracteres**.
- Texto secundario siempre `--muted-foreground`, nunca `--foreground` con opacidad.

---

## 4. Iconografía y estilo visual

### Íconos
- **Librería:** Lucide (line icons, geométricos, stroke uniforme).
- **Stroke:** 1.5 px para 16–20 px; 2 px solo a partir de 24 px.
- **Tamaños:** 14 px (inline en texto chico), **16 px (default)**, 20 px (acciones de barra), 24 px (empty states, headers).
- **Color:** heredan `currentColor`. Íconos decorativos en `--muted-foreground`; íconos de acción en `--foreground`; íconos de estado en su color de estado.
- Un ícono nunca reemplaza una etiqueta en acciones destructivas o poco frecuentes. Solo acciones universales (cerrar, buscar, más) pueden ir sin texto.
- **Prohibido:** emojis como íconos de UI, íconos de estilos mezclados (filled + outline), íconos 3D o ilustrados.

### Radio de bordes
Escala compacta y consistente. Base `--radius: 8px`.

| Elemento | Radio |
|---|---|
| Chips, badges, tags | 4 px |
| Inputs, botones, filas seleccionables | 6 px |
| Cards, popovers, dropdowns | 8 px |
| Modales, drawers | 12 px |
| Avatares, indicadores de estado | 9999 px (pill/círculo) |

Nunca mezclar radios muy distintos en elementos anidados: la diferencia entre contenedor e hijo no debe superar 4 px.

### Elevación y sombras
La jerarquía se construye con **color de superficie + borde de 1px**, no con sombras pesadas. Las sombras solo aparecen en elementos que flotan sobre el contenido.

| Nivel | Uso | Sombra |
|---|---|---|
| **0 — Plano** | Cards en grilla, secciones | Sin sombra. `border: 1px solid --border` |
| **1 — Sutil** | Card hover, fila seleccionada | `0 1px 2px hsl(220 20% 10% / 0.06)` |
| **2 — Flotante** | Dropdown, popover, tooltip | `0 4px 12px hsl(220 20% 10% / 0.10)` |
| **3 — Overlay** | Modal, drawer, command palette | `0 16px 40px hsl(220 20% 10% / 0.16)` |

En tema oscuro las sombras se reducen a la mitad de opacidad y la jerarquía se apoya en la luminancia de la superficie (`card` más claro que `background`).

### Efectos
- **Glassmorphism:** permitido solo en la barra superior sticky y overlays (`backdrop-blur-xl` + superficie al 60–80%). Nunca en cards de contenido.
- **Gradientes:** prohibidos como fondo de superficies. Único uso permitido: barra de progreso de SLA y highlights de gráficos.
- **Glow:** solo el ring de foco y el indicador de "IA generando".

### Movimiento
- **Duración:** 150 ms (micro: hover, foco) · 200 ms (default: expandir, fade) · 300 ms (máximo: drawer, modal).
- **Easing:** `cubic-bezier(0.4, 0, 0.2, 1)` para entradas/salidas; `ease-out` para hover.
- Se animan `opacity` y `transform`. Nunca `width`, `height` o `top/left`.
- Respetar `prefers-reduced-motion`: reducir a fade de 0 ms o transición instantánea.

---

## 5. Componentes clave

### 5.1 Botones

Altura estándar **36 px** (`h-9`); compacto 32 px; grande 40 px. Padding horizontal 12–16 px. Gap ícono-texto 8 px. Peso de texto 500, tamaño 14 px.

| Variante | Reposo | Hover | Active | Uso |
|---|---|---|---|---|
| **Primario** | `bg: primary` · `text: primary-foreground` · sin borde | `brightness 0.95` | `brightness 0.90` + `scale 0.98` | Una sola acción principal por vista: "Publicar respuesta" |
| **Secundario** | `bg: secondary` · `text: secondary-foreground` | `bg: accent` | `bg: surface-active` | Acciones frecuentes no destructivas |
| **Outline** | `bg: transparent` · `border: 1px border` | `bg: accent` | `bg: accent` más oscuro | Acciones alternativas, filtros |
| **Ghost** | Sin fondo ni borde | `bg: accent` | `bg: accent` | Acciones terciarias, barras de herramientas |
| **Destructivo** | `bg: destructive` · `text: destructive-foreground` | `brightness 0.92` | `brightness 0.88` | Eliminar, desconectar cuenta. Siempre con confirmación |
| **Ícono** | Cuadrado 36×36, ghost por defecto | `bg: accent` | — | Requiere `aria-label` y tooltip |

**Estados obligatorios en todas las variantes:**
- `focus-visible`: `ring: 2px primary` + `ring-offset: 2px` sobre `background`.
- `disabled`: `opacity 0.5` + `cursor: not-allowed`, sin cambio de hover.
- `loading`: spinner 14 px reemplaza el ícono, el texto se mantiene, botón deshabilitado. **El ancho no debe cambiar.**

### 5.2 Inputs y formularios

- Altura 36 px, radio 6 px, borde 1px `--border`, fondo `--card` (claro) / `--muted` (oscuro).
- **Foco:** borde `--primary` + ring 2px `primary / 0.25`. Nunca `outline: none` sin reemplazo.
- **Label** siempre visible arriba (13 px, peso 500). El placeholder no es una etiqueta.
- **Texto de ayuda** debajo, 12 px `--muted-foreground`.
- **Error:** borde `--destructive` + mensaje 12 px en `--destructive`, con ícono de alerta 14 px. El mensaje reemplaza al texto de ayuda y se anuncia con `role="alert"`.
- Ancho de campo proporcional al dato: un campo de código postal no ocupa el 100%.
- Densidad de formulario: gap vertical 16 px entre campos, 24 px entre grupos.

### 5.3 Cards

- `bg: card` · `border: 1px border` · `radius: 8px` · `padding: 16px` (20 px en cards de detalle).
- **Estructura:** header (título H3 + acciones a la derecha) → contenido → footer opcional con acciones alineadas a la derecha.
- Cards clickeables: cursor pointer + `hover: border-color primary/30` y sombra nivel 1. Deben ser un `<button>` o `<a>` real.
- Cards de KPI: label overline arriba, número grande al centro, delta con color de estado abajo. Sin ícono decorativo salvo que aporte significado.

### 5.4 Tablas y listas densas

- **Altura de fila:** 44 px (default) · 36 px (modo compacto) · 56 px (con avatar o dos líneas).
- **Header:** overline 11 px uppercase, `--muted-foreground`, fondo `--muted`, sticky al hacer scroll.
- **Divisores** horizontales de 1px `--border`. Sin bordes verticales.
- **Hover de fila:** `bg: accent`. **Fila seleccionada:** `bg: primary / 0.08` + barra izquierda de 2px `--primary`.
- **Alineación:** texto a la izquierda, números y fechas a la derecha, acciones a la derecha en columna fija.
- **Truncado:** una línea con ellipsis + tooltip con el valor completo. Nunca reflow que cambie la altura de fila.
- **Orden y filtros** siempre visibles en el header, no escondidos en un menú.
- En mobile la tabla se convierte en **lista de cards apiladas**, con las 3 columnas más importantes visibles y el resto en el detalle.

### 5.5 Badges y chips

- Altura 20 px, padding horizontal 8 px, radio 4 px, texto 11 px peso 500.
- Formato: `bg: color / 0.15` + `text: color`. Borde opcional `color / 0.25` para badges de estado crítico.
- **Un badge = una dimensión.** No mezclar categoría y estado en el mismo chip.
- Máximo 3 badges visibles por fila; el resto colapsa en `+N` con tooltip.
- **Chip removible:** ícono `x` de 12 px a la derecha con área táctil de 24 px.

### 5.6 Empty states

Centrados, respirados, siempre accionables.

```
[ícono 24px en contenedor 56×56, bg muted, radio 16px]
Título (H3, 15px/600)
Descripción (14px, muted-foreground, máx. 2 líneas, ancho máx. 380px)
[Acción primaria]  [Acción secundaria opcional]
```

Tres variantes distintas — nunca la misma para todo:
1. **Vacío inicial** ("Todavía no conectaste tu cuenta") → acción de setup.
2. **Sin resultados de filtro** ("No encontramos preguntas con esos filtros") → acción "Limpiar filtros".
3. **Todo hecho** ("No hay preguntas pendientes. Estás al día.") → tono celebratorio, sin acción obligatoria.

### 5.7 Skeletons y carga

- Skeleton con la **forma exacta** del contenido final (mismas alturas y anchos aproximados), `bg: muted`, radio igual al elemento, animación de pulso de 1.5 s.
- Umbrales: <300 ms sin indicador · 300 ms–2 s skeleton · >2 s skeleton + texto de progreso.
- Nunca spinner centrado a pantalla completa dentro de la app autenticada.
- Actualizaciones en tiempo real: el contenido nuevo entra con fade de 200 ms, sin desplazar la posición de scroll del usuario.

### 5.8 Feedback y notificaciones

- **Toast:** esquina inferior derecha (desktop) / superior (mobile), 4 s de duración, con acción "Deshacer" cuando aplique. Ícono de estado + una línea de texto.
- **Banner inline:** para condiciones persistentes (cuenta desconectada, suscripción vencida). Fondo de estado al 12%, borde izquierdo de 3px.
- **Confirmación destructiva:** diálogo con el nombre del objeto afectado en el texto, botón destructivo a la derecha, cancelar como ghost.

---

## 6. Badges de categoría

Cada categoría de consulta tiene un color propio, estable y memorizable. El objetivo es que el vendedor identifique el tipo de pregunta **por color periférico**, sin leer.

| Categoría | HSL (claro) | HSL (oscuro) | Hex ref. | Racional |
|---|---|---|---|---|
| **Precio** | `200 80% 45%` | `200 80% 55%` | `#1791CE` | Azul: neutralidad, negociación, dinero |
| **Stock** | `150 60% 35%` | `150 60% 45%` | `#248F63` | Verde: disponibilidad, inventario |
| **Técnico** | `280 60% 50%` | `280 60% 60%` | `#8433CC` | Violeta: especificaciones, detalle |
| **Envío** | `25 85% 45%` | `25 85% 55%` | `#D45D0F` | Naranja: movimiento, logística, tránsito |
| **Garantía** | `340 65% 45%` | `340 65% 55%` | `#BD2957` | Magenta: postventa, cobertura, riesgo |
| **Sin categoría** | `--muted-foreground` | `--muted-foreground` | — | Gris neutro, sin peso visual |

### Reglas de aplicación
- Formato uniforme: `bg: categoria / 0.15` · `text: categoria` · sin borde.
- Los colores de categoría **no se usan fuera de los badges de categoría**. No aparecen en gráficos de estado, botones ni bordes de card.
- Ninguno de estos colores debe confundirse con los de estado: por eso Precio es azul (no verde-éxito) y Garantía es magenta (no rojo-error).
- Todos verificados a ≥4.5:1 contra su fondo al 15% en ambos temas.
- Si se agrega una categoría nueva, debe tener ≥30° de separación de matiz respecto a las existentes.

### Señales de prioridad (dimensión aparte)
Los chips de prioridad (Negociación, Devolución, Urgente, Alta intención, Revisión manual) usan **colores de estado**, no de categoría, y se muestran en una segunda línea debajo del título. Esto mantiene la lectura: *línea 1 = qué tipo de consulta es · línea 2 = por qué requiere atención.*

---

## 7. Layout y navegación

### 7.1 Estructura general (desktop ≥1024 px)

```
┌────────────┬──────────────────────────────────────────────┐
│  SIDEBAR   │  TOPBAR (56px, sticky)                       │
│  240px     ├──────────────────────────────────────────────┤
│            │  LISTA          │  PANEL DE DETALLE          │
│  colapsa   │  360–420px      │  flex-1                    │
│  a 64px    │  scroll propio  │  scroll propio             │
└────────────┴──────────────────────────────────────────────┘
```

- **Altura:** la app ocupa exactamente el viewport (`100dvh`). **El body no scrollea**; cada columna maneja su propio overflow. Esto mantiene sidebar, topbar y filtros siempre accesibles.
- **Sidebar:** superficie `--sidebar-background`, ancho 240 px, colapsable a 64 px (solo íconos + tooltip). Item activo: `bg: sidebar-accent` + barra izquierda 2px `--primary` + texto `--foreground`. Agrupación con overline uppercase.
- **Topbar:** breadcrumb / título de página a la izquierda; buscador, selector de empresa, notificaciones y avatar a la derecha.
- **Selector de empresa (multi-tenant):** siempre visible en la topbar. El contexto activo nunca puede ser ambiguo.
- **Ancho máximo de contenido:** las vistas de lista/detalle usan todo el ancho; las vistas de formulario y configuración se limitan a 720 px centrados.

### 7.2 Espaciado — grilla de 8 pt

Escala permitida: **4, 8, 12, 16, 24, 32, 48, 64 px.** Nada intermedio.

| Contexto | Valor |
|---|---|
| Gap ícono-texto, padding de chip | 4–8 px |
| Padding interno de card, gap entre campos | 16 px |
| Gap entre cards y secciones | 16–24 px |
| Padding de página | 24 px (desktop) · 16 px (mobile) |
| Separación entre bloques mayores | 32–48 px |

### 7.3 Densidad

Tres modos de densidad aplicables a listas y tablas:
- **Cómoda** — filas 56 px, padding 16 px. Default en mobile.
- **Estándar** — filas 44 px, padding 12 px. Default en desktop.
- **Compacta** — filas 36 px, padding 8 px. Para sesiones de trabajo intensivo; el usuario la elige y se recuerda.

La densidad cambia el espaciado y la altura de fila, **nunca el tamaño de fuente por debajo de 13 px**.

### 7.4 Responsive (mobile-first)

| Breakpoint | Comportamiento |
|---|---|
| `< 640px` | Sidebar → drawer con botón hamburguesa. Lista y detalle son **vistas separadas** con navegación push (no split view). Acciones primarias en barra inferior fija. Tablas → cards apiladas. |
| `640–1023px` | Sidebar colapsado a íconos. Split view opcional; detalle como drawer lateral al 90% de ancho. |
| `≥ 1024px` | Layout completo de tres columnas. |
| `≥ 1536px` | El panel de detalle crece; la lista mantiene su ancho máximo. No estirar el contenido indefinidamente. |

**Reglas mobile:**
- Área táctil mínima **44×44 px** para cualquier control.
- Nada crítico depende de hover: siempre hay equivalente por tap o acción visible.
- Respetar `safe-area-inset` en barras fijas.
- Un solo `<main>` por ruta; el orden del DOM sigue el orden visual.

### 7.5 Accesibilidad transversal
- Contraste mínimo **4.5:1** en texto normal, **3:1** en texto ≥18 px y en bordes de controles.
- El color nunca es el único portador de información: siempre acompañado de texto, ícono o forma.
- Foco visible en **todo** elemento interactivo, con ring de 2px y offset de 2px.
- Navegación completa por teclado en listas, drawers y popovers (↑ ↓ Home End Esc Enter/Espacio).
- Regiones `aria-live="polite"` para contadores en tiempo real (preguntas nuevas, notificaciones).

---

## 8. Tono de la marca en texto

### Voz
**Español rioplatense neutro, tratando de "vos".** Cercano pero profesional: como un colega experimentado que te da la data sin vueltas. Nunca infantil, nunca corporativo.

### Principios de microcopy
1. **Concreto antes que amable.** "Se publicó la respuesta" > "¡Genial! Todo listo 🎉".
2. **El usuario es el sujeto.** "Conectá tu cuenta" > "La cuenta debe ser conectada".
3. **Sin jerga técnica.** Nunca "error 401", "token", "endpoint", "RLS". Traducir a consecuencia real.
4. **Sin signos de exclamación** salvo en un único momento de logro genuino.
5. **Sin emojis** en la interfaz de trabajo.
6. **Frases cortas.** Un mensaje de error entra en dos líneas.

### Botones y acciones
Verbo en infinitivo o imperativo, específico al objeto. Máximo 3 palabras.

| ✅ Usar | ❌ Evitar |
|---|---|
| Publicar respuesta | Enviar |
| Conectar Mercado Libre | Continuar |
| Guardar cambios | OK |
| Eliminar producto | Sí, estoy seguro |
| Cancelar | Volver atrás |

### Mensajes de error
Estructura: **qué pasó → por qué → qué hacer.**

| Situación | Mensaje |
|---|---|
| Token de MeLi vencido | "Se desconectó tu cuenta de Mercado Libre. Volvé a conectarla para seguir recibiendo preguntas." |
| Falla al publicar | "Mercado Libre rechazó la respuesta. Suele pasar cuando la pregunta ya fue respondida o se eliminó. Revisala en la publicación." |
| Sin conexión | "No pudimos guardar los cambios. Revisá tu conexión y probá de nuevo." |
| Campo requerido | "Completá este campo para continuar." |
| Sin permisos | "No tenés permiso para hacer esto. Pedile acceso a un administrador de la empresa." |

Nunca: "Ocurrió un error inesperado", "Algo salió mal", "Error 500".

### Empty states

| Contexto | Título | Descripción |
|---|---|---|
| Bandeja vacía | "Estás al día" | "No hay preguntas pendientes. Te avisamos cuando llegue una nueva." |
| Sin resultados | "No encontramos preguntas" | "Probá con otros filtros o cambiá el texto de búsqueda." |
| Sin cuenta conectada | "Conectá tu cuenta de Mercado Libre" | "Cuando la conectes, las preguntas de tus publicaciones aparecen acá automáticamente." |
| Base de conocimiento vacía | "Todavía no cargaste conocimiento" | "Sumá tus políticas de envío, garantía y devolución para que la IA responda mejor." |
| Sin clientes | "Todavía no hay clientes" | "Los compradores que te consulten van a aparecer acá con su historial." |

### Estados de carga y confirmación
- Carga: "Sincronizando preguntas…" / "Generando respuesta…" — verbo en gerundio, con puntos suspensivos.
- Éxito: "Respuesta publicada" / "Cambios guardados" — participio, sin exclamación.
- Confirmación destructiva: "¿Eliminar el producto «Moto Honda CB190»? Esta acción no se puede deshacer."

### Etiquetas de IA
La IA siempre se identifica y nunca se antropomorfiza. No tiene nombre propio, no dice "yo", no se disculpa.

- "Sugerido por IA" (badge en la respuesta generada)
- "Confianza: 87%" (dato, no opinión)
- "Requiere revisión — falta información de garantía" (motivo concreto)
- "Respondido automáticamente" (atribución en el historial)

❌ Nunca: "Creo que la mejor respuesta es…", "Lo siento, no pude…", "¡Preparé esto para vos!".

---

## 9. Checklist de revisión de diseño

- [ ] Ningún color hardcodeado: todo pasa por tokens semánticos.
- [ ] El amarillo primario no se usa como color de texto sobre fondo claro.
- [ ] Todo espaciado pertenece a la escala de 8 pt.
- [ ] Los colores de categoría solo aparecen en badges de categoría.
- [ ] Los colores de estado tienen un único significado consistente en toda la app.
- [ ] Hover, active, focus-visible, disabled y loading están definidos en cada control.
- [ ] El contraste cumple 4.5:1 en texto y 3:1 en bordes, en tema claro y oscuro.
- [ ] Ninguna información depende únicamente del color.
- [ ] Hay skeleton o empty state específico para cada estado de carga y vacío.
- [ ] El body no scrollea; cada panel maneja su propio overflow.
- [ ] Áreas táctiles ≥44 px en mobile.
- [ ] El copy usa "vos", sin jerga técnica, sin emojis, sin exclamaciones.
- [ ] Los errores explican qué pasó y qué hacer.
- [ ] Las animaciones duran ≤300 ms y respetan `prefers-reduced-motion`.
- [ ] Máximo un botón primario por vista.

---

## Notas de reconciliación (pendiente para el arranque de v3)

Tokens que la guía de Lovable propone y que v1 NO tiene (habría que agregarlos en v3):

1. **`--primary-muted`** (`45 93% 47% / 0.12` claro, `/ 0.16` oscuro) - fondos suaves, chips activos.
2. **`--primary-strong`** (`42 90% 38%` claro, `45 95% 60%` oscuro) - texto/íconos de marca con contraste AA.
3. **`--informative`** (azul `210 90% 48%` claro, `210 90% 60%` oscuro) - estado informativo del sistema.
4. **`--surface-active`** (referenciado en botón secundario active) - no existe en v1.
5. **Regla de estado:** fondo al 12-15% + texto al 100% (v1 usa badges con fondo sólido en algunos casos).

Coincidencias confirmadas (v1 ya las tiene): `--primary`, `--primary-foreground`, `--background`, `--card`, `--muted`, `--accent`, `--border`, `--foreground`, `--muted-foreground`, `--sidebar-*`, `--success`, `--warning`, `--destructive`, badges de categoría (precio/stock/tecnico/envio/garantia).

La escala tipográfica de la guía (Display/H1/H2/H3/Body/Small/Caption/Micro/Overline) es más fina que la del skill. Reconciliar en v3.
