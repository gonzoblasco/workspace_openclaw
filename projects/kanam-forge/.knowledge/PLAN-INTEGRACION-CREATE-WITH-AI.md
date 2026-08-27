# Kanam Forge — Plan de integración del stack de create-with-ai

**Estado:** Plan de integración (2026-08-27)
**Disparador:** Gonzo señaló que el scaffold actual de kanam-forge no tiene testing, y que create-with-ai genera proyectos completos con stack opinado (Vitest, Biome, Supabase, CI) desde el vamos. Es el momento de la fusión.
**Decisión de stack (2026-08-27):** kanam-forge **mantiene Next.js** (App Router) como stack base del container. Se porta el **stack opinado** de create-with-ai (analyzer + testing + Supabase + shadcn + Biome + CI) adaptado a Next.js. NO se migra a Vite (el container ya corre `next dev`, y Next.js es el stack diario de Gonzo).

## Qué aporta create-with-ai (a portar)

- **`ai/analyzer.ts`**: descripción → análisis estructurado (projectType, stack, features, tables, authRequired, billingRequired, description). Usa zod para validar.
- **`scaffold/index.ts`**: genera proyecto completo (React+Vite+Supabase+shadcn+TanStack+Zod+Biome+Vitest+CI).
- **`scaffold/migrations.ts`**: genera migraciones SQL (users + tablas custom del análisis).
- **`iteration/reader.ts` + `applier.ts`**: lee contexto del proyecto y aplica cambios (alimentar el contexto inicial del agente).

## Qué se integra a kanam-forge

| Componente | Origen | Destino en kanam-forge | Adaptación |
|---|---|---|---|
| `ai/analyzer.ts` | create-with-ai | `lib/analyzer.ts` | Quitar `@clack/prompts` (wizard CLI). El análisis lo dispara el chat. Soporte Ollama como provider. |
| `scaffold/index.ts` | create-with-ai | `lib/scaffold/index.ts` | Adaptar de Vite → Next.js App Router. Escribir en el workspace del container. |
| `scaffold/migrations.ts` | create-with-ai | `lib/scaffold/migrations.ts` | Casi directo. |
| `provision.ts` (FILES) | kanam-forge (actual) | Reemplazar por el scaffold completo | El scaffold de create-with-ai reemplaza al scaffold básico de Next.js actual. |
| `iteration/reader.ts` | create-with-ai | `lib/iteration/reader.ts` | Alimentar el contexto inicial del agente (auth, supabase, tests presentes). |

## Stack objetivo del scaffold generado (Next.js + stack opinado)

- Next.js 16 (App Router) + React 19 + TypeScript
- Tailwind CSS 4 + shadcn/ui (lucide-react, cva, clsx, tailwind-merge)
- **Vitest + Testing Library** (testing desde el vamos)
- **Biome** (lint + format)
- Supabase client (@supabase/supabase-js + @supabase/ssr)
- TanStack Query + zod + react-hook-form
- Migraciones SQL (supabase/)
- GitHub Actions (CI con typecheck + test + lint)
- **Dev server del container:** `next dev` (sin cambios - el container ya lo corre)

## Fases de integración

### Fase A — Portar el analyzer + scaffold a kanam-forge
- [ ] Portar `ai/analyzer.ts` → `lib/analyzer.ts` (adaptar imports, quitar @clack/prompts, soportar Ollama)
- [ ] Portar `scaffold/index.ts` + `migrations.ts` → `lib/scaffold/` (adaptar de Vite a Next.js App Router)
- [ ] Reemplazar el `FILES` de `provision.ts` por el scaffold completo de create-with-ai (adaptado a Next.js)
- [ ] Configurar Vitest + Biome + shadcn en el scaffold generado

### Fase B — Integrar el analyzer al flujo del chat
- [ ] Cuando el usuario describe un proyecto nuevo, kanam-forge corre el analyzer ANTES de provisionar (para determinar stack/features/tablas/auth/billing)
- [ ] El scaffold se genera con la config del análisis (tablas SQL, auth, billing)
- [ ] Adaptar el system-prompt para que el agente sepa que el proyecto ya viene con stack opinado (Supabase, shadcn, Biome, Vitest, CI)

### Fase C — Portar la iteración (reader)
- [ ] Portar `iteration/reader.ts` → alimentar el contexto inicial del agente (qué tiene el proyecto: auth, supabase, tests)
- [ ] El agente arranca cada sesión sabiendo la estructura del proyecto

### Fase D — Proceso de desarrollo en el agente
- [ ] El system-prompt del agente (ya actualizado con plan + incremental + TDD) ahora tiene sentido porque el scaffold incluye Vitest
- [ ] Verificar el loop completo: pedir app → analyzer → scaffold con tests → agente implementa con TDD → tests pasan → commits

### Fase E — Cierre
- [ ] Archivar create-with-ai en GitHub (sin borrar)
- [ ] Deprecar `@gonzoblasco/create-with-ai` en npm
- [ ] Actualizar MEMORY.md, TOOLS.md, STATUS.md

## Riesgos / decisiones

- **Vite → Next.js:** el scaffold de create-with-ai usa Vite + react-router. Adaptarlo a Next.js App Router requiere reescribir la parte de routing/pages (App Router usa file-based routing, no react-router). El resto (Supabase, Query, Zod, Biome, Vitest, CI) es agnóstico.
- **El analyzer usa @clack/prompts** (CLI interactivo). En kanam-forge el análisis lo dispara el chat - adaptar a flujo no-interactivo.
- **BYOK vs Ollama:** el analyzer debe usar Ollama como provider (ya soporta "custom" URL compatible con OpenAI).
- **shadcn/ui:** requiere el CLI de shadcn o copiar los componentes. En el scaffold se pueden incluir los componentes base (button, input, card) ya generados.
