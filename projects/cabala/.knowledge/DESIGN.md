# DESIGN — Cábala

## Identidad visual

### Concepto
Minimalista, táctil, orgánica. La app no compite con las fotos — las enmarca. Colores oscuros para que las fotos sean protagonistas. Tipografía sans-serif limpia.

### Paleta

- **Fondo:** #0D0D0D (casi negro)
- **Superficie:** #1A1A1A (cards, modales)
- **Superficie elevada:** #262626
- **Texto primario:** #F5F5F5
- **Texto secundario:** #A3A3A3
- **Acento:** #FF6B35 (naranja cálido — como un atardecer)
- **Acento secundario:** #4ECDC4 (turquesa — para tags, mapas)
- **Error:** #FF4757
- **Success:** #2ED573

### Tipografía

- **Principal:** Inter (sans-serif, limpia, legible en pantallas chicas)
- **Monospace:** JetBrains Mono (solo para metadata técnica si aplica)

### Iconografía

- Sistema de iconos outline, línea delgada (1.5px)
- Usar Lucide icons (ya viene con Expo)

## Componentes clave

### EntryCard
- Foto en aspect ratio 4:3
- Título en bold si tiene, sino "Sin título" en gris
- Tags como pills pequeñas abajo
- Fecha relativa ("hace 2h", "ayer", "15 jun")
- Indicador de nota de voz (icono pequeño si tiene)

### PhotoGrid
- Grid 3 columnas en timeline
- Fotos en cuadrado (cropped)
- Al tap, abre detalle

### CalendarView
- Mes actual con dots en días con fotos
- Tap en día → muestra miniaturas de ese día
- Swipe para cambiar mes

### MapView
- Mapa con pins
- Pin al tap → muestra miniatura + fecha
- Pin al tap prolongado → abre detalle

### CabalaPrompt
- Modal que aparece cuando hay una foto para replicar
- Muestra la foto original + ubicación + fecha
- Botones: "Sacar ahora" / "Descartar"

### VoiceRecorder
- Botón de grabar con forma de círculo
- Waveform simple mientras graba
- Al parar, se guarda automáticamente
- En detalle: reproductor simple (play/pause + duración)

## Onboarding (3 pantallas)

1. **"3 momentos al día"** — ilustración de 3 fotos, texto: "Solo 3 fotos. Sin presión."
2. **"Tu vida en un mapa"** — ilustración de mapa con pins
3. **"Mirá atrás"** — ilustración de "un día como hoy", texto: "El pasado vuelve solo."

## Modo oscuro

Default: system. Pero la app está diseñada para modo oscuro nativamente. Si el usuario elige claro, invertir paleta (fondo blanco, texto oscuro).

## Animaciones

- Transición entre tabs: slide suave (300ms ease-out)
- Al guardar foto: scale bounce del botón
- Al abrir detalle: fade + scale del card
- Notificación: slide desde arriba
- Modo Cábala: fade in del modal con la foto original
