# Monad — Definición

## Visión (una frase)
Una app iOS que unifica proyectos, vida diaria, escritura y fotografía en un dashboard personal con IA local, sincronizado con tu workspace de desarrollo.

## MVP — Módulo Proyectos

### Qué entra
- Lista de proyectos desde el workspace (lee `projects/` del workspace)
- Cada proyecto muestra: nombre, estado, último commit, PRs abiertos (via GitHub API)
- Tarjetas con color por estado (activo, pausado, archivado)
- Pull-to-refresh para sincronizar
- Offline: muestra último estado conocido

### Qué NO entra (MVP)
- Editar proyectos desde la app
- Crear proyectos desde la app
- GitHub write operations

## MVP — Módulo Diario

### Qué entra
- Entrada diaria con fecha
- Texto libre (notas, ideas, reflexiones)
- Una foto asociada al día (opcional)
- Sincronización con `memory/YYYY-MM-DD.md` del workspace
- Las notas aparecen como daily notes en el workspace

### Qué NO entra (MVP)
- Edición de entradas pasadas
- Búsqueda
- Tags

## MVP — Módulo Escritura

### Qué entra
- Contador diario de palabras
- Racha de escritura (días consecutivos)
- Total del proyecto actual de ficción
- Input manual (escribes afuera, registras acá)

### Qué NO entra (MVP)
- Editor de texto
- Sincronización con archivos de escritura

## MVP — Módulo IA

### Qué entra
- Resumen automático del día (basado en notas + actividad)
- Sugerencia de próxima acción (qué proyecto merece atención)
- Todo local con CoreML + modelo pequeño

### Qué NO entra (MVP)
- Chat conversacional
- Análisis de fotos
- Predicciones complejas

## MVP — Módulo Fotos (post-MVP)

No entra en MVP. Se agrega después.

## MVP — Módulo Salud (post-MVP)

No entra en MVP. Se agrega después.

## Arquitectura

### Capas

```
┌─────────────────────────────┐
│       SwiftUI App           │
│  (Dashboard + Módulos)      │
├─────────────────────────────┤
│       SwiftData (local)      │
│  (offline-first, sync)      │
├─────────────────────────────┤
│    CoreML / Gemma 4 2B      │
│  (IA local, análisis)       │
├─────────────────────────────┤
│    Sync Engine (Swift)       │
│  (git pull/push workspace)   │
├─────────────────────────────┤
│    Supabase SDK              │
│  (auth, storage, sync)      │
└─────────────────────────────┘
```

### Flujo de datos

1. App escribe a SwiftData local
2. Sync Engine sube cambios a Supabase
3. Edge Functions procesan (push, webhooks)
4. Workspace recibe daily notes via git sync
5. IA local lee SwiftData y genera insights

## UX Principles

- **Offline-first:** la app funciona sin internet. Sync es background.
- **Una mano:** todo alcanzable con el pulgar. Tab bar en la parte inferior.
- **Privacidad por defecto:** nada se comparte. No hay perfiles públicos.
- **Ritmo diario:** la app se abre una vez al día. No es para consumo constante.
- **Sin notificaciones molestas:** solo una daily reminder opcional para escribir.

## Stack detallado

| Capa | Tecnología | Versión |
|---|---|---|
| UI | SwiftUI | iOS 18+ |
| Datos locales | SwiftData | iOS 18+ |
| IA local | CoreML + Gemma 4 2B (Q4) | — |
| Backend | Supabase | Plan Free/Pro |
| Sync | Custom Swift git client | — |
| Edge Functions | Deno / TypeScript | — |
| Auth | Supabase Auth (email + passkey) | — |

## Métricas de éxito (MVP)

- [ ] Gonzo abre la app al menos 5 días a la semana
- [ ] Las daily notes se sincronizan correctamente con el workspace
- [ ] Los proyectos se actualizan desde GitHub sin errores
- [ ] La IA local genera resúmenes útiles al menos 3 de 5 veces
- [ ] La app no crashea en uso normal
- [ ] Sync offline funciona sin pérdida de datos

## Posicionamiento

No es una app de productividad. Es **tu estado mental en un solo lugar**. No compite con Notion, Day One, o Streaks. Las reemplaza a todas con una interfaz que es solo tuya, privada, y con IA que te entiende porque vive en tu teléfono.
