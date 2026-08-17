# LEARNINGS — kanam-story

## 2026-08-16 — U3 chat-assisted global outline (v0.10.0 → v0.10.2)

CONTEXT: Implementing a chat-assisted global outline replacement where the agent proposes a full new chapter+beat structure.

REFLECTION: I initially wanted to avoid touching existing scenes, assuming an outline replacement could be pure metadata. The DB schema and `chaptersDB.delete` cascade proved otherwise: deleting a chapter also deletes its scenes. To preserve manuscript, I had to explicitly orphan scenes (`chapterId: ''`) before deleting old chapters.

LESSON: When an action crosses entity boundaries (chapters → scenes), check cascade behavior in the DB layer early. Pure-state undo also needs key preservation; use `put` with original ids instead of `create` when restoring snapshots.

BIASES DETECTED: Anchoring on "don't touch scenes" delayed the cascade check. The constraint came from the data model, not from user intent, and should have been validated sooner.

## 2026-08-16 — Self-review U4 + botones (v0.11.1 → v0.11.2)

CONTEXT: Después de cerrar U4 y v0.11.1, hicimos un code review propio y revisamos la deuda técnica.

FINDINGS:
1. `OutlineView` definía `orphanScenes` como "escenas sin beats", no "escenas sin capítulo". El panel global de huérfanas mostraba escenas que tenían capítulo pero no beat, duplicando el concepto local de `ChapterSection`. Corregido a `chapterId === ''`.
2. `btn-outline-danger` (Bootstrap default) sobre fondo blanco del tema claro no cumple WCAG AA (2.78:1). Es un problema global, no solo del outline; hay que decidir si se customiza el danger o se acepta el default de Bootstrap.
3. Botones de icono con label (`btn-icon-label`) no tenían `type="button"` explícito. Agregado.
4. El test `lib/db.test.ts` que estaba marcado como "flaky / beforeEach a medias" ahora pasa establemente en 5 corridas; probablemente se resolvió en commits anteriores. Verificación directa lo confirma.

LESSON: Nombres como "orphan" son cargados; hay que validar la condición real (`chapterId === ''` vs `beats.length === 0`) antes de renderizar UI. Un self-review inmediatamente después de mergear atrapa estos errores de modelado.

BIASES DETECTED: Reutilicé el nombre "orphan" sin verificar la condición exacta, asumiendo que coincidía con el caso post-`replace_outline`.

## 2026-08-16 — Beats desde manuscrito del autor + ids de beats (v0.12.1)

CONTEXT: Gonzo pidió poder generar beats desde su manuscrito escrito a mano, idealmente vía chat: el co-writer lee el texto y extrae beats respetando las ideas (sin imponer orden/ritmo).

REFLECTION: El chat ya tenía `add_beat`/`update_beat` y veía el manuscrito, pero truncado a 500 chars por escena, y el contexto de beats NO incluía ids de beats. El smoke test con Ollama reveló el bug: el modelo usó `beatId: "s1"` (id de la escena) porque el contexto mostraba ids de escena pero no de beats. Al exponer `(id: b1, ...)` en el contexto de beats, las acciones por beatId apuntan a beats reales.

LESSON: Para que el modelo genere acciones con ids correctos, TODOS los ids referenciables (escenas, beats, personajes, capítulos) deben estar visibles en el contexto con un formato consistente. Un smoke test end-to-end con el modelo real es indispensable para detectar esto — los tests unitarios del parser no ven el output del modelo.

BIASES DETECTED: Asumí que el contexto ya exponía los ids de beats porque exponía los de escenas. La falta de smoke test del flujo completo permitió que el bug pasara.

VALUE: El smoke test con Ollama local (deepseek-v4-flash) validó que el agente extrae beats fieles al texto del autor, reestructurando sin inventar contenido.

## 2026-08-16 — Sidebar de co-writer con contexto acotado (v0.13.0)

CONTEXT: Gonzo pidió un sidebar expandible desde la página de escritura para chatear con la historia, personajes, lo ya escrito y la escena actual, y que actúe como agente con manos PERO sin modificar otras escenas.

REFLECTION: En vez de una tercera columna fija (comprimiría el editor), hice un overlay deslizable. Para "no modifica otras escenas" no basta con limitar la UI — hay que limitar el CONTEXTO del agente: si solo ve la escena activa + biblia + personajes + mundo + outline del capítulo actual (helper puro `buildSceneContext`), no puede referenciar ni editar otras escenas. El `ChatPanel` se reutilizó con un prop `contextScope` y default 'full' (no rompe el chat existente).

LESSON: "No modificar X" en un agente con manos se resuelve limitando lo que el agente ve en el contexto, no solo restringiendo la UI. Un agente no puede editar lo que no ve. Reusar componentes con un prop de scope (default preserva el comportamiento) evita duplicar el panel de chat.

BIASES DETECTED: Pensé primero en una columna fija de grid; el overlay es mejor porque no comprime el área de escritura. El contexto acotado es la pieza clave que satisface el requisito real.

## 2026-08-17 — Sesión larga de features: chat, editor, export, continuidad (v0.13.1 → v0.16.0)

CONTEXT: Sesión extensa acumulando features sobre Kanam Story: fixes de chat/editor, export, notas de continuidad. Muchos bugs llegaron de reportes de Gonzo probando la app real.

REFLECTION:
1. **Editor no se refresca al aceptar cambios.** El efecto de sync dependía de `scene.id`; un `rewrite_scene` cambia el contenido sin cambiar el id. Fix: depender también de `scene.content`. Lección: cuando una vista muestra una entidad, sync por TODAS las propiedades que pueden cambiar externamente, no solo el id.
2. **Contenido del agente "todo de corrido".** El agente devuelve texto plano/markdown con `\n\n`, pero TipTap espera HTML. Guardarlo crudo lo muestra como un párrafo gigante. Fix: `ensureHtml` (si es HTML lo deja, si no lo convierte). Lección: el modelo y el editor tienen formatos distintos; hay que normalizar en la frontera.
3. **Sidebar con input flotando.** `.chat-panel` tenía altura fija (`min(58vh, 520px)`) pensada para otra sección. Fix: `height: 100%` en contexto sidebar. Lección: componentes reutilizados en contextos distintos pueden necesitar overrides de layout por contexto.
4. **Mocks de tests y firma cambiante.** Cambiar `applyContentActions` a `{undo, failed}` rompió mocks; hay que tiparlos explícitamente (`vi.fn<...>()`) o se infiere `never[]`.

LESSON: Los reportes de Gonzo probando la app real son la fuente más rica de bugs reales (formato, layout, sync). Un smoke test con el modelo real y una prueba manual de UX valen más que tests unitarios para estos casos. Verificar siempre la frontera de formatos (agente → editor) y los contextos de reutilización de componentes.

BIASES DETECTED: Asumí que el editor se refrescaría solo con el cambio de id; asumí que el contenido del agente ya era HTML; asumí que la altura fija del chat servía para todos los contextos. Los tres eran supuestos incorrectos sobre la frontera entre el modelo, el editor y la UI.

## 2026-08-17 — a11y, mobile, PWA, export, co-writer U5+ y roles especializados

CONTEXT: Sesión extensa cerrando el bloque de features: diálogos accesibles, responsive mobile, PWA con Serwist, polish de export, acciones nuevas del co-writer y roles especializados (Plot Doctor, Consistency Checker).

REFLECTION:
1. **Loop sin progreso.** Me trabé repitiendo el mismo grep sin avanzar (Gonzo me avisó "creo te rompiste"). Lección: cuando un comando se repite sin output nuevo, parar y resetear el enfoque, no reintentar igual. El síntoma de un loop es la repetición idéntica; la acción correcta es cambiar de estrategia.
2. **CI usa ESLint, no solo Biome.** Los componentes nuevos pasaban Biome (linter del pre-commit local) pero CI corre `eslint` con reglas de React (react-hooks/refs, react-hooks/purity). Los errores: `useRef(Math.random()...).current` accede a refs en render + llama función impura; `useState`+`useEffect(setState)` causa renders en cascada. Fix: `useId()` y input no controlado (`defaultValue`). Lección: correr el linter del CI localmente antes de pushear, no solo el del pre-commit.
3. **Serwist con Turbopack usa Route Handler, no plugin webpack.** `@serwist/next` no soporta Turbopack; `@serwist/turbopack` compila el SW via un route handler en `app/serwist/[path]/route.ts` (con `params.path` — por eso la ruta necesita el `[path]` dinámico), no `swSrc`/`swDest` en next.config. El SW se sirve en `/serwist/sw.js`, no `/sw.js`. Lección: leer la doc específica de la integración (Turbopack vs webpack) antes de asumir la API.
4. **Smoke test standalone vs endpoint de la app.** `ollamaChat` llama a `/api/ollama` (proxy de la app), no directo a Ollama. Un smoke test standalone debe llamar a `http://127.0.0.1:11434/api/chat` directo. Lección: verificar la frontera de red del helper antes de usarlo fuera de la app.
5. **Roles del agente = especialización del prompt, no infraestructura nueva.** Los agentes especializados (Plot Doctor, Consistency Checker) se implementaron como variantes del prompt (`buildAgentPrompt(role)` + `buildRoleIntro`), reusando toda la infraestructura de acciones/undo/contexto. No se duplicó nada. Lección: cuando una "feature" es solo un cambio de comportamiento del LLM, es un parámetro del prompt, no un subsistema nuevo.
6. **Switch sobre union types exige cubrir todos los cases.** Al agregar `ContentAction` types, los `switch (a.type)` de `describeAction` y `applyContentActions` perdieron exhaustividad → TS exige cubrir los nuevos cases. Lección: al extender una union type, buscar todos los `switch` que la discriminan y agregar los cases (TS lo señala en los que declaran return type, pero no en los que tienen default).
7. **`update_project` no cabe en el estado puro.** El `StoryState` de `lib/actions.ts` no tiene `project` (se maneja por separado en el store). Intentar implementar `update_project` ahí rompió TS. Lo saqué de la función pura y lo dejé solo en el store. Lección: la lógica pura refleja el shape del estado; si la entidad vive fuera, su acción no pertenece a la capa pura.

VALUE: Los smoke tests de roles con Ollama real (deepseek-v4-flash:cloud) confirmaron que cada rol dirige su enfoque: co-writer analiza premisa, plot-doctor propone 3 acciones de estructura, consistency-checker audita coherencia. Validar el comportamiento del LLM con el modelo real es la única forma de confirmar que el prompt cumple su función.

BIASES DETECTED: Sunk cost en el loop del grep (seguí reintentando lo mismo); anchoring en la API de Serwist (asumí que Turbopack usa la misma API que webpack); confirmation bias al creer que Biome bastaba (CI corre ESLint).
