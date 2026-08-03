---
name: "timeline-builder"
metadata:
  category: "Tool"
  tags:
    - timeline
    - visualizacion
    - html
    - interactivo
description: "Generar timelines HTML interactivos desde datos JSON: layouts vertical, horizontal o dual-side, con colapsables y colores personalizados."
user-invocable: false
---

# Workflow: Timeline Builder

## Propósito

Generar páginas HTML interactivas de timelines desde datos JSON. Tres layouts: vertical, horizontal, dual-side. Sin dependencias externas.

## Cuándo usarlo

- Project milestones
- Product release histories
- Company growth timelines
- Personal resume timelines
- Course syllabus outlines

## Uso

```bash
python3 scripts/generate_timeline.py --config data.json --output timeline.html
```

## Outputs

- Archivo HTML auto-contenido
- Timeline interactivo con expand/collapse
- Diseño responsive
- Temas de color personalizables

## Helper Scripts

Scripts en `skills/timeline-builder/scripts/`:

| Script | Uso |
|---|---|
| `generate_timeline.py --config data.json --output timeline.html` | Genera un timeline HTML interactivo desde un JSON de configuración. Usar en cualquier fase de visualización. |

## Related Skills

- [Technical Documentation](../tech-docs): Para documentar roadmaps y releases
- [Product Discovery](../product-discovery): Para visualizar milestones de producto
