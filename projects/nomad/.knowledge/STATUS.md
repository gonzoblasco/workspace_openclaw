# Nomad — Status

## Estado actual: Archivado (22-Jul-2026)
Build exitoso para iOS 18+. No se pudo ejecutar por bugs del simulador de iOS 27 beta 4.

## Lo que se completó
- ✅ Fase 0: Setup + scaffold
- ✅ Fase 1: GitHub sync + Project list (SwiftData models + SyncService)
- ✅ Fase 2: Diario + Escritura (DailyNote, WritingSession, PhotosPicker)
- ✅ Build exitoso para iOS 18+ simulator
- ❌ Fase 3: AI insights (placeholder solamente)
- ❌ Fase 4: Foundation Models (no iniciado)

## Próximos pasos (cuando se retome)
1. Test on device o con simulador funcional (iOS 26 o iOS 27 beta 5+)
2. Implementar AI insights (Fase 3)
3. Foundation Models integration (Fase 4)
4. Evaluar publicación en App Store

## Decisiones tomadas
- SwiftUI + SwiftData + Swift 6
- GitHub como fuente de datos de proyectos
- Offline-first con SwiftData local
- Sin UIKit (reemplazado por ImageIO para fotos)
- iOS 18+ target
