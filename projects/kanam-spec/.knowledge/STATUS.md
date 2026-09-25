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
- **Verificacion en dos capas:** linter determinista (`src/lib/lint.ts`) que detecta secciones sin contenido, requisitos sin criterio y plantillas sin completar; revision cruzada con el modelo cableada a la UI (`ReviewPanel.tsx`), con streaming y marca de vigencia
- **Verificacion en el export:** el Markdown lleva una seccion con los hallazgos abiertos y la ultima revision
- **OpenSpec inicializado** (`openspec/`): el change `add-spec-review` es el primero, con proposal, specs, design y tasks
- **35 tests** en el runner nativo de Node, incluidos los de regresion de anclas del indice

## What's Blocked

- (nada)

## Next Up

1. Verificacion de punta a punta en el navegador (tarea 5.3 del change): recorrido completo brief, generar, hallazgos, revisar, exportar
2. `openspec archive add-spec-review` despues de esa prueba
3. Repo en GitHub (falta decision de visibilidad) y push del proyecto
4. Export a OpenSpec/ADR desde la app (que la spec generada entre al pipeline del proyecto destino)
5. Multi-proyecto en una sidebar con busqueda
6. Importar brief desde URL de issue/README
7. Lint (Biome) y CI: hoy no hay ninguno de los dos
8. Reimport del JSON exportado: el roundtrip esta roto (se descarga pero no se puede volver a cargar)
