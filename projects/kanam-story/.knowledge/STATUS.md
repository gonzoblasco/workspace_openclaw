# STATUS — Kanam Story

**Actualizado:** 2026-08-12

## Estado: 🟢 En definición (Slice 1 en planificación)

- [x] Interview-me convergido (intención confirmada)
- [x] BRIEF
- [x] DATA_MODEL
- [x] ROADMAP (slices 0-5)
- [ ] Slice 0: Fundación sobre sudolab
- [ ] Slice 1: Chat con Manos (MVP con `ultimo-turno`)

## Decisiones clave

| Decisión | Opción |
|---|---|
| Base de código | `sudolab` (Next.js 16, TipTap 3, IndexedDB, Ollama) |
| El corazón | Chat con agente que **aplica** cambios (ContentAction) |
| Modelo de aceptación | Propuesta → diff/resumen → aceptar/deshacer |
| Estructura | Outline & Beats por capítulo/escena, manual o sugerido por IA |
| Idioma | Español (UI y prompts) |
| Slice fino primero | Sí, para no repetir el patrón de abandono |

## Próximo paso

Copiar base `sudolab` → crear stores de chat → Slice 1.
