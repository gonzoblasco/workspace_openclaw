# WCAG 2.2 Criteria Reference

Catálogo completo de criterios WCAG 2.2 por principio y nivel de conformidad.

## Perceivable

### 1.1.1 Non-text Content — A
Todo contenido no textual debe tener alternativa textual equivalente.

### 1.2.1 Audio-only and Video-only (Prerecorded) — A
Alternativa textual para contenido solo audio o solo video.

### 1.2.2 Captions (Prerecorded) — A
Subtítulos para contenido de audio en video sincronizado.

### 1.2.3 Audio Description or Media Alternative (Prerecorded) — A
Descripción auditiva o alternativa textual para video.

### 1.2.4 Captions (Live) — AA
Subtítulos para contenido en vivo.

### 1.2.5 Audio Description (Prerecorded) — AA
Descripción auditiva para video pregrabado.

### 1.3.1 Info and Relationships — A
Relaciones semánticas preservadas en la presentación.

### 1.3.2 Meaningful Sequence — A
Orden de lectura correcto cuando el orden afecta el significado.

### 1.3.3 Sensory Characteristics — A
Instrucciones no dependen solo de características sensoriales (forma, color, tamaño, sonido, ubicación).

### 1.3.4 Orientation — AA
Contenido no restringido a una sola orientación (portrait/landscape).

### 1.3.5 Identify Input Purpose — AA
Propósito de los campos de entrada identificable programáticamente.

### 1.4.1 Use of Color — A
Color no es el único medio para transmitir información.

### 1.4.2 Audio Control — A
Control para pausar/detener audio automático (>3s).

### 1.4.3 Contrast (Minimum) — AA
Contraste texto: ≥ 4.5:1 (normal), ≥ 3:1 (large text ≥18px bold o ≥24px).

### 1.4.4 Resize Text — AA
Texto redimensionable hasta 200% sin pérdida de contenido o funcionalidad.

### 1.4.5 Images of Text — AA
Usar texto real, no imágenes de texto (excepto esencial).

### 1.4.10 Reflow — AA
Contenido sin scroll bidireccional a 320px de ancho (400% zoom).

### 1.4.11 Non-text Contrast — AA
Componentes interactivos y gráficos: ≥ 3:1 contra adyacentes.

### 1.4.12 Text Spacing — AA
Sin pérdida de contenido al ajustar espaciado (line-height 1.5, spacing 0.12em, word 0.16em).

### 1.4.13 Content on Hover or Focus — AA
Contenido emergente (tooltips): dismissible, hoverable, persistente.

## Operable

### 2.1.1 Keyboard — A
Toda funcionalidad operable por teclado.

### 2.1.2 No Keyboard Trap — A
Sin trampas de teclado: se puede mover el foco fuera del componente.

### 2.1.4 Character Key Shortcuts — A
Atajos de tecla única: remapeables o desactivables, o activos solo en foco.

### 2.2.1 Timing Adjustable — A
Límites de tiempo: desactivar, ajustar o extender.

### 2.2.2 Pause, Stop, Hide — A
Contenido en movimiento/parpadeo/auto-actualización: pausable, detenible, ocultable.

### 2.3.1 Three Flashes or Below Threshold — A
Sin destellos que excedan 3 flashes por segundo.

### 2.4.1 Bypass Blocks — A
Mecanismo para saltar bloques de contenido repetitivo (skip link).

### 2.4.2 Page Titled — A
Título de página descriptivo.

### 2.4.3 Focus Order — A
Orden de foco lógico y significativo.

### 2.4.4 Link Purpose (In Context) — A
Propósito del enlace determinable desde el texto del enlace o contexto.

### 2.4.5 Multiple Ways — AA
Múltiples formas de encontrar una página (búsqueda, mapa del sitio, navegación).

### 2.4.6 Headings and Labels — AA
Encabezados y labels descriptivos.

### 2.4.7 Focus Visible — AA
Indicador de foco visible en todo elemento interactivo.

### 2.4.11 Focus Not Obscured (Minimum) — AA
Foco no oculto por otro contenido.

### 2.4.12 Focus Not Obscured (Enhanced) — AAA
Foco completamente visible, no parcialmente oculto.

### 2.4.13 Focus Appearance — AAA
Indicador de foco: ≥ 2px de grosor, contraste ≥ 3:1 con el fondo.

### 2.5.1 Pointer Gestures — A
Gestos complejos (multi-touch, path-based) tienen alternativa de un solo punto.

### 2.5.2 Pointer Cancellation — A
Eventos down/up: cancelación posible (no ejecutar en mousedown).

### 2.5.3 Label in Name — A
Label visible coincide con el name accesible (aria-label debe incluir texto visible).

### 2.5.4 Motion Actuation — A
Funcionalidad activada por movimiento tiene alternativa de interfaz.

### 2.5.7 Dragging Movements — AA
Operaciones de arrastre tienen alternativa de un solo punto.

### 2.5.8 Target Size (Minimum) — AA
Touch targets ≥ 24×24px (preferible 44×44px).

## Understandable

### 3.1.1 Language of Page — A
Idioma de la página definido en `<html lang="...">`.

### 3.1.2 Language of Parts — AA
Cambios de idioma en el contenido marcados programáticamente.

### 3.2.1 On Focus — A
Cambio de contexto no ocurre al recibir foco.

### 3.2.2 On Input — A
Cambio de contexto no ocurre al cambiar valor de input sin confirmación.

### 3.2.3 Consistent Navigation — AA
Navegación repetida en mismo orden relativo en todas las páginas.

### 3.2.4 Consistent Identification — AA
Componentes con misma funcionalidad se identifican consistentemente.

### 3.3.1 Error Identification — A
Errores de input identificados y descritos al usuario.

### 3.3.2 Labels or Instructions — A
Labels o instrucciones presentes cuando se requiere input.

### 3.3.3 Error Suggestion — AA
Sugerencias para corregir errores de input.

### 3.3.4 Error Prevention (Legal, Financial, Data) — AA
Prevención de errores en transacciones legales, financieras o de datos (reversible, verificado, confirmable).

### 3.3.7 Accessible Authentication (Minimum) — AA
Autenticación no depende de tareas cognitivas (recordar contraseña, resolver puzzles).

### 3.3.8 Accessible Authentication (Enhanced) — AAA
Autenticación sin depender de funciones cognitivas en absoluto.

## Robust

### 4.1.1 Parsing — A (obsoleto en WCAG 2.2)
El contenido se parsea correctamente. (Nota: considerado obsoleto, cubierto por HTML spec.)

### 4.1.2 Name, Role, Value — A
Todos los componentes de UI tienen name y role determinables programáticamente.

### 4.1.3 Status Messages — AA
Mensajes de estado (éxito, error, sugerencia) anunciados por AT sin recibir foco (role="status", aria-live="polite").

## Niveles de Conformidad

| Nivel | Criterios | Para qué |
|---|---|---|
| **A** | Mínimos esenciales | Obligatorio legal en muchas jurisdicciones |
| **AA** | Estándar recomendado | Target para la mayoría de productos |
| **AAA** | Accesibilidad extendida | No requerido como nivel completo, aplicar criterios individuales |

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Testing Setup](./testing-setup.md) — Configuración de herramientas de auditoría
- [ARIA Patterns](./aria-patterns.md) — Patrones WAI-APG
