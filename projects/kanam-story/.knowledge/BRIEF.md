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
