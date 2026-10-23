# LinkedIn Post: aria-orientation en los role owners (base-ui)

**Status:** PUBLICADO 24/08/2026
**Nicho:** a11y (diferenciador)
**Proyecto:** mui/base-ui
**PR:** #5551
**Fecha:** 2026-08-28

---

## Post (version publicada)

El error de accesibilidad más difícil de detectar no es el que rompe el screen reader, sino el que lo confunde con información inválida.

Hace unos días mergeé un fix en MUI Base UI que ilustra perfectamente este punto: un `aria-orientation` mal ubicado.

**El problema**

En un Combobox con grid, el componente emitía `aria-orientation="horizontal"` directamente en el elemento con `role="grid"`. El problema: el role `grid` **no soporta** `aria-orientation`. Es un atributo válido en HTML, pero inválido para ese rol ARIA.

El resultado no era un crash ni un error visible. Era algo peor: los screen readers recibían información contradictoria sobre cómo navegar el componente, degradando silenciosamente la experiencia para usuarios de tecnologías de asistencia.

**La solución**

El fix fue mover `aria-orientation` a los elementos que realmente son los "role owners" (los que sí soportan el atributo), y omitirlo en `grid` y `presentation`. Siete archivos, 69 líneas agregadas, 4 eliminadas, con tests de regresión para asegurar que la navegación por teclado se preservara.

**El por qué importa**

La accesibilidad no es solo "poner un aria-label". Es entender el **contrato ARIA**: qué atributos son válidos para cada rol, y cómo los screen readers interpretan esa información. Un atributo inválido no siempre rompe la app, pero siempre degrada la experiencia de alguien.

Cuando la accesibilidad se trata como una disciplina de ingeniería (con tests de regresión, validación de roles y revisión de pares), los bugs sutiles como este se detectan antes de llegar a producción.

#Accessibility #ARIA #WCAG #OpenSource #FrontendEngineering


PR: https://github.com/mui/base-ui/pull/5551

---

*Nota de estado: La fecha de publicacion no quedo registrada. La que se anota es la del merge del PR (#5551, 24/08/2026). Publicacion registrada por Gonzo el 2026-10-22; el `Status:` no existia en el archivo.*
