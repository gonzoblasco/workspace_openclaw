# ADR-001 - Identidad Visual de SoporteML V4

**Status:** Accepted
**Date:** 2026-08-17
**Scope:** SoporteML V4 (frontend)
**Deciders:** Gonzo / Kanam

## Context

SoporteML v3 quedó como un template básico: UI/UX sosa, cards shadcn estándar, cero identidad visual propia, cero diseño avanzado con CSS. Gonzo decidió reiniciar como V4 con estándar superior.

Se validó un mockup de identidad visual (`projects/soporteml-v4/mockups/identidad-v4.html`) con la dirección de diseño. Gonzo la aprobó y pidió incorporar iconografía profesional (Lucide, ver ADR-030).

## Decision

Adoptar la dirección de diseño **híbrido oscuro + color por categoría** para SoporteML V4.

### Principios

1. **Base oscura premium:** fondo casi negro azulado (`#0a0e1a`), superficies elevadas, glassmorphism, glow sutil. Sensación de herramienta de trabajo seria (TradingView, Linear, Raycast).
2. **Acento amarillo MeLi (`#ffe600`):** el color de marca de Mercado Libre como protagonista de los elementos de acción (botón primary, item activo del sidebar, labels de IA). Con glow sutil.
3. **Explosiones de color por categoría:** cada categoría de consulta (precio, stock, técnico, envío, garantía) tiene su propio color vibrante que ilumina la UI. La bandeja se vuelve escaneable al instante.
4. **Iconografía Lucide:** iconos SVG profesionales (ADR-030), no emojis.
5. **Micro-interacciones:** cards que se desplazan al hover, bordes que se iluminan, stats con barra de color por categoría, transiciones suaves.
6. **a11y WCAG 2.1 AA integrada:** contraste 4.5:1, focus visible, `aria-label` en botones de solo icono, jerarquía de headings.

### Paleta de color

| Token | Valor | Uso |
|-------|-------|-----|
| `--bg` | `#0a0e1a` | Fondo general (casi negro azulado) |
| `--bg-elevated` | `#111726` | Superficies elevadas |
| `--bg-sunken` | `#070a13` | Sidebar / paneles hundidos |
| `--surface` | `#151c2e` | Cards |
| `--surface-hover` | `#1a2236` | Hover en cards |
| `--meli` | `#ffe600` | Acento de marca (amarillo MeLi) |
| `--cat-precio` | `#38bdf8` | Categoría precio (azul cielo) |
| `--cat-stock` | `#34d399` | Categoría stock (verde esmeralda) |
| `--cat-tecnico` | `#a78bfa` | Categoría técnico (violeta) |
| `--cat-envio` | `#fb923c` | Categoría envío (naranja) |
| `--cat-garantia` | `#fb7185` | Categoría garantía (rosa) |

### Categorías de consulta (diferenciador visual)

Cada consulta tiene una **barra lateral de color** + **badge de categoría** con su color. Esto hace la bandeja escaneable al instante: de un vistazo sabés qué tipo de consulta es.

## Consecuencias

1. **Identidad visual propia:** SoporteML V4 no se ve como un template shadcn genérico.
2. **Bandeja escaneable:** el color por categoría mejora la eficiencia del flujo de trabajo (el corazón del producto).
3. **Sensación premium:** la base oscura + glow + micro-interacciones dan sensación de herramienta seria.
4. **Mantenible:** los tokens CSS se definen una vez y se reusan; el color por categoría es data-driven (cada categoría mapea a un token).

## Implementación

- Mockup validado: `projects/soporteml-v4/mockups/identidad-v4.html`
- Tokens CSS en `:root` del mockup (base para el design system real)
- Iconos: Lucide (ADR-030)
- El primer slice reconstruye el layout + bandeja con esta identidad sobre el backend de v3

## Referencias

- Mockup: `projects/soporteml-v4/mockups/identidad-v4.html`
- ADR-030 (Lucide): `docs/adr/ADR-030-lucide-iconos-base.md`
- v3 design guide: `projects/soporteml-v3/.knowledge/DESIGN-GUIDE.md`
