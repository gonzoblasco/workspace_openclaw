# DEFINITION — UmbraWriter

> Basado en BRIEF.md. Define MVP, features, métricas y posicionamiento.

## Personas

### 1. Alejo — El Escritor Técnico
- **Perfil:** Dev que escribe ficción. Sabe git, markdown, CLI. Quiere herramientas de dev para escribir.
- **Dolor:** Las herramientas existentes son cerradas, caras, y no se integran con su flujo de trabajo técnico.
- **Valor:** Open source, CLI, git-native, extensible.

### 2. Martina — La Escritora Dedicada
- **Perfil:** Escritora de ficción que publica en Amazon KDP. No es técnica pero quiere herramientas potentes.
- **Dolor:** Sudowrite es caro y la IA es caja negra. Quiere control sin ser dev.
- **Valor:** UI intuitiva, Story Bible visual, precios accesibles (o gratis si es open source).

### 3. Lucas — El Principiante
- **Perfil:** Quiere escribir una novela pero no sabe por dónde arrancar.
- **Dolor:** Blank page syndrome. No tiene estructura ni personajes definidos.
- **Valor:** IA que lo guía desde cero: "dame una premisa", "creame un personaje", "sugerime una estructura".

## MVP (Fase 1)

Lo mínimo para que un escritor pueda escribir una novela completa con IA:

### MVP Features

1. **Story Bible**
   - CRUD de personajes (nombre, descripción, personalidad, apariencia, historia)
   - CRUD de lugares (nombre, descripción, atmósfera)
   - Timeline de historia (eventos clave en orden cronológico)
   - Relaciones entre personajes (básico: aliado/enemigo/familiar/romance)

2. **Story Engine — Beat Sheet Automática**
   - Input: la Story Bible
   - Output: estructura de novela con beats (inciting incident, midpoint, climax, etc.)
   - Basada en la biblia, no en plantillas genéricas
   - Editable manualmente

3. **Canvas de Escenas**
   - Vista de tarjetas con cada escena
   - Arrastrar y soltar para reordenar
   - Cada escena vinculada a su beat en la beat sheet
   - Estado: borrador / en progreso / completo / revisión

4. **Editor de Texto**
   - Editor WYSIWYG para escribir escenas
   - Markdown como formato subyacente
   - Atajos de teclado para escritura rápida
   - Contador de palabras por escena, capítulo, total

5. **AI Co-Writer (chat conversacional integrado)**
   - **Panel de chat** en la UI, al costado del editor
   - **Contexto automático:** la IA sabe qué escena estás editando y conoce la biblia
   - **Nivel 1 — Brainstorming:** "Dame ideas para este personaje", "Sugerime un conflicto para esta escena"
   - **Nivel 2 — Asistencia:** "Reescribí este párrafo en tono más oscuro", "Expandí esta descripción"
   - **Nivel 3 — Consulta:** "¿Cómo va vestido Juan, el sherif del pueblo?" (la IA conoce la biblia)
   - **Nivel 4 — Generación:** "Escribí el diálogo entre Juan y María en la escena 3"
   - **Modo diff:** muestra los cambios propuestos antes de aplicarlos
   - **Selección contextual:** seleccionás texto y pedís cambio directamente

6. **Agent-ready (para cambios globales)**
   - Los archivos (markdown + JSON) son editables por cualquier agente externo
   - Ideal para cambios globales: "cambiá el nombre del pueblo a Santa Clara en toda la novela"
   - Análisis: "¿qué personajes no aparecieron en los últimos 5 capítulos?"
   - Operaciones que el chat de la UI no soporta

### No incluido en MVP (post-MVP)
- Export a EPUB/DOCX
- Colaboración en tiempo real
- Desktop app (Tauri)
- Plugins / extensiones
- Feedback de beta readers
- Import de novelas existentes
- Series management

## Métricas de Éxito

### MVP (3 meses post-lanzamiento)
- **100 usuarios activos** (que usan la herramienta semanalmente)
- **10 novelas completadas** con UmbraWriter
- **5 PRs de la comunidad** (contribuciones open source)
- **NPS > 40** entre usuarios activos

### Crecimiento (6 meses)
- **500 usuarios activos**
- **50 novelas completadas**
- **20 contribuidores** en GitHub
- **Integración CI/CD** funcionando

## Posicionamiento

**UmbraWriter es a Sudowrite lo que VS Code es a Word.**

- Sudowrite = SaaS cerrado, caro, caja negra, tus datos en su nube
- UmbraWriter = local-first, open source, archivos como fuente de verdad, editable por agentes

**Diferenciadores clave:**
1. Open source (MIT) — nadie en este espacio lo es
2. **Local-first** — corre en localhost, tus datos son tuyos
3. **Archivos como fuente de verdad** — markdown + JSON, versionable con git, portable
4. **Agent-ready** — cualquier agente (OpenClaw, Claude Code) puede modificar los archivos mediante lenguaje natural
5. **BYOK** — traés tu propia API key, sin suscripciones
6. **Story Bible como centro** — no es un editor con IA pegada, es una biblia con editor
7. **IA en todos los niveles** — desde brainstorming hasta edición quirúrgica

## Stack Tecnológico (Asumido)

| Capa | Tecnología | Justificación |
|------|-----------|---------------|
| Frontend | React + TypeScript + Tailwind v4 | Stack conocido, maduro, ecosistema |
| Editor | TipTap (ProseMirror) | Extensible, open source, markdown subyacente |
| Server local | Hono + Bun | Liviano, rápido, fácil de empaquetar |
| Datos | Archivos planos (markdown + JSON) | Portables, versionables, editables por agentes |
| IA | AI SDK (Vercel) + BYOK | Multi-model, streaming, open source |
| Desktop | Tauri | Liviano, Rust, open source |
| Testing | Vitest + Playwright | Stack conocido |
| CI/CD | GitHub Actions | Gratuito para open source |

## Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Espacio saturado de AI writing tools | Alta | Medio | Diferenciación clara (OSS + CLI + Bible-first) |
| Modelos de IA muy caros para correr | Media | Alto | Soportar múltiples modelos, incluyendo locales (Ollama) |
| Complejidad del editor (TipTap) | Media | Medio | MVP con features de editor básicas, no intentar clonar Google Docs |
| Poco interés de la comunidad OSS | Media | Alto | Construir para uno mismo primero (dogfooding), la comunidad viene después |
| ADHD — perder foco/motivación | Alta | Alto | Ciclos cortos, MVP chico, features que brillan rápido |
