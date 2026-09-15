# Nivel 1 - El modelo mental (que es y que no es)

Capa 2 (cuaderno). Se completa a medida que avanza el estudio.
Fuente: docs oficiales de Radix Primitives (radix-ui.com/primitives), verificados 2026-09-14.

---

## 1.1 El problema que resuelve

### 1.1.1 Los patrones estan documentados, las implementaciones no sirven

Los patrones de UI comunes -accordion, checkbox, combobox, dialog, dropdown, select, slider, tooltip- **ya estan definidos** por WAI-ARIA (la spec del W3C) y la comunidad los entiende igual. El patron no es la parte dificil.

Lo que falla es la implementacion que trae la plataforma web. En palabras de la vision de Radix: son **inexistentes, pobres en funcionalidad, o no se pueden personalizar lo suficiente**. Un `<select>` nativo no se puede estilar como uno quiere; un `<dialog>` cubre poco; un tooltip no existe en HTML.

La consecuencia practica: cada dev tiene que construir el componente a mano. Y construir un combobox accesible desde cero -foco, teclado, ARIA, edge cases- es un trabajo **muy** dificil.

### 1.1.2 El resultado del hueco

Por eso la mayoria de los componentes de la web son, textual de Radix:

- **inaccesibles** (le falta ARIA, teclado o nombre)
- **poco performantes**
- **sin features clave** (lo que el patron pide y nadie implemento)

**Vocabulario:** WAI-ARIA | APG (Authoring Practices Guide) | primitive | patron de UI.

---

## 1.2 Las propiedades del diseno

Radix se define con seis propiedades. Las tres primeras son la promesa; las otras tres son como se consume.

### 1.2.1 Accessible + Unstyled + Opened

- **Accessible:** los componentes siguen los patrones WAI-ARIA donde se puede, y resuelven internamente los detalles dificiles: atributos `aria` y `role`, **manejo de foco** y **navegacion por teclado**.
- **Unstyled:** los componentes se entregan **sin estilos**. Control total del look. Se pueden estilar con cualquier solucion. Ojo: esto incluye los *estilos funcionales*, no solo los cosmeticos (ver 1.4.1).
- **Opened:** arquitectura abierta y granular. Cada **parte** del componente expone una API propia para envolverla, agregarle props, listeners o refs. No es una caja negra.

### 1.2.2 Uncontrolled + Developer experience

- **Uncontrolled por defecto:** el cableado del comportamiento es interno. No hace falta crear estado local para que funcione. Si se necesita, se puede pasar a **controlado** (ver Nivel 2).
- **DX:** API completamente tipada, consistente entre componentes, y predecible. Incluye `asChild` para controlar el elemento que se renderiza.

### 1.2.3 Adopcion incremental

Dos formas de instalar, misma libreria:

```bash
# recomendada: un solo paquete
npm install radix-ui
```
```jsx
import { Dialog, DropdownMenu, Tooltip } from "radix-ui";
```

```bash
# alternativa: primitive por primitive
npm install @radix-ui/react-dialog
```
```jsx
import * as Dialog from "@radix-ui/react-dialog";
```

El paquete unico existe para **evitar duplicacion y conflictos de version** entre primitives y es **tree-shakeable**: solo se empaqueta lo que se usa. Si se instalan por separado, la regla es actualizarlos **todos juntos**.

**Vocabulario:** tree-shaking | uncontrolled vs controlled | DX | `asChild`.

---

## 1.3 Anatomia de un primitive

### 1.3.1 Partes con rol

Un primitive no es un componente unico: es un **conjunto de partes compuestas**. El caso mas claro es Dialog:

```jsx
<Dialog.Root>          // contiene todo el estado y el contexto
  <Dialog.Trigger />   // el boton que abre

  <Dialog.Portal>      // monta el resto fuera del arbol (en <body>)
    <Dialog.Overlay /> // la capa que cubre el fondo
    <Dialog.Content>   // la ventana en si
      <Dialog.Title />       // nombre accesible (obligatorio de facto)
      <Dialog.Description /> // descripcion accesible (opcional)
      <Dialog.Close />       // el boton que cierra
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

### 1.3.2 Por que importa la composicion

Cada parte es un **punto de intervencion**. Se puede cambiar el elemento que renderiza, sus estilos, sus eventos, sin tocar la logica de accesibilidad que vive en `Root`/`Content`. Eso es el "Opened" de 1.2.1 llevado a la practica: la granularidad es lo que permite integrarlo en un design system propio en vez de aceptar un componente cerrado.

---

## 1.4 Que NO hace Radix

### 1.4.1 No estiliza - ni lo funcional

No es que "le falten colores". Un `Dialog.Overlay` **por defecto no cubre el viewport**: eso es un estilo funcional y lo tenes que escribir vos. La frase de la doc es literal: sos responsable de los estilos funcionales **y** de los de presentacion.

### 1.4.2 No es un design system

No trae look, ni tokens, ni escala tipografica, ni espaciado. No reemplaza a Tailwind ni al sistema de diseño: **es la capa de comportamiento sobre la que se construye uno**.

### 1.4.3 No adivina los nombres

Radix provee las abstracciones (`Title`, `Description`, `Label`), pero el contenido lo pones vos. Un Dialog con `Title` vacio sigue siendo un Dialog sin nombre accesible. La responsabilidad no desaparece, **se acota**.

**Vocabulario:** estilo funcional vs de presentacion | nombre accesible (accessible name).

---

## Callback util: esto ya lo tocamos

Radix describe a Dialog como una ventana que *"renderiza el contenido de abajo como inert"*. Es exactamente el mecanismo del merge de hoy en ibm-products (#9878): el bug era que el hook buscaba `[inert]` para detectar el paso visible, y el componente ocultaba con `display: none`. Radix hace de verdad lo que nuestro bug *asumia*. Distintas formas de "ocultar" (Nivel 3 lo desarrolla).

---

## Verificacion del Nivel 1

Responder estas 3, en una frase cada una:

1. Si Radix ya sigue WAI-ARIA, **que es lo que aporta** frente a leer la spec y escribir el componente?
2. Nombrar **una cosa que Radix NO hace** y que hay que hacer igual.
3. Por que la API esta partida en `Root`/`Trigger`/`Content` en vez de ser un solo componente con props?

---

## Respuestas (Gonzo no las tenia a mano - queda como material de referencia)

**1. Que aporta frente a la spec.** La spec define **que** tiene que pasar; Radix entrega **el cableado ya escrito y probado** de la parte que no se puede improvisar: foco, teclado, ARIA y los edge cases (que son muchos mas de los que uno enumera leyendo la spec). Leer la spec no te da el codigo: te da el enunciado. Aporta la implementacion dificil, no el requisito.

**2. Algo que no hace.** No estiliza **ni lo funcional**: un `Dialog.Overlay` no cubre el viewport hasta que lo escribis. (Alternativas igual de validas: no provee los nombres accesibles -`Title`/`Description`/`Label` son abstracciones, el contenido lo pones vos-, y no valida contraste, jerarquia ni orden de tabulacion del layout.)

**3. Por que esta partida en partes.** Porque **cada parte es un punto de intervencion**: se puede cambiar el elemento que renderiza, sus estilos o sus eventos sin tocar la logica de accesibilidad, que vive en `Root`/`Content`. Un componente unico con props te obligaria a aceptar su estructura; las partes permiten meter el primitive en un design system propio. Es la diferencia entre consumir un componente y componer con el.
