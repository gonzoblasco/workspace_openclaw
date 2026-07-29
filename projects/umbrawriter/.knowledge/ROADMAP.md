# ROADMAP — UmbraWriter

> Fases, sprints y tareas. Desde MVP hasta producto completo.
> Enfoque: local-first, archivos como fuente de verdad, agent-ready.

## Fase 0 — Fundación (Sprint 1-2, ~2 semanas)

**Objetivo:** Repo, server local, estructura de archivos, editor básico. Nada de IA todavía.

### Sprint 1: Scaffold + Server Local
- [ ] Crear repo (`umbrawriter` en GitHub, público, MIT)
- [ ] Configurar monorepo (packages: `web`, `server`, `core`)
- [ ] Server Hono + Bun con:
  - [ ] Sirve la UI en localhost
  - [ ] API REST para CRUD de archivos
  - [ ] Watch mode (detecta cambios en FS y notifica a UI)
- [ ] Estructura de archivos del proyecto (`umbra.json`, `bible/`, `scenes/`)
- [ ] Configurar GitHub Actions (CI: typecheck, lint, test)
- [ ] ESLint + Biome + Prettier
- [ ] Vitest configurado
- [ ] README.md + LICENSE (MIT) + CONTRIBUTING.md

### Sprint 2: UI Base + Editor Markdown
- [ ] Layout base de la web app (sidebar + main content)
- [ ] Dashboard: lista de proyectos (abrir proyecto existente o crear nuevo)
- [ ] Editor de markdown con preview en vivo
- [ ] Frontmatter parser (YAML/JSON en escenas)
- [ ] Contador de palabras
- [ ] Guardado automático en archivos

**Validation Gate:** Un escritor puede crear un proyecto, escribir markdown, y verlo renderizado. Los archivos se guardan en el FS.

---

## Fase 1 — Story Bible (Sprint 3-4, ~2 semanas)

**Objetivo:** Biblia completa + Canvas de escenas.

### Sprint 3: Story Bible UI
- [ ] CRUD de personajes (web)
- [ ] CRUD de lugares (web)
- [ ] Timeline de historia (web)
- [ ] Relaciones entre personajes (web)
- [ ] Vista de biblia completa
- [ ] Persistencia en `bible/*.json`

### Sprint 4: Canvas de Escenas
- [ ] Vista de tarjetas con cada escena
- [ ] Arrastrar y soltar para reordenar
- [ ] Vinculación de personajes a escenas
- [ ] Estados: draft / in_progress / complete / revision
- [ ] Navegación entre escenas

**Validation Gate:** Un escritor puede definir su biblia completa y organizar sus escenas visualmente.

---

## Fase 2 — IA Co-Writer (Sprint 5-7, ~3 semanas)

**Objetivo:** IA en 4 niveles + BYOK.

### Sprint 5: BYOK + Chat IA (Nivel 1 y 2)
- [ ] Configuración de API key en `umbra.json`
- [ ] Integración AI SDK (OpenAI, Anthropic, DeepSeek, Ollama)
- [ ] **Panel de chat IA** en la UI (sidebar colapsable)
- [ ] **Contexto automático:** la IA sabe qué escena estás editando
- [ ] **Nivel 1 — Brainstorming:** "Dame ideas para este personaje"
- [ ] **Nivel 2 — Asistencia:** "Reescribí en tono más oscuro"
- [ ] Streaming de respuestas en el chat
- [ ] Historial de conversaciones por proyecto

### Sprint 6: Story Engine + Chat Avanzado
- [ ] Algoritmo de beat sheet desde la biblia
- [ ] UI de beat sheet (visualización de estructura)
- [ ] Edición manual de beats
- [ ] Vinculación de escenas a beats
- [ ] **Nivel 3 — Consulta:** "¿Cómo va vestido Juan?" (la IA conoce toda la biblia)
- [ ] **Selección contextual:** seleccionás texto → "Reescribí esto..."

### Sprint 7: Modo Diff + Agent Interface
- [ ] **Nivel 4 — Generación:** "Escribí el diálogo entre Juan y María en la escena 3"
- [ ] **Modo diff:** muestra cambios propuestos antes de aplicarlos
- [ ] Botón "Aplicar cambios" / "Descartar"
- [ ] Documentación del formato de archivos para agentes externos
- [ ] Ejemplo: "Cómo usar UmbraWriter con OpenClaw"
- [ ] Export a Markdown completo (la novela entera en un archivo)

**Validation Gate:** Un escritor puede escribir una novela completa con asistencia de IA en todos los niveles. Un agente externo puede leer y modificar los archivos.

---

## Fase 3 — Polish + Tauri (Sprint 8, ~1 semana)

**Objetivo:** App empaquetada, UX pulida, documentación.

### Sprint 8
- [ ] Tauri: empaquetar la app como aplicación de escritorio
- [ ] UI polish: estados vacíos, loading, errores, animaciones
- [ ] Testing: Playwright para web, Vitest para core
- [ ] Documentación de usuario completa
- [ ] Landing page / docs site
- [ ] Publicar en GitHub

**Validation Gate:** Cualquier persona puede descargar UmbraWriter, abrirlo, y empezar a escribir.

---

## Post-MVP (Fase 4+)

- **Export:** EPUB, DOCX, PDF
- **Plugins:** Sistema de extensiones
- **Import:** Importar novelas existentes (Markdown, DOCX)
- **Series:** Management de series de libros
- **Sincronización opcional:** Backup en la nube (Git, Dropbox, etc.)
- **AI avanzado:** Detección de plot holes, consistencia de personajes, sugerencias de ritmo
- **Temas visuales:** Modo oscuro, fuentes personalizables, modo escritura sin distracciones

## Timeline Estimado

| Fase | Duración | Entrega |
|------|----------|---------|
| Fase 0 — Fundación | 2 semanas | Día 14 |
| Fase 1 — Story Bible | 2 semanas | Día 28 |
| Fase 2 — IA Co-Writer | 3 semanas | Día 49 |
| Fase 3 — Polish + Tauri | 1 semana | Día 56 |
| **MVP Completo** | **8 semanas** | **Día 56** |

## Criterios de Go/No-Go por Fase

- **Fase 0 → Fase 1:** Server local funcionando, editor markdown operativo, archivos en FS
- **Fase 1 → Fase 2:** Biblia completa + canvas de escenas funcionando
- **Fase 2 → Fase 3:** IA en 4 niveles + BYOK + formato de archivos documentado
- **Fase 3 → Publicación:** App empaquetada, documentada, testeada
