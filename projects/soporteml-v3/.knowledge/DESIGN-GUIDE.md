# SoporteML - Guía de Estilos (basada en v1)

> **Fuente:** Documentada desde el código real de `soporteml` (v1) - `src/index.css`, `tailwind.config.ts`, `components.json` y estructura de componentes. No es inventada: cada token y patrón acá existe en v1.
> **Uso:** Esta guía define la identidad visual de SoporteML. Se usa junto con `UI-DESIGN-SKILL.md` (el estándar de implementación). Aplica a v1, v3 y futuras versiones.

---

## 1. Identidad y Marca

- **Producto:** CRM multi-tenant para vendedores de Mercado Libre, con asistencia de IA.
- **Público:** Vendedores que gestionan consultas, productos, stock, envíos y garantías.
- **Tono visual:** Profesional, denso pero legible, con acentos cálidos (amarillo/dorado) sobre neutros fríos (grises azulados).
- **Personalidad:** Confiable, eficiente, orientado a datos. No es una landing de marketing; es una herramienta de trabajo.

---

## 2. Paleta de Color (tokens semánticos)

Definidos en `src/index.css` (`:root` para claro, `.dark` para oscuro). Usar SIEMPRE las variables, nunca hex inline.

### Tema claro

| Token | Valor HSL | Uso |
|-------|-----------|-----|
| `--background` | `220 20% 97%` | Fondo general (gris azulado muy claro) |
| `--foreground` | `220 20% 10%` | Texto principal (casi negro azulado) |
| `--card` | `0 0% 100%` | Fondo de cards (blanco) |
| `--card-foreground` | `220 20% 10%` | Texto en cards |
| `--popover` | `0 0% 100%` | Fondo de popovers/dropdowns |
| `--primary` | `45 93% 47%` | **Color de marca** (amarillo/dorado) |
| `--primary-foreground` | `220 20% 10%` | Texto sobre primary (oscuro) |
| `--secondary` | `220 14% 90%` | Fondo secundario |
| `--secondary-foreground` | `220 20% 10%` | Texto sobre secondary |
| `--muted` | `220 14% 94%` | Fondo atenuado |
| `--muted-foreground` | `220 10% 46%` | Texto secundario (gris medio) |
| `--accent` | `220 14% 90%` | Fondo de hover/accent |
| `--accent-foreground` | `220 20% 10%` | Texto sobre accent |
| `--destructive` | `0 84% 60%` | Errores / acciones destructivas (rojo) |
| `--destructive-foreground` | `0 0% 100%` | Texto sobre destructive (blanco) |
| `--border` | `220 13% 87%` | Bordes |
| `--input` | `220 13% 87%` | Bordes de inputs |
| `--ring` | `45 93% 47%` | Anillo de foco (amarillo) |
| `--radius` | `0.5rem` | Radio de bordes base |
| `--success` | `150 60% 40%` | Estados de éxito (verde) |
| `--success-foreground` | `0 0% 100%` | Texto sobre success |
| `--warning` | `38 92% 50%` | Advertencias (ámbar) |
| `--warning-foreground` | `220 20% 10%` | Texto sobre warning |

### Tema oscuro

| Token | Valor HSL | Uso |
|-------|-----------|-----|
| `--background` | `222 28% 7%` | Fondo general (azul muy oscuro) |
| `--foreground` | `210 20% 92%` | Texto principal (casi blanco) |
| `--card` | `222 24% 10%` | Fondo de cards |
| `--primary` | `45 93% 47%` | **Color de marca** (se mantiene) |
| `--primary-foreground` | `222 28% 7%` | Texto sobre primary (oscuro) |
| `--muted-foreground` | `215 15% 55%` | Texto secundario |
| `--destructive` | `0 62% 50%` | Errores |
| `--border` | `220 18% 18%` | Bordes |
| `--ring` | `45 93% 47%` | Anillo de foco (se mantiene) |
| `--success` | `150 60% 45%` | Éxito |
| `--warning` | `38 92% 50%` | Advertencia |

### Sidebar (tokens propios)

| Token | Claro | Oscuro | Uso |
|-------|-------|--------|-----|
| `--sidebar-background` | `220 20% 95%` | `222 28% 5%` | Fondo del sidebar |
| `--sidebar-foreground` | `220 10% 30%` | `215 15% 60%` | Texto del sidebar |
| `--sidebar-primary` | `45 93% 47%` | `45 93% 47%` | Item activo / acento |
| `--sidebar-primary-foreground` | `220 20% 10%` | `222 28% 7%` | Texto sobre item activo |
| `--sidebar-accent` | `220 14% 90%` | `220 18% 12%` | Hover en items |
| `--sidebar-accent-foreground` | `220 20% 10%` | `210 20% 85%` | Texto sobre hover |
| `--sidebar-border` | `220 13% 87%` | `220 18% 14%` | Bordes del sidebar |
| `--sidebar-ring` | `45 93% 47%` | `45 93% 47%` | Anillo de foco |

### Badges de estado (tokens propios de SoporteML)

Usados para categorizar consultas/temas en el CRM. Son el diferenciador visual del producto.

| Token | Claro | Oscuro | Uso |
|-------|-------|--------|-----|
| `--badge-precio` | `200 80% 45%` | `200 80% 55%` | Precio / ofertas (azul) |
| `--badge-stock` | `150 60% 35%` | `150 60% 45%` | Stock / disponibilidad (verde) |
| `--badge-tecnico` | `280 60% 50%` | `280 60% 60%` | Temas técnicos (violeta) |
| `--badge-envio` | `25 85% 45%` | `25 85% 55%` | Envío / logística (naranja) |
| `--badge-garantia` | `340 65% 45%` | `340 65% 55%` | Garantía (rosa/rojo) |

---

## 3. Tipografía

- **Fuente:** Inter (importada en `index.css` desde Google Fonts, pesos 300-800).
- **Familia:** `font-sans` = `Inter, system-ui, sans-serif` (definida en `tailwind.config.ts`).
- **Base:** `body` usa `font-sans antialiased`.

| Uso | Tamaño | Weight | Color |
|-----|--------|--------|-------|
| Título de página / H1 | `text-2xl` o `text-3xl` | `font-semibold` | `text-foreground` |
| Subtítulo / H2 | `text-xl` | `font-semibold` | `text-foreground` |
| Sección / H3 | `text-lg` | `font-medium` | `text-foreground` |
| Cuerpo principal | `text-sm` | `font-normal` | `text-foreground` |
| Texto secundario | `text-sm` | `font-normal` | `text-muted-foreground` |
| Caption / metadata | `text-xs` | `font-normal` | `text-muted-foreground` |
| Datos numéricos (precios, métricas) | `text-lg` o `text-xl` | `font-semibold` | `text-foreground` |

---

## 4. Utilidades Custom (definidas en `src/index.css`)

| Utilidad | Efecto | Uso recomendado |
|----------|--------|-----------------|
| `glass-panel` | `bg-card/60 backdrop-blur-xl border border-border/50` | Paneles con efecto glass (headers, overlays) |
| `glow-primary` | `box-shadow: 0 0 20px hsl(var(--glow-primary))` | Glow sutil con color primario (elementos destacados) |
| `text-gradient` | Gradiente `from-primary to-amber-400` con `bg-clip-text` | Solo títulos destacados / hero |
| `animate-slide-up` | Slide up 0.3s ease-out | Entrada de paneles |
| `animate-fade-in` | Fade in 0.2s ease-out | Entrada sutil |
| `animate-slide-from-left` | Slide from left 0.25s ease-out | Sidebar / drawers |

---

## 5. Componentes y Patrones

### Stack de componentes

- **shadcn/ui** (style default, baseColor slate, cssVariables true) - ver `components.json`.
- **Radix UI** (primitivas subyacentes de shadcn).
- **Lucide Icons** para iconografía.
- **Framer Motion** para animaciones avanzadas (usar con moderación).
- **next-themes** para el toggle claro/oscuro.

### Componentes UI disponibles (shadcn)

`accordion, alert-dialog, alert, aspect-ratio, avatar, badge, breadcrumb, button, calendar, card, carousel, chart, checkbox, collapsible, command, dialog, dropdown-menu, form, hover-card, input, label, menubar, navigation-menu, popover, progress, radio-group, resizable, scroll-area, select, separator, sheet, sidebar, skeleton, slider, sonner, switch, table, tabs, textarea, toast, toaster, toggle-group, toggle, tooltip`

### Componentes propios de SoporteML (en `src/components/`)

| Componente | Uso |
|------------|-----|
| `AppSidebar` | Navegación lateral principal (colapsable, mobile-aware) |
| `DashboardLayout` | Layout del dashboard con sidebar + outlet |
| `CompanySwitcher` | Cambio de tenant/empresa |
| `NotificationBell` | Notificaciones |
| `CategoryBadge` | Badge de categoría (usa tokens `badge-*`) |
| `EmptyState` | Estado vacío estándar |
| `SkeletonCards` | Skeleton para cargas |
| `QuestionCard` / `GroupedQuestionCard` | Cards de consultas |
| `QuestionDetail` / `ThreadSummary` | Detalle de consulta / hilo |
| `AICopilotPanel` | Panel de asistente IA |
| `OnboardingWizard` | Onboarding inicial |
| `MeliConnectionStatus` | Estado de conexión con Mercado Libre |
| `ProductSideCard` | Card lateral de producto |

### Navegación principal (AppSidebar)

- **Dashboard:** Home, Inbox, Priority, Plantillas, Analytics, Settings
- **CRM:** Productos, Base de conocimiento, Clientes, Órdenes (algunos deshabilitados en v1)
- **Admin:** panel de administración (solo super admin)

---

## 6. Layout y Navegación

- **Dashboard:** `DashboardLayout` con `AppSidebar` fijo + `<main>` con scroll interno. En mobile, el sidebar se convierte en drawer.
- **Sidebar colapsable:** estado `collapsed` vía `SidebarContext`.
- **Páginas principales:** `Home, Inbox, PriorityInbox, Templates, Analytics, Settings, Catalog, KnowledgeBase, Customers, AdminPanel, Landing, Login, NotFound`.

---

## 7. Reglas de Implementación

> Las reglas detalladas de implementación (espaciado 8pt, estados interactivos, a11y, anti-patrones, workflow de revisión) están en `UI-DESIGN-SKILL.md`. Esta guía define el QUÉ (identidad y tokens); el skill define el CÓMO (implementación).

Resumen rápido:

- **Espaciado:** escala 8pt (múltiplos de 4).
- **Colores:** solo tokens semánticos de esta guía. Prohibido hex inline.
- **Badges:** usar tokens `badge-*` para categorías de consultas.
- **Mobile-first:** estilos base mobile, breakpoints progresivos.
- **a11y:** contraste 4.5:1, `aria-label` en botones ícono, focus visible con ring.
- **Tema claro/oscuro:** respetar ambos, usar `next-themes`.
