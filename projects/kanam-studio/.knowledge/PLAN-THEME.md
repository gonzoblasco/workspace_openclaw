# Toggle de tema light/dark (plan de implementación)

**T=10 (low)** | Pipeline: A escribe → Kanam revisa

## Objetivo

Toggle accesible para cambiar entre tema light y dark, con persistencia en localStorage y respeto a `prefers-color-scheme` como default.

## Arquitectura

```
src/lib/theme.tsx          - ThemeProvider (context + localStorage + prefers-color-scheme)
src/app/globals.css        - CSS variables para ambos temas (data-theme attr en <html>)
src/app/layout.tsx         - envolver con ThemeProvider + script inline anti-FOUC
src/components/ThemeToggle.tsx - botón toggle accesible (aria-pressed, icono sol/luna)
src/app/page.tsx           - toggle en el header del editor + home
```

### 1. CSS variables (globals.css)

```css
:root[data-theme='dark'] {
  --bg: #0f172a;            /* fondo app */
  --bg-elevated: #1e293b;   /* paneles, botones, inputs */
  --bg-hover: #334155;      /* hover */
  --border: #334155;        /* bordes */
  --border-strong: #475569; /* bordes inputs */
  --text: #e2e8f0;          /* texto principal */
  --text-muted: #94a3b8;    /* texto secundario */
  --accent: #fbbf24;        /* foco, selección */
  --error-bg: #7f1d1d; --error-text: #fecaca; --error-border: #ef4444;
  --warning-bg: #78350f; --warning-text: #fde68a; --warning-border: #f59e0b;
  --info-bg: #1e3a8a; --info-text: #bfdbfe; --info-border: #3b82f6;
  --node-start-bg: #14532d; --node-start-border: #22c55e;
  --node-passage-bg: #1e293b; --node-passage-border: #38bdf8;
  --node-ending-bg: #7f1d1d; --node-ending-border: #ef4444;
}

:root[data-theme='light'] {
  --bg: #f8fafc;
  --bg-elevated: #ffffff;
  --bg-hover: #f1f5f9;
  --border: #e2e8f0;
  --border-strong: #cbd5e1;
  --text: #0f172a;
  --text-muted: #64748b;
  --accent: #d97706;
  --error-bg: #fef2f2; --error-text: #b91c1c; --error-border: #ef4444;
  --warning-bg: #fffbeb; --warning-text: #b45309; --warning-border: #f59e0b;
  --info-bg: #eff6ff; --info-text: #1d4ed8; --info-border: #3b82f6;
  --node-start-bg: #dcfce7; --node-start-border: #16a34a;
  --node-passage-bg: #ffffff; --node-passage-border: #0ea5e9;
  --node-ending-bg: #fee2e2; --node-ending-border: #dc2626;
}
```

Default (sin attr): dark (comportamiento actual). `body { background: var(--bg); color: var(--text); }` y transición suave de colores.

### 2. ThemeProvider (src/lib/theme.tsx)

- Context: `{ theme: 'dark' | 'light', toggle: () => void }`.
- Estado inicial: `localStorage.getItem('kanam-theme')` → si no existe, `matchMedia('(prefers-color-scheme: light)')`.
- `useEffect`: setea `document.documentElement.dataset.theme` y persiste en localStorage.
- Script inline en layout (antes del render) para evitar FOUC: lee localStorage/matchMedia y setea el attr antes de hidratar.

### 3. ThemeToggle (src/components/ThemeToggle.tsx)

- Botón con `aria-pressed={theme === 'light'}`, `aria-label` dinámico ("Cambiar a tema claro"/"Cambiar a tema oscuro").
- Icono: sol (light) / luna (dark) - inline SVG, sin dependencias.
- Estilo: usa CSS variables (fondo elevado, borde, texto).

### 4. Integración

- `layout.tsx`: `<ThemeProvider>` envuelve todo + script anti-FOUC en `<head>`.
- `page.tsx`: toggle en el header del editor (junto a "← Volver") y en la home (arriba a la derecha).

### 5. Migración de colores

Reemplazar TODOS los hex hardcoded de los 9 archivos por `var(--...)`:
- page.tsx, StoryGraphEditor.tsx, StoryFlowNode.tsx, StoryPlayer.tsx, CanonPanel.tsx, VariablesPanel.tsx, NodeInspector.tsx, AICoAuthor.tsx, globals.css (React Flow dark styles → variables).

## Criterios de done

- [ ] Toggle en header del editor y home, con icono sol/luna y aria-pressed.
- [ ] Persistencia en localStorage + default prefers-color-scheme.
- [ ] Sin FOUC (script inline).
- [ ] Todos los colores hardcoded migrados a variables (grep de hex en src/ = solo globals.css).
- [ ] React Flow (controles, minimap, edges) usa variables.
- [ ] Tests: ThemeProvider (default, toggle, persistencia) + ThemeToggle (render, aria).
- [ ] Tests verdes, lint, typecheck, build OK.
- [ ] E2E: toggle cambia el attr data-theme y persiste al recargar.
