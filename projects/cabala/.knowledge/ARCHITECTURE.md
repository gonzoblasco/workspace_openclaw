# ARCHITECTURE — Cábala

## Stack

- **Framework:** React Native + Expo SDK 52+
- **Lenguaje:** TypeScript
- **Navegación:** expo-router (file-based routing)
- **Base de datos:** expo-sqlite (SQLite local)
- **Estado global:** React Context + hooks (sin Redux/Zustand para mantenerlo simple)
- **Mapa:** react-native-maps (Apple Maps / Google Maps)
- **Audio:** expo-av (grabación y reproducción)
- **Notificaciones:** expo-notifications
- **Cámara:** expo-camera + expo-image-picker
- **Compresión:** expo-image-manipulator
- **Geolocalización:** expo-location
- **Widget:** expo-widget (iOS) / expo-app-widgets (Android)
- **Backup:** expo-file-system + expo-sharing (para export); iCloud/Google Drive vía share sheet

## Arquitectura general

```
App
├── app/                    # expo-router pages
│   ├── (tabs)/             # Tab navigation
│   │   ├── index.tsx       # Timeline (default)
│   │   ├── calendar.tsx    # Vista calendario
│   │   ├── map.tsx         # Vista mapa
│   │   └── settings.tsx    # Configuración
│   ├── entry/
│   │   ├── [id].tsx        # Detalle de entrada
│   │   └── new.tsx         # Nueva entrada (cámara)
│   └── _layout.tsx
├── components/             # UI components reutilizables
│   ├── EntryCard.tsx
│   ├── PhotoGrid.tsx
│   ├── TagInput.tsx
│   ├── VoiceRecorder.tsx
│   ├── MapView.tsx
│   ├── CalendarView.tsx
│   └── CabalaPrompt.tsx
├── db/                     # Database layer
│   ├── schema.ts           # Definición de tablas
│   ├── migrations.ts      # Migraciones
│   └── queries.ts          # Queries tipadas
├── hooks/                  # Custom hooks
│   ├── useEntries.ts
│   ├── useNotifications.ts
│   ├── useLocation.ts
│   ├── useCamera.ts
│   └── useCabala.ts
├── services/               # Lógica de negocio
│   ├── photo.service.ts    # Compresión, almacenamiento
│   ├── audio.service.ts    # Grabación, reproducción
│   ├── export.service.ts   # Export/backup
│   ├── notification.service.ts
│   └── challenge.service.ts
├── types/                  # TypeScript types
│   └── index.ts
├── constants/              # Constantes
│   └── index.ts
└── utils/                  # Utilidades
    ├── date.ts
    ├── geo.ts
    └── compression.ts
```

## Data flow

```
User → Camera → Image → Compression → Save to filesystem
                                    → Insert metadata to SQLite
                                    → Update timeline UI

Notification → User opens app → Check pending photos today
                              → If < limit, show prompt
                              → If >= limit, show timeline
```

## Decisiones arquitectónicas

### ¿Por qué SQLite y no algo más?
- Sin backend, sin cuenta. SQLite es lo más simple que funciona offline.
- expo-sqlite es maduro y bien mantenido.

### ¿Por qué no Zustand/Redux?
- La app es chica. El estado se maneja con React Context + queries a SQLite.
- Si crece, se puede migrar. No premature optimization.

### ¿Archivos de audio en filesystem o SQLite?
- Filesystem. SQLite guarda la referencia (path). Los BLOBs en SQLite son lentos y ocupan espacio innecesario en la DB.

### ¿Compresión en cliente?
- Sí, con expo-image-manipulator. Se comprime antes de guardar. La original se descarta.

### ¿Galería?
- No. Solo cámara. La foto se toma en el momento o no es. Esto refuerza el concepto de bitácora del presente.
