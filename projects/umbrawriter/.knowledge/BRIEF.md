# BRIEF — UmbraWriter

> AI Fiction Co-Writer. Open source. Web-first, CLI-always.

## El Problema en Una Frase

Los escritores de ficción no tienen herramientas modernas que traten la IA como **co-writer** en vez de ghostwriter, que sean **open source**, y que funcionen tanto visualmente (para escribir) como por CLI (para que la IA manipule el texto con precisión).

## Público Objetivo

- **Primario:** Escritores de ficción que también son developers (o quieren herramientas de dev)
- **Secundario:** Escritores de ficción general que buscan una alternativa open source a Sudowrite
- **Terciario:** Talleres de escritura, grupos de co-writing, beta readers

## Propuesta de Valor

UmbraWriter es un **co-writer de ficción con IA** que:

1. **Story Bible first** — la biblia de la historia es el centro de todo. Personajes, lugares, timeline, lore. Todo se define ahí y la IA lo conoce.
2. **Story Engine con Beat Sheets automáticas** — definí la biblia, y UmbraWriter te genera una estructura de novela (beat sheet) basada en tu historia, no en plantillas genéricas.
3. **IA en todos los niveles** — desde "no sé por dónde arrancar" (generación de premisa, personajes, mundo) hasta "¿cómo va vestido Juan, el sherif del pueblo?" (consulta puntual sobre un personaje).
4. **Local-first, UI-web, agent-ready** — corre en localhost, los archivos son la fuente de verdad (markdown + JSON). La UI web es para escribir visualmente. **Chat conversacional integrado en la UI** para cambios quirúrgicos sin salir del flow. Además, un agente externo (OpenClaw, Claude Code, etc.) puede leer y modificar los archivos mediante lenguaje natural para cambios globales.
5. **BYOK (Bring Your Own Key)** — cada usuario trae su propia API key de IA. Sin suscripciones, sin vendor lock-in.
6. **Open source (MIT)** — transparente, extensible. El escritor es dueño de sus datos y su herramienta.

## Features Core (Alto Nivel)

- **Story Bible** — editor de biblia con personajes, lugares, timeline, lore, relaciones
- **Story Engine** — generación de beat sheet automática desde la biblia
- **Canvas de Escenas** — visualización y organización de escenas tipo tarjetas
- **Editor de Texto** — editor WYSIWYG para escribir capítulos y escenas
- **AI Co-Writer** — chat conversacional integrado en la UI para cambios quirúrgicos sin salir del flow. Agent-ready para cambios globales vía archivos.
- **Agent-ready** — archivos editables por agentes externos para cambios globales y análisis
- **Export** — Markdown, EPUB, DOCX (post-MVP)

## Stack Asumido

- **Frontend:** React + TypeScript + Tailwind v4
- **Backend/Datos:** SQLite (local, embebido) o mejor: archivos planos (markdown + JSON) con un server liviano tipo Hono + Bun
- **IA:** AI SDK (Vercel) + BYOK (OpenAI, Anthropic, DeepSeek, Ollama)
- **Editor:** TipTap/ProseMirror (extensible, open source)
- **Formato de archivo:** Markdown para escenas, JSON para biblia y metadatos
- **Desktop:** Tauri (para empaquetar la app local)

## Restricciones Conocidas

- Open source desde el día 1 — el código es público
- Sin vendor lock-in — el usuario puede cambiar de modelo de IA
- Los datos del escritor son suyos — exportables, en formatos abiertos
- Sin telemetría obligatoria — respeto a la privacidad

## Preguntas Abiertas para el Arquitecto

- ¿Archivos planos (markdown + JSON) o SQLite embebido?
- ¿Editor basado en TipTap o editor custom más liviano?
- ¿Server liviano con Hono/Bun o Tauri con Rust backend?
- ¿Modelo de IA default (recomendado) o dejar que el usuario configure el suyo?
- ¿Sincronización opcional con la nube (para backup/colaboración) o 100% local?
