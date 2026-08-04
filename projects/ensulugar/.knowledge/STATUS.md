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

- `npm run build:content` genera `dist/ensulugar.db` y `dist/ensulugar.json` sin errores.
- Motor de rutas verificado para perfiles principiante e intermedio.
- No hay técnicas "fantasma" sin receta.

### Issues resueltos en este turno

1. Receta fantasma `"Errores Comunes del Hojaldre"` convertida a sección `###` dentro de la receta principal.
2. Técnicas placeholder (`masa-madre`, `confit`, `sous-vide`, `merengue`) removidas del grafo hasta tener recetas.
3. Descripción de `hojaldre` corregida.

### Siguiente

- Agregar recetas para técnicas avanzadas pendientes (masa-madre, confit, sous-vide, merengue) o avanzar a Fase 3 (frontend/app).
