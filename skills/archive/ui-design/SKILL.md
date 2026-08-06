---
name: "ui-design"
description: "Diseño de interfaces UI/UX: estructura visual, componentes, layout, responsive, modo oscuro, flujos de usuario, accesibilidad visual."
---

# Skill: UI Design

## Metadata
- **Categoría:** Design
- **Tags:** ui, ux, design, frontend, css, layout, responsive, dark-mode
- **Reemplaza:** N/A (skill nueva)

## Propósito
Diseñar y construir interfaces de usuario web desde cero: estructura visual, componentes, layout, responsive, modo oscuro, flujos de usuario. Produce HTML/CSS/JS listo para usar, sin dependencias de frameworks pesados.

## Cuándo usarla
- Diseñar una interfaz para un proyecto existente (web app, dashboard, landing)
- Crear prototipos funcionales sin backend
- Definir el sistema de diseño visual de un proyecto (colores, tipografía, espaciado, componentes)
- Refinar una UI existente (mejorar layout, responsive, modo oscuro)

## Fases

### 1. Análisis de requerimientos visuales
- ¿Qué tipo de interfaz? (lista/detalle, dashboard, landing, herramienta)
- ¿Quién la usa? (público general, admin, mobile-first?)
- ¿Hay guías de estilo existentes? (colores, tipografía, branding)
- ¿Modo oscuro necesario?
- ¿Animaciones/transiciones o funcional puro?

### 2. Arquitectura visual
- **Layout principal:** header, sidebar, contenido, footer. Responsive breakpoints.
- **Sistema de colores:** paleta primaria, secundaria, neutral, semántica (success, warning, error). Modo oscuro.
- **Tipografía:** jerarquía (h1-h6, body, small). Sistema de espaciado (4px/8px base).
- **Componentes:** tarjetas, botones, inputs, tabs, modales, listas. Estados (default, hover, active, disabled, focus).

### 3. Diseño de componentes
Para cada componente definir:
- Estructura HTML semántica
- Estados visuales
- Variantes (si aplica)
- Comportamiento responsive
- Accesibilidad (roles ARIA, focus management, contraste)

### 4. Implementación
- HTML semántico (landmarks, headings, lists)
- CSS moderno (Grid, Flexbox, Custom Properties, Container Queries)
- JS vanilla mínimo o nulo (preferir CSS-first)
- Modo oscuro con `prefers-color-scheme` + toggle manual
- Sin dependencias externas (Tailwind CDN aceptable para prototipos rápidos)

### 5. Verificación
- Responsive: 320px, 768px, 1024px, 1440px
- Modo oscuro: todos los componentes
- Contraste WCAG AA mínimo (4.5:1 texto normal, 3:1 texto grande)
- Navegación por teclado (Tab, Enter, Escape, focus visible)
- Sin dependencias rotas (si usó CDN, verificar URLs)

### 6. Post-diseño
- Documentar decisiones visuales en el proyecto (BRIEF o ADR visual)
- Integrar con build-scaffold si el proyecto necesita estructura más compleja
- Pasar por accessibility-studio para auditoría WCAG completa
- Pasar por copy-editing para pulir textos de la interfaz

## Principios de diseño
1. **Menos es más** — cada elemento debe tener una razón. Si no suma, sobra.
2. **Jerarquía visual clara** — el ojo debe saber a dónde mirar primero.
3. **Consistencia** — mismos colores, mismos espaciados, mismos patrones en toda la interfaz.
4. **Mobile-first** — diseñar para pantalla chica primero, después escalar.
5. **Accesibilidad no es opcional** — contraste, navegación por teclado, HTML semántico.
6. **Performance** — CSS > JS. HTML semántico > divs infinitos.

## Outputs
- Archivo(s) HTML/CSS/JS funcionales
- Sistema de diseño documentado (colores, tipografía, componentes)
- Verificación responsive + modo oscuro + accesibilidad básica

## Skills relacionadas
- [build-scaffold](../build-scaffold/SKILL.md): Para estructurar el proyecto después del diseño
- [accessibility-studio](../accessibility-studio/SKILL.md): Auditoría WCAG completa
- [vibe-code-cleanup](../vibe-code-cleanup/SKILL.md): Limpieza de código post-implementación
- [copy-editing](../copy-editing/SKILL.md): Pulido de textos de interfaz
- [tech-docs](../tech-docs/SKILL.md): Documentación de decisiones de diseño
