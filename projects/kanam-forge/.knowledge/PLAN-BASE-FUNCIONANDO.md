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

### P1 - El agente usa path absoluto `/workspace/...` que falla - RESUELTO (cb5eea8)
- **Síntoma:** el agente intentó `readFileTool` con `/workspace/app/layout.tsx` → "Invalid file path" (ENOENT). Se auto-corrigió con path relativo `app/layout.tsx`.
- **Causa:** el `system-prompt.ts` decía que el workspace está en `${WORKDIR}` (`/workspace`), pero las tools esperan paths relativos.
- **Fix (cb5eea8):** lista de archivos con paths relativos + sección "File paths" que prohíbe paths absolutos. **Verificado:** el agente usa paths relativos sin ENOENT.
- **Bug 2 (puerto 3000) también resuelto en cb5eea8:** el agente ya no inventa `localhost:3000` como URL pública, dice "miralo en el preview de la interfaz". **Verificado** con prueba real.

### P2 - `.env.local` duplicado (root y `adorable/`) - RESUELTO (94f3d36)
- **Fix:** ubicación canónica = `adorable/.env.local` (donde corre Next.js). Eliminado el del root. `.env.example` actualizado (nota de ubicación, `/api` en OLLAMA_BASE_URL, advertencia sobre `~`).

### P3 - Warning de lockfiles del workspace - RESUELTO (turbopack.root)
- **Fix:** el `turbopack.root` configurado en `next.config.ts` eliminó el warning. Verificado: dev server arranca limpio sin warnings.

### P4 - 5 vulnerabilidades npm (2 low, 3 high) - RESUELTO (94f3d36)
- **Fix:** upgrade `next` 16.1.5 → 16.3.3 (fix de advisories high). Verificado: build + loop del agente OK. Quedan 3 vulnerabilidades low (de @ai-sdk, requieren breaking change - documentado como deuda).

### P5 - Dev server no es un servicio - RESUELTO (02614dd)
- **Fix:** README documenta los pasos exactos de arranque (Docker, .env.local en adorable/, npm run dev) + troubleshooting.

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

## Criterio de "base funcionando" - COMPLETADO (2026-08-27)

- [x] Crear un proyecto nuevo desde cero (POST /api/repos) sin errores
- [x] El agente responde a un pedido de cambio SIN fallar con path absoluto
- [x] El preview refleja el cambio
- [x] El workspace del proyecto tiene commit del cambio
- [x] README documenta el arranque
- [x] STATUS.md actualizado

## Notas

- El dev server quedó corriendo en localhost:3000 (para pruebas).
- Docker Desktop quedó corriendo (daemon activo).
- La imagen sandbox está construida.
- Los proyectos de prueba se limpiaron (containers + carpetas).
- **Deuda documentada:** 3 vulnerabilidades low de @ai-sdk (requieren breaking change, diferir a upgrade planificado del stack).
