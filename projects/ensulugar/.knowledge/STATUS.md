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
  - Filtro por técnica y búsqueda por título/categoría.
  - Tarjetas de receta expandibles con ingredientes y pasos (incluye notas pedagógicas).
- Comandos:
  - `npm run dev:app` — servidor de desarrollo Vite (puerto 5173).
  - `npm run build:app` — build de producción.
  - `npm run preview:app` — preview en puerto 4173.
- Validado: `npm run build:app` ✅, `npm run build` ✅, `npm run build:content` ✅.

### Issues resueltos en este turno

1. Receta fantasma `"Errores Comunes del Hojaldre"` convertida a sección `###` dentro de la receta principal.
2. Técnicas placeholder (`masa-madre`, `confit`, `sous-vide`, `merengue`) removidas del grafo hasta tener recetas.
3. Descripción de `hojaldre` corregida.
4. Dependencias de React movidas a `dependencies` y scripts de Vite agregados.
5. `vite.config.ts` configurado con alias `@shared` para reusar el motor desde el frontend.

### Siguiente

- Conectar generación de lecciones al frontend (requiere endpoint backend o integración con LLM).
- Agregar recetas para técnicas avanzadas pendientes: masa-madre, confit, sous-vide, merengue.
- Mejorar UX: navegación por técnica, favoritos, progreso del usuario.
- PWA + deploy (GitHub Pages / Vercel).
