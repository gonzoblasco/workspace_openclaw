# Monad — Roadmap

## Fase 0: Foundation (Semana 1-2)
- [ ] Setup del proyecto Xcode + SwiftUI
- [ ] SwiftData schema inicial (Project, DailyNote, WritingSession)
- [ ] Tab bar con módulos (Proyectos, Diario, Escritura, IA)
- [ ] Navegación básica entre módulos
- [ ] Conexión a Supabase (auth + sync)

## Fase 1: Módulo Proyectos (Semana 3-4)
- [ ] Leer `projects/` del workspace (mock local primero)
- [ ] Lista de proyectos con estado y color
- [ ] Pull-to-refresh
- [ ] Integración GitHub API (solo lectura)
- [ ] Offline: último estado conocido

## Fase 2: Módulo Diario (Semana 5-6)
- [ ] Entrada diaria con fecha
- [ ] Editor de texto libre
- [ ] Adjuntar foto del día
- [ ] Sync con `memory/YYYY-MM-DD.md`
- [ ] Offline: guarda local, sync cuando hay conexión

## Fase 3: Módulo Escritura (Semana 7)
- [ ] Contador diario de palabras
- [ ] Racha de escritura
- [ ] Input manual

## Fase 4: Módulo IA (Semana 8-10)
- [ ] Integrar Gemma 4 2B via CoreML
- [ ] Resumen automático del día
- [ ] Sugerencia de próxima acción
- [ ] Evaluar performance en iPhone 14 Pro

## Fase 5: Sync Engine (Semana 11-12)
- [ ] Git sync bidireccional con workspace
- [ ] Manejo de conflictos
- [ ] Push de daily notes al workspace

## Fase 6: Polish (Semana 13-16)
- [ ] Widgets (Lock Screen, Home Screen)
- [ ] Daily reminder (push notification)
- [ ] Dark mode
- [ ] Animaciones y transiciones
- [ ] Performance profiling
- [ ] Beta testing personal (usar la app 2 semanas)

## Post-MVP
- [ ] Módulo Fotos (portfolio fotográfico)
- [ ] Módulo Salud (actividad física, sueño)
- [ ] Watch app
- [ ] Widgets interactivos
- [ ] Siri shortcuts
- [ ] Live Activities
