# ADR-037: Lucide Iconos Base

**Status:** Accepted
**Fecha:** 2026-08-17
**Origen:** kanam-workflow
**Scope:** Global - aplica a todos los proyectos (web, apps, dashboards)
**Deciders:** Gonzo / Kanam

## Contexto

Los proyectos de Gonzo (Soporteml v1/v3, Kanam Story, Kanam Forge, y futuros) usan iconografía en sus UIs. Hasta ahora la elección de iconos era implícita: cada proyecto usaba lo que traía el template (shadcn/ui incluye Lucide por default, pero no estaba documentado como decisión).

En el mockup de identidad visual de SoporteML v4, se validó la dirección de diseño (híbrido oscuro + color por categoría) y se decidió reemplazar los emojis placeholder por iconografía profesional. Esto expuso la necesidad de una **decisión explícita y documentada** sobre la librería de iconos base.

**Anti-patrón a evitar:** emojis como iconografía de producto. Se ven distintos según el SO, no son consistentes, no soportan estados (hover/active/focus), no escalan con el peso visual, y no se integran con el sistema de tokens.

## Decision

Usar **Lucide** (`lucide-react` para React) como librería de iconos base en todos los proyectos.

### Por qué Lucide

1. **Ecosistema shadcn/Radix:** es la librería que shadcn/ui y Radix usan por default. Se integra sin fricción con el stack existente.
2. **1500+ iconos SVG consistentes:** stroke-based, mismo peso visual, diseño coherente.
3. **Tree-shakeable:** solo se importan los iconos usados, sin bloat.
4. **`currentColor`:** los iconos heredan el color del contexto (item activo del sidebar, botón primary, etc.), lo que los integra con el sistema de tokens CSS.
5. **Accesible:** SVG con `aria-hidden` por default (los iconos decorativos no deben leerse por screen readers; el texto del label es el que comunica).
6. **Activa y mantenida:** proyecto open source con releases frecuentes.

### Reglas de uso

- **Iconos decorativos:** `aria-hidden="true"` (o el default de Lucide) + `focusable="false"`. El significado lo da el texto adyacente o `aria-label` en el elemento interactivo.
- **Botones de solo icono:** siempre `aria-label` descriptivo (WCAG 2.1 AA, 4.1.2).
- **Tamaño:** heredar del contexto (16px sidebar, 15px botones, 12px labels). No hardcodear tamaños salvo necesidad.
- **Color:** usar `currentColor` (default) para que herede del token del contexto. No colorear iconos individualmente salvo casos específicos (ej. icono de IA en amarillo MeLi).
- **Nunca emojis** como iconografía de producto.

## Consecuencias

1. **Consistencia visual** entre proyectos: misma librería, mismo estilo de iconos.
2. **Menos fricción:** los iconos se integran con el sistema de tokens y el stack shadcn/Radix.
3. **Accesibilidad por default:** los iconos decorativos no rompen la lectura por screen readers.
4. **Decisión documentada:** no se re-discute por proyecto; es la base.

## Implementación

```bash
# React (estándar en los proyectos de Gonzo)
pnpm add lucide-react
```

```tsx
import { Inbox, Zap, BarChart } from "lucide-react";

// Icono decorativo en un nav item
<nav aria-label="Principal">
  <a href="/inbox" aria-current="page">
    <Inbox aria-hidden="true" />
    <span>Inbox</span>
  </a>
</nav>

// Botón de solo icono (requiere aria-label)
<button aria-label="Sincronizar">
  <RefreshCw aria-hidden="true" />
</button>
```

## Referencias

- Lucide: https://lucide.dev
- `lucide-react` en npm: https://www.npmjs.com/package/lucide-react
- Ya usado en: Soporteml v1 (`projects/soporteml`), Soporteml v3 (`projects/soporteml-v3`), mockup de identidad V4 (ver nota abajo)

## Nota (2026-09-22): ubicacion del mockup

El mockup `projects/soporteml-v4/mockups/identidad-v4.html` **existio y fue validado por Gonzo**, pero **ya no esta en disco**: se commiteo en `b450ebda` (restart de soporteml-v4 con diseno premium) y se removio al limpiar el proyecto terminado, que borra el codigo y conserva solo `.knowledge/` (ver AGENTS.md, Project Cleanup). No es un artefacto que nunca se creo.

La decision de identidad visual que ese mockup fundamento sigue registrada en `projects/soporteml-v4/.knowledge/ADR-001-identidad-visual.md`, que conserva los tokens CSS y la direccion de diseno. Si hace falta el archivo en si, recuperarlo con `git show b450ebda:projects/soporteml-v4/mockups/identidad-v4.html`.

## Nota (2026-09-14)

El punto 1 de "Por que Lucide" cita *el ecosistema shadcn/Radix*. En su momento era una referencia circular: este ADR admitia que la eleccion venia del template y la usaba igual como fundamento. Desde el **ADR-048** esa cita tiene respaldo real - la adopcion de Radix/shadcn quedo documentada como decision explicita, con reglas de uso y disparadores de revision.
