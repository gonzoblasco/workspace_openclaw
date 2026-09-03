# Slice 8 - Modo personaje (chat de roleplay con la biblia) (plan)

**T=15 (high)** | Pipeline: Kanam diseña → A escribe → B revisa → verificación

## Contexto (visión corregida 2026-09-01)

Kanam Studio es un taller de mundos: la biblia define personajes, lugares, reglas y tramas. El **modo personaje** es la herramienta de planificación interactiva: el autor elige un personaje de la biblia y la IA lo **interpreta** - con su voz, sus motivaciones, sus secretos - para planificar escenas conversando con él. El personaje **no puede contradecir la biblia**.

## Objetivo

1. **Chat de roleplay** (`/api/character`): la IA interpreta un personaje de la biblia según su ficha (descripción, tags, relaciones) + el contexto del mundo (otros personajes, lugares, reglas, tramas).
2. **Selector de personaje**: elegir qué personaje interpretar (solo los de kind `character`).
3. **Consistencia con la biblia**: el prompt le ordena al personaje no contradecir su ficha ni el mundo; si el autor propone algo que contradice la biblia, el personaje lo señala (en su voz).
4. **UI**: panel "Personaje" con selector + chat (reusa el patrón de streaming SSE).

## Arquitectura

```
src/lib/character.ts          - tipos + schema de la request (reusa world.ts)
src/app/api/character/route.ts - proxy a Ollama (roleplay, streaming SSE)
src/components/CharacterPanel.tsx - selector de personaje + chat, CSS Modules, a11y
StoryGraphEditor.tsx           - 8vo panel 'character'
```

### 1. Request (src/lib/character.ts)

```ts
characterRequestSchema = z.object({
  story: storySchema,          // biblia + grafo
  characterId: z.string().min(1),  // id de la entidad character
  message: z.string().min(1),
  history: z.array(chatMessageSchema).default([]),
})
```

- Validar que `characterId` exista en `story.world.entities` y sea `kind: 'character'` (400 si no).

### 2. Route (src/app/api/character/route.ts)

- POST: `{ story, characterId, message, history }`.
- Construye el prompt de sistema:
  - **Rol:** "Sos {nombre}, personaje de la historia {título}".
  - **Ficha del personaje:** descripción, tags, relaciones (con quién y cómo se relaciona).
  - **Contexto del mundo:** otros personajes (nombres + descripción corta), lugares, reglas, tramas.
  - **Reglas de interpretación:**
    - Hablá SIEMPRE como el personaje: su voz, su registro, sus motivaciones. No salgas del personaje.
    - No contradigas tu ficha ni el mundo: si el autor propone algo que contradice la biblia, señalalo EN TU VOZ (ej. "¿Reconciliarme con mi padre? Después de lo que hizo, ni muerto.").
    - No reveles secretos que la biblia no define (si no está en la ficha, no lo inventes).
    - Respondé en el idioma del autor (español por defecto).
    - Texto plano, sin JSON, sin markdown pesado.
  - **MISMO estilo crítico** que la IA co-autora: el personaje puede discutir con el autor si su plan no tiene sentido para el personaje.
- Streaming SSE idéntico a /api/chat (delta/done/error). Sin acciones (el personaje no toca el grafo - solo conversa).
- Timeout 180s. Seguridad: nunca exponer la story en errores.

### 3. Panel Personaje (src/components/CharacterPanel.tsx)

- **Selector:** lista de personajes de la biblia (kind: character). Si no hay personajes, hint "Definí personajes en el panel Mundo primero".
- **Chat:** reusa el patrón de AICoAuthor (streaming SSE, markdown, aria-live, foco).
- **Header:** nombre del personaje activo + badge "en personaje".
- a11y: labels, foco, CSS Modules (regla v0.6.0).

## Criterios de done

- [ ] `/api/character` con streaming SSE, prompt de interpretación, validación de characterId.
- [ ] CharacterPanel: selector + chat, CSS Modules, a11y.
- [ ] Tests: schema de request, validación de characterId inexistente/no-character.
- [ ] Tests verdes, lint, typecheck, build OK.
- [ ] E2E: abrir panel Personaje, ver selector, elegir personaje, chat responde.
- [ ] Validado contra Ollama real (deepseek-v4-flash:cloud): el personaje habla en su voz y no contradice la biblia.
