# DEFINITION.md — BrainWeb

> Phase 2 — Product Definition
> Fecha: 2026-07-15

## MVP Scope

### Core value
Una web app de notas que podés hostear vos mismo, con editor markdown, tags, y un graph view que muestra cómo se conectan tus ideas.

### In scope (MVP)
1. **Auth** — registro y login con email/password (Supabase Auth)
2. **Notas CRUD** — crear, editar (markdown con preview), eliminar notas
3. **Tags** — agregar/quitar tags por nota, filtrar por tag
4. **Búsqueda** — buscar en título y contenido de notas
5. **Graph view** — visualización SVG de notas como nodos conectados por tags compartidos
6. **Persistencia en servidor** — todo en Supabase, no más localStorage
7. **Self-hosted deploy** — guía de deploy con Supabase (docker-compose o CLI)

### Out of scope (post-MVP)
- Sync multi-dispositivo en tiempo real — post-MVP
- AI features (resúmenes, sugerencias) — post-MVP
- Plugins / extensiones — post-MVP
- Mobile app — post-MVP
- Colaboración multi-usuario — post-MVP
- Import desde Obsidian/Notion — post-MVP
- Billing / monetización — post-MVP (si aplica)

### Explicit non-goals
- No es un clon de Obsidian — no va a tener cien plugins
- No es una plataforma de colaboración — es personal
- No tiene modo offline avanzado — funciona online
- No tiene versionado de notas — el markdown es el source of truth

## User Personas

### Persona 1: El dev que quiere control
- **Quién:** Desarrollador fullstack, 25-40 años
- **Context:** Cansado de que sus notas estén en manos de terceros (Notion, Google Docs)
- **Necesita:** Una web app de notas que pueda hostear él mismo, con control total de sus datos
- **Qué hace:** Escribe notas técnicas, guarda snippets, linkea conceptos
- **Éxito:** Tiene su propio "second brain" corriendo en su VPS, accesible desde cualquier browser

### Persona 2: El power user de PKM
- **Quién:** Usuario avanzado de productividad, 20-45 años
- **Context:** Usa Obsidian/Logseq pero quiere acceso web sin depender de una app nativa
- **Necesita:** Editor markdown, tags, graph view, búsqueda rápida
- **Qué hace:** Toma notas de libros, podcasts, ideas; conecta conceptos visualmente
- **Éxito:** Puede acceder a su base de conocimiento desde cualquier dispositivo sin instalar nada

## User Flows

### Flow 1: Registro y primer uso
- **Trigger:** Usuario entra a la app por primera vez
- **Steps:**
  1. Ve landing/login page
  2. Se registra con email + password
  3. Es redirigido al dashboard vacío
  4. Ve empty state con CTA "Crear primera nota"
- **Outcome:** Usuario logueado, listo para crear notas
- **Error:** Email ya registrado → mensaje claro, link a login

### Flow 2: Crear nota
- **Trigger:** Usuario hace clic en "Nueva nota"
- **Steps:**
  1. Se crea nota con título "Nueva nota" y contenido vacío
  2. Aparece en la sidebar como seleccionada
  3. Editor markdown se abre con placeholder
  4. Usuario escribe título y contenido
  5. Auto-guarda al perder foco (debounced)
- **Outcome:** Nota creada y persistida en Supabase
- **Error:** Error de red → toast "Error al guardar", reintento automático

### Flow 3: Editar nota con markdown
- **Trigger:** Usuario selecciona una nota de la sidebar
- **Steps:**
  1. Nota se carga en el editor
  2. Panel izquierdo: editor markdown (textarea o CodeMirror)
  3. Panel derecho: preview renderizado (react-markdown)
  4. Usuario escribe markdown, preview se actualiza en vivo
  5. Tags se muestran arriba, se pueden agregar/quitar
- **Outcome:** Nota editada y guardada
- **Error:** Contenido muy largo → límite de caracteres con aviso

### Flow 4: Buscar y filtrar
- **Trigger:** Usuario escribe en la barra de búsqueda
- **Steps:**
  1. Mientras escribe, la sidebar filtra notas en tiempo real
  2. Búsqueda incluye título + contenido + tags
  3. Usuario puede hacer clic en un tag para filtrar por ese tag
  4. Combinable: búsqueda + tag activo
- **Outcome:** Lista filtrada de notas
- **Error:** Sin resultados → mensaje "Sin resultados" con sugerencia

### Flow 5: Graph view
- **Trigger:** Usuario cambia a vista de grafo
- **Steps:**
  1. Notas se renderizan como nodos SVG
  2. Conexiones entre nodos = tags compartidos
  3. Nodo activo se resalta
  4. Click en nodo → selecciona esa nota y vuelve a vista de notas
  5. Zoom y pan con mouse
- **Outcome:** Visualización de la red de conocimiento
- **Error:** Sin notas → mensaje "Creá algunas notas para ver tu grafo"

### Flow 6: Eliminar nota
- **Trigger:** Usuario hace clic en eliminar (icono trash)
- **Steps:**
  1. Confirmación: "¿Eliminar esta nota?"
  2. Si confirma → nota se elimina de Supabase
  3. Sidebar se actualiza, editor se cierra
- **Outcome:** Nota eliminada permanentemente
- **Error:** Nota no encontrada → toast de error, recargar lista

## Success Metrics

1. **Notas creadas por usuario** — mínimo 5 notas en la primera semana = señal de adopción
2. **Tags usados** — al menos 1 tag por nota en promedio = señal de que el sistema de organización funciona
3. **Graph view visits** — al menos 1 visita al grafo por sesión = señal de que la feature diferencial se usa
4. **Retención día 7** — usuario vuelve después de una semana = señal de valor real
5. **GitHub stars** — 50+ stars en 3 meses = señal de interés comunitario
