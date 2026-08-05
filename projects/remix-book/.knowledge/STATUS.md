# STATUS — Full Stack Web Development with Remix

## Progreso general

| Capitulo | Estado | Proyectos | Fecha |
|----------|--------|-----------|-------|
| Preface | Saltado | — | — |
| Capitulo 1 | Completado | — | 2026-08-05 |
| Capitulo 2 | Completado | — | 2026-08-05 |
| Capitulo 3 | Completado | — | 2026-08-05 |
| Capitulo 4 | Completado | BeeRich (routing) | 2026-08-05 |
| Capitulo 5 | Completado | BeeRich (data) | 2026-08-05 |
| Capitulo 6 | Completado | BeeRich (UX) | 2026-08-05 |
| Capitulo 7 | Completado | BeeRich (errors) | 2026-08-05 |
| Capitulo 8 | Completado | BeeRich (auth) | 2026-08-05 |
| Capitulo 9 | Completado | BeeRich (assets) | 2026-08-05 |
| Capitulo 10 | Completado | BeeRich (uploads) | 2026-08-05 |
| Capitulo 11 | Completado | BeeRich (optimistic) | 2026-08-05 |

## Documentos generados

- `LEARNINGS.md` — conceptos clave, citas, preguntas, conexiones
- `ADR-001` a `ADR-011` — 11 ADRs cubriendo todos los patrones del libro

## Proyectos

### BeeRich (demo app del libro)

- **Ubicacion:** `bee-rich/`
- **Stack:** Remix v2 + Express.js + Prisma + SQLite + Tailwind CSS + bcrypt + Google Fonts
- **Estado:** Optimistic UI completo (capitulo 11)
- **Features:** Optimistic delete con `if (isSubmitting) return null`, optimistic attachment upload/remove con `navigation.formData`, error feedback inline con `fetcher.data`, disabled states condicionales

## Leyenda

- **Pendiente** — no procesado
- **En curso** — siendo analizado
- **Completado** — analizado, ejercicios hechos, documentado
- **Saltado** — no aplica / no relevante

## Ultima actualizacion

2026-08-05 — Capitulo 11 procesado. BeeRich con optimistic UI. ADR-011 creado.
