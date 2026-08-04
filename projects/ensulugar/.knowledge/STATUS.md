# EnSuLugar — STATUS

## Estado actual (2026-08-04)

### Contenido

- **Recetas:** 41 (23 originales + 18 nuevas)
- **Técnicas en grafo:** 28, todas con al menos una receta vehículo
- **Fichas markdown:** 14 fichas categorizadas

### Nuevas técnicas agregadas

| Prioridad | Técnicas | Recetas |
|---|---|---|
| 1 | cuchillo, arroz, fritura, huevo-duro | 8 |
| 2 | risotto, braseado, encurtido, caramelo, crema-pastelera | 8 |
| 3 | hojaldre | 2 |

### Pipeline

- `npm run build:content` genera `dist/ensulugar.db`, `dist/ensulugar.json` y copia el JSON a `app/public/ensulugar.json` como fallback para el frontend.
- Motor de rutas verificado para perfiles principiante, intermedio y avanzado.
- No hay técnicas "fantasma" sin receta.

### MVP de producto (Fase 3+)

- Stack: Vite 6 + React 19 + TypeScript + backend Node puro.
- Ubicación: `app/`, backend `src/server.ts`, build output `dist-app/`.
- **Onboarding**: pantalla inicial que pregunta nombre, nivel objetivo y técnicas ya dominadas.
- **Persistencia local**: perfil y progreso en `localStorage` (`ensulugar:perfil`).
- **Ruta realmente adaptativa**: usa el perfil guardado (técnicas dominadas + nivel) para calcular qué falta aprender.
- **Progreso visible**: contador de técnicas dominadas y recetas completadas en el header.
- **Marcar receta como completada**: actualiza técnicas dominadas y recetas completadas; la ruta se recalcula.
- **Filtros**: chips de técnica multi-selección + búsqueda normalizada (título/categoría/técnica).
- **Lecciones con IA**: botón en cada receta, llama a `/api/leccion` con el perfil real, renderiza Markdown con estilos.
- **Reiniciar progreso**: disponible en el header.
- Comandos:
  - `npm run dev:app` — Vite (5173).
  - `npm run dev:server` — backend Node con HMR (3001).
  - `npm run build:app` / `npm run preview:app` — build/preview frontend.
  - `npm run start:server` — backend compilado.
- Validado: `npm run build:app` ✅, `npm run build` ✅, `npm run build:content` ✅, `npx tsc --noEmit` en `app/` ✅, endpoint `/api/leccion` con Ollama local ✅.

### CLI

- `npx tsx src/cli.ts --perfil principiante|intermedio|avanzado` ahora funciona correctamente.
- Sin `--perfil` muestra rutas para los tres perfiles.
- `npx tsx src/cli.ts --leccion` genera una lección para la siguiente técnica recomendada.

### Backend

- `src/server.ts` expone:
  - `GET /api/health` — estado y cantidad de recetas.
  - `GET /api/recetas` — todas las recetas.
  - `POST /api/leccion` — genera lección LLM para una receta y perfil.
- CORS habilitado; en desarrollo Vite proxya `/api` a `localhost:3001`.
- Usa la misma configuración BYOK de `.env` que la CLI.

### Siguiente

- Hacer el onboarding más ligero (quizás solo 3 preguntas clave).
- Agregar modo offline: que la app funcione sin backend usando el JSON estático (lecciones deshabilitadas).
- Agregar recetas para técnicas avanzadas pendientes: masa-madre, confit, sous-vide, merengue.
- PWA + service worker para instalar en móvil.
- Deploy: frontend en GitHub Pages/Vercel + backend en Fly/Railway.
- Analytics mínimo: qué lecciones se generan, qué recetas se completan.
