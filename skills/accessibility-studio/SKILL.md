---
name: "accessibility-studio"
metadata:
  category: "Product"
  tags:
    - accesibilidad
    - auditoria
    - wcag
description: "Workflow de Accessibility Studio: diseño, auditoría, autofix y validación de accesibilidad. Reemplaza a11y-system-designer, ux-a11y-studio."
user-invocable: false
---

# Workflow: Accessibility Studio

## Skills que reemplaza
- `a11y-system-designer`
- `ux-a11y-studio`

## Propósito
Diseño, auditoría, corrección y validación de accesibilidad en productos digitales. Incluye autofix loop (auditar → corregir → verificar) y checklist WCAG 2.2 granular.

## Cuándo usarlo
- Diseñar o auditar accesibilidad en un producto digital
- Corregir issues WCAG 2.2 (contraste, teclado, screen reader, ARIA)
- Validar accesibilidad pre-launch o post-cambios
- Generar reporte de cumplimiento con nivel de conformidad (A, AA, AAA)

## Fases

### 1. Discovery
Usuarios con discapacidades, necesidades, contexto de uso.

### 2. Audit — WCAG 2.2
Especificar nivel de conformidad objetivo (A, AA, AAA) al inicio.
- **Automated:** axe-core, Lighthouse, WAVE
- **Manual:** keyboard navigation, screen reader (VoiceOver), cognitive, visual

Checklist granular por principio:

**Perceivable**
- Contraste texto ≥ 4.5:1 (3:1 para texto grande) — 1.4.3
- Contraste componentes interactivos ≥ 3:1 — 1.4.11
- Alt text descriptivo en imágenes — 1.1.1
- Información no solo por color — 1.4.1

**Operable**
- Navegación por teclado completa — 2.1.1
- Focus visible en todos los elementos interactivos — 2.4.7
- Orden de tab lógico (izquierda→derecha, arriba→abajo) — 2.4.3
- Touch targets ≥ 24×24px (preferible 44×44px) — 2.5.8
- Sin keyboard traps en modales, dropdowns — 2.1.2

**Understandable**
- Labels visibles o aria-label en inputs — 3.3.2
- Mensajes de error claros asociados al campo — 3.3.1
- Idioma del documento definido — 3.1.1

**Robust**
- HTML semántico (main, nav, button, a) — 4.1.2
- ARIA solo cuando HTML nativo no alcanza — 4.1.2

### 3. Autofix (loop audit → edit → verify)
Dos modos:

**Report Mode:** auditar y generar reporte priorizado sin editar archivos.

**Fix Mode:** por cada issue identificado:
1. Corregir el código
2. Re-auditar para confirmar el fix
3. Pasar al siguiente issue

Priorizar por severidad: Critical → Major → Minor.

### 4. Design System
Tokens de contraste verificado, componentes accesibles con estados focus, hover, active, disabled.

### 5. Implementación
Componentes headless (WAI-APG), 3 capas de tests: unit (Vitest), integration (Testing Library), E2E (Playwright a11y).

### 6. Validación
Pre-launch, regresión post-cambios, reporte de cumplimiento. Si es posible, pruebas con usuarios reales con discapacidades. Si no, documentar las limitaciones.

## Outputs
- Reporte de audit WCAG 2.2 con nivel de conformidad y severidad por issue
- Issues corregidos (automática y manualmente) con verificación post-fix
- Design system con contraste verificado
- Componentes accesibles con tests
- Certificación de accesibilidad pre-launch

## Related Skills

- [Review & Quality](../review-quality): Para revisar accesibilidad pre-merge
- [Pre-Deploy QA](../pre-deploy-qa): Para validación pre-deploy con accesibilidad
