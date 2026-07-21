# HANDOFF — Cábala

## Contexto

App mobile de bitácora visual: 3 fotos por día, organizadas por ubicación y tiempo, con notas de voz, tags, modo Cábala (replicar fotos del pasado), desafíos de fotografía.

## Estado actual

**Fase 0: Discovery COMPLETADA.** Producto definido, documentación generada en `.knowledge/`.

## Documentación generada

- `BRIEF.md` — visión, problema, stack
- `EVALUATION.md` — mercado, competidores, viabilidad, features adicionales
- `DEFINITION.md` — MVP, personas, features priorizadas, user flow
- `ARCHITECTURE.md` — stack, estructura, decisiones técnicas
- `DATA_MODEL.md` — esquema SQLite completo
- `DESIGN.md` — paleta, tipografía, componentes, onboarding
- `ROADMAP.md` — fases y semanas estimadas
- `STATUS.md` — estado actual

## Próximo paso

**Fase 1, Semana 1-2:** Scaffold Expo + SQLite + cámara + entrada básica.

Usar `workflow-build-scaffold` para crear el proyecto.

## Decisiones clave

- **Stack:** Expo + TypeScript + expo-sqlite + expo-router
- **Sin backend:** 100% offline, SQLite local
- **3 fotos default:** configurable en settings, no obvio
- **Notificaciones por ventanas:** no horas fijas, márgenes configurables
- **Compresión automática:** calidad pantalla de celular
- **Backup:** export manual + backup cifrado opcional a iCloud/Google Drive (post-MVP)
- **Nombre tentativo:** Cábala (evaluar antes de publicar)
