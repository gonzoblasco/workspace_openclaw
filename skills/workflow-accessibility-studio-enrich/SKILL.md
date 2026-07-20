---
name: "workflow-accessibility-studio-enrich"
description: "Enriquecer workflow-accessibility-studio con autofix loop, checklist WCAG detallado y formato de reporte."
---

# Propuesta: Enriquecer workflow-accessibility-studio

## Problema

`workflow-accessibility-studio` cubre discovery, audit, design system, implementación y validación, pero:
- No tiene un paso estructurado de autofix con verificación
- El checklist WCAG es genérico, sin criterios específicos por severidad
- No tiene un formato de reporte definido

## Inspiración

Del AI Developer Stack (gonzoblasco/ai-developer-stack):
- `accesslint-audit` — loop audit→edit→verify con dos modos (report y fix)
- `wcag-audit-patterns` — checklist WCAG 2.2 con criterios específicos y remediación

## Propuesta de Cambios

### 1. Nueva Fase: Autofix (opcional, post-audit)

Agregar entre Audit y Design System:

1. **Report Mode** — auditar y generar reporte priorizado sin editar
2. **Fix Mode** — loop audit→edit→verify por cada issue
3. **Verificación** — re-auditar después de fixes

### 2. Checklist WCAG 2.2 Detallado

Reemplazar el checklist genérico por uno estructurado:

- **Perceivable:** contraste (4.5:1 / 3:1), alt text, uso de color
- **Operable:** keyboard, focus visible, touch targets (24x24 / 44x44)
- **Understandable:** labels, errores, lenguaje
- **Robust:** HTML semántico, ARIA correcto

### 3. Formato de Reporte

```markdown
# Auditoría de accesibilidad — <scope>
## Summary
- N critical, M serious, K moderate
## Issues
- **Pattern**: <desc>
- **WCAG**: <ID> — <name>
- **Severity**: Critical | Major | Minor
- **Fix**: <código de remediación>
```

## Próximos pasos

1. Aprobar propuesta
2. Actualizar SKILL.md de workflow-accessibility-studio
3. Probar en un proyecto real
