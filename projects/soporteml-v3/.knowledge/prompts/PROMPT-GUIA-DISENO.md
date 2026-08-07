# Prompt: Guía de Diseño oficial de SoporteML (para Lovable)

> **Cuándo usar:** para pedirle a Lovable la guía de diseño de marca de SoporteML.
> **Estado:** YA EJECUTADO (2026-08-07). La respuesta de Lovable está en `../DESIGN-GUIDE-LOVABLE.md`.
> **Nota:** este prompt es la versión que se usó. Si se vuelve a pedir, ajustar según lo aprendido.

---

```
Actúa como un Lead Product Designer y Design System Engineer. Necesito que generes una GUÍA DE DISEÑO (design guide) para un CRM multi-tenant llamado "SoporteML", dirigido a vendedores de Mercado Libre, con asistencia de IA.

Contexto: la app es una herramienta de trabajo densa (paneles de gestión, tablas, formularios, dashboards), no una landing de marketing. El público la usa en desktop y mobile. La accesibilidad es un requisito central.

La guía debe definir la IDENTIDAD VISUAL y la MARCA, no la implementación técnica (eso ya está cubierto por un skill aparte). Incluí:

1. **Marca y personalidad**: posicionamiento visual, tono, valores que transmite la UI.
2. **Paleta de color**: paleta primaria y secundaria, con valores exactos (hex o HSL), y cómo se distribuye entre fondos, superficies, texto, acentos y estados (éxito, error, advertencia). Debe funcionar en tema claro y oscuro.
3. **Tipografía**: jerarquía tipográfica completa (títulos, subtítulos, cuerpo, captions, datos numéricos), con tamaños, pesos y usos.
4. **Iconografía y estilo visual**: qué estilo de íconos, radio de bordes, sombras, profundidad.
5. **Componentes clave**: cómo se ven botones (primario, secundario, destructivo, ícono), inputs, cards, tablas, badges, empty states, skeletons.
6. **Badges de categoría**: SoporteML categoriza consultas por tema (precio, stock, técnico, envío, garantía). Definí una paleta de badges distintiva para cada categoría.
7. **Layout y navegación**: estructura de dashboard con sidebar, patrones de densidad para datos, responsive mobile-first.
8. **Tono de la marca en texto**: microcopy, mensajes de error, empty states - el tono de voz de la app.

Devuelve la guía de diseño completa en Markdown, lista para ser usada como referencia de diseño por un equipo de desarrollo.
```
