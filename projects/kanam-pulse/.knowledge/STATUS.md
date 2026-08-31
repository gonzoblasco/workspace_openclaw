# STATUS - Project Status

> **Ultima actualizacion:** 2026-08-31 12:05

## Current Phase

**v1.0.0 RELEASED + M6 UI polish (CleanMyMac-inspired dark theme) en desarrollo.**

## What's Working

- [x] M0-M5 completos. Tag v1.0.0 + GitHub Release (31/08)
- [x] Monorepo npm workspaces (core + server + web)
- [x] Engine health-check (46 tests) + dashboard + SSE
- [x] Consent-driven fixes (scan/dry-run/apply con confirmacion + trash-style)
- [x] Ollama audit summary (explain) - FIXED: think:false + default deepseek-v4-flash
- [x] a11y axe tests + CI (lint+test+build) + i18n (ES default/EN)
- [x] Biome lint + CHANGELOG + CONTRIBUTING + trash-style (SPEC trash-over-delete)
- [x] **M6 UI polish (31/08):** design system CleanMyMac-inspired (tema oscuro), sidebar + header + layout shell, gauge circular de salud, cards de checks, fixes con toggles, dialog con tema. lucide-react icons.

## Quality

- 37 tests verdes en web (36 previos + 1 nuevo AppShell render) + core 61 + server 21 = 119 total
- Biome lint exit 0 (6 warnings pre-existentes), build OK, CI gateado

## M6 UI polish - que se hizo (31/08)

- **Design tokens CSS** (`styles/App.css`): paleta oscura elegante (surfaces, borders, text, accent, status colors), tipografia, spacing scale, radius, sombras, focus ring a11y.
- **Layout shell** (`App.tsx`): sidebar de navegacion (brand + nav items + footer local-first) + header (titulo + status live) + main content. Responsive (grid colapsa a 1 columna < 860px).
- **HealthScoreCard**: gauge circular SVG (score + label), status badge con icono, boton explain con spinner, breakdown de checks por categoria con iconos de estado.
- **FixesPanel**: toolbar con botones (scan/dry-run/apply) con iconos, targets como rows con checkbox + label + descripcion + size, fieldset/legend para agrupar (a11y), empty states, result blocks.
- **ConfirmDialog**: tema oscuro, overlay + dialog con sombra, botones danger/cancel.
- **Iconografia**: lucide-react (ADR-037, estandar de Gonzo).
- **Tests actualizados**: HealthScoreCard usa `data-testid="health-score"` (el score del gauge es unico), FixesPanel mantiene fieldset/legend (role=group). Nuevo AppShell.test.tsx verifica el shell completo.

## Next / Pendiente

1. **Ver UI en browser** (Gonzo): `http://localhost:5173` - el browser de OpenClaw no puede navegar a localhost (politica). Confirmar visualmente.
2. Tag v1.0.1 (3 hotfixes en main) - decision Gonzo
3. Community announcement (LinkedIn)
4. Backlog: core a TypeScript, envoltorio nativo

## Decisions Log

- M6 UI polish: tema oscuro CleanMyMac-inspired (31/08)
- v1.0.0 released (31/08)
- explainAudit: think:false + default deepseek-v4-flash (31/08)
- trash-style con /usr/bin/trash (SPEC trash-over-delete)
- i18n es default + en pack (M4)
