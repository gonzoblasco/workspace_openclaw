# SoporteML v3 - STATUS

## 2026-08-11 - Definición de producto

### Completado
- **Creado `PRODUCT.md`** - definición completa del producto: visión, usuarios/roles, features core, integraciones (MeLi funcional, MP nunca probado), límites explícitos, principios de arquitectura (independencia de vendor, alpha 100% local), preguntas abiertas.
- **Creado `ROADMAP.md`** - roadmap vivo: Fase 0 definición → Fase 1 alpha local → Fase 2 validación de integraciones → Fase 3 decisión de despliegue → Fase 4 beta.
- **Actualizado `BRIEF.md`** - refleja la nueva dirección: independencia de vendor, alpha local, stack propuesto.
- **Decisión de dirección (Gonzo):** primera alpha 100% local (SQLite + backend local). Supabase solo si hay razones válidas después. Recrear edge functions en runtime local (Deno/Node+Hono a decidir). Mercado Pago nunca probado → mockear en alpha.

### Pendiente (Fase 0)
- [ ] Resolver preguntas abiertas de PRODUCT.md (sección 7)
- [ ] Decidir runtime del backend (Deno vs Node+Hono) → ADR
- [ ] Cruzar tokens de Lovable contra v1 → ADR design system
- [ ] Definir estructura del monorepo

## 2026-08-07 - Arranque (sesión nocturna)

### Completado
- Creado repo v3 con estructura `.knowledge/`.
- Copiado `UI-DESIGN-SKILL.md` (estándar de implementación, basado en v1).
- Creado `DESIGN-GUIDE.md` (identidad visual documentada desde el código real de v1).
- Creado `BRIEF.md` con contexto de versiones (v1 = referencia, v2 = experimento descartado).
- **Recibida la guía de diseño oficial de Lovable** → guardada en `DESIGN-GUIDE-LOVABLE.md` (fuente de verdad de identidad visual para v3).
- Guardados prompts de referencia en `prompts/`:
  - `PROMPT-GUIA-DISENO.md` (ya ejecutado)
  - `PROMPT-SCHEMAS-BD.md` (pendiente de ejecutar)

## 2026-08-11 - Backend + design tokens aclarados

### Completado
- **Recibida la referencia técnica del backend de Lovable** → guardada en `BACKEND-REFERENCE.md` (327 líneas).
  - Schemas completos de Supabase/PostgreSQL: 20+ tablas, enums, RLS por tabla, funciones SQL, triggers, jobs pg_cron.
  - 25 Edge Functions con auth, input/output e integraciones.
  - Integraciones: MeLi (OAuth PKCE + webhook + cron), Lovable AI Gateway (Gemini), OpenAI embeddings, Mercado Pago (preapproval), Resend, Lovable Email.
  - Roles: agent / admin / super admin. Multi-tenant vía `memberships` + `user_belongs_to_company`.
  - Variables de entorno completas (solo nombres).
- El prompt `prompts/PROMPT-SCHEMAS-BD.md` quedó **ejecutado**.
- **Recibida la especificación de design tokens de Lovable** → guardada en `DESIGN-TOKENS-LOVABLE.md` (423 líneas).
  - Tokens nuevos: `--primary-muted`, `--primary-strong`, `--informative` (+foreground/muted/strong), `--surface-active`, `--surface-raised`, `--surface-sunken`, `--overlay`, `--glass`, `--focus-ring`, `--border-strong`, `--chart-1..5`, `--success/warning/destructive/informative-*-muted/strong`, badges de categoría con muted/strong.
  - Regla de estado global: fondo 12-15% + texto 100% con `*-strong` (no color base). Preferir tokens `*-muted` sobre `bg-<estado>/15`.
  - Escala tipográfica fina (Display→Micro/Overline/Metric/Mono) con Inter, tabular-nums para métricas.
  - Paleta completa v3 (base, marca, estados, badges, bordes, sidebar, gráficos, radio/sombras) + mapa token→componente + reglas WCAG AA + snippet CSS/Tailwind.
- El prompt `prompts/PROMPT-RECONCILIACION-TOKENS.md` quedó **ejecutado**.

### Pendiente
- [ ] Cruzar `DESIGN-TOKENS-LOVABLE.md` contra `DESIGN-GUIDE.md` y el skill (verificar que no haya conflictos con v1).
- [ ] Scaffold del repo v3.
- [ ] Implementación.

## Objetivo
Arrancar la versión definitiva de SoporteML a más tardar el lunes, con el design system y el backend aclarados desde el día uno.
