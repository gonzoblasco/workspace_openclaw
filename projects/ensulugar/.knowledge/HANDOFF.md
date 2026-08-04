# EnSuLugar — HANDOFF

## Fecha: 2026-08-04

## Estado del proyecto

EnSuLugar es un tutor de cocina adaptativo con IA (BYOK). Pasó de POC a MVP de producto en esta sesión.

## Lo que está hecho y funcionando

### Motor (Fase 1-2)
- Grafo de 28 técnicas con prerrequisitos (`src/engine/graph.ts`)
- Algoritmo de ruta adaptativa (`src/engine/path.ts`)
- Pipeline markdown → SQLite + JSON (`src/build/build.ts`)
- 41 recetas en 14 fichas markdown (`fichas/*.md`)
- Mapeo curado receta → técnica (`src/build/tecnicas-por-receta.ts`)
- CLI con `--perfil` funcionando (`src/cli.ts`)

### Backend (Fase 3)
- `src/server.ts` — Node puro, sin dependencias extra
- Endpoints: `GET /api/health`, `GET /api/recetas`, `POST /api/leccion`
- BYOK: lee `.env` para config de LLM (Ollama/OpenAI/Anthropic)
- CORS habilitado, Vite proxya `/api` a `localhost:3001` en dev

### Frontend (Fase 3 — MVP)
- Vite 6 + React 19 + TypeScript
- Onboarding: nombre, nivel objetivo, técnicas que ya dominás
- Persistencia en `localStorage` (`app/src/storage.ts`)
- Ruta adaptativa real (usa perfil guardado, no genérico)
- Marcar receta como completada → actualiza perfil → recalcula ruta
- Filtros: chips de técnica multi-selección + búsqueda normalizada
- Lecciones con IA: botón en cada receta, renderiza Markdown con estilos
- Grid de recetas (2 columnas desktop, 1 mobile)
- Reiniciar progreso desde header

### Contenido
- 23 recetas originales + 18 nuevas = 41 total
- Técnicas placeholder removidas (masa-madre, confit, sous-vide, merengue) — sin receta todavía

## Commits de esta sesión (subrepo ensulugar)

1. `fix(content): clean hojaldre mapping and remove placeholder techniques`
2. `chore: leave .knowledge tracking to workspace repo`
3. `feat(frontend): add Vite + React app with recipe catalog and learning paths`
4. `fix(frontend): interactive technique chips, numbered learning path, working filters`
5. `feat(backend): connect LLM lesson generation to frontend via local API`
6. `fix(frontend): render LLM lessons as styled markdown instead of plain text`
7. `feat(app): onboarding, local progress persistence, adaptive learning path`
8. `feat(ui): recipe grid layout (2 columns on desktop)`

## Cómo correrlo

```bash
cd projects/ensulugar
npm run build:content        # regenera DB/JSON
npm run dev:server           # terminal 1 — backend en :3001
npm run dev:app              # terminal 2 — frontend en :5173
```

Abrir http://localhost:5173/

Para preview estático (sin backend, sin lecciones IA):
```bash
npm run build:app && npm run preview:app   # :4173
```

## Lo que NO está hecho

- [ ] Técnicas avanzadas sin receta: masa-madre, confit, sous-vide, merengue
- [ ] PWA / service worker
- [ ] Deploy (frontend GitHub Pages/Vercel + backend Fly/Railway)
- [ ] Modo oscuro
- [ ] Diseño responsive fino (el grid básico está, pero falta pulir mobile)
- [ ] Onboarding más ligero (3 preguntas clave en lugar de checklist de 28 técnicas)
- [ ] Analytics mínimo
- [ ] Tests del frontend
- [ ] El workspace commit del último cambio (grid layout) puede no haber llegado al remoto — verificar

## Notas

- El modelo se trabó repetiendo texto al final de la sesión (GLM-5.2). Gonzo decidió cerrar.
- `app/public/ensulugar.json` es artefacto generado, no se commitea al subrepo.
- `.knowledge/` se ignora en el subrepo via `.git/info/exclude` y se trackea en el workspace.
- `happy-dom` se instaló para test de render (`app/test-render.ts`), se puede limpiar.
- El workspace commit del grid layout puede no haber pusheado. Verificar y pushear si falta.