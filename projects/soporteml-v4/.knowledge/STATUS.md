# SoporteML v4 - STATUS

**Actualizado:** 2026-08-17

## Estado: 🟡 REINICIO - Fase 0 en curso

## Fase 0 - Fundamentos del reinicio

- [x] Crear `.knowledge/` de V4 (BRIEF, PLAN, STATUS)
- [x] **Decidir la identidad visual de V4** - dirección híbrido oscuro + color por categoría (ADR-001)
- [x] Mockup de identidad validado por Gonzo (`mockups/identidad-v4.html`)
- [x] Iconografía Lucide incorporada al mockup (ADR-030, workspace)
- [ ] Decidir el alcance del primer slice
- [ ] Definir el pipeline A/B para este proyecto

## Identidad visual decidida (2026-08-17)

**Dirección:** híbrido oscuro + color por categoría (ADR-001).

- Base oscura premium (`#0a0e1a`) + acento amarillo MeLi (`#ffe600`) con glow
- Color por categoría de consulta (precio=azul, stock=verde, técnico=violeta, envío=naranja, garantía=rosa)
- Iconografía Lucide (ADR-030)
- Micro-interacciones + a11y WCAG 2.1 AA integrada
- Mockup validado: `mockups/identidad-v4.html`

## Contexto del reinicio

**Motivo (decisión de Gonzo, 2026-08-17):** v3 quedó como template básico - features limitadas en la UI (solo 3 vistas genéricas) y UI/UX sosa (cards shadcn estándar, cero diseño avanzado). V4 reconstruye el frontend con diseño impactante y desbloquea las features que el schema ya modela.

**Activo conservado de v3:** backend (OAuth MeLi real, sync, IA, billing mock) + capa de datos (schema 20+ tablas, repositorios) + token real de producción MeLi.

**Metodología:** pipeline en cadena A/B, slices finos con release usable, `.knowledge/` vivo, a11y WCAG 2.1 AA integrada, diseño avanzado con CSS custom. Adaptada de Kanam Story/Forge, no fuente única de verdad.

## Próximo paso

Decidir la identidad visual de V4 con Gonzo (moodboard, dirección de diseño, tokens) antes de tocar código.
