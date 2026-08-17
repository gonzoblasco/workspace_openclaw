# Plan U3 — Chat-assisted global outline generation

**Proyecto:** Kanam Story  
**Estado:** ✅ U3 completada y liberada en v0.10.0. U4 (panel de escenas huérfanas) completada y liberada en v0.11.0.  
**Dependencias:** U1 y U2 completadas. U3 implementó `replace_outline`. U4 agregó UI para escenas huérfanas resultantes.

---

## Objetivo

Permitir que el co-writer proponga, refine y aplique una estructura global de capítulos + beats directamente desde el chat, reusando el flujo de aceptación/descarte/deshacer del agente (`ContentAction` → diff → aceptar/descartar).

---

## Diseño

### 1. Nueva acción: `replace_outline`

Agregar a `ContentAction` en `types/index.ts`:

```ts
{
  type: 'replace_outline';
  chapters: { title: string; order: number }[];
  beats: { title: string; kind: BeatKind; description: string; notes: string; chapterIndex: number; position: number }[];
}
```

- `chapterIndex` es un índice en el array de capítulos propuestos (no un id, porque aún no existen en DB).
- Al aplicarse, se borran los capítulos y beats actuales del proyecto y se crean los nuevos.
- Se mantiene el modelo de deshacer: el store guarda el estado previo (chapters + beats) y puede restaurarlo.

### 2. Estado puro (`lib/actions.ts`)

Extender `StoryState` con `chapters: Chapter[]`. Implementar `case 'replace_outline'` en `applyAction`:

- Reemplaza `state.chapters` y `state.beats` por los propuestos.
- Genera ids nuevos con `crypto.randomUUID()`.
- Undo: restaura `chapters` y `beats` anteriores.

### 3. Validación (`lib/agentReply.ts`)

Extender `isValidAction` para validar:

- `chapters` es un array no vacío de objetos `{ title: string }`.
- `beats` es un array de objetos con `title`, `kind` válido, `chapterIndex` dentro de rango y `position` numérica.

### 4. Aplicación en DB (`lib/store.tsx`)

En `applyContentActions`, manejar `replace_outline` como caso especial (no pasa por `updateScene`/`updateBeat`):

1. Guardar copia de chapters y beats actuales para undo.
2. Borrar todos los beats y chapters del proyecto.
3. Crear los nuevos chapters en orden.
4. Crear los nuevos beats asociados a los nuevos chapterIds.
5. `loadProjectData(currentProject.id)`.
6. Navegar a la vista `outline` y seleccionar el primer capítulo.

### 5. Prompt del agente (`lib/agentPrompts.ts`)

Actualizar el system/context para describir la acción `replace_outline`:

- "Podés proponer un outline global completo con `replace_outline`. Incluí todos los capítulos y sus beats. Los capítulos se crearán en orden, los beats se asignarán al capítulo indicado por `chapterIndex`."
- Reglas: no mezclar con otras acciones cuando se reemplaza el outline; el usuario puede pedir ajustes antes de aceptar.

### 6. UI del chat (`ChatPanel` / `MessageRenderer`)

Renderizar una propuesta `replace_outline` como preview:

- Lista de capítulos con beats anidados.
- Botones "Aplicar estructura" / "Descartar".
- Al aceptar, aplicar vía `applyContentActions` como cualquier otra acción del chat.
- Al descartar, limpiar la propuesta.
- Si hay escenas generadas ya, advertir que el reemplazo elimina capítulos/beats existentes (no escenas; las escenas quedan huérfanas o se vinculan? Decisión: por ahora, las escenas huérfanas aparecen en el outline para vinculación manual; no borrar escenas).

### 7. Tests

- `lib/actions.test.ts`: test de `replace_outline` puro (aplica y undo).
- `lib/agentReply.test.ts`: validación de `replace_outline` válido/inválido.
- `components/ChatPanel.test.tsx` o nuevo test: el chat muestra preview y llama a `applyContentActions` al aceptar.

---

## Tareas y commits atómicos

1. `feat(types): add replace_outline ContentAction`
2. `feat(actions): implement replace_outline in pure story state`
3. `feat(agent): validate replace_outline and update prompts`
4. `feat(store): apply replace_outline to IndexedDB with undo`
5. `feat(chat): render outline replacement proposal in ChatPanel`
6. `test(chat): cover outline replacement acceptance/discard flow`
7. `docs(knowledge): update STATUS.md marking U3 complete`

---

## Criterios de aceptación

- Desde el chat, decir "reorganizá la historia en 3 actos" produce una propuesta estructurada.
- La propuesta se muestra con capítulos y beats en el chat.
- Aceptarla reemplaza el outline actual del proyecto.
- Descartarla no toca nada.
- Deshacer (botón global o por acción) restaura el outline anterior.
- 316+ tests, build + TS + lint verdes.
- a11y: preview navegable por teclado, botones con labels descriptivos, anuncio de éxito/error vía live region.

---

## U4 — Panel de escenas huérfanas (v0.11.0)

Las escenas con `chapterId: ''` tras `replace_outline` quedan huérfanas. U4 agrega un panel global "Escenas sin capítulo" en el outline que permite:

- Mover la escena a un capítulo existente (`updateScene`).
- Mover la escena y crear un beat vinculado (`updateScene` + `createBeat`).
- Abrir la escena en el editor (`selectScene` + `setView('editor')`).
- Eliminar la escena (`deleteScene` con confirmación).

### Archivos nuevos
- `components/OrphanScenesPanel.tsx`

### Archivos modificados
- `components/OutlineView.tsx`: renderiza `OrphanScenesPanel` en modo global.
- `components/OutlineView.test.tsx`: tests de movimiento, vinculación, eliminación y apertura.

### Tests
- 321 tests pasan (se agregaron 5 tests nuevos).

### a11y
- Panel como `<section aria-label="Escenas sin capítulo">`.
- Cada `<select>` y `<button>` tiene `aria-label` descriptivo.
- Iconos decorativos con `aria-hidden="true"`.
- Checklist de auditoría manual en artifact `Kanam Story U4 - Panel de escenas huérfanas - a11y audit checklist`.

---

## Notas

- No se tocan escenas existentes. Las escenas de capítulos borrados quedan "huérfanas" y aparecen en el outline para vinculación manual (flujo existente).
- El parser de U2 (`parseGlobalOutline`) se puede reusar internamente si el agente responde en markdown, pero la acción estructurada (`replace_outline`) es la fuente de verdad para el chat.
- Considerar en U3+ iteraciones: `update_outline` para cambios parciales (agregar capítulo, mover beat) sin reemplazo total.
