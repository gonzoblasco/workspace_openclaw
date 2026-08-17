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
- [ ] Eliminar identity-session.ts (auth local)
- [ ] **HITO:** loop completo funciona local (chat → codigo → dev server → preview → checkApp → commit)

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

**Último log:** 2026-08-17 — Inicio del proyecto. Decisiones A/A/único/Kanam Forge tomadas. Creando estructura.
