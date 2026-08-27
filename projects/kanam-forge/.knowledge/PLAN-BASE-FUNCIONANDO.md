# Kanam Forge — Plan de acción: dejar la base funcionando

**Estado:** 2026-08-27. Base verificada funcionando (build + dev server + loop del agente).
**Objetivo:** dejar kanam-forge operativo como base sólida ANTES de la fusión con create-with-ai.

## Estado verificado (hoy)

**✅ Funciona:**
- Build compila (TypeScript OK, todas las rutas generadas)
- Dev server corre en localhost:3000
- Docker daemon + imagen sandbox construida (`kanam-forge/sandbox:latest`)
- Creación de proyecto (POST /api/repos): container + workspace provisionado + preview
- **Loop completo del agente**: chat → Ollama (deepseek-v4-flash) → tools (readFile, replaceInFile, checkApp) → exec en container → verificación. Probado: cambió el título de la app y el preview lo reflejó.

**🐛 Bugs arreglados hoy (commits `ce390dd`):**
1. `turbopack.root` no configurado → Next.js usaba el root del workspace, no leía `.env.local`. Fix: `turbopack.root: join(__dirname, "..")` en `next.config.ts`.
2. `KANAM_FORGE_DATA_DIR=~/.kanam-forge/projects` en `.env.local` → el `~` no se expande en Node, `existsSync` fallaba. Fix: quitar la línea (usa el default `join(homedir(), ...)`).

## Pendientes / deuda detectada

### P1 - El agente usa path absoluto `/workspace/...` que falla
- **Síntoma:** el agente intentó `readFileTool` con `/workspace/app/layout.tsx` → "Invalid file path" (ENOENT). Se auto-corrigió con path relativo `app/layout.tsx`.
- **Causa:** el `system-prompt.ts` dice que el workspace está en `${WORKDIR}` (`/workspace`), pero las tools esperan paths relativos.
- **Fix:** ajustar el system-prompt para que el agente use paths relativos (sin prefijo `/workspace`). Es el pendiente que ya estaba anotado en STATUS.md ("Ajustar system prompt para paths relativos").

### P2 - `.env.local` duplicado (root y `adorable/`)
- **Síntoma:** el `.env.local` está en `projects/kanam-forge/` y también en `adorable/` (lo copié para que Next.js lo lea).
- **Causa:** Next.js con workspaces busca los env files en el directorio del proceso (`adorable/`), no en el root del proyecto.
- **Fix:** decidir dónde vive. Opción A: solo en `adorable/` (donde corre Next). Opción B: configurar el root para que lea del root del proyecto. El `.env.local` está gitignored, así que no afecta el repo.

### P3 - Warning de lockfiles del workspace
- **Síntoma:** Next.js detecta el `package-lock.json` del workspace y se confunde.
- **Causa:** el workspace tiene su propio lockfile.
- **Fix:** mitigado con `turbopack.root`, pero el warning puede volver. Evaluar si hace falta más config.

### P4 - 5 vulnerabilidades npm (2 low, 3 high)
- **Síntoma:** `npm audit` reporta 5 vulnerabilidades.
- **Causa:** del upstream (Adorable).
- **Fix:** evaluar `npm audit fix` (con cuidado, puede romper el stack pinneado de assistant-ui).

### P5 - Dev server no es un servicio
- **Síntoma:** hay que levantar `npm run dev` manualmente cada vez.
- **Fix:** opcional - crear un script de arranque o documentar el comando.

## Plan de ejecución (pipeline A/B)

### Fase 1 - Arreglar el system-prompt (P1) - PRIORIDAD
- [ ] **Agente A (HIGH):** ajustar `system-prompt.ts` para que el agente use paths relativos (sin prefijo `/workspace`). Aclarar que el workspace ya está provisionado con Next.js y que las tools esperan paths relativos.
- [ ] **Agente B (HIGH):** cross-review del cambio.
- [ ] **Kanam (MAX):** revisión final + verificación con un chat de prueba (crear proyecto, pedir un cambio, verificar que no falle con path absoluto).

### Fase 2 - Resolver `.env.local` (P2)
- [ ] Decidir la ubicación canónica del `.env.local`.
- [ ] Documentar en README cómo configurarlo.

### Fase 3 - Vulnerabilidades (P4) - OPCIONAL
- [ ] Evaluar `npm audit fix` en un branch aparte (no romper el stack pinneado).
- [ ] Si rompe, documentar y dejar para después.

### Fase 4 - Documentar el arranque (P5)
- [ ] Actualizar README con los pasos exactos: Docker up, npm install, .env.local, npm run dev.
- [ ] Actualizar STATUS.md de kanam-forge con el estado real.

## Criterio de "base funcionando"

- [ ] Crear un proyecto nuevo desde cero (POST /api/repos) sin errores
- [ ] El agente responde a un pedido de cambio SIN fallar con path absoluto
- [ ] El preview refleja el cambio
- [ ] El workspace del proyecto tiene commit del cambio
- [ ] README documenta el arranque
- [ ] STATUS.md actualizado

## Notas

- El dev server quedó corriendo en localhost:3000 (para pruebas).
- Docker Desktop quedó corriendo (daemon activo).
- La imagen sandbox está construida.
- El proyecto de prueba se limpió (container + carpeta).
