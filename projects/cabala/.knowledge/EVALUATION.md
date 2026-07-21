# EVALUATION — Cábala

## Mercado

### Competidores directos

| App | Diferenciador | Problema |
|---|---|---|
| **Day One** | Diario con fotos, ubicación, clima | Pesada, suscripción, nube, demasiadas features |
| **1 Second Everyday** | 1 segundo de video por día | Video, no foto; suscripción |
| **Grid Diary** | Diario con templates | Enfocado en texto, no en fotos |
| **Momento** | Diario automatizado (fotos, redes, ubicación) | Automatizado, no intencional; suscripción |
| **Google Photos** | Backup automático | Sin estructura de diario, sin límite diario |

### Competidores indirectos

- Apps de notas (Apple Notes, Notion, Obsidian) — se puede hacer pero no está diseñado para eso
- Apps de hábitos — diferente propósito
- Apps de fotografía (VSCO, Lightroom) — edición, no bitácora

### Oportunidad

Ninguna app combina:
1. **Límite deliberado** (3 fotos por día)
2. **Offline-first** (sin cuenta, sin nube)
3. **Organización multi-eje** (mapa + calendario + tags)
4. **Modo Cábala** (replicar fotos del pasado)
5. **Notas de voz** como entrada primaria (no secundaria)

## Viabilidad técnica

### Stack
- **React Native / Expo** — biplataforma, fácil de arrancar
- **expo-sqlite** — SQLite local, sin backend
- **expo-notifications** — notificaciones locales
- **expo-camera / expo-image-picker** — fotos
- **expo-location** — geolocalización
- **expo-av** — grabación de audio
- **expo-file-system** — export/import

### Riesgos técnicos
- **Compresión de imágenes** — Expo tiene herramientas, pero hay que testear calidad vs tamaño
- **Mapa offline** — para vista mapa sin conexión, requiere tiles locales o usar mapbox con caché
- **Notificaciones en iOS** — requieren permiso explícito, diseño cuidadoso
- **Audio en SQLite** — guardar como BLOB o en filesystem con referencia. Filesystem es mejor.

### Tiempo estimado (MVP)
- **Semana 1-2:** Scaffold + cámara + SQLite + entrada básica
- **Semana 3:** Notificaciones + geolocalización + tags
- **Semana 4:** Timeline (calendario, mapa, lista) + búsqueda
- **Semana 5:** Notas de voz + compresión + pulido
- **Semana 6:** Modo Cábala + compartir + export

~6 semanas para MVP funcional.

## Oportunidades de features adicionales

### Ya identificadas
- Widget foto del día
- Export zip con metadata
- Estadísticas
- Modo incógnito
- Modo paseo

### Nuevas ideas para evaluar
- **"El día en 3 fotos"** — resumen semanal/mensual generado automáticamente (collage)
- **Recordatorios contextuales** — "estás en un lugar donde ya sacaste fotos, ¿querés verlas?"
- **Mood tracking** — emoji de humor por entrada, sin complicar
- **Compartir como historia** — exportar un día completo como hilo de imágenes
- **Modo "desafío"** — ej: "30 días de fotos en blanco y negro", "7 días de texturas"
- **Backup cifrado opcional** — a iCloud Drive / Google Drive como archivo, no como sincronización
- **Watch app** — preview de la foto del día en el watch
- **Live Activity** — recordatorio persistente de "foto pendiente hoy"

## Riesgos / Debilidades

- **App store saturation** — hay muchas apps de diario/fotos. El diferenciador tiene que ser obvio en el primer minuto de uso.
- **3 fotos por día puede sentirse restrictivo** — para algunos es feature, para otros es limitación. Evaluar si hacerlo configurable.
- **Sin backend = sin sincronización** — si el usuario cambia de celular, pierde datos. El export mitiga esto parcialmente.
- **Monetización** — MVP sin monetización. Para producción, considerar compra única o "tip jar".

## Veredicto preliminar

**Go condicional.** La idea tiene un ángulo claro y ejecutable. El riesgo principal no es técnico sino de posicionamiento: la app tiene que comunicar su valor en segundos. Recomiendo invertir tiempo en el naming definitivo y el pitch de 1 línea antes de construir.

## Próximo paso

DEFINITION.md — definir MVP concreto, features priorizadas, user flow.
