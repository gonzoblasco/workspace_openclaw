# PLAN — Fase 4: Navegación por secciones + Estructuras opcionales (v0.9.0)

> **Fecha:** 2026-08-14
> **Autor:** Kanam (planificación y documentación)
> **Estado:** Planificado. Pendiente de ejecución por Agentes A y B.
> **Fuente:** pedidos de Gonzo (2026-08-14) + mockup aprobado en `projects/kanam-story/preview-layout-v090.html` + patrón de Sudowrite/NovelCrafter.

---

## Objetivo

Rediseñar la navegación de Kanam Story para que las secciones de la historia se muestren **apiladas en el área central** (como Sudowrite/NovelCrafter) en vez de como tabs del panel derecho, y hacer que las **estructuras (capítulos/escenas) sean opcionales** — el usuario puede generar desde el outline y que se cree la escena automáticamente. Además, pulir la UI (renombrar "Story Bible", consistencia visual) y cerrar deuda técnica (test flaky, tests del nuevo layout).

## Alcance (15 items en 5 ejes — "arreglar todo")

### Eje 1 — Navegación y layout
1. **Secciones apiladas en el main** — las secciones (Co-writer, Brainstorm, Personajes, Mundo, Biblia, Ajustes) apiladas verticalmente con scroll, en vez de tabs del panel derecho. El panel derecho desaparece como contenedor de tabs.
2. **Scrollspy** — al hacer scroll por las secciones apiladas, el sidebar resalta la sección activa.
3. **Colapsar secciones individuales** — cada sección apilada puede colapsarse/expandirse (acordeón).

### Eje 2 — Estructuras opcionales
4. **Generar escena desde outline** — ponés beats/estructura → "generar escena" → abre el editor con la escena generada (sin pre-crear capítulos/escenas a mano).
5. **Onboarding por plantillas** — al crear un proyecto: empezar por (a) outline en blanco, (b) biblia en blanco, (c) plantilla de género (thriller/romance/sci-fi con estructura sugerida), (d) proyecto vacío libre. No obliga a nada.
6. **Creación en línea** — botones "＋" contextuales en cada vista (en biblia crear personaje directo, en outline crear beat, etc.), sin pasar por el árbol.

### Eje 3 — Co-writer y IA
7. **Chat con input sticky** — el Co-writer como sección apilada pero con el input fijo al fondo (no queda en medio del scroll).
8. **Inserción contextual desde el chat** — las sugerencias del co-writer se insertan en la sección correcta (personaje → Personajes, beat → outline) con el flujo de aceptación.

### Eje 4 — Pulido de UI
9. **Renombrar "Story Bible" → "Ajustes"** — resuelve la confusión con "Biblia".
10. **Consistencia visual** — unificar estilos de las secciones apiladas (mismo card, espaciado, encabezados) para que se vean como un sistema.

### Eje 5 — Calidad y deuda técnica
11. **Fix test flaky de DB** — el `beforeEach` de `lib/db.test.ts` (race condition con el singleton; quedó a medias en la sesión del 2026-08-14).
12. **Tests del nuevo layout** — jsdom + testing-library para la navegación de secciones apiladas (cambio estructural = riesgo alto).
13. **Extraer lógica de "generar escena desde outline" a función pura testeable** — el patrón de `bibleSync.ts`/`search.ts`/`snapshots.ts`.

---

## Roles de los agentes

| Agente | Entorno | Rol |
|---|---|---|
| **Agente A** | VS Code | Desarrolla unidades impares. Revisa las pares de B. |
| **Agente B** | ZCode | Desarrolla unidades pares. Revisa las impares de A. |
| **Orquestador** | Kanam | Planifica, coordina, documenta, cierra (release v0.9.0). |

**Regla de oro:** cada agente, antes de empezar su unidad, revisa y corrige la unidad que el otro acaba de terminar. Nadie avanza sin validar lo anterior. Cada unidad = commit atómico + push. Revisión multi-ronda para calidad.

---

## Desglose de tareas (unidades atómicas)

### Feature 1 — Navegación por secciones apiladas (Eje 1 + 4)

| Unidad | Agente | Tarea | Detalle |
|---|---|---|---|
| **U1** | A | **Refactor de layout** | Eliminar las tabs del `RightPanel` y montar las secciones apiladas en el main (item 1). Crear un contenedor de "vistas" que alterna entre Editor / Outline / Historia (secciones apiladas). Mover el contenido de los 7 paneles (Chat, Brainstorm, Characters, World, Bible, Settings, Compass) a secciones apiladas. El grid pasa de 3 columnas a 2 (sidebar + main). |
| **U2** | B | **Scrollspy + colapsar secciones** | Scrollspy en el sidebar (resalta la sección activa al hacer scroll, item 2) + acordeón para colapsar/expandir cada sección apilada (item 3). |
| **U3** | A | **Renombrar + consistencia visual** | Renombrar "Story Bible" → "Ajustes" en la navegación (item 9). Unificar estilos de las secciones apiladas (item 10): mismo card, espaciado, encabezados. Ajustar `globals.css` (`.stack-section`, etc.) con los estilos del mockup aprobado. |

### Feature 2 — Estructuras opcionales (Eje 2)

| Unidad | Agente | Tarea | Detalle |
|---|---|---|---|
| **U4** | B | **Generar escena desde outline** | En `OutlineView`, agregar botón "Generar escena" por beat → crea la escena (sin pre-crear capítulo a mano, o creando el capítulo si no existe) → `selectScene` + `setView('editor')` (item 4). Extraer la lógica a función pura testeable en `lib/` (item 13, patrón existente). |
| **U5** | A | **Onboarding por plantillas** | Al crear proyecto, ofrecer empezar por: outline en blanco, biblia en blanco, plantilla de género (con estructura sugerida), o proyecto vacío libre (item 5). Adaptar `NewProjectModal`. |
| **U6** | B | **Creación en línea** | Botones "＋" contextuales en cada vista (biblia → crear personaje directo, outline → crear beat, etc.), sin pasar por el árbol (item 6). |

### Feature 3 — Co-writer y IA (Eje 3)

| Unidad | Agente | Tarea | Detalle |
|---|---|---|---|
| **U7** | A | **Chat con input sticky + inserción contextual** | El Co-writer apilado con input fijo al fondo (item 7). Las sugerencias del co-writer se insertan en la sección correcta (personaje → Personajes, beat → outline) con el flujo de aceptación (item 8). |

### Feature 4 — Calidad y cierre (Eje 5)

| Unidad | Agente | Tarea | Detalle |
|---|---|---|---|
| **U8** | B | **Fix test flaky + tests del layout + cierre** | Fix del `beforeEach` de `lib/db.test.ts` (race condition, item 11). Tests del nuevo layout (navegación de secciones apiladas, item 12). Verificación final (build + tests + lint + CI). |

---

## Cierre de la Fase 4

- [ ] **Release v0.9.0** — bump de versión, CHANGELOG, tag + GitHub Release.
- [ ] **Actualizar docs** — STATUS.md, ROADMAP.md (marcar items), HANDOFF.md.
- [ ] **Verificación final** — tests, build + TS, lint 0 errores, CI verde.

---

## Notas para los agentes

- **El mockup aprobado** está en `projects/kanam-story/preview-layout-v090.html` — es la referencia visual de la U1/U3.
- **No romper el modelo de aceptación del chat** (propuesta → diff → aceptar/deshacer).
- **El editor ya usa TipTap/StarterKit** — no reinventar.
- **Migraciones de DB** con bump de `DB_VERSION` si se agregan campos.
- **Idioma:** UI y prompts en español; commits/PRs en inglés.
- **Cada unidad = commit atómico + push.** Dejar mensaje claro de qué se hizo y qué necesita revisión.
- **Al cerrar cada unidad:** actualizar este PLAN (marcar la unidad) y el STATUS.md.
- **Patrón de lógica pura testeable:** extraer a `lib/*.ts` (sin DB/DOM) como `bibleSync.ts`, `search.ts`, `snapshots.ts`.

## Estado de la sesión previa (pendientes que entran en Fase 4)

- **Fix test flaky de DB** — el `beforeEach` de `lib/db.test.ts` quedó a medias (cambié a `deleteDatabase` + reimport; falta confirmar que no cuelga y que elimina la flakiness). → entra en U8.
- **Fix toolbar desbordado** — commit `01e523a` (nowrap + scroll) ya está; con U1 el toolbar desaparece, el fix no estorba.
