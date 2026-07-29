# EVALUATION — UmbraWriter

> Análisis de mercado, competidores, viabilidad y fit estratégico.

## Mapa de Competidores

| Herramienta | Tipo | Precio | Open Source | Story Bible | CLI | IA Levels |
|------------|------|--------|-------------|-------------|-----|-----------|
| **Sudowrite** | SaaS | $29/mo | ❌ | ✅ (básico) | ❌ | Medio |
| **Novelcrafter** | SaaS | $10-25/mo | ❌ | ✅ (Codex) | ❌ | Alto (BYOK) |
| **Dabble** | SaaS | $8-16/mo | ❌ | ✅ | ❌ | Bajo |
| **WriteHERE** | OSS | Gratis | ✅ (MIT) | ❌ | ❌ | Medio |
| **Inkos** | OSS | Gratis | ✅ (AGPL) | ❌ | ❌ | Alto (generación) |
| **Novel-OS** | OSS | Gratis | ✅ (MIT) | ❌ | ❌ | Alto (multi-agente) |
| **novel-engine** | OSS | Gratis | ✅ | ❌ | ❌ | Alto (7 agentes) |
| **UmbraWriter** | OSS | Gratis | ✅ (MIT) | ✅ (core) | ✅ (agent-ready) | Alto (4 niveles) |

## Análisis por Competidor

### Sudowrite
- **Lo que hace bien:** Story Engine, beat sheets, UI pulida, expand/rewrite
- **Lo que hace mal:** Caro ($29/mo), caja negra, no open source, no CLI, vendor lock-in
- **Nuestro angle:** Open source + CLI + Bible-first. No competimos en UI pulida (al principio), competimos en libertad y transparencia.

### Novelcrafter
- **Lo que hace bien:** Codex (story bible), BYOK (traés tu propia API key), comunidad grande (200k+)
- **Lo que hace mal:** No es open source, no tiene CLI, la IA es un add-on, no integrada
- **Nuestro angle:** Novelcrafter es el competidor más directo. Su Codex es similar a nuestra Story Bible. Pero ellos son SaaS cerrado. Nosotros somos open source + CLI. La diferencia es VS Code vs Word.

### WriteHERE (958 ⭐)
- **Lo que hace bien:** Open source, Python backend, agnóstico de modelo
- **Lo que hace mal:** No tiene story bible, no tiene CLI, es más "generador de texto" que co-writer
- **Nuestro angle:** WriteHERE es el OSS más grande del espacio. Pero no tiene biblia ni CLI. Podemos diferenciarnos claramente.

### Inkos (8.2k ⭐)
- **Lo que hace bien:** Muchas estrellas, comunidad grande, multi-idioma
- **Lo que hace mal:** AGPL (restrictivo), chino-first, es generador no co-writer, no tiene UI web
- **Nuestro angle:** No competimos directamente. Inkos es para generar novelas completas con IA. Nosotros somos para escribir *con* IA.

## Diferenciación Clave

| Dimensión | UmbraWriter | Competencia |
|-----------|-------------|-------------|
| **Licencia** | MIT | AGPL (inkos), propietario (Sudowrite, Novelcrafter) |
| **Story Bible** | Centro del producto | Add-on (Sudowrite, Novelcrafter) |
| **CLI / Agent-ready** | Sí, archivos como API | Nadie lo tiene |
| **IA contextual** | 4 niveles (brainstorm → consulta) | 1-2 niveles |
| **Web-first** | Sí | Sí (Sudowrite, Novelcrafter) |
| **BYOK** | Sí | Sí (Novelcrafter) |
| **Modelos locales** | Sí (Ollama) | No |

## Viabilidad Técnica

- **Stack conocido:** React/TS, Supabase, TipTap, AI SDK — todo lo que ya manejás
- **Riesgo principal:** TipTap/ProseMirror es complejo. El editor WYSIWYG es la parte más difícil.
- **Mitigación:** MVP con editor básico (markdown con preview, no WYSIWYG completo). TipTap para post-MVP.
- **IA:** AI SDK de Vercel abstrae la complejidad multi-modelo. Soportar OpenAI, Anthropic, DeepSeek, Ollama desde el día 1.

## Fit Estratégico

- ✅ **Open source portfolio:** PRs a shadcn/ui, TanStack, vercel/ai — este proyecto es el siguiente nivel
- ✅ **Dogfooding:** Vas a escribir tu novela mientras lo construís
- ✅ **Stack conocido:** No necesitás aprender nada nuevo para arrancar
- ✅ **Diferenciación real:** Nadie en el mercado combina OSS + CLI + Bible-first
- ⚠️ **Riesgo ADHD:** Ciclos cortos, features que brillan rápido, MVP chico

## Veredicto

**GO.** El mercado tiene espacio, la diferenciación es real, el stack es conocido, y el dogfooding garantiza que el producto resuelva un problema real. El riesgo principal es la complejidad del editor, pero se mitiga con un MVP de markdown + preview en vez de WYSIWYG completo.
