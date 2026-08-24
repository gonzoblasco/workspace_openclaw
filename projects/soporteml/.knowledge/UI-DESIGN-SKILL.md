---
name: soporteml-ui-design
description: Enforce the SoporteML design system in React + Tailwind CSS + shadcn/ui. Prevents generic LLM design mistakes by requiring SoporteML semantic tokens, 8pt spacing, explicit interactive states, mobile-first layouts, and WCAG-compliant accessibility. Applies ONLY to SoporteML projects.
---

# SoporteML - UI/UX Design System Engineering Skill

> **Scope:** Este skill aplica EXCLUSIVAMENTE a proyectos SoporteML (v1, v2, v3 y futuras). No se usa en otros proyectos. Los tokens, utilidades y componentes referenciados son los del design system de SoporteML.

## 1. Visión General y Filosofía de UI/UX

### Principios de diseño

1. **Jerarquía visual clara**: Cada pantalla debe tener un único punto focal. Usá tamaño, peso y color para guiar la atención del usuario, no decoración.
2. **Minimalismo funcional**: Eliminá lo que no aporta valor. No agregues sombras, bordes, gradientes o animaciones solo porque "se ve bien".
3. **Densidad equilibrada**: SoporteML es un CRM multi-tenant con datos densos (vendedores de Mercado Libre). Priorizá la legibilidad y la escaneabilidad. No dejes espacio vacío innecesario, pero tampoco amontones elementos.
4. **Consistencia sistémica**: Cada decisión visual debe derivarse del sistema de tokens de SoporteML. Si no hay un token para algo, consultá antes de inventar uno.

### Regla de oro

> **No inventar estilos ni colores fuera de los tokens definidos de SoporteML.**
>
> Si no existe un token para lo que necesitás, no uses un valor arbitrario. Proponé agregarlo al design system o consultá antes de hardcodear.

---

## 2. Sistema de Tokens y Reglas de Maquetación (Tailwind CSS)

### Espaciado: escala de 8pt

Usá exclusivamente múltiplos de 4 u 8 para `gap`, `padding`, `margin`, `w`, `h`, etc.

- `0`, `1` (4px), `2` (8px), `3` (12px), `4` (16px), `6` (24px), `8` (32px), `10` (40px), `12` (48px).
- Evitá valores intermedios como `p-3.5`, `m-5`, `gap-7` salvo justificación explícita.
- Para componentes compactos de datos densos, preferí `gap-2` o `gap-3`.

### Tipografía

| Uso | Tamaño | Weight | Color |
|-----|--------|--------|-------|
| Título de página / H1 | `text-2xl` o `text-3xl` | `font-semibold` | `text-foreground` |
| Subtítulo / H2 | `text-xl` | `font-semibold` | `text-foreground` |
| Sección / H3 | `text-lg` | `font-medium` | `text-foreground` |
| Cuerpo principal | `text-sm` | `font-normal` | `text-foreground` |
| Texto secundario | `text-sm` | `font-normal` | `text-muted-foreground` |
| Caption / metadata | `text-xs` | `font-normal` | `text-muted-foreground` |
| Datos numéricos (precios, métricas) | `text-lg` o `text-xl` | `font-semibold` | `text-foreground` |

- Fuente del sistema: **Inter** (ya definida en `index.css`). No uses `font-serif`.
- No uses `font-bold` en textos pequeños; preferí `font-medium` o `font-semibold`.
- El tracking por defecto de Tailwind es correcto. No agregues `tracking-tight` o `tracking-wide` sin razón.
- Usá `leading-relaxed` solo en bloques de texto largo; en tablas y listas, `leading-normal` o `leading-snug`.

### Paleta Cromática y Temas

Usá **exclusivamente las variables semánticas de SoporteML** (definidas en `src/index.css` y `tailwind.config.ts`):

- **Fondos**: `bg-background`, `bg-card`, `bg-muted`, `bg-accent`, `bg-popover`, `bg-secondary`
- **Textos**: `text-foreground`, `text-muted-foreground`, `text-primary`, `text-secondary-foreground`, `text-card-foreground`
- **Bordes**: `border-border`, `border-input`, `border-border/50`
- **Estados semánticos**: `text-destructive`, `text-success`, `text-warning`, `bg-destructive`, `bg-success`, `bg-warning` (todos definidos en SoporteML)
- **Sidebar**: `bg-sidebar`, `text-sidebar-foreground`, `bg-sidebar-primary`, `text-sidebar-primary-foreground`, `bg-sidebar-accent`, `text-sidebar-accent-foreground`, `border-sidebar-border`, `ring-sidebar-ring`
- **Badges de estado** (tokens propios de SoporteML):
  - `bg-badge-precio` - precio / ofertas
  - `bg-badge-stock` - stock / disponibilidad
  - `bg-badge-tecnico` - temas técnicos
  - `bg-badge-envio` - envío / logística
  - `bg-badge-garantia` - garantía

**Prohibido:**

- Colores hex inline: `bg-[#3b82f6]`, `text-[#888]`
- Colores arbitrarios de Tailwind: `bg-gray-100`, `text-blue-500`, `border-red-300`
- Colores estáticos: `bg-white`, `text-black`, `bg-black`
- Gradientes decorativos salvo que estén definidos en tokens del proyecto
- `!important` arbitrario (`!bg-primary`)

Si necesitás un color nuevo, agregalo como variable CSS en `src/index.css` (en `:root` y `.dark`) y en `tailwind.config.ts` antes de usarlo.

### Utilidades propias de SoporteML

Usá estas utilidades custom cuando corresponda (definidas en `src/index.css`):

- `glass-panel` - panel con efecto glass (`bg-card/60 backdrop-blur-xl border border-border/50`)
- `glow-primary` - glow sutil con el color primario
- `text-gradient` - gradiente de texto `from-primary to-amber-400` (solo para títulos destacados)
- `animate-slide-up`, `animate-fade-in`, `animate-slide-from-left` - animaciones de entrada del sistema

---

## 3. Reglas de Componentes y Microinteracciones

### Estados obligatorios (regla transversal)

Toda entidad interactiva debe implementar explícitamente:

1. **`hover`**: Cambio visible pero sutil (ej. `hover:bg-accent`, `hover:text-foreground`).
2. **`active`**: Feedback de clic (`active:scale-[0.98]` o cambio de fondo).
3. **`focus-visible`**: Anillo de foco accesible (`focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2`).
4. **`disabled`**: Apariencia atenuada, cursor no permitido, sin eventos (`disabled:opacity-50 disabled:cursor-not-allowed`).
5. **`loading`**: Estado de carga con spinner o skeleton; el botón debe mantener su layout y no cambiar de tamaño.

### Botones

- Botón primario: `variant="default"` de shadcn (usa el token `primary` de SoporteML).
- Botón secundario: `variant="outline"` o `variant="secondary"`.
- Botón destructivo: `variant="destructive"`.
- Botón ícono: `variant="ghost"` o `variant="outline"` con `size="icon"` y SIEMPRE `aria-label="Descripción de la acción"`.
- Los botones con ícono + texto deben tener un `gap-2`.

### Inputs y formularios

- Todos los inputs deben tener una etiqueta visible o `aria-label`.
- Usá `placeholder:text-muted-foreground`, nunca `placeholder:text-gray-400`.
- Los estados de error usan `border-destructive` y `text-destructive`.
- El mensaje de error debe estar asociado vía `aria-describedby`.

### Animaciones

- Transiciones por defecto: `transition-all duration-150 ease-in-out` o `transition-colors duration-150`.
- Evitá `duration-500` o más en microinteracciones.
- Respetá `prefers-reduced-motion`: no uses animaciones de entrada automáticas en listas densas.
- Usá las animaciones propias de SoporteML (`animate-slide-up`, `animate-fade-in`) con moderación. No animes cada celda de una tabla.

### Empty States y Skeletors

- **Skeleton**: Usá el componente `Skeleton` de shadcn para cargas iniciales. Mantené la estructura visual final (mismo número de filas, mismos espacios).
- **Empty state**: Ícono de 48-56px, título claro, descripción breve y acción principal si aplica.
- **Error state**: Mensaje útil, no genérico. Ofrecé una acción de reintento cuando sea posible.

---

## 4. Layouts, Responsive Design y Grids

### Patrones de maquetación

- **Flexbox-first** para alineaciones simples (header, filas, badges).
- **Grid-first** para layouts de panel (dashboard, cards, tablas).
- **Evitá posiciones absolutas** salvo en modales, tooltips, dropdowns o elementos flotantes justificados.

### Estrategia Mobile-First

Escribí los estilos base para mobile y agregá breakpoints progresivos:

```tsx
// Correcto
<div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">

// Incorrecto
<div className="grid grid-cols-3 max-sm:grid-cols-1">
```

### Breakpoints estándar

- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

### Layouts comunes de SoporteML

- **Panel lateral + contenido**: `flex h-dvh overflow-hidden` con sidebar fijo y scroll interno en `<main>`.
- **Lista + detalle**: Grid de 2 columnas en desktop, stack en mobile.
- **Dashboard**: Grid de cards `grid-cols-1 md:grid-cols-2 lg:grid-cols-4`.
- **Tablas densas**: Contenedor `overflow-x-auto` con tabla de ancho mínimo. No reduzcas el tamaño de fuente para que entre.

---

## 5. Accesibilidad (a11y) y Semántica HTML

### Estructura semántica

- Un único `<main>` por ruta.
- `<nav>` para la navegación principal.
- `<header>` para el encabezado de página.
- `<article>` o `<section>` para cards y bloques de contenido independientes.
- `<table>`, `<thead>`, `<tbody>`, `<th scope="col">` para tablas de datos.

### WCAG

- **Contraste**: El texto debe tener al menos 4.5:1 contra su fondo. Usá `text-foreground` sobre `bg-background` y `text-muted-foreground` solo para texto no esencial.
- **Botones ícono**: SIEMPRE con `aria-label`.
- **Imágenes**: Atributo `alt` descriptivo o `alt=""` si es decorativa.
- **Focus visible**: Nunca elimines el anillo de foco. Si lo reemplazás, asegurate de que sea visible.
- **ARIA redundante**: No uses `role="button"` en `<button>` ni `role="link"` en `<a>`.

### Navegación por teclado

- Los menús desplegables deben cerrarse con `Escape`.
- Las listas deben navegarse con flechas si son menús.
- El foco debe quedar atrapado dentro de modales mientras estén abiertos (Radix/shadcn lo maneja por defecto).

---

## 6. Anti-patrones explícitos ("Qué NO hacer")

No hagas esto:

- Usar `bg-white`, `bg-black`, `text-white`, `text-gray-400`, `border-gray-200`.
- Agregar gradientes decorativos sin token correspondiente.
- Usar `rounded-full` en elementos que no sean avatares o badges de estado.
- Aplicar `shadow-xl` o sombras grandes en cards comunes.
- Dejar botones sin estado `disabled` o sin `aria-label` si son ícono.
- Usar `h-screen` en lugar de `h-dvh` para layouts de altura completa en mobile.
- Animar `height` o `width` con CSS puro en lugar de usar las utilidades de Radix.
- Crear inputs custom cuando shadcn ya tiene el componente.
- Usar `tabIndex` mayor a 0.
- Centrar todo el texto por defecto; el texto de datos debe alinearse a la izquierda.
- Hacer cards con bordes muy oscuros o fondos muy diferentes del fondo de la app.
- Usar tokens de color que no existan en SoporteML (verificar en `src/index.css` antes).

---

## 7. Workflow de revisión

Antes de dar por terminado un cambio de UI, ejecutá estos pasos:

1. **Revisar el DOM renderizado**: Abrir DevTools y verificar que haya un único `<main>`, que los botones ícono tengan `aria-label` y que los inputs tengan label o `aria-label`.
2. **Buscar clases arbitrarias**: Hacer grep en el archivo editado por:
   - `#[a-fA-F0-9]{3,6}`
   - `bg-(white|black|gray|blue|red|green|yellow)-`
   - `text-(white|black|gray|blue|red|green|yellow)-`
   - `border-(gray|blue|red)-`
   - `h-screen`
3. **Probar estados interactivos**: En el navegador, verificar hover, focus-visible (tab), disabled y loading.
4. **Verificar responsive**: Capturar screenshot en mobile (375px) y desktop (1280px). Asegurarse de que no haya overflow horizontal ni elementos tapados.
5. **Validar contraste**: Usar las herramientas del navegador o Lighthouse para confirmar que no hay fallas de contraste.
6. **Revisar animaciones**: Confirmar que las transiciones no superan los 300ms y que no hay animaciones en listas grandes.

---

## 8. Scope y cuándo NO aplicar

Este skill aplica SOLO a proyectos SoporteML. NO aplica en:

- Cualquier proyecto que no sea SoporteML (aunque use el mismo stack).
- Proyectos sin Tailwind CSS, shadcn/ui o Radix UI.
- Landings de marketing donde el diseño artístico justifica gradientes, texto centrado y composiciones no utilitarias.
- Prototipos de baja fidelidad o wireframes.
- Componentes de terceros que no se pueden modificar.

Si un proyecto SoporteML tiene un design system que contradice estas reglas, seguir el design system existente del proyecto.

---

## 9. Checklist final

Antes de entregar un cambio de UI, verificá:

- [ ] No hay colores hex ni clases de color arbitrarias hardcodeadas.
- [ ] Se usan tokens semánticos de SoporteML (`bg-background`, `text-foreground`, `border-border`, etc.).
- [ ] Los badges usan los tokens propios (`bg-badge-precio`, `bg-badge-stock`, etc.) cuando corresponda.
- [ ] El espaciado respeta la escala de 8pt (múltiplos de 4).
- [ ] Los estados `hover`, `active`, `focus-visible`, `disabled` y `loading` están implementados.
- [ ] La tipografía usa los tamaños y pesos definidos.
- [ ] Hay un único `<main>` por ruta.
- [ ] Los botones ícono tienen `aria-label`.
- [ ] Los inputs tienen etiqueta visible o `aria-label`.
- [ ] El layout es mobile-first.
- [ ] No hay `h-screen` en layouts de altura completa (usar `h-dvh`).
- [ ] Las cargas muestran skeleton o empty state apropiado.
- [ ] No se introdujeron animaciones innecesarias o lentas.
- [ ] Se respetan los tokens de tema claro/oscuro.
- [ ] Se verificó responsive en mobile y desktop.
- [ ] No hay `tabIndex` mayor a 0 ni ARIA redundante.
