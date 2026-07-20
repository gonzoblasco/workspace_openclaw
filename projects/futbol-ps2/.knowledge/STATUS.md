# STATUS — Juego de Fútbol 3D (FIFA/PES PS2-like)

**Última actualización:** 2026-07-20

## Estado general

🟢 **Setup completo** — Fase 0 terminada, proyecto Godot funcional

## Progreso por fase

| Fase | Estado | % |
|------|--------|---|
| 0 — Setup del proyecto | ✅ Completa | 100% |
| 1 — La cancha | ✅ Completa | 100% |
| 2 — La pelota | ✅ Completa | 100% |
| 3 — El jugador | ✅ Completa | 100% |
| 4 — El equipo humano | ✅ Completa | 100% |
| 5 — IA CPU | ✅ Completa | 100% |
| 6 — Reglas básicas | ✅ Completa | 100% |
| 7 — UI y pulido MVP | ✅ Completa | 100% |

## MVP

**Definido:** Partido 1vsCPU, 5 min, 2 equipos genéricos, controles teclado, cámara dinámica PS2

**Completitud:** 100% — 🎉 MVP COMPLETO

## Próximo paso

Post-MVP: menú principal, selección de equipos, offside, faltas, córners, sonido, gamepad, 2 jugadores locales

## Pendientes inmediatos

- Ajustar cámara para que el campo ocupe todo el viewport (eliminar letterboxing negro a los costados)
- La cámara está más cerca (pos 0,12,15, rot -50°, FOV 50°) pero el campo no escala al ancho de la ventana

## Bloqueos

Ninguno. Godot 4.4+ instalado.

## Cambios recientes

- **2026-07-20:** Ajuste de cámara: posición (0,12,15), rotación -50°, FOV 50°. Los jugadores se ven más grandes pero el campo no ocupa todo el viewport horizontal.
