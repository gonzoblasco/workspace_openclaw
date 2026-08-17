# SoporteML v4 - PLAN

**Sueño:** un CRM para vendedores de MeLi que se sienta premium - diseño impactante, IA que realmente ayuda, features completas. No un template.

**MVP de V4:** el frontend reconstruido con diseño avanzado + las features core desbloqueadas (bandeja, KB, autopilot, clientes, métricas), sobre el backend sólido de v3.

**Decisiones clave (2026-08-17):**
- **Conservar** backend + capa de datos de v3 (activo valioso, no se tira).
- **Reconstruir** frontend con diseño avanzado (CSS custom, identidad propia, a11y integrada).
- **Desbloquear** features que el schema ya modela pero la UI no expone.
- **Metodología** de Kanam Story/Forge adaptada: pipeline A/B, slices finos, `.knowledge/` vivo.

---

## Fase 0 - Fundamentos del reinicio (EN CURSO)

**Objetivo:** definir la identidad visual de V4 y la estructura del trabajo antes de tocar código.

- [x] Crear `.knowledge/` de V4 (BRIEF, PLAN, STATUS)
- [ ] **Decidir la identidad visual de V4** (el corazón del reinicio):
  - [ ] Moodboard / dirección de diseño (¿oscuro premium? ¿claro limpio? ¿acento amarillo MeLi? ¿otra?)
  - [ ] Design tokens propios (no los genéricos de v3)
  - [ ] Tipografía, espaciado, elevación, micro-interacciones
  - [ ] ADR de identidad visual
- [ ] Decidir el alcance del primer slice (¿bandeja rediseñada? ¿onboarding? ¿KB?)
- [ ] Definir el pipeline A/B para este proyecto (agentes, prompts, cross-review)

**Criterio de salida:** identidad visual decidida y documentada, primer slice definido, pipeline listo.

---

## Fase 1 - Fundación visual (primer slice)

**Objetivo:** reconstruir el esqueleto visual de la app con la identidad nueva. Nada de template.

- [ ] Design system avanzado: tokens propios, CSS custom, componentes de marca
- [ ] Layout principal rediseñado (sidebar, header, navegación) con identidad propia
- [ ] Login/onboarding con diseño impactante (no la card genérica de v3)
- [ ] Bandeja de consultas rediseñada (el corazón del producto) con micro-interacciones
- [ ] Playground de componentes actualizado a la identidad nueva
- [ ] a11y WCAG 2.1 AA integrada + validación AT manual

**Criterio de salida:** la app se ve y se siente premium, no template. Bandeja usable con diseño avanzado.

---

## Fase 2 - Features desbloqueadas

**Objetivo:** exponer en la UI las features que el schema ya modela.

- [ ] **KB (RAG):** artículos + búsqueda semántica + respuesta con contexto de la empresa
- [ ] **Autopilot:** sugerencia automática con IA + aprobación humana (definir el flujo)
- [ ] **SLA:** tracking de tiempo de respuesta + alertas
- [ ] **Plantillas:** respuestas reutilizables con variables
- [ ] **Clientes:** CRM de compradores con tags + historial
- [ ] **Métricas:** dashboard con datos reales de ventas/consultas

**Criterio de salida:** todas las features del schema accesibles desde una UI premium.

---

## Fase 3 - Validación de integraciones restantes

**Objetivo:** probar lo que nunca se validó.

- [ ] Mercado Pago real en sandbox (suscripciones recurrentes + webhook IPN)
- [ ] Email (Resend + Lovable Email) para alertas SLA
- [ ] IA con API keys reales si hace falta

**Criterio de salida:** integraciones probadas o descartadas con razón.

---

## Fase 4 - Decisión de despliegue + Beta

**Objetivo:** llevar el producto a producción.

- [ ] Evaluar Supabase vs backend propio (con razones válidas, no por default)
- [ ] Migrar SQLite → Postgres si corresponde
- [ ] Auth real + CI/CD
- [ ] Onboarding de primeros vendedores + iterar con feedback real

---

## Riesgos / a considerar

- **No perder el backend de v3:** el reinicio es del frontend y del alcance, no del backend. Conservar OAuth MeLi + schema.
- **Diseño avanzado ≠ sobre-ingeniería:** el CSS custom debe ser mantenible y accesible, no solo bonito. Balance entre impacto y calidad.
- **Alcance:** no ampliar a e-commerce/ERP (límites de PRODUCT.md de v3 se mantienen). El foco es la bandeja + IA.
- **Mercado Pago** sigue siendo el mayor riesgo técnico (nunca probado) - aislado en Fase 3, no bloquea.
