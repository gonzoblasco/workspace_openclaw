# SoporteML v4 - PLAN

> **Filosofía (2026-08-17):** este ecosistema de MDs es un **sistema vivo** que crece paso a paso. No fijamos el contenido de todas las fases con anticipación. Definimos los requisitos y recursos de la **fase actual**, la ejecutamos, y recién entonces definimos la siguiente. Cada fase se revisa y ajusta al alcanzarla.

**Sueño:** un CRM para vendedores de MeLi que se sienta premium - diseño impactante, IA que realmente ayuda, features completas. No un template.

**MVP de V4:** el frontend reconstruido con diseño avanzado + las features core desbloqueadas (bandeja, KB, autopilot, clientes, métricas), sobre el backend sólido de v3.

**Decisiones clave (2026-08-17):**
- **Conservar** backend + capa de datos de v3 (activo valioso, no se tira).
- **Reconstruir** frontend con diseño avanzado (CSS custom, identidad propia, a11y integrada).
- **Desbloquear** features que el schema ya modela pero la UI no expone.
- **Metodología** de Kanam Story/Forge adaptada: pipeline A/B, slices finos, `.knowledge/` vivo.

---

## Fase 0 - Fundamentos del reinicio (EN CURSO)

**Objetivo:** asegurar la base antes de construir: backend sano, identidad visual decidida, tests del API.

### Requisitos de la Fase 0

- [x] Crear `.knowledge/` de V4 (BRIEF, PLAN, STATUS)
- [x] **Decidir la identidad visual de V4** (ADR-001) - híbrido oscuro + color por categoría
- [x] Mockup de identidad validado por Gonzo (`mockups/identidad-v4.html`)
- [x] Iconografía Lucide incorporada (ADR-030, workspace)
- [x] **Verificar que el backend de v3 funciona** - verificado de punta a punta (`BACKEND-VERIFICADO.md`)
- [x] **Agregar tests del API** (el backend de v3 no tiene cobertura - hallazgo de la verificación)
- [x] **Definir el pipeline A/B para este proyecto** (`PIPELINE-AB.md`)

**Criterio de salida de Fase 0:** backend verificado + tests del API agregados + identidad visual decidida + pipeline definido. Recién entonces se define la Fase 1 (primer slice del frontend).

## Fase 1 - Pulido + integraciones (EN CURSO)

**Objetivo:** cerrar los pendientes de calidad (RAG, code-splitting) y validar las integraciones reales (email, MP, OAuth MeLi).

### Unidades (pipeline A/B, ver `PIPELINE-AB.md`)

- [ ] U1 - Ajuste fino RAG (minScore) - Agente A
- [ ] U2 - Code-splitting (chunk > 500kB) - Agente B
- [ ] U3 - Validación visual de Gonzo - Orquestador
- [ ] U4 - Email (Resend) - Agente B
- [ ] U5 - Mercado Pago (billing real) - Agente A
- [ ] U6 - OAuth MeLi real (túnel persistente) - Agente B

---

## Fases futuras (se definen al alcanzarlas, no con anticipación)

> Estas son direcciones tentativas, NO un plan congelado. Se revisan y ajustan cuando se alcanza cada fase.

- **Fase 1 (tentativa):** reconstruir el esqueleto visual del frontend con la identidad nueva (layout, sidebar, bandeja).
- **Fase 2 (tentativa):** desbloquear features que el schema ya modela (KB, autopilot, SLA, plantillas, clientes, métricas).
- **Fase 3 (tentativa):** validar integraciones restantes (Mercado Pago, email).
- **Fase 4 (tentativa):** decisión de despliegue + beta.

---

## Riesgos / a considerar

- **No perder el backend de v3:** el reinicio es del frontend y del alcance, no del backend. Conservar OAuth MeLi + schema.
- **El API no tiene tests:** agregar cobertura antes de construir el frontend encima (red de seguridad).
- **Diseño avanzado ≠ sobre-ingeniería:** el CSS custom debe ser mantenible y accesible, no solo bonito. Balance entre impacto y calidad.
- **Alcance:** no ampliar a e-commerce/ERP (límites de PRODUCT.md de v3 se mantienen). El foco es la bandeja + IA.
- **Mercado Pago** sigue siendo el mayor riesgo técnico (nunca probado) - aislado en Fase 3, no bloquea.
