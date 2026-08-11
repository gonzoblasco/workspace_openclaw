# SoporteML v3 - BRIEF

## Estado: EN DEFINICIÓN (2026-08-11)

## Qué es

CRM multi-tenant para vendedores de Mercado Libre, con asistencia de IA. Gestiona consultas, productos, stock, envíos, garantías y métricas.

## Contexto de versiones

- **v1** (`soporteml`): la versión de referencia. Design system estable, documentado en `.knowledge/`.
- **v2** (`soporteml-v2`): **EXPERIMENTO - NO USAR DE REFERENCIA.** Se descarta.
- **v3** (`soporteml-v3`): repo nuevo, en arranque. Se construye sobre v1.

## Objetivo de v3

Reconstruir SoporteML sobre la base sólida de v1, con el design system y el backend aclarados desde el arranque, **independizándonos de los servicios cloud** (primera alpha 100% local: SQLite + backend local). Supabase u otros servicios son opción futura solo con razones válidas.

## Documentos de referencia

- `PRODUCT.md` - definición completa del producto (visión, usuarios, features, límites, principios).
- `ROADMAP.md` - roadmap vivo (Fase 0 definición → Fase 1 alpha local → Fase 2 validación → Fase 3 despliegue → Fase 4 beta).
- `BACKEND-REFERENCE.md` - referencia técnica del backend actual (schemas, edge functions, integraciones).
- `DESIGN-TOKENS-LOVABLE.md` - design tokens oficiales de Lovable (fuente de verdad visual).
- `DESIGN-GUIDE.md` - identidad visual de SoporteML documentada desde v1.
- `UI-DESIGN-SKILL.md` - estándar de implementación UI.

## Stack (propuesto, a confirmar en ADR)

- Frontend: React + TypeScript + Vite + Tailwind + shadcn/ui + Radix + Lucide + Framer Motion
- Backend local: runtime a decidir (Deno vs Node+Hono) — recrear edge functions
- DB alpha: SQLite con capa de repositorios (Postgres/Supabase como opción futura)

## Pendiente (ver ROADMAP.md)

- [ ] Resolver preguntas abiertas de PRODUCT.md
- [ ] Decidir runtime del backend (ADR)
- [ ] Cruzar tokens de Lovable contra v1 (ADR design system)
- [ ] Scaffold monorepo
- [ ] Alpha local
