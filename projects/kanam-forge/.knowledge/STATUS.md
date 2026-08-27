# Kanam Forge — STATUS

## Fase 0 — Fundamentos

- [x] Crear estructura del proyecto con .knowledge/ (BRIEF, STATUS)
- [x] Fork de Adorable + git init + remote (gonzoblasco/kanam-forge, upstream freestyle-sh/Adorable)
- [x] npm install + build baseline (fix TS en attachment.tsx)
- [x] Revisar env: .env.example creado, ApiKeyGate de la UI para keys de usuario
- [x] Commit + push inicial (ecfb84b)

**Nota Fase 0:** el build del upstream fallaba con error TS en `attachment.tsx` (`_exhaustiveCheck: never` vs tipo amplio de assistant-ui). Fix: cast `as never`. Build OK, 881 paquetes, 22 vulnerabilidades del upstream (revisar luego).

## Fase 1 — Desacoplar Freestyle → Docker local

- [ ] docker-vm.ts (interfaz exec/fs via Docker)
- [ ] Dockerfile base (Node + Next.js + git + ttyd)
- [ ] Reemplazar adorable-vm.ts → container local
- [ ] Reemplazar repo-storage.ts → git local en volumen
- [ ] Reemplazar chat/route.ts → ref a container local
- [x] Eliminar identity-session.ts (auth local, stub sin Freestyle)
- [x] Stub deployment-status.ts + promote (sin serverless en MVP)
- [x] provision.ts (scaffold Next.js + npm install + dev server en container)
- [x] LLM provider Ollama local (LLM_PROVIDER=ollama, modelo deepseek-v4-flash:cloud)
- [x] **HITO PARCIAL:** crear proyecto → provisionar → npm install → dev server → preview HTTP 200 (puerto dinámico)
- [x] **HITO: loop completo del AGENTE validado** (chat → Ollama deepseek-v4-flash → tools → exec en container)
- [x] Ajustar system prompt para paths relativos (el agente usa `workspace/` como prefijo → ENOENT) - FIX cb5eea8
- [ ] Supabase central compartido + integración de backend en apps generadas
- [x] **BUG:** el agente informa el puerto 3000 en lugar de la `previewUrl` al finalizar la creación - FIX cb5eea8

**Stack alineado (2026-08-17):** el stack de Adorable estaba atado a AI SDK 6 con `ollama-ai-provider` v1 (spec v1, incompatible). Fix: `ollama-ai-provider-v2@3.6.0` (spec v2, compatible con ai@6) + pin `@assistant-ui/react@0.12.12` con overrides de `store@0.2.1`/`core@0.1.1`/`tap@0.5.1` (evita `tapAssistantClientRef` roto). Ollama baseURL necesita sufijo `/api`. ApiKeyGate salta con Ollama (no requiere key). Commit `e72f10b`.

**Bloqueante de recursos (2026-08-17):** ~~la MacBook Air M2 (8GB) no puede correr el stack de Supabase de sportcars~~ **RESUELTO** - sportcars borrado (local + repo). El loop del agente ya se validó con deepseek-v4-flash.

## Fase 2 — Pipeline Gonzo

- [ ] Sistema prompt con stack opinado (Biome, pre-commit, ADRs, a11y)
- [ ] Template create-stack-next + hooks
- [ ] Memoria de proyecto persistente (.knowledge/)

## Fase 3 — Multi-agente

- [ ] Agente A escribe → Agente B revisa (cross-review a11y + calidad)

## Fase 4 — Cloud (sueño)

- [ ] Servidor propio de VMs Docker + dominio
- [ ] Publish multi-tenant
- [ ] Producto

## FUSIÓN con create-with-ai (2026-08-27)

- **Decisión:** kanam-forge es el proyecto DESTINO de la fusión. create-with-ai se archiva (sin más cambios).
- **Plan completo:** `FUSION-CREATE-WITH-AI.md`
- **Punto de integración clave:** reemplazar el scaffold básico de `provision.ts` por el scaffold completo de create-with-ai (React+Vite+Supabase+shadcn+CI+migraciones) + integrar el `ai/analyzer` al flujo del chat.

## BASE FUNCIONANDO (2026-08-27) - COMPLETA ✅

- **Build:** compila (TypeScript OK, todas las rutas).
- **Dev server:** corre en localhost:3000.
- **Docker:** daemon + imagen sandbox construida (`kanam-forge/sandbox:latest`).
- **Creación de proyecto:** POST /api/repos → container + workspace provisionado + preview.
- **Loop del agente:** chat → Ollama (deepseek-v4-flash) → tools (readFile, replaceInFile, checkApp) → exec en container → verificación. Probado: cambió el título de la app y el preview lo reflejó.
- **Bugs arreglados:**
  - `ce390dd`: turbopack.root (Next.js no leía .env.local) + KANAM_FORGE_DATA_DIR con `~` sin expandir.
  - `cb5eea8`: system-prompt - paths relativos (sin ENOENT) + no inventar puerto 3000.
  - `94f3d36`: upgrade next 16.1.5 → 16.3.3 (fix vulns high) + .env.example corregido.
  - `02614dd`: README con setup + troubleshooting.
- **Deuda documentada:** 3 vulnerabilidades low de @ai-sdk (requieren breaking change, diferir).
- **Plan:** `PLAN-BASE-FUNCIONANDO.md` (completo).

## ESTRUCTURA APLANADA (2026-08-27) - commit 656292d

- **Cambio:** se eliminó la subcarpeta `adorable/` (residuo del monorepo de Adorable). Todo el código ahora vive en el root del proyecto: `app/`, `components/`, `lib/`, `docker/`, `hooks/`, `next.config.ts`, `tsconfig.json`, etc.
- **package.json:** fusionado (deps + overrides + allowScripts), sin workspaces. Nombre: `kanam-forge`.
- **.env.local:** movido al root (ya no hay problema de ubicación).
- **next.config.ts:** removido el `turbopack.root` (ya no hace falta con estructura plana).
- **Verificado:** build + loop del agente funcionan con la estructura plana.
- **Nota:** queda un warning de Next.js sobre el lockfile del workspace (fuera del repo) - inofensivo, Next.js lo ignora correctamente.

## BRANDING (2026-08-27) - commit 8c280d3

- **Título:** Adorable → Kanam Forge (layout, sidebars, api-key-gate).
- **Logo:** nuevo `KanamLogo` (hoja estilizada, evolución del emoji 🌿, no el emoji directo). Reemplaza el perrito de Adorable en los 2 sidebars.
- **Favicon:** `icon.svg` + `icon.png` + `apple-icon.png` (marca de hoja).
- **Light mode:** removida la clase `dark` del `<html>` (usa las variables light de `:root`).
- **System prompt:** el agente se presenta como "Kanam Forge".
- **Tools:** "Adorable VM" → "sandbox" en descripciones.

## UI AJUSTES (2026-08-27) - commit 09520d5

- **Settings:** removido el botón de API key settings (Ollama local no necesita key).
- **Terminal:** colapsado por default (solo barra con toggle), expandir/colapsar con ChevronUp.
- **Divisor:** arrastrable entre chat y viewport (resizer, 25%-70% del ancho del chat).
- **Paleta:** bajada la saturación del fondo (oklch 0.97 0.008 20) y sidebar (0.99 0.004 20).

---

**Último log:** 2026-08-27 — Base completa y verificada. Fase 1 del fork operativa (loop del agente validado). Estructura aplanada (sin adorable/). Branding a Kanam Forge (hoja + light mode). UI: settings removido, terminal colapsable, divisor resizable, paleta suavizada. Commits: ecfb84b (F0), 4150854 (fase-1), e72f10b (fix stack), ce390dd (fix turbopack root), cb5eea8 (fix system-prompt), 94f3d36 (upgrade next), 02614dd (docs), 656292d (flatten), 8c280d3 (branding), 94a1fb4 (palette), 09520d5 (ui).
