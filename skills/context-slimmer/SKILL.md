---
name: "context-slimmer"
description: "Audita y reduce el token footprint de archivos de contexto del workspace"
---

# context-slimmer

## Descripción
Audita los archivos de contexto siempre cargados del workspace y reduce su token footprint. Mide el costo actual de tokens en archivos como AGENTS.md, MEMORY.md y SOUL.md, luego identifica qué mover a on-demand skills, eliminar completamente, o comprimir. Output con recomendaciones por archivo y proyección de ahorro.

## Cuándo usarlo
- Para reducir uso de tokens antes de llegar al límite del context window
- Para encontrar contenido duplicado entre MEMORY.md y AGENTS.md
- Para mover config específica de tareas fuera de archivos always-loaded a skills on-demand
- Para auditar el workspace después de meses de context drift acumulado
- Para establecer y enforce targets de tamaño para cada archivo de contexto

## Workflow
1. Ejecutar context-slimmer
2. Recibir reporte con token cost por archivo
3. Revisar recomendaciones (mover, eliminar, comprimir)
4. Aplicar cambios
5. Re-ejecutar para verificar ahorro

## Notas
- Sin dependencias externas
- Mide tokens reales, no estimaciones
- Agrupa recomendaciones por tipo de acción
