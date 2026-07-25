# DESIGN.md — Quedamos

> Identidad visual y experiencia de usuario. Output de Fase 0.3.

## Personalidad de la Marca

**Quedamos** no es una corporación. Es una invitación.

- **Tono:** Cálido, directo, argentino. Como cuando le decís a un amigo "che, ¿quedamos?"
- **Vibra:** Relajada, sin presión. La app no compite por tu atención, te invita a salir.
- **Sin vueltas corporativas:** Nada de "plataforma de encuentros sociales". Es "la app para salir con gente copada".
- **Inclusivo:** Sin sesgo de género, edad, o actividad. Todos son bienvenidos.

## Paleta de Colores

### Primarios
- **Naranja Quedamos** `#FF6B35` — El color principal. Cálido, energético, amigable. Representa la acción de "salir".
- **Blanco Hueso** `#FFF8F0` — Fondo principal. Suave, no frío como el blanco puro.

### Secundarios
- **Verde Menta** `#2EC4B6` — Éxito, confirmación, feedback positivo. Fresco, relajante.
- **Violeta Noche** `#5E2C8A` — Acento, personalidad, matching. Un toque de misterio y profundidad.

### Neutros
- **Gris Pizarra** `#2D3436` — Texto principal. Casi negro pero más suave.
- **Gris Humo** `#636E72` — Texto secundario, metadatos.
- **Gris Fondo** `#F5F0EB` — Fondos secundarios, cards, separadores.
- **Borde** `#E0D5C8` — Bordes suaves, divisores.

### Semánticos
- **Rojo Error** `#E74C3C` — Errores, no-shows, alertas.
- **Amarillo Atención** `#F39C12` — Advertencias, cupo bajo.

### Modo Oscuro (futuro)
- Fondo: `#1A1A2E`
- Superficie: `#16213E`
- Texto: `#E8E8E8`

## Tipografía

### Principal: Inter
- **Razón:** Excelente legibilidad en pantalla, variable font, gratuita, versátil para títulos y cuerpo.
- **Usos:** Toda la interfaz. Títulos, cuerpo, botones, labels.
- **Pesos:** Regular 400, Medium 500, SemiBold 600, Bold 700.

### Jerarquía
- **H1:** Inter SemiBold 28px — Títulos de página
- **H2:** Inter SemiBold 22px — Títulos de sección
- **H3:** Inter Medium 18px — Títulos de card
- **Body:** Inter Regular 16px — Texto general
- **Body Small:** Inter Regular 14px — Metadatos, descripciones
- **Caption:** Inter Regular 12px — Etiquetas, timestamps
- **Button:** Inter Medium 16px — Botones

## Iconografía

- **Estilo:** Lucide icons (ya viene con shadcn/ui)
- **Tamaño:** 20px default, 24px en navegación
- **Trazo:** 2px, consistente
- **Esquinas:** Redondeadas (round)

## Componentes Visuales Clave

### CompatibilityBadge
- Score 0-100% con color degradado:
  - 0-30%: Gris
  - 31-60%: Naranja claro
  - 61-80%: Naranja
  - 81-100%: Verde menta
- Formato: pill redondeado con ícono de persona + número
- Tooltip: "Basado en personalidad + actividades + feedback"

### SalidaCard
- Fondo blanco hueso con sombra suave
- Esquinas redondeadas (12px)
- Header: actividad + fecha
- Body: lugar, hora, cupo disponible
- Footer: avatares de participantes (iniciales del apodo) + compatibility score promedio
- Badge de "Sugerida para vos" si viene de las 5 semanales

### Botones
- **Primario:** Fondo naranja, texto blanco, border-radius 8px
- **Secundario:** Borde gris, texto gris, sin fondo
- **Ghost:** Sin borde, texto gris, hover con fondo suave
- **Peligro:** Fondo rojo, texto blanco

### Inputs
- Borde gris suave, focus ring naranja
- Placeholder en gris humo
- Label arriba, en semi-bold

### Navigation
- Bottom tab bar (mobile): 4 íconos + label
  - 🏠 Inicio (feed)
  - 🔍 Explorar
  - 👤 Perfil
  - ⚙️ Admin (solo visible para admins)

## Wireframes (Pantallas Clave)

### 1. Onboarding — Test de Personalidad
```
┌─────────────────────┐
│  ✨ Quedamos         │
│                      │
│  Conocé gente        │
│  para salir          │
│                      │
│  [Barra de progreso] │
│                      │
│  Pregunta 3/20       │
│                      │
│  "En una reunión,    │
│   prefiero..."       │
│                      │
│  [○] Hablar con      │
│      todos           │
│  [○] Observar y      │
│      escuchar        │
│  [○] Depende el día  │
│                      │
│  [Continuar →]       │
└─────────────────────┘
```

### 2. Feed — Sugerencias + Salidas
```
┌─────────────────────┐
│  ☀️ Hola, [apodo]    │
│                      │
│  Tus sugerencias     │
│  de esta semana  →   │
│                      │
│  ┌─────────────────┐ │
│  │ 🎬 Cine          │ │
│  │ Hoy 20:00        │ │
│  │ Cinema City      │ │
│  │ 4/20 cupos       │ │
│  │ 👤👤👤 78%       │ │
│  │ [⭐ Sugerida]     │ │
│  └─────────────────┘ │
│                      │
│  ┌─────────────────┐ │
│  │ 🍕 Birra         │ │
│  │ Sáb 15:00        │ │
│  │ Antares Palermo  │ │
│  │ 6/20 cupos       │ │
│  │ 👤👤👤👤 82%     │ │
│  └─────────────────┘ │
│                      │
│  [Ver más salidas →] │
│                      │
│  [🏠] [🔍] [👤] [⚙️] │
└─────────────────────┘
```

### 3. Detalle de Salida
```
┌─────────────────────┐
│  ← Volver           │
│                      │
│  🎬 Cine             │
│                      │
│  📍 Cinema City      │
│     Av. Corrientes   │
│                      │
│  📅 Sábado 26 Jul    │
│  🕐 20:00 hs         │
│                      │
│  Cupo: 4/20          │
│  [░░░░░░░░░░] 20%    │
│                      │
│  Quiénes van         │
│                      │
│  👤 Luna · 92%       │
│  👤 Max · 85%        │
│  👤 Sofi · 78%       │
│  👤 vos              │
│                      │
│  [Unirme a esta      │
│   salida 🎉]         │
│                      │
│  [🏠] [🔍] [👤] [⚙️] │
└─────────────────────┘
```

### 4. Feedback Post-Salida
```
┌─────────────────────┐
│  ¿Cómo la pasaste?   │
│                      │
│  Calificá a cada     │
│  persona que         │
│  conoció hoy         │
│                      │
│  ┌─────────────────┐ │
│  │ 👤 Luna          │ │
│  │ [1] [2] [3] [4]  │ │
│  │ [5] [6] [7] [8]  │ │
│  │ [9] [10]         │ │
│  └─────────────────┘ │
│                      │
│  ┌─────────────────┐ │
│  │ 👤 Max           │ │
│  │ [1] [2] [3] [4]  │ │
│  │ [5] [6] [7] [8]  │ │
│  │ [9] [10]         │ │
│  └─────────────────┘ │
│                      │
│  [Enviar feedback]   │
│                      │
│  (Tus respuestas son │
│   anónimas)          │
└─────────────────────┘
```

### 5. Perfil
```
┌─────────────────────┐
│  ← Volver            │
│                      │
│  👤 Luna             │
│                      │
│  "Siempre lista      │
│   para un café y     │
│   charla"            │
│                      │
│  🎯 Actividades      │
│  [Cine] [Café] [Bar] │
│                      │
│  📊 Confiabilidad    │
│  ✅ 8/10 asistencias │
│                      │
│  📋 Historial        │
│  🎬 Cine - 26 Jul    │
│  ☕ Café - 19 Jul    │
│  🍕 Birra - 12 Jul  │
│                      │
│  [🏠] [🔍] [👤] [⚙️] │
└─────────────────────┘
```

### 6. Admin — Programar Salida
```
┌─────────────────────┐
│  ← Volver            │
│                      │
│  ⚙️ Admin            │
│                      │
│  Programar salida    │
│                      │
│  Lugar: [Cinema City]│
│  Actividad: [Cine ▼] │
│  Fecha: [26/07/2026] │
│  Hora: [20:00     ]  │
│  Cupo: [20          ]│
│  Descripción:        │
│  [Estreno de...     ]│
│                      │
│  [Publicar salida]   │
│                      │
│  ── Salidas activas ─│
│  🎬 Cine · 4/20      │
│  🍕 Birra · 6/20     │
│                      │
│  [🏠] [🔍] [👤] [⚙️] │
└─────────────────────┘
```

## Flujo de Navegación

```
Landing (no auth)
  → Login / Register
  → Onboarding (test personalidad + actividades)
  → Feed (sugerencias semanales + todas las salidas)

Feed
  → Detalle de salida
    → Unirse a salida
  → Perfil de otro usuario (tocando avatar)

Perfil
  → Editar perfil
  → Historial de salidas

Admin (solo admins)
  → Programar salida
  → Gestionar lugares
  → Ver salidas activas

Post-salida (24h después)
  → Feedback modal (push notification lleva acá)
```

## Estados

### Loading
- Skeleton cards con animación de pulso
- Mismo layout que las cards reales

### Vacío
- Ilustración simple + mensaje amigable
- "No hay salidas esta semana. Vuelve pronto o crea una."
- Botón de acción (si aplica)

### Error
- Toast notification (naranja/rojo) en la parte superior
- Mensaje claro: "No pudimos cargar las salidas. ¿Probás de nuevo?"
- Botón de retry

### Offline
- Banner suave: "Estás sin conexión. Los datos pueden no estar actualizados."
- Datos cacheados del service worker

## Micro-interacciones

- **Unirse a salida:** Animación de check + confeti sutil
- **Feedback enviado:** Check verde + "¡Gracias! Tu feedback ayuda a mejorar los matches"
- **Navegación:** Transición suave entre páginas (slide)
- **Pull to refresh:** En feed, recarga de salidas

## Responsive

- **Mobile-first:** Diseñado para pantallas de 375px+
- **Tablet:** Layout de 2 columnas en feed
- **Desktop:** Layout de 3 columnas, sidebar de navegación en lugar de bottom tabs

## Accesibilidad (básica)

- Contraste WCAG AA en todos los colores
- Focus visible en todos los elementos interactivos
- Labels en todos los inputs
- Alt text en imágenes/iconos
- Soporte de navegación por teclado
- Reducir movimiento respeta prefers-reduced-motion
