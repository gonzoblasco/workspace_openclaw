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

1. Cierre del change `add-spec-review`: verificacion de punta a punta en el navegador (tarea 5.3) y `openspec archive`
2. Repo en GitHub (falta decision de visibilidad) y push del proyecto
3. Export a OpenSpec/ADR desde la app (que la spec generada entre al pipeline del proyecto destino)
4. Multi-proyecto en una sidebar con busqueda
5. Importar brief desde URL de issue/README
