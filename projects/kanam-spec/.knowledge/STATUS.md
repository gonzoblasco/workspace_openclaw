# STATUS - kanam-spec

## Current Phase

Development (M0: app funcional con generacion por seccion, export y persistencia local)

## What's Working

- Scaffold Vite + React + TS, build productivo
- Catalogo de 14 secciones de spec con esqueleto y prompt propio
- Cliente Ollama con streaming (NDJSON) via proxy `/api`
- UI: brief, navegacion de secciones, generacion/regeneracion, edicion, cancelar
- Export a Markdown y JSON, copiado al portapapeles, descarga de archivo
- Persistencia local de proyectos en `localStorage`
- Servidor Node sin dependencias que sirve `dist/` y proxea a Ollama
- **Servicio permanente (LaunchAgent `dev.gonzoblasco.kanam-spec`):** auto-start al boot, `KeepAlive` incondicional, puerto 4173
- **Watchdog (LaunchAgent `dev.gonzoblasco.kanam-spec-watchdog`):** cada 60 s revive el servicio si se cayo y respeta el apagado deliberado via `config/.intentional-stop`
- `scripts/service.sh` (`start|stop|restart|status`) opera el servicio por launchctl, sin procesos sueltos

## What's Blocked

- (nada)

## Next Up

1. Deteccion de modelos con capacidad de `tools` para habilitar un modo "revisar spec" con agente
2. Export a OpenSpec (`openspec/` con change proposal) y a ADR
3. Multi-proyecto en una sidebar con busqueda
4. Tests: unitarios de `buildSectionPrompt` y de los exporters (Vitest)
5. Importar brief desde URL de issue/README
