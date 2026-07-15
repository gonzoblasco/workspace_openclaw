# ROADMAP.md — BrainWeb

> Phase 3 — Product Roadmap
> Fecha: 2026-07-15

## Phase breakdown

### Phase 1: Backend + Auth — ~3 días
- **Goal:** Migrar de localStorage a Supabase
- **Deliverable:** App funcional con auth y persistencia en servidor
- **Tasks:**
  1. Configurar proyecto Supabase (nuevo, no el de SoporteML v2)
  2. Schema SQL: tabla `notes` (id, user_id, title, content, tags[], created_at, updated_at) + RLS
  3. Migrar notes-store.ts de localStorage a Supabase queries
  4. Implementar auth: login/register pages + useAuth hook
  5. Proteger rutas (redirect a login si no autenticado)
- **Demo:** Usuario se registra, crea nota, recarga y la nota sigue ahí
- **Skill:** sdd-brownfield (delta spec para backend) + agent-dispatcher (implementación)

### Phase 2: Editor + Preview — ~2 días
- **Goal:** Editor markdown funcional con preview en vivo
- **Deliverable:** Editor split-pane con markdown + preview
- **Tasks:**
  1. Integrar react-markdown + remark-gfm para preview
  2. Auto-guardado debounced (2s después de último cambio)
  3. Manejo de tags: input de tags con autocomplete
  4. Sincronizar con Supabase en cada guardado
- **Demo:** Escribir markdown, ver preview en vivo, recargar y contenido persiste
- **Skill:** agent-dispatcher

### Phase 3: Graph View — ~2 días
- **Goal:** Graph view funcional conectado a datos reales
- **Deliverable:** Graph view SVG con datos de Supabase
- **Tasks:**
  1. Adaptar GraphView existente para recibir notas desde Supabase
  2. Conexiones entre nodos por tags compartidos
  3. Click en nodo → navegar a nota
  4. Zoom + pan
- **Demo:** Ver grafo con notas reales, click en nodo abre la nota
- **Skill:** agent-dispatcher

### Phase 4: Search + Polish — ~2 días
- **Goal:** Búsqueda funcional + pulido de UX
- **Deliverable:** Búsqueda server-side + edge cases cubiertos
- **Tasks:**
  1. Búsqueda en Supabase (ILIKE en title + content + tags)
  2. Loading states, error states, empty states
  3. Toasts para feedback de acciones
  4. Responsive: mobile funciona bien
- **Demo:** Buscar notas, filtrar por tag, todo funciona en mobile
- **Skill:** agent-dispatcher + agent-review

### Phase 5: Deploy + Docs — ~2 días
- **Goal:** App deployada + documentación
- **Deliverable:** App en producción + README.md + deploy guide
- **Tasks:**
  1. Deploy en Vercel (frontend) + Supabase (backend)
  2. README.md con: qué es, cómo deployar, features, screenshots
  3. Guía de deploy self-hosted (docker-compose o manual)
  4. LICENSE (MIT)
  5. GitHub Pages o landing mínima
- **Demo:** App funcionando en producción, cualquier persona puede deployarla
- **Skill:** agent-dispatcher

### Post-MVP
- Sync multi-dispositivo en tiempo real (Supabase Realtime)
- AI features (resumen automático, sugerencias de tags)
- Import/export (Markdown files, JSON)
- Plugins API
- Mobile PWA

## Skill mapping

| Phase | Skill | Why |
|---|---|---|
| 1. Backend + Auth | sdd-brownfield + agent-dispatcher | Spec del backend + implementación |
| 2. Editor + Preview | agent-dispatcher | Feature existente, migrar a backend |
| 3. Graph View | agent-dispatcher | Feature existente, conectar a backend |
| 4. Search + Polish | agent-dispatcher + agent-review | Feature nueva + gate de calidad |
| 5. Deploy + Docs | agent-dispatcher | Deploy + documentación |

## Risk register

| Riesgo | Impacto | Probabilidad | Mitigación |
|---|---|---|---|
| Migración de localStorage a Supabase rompe features existentes | Alto | Media | Tests manuales de cada flow post-migración |
| Graph view SVG no escala con muchas notas | Medio | Baja | Límite de nodos visibles (50), agrupación |
| Deploy self-hosted muy complejo para usuarios no-técnicos | Medio | Alta | Guía paso a paso + template docker-compose |
| Gonzo pierde momentum por priorizar SoporteML v2 | Alto | Alta | MVP en 2 semanas o se congela |
| Nadie encuentra el proyecto en GitHub | Medio | Alta | SEO en README, post en r/selfhosted y r/PKM |
