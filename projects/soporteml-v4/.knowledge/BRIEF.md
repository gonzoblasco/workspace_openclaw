# SoporteML v4 - BRIEF

**Estado:** REINICIO (2026-08-17)
**Última actualización:** 2026-08-17

## Qué es

CRM multi-tenant para vendedores de Mercado Libre, con asistencia de IA. Centraliza consultas de compradores, las categoriza, sugiere respuestas con IA y permite publicarlas de vuelta a MeLi en un clic.

## Por qué V4 (decisión de Gonzo, 2026-08-17)

**v3 quedó como un template básico.** Dos problemas concretos:

1. **Features limitadas:** el schema modela un producto completo (KB con embeddings, autopilot, SLA, plantillas, clientes, métricas, auditoría) pero la UI solo expone 3 vistas genéricas (Inbox, Productos, Ajustes). El backend tiene features que el frontend ni toca.
2. **UI/UX sosa:** diseño de template shadcn estándar - cards con `border rounded-xl`, badges de colores planos, inputs genéricos, cero identidad visual, cero diseño avanzado con CSS. Nada de lo que aprendimos en Kanam Story (diseño accesible e impactante) ni Kanam Forge (pipeline de calidad).

**V4 = reinicio con estándar superior.** No es un reencuadre cosmético: es reconstruir el frontend con diseño avanzado y desbloquear las features que el schema ya soporta, usando la metodología que funcionó en Kanam Story (pipeline en cadena A/B, slices finos con release usable, `.knowledge/` vivo, a11y integrada).

## Qué se conserva de v3 (activo valioso)

- **Backend (apps/api):** OAuth MeLi real end-to-end (PKCE S256), sync service, token service con refresh automático, IA con Ollama, billing mock.
- **Capa de datos (packages/db):** schema SQLite de 20+ tablas (multi-tenant, KB, autopilot, SLA, plantillas, auditoría, blacklist, webhooks MP) + repositorios.
- **Token real de producción MeLi** (GONZOBLASCO / MLA) - el activo más difícil de conseguir.

## Qué se reconstruye (el corazón de V4)

- **Frontend completo (apps/web):** diseño avanzado con CSS custom, identidad visual propia, micro-interacciones, animaciones de marca, a11y WCAG 2.1 AA integrada desde el arranque. Nada de template shadcn genérico.
- **Features desbloqueadas:** KB (RAG), autopilot, SLA, plantillas, clientes, métricas - todo lo que el schema ya modela pero la UI no expone.

## Stack

- Monorepo Turborepo + pnpm (heredado de v3)
- Frontend: React + TypeScript + Vite + Tailwind + shadcn/ui (base) + Radix + Framer Motion + CSS avanzado custom
- Backend: Node + Hono (heredado de v3)
- DB alpha: SQLite con capa de repositorios (heredado de v3)
- IA: Ollama local (deepseek-v4-flash:cloud)

## Metodología (de Kanam Story/Forge, adaptada - no fuente única de verdad)

- **Pipeline en cadena A/B:** agente A desarrolla unidades impares, B pares; cada uno revisa la unidad del otro (incluida a11y) antes de seguir.
- **Slices finos:** cada slice termina en release usable. No bloques monolíticos.
- **`.knowledge/` vivo:** BRIEF, ROADMAP, STATUS, PLAN, ADRs, LEARNINGS - se actualizan con cada hito.
- **a11y integrada:** WCAG 2.1 AA desde el arranque, no al final. Validación AT manual con VoiceOver/NVDA.
- **Diseño avanzado:** CSS custom para crear diseños únicos e impactantes, no templates.

## Referencias

- v3: `projects/soporteml-v3/` (repo `gonzoblasco/soporteml-v3`)
- v1: `projects/soporteml/` (design system de referencia)
- PRODUCT.md de v3: `projects/soporteml-v3/.knowledge/PRODUCT.md`
- BACKEND-REFERENCE.md de v3: `projects/soporteml-v3/.knowledge/BACKEND-REFERENCE.md`
