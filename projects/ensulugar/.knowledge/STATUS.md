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

- `npm run build:content` genera `dist/ensulugar.db`, `dist/ensulugar.json` y copia el JSON a `app/public/ensulugar.json` para el frontend.
- Motor de rutas verificado para perfiles principiante, intermedio y avanzado.
- No hay técnicas "fantasma" sin receta.

### Fase 3 — Frontend (MVP)

- Stack: Vite 6 + React 19 + TypeScript.
- Ubicación: `app/`, build output `dist-app/`.
- Funcionalidad:
  - Carga recetas desde `/ensulugar.json`.
  - Selector de perfil (principiante/intermedio/avanzado) arma la ruta de aprendizaje con el motor real (`src/engine/path.ts`).
  - **Filtro por chips de técnica** — permite seleccionar múltiples técnicas (OR).
  - Búsqueda por título, categoría o técnica, con normalización de acentos.
  - **Ruta de aprendizaje numerada** con nombres legibles; click en un paso filtra recetas de esa técnica.
  - Tarjetas de receta expandibles con ingredientes y pasos (incluye notas pedagógicas).
  - Tags de técnicas clickeables; sin tag de categoría duplicado.
- Comandos:
  - `npm run dev:app` — servidor de desarrollo Vite (puerto 5173).
  - `npm run build:app` — build de producción.
  - `npm run preview:app` — preview en puerto 4173.
- Validado: `npm run build:app` ✅, `npm run build` ✅, `npm run build:content` ✅, `npx tsc --noEmit` en `app/` ✅.

### CLI

- `npx tsx src/cli.ts --perfil principiante|intermedio|avanzado` ahora funciona correctamente.
- Sin `--perfil` muestra rutas para los tres perfiles.

### Issues resueltos en este turno

1. Frontend: reemplazado select único de técnica por chips multi-selección.
2. Frontend: corregida ruta de aprendizaje — ahora numerada, con nombres legibles e interactiva.
3. Frontend: eliminada tag de categoría duplicada; las técnicas se muestran como tags clickeables.
4. Frontend: búsqueda normalizada (ignora tildes) y busca también en técnicas.
5. Frontend: corregidos tipos `Dificultad` y `PerfilUsuario` en `App.tsx`.
6. CLI: `src/cli.ts` ahora respeta `--perfil` en lugar de ignorarlo.

### Siguiente

- Conectar generación de lecciones al frontend (requiere endpoint backend o integración con LLM).
- Agregar recetas para técnicas avanzadas pendientes: masa-madre, confit, sous-vide, merengue.
- Mejorar UX: progreso del usuario, recetas completadas, favoritos.
- PWA + deploy (GitHub Pages / Vercel).
