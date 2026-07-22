# Nomad — ADR-001: Scaffold y estructura del proyecto

## Contexto
Arrancamos Nomad desde cero. Necesitamos definir la estructura del proyecto Xcode, el esquema de SwiftData, y las convenciones de código antes de escribir la primera línea.

## Decisión

### Estructura del proyecto

```
nomad/
├── Nomad/
│   ├── App/
│   │   └── NomadApp.swift
│   ├── Models/
│   │   ├── Project.swift
│   │   ├── DailyNote.swift
│   │   └── WritingSession.swift
│   ├── Views/
│   │   ├── Dashboard/
│   │   ├── Projects/
│   │   ├── Diary/
│   │   ├── Writing/
│   │   └── AI/
│   ├── Services/
│   │   ├── SyncService.swift
│   │   ├── GitHubService.swift
│   │   └── AIService.swift
│   ├── Utilities/
│   └── Resources/
├── Nomad.xcodeproj
├── .knowledge/
├── .gitignore
└── README.md
```

### SwiftData schema inicial

```swift
@Model
final class Project {
    var name: String
    var slug: String
    var status: String // "active", "paused", "archived"
    var lastCommitDate: Date?
    var openPRs: Int
    var lastSyncedAt: Date
}

@Model
final class DailyNote {
    var date: Date
    var content: String
    var photoData: Data?
    var syncedToWorkspace: Bool
    var createdAt: Date
    var updatedAt: Date
}

@Model
final class WritingSession {
    var date: Date
    var wordCount: Int
    var projectName: String
    var notes: String
}
```

### Convenciones
- SwiftUI con MVVM ligero (View + ViewModel, sin Combine innecesario)
- SwiftData como fuente de verdad local
- iOS 18+ target (Foundation Models requiere iOS 27+, pero el resto de la app funciona en 18+)
- Sin dependencias externas en Fase 0 (ni Alamofire, ni Kingfisher, nada)
- Formateo con swift-format

### Dependencias (futuras)
- Supabase SDK (Fase 1)
- GitHub REST API via URLSession (Fase 1)

## Consecuencias
- Positivo: estructura clara desde el día 1, fácil de navegar
- Positivo: sin deuda técnica de scaffolding
- Negativo: iOS 18+ target deja fuera iPhones viejos (no relevante para uso personal)
- Negativo: sin dependencias externas vamos a escribir más código nosotros (tradeoff aceptable para aprender)
