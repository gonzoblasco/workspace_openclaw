# STATUS.md — Quedamos

> Estado: **Arquitectura** (Fase 0.2 completa)
> Próximo paso: Go/No-Go → Build & Scaffold

## Hitos

- [x] 2026-07-24: Idea inicial (inspirada en Timeleft)
- [x] 2026-07-24: Product Discovery Fase 0.1 — BRIEF, DEFINITION, EVALUATION
- [x] 2026-07-24: Product Discovery Fase 0.2 — ARCHITECTURE, DATA_MODEL, ADRs, ROADMAP, TRACKER
- [ ] Pendiente: Product Discovery Fase 0.3 — DESIGN.md (identidad visual, wireframes)
- [x] 2026-07-25: Repo creado: github.com/gonzoblasco/quedamos
- [x] 2026-07-25: Fase 0.4 — Issues creados (4 epics, 30 issues) con labels por sprint
- [ ] Pendiente: Respuesta de amigos devs
- [ ] Pendiente: Go/No-Go final
- [ ] Pendiente: Build & Scaffold
- [ ] Pendiente: MVP (Sprints 1-4)

## Decisiones Tomadas

- **Nombre:** Quedamos
- **Matching:** Opción B (semi-automático, compatibility score visible) — es core
- **Creación de salidas:** Solo la plataforma (y eventualmente comercios) programa salidas. Los usuarios se suman a las existentes.
- **Cupos:** 20 para comida, 40 para cine, según capacidad del lugar.
- **Visibilidad:** Las salidas se ven, no hay acertijo
- **Sugerencias:** 5 semanales por usuario (core loop)
- **Apodos:** Sí, sin foto requerida
- **Feedback:** Anónimo post-salida, alimenta algoritmo
- **Tecnología:** PWA (Next.js 15 + Supabase)
- **Licencia:** Código visible con licencia restrictiva
- **Monetización futura:** Locales pagan por visibilidad/descuentos (tipo Groupon inverso)
- **Gobernanza:** Sin admins con poder absoluto. Bloqueos individuales, no expulsiones.
- **Filosofía:** No es negocio, es proyecto de vida. Hacer amigos.
- **Rango edad:** 20-45

## Archivos Generados

### Fase 0.1
- `BRIEF.md` — Visión, problema, features core, métricas
- `DEFINITION.md` — Personas, user journey, principios, algoritmo conceptual, fases
- `EVALUATION.md` — Mercado, competidores, viabilidad, veredicto Go

### Fase 0.2
- `ARCHITECTURE.md` — Stack definitivo, patrones, diagrama C4, riesgos
- `DATA_MODEL.md` — Esquemas SQL completos, índices, RLS, funciones
- `ROADMAP.md` — 4 sprints, desglose de tareas, dependencias, riesgos
- `TRACKER.md` — Seguimiento de progreso
- `docs/adr/ADR-001-pwa-vs-nativa.md`
- `docs/adr/ADR-002-supabase-backend.md`
- `docs/adr/ADR-003-matching-algorithm.md`
- `docs/adr/ADR-004-sin-admins.md`
- `docs/adr/ADR-005-sugerencias-semanales.md`

### Reclutamiento
- `PITCH_DEVS.md` — Documento para compartir con amigos devs
