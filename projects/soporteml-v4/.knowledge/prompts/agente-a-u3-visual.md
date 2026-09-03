# Prompt - Agente A, U3 (Validación visual)

> Copiar y pegar en el Agente A (VS Code). El workspace que tiene cargado es el mismo que el de Kanam, así que el proyecto está en `projects/soporteml-v4/`.

---

Estás trabajando en SoporteML V4, Fase 1 (pulido + integraciones). Sos el Agente A (VS Code). Tu rol en el pipeline de revisión cruzada: primero REVISAR la U2 del Agente B (code-splitting), y luego DESARROLLAR la U3 (validación visual).

## Contexto del pipeline
SoporteML V4 usa el pipeline A/B de revisión cruzada (skill agent-orchestration-pipeline): el Agente A desarrolla unidades impares, el B pares, y cada uno revisa la del otro antes de avanzar. El Agente B desarrolló U2 (code-splitting). Tu trabajo tiene dos partes: (1) revisar U2 con ojos frescos, y (2) desarrollar U3 (validación visual).

## El proyecto
Todo vive en `projects/soporteml-v4/` (el workspace que tenés cargado es el mismo que el mío). El código está en la raíz de `projects/soporteml-v4/` (monorepo pnpm: apps/api, apps/web, packages/db). El `.knowledge/` (BRIEF, PLAN, STATUS, HANDOFF, PIPELINE-AB, ADR-001) está en `projects/soporteml-v4/.knowledge/`. Leé el HANDOFF, el PIPELINE-AB y el ADR-001 (identidad visual) primero para contexto completo.

## Estado actual del repo
- Repo git: `gonzoblasco/soporteml-v4` (independiente).
- U1 (RAG) y U2 (code-splitting) completadas. 34 tests verdes. Build sin warning de chunk.
- **Servidores dev corriendo desde v4:** API en `localhost:3001`, web en `localhost:5173`. La app ya carga el mock de datos al login (auto-sync).
- **Nota operativa:** el pre-commit hook usa `turbo`, que en el sandbox de VS Code falla con un I/O error al leer `~/Library/Application Support/com.vercel.cli/auth.json`. Corré `git commit` fuera del sandbox (o con `SKIP_SIMPLE_GIT_HOOKS=1` SOLO si ya verificaste lint + test manualmente).

## PARTE 1 - REVISAR la U2 del Agente B (cross-review)

El Agente B dejó una nota en `HANDOFF.md`. Verificá con ojos frescos:

### Cambios de U2 (commits `21fda14` + `ab914c8`)
1. **`21fda14`** - fix del score: `searchChunks` ahora devuelve `ScoredKbChunk[]` con el score real de similitud coseno (antes devolvía `score: 0`).
2. **`ab914c8`** - code-splitting: las 7 vistas (Inbox, Products, Templates, KnowledgeBase, Customers, Metrics, Settings) se extrajeron de `App.tsx` (~1491 líneas) a `apps/web/src/views/`, con `React.lazy` + `<Suspense>`. Bundle principal 512 kB → 339 kB.

### Puntos de revisión
1. **Que el code-splitting no rompió nada** - las vistas cargan bien, el sidebar sigue cambiando de vista, no hay imports rotos.
2. **Que el fix del score no rompió el contrato** - `searchChunks` devuelve `ScoredKbChunk[]` ahora; verificá que los consumidores (kb-service, tests) estén alineados.
3. **A11y del Suspense fallback** - el Agente B dice que usó `role="status"` + `aria-live="polite"` + sr-only. Verificá que esté bien.
4. **Que no quedaron referencias colgantes** a las vistas viejas en `App.tsx`.

### Reglas de la revisión
- Si encontrás bugs, corregilos (commit aparte, con mensaje claro).
- Documentá el resultado de tu revisión en el HANDOFF.

## PARTE 2 - DESARROLLAR la U3: Validación visual

### Contexto
La identidad visual de V4 está definida en `ADR-001-identidad-visual.md` (híbrido oscuro + acento amarillo MeLi + color por categoría). El mockup validado está en `mockups/identidad-v4.html`. La app ya corre con esta identidad, pero el code-splitting (U2) extrajo las vistas a archivos nuevos - es momento de verificar que la identidad se mantuvo consistente en todas las vistas y pulir detalles.

**IMPORTANTE:** esta es una unidad de VALIDACIÓN VISUAL. El criterio de aceptación es que la app se vea profesional y consistente con el ADR-001, NO solo que compile. Usá el browser (tenés la tool `browser` disponible) para ver la app corriendo en `localhost:5173` y evaluar cada vista.

### Criterios de aceptación
1. **La app se ve profesional y consistente** con la identidad V4 (ADR-001): base oscura premium, acento amarillo MeLi, color por categoría, glassmorphism, glow sutil.
2. **Todas las vistas** (bandeja, productos, plantillas, KB, clientes, métricas, ajustes) mantienen la identidad - ninguna quedó "pelada" o con estilo por defecto tras el code-splitting.
3. **A11y WCAG 2.1 AA** - contraste 4.5:1, focus visible, labels en botones de solo icono, jerarquía de headings.
4. **Micro-interacciones** - cards con hover, bordes que se iluminan, stats con barra de color por categoría.
5. **Sin regresiones** - la app funciona igual (login, sync, responder, navegar).
6. **Build + tests + lint verdes.**

### Enfoque sugerido
1. **Abrí la app en el browser** (`localhost:5173`) y recorré cada vista con el sidebar.
2. **Compará contra el mockup** (`mockups/identidad-v4.html`) y contra el ADR-001.
3. **Detectá inconsistencias:** colores fuera de paleta, espaciado irregular, tipografía inconsistente, elementos sin glow, vistas que perdieron la identidad tras el code-splitting.
4. **Ajustá lo que detectes** - CSS en `apps/web/src/index.css` o en las vistas.
5. **Documentá** qué ajustaste y qué quedó pendiente de validación de Gonzo.

### Archivos relevantes
- `apps/web/src/index.css` - tokens V4 (base oscura, acento MeLi, colores por categoría)
- `apps/web/src/views/*.tsx` - las 7 vistas (verificá consistencia)
- `apps/web/src/components/AppSidebar.tsx` - navegación
- `apps/web/src/components/CategoryBadge.tsx` - badge de categoría con color
- `mockups/identidad-v4.html` - el mockup validado (referencia visual)
- `.knowledge/ADR-001-identidad-visual.md` - la identidad definida

## Reglas
- Commit atómico + push. Idealmente 1-2 commits para U3 (ajustes visuales + docs).
- Commits en inglés, UI/prompts en español.
- No romper invariantes: multi-tenant, ADRs, identidad V4, a11y.
- Verificación obligatoria: build + tests + lint verdes antes de commitear.
- Actualizar docs: al cerrar U3, marcar U3 como hecha en `PLAN.md` y `STATUS.md` (en `.knowledge/`), y commitear los docs al repo v4.
- Dejar nota para el Agente B (próximo en la cadena) en el HANDOFF.

## Nota para el próximo agente (Agente B)
Dejá un mensaje claro de qué revisaste de U2, qué ajustaste visualmente, y qué necesita la validación final de Gonzo (que es quien aprueba la identidad visual).
