# PLAN — Fase 4: Rediseño de navegación accesible (v0.9.0)

> **Fecha:** 2026-08-14
> **Autor:** Kanam (planificación y documentación)
> **Estado:** U1 completada y revisada por Agente B; **U2 completada** (2026-08-14, commit `771dabb`). Pendiente U3.
> **Fuente:** pedidos de Gonzo (2026-08-14) + mockup aprobado en `projects/kanam-story/preview-layout-v090.html` + patrón de Sudowrite/NovelCrafter.
> **Visión:** NO es solo corregir bugs — es un **rediseño donde UI y a11y están integradas desde el diseño**, no como capa final.

---

## Objetivo

Rediseñar la navegación de Kanam Story con **accesibilidad integrada**:
1. **Secciones apiladas en el área central** (como Sudowrite/NovelCrafter) en vez de tabs del panel derecho.
2. **Estructuras opcionales** — el usuario genera desde el outline sin pre-crear capítulos/escenas.
3. **UI + a11y como requisito de diseño** — cada unidad considera WCAG (navegación por teclado, foco visible, roles ARIA, contraste, landmarks) desde el mockup, no al final.

## Principio rector: a11y integrada (no agregada)

Cada unidad de la Fase 4 debe cumplir desde el diseño:

### Navegación y teclado
- **Navegación por teclado completa**: todos los controles operables con Tab/Shift+Tab, sin trampas de foco.
- **Foco visible** claro (no solo el outline por defecto del browser) — `:focus-visible` con un anillo visible y contraste adecuado.
- **Orden de tabulación lógico** que sigue la estructura visual.
- **Skip link** para saltar al contenido principal.

### Landmarks y semántica
- Usar landmarks HTML (`<nav>`, `<main>`, `<aside>`, `<header>`) con `aria-label` descriptivos.
- **Navegación del sidebar** como `<nav aria-label="Secciones">` con `aria-current` en la sección activa.
- **Scrollspy** (U2) con `aria-current="true"` en el item activo — no solo cambio visual.

### Secciones apiladas (el nuevo layout)
- Cada sección apilada como `<section aria-labelledby="...">` con su heading.
- **Colapsar/expandir** (acordeón) con `aria-expanded` y `aria-controls`, operables por teclado (Enter/Espacio).
- Encabezados con jerarquía correcta (h1 → h2 → h3) sin saltos.

### Interacciones
- **Chat sticky** con el input correctamente etiquetado (`aria-label`) y foco gestionado.
- **Generar escena desde outline**: los botones con `aria-label` descriptivo, feedback de éxito/error anunciado (live region si aplica).
- **Onboarding por plantillas**: opciones como radio group accesible o lista con navegación por teclado.
- **Contraste WCAG AA** en todo el rediseño (texto sobre superficies, botones primarios, focus ring).

### Validación AT manual (skill `a11y-at-validation`)
- Cualquier cambio que toque anuncio de screen reader (roving focus, `aria-activedescendant`, live regions, labels dinámicos) requiere **validación manual con VoiceOver/NVDA**, no solo tests.
- Los tests verdes NO son suficientes cuando cambia lo que el AT anuncia.

---

## Roles de los agentes

| Agente | Entorno | Rol |
|---|---|---|
| **Agente A** | VS Code | Desarrolla unidades impares. Revisa las pares de B. |
| **Agente B** | ZCode | Desarrolla unidades pares. Revisa las impares de A. |
| **Orquestador** | Kanam | Planifica, coordina, documenta, cierra (release v0.9.0). |

**Regla de oro:** cada agente, antes de empezar su unidad, revisa y corrige la unidad que el otro acaba de terminar. Nadie avanza sin validar lo anterior. Cada unidad = commit atómico + push. **La a11y se revisa en el cross-review, no al final.**

---

## Estrategia de ejecución (decisión del orquestador, 2026-08-14)

**Correr en CADENA (lineal), un agente a la vez** — NO en paralelo. Mismo pipeline que la Fase 3 (U1-U8 en cadena con cross-review).

### Por qué NO en paralelo

La Fase 4 tiene **dependencias fuertes** entre unidades (a diferencia de B1-B7 que eran independientes):
- **U1 (layout) es la base** — U2-U7 no pueden empezar sin el nuevo layout de secciones apiladas montado.
- **U2, U3** dependen de U1 (scrollspy/colapso y renombrado/estilos operan sobre el layout nuevo).
- **U4-U7** dependen de U1 (outline, onboarding, creación y chat viven dentro del layout nuevo).
- **U8** es el cierre (depende de todo).

### Por qué en cadena

1. **Dependencias fuertes** — en paralelo, el agente que espera por U1 se bloquea o asume un layout que no existe.
2. **Cross-review integra la a11y** — en cadena, cada agente revisa la a11y de la unidad anterior antes de seguir (visión de a11y integrada).
3. **Sin conflictos de archivos** — en paralelo, dos agentes tocando `globals.css`/`store.tsx`/layout chocarían. En cadena, uno a la vez.
4. **La Fase 3 lo validó** — el pipeline en cadena U1-U8 funcionó y atrapó bugs reales.

### Excepción considerada (no adoptada)

U2 y U3 son ambas post-U1 y tocan archivos distintos (U2: scrollspy/acordeón; U3: renombrado/estilos). **Podrían ir en paralelo** después de U1 para acelerar. Pero se mantienen en cadena para preservar el cross-review limpio y evitar que el orquestador tenga que coordinar dos agentes a la vez. Si en la práctica U1 queda sólida y se quiere acelerar, se puede reconsiderar.

### Flujo de ejecución

```
U1 (A) → B REVISA U1 + U2 (B) → A REVISA U2 + U3 (A) → B REVISA U3 + U4 (B) →
A REVISA U4 + U5 (A) → B REVISA U5 + U6 (B) → A REVISA U6 + U7 (A) →
B REVISA U7 + U8 (B) → Cierre (A y B revisan conjunto + orquestador hace release v0.9.0)
```

El orquestador guía: en cada paso le pasa el prompt al agente correspondiente (contexto + revisar unidad anterior + desarrollar la suya + reglas a11y).

---

## Desglose de tareas (unidades atómicas con a11y integrada)

### Feature 1 — Navegación por secciones apiladas

| Unidad | Agente | Tarea | Requisitos a11y |
|---|---|---|---|
| **U1** ✅ | A | **Refactor de layout** — eliminar tabs del `RightPanel`, montar secciones apiladas en el main. Grid 3→2 columnas. Mover contenido de los 7 paneles a secciones apiladas. | Landmarks (`<nav>`, `<main>`, `<section aria-labelledby>`), jerarquía de headings (h1→h2→h3), skip link, foco visible, orden de tabulación lógico. |
| **U2** ✅ | B | **Scrollspy + colapsar secciones** — sidebar resalta sección activa al scroll; acordeón para colapsar/expandir. | `aria-current="true"` en item activo; `aria-expanded`/`aria-controls` en el acordeón; operación por teclado (Enter/Espacio); foco gestionado al expandir. |
| **U3** | A | **Renombrar "Story Bible"→"Ajustes" + consistencia visual** — unificar estilos de secciones apiladas (card, espaciado, encabezados) según mockup. | Contraste WCAG AA en el nuevo estilo; foco visible en todos los controles; labels descriptivos. |

### Feature 2 — Estructuras opcionales

| Unidad | Agente | Tarea | Requisitos a11y |
|---|---|---|---|
| **U4** | B | **Generar escena desde outline** — botón por beat → crea escena → abre editor. Lógica pura testeable en `lib/`. | Botones con `aria-label` descriptivo; feedback de éxito/error anunciado (live region polite); foco movido al editor al generar. |
| **U5** | A | **Onboarding por plantillas** — al crear proyecto: outline/biblia/plantilla de género/vacío. | Opciones como radio group accesible (`role="radiogroup"`) o lista navegable por teclado; `aria-checked`; instrucciones claras. |
| **U6** | B | **Creación en línea** — botones "＋" contextuales en cada vista. | Botones con `aria-label` (no solo "＋"), foco visible, feedback anunciado al crear. |

### Feature 3 — Co-writer y IA

| Unidad | Agente | Tarea | Requisitos a11y |
|---|---|---|---|
| **U7** | A | **Chat con input sticky + inserción contextual** — input fijo al fondo; sugerencias insertadas en la sección correcta. | Input con `aria-label`; región de mensajes como live region; foco gestionado; inserción contextual respeta el flujo de aceptación (anunciado). |

### Feature 4 — Calidad, a11y y cierre

| Unidad | Agente | Tarea | Requisitos a11y |
|---|---|---|---|
| **U8** | B | **Fix test flaky DB + tests del layout + validación a11y + cierre** — fix `beforeEach` de `db.test.ts`; tests del nuevo layout (navegación); **auditoría a11y** del rediseño; cierre. | Auditoría WCAG del layout nuevo (teclado, foco, landmarks, contraste); validación AT manual de los cambios que tocan anuncio (roving focus, live regions); corregir hallazgos. |

---

## Cierre de la Fase 4

- [ ] **Release v0.9.0** — bump de versión, CHANGELOG, tag + GitHub Release.
- [ ] **Actualizar docs** — STATUS.md, ROADMAP.md (marcar items), HANDOFF.md.
- [ ] **Verificación final** — tests, build + TS, lint 0 errores, CI verde.
- [ ] **Auditoría a11y final** — revisar que todo el rediseño cumple WCAG AA (teclado, foco, landmarks, contraste, anuncio AT).

---

## Notas para los agentes

- **El mockup aprobado** está en `projects/kanam-story/preview-layout-v090.html` — es la referencia visual de U1/U3.
- **a11y integrada**: la accesibilidad es requisito de cada unidad, se revisa en el cross-review, no al final. Usar la skill `a11y-at-validation` para validación AT manual cuando el cambio toca anuncio.
- **No romper el modelo de aceptación del chat** (propuesta → diff → aceptar/deshacer).
- **Migraciones de DB** con bump de `DB_VERSION` si se agregan campos.
- **Idioma:** UI y prompts en español; commits/PRs en inglés.
- **Cada unidad = commit atómico + push.** Dejar mensaje claro de qué se hizo y qué necesita revisión.
- **Al cerrar cada unidad:** actualizar este PLAN (marcar la unidad) y el STATUS.md.
- **Patrón de lógica pura testeable:** extraer a `lib/*.ts` (sin DB/DOM) como `bibleSync.ts`, `search.ts`, `snapshots.ts`.

## Estado de la sesión previa (pendientes que entran en Fase 4)

- **Fix test flaky de DB** — el `beforeEach` de `lib/db.test.ts` quedó a medias (cambié a `deleteDatabase` + reimport; falta confirmar que no cuelga y que elimina la flakiness). → entra en U8.
- **Fix toolbar desbordado** — commit `01e523a` (nowrap + scroll) ya está; con U1 el toolbar desaparece, el fix no estorba.

---

## Bitácora de ejecución

### U1 — Agente A (2026-08-14) — commit `3437359`

**Qué se hizo:**
- Grid pasó de `280px 1fr 360px` a `280px 1fr` (2 columnas). `RightPanel.tsx` eliminado como contenedor de tabs (borrado el componente y su CSS).
- Store: `view` extendido de `'editor' | 'outline'` a `'editor' | 'outline' | 'story'` + estado `activeStorySection` (tipo `StorySectionKey` en `types/index.ts`).
- `components/StorySections.tsx`: renderiza las 7 secciones apiladas verticalmente en el main. Definiciones centralizadas en `lib/storySections.ts` (`STORY_SECTIONS`).
- Sidebar (`ProjectTree.tsx`): ahora es `<nav aria-label="Secciones">` que navega **Escritura / Outline / Historia** (7 items), con `aria-current="true"` en el item activo.
- a11y integrada: skip link (`#contenido-principal`), `<main id="contenido-principal">`, cada sección como `<section aria-labelledby>` con h2 bajo h1 "Historia", `:focus-visible` global.

**Verificación:** 244 tests, build + TS (solo 3 errores pre-existentes en `bibleSync.test.ts`/`export.test.ts`, fuera del scope de U1), lint 0 errores. Verificado manualmente en browser: 2 columnas, 7 secciones apiladas con landmarks y `aria-current`, editor/outline intactos.

**Revisión por Agente B (U2):**
- U1 **aprobada sin correcciones**. a11y validada: skip link correcto (`#contenido-principal` + visible al foco), jerarquía h1→h2 intacta, landmarks presentes, `aria-current` actualizado, y `:focus-visible` global no rompe el anillo de Bootstrap (usa `outline` distinto del `box-shadow` de Bootstrap, con offset visible sobre el fondo).
- No se encontró código muerto extra (el único residuo, `rightPanelCollapsed`, queda intencionalmente en `Settings`/DB por compatibilidad).

**Pendiente de revisión (Agente A, al iniciar U3):**
1. **Renombrar título interno "Story Bible" → "Ajustes"** — la sección stacked se llama "Ajustes", pero `StoryBibleSettingsPanel` sigue pintando su propio heading "Story Bible" dentro del body. Unificar en U3.
2. **Consistencia visual de secciones apiladas** — unificar cards, espaciado, encabezados y eliminar títulos duplicados entre section heading y panel interno.
3. **Heading de OutlineView** — la vista outline no tiene h1 de página (comportamiento pre-existente); puede unificarse en U3.
4. **a11y de U3** — contraste WCAG AA, foco visible y labels descriptivos al unificar estilos.

### U2 — Agente B (2026-08-14) — commit `771dabb`

**Qué se hizo:**
- `components/StorySections.tsx`: scrollspy con `IntersectionObserver` en el `<main id="contenido-principal">`. La sección más visible en la banda superior del main actualiza `activeStorySection` del store, con lo cual el sidebar resalta el item activo y actualiza `aria-current="true"`.
- Acordeón accesible: cada h2 de sección contiene un `<button type="button">` con `aria-expanded` y `aria-controls="body-{key}"`. El cuerpo colapsa con `hidden={!open}`; al colapsar, el h2 permanece visible, preservando la jerarquía h1→h2.
- Integración sidebar↔scroll: al clickear una sección en el sidebar, `activeStorySection` cambia y un `useEffect` hace `scrollIntoView({ behavior: 'smooth', block: 'start' })`. Un `ref` distingue estos cambios de los generados por scrollspy para evitar bucles.
- CSS (`app/globals.css`): estilos `.stack-section-toggle` y `.stack-chevron`; foco visible hereda el anillo global `:focus-visible`.

**Verificación:** 244 tests, build + TS (3 errores pre-existentes en tests, fuera de scope), lint 0 errores. Chequeo manual en browser: scrollspy responde al subir/bajar (Brújula/Biblia/Co-writer), acordeón colapsa/expande con `aria-expanded` y body `hidden`, Space opera el toggle, jerarquía de headings intacta.

**Pendiente de revisión (Agente A, U3):**
- Renombrar/eliminar el título interno "Story Bible" dentro de la sección "Ajustes".
- Consistencia visual de cards y espaciado; heading h1 para OutlineView.
