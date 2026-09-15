# Nivel 2 - La API (como se usa)

Capa 2 (cuaderno). Fuente: docs oficiales de Radix Primitives, verificadas 2026-09-14.
**Version verificada en npm al dia de hoy:** `radix-ui` **1.6.7** (publicada 2026-07-24, licencia MIT, 55 dependencias internas `@radix-ui/*`).

---

## 2.1 Instalacion

### 2.1.1 Paquete unico vs primitives individuales

```bash
npm install radix-ui            # RECOMENDADO
```
```jsx
import { Dialog, DropdownMenu, Tooltip } from "radix-ui";
```

```bash
npm install @radix-ui/react-dialog   # alternativa
```
```jsx
import * as Dialog from "@radix-ui/react-dialog";
```

El paquete unico es la via recomendada por la doc por una razon concreta: **evita conflictos de version y duplicacion** entre primitives, que comparten dependencias internas. Y es **tree-shakeable**: solo se empaqueta lo que se importa, asi que el peso no es el del paquete completo.

Verificado: `radix-ui@1.6.7` declara **55 dependencias internas `@radix-ui/*`**. Ese es el motivo real de la recomendacion: instalar 5 primitives por separado puede arrastrar el mismo paquete interno en 5 versiones distintas.

### 2.1.2 Regla de mantenimiento

Si se instalan por separado, **actualizarlos todos juntos**. Mezclar versiones de primitives que comparten dependencias es la forma mas facil de romper algo sin tocar una linea de codigo propio.

---

## 2.2 Composicion (`asChild`)

### 2.2.1 Que hace

Todas las partes que renderizan un elemento del DOM aceptan `asChild`. Con `asChild`, Radix **no renderiza su elemento por defecto**: clona el hijo y le pasa **las props y el comportamiento** necesarios para que funcione.

```jsx
<Tooltip.Root>
  <Tooltip.Trigger asChild>
    <a href="...">Radix UI</a>   {/* en vez del <button> por defecto */}
  </Tooltip.Trigger>
  ...
</Tooltip.Root>
```

El caso tipico es un `Trigger`: sirve para colgar el comportamiento de un elemento de tu design system (tu boton, tu link) en vez del default.

**Aviso de la doc, importante:** si cambias el elemento, **la accesibilidad vuelve a ser tu responsabilidad**. El ejemplo es literal: si cambias `Tooltip.Trigger` por un `div`, deja de ser accesible. Radix te da el comportamiento, no la garantia del elemento.

### 2.2.2 Los dos gotchas al componer con componentes propios

Para que `asChild` funcione sobre un componente tuyo, el componente tiene que:

1. **Hacer spread de props** - Radix le va a pasar sus props y handlers; si no los reenvía al DOM, se rompe.
   ```jsx
   const MyButton = (props) => <button {...props} />;
   ```
2. **Forwardear `ref`** - Radix a veces necesita medir el elemento.
   ```jsx
   const MyButton = React.forwardRef((props, ref) => <button {...props} ref={ref} />);
   ```

La doc recomienda hacer **las dos cosas siempre** en componentes "hoja", aunque ese part no las necesite: evita tener que averiguar que props acepta cada caso.

### 2.2.3 Composicion en profundidad

`asChild` se puede anidar todo lo necesario. Puede componer **varios primitives entre si**:

```jsx
<Dialog.Root>
  <Tooltip.Root>
    <Tooltip.Trigger asChild>
      <Dialog.Trigger asChild>
        <MyButton>Open dialog</MyButton>   {/* un solo elemento, 3 comportamientos */}
      </Dialog.Trigger>
    </Tooltip.Trigger>
    ...
```

Un boton que a la vez tiene tooltip y abre un dialog, sin wrapper extra. Esto es lo que compra la composicion: apilar comportamientos sobre el **mismo** nodo.

---

## 2.3 Estado

### 2.3.1 No controlado por defecto, controlado si hace falta

| Modo | Como se usa |
|---|---|
| **No controlado** (default) | No pasas nada. `defaultOpen` si necesitas arrancar abierto. |
| **Controlado** | `open` + `onOpenChange`. Vos sos dueño del estado. |

El caso de uso tipico del controlado (de la doc): **cerrar un Dialog despues de un submit asincronico** - el `setOpen(false)` va en el `.then()`.

```jsx
<Dialog.Root open={open} onOpenChange={setOpen}>
```

### 2.3.2 Cuando controlar

- **No controlado** por defecto: es menos codigo y Radix ya resuelve interacciones.
- **Controlado** cuando el estado necesita **vivir afuera** del componente: para sincronizarlo con otra cosa, para cerrarlo programaticamente tras una operacion asincronica, o para tener varios elementos disparando el mismo popup.

Regla practica: si tenes que leer o escribir el estado desde afuera, controla. Si no, deja que Radix lo maneje.

---

## 2.4 Estilos

### 2.4.1 `className` + `data-state`

Cada parte acepta `className`, que se pasa al DOM. Y lo importante: los componentes con estado exponen su estado en **`data-state`**, asi que se puede estilar un estado sin JavaScript:

```css
.AccordionItem { border-bottom: 1px solid gainsboro; }
.AccordionItem[data-state="open"] { border-bottom-width: 2px; }
```

Los valores varian por componente (ver 2.5: `Tooltip` tiene tres, no dos). Ademas de `data-state`, cada componente agrega los data-attributes que le hacen falta: `Select` tiene `data-placeholder` y `data-disabled`.

### 2.4.2 Cualquier solucion de estilos

CSS, CSS Modules, CSS-in-JS (el ejemplo de la doc usa `styled-components`, explicitamente "podes usar la que quieras"). No hay lock-in de estilos: es la contraparte de ser unstyled.

### 2.4.3 Extender un primitive

Se hace como con cualquier componente React: `forwardRef` + los tipos del primitive.

```tsx
import { Accordion as AccordionPrimitive } from "radix-ui";

const AccordionItem = React.forwardRef<
  React.ElementRef<typeof AccordionPrimitive.Item>,
  React.ComponentPropsWithoutRef<typeof AccordionPrimitive.Item>
>((props, forwardedRef) => <AccordionPrimitive.Item {...props} ref={forwardedRef} />);

AccordionItem.displayName = "AccordionItem";
```

Nota: **`React.ElementRef` y `ComponentPropsWithoutRef`** son los tipos que hacen el trabajo. Y `displayName` explicito porque `forwardRef` lo pierde (afecta devtools y mensajes de error).

---

## 2.5 Primitives clave

### 2.5.1 Dialog (y AlertDialog)

Ventana que **renderiza el contenido de abajo como inert**. Es el modal.

- `Root`: `open`/`onOpenChange`, y **`modal`** (default **`true`**).
- `Trigger`, `Portal` (monta en `body`), `Overlay`, `Content`, `Close`.
- `Title` y `Description`: los componentes de **nombre y descripcion accesible**. De la doc: si queres ocultar el titulo, va dentro de `VisuallyHidden`; si no queres descripcion, se omite el part y se pasa `aria-describedby={undefined}` al `Content`.
- Lo que trae hecho: **foco atrapado dentro del modal** cuando es modal; `Esc` cierra solo; maneja los anuncios de screen reader con `Title`/`Description`.
- Hooks de control en `Content`: `onOpenAutoFocus`, `onCloseAutoFocus`, `onEscapeKeyDown`, `onPointerDownOutside`, `onInteractOutside`.

### 2.5.2 Popover y Tooltip (los no-modales)

**Popover** - contenido rico en un portal, disparado por un boton.

- Partes: `Root`, `Trigger`, `Anchor`, `Portal`, `Content`, `Close`, `Arrow`.
- **`Anchor`** es interesante: posiciona el `Content` contra **otro** elemento que no es el trigger (sin el, se posiciona contra el trigger).
- **`modal` default `false`** (al contrario de Dialog).
- `Content` expone los mismos hooks de foco/dismiss que Dialog.
- Customizable: lado, alineacion, offsets, colision. `Arrow` opcional.

**Tooltip** - informacion al **foco o al hover**.

- Envuelto en un **`Provider`** global: `delayDuration` (default **700ms**), `skipDelayDuration` (default **300ms**), `disableHoverableContent`.
- Se abre al foco o hover; se cierra al activar o con `Esc`.
- `data-state` con **tres** valores: `"closed" | "delayed-open" | "instant-open"`.
- El `skipDelayDuration` es el detalle de UX fino: una vez que viste un tooltip, los siguientes abren instantaneo si pasas el mouse dentro de esa ventana.

### 2.5.3 Select

Lista de opciones disparada por un boton. El mas complejo de los cuatro.

- Trae hecho: **navegacion completa por teclado**, **typeahead**, soporte **RTL**, 2 modos de posicionamiento, items/labels/groups/separators.
- Partes: `Root`, `Trigger`, `Value`, `Icon`, `Portal`, `Content`, `Viewport`, `Item`, `ItemText`, `ItemIndicator`, `Group`, `Label`, `Separator`, `ScrollUpButton`, `ScrollDownButton`, `Arrow`.
- `Root` acepta `name`, `required`, `disabled`, `dir` - o sea **participa de un `<form>`** sin envolverlo a mano.
- `data-state` (`open|closed`), **`data-disabled`**, **`data-placeholder`**. Los ultimos dos permiten estilar "sin valor seleccionado" y "deshabilitado" en CSS puro.

### 2.5.4 Label y VisuallyHidden (los helpers de nombre)

- **`Label`** - pensado para trabajar con los controles de Radix. Provee el mecanismo; el texto lo pones vos.
- **`VisuallyHidden`** - oculta visualmente sin sacar del arbol de accesibilidad. Su uso tipico: `<VisuallyHidden asChild>` envolviendo un `Title` de Dialog cuando el diseño no muestra titulo (ver 2.5.1). Es el pattern "invisible pero nombrado".

---

## Lo que revela la API (insights del nivel)

1. **`modal` cambia de default segun el componente:** `true` en Dialog, `false` en Popover. No es un detalle: define si el foco queda atrapado y si el fondo se vuelve inert. Elegir mal el primitive cambia el comportamiento de accesibilidad, no solo el visual.
2. **`data-state` no siempre es binario:** Tooltip tiene 3 valores porque tiene delay. Estilar asumiendo `open|closed` en un Tooltip deja el estado intermedio sin estilo.
3. **El estado vive en el DOM, no en JS:** toda la estilizacion de estados se hace por `data-*`. Es lo que permite integrar Radix con Tailwind/CSS Modules sin puentes.
4. **`asChild` es la puerta de entrada al design system propio:** es el mecanismo que evita wrappers y permite apilar comportamientos sobre un mismo nodo. Sus dos requisitos (spread + forwardRef) son, literalmente, las dos cosas que un componente hoja tiene que hacer bien.

---

## Verificacion del Nivel 2

1. Por que la doc recomienda `radix-ui` (paquete unico) y que costo evita?
2. Que dos cosas tiene que hacer un componente propio para funcionar dentro de un `asChild`?
3. Cuando pasarias un `Dialog` a **controlado** en lugar de dejarlo no controlado?
