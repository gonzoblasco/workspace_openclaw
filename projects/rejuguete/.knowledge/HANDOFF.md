# ReJuguete — HANDOFF

**Fecha:** 2026-07-22
**Sesión:** Inicial — Scaffolding y documentación

## Resumen

Arrancamos ReJuguete, una juguetería de segunda mano. Next.js 15 + Tailwind + datos mockeados en v1. Quedó el scaffold listo y toda la documentación base.

## Estado actual

- Next.js scaffold creado en `projects/rejuguete/`
- Dependencias instaladas (Radix UI, Lucide, CVA, clsx, tailwind-merge)
- `.knowledge/` completo: BRIEF, DEFINITION, 3 ADRs, STATUS
- **Cero código de componentes o páginas** — solo el boilerplate de create-next-app

## Lo que sigue

1. **Tipos** — `Juguete`, `Vendedor`, `Categoria` en `src/types/index.ts`
2. **Datos mock** — Array de juguetes seed en `src/lib/data.ts`
3. **Componentes base** — Button, Card, Badge, Input en `src/components/ui/`
4. **Layout** — Header con logo + nav, Footer
5. **Home** — Catálogo con grilla de JugueteCard
6. **Búsqueda y filtros** — SearchBar + Filtros (categoría, edad, precio)
7. **Detalle** — Página `/juguete/[id]`
8. **Publicar** — Formulario en `/publicar`
9. **Perfil vendedor** — Página `/vendedor/[id]`

## Decisiones tomadas

- Stack: Next.js 15 App Router + TypeScript + Tailwind
- Datos mockeados en v1 (sin DB)
- Diseño colorido pastel + acentos vibrantes
- Sin auth real en v1

## Pendientes de decisión

- Paleta de colores exacta (propuesta en ADR-003, ajustar)
- Nombre definitivo (ReJuguete confirmado)
- Si usar imágenes placeholder o reales en v1

## Notas

- El proyecto está en `projects/rejuguete/` (no en la raíz del workspace)
- La sesión se cortó antes de escribir código real
- Próxima sesión: arrancar por tipos y datos mock
