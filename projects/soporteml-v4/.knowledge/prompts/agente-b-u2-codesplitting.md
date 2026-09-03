# Prompt - Agente B, U2 (Code-splitting) + revisión de U1

> Copiar y pegar en el Agente B (VS Code). El workspace que tiene cargado es el mismo que el de Kanam, así que el proyecto está en `projects/soporteml-v4/`.

---

Estás trabajando en SoporteML V4, Fase 1 (pulido + integraciones). Sos el Agente B (VS Code). Tu rol en el pipeline de revisión cruzada: primero REVISAR la U1 del Agente A (RAG), y luego DESARROLLAR la U2 (code-splitting).

## Contexto del pipeline
SoporteML V4 usa el pipeline A/B de revisión cruzada (skill agent-orchestration-pipeline): el Agente A desarrolla unidades impares, el B pares, y cada uno revisa la del otro antes de avanzar. El Agente A desarrolló U1 (ajuste fino RAG). Tu trabajo tiene dos partes: (1) revisar U1 con ojos frescos y corregir bugs si encontrás, y (2) desarrollar U2.

## El proyecto
Todo vive en `projects/soporteml-v4/` (el workspace que tenés cargado es el mismo que el mío). El código está en la raíz de `projects/soporteml-v4/` (monorepo pnpm: apps/api, apps/web, packages/db). El `.knowledge/` (BRIEF, PLAN, STATUS, HANDOFF, PIPELINE-AB) está en `projects/soporteml-v4/.knowledge/`. Leé el HANDOFF y el PIPELINE-AB primero para contexto completo.

## Estado actual del repo
- Repo git: `gonzoblasco/soporteml-v4` (independiente, no es subdirectorio del workspace).
- U1 completada por el Agente A (commit `6c95905`): RAG minScore subido a 0.45 + threshold configurable por empresa + 4 tests nuevos.
- 30 tests del API, todos verdes. Build OK. Pre-commit hook corre `pnpm lint && pnpm test`.
- **Nota operativa:** el pre-commit hook usa `turbo`, que en el sandbox de VS Code falla con un I/O error al leer `~/Library/Application Support/com.vercel.cli/auth.json`. Corré `git commit` fuera del sandbox (o con `SKIP_SIMPLE_GIT_HOOKS=1` SOLO si ya verificaste lint + test manualmente).

## PARTE 1 - REVISAR la U1 del Agente A (cross-review)

El Agente A dejó una nota en `HANDOFF.md` con los puntos a mirar. Verificá con ojos frescos:

### Cambios de U1 (commit `6c95905`)
1. **`packages/db/src/repo/kb.ts`** - nueva constante `DEFAULT_MIN_SCORE = 0.45`, default de `searchChunks`.
2. **`apps/api/src/kb-service.ts`** - `search` lee `kb_similarity_threshold` de los settings de la empresa (configurable por tenant), respeta un `minScore` explícito en `opts`.
3. **`packages/db/src/repo/settings.ts`** + **`apps/api/src/app.ts`** - `PUT /settings` acepta `kbSimilarityThreshold` (y `kbTopK`).
4. **`apps/api/src/kb-service.test.ts`** - 4 tests con embeddings one-hot determinísticos (stub de `embed`, sin Ollama).

### Puntos de revisión (del Agente A + míos)
1. **El default 0.45 no rompe matches reales** - el agente lo cubrió con vectores controlados, pero si tenés Ollama disponible, validá el caso real ("¿Cuánto tarda el envío?" → Política de envíos).
2. **La decisión de exponer el threshold en `company_settings` (per-empresa)** en vez de una constante global única.
3. **Que `search` respeta un `minScore` explícito en `opts`** por encima del threshold de settings.
4. **BUG MENOR DETECTADO POR EL ORQUESTADOR (revisar):** `apps/api/src/kb-service.ts` línea ~63 hace `chunks.map((c) => ({ content: c.content ?? "", score: 0 }))` - **devuelve `score: 0` siempre**, aunque `searchChunks` calcula el score real con `cosineSimilarity`. El score se pierde. Si es trivial de arreglar, arreglalo en U2 (devolver el score real). Si toca la API (los consumidores esperan score), verificá que no rompa el contrato.

### Reglas de la revisión
- Si encontrás bugs, corregilos (commit aparte, con mensaje claro).
- Si U1 está correcta, confirmalo en tu nota de cierre.
- Documentá el resultado de tu revisión en el HANDOFF.

## PARTE 2 - DESARROLLAR la U2: Code-splitting

### Contexto del problema
El bundle principal de la web es **512 kB** (157 kB gzip), justo por encima del warning de 500 kB de Vite. La causa: `apps/web/src/App.tsx` es un archivo gigante (~1400+ líneas) con **todas las vistas inline** como funciones en el mismo archivo: `Inbox`, `Products`, `Templates`, `KnowledgeBase`, `Customers`, `Metrics`, `Settings`. Como todas están en un solo archivo, se empaquetan en un solo chunk. La app NO usa React Router - usa un estado `view` (`useState<View>("inbox")`) que se pasa por `AppSidebar` y renderiza condicionalmente (`{view === "inbox" && <Inbox />}`, etc.).

### Criterios de aceptación
1. **Build sin warning de chunk > 500 kB** - el bundle principal debe bajar de 512 kB.
2. **Las vistas cargan bajo demanda** - `Inbox`, `Metrics`, `Customers`, `Settings`, etc. se cargan como chunks separados (lazy).
3. **La app funciona igual** - sin regresión visual ni funcional. Las vistas siguen cambiando con el sidebar.
4. **A11y preservada** - los cambios no rompen la navegación por teclado ni los labels (la accesibilidad es especialización activa del proyecto, ADR-001 identidad V4).
5. **Build + tests + lint verdes.**

### Enfoque sugerido (no obligatorio)
1. **Extraer cada vista a su propio archivo** en `apps/web/src/views/` (ej. `views/Inbox.tsx`, `views/Metrics.tsx`, `views/Customers.tsx`, `views/Templates.tsx`, `views/KnowledgeBase.tsx`, `views/Products.tsx`, `views/Settings.tsx`).
2. **Usar `React.lazy` + `<Suspense>`** para cargar cada vista bajo demanda. Mantener la vista actual en el estado `view` (no introducir React Router - sería un cambio de arquitectura más grande de lo necesario para U2).
3. **Compartir helpers** - si varias vistas usan el mismo código (CATEGORY_COLORS, api, etc.), extraerlo a un lugar compartido si hace falta.
4. Verificar que el chunk principal baja y que cada vista genera su propio chunk.

### Archivos relevantes
- `apps/web/src/App.tsx` - el archivo gigante con todas las vistas inline
- `apps/web/vite.config.ts` - config de Vite (sin React Router, sin manualChunks)
- `apps/web/src/components/AppSidebar.tsx` - define el tipo `View` y navegación
- `apps/web/src/lib/api.ts` - cliente de API
- `apps/web/src/components/CategoryBadge.tsx`, `EmptyState.tsx`, `SkeletonCards.tsx` - helpers compartidos

## Reglas
- Commit atómico + push. Idealmente 1-2 commits para U2 (uno por extracción de vistas + lazy, otro por el fix del score si aplica).
- Commits en inglés, UI/prompts en español.
- No romper invariantes: multi-tenant, ADRs, identidad V4, a11y.
- Verificación obligatoria: build + tests + lint verdes antes de commitear.
- Actualizar docs: al cerrar U2, marcar U2 como hecha en `PLAN.md` y `STATUS.md` (en `.knowledge/`), y commitear los docs al repo v4.
- Dejar nota para el Agente A (próximo en la cadena) en el HANDOFF.

## Nota para el próximo agente (Agente A)
Dejá un mensaje claro de qué revisaste de U1, qué corregiste, qué hiciste en U2, y qué necesita revisión del Agente A.
