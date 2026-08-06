# ARIA Patterns — WAI-APG Reference

Patrones de componentes accesibles basados en WAI-ARIA Authoring Practices Guide (APG).

## Modal Dialog

```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-desc"
>
  <h2 id="dialog-title">Confirmar acción</h2>
  <p id="dialog-desc">¿Estás seguro de eliminar este elemento?</p>
  <button autofocus>Confirmar</button>
  <button>Cancelar</button>
</div>
```

**Keyboard:**
- `Tab`: cycle through focusable elements (trap inside modal)
- `Shift+Tab`: reverse cycle
- `Escape`: close modal
- Focus returns to trigger on close

## Tabs

```html
<div role="tablist" aria-label="Secciones">
  <button role="tab" aria-selected="true" aria-controls="panel-1" id="tab-1">
    Detalles
  </button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" id="tab-2">
    Envío
  </button>
</div>
<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
  Contenido del panel 1
</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  Contenido del panel 2
</div>
```

**Keyboard:**
- `ArrowLeft/ArrowRight`: switch tabs (manual activation)
- `Home`: first tab
- `End`: last tab
- `Tab`: move focus into active tabpanel

## Combobox (Autocomplete)

```html
<div role="combobox" aria-expanded="false" aria-haspopup="listbox">
  <input
    type="text"
    role="combobox"
    aria-autocomplete="list"
    aria-controls="listbox-1"
    aria-activedescendant=""
  />
  <ul role="listbox" id="listbox-1" aria-label="Sugerencias">
    <li role="option" id="opt-1">Opción 1</li>
    <li role="option" id="opt-2">Opción 2</li>
  </ul>
</div>
```

**Keyboard:**
- `ArrowDown`: open listbox, move to next option
- `ArrowUp`: move to previous option
- `Enter`: select highlighted option
- `Escape`: close listbox
- `Typing`: filter options

## Disclosure (Show/Hide)

```html
<button
  aria-expanded="false"
  aria-controls="content-1"
>
  Más información
</button>
<div id="content-1" hidden>
  Contenido expandible
</div>
```

**Keyboard:**
- `Enter/Space`: toggle visibility
- Focus stays on trigger

## Menu Button

```html
<button
  aria-haspopup="true"
  aria-expanded="false"
  aria-controls="menu-1"
>
  Acciones
</button>
<ul role="menu" id="menu-1" aria-label="Acciones">
  <li role="menuitem" tabindex="-1">Editar</li>
  <li role="menuitem" tabindex="-1">Eliminar</li>
</ul>
```

**Keyboard:**
- `Enter/Space/Space`: open menu
- `ArrowDown/ArrowUp`: navigate items
- `Enter`: activate item
- `Escape`: close menu
- Focus returns to button on close

## Tooltip

```html
<button aria-describedby="tooltip-1">Guardar</button>
<div role="tooltip" id="tooltip-1" hidden>
  Guarda los cambios actuales
</div>
```

**Keyboard:**
- Tooltip appears on focus/hover
- `Escape`: dismiss tooltip
- Tooltip must be dismissible without moving focus

## Alert

```html
<div role="alert" aria-live="assertive">
  El formulario contiene errores.
</div>
```

**Notes:**
- `role="alert"` implies `aria-live="assertive"`
- Automatically announced by screen readers
- Do not use for persistent content

## Status

```html
<div role="status" aria-live="polite">
  3 resultados encontrados.
</div>
```

**Notes:**
- `role="status"` implies `aria-live="polite"`
- For non-critical updates
- Does not interrupt current task

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [WCAG 2.2 Criteria](./wcag-22-criteria.md) — Catálogo de criterios
- [Testing Setup](./testing-setup.md) — Configuración de herramientas
