# Monad — Status

## Estado actual
Discovery completo. GO decidido. Pendiente de inicio de Fase 0.

## Próximo paso
Setup del proyecto Xcode + scaffold inicial.

## Decisiones tomadas
- Nombre: Monad
- Stack: SwiftUI + SwiftData + CoreML + Supabase
- MVP: 4 módulos (Proyectos, Diario, Escritura, IA)
- IA local con Gemma 4 2B (Q4), plan B si no corre en 14 Pro
- Offline-first desde el día 1
- Sin publicación en App Store (por ahora)

## Decisiones tomadas
- Repo separado: `@gonzoblasco/nomad` (`.knowledge/` queda en workspace)
- Supabase: Free plan (MVP)
- IA local: Foundation Models framework (iOS 27+) como plan A. Gemma 4 2B via Core ML como plan C.
- Apple LLM integration: Foundation Models framework es la respuesta. 0MB, ~3B params, guided generation, tool calling.

## Riesgos activos
- Foundation Models requiere iOS 27+ (iPhone 14 Pro lo soporta)
- El modelo de Apple (~3B) puede no ser suficiente para tareas específicas
- Scope creep (MVP definido, hay que mantenerlo)
- SwiftUI learning curve (real pero manejable)
