---
name: "sovereign-accessibility-auditor"
description: "Audita HTML/CSS contra WCAG 2.1: contraste, ARIA, teclado, screen readers"
---

# sovereign-accessibility-auditor

## Descripción
Audita HTML y CSS contra estándares WCAG 2.1: color contrast ratios, cobertura de ARIA labels, keyboard navigation paths, y screen reader compatibility. Provee findings accionables con code examples y explica trade-offs entre approaches de remediación.

## Cuándo usarlo
- Para verificar un form por ARIA labels faltantes antes de un launch
- Para verificar color contrast ratios contra thresholds WCAG AA o AAA
- Para revisar keyboard tab order en un navigation menu o modal dialog
- Para encontrar screen reader compatibility issues en contenido renderizado dinámicamente
- Para preparar un audit report antes de someter un sitio a certificación de accesibilidad

## Workflow
1. Pasar el HTML/CSS a auditar
2. sovereign-accessibility-auditor analiza contra WCAG 2.1
3. Recibir findings con code examples y sugerencias de fix
4. Aplicar correcciones
5. Re-auditar para verificar

## Notas
- Sin dependencias externas
- Cubre contraste, ARIA, teclado, screen readers en un solo pase
- Complementa a11y-fixer para auditoría de componentes estáticos
