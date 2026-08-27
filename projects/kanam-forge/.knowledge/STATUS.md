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
- [ ] Ajustar system prompt para paths relativos (el agente usa `workspace/` como prefijo → ENOENT)
- [ ] Supabase central compartido + integración de backend en apps generadas

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
- **Pendiente:** clonar el repo de kanam-forge en el workspace (hoy solo está `.knowledge/`) para trabajar la fusión.

---

**Último log:** 2026-08-27 — Plan de fusión con create-with-ai creado (FUSION-CREATE-WITH-AI.md). kanam-forge = destino, create-with-ai = archivar. Fase 1 del fork sigue casi completa (loop del agente validado con Ollama). Commits del fork: ecfb84b (F0), 4150854 (fase-1), e72f10b (fix stack).
