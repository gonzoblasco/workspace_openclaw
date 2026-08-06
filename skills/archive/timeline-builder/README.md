# Timeline Builder

Generador de timelines HTML interactivos.

## ¿Para qué sirve?

Para **visualizar secuencias cronológicas** como páginas HTML interactivas. Tres layouts: vertical (clásico), horizontal (scrollable), dual-side (comparación). Sin dependencias externas, se abre en cualquier browser.

## ¿Cuándo usarlo?

- Project milestones
- Product release histories
- Company growth timelines
- Resumes
- Qualquier secuencia de eventos que quieras mostrar lindo

## ¿Cómo se usa?

### Preparar datos JSON

```json
{
  "title": "Project Milestones",
  "layout": "vertical",
  "theme": {
    "primaryColor": "#2563eb",
    "backgroundColor": "#ffffff"
  },
  "events": [
    {
      "date": "2024-01-15",
      "title": "Project Kickoff",
      "summary": "Core team assembled",
      "details": "Detailed description, shown on click",
      "icon": "🚀",
      "category": "Milestone",
      "color": "#10b981"
    }
  ]
}
```

### Generar HTML

```bash
python3 scripts/generate_timeline.py --config data.json --output timeline.html
```

### Layouts

| Layout | Cuándo usarlo |
|---|---|
| **vertical** | Muchos eventos, lectura top-to-bottom |
| **horizontal** | Pocos eventos, scroll horizontal |
| **dual-side** | Comparación lado a lado (izquierda/derecha) |

## Skills relacionadas

- [Technical Documentation](../tech-docs) — Para documentar roadmaps y releases
- [Product Discovery](../product-discovery) — Para visualizar milestones de producto
