# BRIEF — Kanam Story

> **Co-writer de ficción local-first donde la conversación ES el producto.**

## Problema

Gonzo intentó clonar Sudowrite tres veces (`umbrawriter` v1, `sudolab`, `umbrawriter-v2`). Los tres fracasaron no por la tecnología ni por la calidad de los modelos (Ollama + deepseek-v4 / glm-5.2 resueltos), sino por la **interfaz**: el editor era el centro y la IA un asistente pasivo de botones. Lo que faltaba era un **colaborador con quien conversar**.

No es un problema de "escribir mejor". Es: debatir ideas, estudiar casos, explorar finales alternativos para personajes, con un agente que **conoce toda la obra y tiene manos para aplicarla**.

## Propuesta

**Kanam Story** — un co-writer de ficción local-first (BYOK → Ollama), en español, sin login, sin SaaS, valor del día 1, donde:

1. **El Chat es la puerta de entrada (el corazón).** Conversás con un agente que conoce el manuscrito, la biblia viva y la brújula narrativa. Debates ideas, finales, casos. **El agente no solo habla: actúa** — cuando acordás algo, lo aplica al manuscrito y a la biblia. Co-autor, no asistente pasivo.
2. **Outline & Beats (la estructura).** Definís la estructura de un capítulo o escena como un **mapa de beats**, **a mano** o **sugerido por IA** desde la biblia/brújula/lo escrito. Los beats son objetos editables conectados con la escritura y el chat.
3. **La Biblia Viva (consistencia automática).** Personajes (qué quieren, su voz), mundo, reglas. Se actualiza sola desde lo escrito y desde los cambios del chat.
4. **La Brújula Narrativa (orientación).** Premisa, promesa al lector, arco del protagonista, tema. Visible al escribir y al discutir.
5. **Editor Delgado.** Existe para escribir a mano; no es el protagonista.

## Dirección Fase 2 — Hacia el Story Bible de Sudowrite (2026-08-13)

> Auditoría de 10 capturas de Sudowrite. El gap principal no es el chat (ya lo tenemos y es el corazón), sino el **Story Bible estructurado y editable** que hace que la IA sea coherente. Sudowrite lo muestra como la base de todo: Genre, Style, Synopsis, Braindump, fichas de personaje ricas, worldbuilding tipado. De ahí cuelgan la generación asistida y el Match My Style.

**Lo que Sudowrite tiene y nosotros no (aún):**

- **Story Bible editable y tipado** — Genre, Style (3 modos), Synopsis editable, Braindump. Hoy nuestra biblia es auto-generada; la hacemos editable.
- **Fichas de personaje ricas** — Type (rol), Pronouns, Groups, Other Names, Traits, toggle de inclusión en contexto IA.
- **Worldbuilding tipado fino** — Setting, Organization, Lore, Key Event, Clue, Magic System, Item.
- **Generación asistida de personajes** — modal Generate Character + Surprise Me.
- **Match My Style** — clonar la voz del autor desde una muestra (la feature PRO de Sudowrite, gratis con Ollama local).
- **Filtros de outline** por POV y tiempo verbal + vinculación documento↔outline.

**Nuestra ventaja:** el chat con manos (que Sudowrite no tiene como corazón) + todo esto gratis y local-first. La dirección es converger: un co-writer que conversa Y tiene un Story Bible rico y editable.

**Plan:** slices 6-10 en [ROADMAP.md](./ROADMAP.md), cada uno termina en release usable (v0.2.0 → v0.6.0). Implementan los agentes A (VS Code) y B (ZCode); Kanam planifica y documenta.

## Usuario

Gonzo, solo. Escritor de novela activa (`ultimo-turno`), ADHD. Necesita estructura y orientación, no más distracción.

## Stack (base)

Reutilizar `sudolab` (Next.js 16 App Router, TipTap 3, Bootstrap 5 + tokens, IndexedDB vía `idb`, Ollama vía rutas API, 38 tests vitest). Español en UI y prompts.

## Estrategia anti-repetición

- **Slice fino primero:** Chat con manos + Outline/Beats, usable hoy con `ultimo-turno`. Sin monorepo turbo de cero.
- Brújula en fase siguiente, una vez que chat-estructura funcione.
- Cada slice termina en un release usable, no en más discovery.

## Success

Abrís la app y en 10 segundos sabés qué capítulo sigue, qué prometiste contar y qué necesita cada personaje — y podés *debatirlo* con el agente, que lo aplica.
