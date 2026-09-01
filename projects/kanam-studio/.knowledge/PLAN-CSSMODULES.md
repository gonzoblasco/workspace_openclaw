# Migración de estilos inline a CSS Modules (plan)

**T=9 (low)** | Pipeline: A escribe → Kanam revisa

## Objetivo

Eliminar los 105 `style={{}}` inline de 9 componentes y migrarlos a **CSS Modules** (`.module.css` con clases scoped). Refactor mecánico: **cero cambio visual**, cero cambio de comportamiento.

## Por qué CSS Modules (no Tailwind, no styled-components)

- Stack actual: Next.js + Biome, sin Tailwind. CSS Modules es nativo de Next (cero deps).
- Scoped por componente (los nombres se hashean), tipado con `styles.clase`.
- Las CSS variables del tema (`var(--bg)`, `var(--text)`, etc.) se usan igual desde CSS.
- Los estilos dinámicos (condicionales: `selected`, `disabled`, `aria-pressed`) se resuelven con clases condicionales + `:global` o atributos, no con objetos.

## Archivos a migrar (9)

| Archivo | Inline | Notas |
|---|---|---|
| `src/app/page.tsx` | 20 | Home + header del editor |
| `src/components/StoryPlayer.tsx` | 20 | Modo jugar |
| `src/components/AICoAuthor.tsx` | 18 | Panel IA |
| `src/components/VariablesPanel.tsx` | 18 | Panel variables |
| `src/components/CanonPanel.tsx` | 12 | Panel canon |
| `src/components/NodeInspector.tsx` | 7 | Inspector nodo |
| `src/components/StoryGraphEditor.tsx` | 7 | Toolbar + hint + layout |
| `src/components/StoryFlowNode.tsx` | 2 | Nodo custom React Flow |
| `src/components/ThemeToggle.tsx` | 1 | Botón toggle |

## Reglas del refactor

1. **Un `.module.css` por componente** (`AICoAuthor.module.css`, etc.).
2. **Clases semánticas** (`.header`, `.message`, `.input`, `.actions`), no genéricas.
3. **Estilos dinámicos** → clases condicionales:
   - `selected` → `styles.selected` (definida en el CSS).
   - `disabled` → `:disabled` en CSS (no inline).
   - `aria-pressed` → `[aria-pressed='true']` en CSS.
4. **CSS variables del tema** se usan tal cual (`background: var(--bg-elevated)`).
5. **NO tocar** `globals.css` (variables del tema + React Flow dark) ni `layout.tsx`.
6. **NO cambiar** ningún valor visual: mismo color, mismo spacing, mismo border-radius. Es refactor mecánico.
7. **React Flow** (`StoryFlowNode`): los nodos custom necesitan clases globales para que React Flow las aplique - usar `:global` en el module o clases normales en globals.css. Verificar que el nodo siga renderizando igual.

## Criterios de done

- [x] Cero `style={{}}` en los 9 componentes (grep = 0).
- [x] Tests unit verdes (67) + E2E verdes (8).
- [x] Lint + typecheck + build OK.
- [x] Screenshot comparativo antes/después (editor con nodos + panel IA) - sin cambio visual.
- [x] El tema light/dark sigue funcionando (CSS variables intactas).

## Resultado (2026-09-01)

- 9 `.module.css` creados (uno por componente), 105 `style={{}}` eliminados.
- Verificación: `grep style={{}}` = 0, `npm run test:run` 67/67, E2E 8/8, `tsc --noEmit` OK, `biome check` OK, `next build` OK.
- Screenshots comparativos (editor + panel IA, dark/light) en `screenshots/cssmodules/`: dark byte-idéntico; light difiere solo en el hover del toggle (el inline style previo bloqueaba `button:hover` global; ahora el hover se ve, consistente con el resto de la app).
- Nota TS: con `noUncheckedIndexedAccess`, los `styles.x` tipan `string | undefined`; los Records de clases condicionales se tipan con `string | undefined` (className lo acepta).
