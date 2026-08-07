# Prompt: Skill de UI/UX Design System Engineering (para Lovable)

> **Cuándo usar:** para pedirle a Lovable el contenido del skill `ui-design-engineer` (estándar de implementación UI).
> **Estado:** YA EJECUTADO (2026-08-07). La respuesta de Lovable se convirtió en `../UI-DESIGN-SKILL.md` (luego adaptada a SoporteML).
> **Nota:** este es el prompt ORIGINAL que generó el skill. El skill final (específico de SoporteML) está en `../UI-DESIGN-SKILL.md`.

---

```
Actúa como un Lead Product Designer y Design System Engineer. Necesito que generes el contenido para un archivo `SKILL.md` técnico y ejecutable, diseñado específicamente para que un agente de IA para desarrollo (como Claude Code o Cursor) implemente interfaces de usuario de alta calidad con nivel profesional.

El objetivo de este SKILL.md es restringir las malas decisiones genéricas de diseño que suelen cometer los LLMs y forzar un estándar visual pulido, moderno y consistente.

El agente asumirá un stack moderno (React + Tailwind CSS + shadcn/ui o Radix UI + Lucide Icons). El skill es GENÉRICO y stack-bound: aplica a cualquier proyecto con ese stack, NO es específico de una marca o producto. No incluyas paletas, logos ni componentes propietarios de ningún producto concreto.

Contexto de uso principal (para calibrar las decisiones de densidad, jerarquía y accesibilidad): un CRM multi-tenant para vendedores de e-commerce, con paneles de gestión de datos densos, tablas, formularios y dashboards. El público usa la app en desktop y mobile. La accesibilidad es un requisito central, no un checkbox.

Estructura el archivo `SKILL.md` en formato Markdown técnico. Incluí el frontmatter YAML obligatorio al inicio con `name` y `description` (el description debe decir qué hace el skill y para qué stack aplica, en una o dos frases). Abarcá las siguientes secciones:

1. Visión General y Filosofía de UI/UX
- Principios de diseño: jerarquía visual clara, minimalismo funcional, densidad equilibrada y consistencia.
- Regla de oro: No inventar estilos o colores fuera de los tokens definidos. Si no existe un token, consultar antes de crearlo.

2. Sistema de Tokens y Reglas de Maquetación (Tailwind CSS)
- Espaciado: Estricto uso de la escala de 8pt (gap, padding, margin en múltiplos de 4 u 8).
- Tipografía: Definición de escala (`text-xs` a `text-3xl`), tracking y font-weights según el contexto (encabezados, cuerpo, captions).
- Paleta Cromática y Temas: Uso exclusivo de variables semánticas (`bg-background`, `text-foreground`, `text-muted-foreground`, `border-border`, `bg-primary`, etc.). Prohibido usar hex o colores arbitrarios inline.

3. Reglas de Componentes y Microinteracciones
- Estados obligatorios: Toda entidad interactiva debe manejar e implementar explícitamente estados `hover`, `active`, `focus-visible` (con ring accesible), `disabled` y `loading`.
- Animaciones: Uso de transiciones sutiles (`transition-all duration-150 ease-in-out`), respetando `prefers-reduced-motion`.
- Empty States y Skeletors: Guía para manejar visualmente la carga de datos y las pantallas sin contenido.

4. Layouts, Responsive Design y Grids
- Patrones de maquetación: Flexbox y Grid-first. Evitar posiciones absolutas salvo casos extremos (modales, tooltips).
- Estrategia Mobile-First: Reglas explícitas de breakpoints (`sm`, `md`, `lg`), con la regla de escribir estilos base para mobile y agregar breakpoints progresivos.

5. Accesibilidad (a11y) y Semántica HTML
- Estructura semántica (`<main>`, `<nav>`, `<header>`, `<article>`).
- Cumplimiento WCAG: Contraste de texto y etiquetas `aria-*` cuando los componentes carezcan de texto visible.

6. Anti-patrones explícitos ("Qué NO hacer")
- Lista de errores comunes a evitar por la IA (p. ej., bordes demasiado oscuros, gradientes innecesarios, tamaños de fuente inconsistentes, animaciones lentas o molestas, botones sin feedback visual).

7. Workflow de revisión (el "cómo", no solo el "qué")
- Pasos concretos y verificables para auditar un cambio de UI antes de darlo por terminado: revisar el DOM renderizado, buscar clases arbitrarias o hex inline (grep), probar estados hover/focus/disabled en el navegador, verificar mobile y desktop con screenshot, y validar contraste.

8. Scope y cuándo NO aplicar
- Indicá explícitamente en qué casos este skill NO aplica (p. ej., proyectos sin Tailwind/shadcn, landings de marketing donde el texto centrado o los gradientes sí tienen sentido).

9. Checklist final
- Checklist accionable y verificable de puntos a cumplir antes de entregar un cambio de UI.

Devuelve únicamente el contenido del archivo `SKILL.md` dentro de un bloque de código Markdown, listo para ser copiado.
```
