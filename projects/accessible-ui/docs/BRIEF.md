# accessible-ui — Regeneración v1.0

## Producto

Librería headless de componentes de accesibilidad para React 19/TypeScript. Librería minimalista que expone primitives sin estilos; el consumidor proporciona los clases.

## Quién es el usuario

- Devs frontend modernos que buscan componentes headless ARIA-compliant
- Equipos que quieren control total de styling (Tailwind, CSS Modules, SCSS)
- Anyone que necesita compliance WAI-APG sin overhead

## ¿Qué hace

| Component | Desc | ARIA Pattern |
|-----------|------|---------------|
| **Combobox** | Editable input + list autocomplete | [Editable Combobox with List Autocomplete](https://www.w3.org/WAI/ARIA/apg/patterns/combobox/) |
| **Modal** | Focus-trapped dialog con focus trap y cierre ESC/A | [Dialog (Modal)](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/) |
| **Tabs** | Keyboard-navigable tabs (manual activation) | [Tabs](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/) |

## ¿Por qué ahora?

- **Deuda técnica eliminada**: 12 commits de decisiones no aplicadas en el código actual
- **Stack limpio**: React 19 + TypeScript + Vite + Vitest + Storybook 10 + Tailwind v4
- **Testing fresco**: Estrategia 3-layer desde cero sin deuda acumulada
- **Regeneración honesta**: Mejor que refactorizar para mejorar

## Metas v1.0

| Fase | Target | Desc |
|------|--------|------|
| F0 | Scaffold + ADRs base | Stack actualizado, docs framework |
| F1 | Components core | Combobox, Modal, Tabs con WAI-APG compliance |
| F2 | Testing layer | Vitest + jest-axe integration |
| F3 | Docs | BRIEF/EVALUATION/DEFINITION en workspace |
| F4 | CI/CD | GitHub Actions, npm publish ready (@gonzoblasco/) |

## Stack Técnico

```json
{
  "react": "19.x",
  "typescript": "^5.6",
  "vite": "^6.x",
  "vitest": "^2.x",
  "storybook": "^10.x",
  "@storybook/addon-a11y": "^10.x",
  "@storybook/addon-docs": "^10.x",
  "tailwindcss": "^4.x",
  "jest-axe": "^8.x"
}
```

## Roadmap Inicial

- **v1.0.0**: Core components + docs (Fase 0-3)
- **v1.1.0**: Auto-reflection (componentes que se autodocumentan de su codegen)
- **v2.0.0**: Ecosystem extensible (plugins para nuevos componentes WAI-APG)

## Success Metrics

- ✅ Zero axe violations en core components
- ✅ 100% keyboard navigation tested (user-event)
- ✅ npm publish ready (@gonzoblasco/accessible-ui)
- ✅ Docs 1:1 con source code
