# Nomad — Handoff

## Estado: Archivado (22-Jul-2026)

### Resumen
Nomad se implementó como app iOS nativa (SwiftUI + SwiftData + Swift 6) con Package Manager. Se llegó a build exitoso para target iOS 18+ (simulador), pero no se pudo ejecutar debido a bugs del simulador de iOS 27 beta 4 (PosterBoard crash) + falta de cable para test on device.

### Stack implementado
- SwiftUI + SwiftData (modelos: Project, DailyNote, WritingSession)
- GitHub SyncService (trae repos como proyectos)
- PhotosPicker para adjuntar fotos al diario
- Stepper para word count en writing sessions
- NavigationStack + TabView

### Archivos modificados durante la sesión
- `Package.swift` → cambiado de `.library` a `.executableTarget`
- `Sources/Nomad/Models/Project.swift` → `@available(iOS 17, macOS 14, *)`
- `Sources/Nomad/Models/DailyNote.swift` → `@available(iOS 17, macOS 14, *)`
- `Sources/Nomad/Models/WritingSession.swift` → `@available(iOS 17, macOS 14, *)`
- `Sources/Nomad/Services/SyncService.swift` → `@available` + `@unchecked Sendable` + `@MainActor` en `syncProjects` + reemplazo de `#Predicate` por filter manual
- `Sources/Nomad/App/NomadApp.swift` → `@available(iOS 17, macOS 14, *)`
- `Sources/Nomad/Views/Projects/ProjectsView.swift` → `@available` + `@MainActor` en `performSync` + subview `ProjectRow` con `@available`
- `Sources/Nomad/Views/Diary/DiaryView.swift` → `@available` + subview `PhotoPickerLabel` + fix concurrency en `onChange` + reemplazo de UIKit por ImageIO
- `Sources/Nomad/Views/Writing/WritingView.swift` → `@available` + reemplazo de TextField numérico por Stepper (bug de keyboardType en iOS 27 beta)
- `Sources/Nomad/Views/AI/AIView.swift` → `@available(iOS 16, macOS 13, *)`

### Problemas conocidos
1. **Simulador iOS 27 beta 4 crashea** — PosterBoard crash al iniciar (wallpaper system). Bug de la beta. Solución: test on device o esperar beta 5.
2. **KeyboardType en TextField+format(.number)** — no disponible en iOS 27 beta 4. Workaround: Stepper.
3. **navigationBarTitleDisplayMode** — unavailable en macOS. Sacado del código.
4. **Swift 6 strict concurrency** — varios warnings de Sendable/actor isolation fixeados con `@MainActor` + `@unchecked Sendable`.

### Pendientes
- Test on device (requiere cable USB-C)
- GitHub token setup sheet funcional
- AI insights view (placeholder)
- Sync de daily notes al workspace (Fase 2)
- App Store distribution (post-MVP)

### Fases originales
- Fase 0: Setup + scaffold ✅ (completado)
- Fase 1: GitHub sync + Project list ✅ (build exitoso)
- Fase 2: Diario + Escritura ✅ (build exitoso)
- Fase 3: AI insights ❌ (placeholder)
- Fase 4: Foundation Models ❌ (no iniciado)

### Cómo retomar
1. Abrir `Nomad.xcodeproj` en Xcode
2. Seleccionar simulador de iOS (evitar iOS 27 beta si sigue roto)
3. Build For > Running (Cmd+Shift+R)
4. Si build falla: `rm -rf ~/Library/Developer/Xcode/DerivedData/nomad-*`
5. Run (Cmd+R)
