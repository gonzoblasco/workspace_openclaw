# SoporteML v3 - BRIEF

## Estado: EN ARRANQUE (2026-08-07)

## Qué es

CRM multi-tenant para vendedores de Mercado Libre, con asistencia de IA. Gestiona consultas, productos, stock, envíos, garantías y métricas.

## Contexto de versiones

- **v1** (`soporteml`): la versión de referencia. Design system estable, documentado en `.knowledge/`.
- **v2** (`soporteml-v2`): **EXPERIMENTO - NO USAR DE REFERENCIA.** Se descarta.
- **v3** (`soporteml-v3`): repo nuevo, en arranque. Se construye sobre v1.

## Objetivo de v3

Reconstruir SoporteML sobre la base sólida de v1, con el design system aclarado desde el arranque (skill de UI + guía de estilos), para que esta versión quede bien.

## Documentos de referencia

- `UI-DESIGN-SKILL.md` - estándar de implementación UI (tokens, espaciado, a11y, anti-patrones, workflow de revisión).
- `DESIGN-GUIDE.md` - identidad visual de SoporteML (paleta, tipografía, utilidades, componentes, layout) documentada desde v1.

## Stack

- React + TypeScript + Vite
- Tailwind CSS + shadcn/ui + Radix UI
- Lucide Icons + Framer Motion
- Supabase (backend + Edge Functions)
- next-themes (claro/oscuro)

## Pendiente

- [ ] Definir estructura del repo v3 (scaffold).
- [ ] Pedir a Lovable la guía de diseño oficial (prompt pendiente).
- [ ] Cruzar la guía de Lovable contra `DESIGN-GUIDE.md` y ajustar tokens si hace falta.
- [ ] Arrancar implementación.
