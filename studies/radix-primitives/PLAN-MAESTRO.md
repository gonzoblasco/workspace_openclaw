# PLAN-MAESTRO - radix-primitives

Capa 1 (estatica). Nivel -> subnivel -> topic. Cada topic se completa y se verifica solo.
XP: 10 por topic, badge por nivel, jefe final al cierre.

---

## Nivel 1 - El modelo mental (que es y que no es)

**Subnivel 1.1 - El problema que resuelve**
- **1.1.1** Los patrones de UI (accordion, dialog, select, tooltip) estan documentados por WAI-ARIA, pero las implementaciones del browser son insuficientes. Radix existe para llenar ese hueco.
- **1.1.2** La consecuencia del hueco: la mayoria de los componentes de la web son inaccesibles, poco performantes o sin features clave.

**Subnivel 1.2 - Las 5 propiedades del diseno**
- **1.2.1** Accessible (WAI-ARIA + foco + teclado), Unstyled (estilos 100% tuyos), Opened (granularidad por parte del componente).
- **1.2.2** Uncontrolled por defecto (controlado si hace falta) y DX (API tipada, consistente, `asChild`).
- **1.2.3** Adopcion incremental: el paquete `radix-ui` es tree-shakeable, o se instala primitive por primitive.

**Subnivel 1.3 - Anatomia de un primitive**
- **1.3.1** Partes compuestas con roles: `Root`, `Trigger`, `Portal`, `Overlay`, `Content`, `Title`, `Description`, `Close` (caso Dialog).
- **1.3.2** Por que la composicion importa: cada parte es un punto de intervencion.

**Subnivel 1.4 - Que NO hace Radix**
- **1.4.1** No estiliza. Ni siquiera los estilos funcionales: un `Dialog.Overlay` no cubre el viewport hasta que vos lo haces.
- **1.4.2** No es un design system ni una libreria de componentes "con look". No reemplaza a Tailwind ni a los tokens.
- **1.4.3** No es magia: los nombres accesibles (`Title`, `Description`, `Label`) los provee el consumidor.

**Verificacion del nivel:** explicar en 3 frases que problema resuelve Radix y que queda fuera de su alcance.

---

## Nivel 2 - La API (como se usa)

**Subnivel 2.1 - Instalacion**
- **2.1.1** Paquete unico `radix-ui` (recomendado: evita duplicacion y conflictos de version) vs paquetes individuales `@radix-ui/react-*`.
- **2.1.2** Regla de mantenimiento: si se instalan por separado, actualizar todos juntos.

**Subnivel 2.2 - Composicion**
- **2.2.1** `asChild`: no renderiza el elemento por defecto, clona el hijo y le pasa props + comportamiento (ej. `Tooltip.Trigger asChild` sobre un `<a>`).
- **2.2.2** Los dos gotchas al componer con componentes propios: el componente debe hacer **spread de props** y debe **forwardear ref**.
- **2.2.3** `asChild` compone en profundidad (Tooltip.Trigger > Dialog.Trigger > MyButton).

**Subnivel 2.3 - Estado**
- **2.3.1** No controlado por defecto; controlado con `open`/`onOpenChange` (ej. cerrar un Dialog tras un submit async).
- **2.3.2** Cuando conviene controlar y cuando no.

**Subnivel 2.4 - Estilos**
- **2.4.1** `className` en cada parte + `data-state` (`"open" | "closed"`) para estilar estados.
- **2.4.2** Compatible con cualquier solucion: CSS, CSS Modules, CSS-in-JS.
- **2.4.3** Extender un primitive con `forwardRef` + tipos (`ComponentPropsWithoutRef`, `ElementRef`).

**Subnivel 2.5 - Primitives clave a conocer** (uno por patron, no todos)
- **2.5.1** Dialog / AlertDialog (modal + foco + title/description).
- **2.5.2** Popover / Tooltip (no modal, posicionamiento, `Arrow`).
- **2.5.3** Select / DropdownMenu.
- **2.5.4** Label + VisuallyHidden (helpers de nombre accesible).

**Verificacion del nivel:** construir un componente chico propio, envuelto en un primitive con `asChild`, con estilos por `data-state`.

---

## Nivel 3 - La accesibilidad (el contrato)

**Subnivel 3.1 - La base**
- **3.1.1** WAI-ARIA APG como documento fuente; Radix lo sigue "donde es posible".
- **3.1.2** Que significa "donde es posible": hay huecos declarados.

**Subnivel 3.2 - Nombres accesibles**
- **3.2.1** `Label` para controles de formulario; la calculacion de nombre accesible segun la spec.
- **3.2.2** `Title` / `Description` en Dialog; `VisuallyHidden` para ocultar visualmente sin perder el nombre.

**Subnivel 3.3 - Teclado**
- **3.3.1** Que teclas espera cada patron (Tabs, Dialog) segun APG.
- **3.3.2** Que cubre Radix y que tenes que cablear vos.

**Subnivel 3.4 - Foco**
- **3.4.1** Trampa de foco en modal; autofocus al abrir; retorno de foco al cerrar.
- **3.4.2** Los hooks de control: `onOpenAutoFocus`, `onCloseAutoFocus`, `onEscapeKeyDown`, `onInteractOutside`.

**Subnivel 3.5 - Donde Radix no alcanza**
- **3.5.1** Lo que sigue siendo responsabilidad del consumidor: labels, orden de tabulacion del layout, contenido y jerarquia.
- **3.5.2** Patrones de a11y que ningun primitive resuelve (anuncios live, errores de formulario, contraste).

**Verificacion del nivel:** auditar un Dialog propio y listar que garantiza Radix y que verificamos nosotros.

---

## Nivel 4 - Radix en el stack real (shadcn y nuestros proyectos)

**Subnivel 4.1 - Radix y shadcn**
- **4.1.1** Que agrega shadcn sobre Radix: archivos propios en tu repo, estilos con Tailwind, CLI. No es una dependencia de runtime.
- **4.1.2** Implicancia: el codigo de shadcn es tuyo y editable; Radix sigue siendo la dependencia real.

**Subnivel 4.2 - Cuando bajar al primitive**
- **4.2.1** Cuando el wrapper de shadcn tapa una parte o impone una API que estorba.
- **4.2.2** Como bajar sin romper el resto (extender, no forkear).

**Subnivel 4.3 - Cuando NO usar Radix**
- **4.3.1** Lo que el HTML nativo ya resuelve (un `<dialog>` simple, un `<details>`).
- **4.3.2** Lo que ni shadcn ni Radix cubren y hay que escribir.

**Subnivel 4.4 - Aplicacion a proyectos propios**
- **4.4.1** Barrido de los proyectos que declaran shadcn/Radix: `kanam-forge` (ancla), `quedamos`, `kanam-mind`. Que primitives estan en uso y por que. **Fuera del barrido: toda la familia `soporteml`** (v1, v3, v4) - ADR-001 la excluye de narrativa y de auditorias; no se toca ni se lista. **Caso aparte - `kanam-pulse`:** a11y WCAG 2.2 AA desde el dia uno y **NO usa Radix**. Es el contraejemplo que vale estudiar: por que un proyecto a11y-first no necesita primitives.
- **4.4.2** Donde el uso es correcto, donde es inercia.

**Verificacion del nivel:** producir la lista de primitives realmente usados en los proyectos, con justificacion por cada uno.

---

## Nivel 5 - Criterio de decision y mantenimiento

**Subnivel 5.1 - Radix contra alternativas**
- **5.1.1** Criterios comparables: cobertura de APG, licencia, mantenimiento, granularidad, peso, DX.
- **5.1.2** Alternativas a evaluar: HTML nativo, Base UI, Ariakit, headless propio.

**Subnivel 5.2 - La decision documentada**
- **5.2.1** Escribir el ADR que hoy no existe (adopcion de shadcn/Radix, con fundamentos reales).

**Subnivel 5.3 - Mantenimiento**
- **5.3.1** Versionado y alineacion de paquetes; cuanto pesa en el bundle.

**Verificacion del nivel (jefe final):** escribir el ADR de adopcion de Radix/shadcn con los criterios verificados, sin citar el precedente como motivo.
