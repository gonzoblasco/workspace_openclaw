# LinkedIn Post: TreeList sin nombre (astryx)

**Status:** PUBLICADO 26/08/2026
**Nicho:** a11y (diferenciador)
**Proyecto:** facebook/astryx
**PR:** #5493
**Fecha:** 2026-08-28

---

## Post (version publicada)

Un árbol sin nombre es un árbol invisible para el screen reader.

Hace unos días mergeé un fix en Astryx que resuelve un bug de accesibilidad sutil pero importante: un componente `TreeList` que no podía ser nombrado cuando no tenía un header visible.

**El problema**

El `TreeList` renderizaba un `<ul role="tree">` con los items, pero no exponía `aria-label` ni `aria-labelledby` al elemento raíz. El resultado: cuando el árbol no tenía un header visible que lo describiera, los usuarios de screen readers escuchaban un "tree" sin contexto. No sabían qué contenía, ni para qué servía, ni cómo navegarlo de forma significativa.

**La solución**

El fix forwardea `BaseProps` (incluyendo `aria-label` y `aria-labelledby`) al `<ul role="tree">`. La lógica de prioridad: si hay un header visible, gana el header; si no, se usa el `aria-label` explícito. El `role` se aplica después del resto de props para no pisar la semántica.

**El por qué importa**

Este es un ejemplo clásico de por qué la accesibilidad no es un "checkbox" al final del desarrollo. Un componente que no puede ser nombrado es un componente que excluye a usuarios de tecnologías de asistencia, sin que nadie lo note en el código.

La accesibilidad es una propiedad del diseño del componente, no un parche. Cuando el naming (cómo se identifica un elemento) se diseña desde el inicio, los bugs como este no existen.

#Accessibility #ARIA #WCAG #OpenSource #ComponentDesign


PR: https://github.com/facebook/astryx/pull/5493

---

*Nota de estado: La fecha de publicacion no quedo registrada. La que se anota es la del merge del PR (#5493, 26/08/2026). Publicacion registrada por Gonzo el 2026-10-22; el `Status:` no existia en el archivo.*
