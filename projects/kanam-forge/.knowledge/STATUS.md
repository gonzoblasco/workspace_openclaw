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
- [x] LLM provider Ollama local (LLM_PROVIDER=ollama, modelo kimi-k2.7-code:cloud)
- [x] **HITO PARCIAL:** crear proyecto → provisionar → npm install → dev server → preview HTTP 200 (puerto dinámico)
- [ ] Validar loop completo del AGENTE (chat → código → preview) con Ollama - **BLOQUEADO por RAM**
- [ ] Supabase central compartido + integración de backend en apps generadas

**Bloqueante de recursos (2026-08-17):** la MacBook Air M2 (8GB) no puede correr el stack de Supabase de sportcars (~1.8GB, 11 containers) + Docker + gateway + VSCode + dev server Kanam Forge + sandbox npm install a la vez. macOS mata procesos (SIGKILL). El build completo de Turbopack y el typecheck OOM. El runtime de dev funciona cuando hay memoria. **Decisión necesaria de Gonzo:** pausar/detener el stack de sportcars mientras se trabaja en Kanam Forge, o usar otra máquina.

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

---

**Último log:** 2026-08-17 — Fase 1 en progreso. Desacople Freestyle → Docker local implementado y verificado en runtime (crear proyecto → preview HTTP 200). LLM Ollama local configurado. **Bloqueado por RAM:** el stack de Supabase de sportcars (1.8GB) impide build/typecheck y el loop completo del agente. Commits proyecto: ecfb84b (F0), fase-1 commit posterior. Falta: validar chat con Ollama y Supabase central.
