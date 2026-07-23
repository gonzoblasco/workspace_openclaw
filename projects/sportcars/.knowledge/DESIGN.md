# DESIGN — Sport Cars Jeep

## Filosofía de diseño

El sitio debe **vender confianza y facilitad**, no solo autos. Diseño premium pero accesible, alineado con la estética Jeep (aventura, robustez, calidad) sin copiar el template genérico actual.

### Principios
1. **Mobile-first:** el tráfico de concesionarias es mayoritariamente mobile.
2. **CTA claro en cada pantalla:** siempre hay un siguiente paso obvio.
3. **Información sin fricción:** precios, specs, disponibilidad al alcance.
4. **Calidez humana:** chatbot útil, no robótico; derivación a vendedor fácil.
5. **Velocidad percibida:** cargas rápidas, transiciones sutiles, sin páginas vacías.

## Identidad visual

### Paleta de colores

| Token | Valor | Uso |
|---|---|---|
| `--color-primary` | `#1A1A1A` o `#111827` | Textos principales, fondos oscuros |
| `--color-accent` | `#D97706` o `#F59E0B` | Naranja/ambar Jeep-adjunto; CTAs secundarios |
| `--color-brand` | `#B91C1C` o `#DC2626` | Rojo Jeep para highlights |
| `--color-surface` | `#FFFFFF` | Fondos de cards |
| `--color-background` | `#F9FAFB` | Fondo general |
| `--color-muted` | `#6B7280` | Textos secundarios |
| `--color-border` | `#E5E7EB` | Bordes suaves |

**Nota:** Si Stellantis impone guidelines estrictos de color, ajustar a los oficiales Jeep.

### Tipografía
- **Headings:** Inter o Geist (de Next.js / Vercel)
- **Body:** Inter
- **Tamaños:**
  - H1: 2.25rem / 3rem (mobile/desktop)
  - H2: 1.5rem / 2.25rem
  - Body: 1rem / 1.125rem
  - Small: 0.875rem

### Logo
- Mantener logo actual de Sport Cars.
- Jeep y Ram logos según guidelines oficiales.

### Imágenes
- Fotos oficiales de modelos para 0km.
- Fotos reales de publicaciones MeLi para usados.
- Lazy loading + Next.js Image.
- Placeholder de carga con skeleton.

## Estructura de páginas

### Home (`/`)
1. **Hero**
   - Imagen de fondo con Jeep/Ram
   - Titular: "Encontrá tu Jeep o Ram en Sport Cars"
   - Subtítulo: "3 sucursales | Stock real | Atención personalizada"
   - CTAs: "Ver vehículos" + "Hablar con asesor"
2. **Modelos destacados**
   - Grid de 6 modelos Jeep + Ram
   - Card con imagen, nombre, precio desde, CTA "Cotizar"
3. **Usados destacados**
   - Últimos 4-6 listings de MeLi
   - Precio real, año, km
   - CTA "Ver todos los usados"
4. **Por qué Sport Cars**
   - 3 diferenciadores (stock real, chatbot IA, 3 sucursales)
5. **Sucursales preview**
   - Cards con dirección, horario, WhatsApp
6. **CTA final**
   - "¿Tenés dudas? Hablá con un asesor"

### Catálogo 0km (`/vehiculos`)
- Filtros laterales/top: marca, tipo, rango de precio
- Grid de cards de modelos
- Página de detalle por modelo (`/vehiculos/[slug]`)

### Usados (`/usados`)
- Grid de listings reales de MeLi
- Filtros: marca, modelo, año, km, precio
- Ordenamiento: precio, año, km
- Página de detalle (`/usados/[id]`)
- CTA "Consultar por este auto"

### Sucursales (`/sucursales`)
- Lista de 3 sucursales con:
  - Nombre, dirección, mapa
  - Horarios showroom y taller
  - Teléfono y WhatsApp de ventas y postventa
- Botón "Ver en mapa" por sucursal

### Test Drive (`/test-drive`)
- Formulario: modelo, sucursal, fecha/hora preferida, datos de contacto
- Confirmación visual
- Lead guardado en Supabase

### Cotizá tu usado (`/cotiza-tu-usado`)
- Formulario: marca, modelo, año, km, versión, estado, datos de contacto
- Mensaje: "Un asesor te contactará con una evaluación"

### Contacto (`/contacto`)
- Formulario simple
- Teléfonos y WhatsApp de cada sucursal
- Horarios

### Admin (MVP simple)
- `/admin/leads` — tabla de leads con filtros, exportar CSV
- Protegido por password simple o middleware básico

## Componentes UI

### Componentes de shadcn/ui base
- Button (variantes: default, outline, ghost, cta)
- Card
- Dialog / Sheet (para chatbot mobile)
- Form + Input + Select + Textarea
- Badge (estado de leads, condición de usado)
- Separator
- Skeleton (loading states)
- Accordion (FAQs)
- Tabs (detalle de vehículo)

### Componentes custom
- `ChatWidget` — botón flotante + ventana de chat
- `VehicleCard` — para 0km y usados
- `BranchCard` — sucursal con mapa y contactos
- `LeadForm` — formulario de captura reutilizable
- `PriceRange` — filtro de precio
- `MeliInventoryGrid` — grid de usados con cache

## Chatbot UX

### Widget
- Botón flotante abajo a la derecha
- Icono de chat / asistente
- Badge de "Online" o "Asistente Sport Cars"

### Ventana de chat
- Header con logo + "Asistente Sport Cars"
- Área de mensajes con burbujas
- Input con placeholder "Escribí tu consulta..."
- Sugerencias rápidas debajo del input:
  - "Ver modelos 0km"
  - "Usados disponibles"
  - "Agendar test drive"
  - "Horarios de sucursales"

### Flujo de conversación
1. Saludo + ofrecer ayuda
2. Usuario hace pregunta o clickea sugerencia
3. Bot responde con RAG o acción (abrir página/filtro)
4. Si la consulta requiere datos personales, pide nombre + teléfono
5. Si no puede resolver o el usuario pide vendedor, deriva a WhatsApp con contexto

### Mensajes del bot
- Tonada cordial, argentina, profesional pero cercana
- Ejemplos:
  - "¡Hola! Soy el asistente de Sport Cars. ¿En qué puedo ayudarte?"
  - "Para darte el mejor asesoramiento, ¿me pasás tu nombre y teléfono?"
  - "No tengo esa info ahora. Te paso con un asesor por WhatsApp."

## Responsive breakpoints

| Breakpoint | Ancho | Ajustes |
|---|---|---|
| Mobile | < 640px | Menú hamburguesa, 1 columna, chat en sheet |
| Tablet | 640px - 1024px | 2 columnas |
| Desktop | > 1024px | Navegación completa, filtros laterales |

## Accesibilidad

- WCAG 2.1 AA mínimo
- Contraste de texto > 4.5:1
- Focus visible en todos los elementos interactivos
- Labels asociadas a inputs
- Chatbot usable por teclado
- Alt text en imágenes de vehículos
- Skip link en navegación

## Animaciones y microinteracciones

- Transiciones suaves en cards (hover: lift + shadow)
- Skeleton loading en inventario MeLi
- Toast de confirmación tras enviar formulario
- Indicador de "escribiendo..." en chatbot
- Transición de apertura del chat (200ms ease-out)

## Iconografía
- Lucide React (consistente con shadcn/ui)
- Iconos por contexto:
  - WhatsApp, teléfono, ubicación
  - Auto, calendario, tag/precio
  - Chat, user, check

## Notas de implementación

- Usar Tailwind CSS con variables CSS para tokens de color.
- Tema por defecto: claro. Dark mode opcional (no prioritario).
- Mobile-first: probar primero en 375px.
- Componentes reutilizables para no duplicar formularios.
- Imágenes oficiales Jeep: verificar licencia de uso o usar las de MeLi para usados.