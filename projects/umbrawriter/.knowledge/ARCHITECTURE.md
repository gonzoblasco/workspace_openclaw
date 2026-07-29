# ARCHITECTURE — UmbraWriter (v2)

> Actualizado 2026-07-28. Enfoque local-first, archivos como fuente de verdad, agent-ready.

## Stack Definitivo

| Capa | Tecnología | Justificación |
|------|-----------|---------------|
| **Frontend** | React 19 + TypeScript + Tailwind v4 | Stack conocido, maduro |
| **Editor** | Markdown + Preview (MVP) → TipTap (post-MVP) | Reducir riesgo inicial |
| **Server local** | Hono + Bun | Liviano, rápido, sin dependencias pesadas |
| **Datos** | Archivos planos (markdown + JSON) | Fuente de verdad portable, editable por agentes externos |
| **IA** | AI SDK (Vercel) + BYOK | Multi-model, streaming, sin vendor lock-in |
| **Desktop** | Tauri | Empaqueta la app local, nativa, liviana |
| **Testing** | Vitest + Playwright | Stack conocido |
| **CI/CD** | GitHub Actions | Gratuito para OSS |

## Filosofía de Datos

**Los archivos son la fuente de verdad.** No una base de datos. Esto es clave porque:

1. **Un agente externo (OpenClaw) puede leer y modificar los archivos directamente** — sin pasar por la UI, sin APIs, sin autenticación
2. **El escritor puede usar git** para versionar su novela
3. **Portabilidad:** los archivos se pueden abrir en cualquier editor de texto
4. **Sin vendor lock-in:** si UmbraWriter desaparece, los archivos siguen siendo tuyos

### Estructura de Archivos

```
mi-novela/
├── umbra.json              # Config del proyecto (modelo IA, API key, etc.)
├── bible/
│   ├── characters.json     # Personajes
│   ├── locations.json      # Lugares
│   ├── timeline.json       # Timeline de historia
│   └── lore.json           # Lore, reglas del mundo, etc.
├── beats.json              # Beat sheet (estructura de la novela)
├── scenes/
│   ├── 01-capitulo-1/
│   │   ├── 01-escena-1.md
│   │   └── 02-escena-2.md
│   ├── 02-capitulo-2/
│   │   └── 01-escena-1.md
│   └── ...
└── export/                 # Archivos generados (EPUB, DOCX, etc.)
```

### Formato de Archivos

**Escenas (markdown):**
```markdown
---
title: "El encuentro en el bar"
chapter: 1
scene: 3
characters: ["juan-sherif", "maria"]
status: draft
word_count: 450
---

Juan entró al bar y el silencio lo recibió antes que María.

—No esperaba verte tan temprano —dijo ella, sin levantar la vista del vaso que secaba.

—Tampoco yo esperaba estar acá.
```

**Biblia (JSON):**
```json
{
  "characters": [
    {
      "id": "juan-sherif",
      "name": "Juan",
      "role": "protagonist",
      "description": "Sherif del pueblo. Viudo. 45 años.",
      "personality": "Reservado, observador, carga con una culpa silenciosa",
      "appearance": "Barba canosa, ojos cansados, siempre viste el uniforme aunque esté fuera de servicio",
      "backstory": "Perdió a su esposa en un accidente de auto hace 3 años. Desde entonces se refugia en el trabajo.",
      "goals": "Descubrir la verdad sobre la desaparición de su hija",
      "fears": "Quedarse solo, no poder proteger a los que ama"
    }
  ]
}
```

## Cómo Funciona el Flujo Agent-Ready

### Escenario: Gonzo escribe en la UI, después me pide un cambio

1. **Gonzo escribe** el capítulo 4 en la UI web de UmbraWriter
2. **Los archivos se guardan** en `mi-novela/scenes/04-capitulo-4/01-escena-1.md`
3. **Gonzo me dice:** "En el capítulo 4 Juan está demasiado feliz después de que perdió a su perro, no se siente natural, arreglalo"
4. **Yo (OpenClaw) leo** `scenes/04-capitulo-4/01-escena-1.md` y `bible/characters.json`
5. **Entiendo el contexto:** Juan acaba de perder a su perro → debería estar triste, no feliz
6. **Modifico el archivo** directamente — reescribo los párrafos que no funcionan
7. **Gonzo abre la UI** y ve los cambios reflejados (la UI lee los mismos archivos)

### Escenario: Gonzo quiere un cambio global

1. **Gonzo me dice:** "Cambiá el nombre del pueblo a Santa Clara en toda la novela"
2. **Yo leo** todos los archivos `scenes/**/*.md` y `bible/locations.json`
3. **Hago el reemplazo** en todos los archivos
4. **La UI refleja** los cambios automáticamente

## Patrones Arquitectónicos

### Frontend
- **SPA con Vite + React Router** — liviano, rápido, sin Next.js (no necesitamos SSR para una app local)
- **Estado:** React context + hooks (Zustand si se complica)
- **Editor:** Markdown con preview en MVP, TipTap en post-MVP
- **Panel de Chat IA** — sidebar colapsable al costado del editor
  - Input de texto + streaming de respuestas
  - Contexto automático: escena actual + biblia
  - Botón "Aplicar cambios" con modo diff
  - Selección contextual: seleccionás texto → "Reescribí esto..."
- **File System Access API** — para leer/escribir archivos directamente desde el browser (o Tauri fs)

### Server Local (Hono + Bun)
- **Sirve la UI** en localhost
- **API REST** para CRUD de archivos (la UI se comunica con el server, no con el FS directo)
- **Proxy de IA** — las llamadas a la API de IA pasan por el server (para no exponer la API key en el frontend)
- **Watch mode** — detecta cambios en archivos y notifica a la UI

### IA Layer
- **AI SDK** como abstracción — un solo interface para múltiples modelos
- **Context Builder** — construye el contexto de la IA basado en la biblia + escena actual
- **Prompt Templates** — templates por tipo de operación
- **Chat History** — historial de conversaciones por proyecto (persistido en archivos)
- **Diff Engine** — muestra cambios propuestos antes de aplicarlos
- **Streaming** — respuestas en tiempo real en el chat

### Agent Interface (para cambios globales)
- **Formato de archivos documentado** — cualquier agente sabe cómo leer/escribir
- **Sin autenticación** — es local, los archivos están en el filesystem
- **Sin API secreta** — los archivos son el API
- **Caso de uso:** cambios globales que el chat de la UI no cubre (rename masivo, análisis cross-capítulo)

## ADRs Iniciales

### ADR-001: Archivos planos como fuente de verdad
**Contexto:** Necesitamos que agentes externos puedan modificar el contenido sin pasar por la UI.
**Decisión:** Markdown para escenas, JSON para biblia y metadatos. Sin base de datos.
**Consecuencias:** Portabilidad total, versionable con git, editable por cualquier agente. La UI es una ventana a los archivos.

### ADR-002: Markdown-first, WYSIWYG después
**Contexto:** El editor WYSIWYG es complejo. Los agentes trabajan mejor con texto plano.
**Decisión:** MVP con editor de markdown + preview en vivo. TipTap en post-MVP.
**Consecuencias:** Menos riesgo técnico. Los archivos son markdown puro → fáciles de parsear por agentes.

### ADR-003: Server local con Hono + Bun
**Contexto:** Necesitamos un server liviano que sirva la UI, maneje el FS, y proxee llamadas a IA.
**Decisión:** Hono sobre Bun. Sin Next.js, sin Express, sin frameworks pesados.
**Consecuencias:** Rápido, liviano, fácil de empaquetar con Tauri.

### ADR-004: BYOK desde el día 1
**Contexto:** El usuario debe poder usar su propia API key de IA.
**Decisión:** La API key se guarda en `umbra.json` (local, no se sube a ningún lado). AI SDK abstrae los proveedores.
**Consecuencias:** Sin costo de infraestructura para nosotros. El usuario elige su modelo.

## Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────┐
│                    Máquina Local                         │
│                                                          │
│  ┌──────────────────────┐    ┌──────────────┐           │
│  │       Browser         │    │              │           │
│  │  ┌────────────────┐   │    │  Hono Server  │           │
│  │  │   Editor        │   │    │  (localhost)  │           │
│  │  │   (markdown)    │   │    │              │           │
│  │  └────────┬───────┘   │    │  - Sirve UI   │           │
│  │           │           │    │  - CRUD FS    │           │
│  │  ┌────────▼───────┐   │    │  - Proxy IA   │           │
│  │  │  Chat IA        │◄──┼────┤  - Watch mode│           │
│  │  │  (sidebar)      │   │    │              │           │
│  │  │                 │   │    └──────┬───────┘           │
│  │  │  "Juan está     │   │           │                   │
│  │  │   muy feliz     │   │    ┌──────▼───────┐          │
│  │  │   acá, arreglalo"│   │    │  Archivos FS  │          │
│  │  │                 │   │    │  (markdown +  │          │
│  │  │  [Aplicar diff] │   │    │   JSON)       │          │
│  │  └─────────────────┘   │    └───────────────┘          │
│  └──────────────────────┘                                 │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │  AI SDK Proxy (BYOK)                             │    │
│  │  OpenAI / Anthropic / DeepSeek / Ollama          │    │
│  └──────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              Agente Externo (OpenClaw)                   │
│                                                          │
│  Para cambios globales que el chat no cubre:             │
│  "Cambiá el nombre del pueblo a Santa Clara             │
│   en toda la novela"                                     │
│                                                          │
│  → Lee/escribe archivos directamente en el FS            │
│  → Sin pasar por la UI, sin APIs, sin auth               │
│  → La UI refleja los cambios automáticamente             │
└─────────────────────────────────────────────────────────┘
```

## Riesgos Técnicos

| Riesgo | Impacto | Mitigación |
|--------|---------|-------------|
| File System Access API no soportada en todos los browsers | Medio | Tauri para desktop, Hono server como fallback |
| Conflictos si el agente y la UI modifican el mismo archivo | Medio | Watch mode + debounce, el agente escribe atómicamente |
| La API key del usuario queda en texto plano en `umbra.json` | Bajo | Es local, el usuario es dueño de su máquina. Opcional: keychain del SO |
| El markdown de las escenas no captura metadatos complejos | Bajo | Frontmatter YAML/JSON en cada archivo de escena |
