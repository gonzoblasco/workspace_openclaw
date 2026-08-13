# PROMPT — Agente A (VS Code) · U3: Selección contextual IA

> **Proyecto:** Kanam Story
> **Fase 3, Unidad 3 (U3)** — ver `PLAN-FASE-3.md` para el contexto completo del pipeline.
> **Fecha:** 2026-08-13

---

## Tu tarea (U3) — dos partes

1. **REVISAR la U2** (barra de formato completa, commit `4c10c8f` del Agente B). Corregir si hace falta.
2. **DESARROLLAR la U3**: **selección contextual IA** — al seleccionar texto en el editor, mostrar un indicador flotante (como el círculo azul de Sudowrite) que conecte la selección con las herramientas de IA existentes (Write/Rewrite/Describe/Expand).

## Contexto técnico (verificado)

- El editor (`components/Editor.tsx`) ya tiene la barra de IA (`ai-bar`) con botones Write/Rewrite/Describe/Expand/Dialogue/Tension, y la función `runAI(kind)` que ya usa `editor.state.selection` (líneas 190-193: `from`, `to`, `selection = editor.state.doc.textBetween(from, to, '\n')`).
- **La lógica de IA ya existe y funciona.** La U3 es el **disparador visual**: un indicador flotante que aparece cuando hay selección de texto, y que ofrece las acciones de IA relevantes.
- El editor ya tiene un listener de `transaction` (agregado en U1) que fuerza re-render — reusalo para detectar la selección.
- Referencia visual: Sudowrite muestra un **círculo azul con icono de IA** a la izquierda de la selección, y un contador "Highlighted words: N" en la barra superior.

## Qué hacer

### Parte 1 — Revisar la U2 (commit `4c10c8f`)
- `git show 4c10c8f` para ver el diff (subrayado, listas, headings H1-H3, enlaces en `Editor.tsx` + estilos en `globals.css`).
- Verificar: U funciona, listas viñetas/numeradas, H1-H3, enlaces (set/unset), estado activo correcto, autosave y barra IA intactos.
- Corregir cualquier bug. Si está bien, dejarlo y seguir.

### Parte 2 — Desarrollar la U3
1. **Detectar selección:** cuando `editor.state.selection` tiene texto seleccionado (no vacío), mostrar el indicador flotante. Reusar el listener de `transaction` existente.
2. **Indicador flotante:** un elemento posicionado cerca de la selección (o en el borde del editor) con las acciones de IA relevantes. Mínimo: **Rewrite** y **Describe** (las que actúan sobre selección). Opcional: Expand.
3. **Acciones:** al hacer click en una acción del indicador, llamar a `runAI(kind)` existente (rewrite/describe/expand). No duplicar la lógica de IA.
4. **Contador de palabras seleccionadas:** mostrar "N palabras" en el indicador (como "Highlighted words: N" de Sudowrite).
5. **Ocultar:** el indicador se oculta cuando no hay selección o al hacer click fuera.
6. **Estilos:** agregar estilos en `app/globals.css` consistentes con el diseño actual.

## Criterios de aceptación (U3)

- [ ] Al seleccionar texto, aparece el indicador flotante con acciones de IA.
- [ ] Rewrite y Describe funcionan desde el indicador (reusan `runAI`).
- [ ] Muestra el contador de palabras seleccionadas.
- [ ] Se oculta al deseleccionar o click fuera.
- [ ] No rompe la barra de IA existente ni el autosave.
- [ ] Build + TS pasan, lint 0 errores, tests existentes verdes.

## Al terminar

1. Commit atómico en inglés: `feat: add contextual AI selection indicator to editor (U3)`.
2. Push a `origin/main`.
3. Dejar mensaje claro de qué se hizo, qué se corrigió de la U2 (si algo), y qué necesita revisión.
4. Actualizar `PLAN-FASE-3.md` (marcar U3) y `STATUS.md`.

## Después de vos

**Agente B (ZCode)** revisa tu U3 y hace la U4 (contador de palabras + polish + verificar copiar/pegar/editar). No avances a la U5 hasta que B haya revisado y pusheado la U4.
