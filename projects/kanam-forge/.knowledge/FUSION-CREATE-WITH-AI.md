# Kanam Forge — FUSIÓN con create-with-ai

**Estado:** Plan creado (2026-08-27)
**Decisión:** kanam-forge es el proyecto DESTINO de la fusión. create-with-ai se archiva (sin más cambios).

## Contexto

- **create-with-ai** (PRIVADO, `@gonzoblasco/create-with-ai` 0.0.2): CLI "Lovable propio". Creado 16/7, push 17/8. Código real: `ai/analyzer`, `scaffold`, `generator`, `iteration`. Nace de la MISMA idea que kanam-forge (NO padre-hijo).
- **kanam-forge** (fork de freestyle-sh/Adorable, MIT): app web conversacional iterativa (chat + preview + terminales, 13 tools de agente, Docker local + Ollama). Fase 1 casi completa (loop del agente validado).
- **Decisión (2026-08-20, backlog id 17):** NO borrar create-with-ai - evaluar FUSIÓN con kanam-forge.
- **Decisión (2026-08-27):** kanam-forge es el destino. create-with-ai se archiva, no tendrá más cambios.

## Qué aporta cada uno

| | kanam-forge (destino) | create-with-ai (a integrar) |
|---|---|---|
| **Interfaz** | Chat web iterativo + preview + terminales | CLI interactivo |
| **Motor** | 13 tools de agente (bash, fs, commit, checkApp) | `ai/analyzer` (descripción → stack/features/tablas/auth/billing) |
| **Generación** | `provision.ts` (scaffold Next.js básico) | `scaffold` (React+Vite+Supabase+shadcn+CI) + `migrations` |
| **Iteración** | Chat sobre el proyecto en el container | `iteration/` (lee contexto, aplica cambios) |
| **LLM** | Ollama local (deepseek-v4-flash) | BYOK (OpenAI/Anthropic/DeepSeek/custom) |

## Punto de integración clave

**`provision.ts` de kanam-forge** ya hace lo que hace el `scaffold` de create-with-ai: escribe un scaffold en el workspace del container. La fusión es **reemplazar el scaffold básico de `provision.ts` por el scaffold completo de create-with-ai**.

Hoy `provision.ts` genera un Next.js mínimo (package.json, app/layout, app/page, globals.css, next.config, tsconfig, postcss, .gitignore, next-env). El scaffold de create-with-ai genera un proyecto completo: React 19 + Vite + Supabase + shadcn/ui + TanStack Query + Biome + Vitest + CI + migraciones SQL.

## Plan de fusión

### Fase A — Integrar el scaffold de create-with-ai a kanam-forge

**Objetivo:** que kanam-forge genere proyectos completos (stack opinado) en vez del scaffold básico.

- [ ] Portar `ai/analyzer.ts` → `adorable/lib/analyzer.ts` (adaptar imports, quitar dependencia de @clack/prompts para el wizard manual - en kanam-forge el análisis lo dispara el chat, no un CLI)
- [ ] Portar `scaffold/index.ts` + `scaffold/migrations.ts` → `adorable/lib/scaffold/` (adaptar para escribir en el workspace del container, no en `process.cwd()`)
- [ ] Reemplazar el `FILES` de `provision.ts` por el scaffold completo de create-with-ai
- [ ] Integrar el analyzer al flujo del chat: cuando el usuario describe un proyecto nuevo, kanam-forge corre el analyzer para determinar stack/features/tablas/auth/billing ANTES de provisionar
- [ ] Adaptar el system-prompt para que el agente sepa que el proyecto ya viene con stack opinado (Supabase, shadcn, Biome, Vitest, CI)

**Resultado:** kanam-forge crea proyectos completos con stack opinado desde el chat.

### Fase B — CLI como interfaz de kanam-forge

**Objetivo:** exponer kanam-forge también por CLI (crear por chat O por CLI, mismo motor).

- [ ] Decidir: ¿el CLI de create-with-ai se convierte en un wrapper que llama a kanam-forge, o kanam-forge expone un binario CLI propio?
- [ ] Si es wrapper: `@gonzoblasco/create-with-ai` deprecado en npm, apunta a kanam-forge
- [ ] Si es binario propio: kanam-forge gana un `bin` que reusa el analyzer + scaffold

### Fase C — Iteración unificada

**Objetivo:** unificar el modo iteración de create-with-ai con el chat de kanam-forge.

- [ ] Portar `iteration/reader.ts` + `iteration/applier.ts` → kanam-forge
- [ ] El chat de kanam-forge ya itera sobre el proyecto en el container; el `reader` de create-with-ai puede alimentar el contexto inicial del agente (qué tiene el proyecto: auth, supabase, tests)

### Fase D — Cierre

- [ ] Archivar create-with-ai en GitHub (sin borrar - tiene 288 descargas npm)
- [ ] Deprecar `@gonzoblasco/create-with-ai` en npm (o dejar como wrapper)
- [ ] Actualizar MEMORY.md, TOOLS.md, OSS-TRACKER si aplica
- [ ] Actualizar BRIEF/STATUS/PLAN de kanam-forge

## Riesgos / consideraciones

- **Stack generado:** create-with-ai genera React+Vite+Supabase; kanam-forge hoy provisiona Next.js. Decidir si kanam-forge genera Next.js (consistente con el container que ya corre Next) o Vite (lo que genera create-with-ai). El container de kanam-forge ya corre `next dev` - generar Vite requeriría adaptar el dev server.
- **El analyzer usa @clack/prompts** (CLI interactivo). En kanam-forge el análisis lo dispara el chat, no un CLI - hay que adaptar el wizard manual a un flujo no-interactivo o dejarlo para el CLI.
- **BYOK vs Ollama:** kanam-forge usa Ollama local; create-with-ai usa BYOK. El analyzer debe poder usar Ollama como provider (ya soporta "custom" URL compatible con OpenAI).

## Estado del repo kanam-forge (2026-08-27)

- Repo: `github.com/gonzoblasco/kanam-forge` (público, main = `e72f10b` Fase 1)
- El workspace solo tiene `.knowledge/` + README (el código del fork NO está clonado en el workspace)
- Para trabajar la fusión: clonar el repo en `projects/kanam-forge/` (sin pisar `.knowledge/`)
- Branches en GitHub: main, local, v2, adorable-v2, mastra, mobile, durability, experimental-vms, copilot/add-mit-license, local-maverick
