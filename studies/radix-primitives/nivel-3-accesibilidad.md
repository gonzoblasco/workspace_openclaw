# Nivel 3 - La accesibilidad (el contrato)

Capa 2 (cuaderno). Fuente: docs oficiales de Radix Primitives (overview de accesibilidad + features por componente), verificadas 2026-09-14.
Es el nivel que cruza el estudio con la especialidad: **que garantiza Radix y que queda en nuestra cancha**.

---

## 3.1 La base

### 3.1.1 WAI-ARIA APG como documento fuente

Radix se apoya en dos documentos del W3C:

- **WAI-ARIA** (la spec): define la **semantica** de los patrones. El ejemplo de la doc es exacto: si usas un `div` en vez de un `button`, hay atributos que tenes que agregar para que se anuncie como boton.
- **WAI-ARIA APG** (Authoring Practices): define los **comportamientos** esperados. Un `button` responde a ciertas interacciones que un `div` no: esas interacciones hay que reimplementarlas con JavaScript.

La frase de Radix sobre esto: los componentes **"siguen los patrones WAI-ARIA donde es posible"** y estan probados en browsers modernos y tecnologias de asistencia comunes.

### 3.1.2 Que significa "donde es posible"

Es la parte honesta y hay que leerla literal: **hay huecos declarados**. Radix cubre "muchos de los detalles de implementacion dificiles" -atributos `aria` y `role`, manejo de foco, navegacion por teclado-, pero la cobertura se llama **"basic keyboard support"** en la doc de teclado.

Traduccion operativa: no asumir cobertura total por usar el primitive. **Verificar por componente** contra el APG. Es el mismo criterio que aplica a cualquier dependencia que delega accesibilidad.

**Vocabulario:** WAI-ARIA | APG | role | accessible name.

---

## 3.2 Nombres accesibles

### 3.2.1 El problema que Radix no puede resolver por vos

Para controles nativos de formulario, el `<label>` de HTML da el nombre. Para controles no nativos, WAI-ARIA define como calcular un **nombre accesible**.

Radix provee **`Label`**, "disenado para trabajar con muchos de nuestros controles" - y aclara el limite: **"en ultima instancia, depende de vos proveer esos labels de modo que los usuarios tengan el contexto apropiado"**.

`Label.Root` es un wrapper del `label` nativo:

| Prop | Para que |
|---|---|
| `htmlFor` | Asociar por id (sin anidar) |
| `asChild` | Componer con otro elemento |

Dos features concretas y no obvias: **evita la seleccion de texto al doble click** sobre el label (molestia clasica) y **soporta controles anidados**.

**Y un limite importante, textual de la doc:** *"For your own custom controls to work correctly, ensure they use native elements such as `button` or `input` as a base."* O sea: `Label` garantiza el enlace **si tu control es nativo o se apoya en uno**. Un `div` con `role="button"` no queda cubierto por la garantia.

### 3.2.2 Title / Description / VisuallyHidden

En modales, el nombre no viene de un `label` sino del contenido:

- **`Dialog.Title` / `AlertDialog.Title`** - "nombre accesible que se anuncia cuando el dialog se abre". Radix **maneja los anuncios de screen reader** con `Title` y `Description`.
- **`Dialog.Description`** - descripcion opcional. Para omitirla se quita el part y se pasa `aria-describedby={undefined}` al `Content` (si se deja el part vacio, queda una referencia a la nada).
- **`VisuallyHidden`** - oculta **visualmente** sin sacar del arbol de accesibilidad. Dos usos: dar nombre a un boton de solo icono, y envolver el `Title` cuando el diseño no muestra titulo (`<VisuallyHidden asChild>`, en vez del `Title`).

La doc de `VisuallyHidden` lo posiciona explicitamente como **alternativa a `aria-label` / `aria-labelledby`**. Es el criterio practico: cuando el nombre tiene que existir y no puede verse, `VisuallyHidden` suele ganarle a `aria-label`, porque **el texto vive en el DOM** (traducible, testeable, visible para otras herramientas) en vez de quedar en un atributo suelto.

---

## 3.3 Teclado

### 3.3.1 Que espera cada patron

No es una tabla universal: cada patron APG define sus teclas.

- **Dialog / AlertDialog:** `Esc` **cierra solo** (feature declarada de Radix).
- **Popover:** `Esc` cierra; foco gerenciado.
- **Tooltip:** abre con **foco o hover**, cierra al activar el trigger o con `Esc`.
- **Select:** la feature mas cargada - **navegacion por teclado completa**, **typeahead**, y soporte **RTL**.

### 3.3.2 Que cubre Radix y que no

Radix: navegacion por teclado de la **estructura del componente** (moverse dentro del select, entre tabs, atrapar el tab en un modal). Eso es lo dificil y es lo que trae hecho.

Fuera de Radix: todo lo que depende del **layout de la pagina** - el orden de tabulacion de tu composicion, los `tabIndex` manuales, y garantizar que no haya **elementos enfocables dentro de un contenedor oculto** (ver 3.5).

**Vocabulario:** typeahead | focus trap | tab order.

---

## 3.4 Foco

### 3.4.1 El comportamiento

La doc explica **por que** importa: cuando algo cambia como resultado de una interaccion, conviene **mover el foco** con la interaccion para que el siguiente tab stop sea logico. Y para screen readers, mover el foco suele producir un **anuncio** que comunica el contexto nuevo - lo que a su vez depende de que el nombre este bien.

Lo que Radix hace por defecto:

- **Dialog modal: foco atrapado automaticamente** dentro del modal.
- **AlertDialog: foco automaticamente atrapado**, y al abrirse lo mueve al boton **Cancel** para anticipar la respuesta. Es el ejemplo que da la doc de "movemos el foco segun la interaccion esperada".
- Los componentes **no modales** (Popover) no atrapan el foco.

### 3.4.2 Los hooks de control

`Dialog.Content` (y `Popover.Content`) exponen:

| Hook | Cuando corre | Para que |
|---|---|---|
| `onOpenAutoFocus` | al abrir, antes del foco automatico | cambiar donde cae el foco inicial (ej. al primer campo) |
| `onCloseAutoFocus` | al cerrar | decidir a donde vuelve el foco |
| `onEscapeKeyDown` | `Esc` | interceptar el cierre |
| `onPointerDownOutside` / `onInteractOutside` | click fuera | decidir si el click afuera cierra |

Estos cuatro son el punto donde la mayoria de los bugs de foco se arreglan. Y son la respuesta a la pregunta "y si el default no me sirve?": **el default es sensato, pero esta hecho para ser reemplazado**.

---

## 3.5 Donde Radix no alcanza

### 3.5.1 Lo que sigue siendo del consumidor

Lo declara la propia doc, en tres lugares distintos:

1. **Los nombres:** `Title`, `Description` y `Label` son **abstracciones**. El contenido lo pones vos. Un `Dialog.Title` vacio es un dialog sin nombre.
2. **El elemento base:** si cambias el elemento (por `asChild` a un `div`) o construis un control custom, "es tu responsabilidad que siga siendo accesible y funcional".
3. **La cobertura de teclado:** "basic keyboard support" - hay que verificar contra el APG por componente.

### 3.5.2 Lo que ningun primitive entrega

No figura en la lista de features de Radix (no es que la doc diga que no lo hace: es que **no forma parte del contrato**):

- **Contraste y color:** un primitive unstyled no puede tener opinion sobre colores. Es 100% nuestro - y es exactamente lo que verificamos a mano en TERRARIO/PLAZA (ratios calculados).
- **Orden de tabulacion del layout:** es de la composicion, no del componente.
- **Anuncios live:** no hay primitive de region live en el catalogo basico.
- **Errores de formulario:** el `aria-invalid`, el mensaje asociado y su anuncio son nuestros.
- **Jerarquia de encabezados y landmarks:** estructura del documento, no del componente.
- **Contenido y prioridad de la informacion:** que dice el texto y que se anuncia primero.

**La sintesis del nivel:** Radix se hace cargo de la **implementacion dificil y repetible** (foco, teclado, roles, anuncios de modal). El **contenido, la semantica de tu producto y la verificacion** siguen siendo nuestros. No es un atajo: es **una linea divisoria mas alta**.

---

## Callback: el bug de #9878 vivido desde el otro lado

Radix resuelve el foco de un modal **de verdad**: el overlay "cubre la porcion inert de la vista" y el foco queda atrapado.

Nuestro bug de ibm-products (#9878) fue lo mismo mal hecho: `getActiveStep()` buscaba `[inert]` para saber que paso estaba visible, y el componente ocultaba con `display: none`. **Asumia el mecanismo de Radix en un componente que no lo implementa.**

La leccion que conecta los dos: "oculto" no es una sola cosa. `inert` (foco + AT), `display: none` (layout + AT), `aria-hidden` (solo AT) y `visibility: hidden` (paint) son **cuatro superficies distintas**. El codigo que asume una y recibe otra falla en silencio - sin error, sin excepcion, con el foco en otro lado.

---

## Verificacion del Nivel 3

1. Radix dice cubrir "los detalles dificiles de accesibilidad": **nombrar dos cosas que quedan explicitamente de nuestro lado**.
2. Cuando usarias **`VisuallyHidden`** en lugar de **`aria-label`**?
3. **`Dialog`** vs **`Popover`**: que cambia en el foco, y por que es una decision de accesibilidad (no solo visual)?
