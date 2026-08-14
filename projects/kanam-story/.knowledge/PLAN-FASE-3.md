# PLAN — Fase 3: Editor refinado + Sincronización Biblia↔tabs

> **Fecha:** 2026-08-13
> **Autor:** Kanam (planificación y documentación)
> **Estado:** Planificado. Pendiente de ejecución por Agentes A y B.
> **Fuente:** pedidos de Gonzo (2026-08-13) + captura de Sudowrite (área de texto refinada).

---

## Objetivo

Dos features prioritarias que Gonzo pidió antes de tocar el resto del backlog:

1. **Área de texto refinada** — barra de formato + selección contextual IA en el editor. El usuario debe poder escribir, copiar/pegar y editar libremente (no todo generado por IA).
2. **Sincronización Biblia ↔ tabs** — lo generado en la Biblia de la Historia se duplica automáticamente en las tabs Personajes y Mundo.

---

## Roles de los agentes

| Agente | Entorno | Rol |
|---|---|---|
| **Agente A** | VS Code | Desarrolla unidades impares (1, 3, 5...). Revisa las unidades pares de B. |
| **Agente B** | ZCode | Desarrolla unidades pares (2, 4, 6...). Revisa las unidades impares de A. |

**Regla de oro del pipeline en cadena:** cada agente, antes de empezar su unidad, **revisa y corrige** la unidad que el otro acaba de terminar. Nadie avanza sin que el otro haya validado lo anterior. Así "cada cual corrige lo anterior y sigue con lo suyo".

---

## Pipeline de revisión cruzada (el flujo)

```
Unidad 1 (A desarrolla)
   ↓
Unidad 2 (B REVISA la 1 + desarrolla la 2)
   ↓
Unidad 3 (A REVISA la 2 + desarrolla la 3)
   ↓
Unidad 4 (B REVISA la 3 + desarrolla la 4)
   ↓
Unidad 5 (A REVISA la 4 + desarrolla la 5)
   ↓
Unidad 6 (B REVISA la 5 + desarrolla la 6)
   ↓
Unidad 7 (A REVISA la 6 + desarrolla la 7)
   ↓
Unidad 8 (B REVISA la 7 + desarrolla la 8)
   ↓
Cierre (A y B revisan el conjunto + release)
```

**Cada unidad = commit atómico.** Al terminar una unidad, el agente pushea y deja un mensaje claro de qué hizo y qué necesita revisión. El otro agente revisa (con `git log`/`git diff`), corrige si hace falta, y continúa.

---

## Desglose de tareas (unidades atómicas)

### Feature 1 — Área de texto refinada (editor)

| Unidad | Agente | Tarea | Detalle |
|---|---|---|---|
| **U1** | A | **Barra de formato básica** | Agregar barra de formato al `Editor.tsx`: negrita, cursiva, subrayado, tachado, deshacer/rehacer. Usar los comandos de TipTap (`editor.chain().focus().toggleBold().run()`, etc.). StarterKit ya soporta estos marks; solo falta exponerlos en la UI. ✅ **Hecho 2026-08-13 (commit `b5e9484`).** B/I/S + undo/redo. Subrayado: StarterKit NO lo trae; `@tiptap/extension-underline` está en node_modules pero no en package.json → botón U deshabilitado, lo agrega B en U2. |
| **U2** | B | **Listas + headings + enlaces** | Completar la barra: listas (viñetas/numeradas), H1/H2/H3, enlaces. ✅ **Hecho 2026-08-13 (commit `4c10c8f`).** Subrayado habilitado (StarterKit 3.27.1 YA lo incluye), listas viñetas/numeradas, H1-H3 (config `levels: [1,2,3]`), enlaces (`setLink`/`unsetLink`). **Revisado por A en U3:** correcto, no hizo falta instalar nada. (Nota: A intentó registrar `Underline`/`Link` explícitamente en `4dbe1ba` pero era duplicado — StarterKit ya los provee; revertido en `7bbf398`.) |
| **U3** | A | **Selección contextual IA** | Al seleccionar texto en el editor, mostrar un indicador flotante (como el círculo azul de Sudowrite) que conecte la selección con las herramientas de IA existentes (Write/Rewrite/Describe/Expand). Reusar la lógica de `runAI` que ya existe. ✅ **Hecho 2026-08-13 (commits `4dbe1ba` + `7bbf398`).** Indicador flotante con contador de palabras + Rewrite/Describe, reusa `runAI`. Se oculta al deseleccionar o click fuera. **Revisado por B (U4): correcto, sin bugs.** |
| **U4** | B | **Contador de palabras seleccionadas + polish** | Mostrar "Highlighted words: N" cuando hay selección (como Sudowrite). Ajustar estilos de la barra de formato y del indicador contextual. Verificar que copiar/pegar/editar libre funciona sin romper el autosave. ✅ **Hecho 2026-08-14 (commit `58369fb`).** Contador preciso (multilínea) + polish de estilos (`.format-bar` flex-wrap, contador del indicador). Copiar/pegar/editar verificado: no rompe autosave. **Revisado por A (U5): correcto, sin bugs.** (Nota menor: la transición de opacidad del indicador es inefectiva porque el elemento se desmonta del DOM al ocultarse — no deja fantasma, solo no hay fade-out. No bloquea.) |

### Feature 2 — Sincronización Biblia ↔ tabs

| Unidad | Agente | Tarea | Detalle |
|---|---|---|---|
| **U5** | A | **Auto-import de personajes** | Al regenerar la Biblia, detectar personajes y crearlos/actualizarlos automáticamente en la tab Personajes (con marca "de biblia"). Reusar `previewBibleCharacters` + `importCharactersFromBible` del store. Sin duplicar entradas existentes (dedupe por nombre). ✅ **Hecho 2026-08-14 (commit `82de211`).** `syncCharactersFromBible` en el store: dedupe por nombre (case-insensitive), solo toca personajes con `source === 'biblia'` (no pisa manual), rellena solo campos vacíos. Se llama tras regenerar la Biblia en `StoryBiblePanel`. Mensaje "Sincronizados N nuevos y M actualizados". **Revisado por B (U6): bug de orden corregido** — el sync corría ANTES de regenerar (sincronizaba la biblia vieja); ahora corre después y lee la biblia fresca de la DB. |
| **U6** | B | **Auto-import de mundo** | Ídem para el mundo → tab Mundo. Reusar `previewBibleWorld` + `importWorldFromBible`. Dedupe por nombre. ✅ **Hecho 2026-08-14 (commit `49501c9`).** `syncWorldFromBible` en el store (mismo patrón que U5): dedupe por nombre, marca `source: 'biblia'`, solo toca entidades `source === 'biblia'`, rellena `description` vacía. Se llama tras regenerar junto a la de personajes. Mensaje de sincronización de mundo. |
| **U7** | A | **Sincronización bidireccional + no pisar manual** | Si la Biblia se regenera, las tabs reflejan cambios sin pisar ediciones manuales del usuario. Preservar el modelo de aceptación: los cambios automáticos deben ser revisables (marca "de biblia" + opción de revertir). |
| **U8** | B | **Tests + integración** | Tests de la sincronización (dedupe, no pisar manual, marca "de biblia"). Verificar que el flujo completo funciona end-to-end. |

---

## Cierre de la Fase 3

- [ ] **Release v0.7.0** — bump de versión, CHANGELOG, tag + GitHub Release.
- [ ] **Actualizar docs** — STATUS.md, ROADMAP.md (marcar items), HANDOFF.md.
- [ ] **Verificación final** — 155+ tests, build + TS, lint 0 errores, CI verde.

---

## Notas para los agentes

- **No romper el modelo de aceptación del chat** (propuesta → diff → aceptar/deshacer).
- **El editor ya usa TipTap/StarterKit** — el formato existe a nivel de extensión; solo falta exponerlo en la UI. No reinventar.
- **La sincronización Biblia↔tabs ya tiene la base** — el bridge manual (Detectar → Importar) existe en `StoryBiblePanel.tsx`; hay que automatizarlo, no construirlo de cero.
- **Migraciones de DB** con bump de `DB_VERSION` si se agregan campos.
- **Idioma:** UI y prompts en español; commits/PRs en inglés.
- **Cada unidad = commit atómico + push.** Dejar mensaje claro de qué se hizo y qué necesita revisión.
- **Al cerrar cada unidad:** actualizar este PLAN (marcar la unidad) y el STATUS.md.
