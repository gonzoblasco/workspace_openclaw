# ROADMAP — Kanam Studio

> Slices finos, cada uno termina en release usable. Patrón heredado de kanam-story: la interfaz mata al producto, no la tecnología. Pipeline A/B para implementar (Kanam planifica, agentes ejecutan).

## Slice 1 — Grafo editable + persistencia (MVP)

**Objetivo:** dibujar una historia ramificada a mano, con persistencia local. El día 1 es usable.

- Nodos (pasajes) con título y contenido.
- Aristas (elecciones) entre nodos, con texto de elección.
- Variables de estado (flags, contadores) declaradas por nodo/elección.
- Visualización de grafo navegable (no solo lista): canvas simple o layout jerárquico.
- Persistencia en IndexedDB (patrón kanam-story: `idb`).
- a11y integrada: navegación por teclado del grafo, foco visible, contraste.

**Release:** v0.1.0. **Éxito:** creás una historia de 10+ nodos sin tocar código.

## Slice 2 — Modo jugar

**Objetivo:** recorrer la historia desde cualquier nodo, viendo el estado de variables en vivo. Testear el flujo es parte del editor.

- Player: muestra el pasaje actual, las elecciones disponibles (con condiciones evaluadas), aplica efectos.
- Panel de estado: variables y hechos visibles en vivo durante el recorrido.
- Empezar desde cualquier nodo (no solo el inicial) - clave para testear ramas aisladas.

**Release:** v0.2.0. **Éxito:** jugás una historia completa y detectás ramas rotas (elección que no lleva a ningún lado).

## Slice 3 — IA co-autora de ramas

**Objetivo:** la IA extiende una rama desde el estado acumulado de esa ruta, no desde el grafo entero.

- Chat con manos (patrón kanam-story): conversás con el agente y aplica cambios al grafo.
- Generación de ramas: "¿qué pasa si el jugador le miente a María?" → la IA crea nodos/elecciones consistentes con el estado de esa ruta.
- Contexto = ruta (estado acumulado + nodos visitados), no el grafo completo. BYOK → Ollama.

**Release:** v0.3.0. **Éxito:** generás una rama de 3+ nodos y la integrás al grafo sin reescribirla a mano.

## Slice 4 — Canon checker

**Objetivo:** detección automática de contradicciones e inconsistencias.

- "En la ruta A el personaje murió, en esta rama lo mencionás vivo" → alerta.
- Ramas huérfanas (nodos sin entrada), finales inalcanzables (condiciones imposibles), callejones sin salida.
- Chequeo on-demand + al guardar. La IA explica el conflicto y sugiere fixes.

**Release:** v0.4.0. **Éxito:** agregás una rama contradictoria y la app te lo dice antes de que un lector lo descubra.

## Slice 5 — World-building con IA

**Objetivo:** personajes, mundo y reglas construidos y mantenidos con IA durante todo el viaje. La versión superada de la biblia viva de kanam-story.

- Fichas de personajes (rol, voz, relaciones), mundo (lugares, organizaciones, lore), reglas (magia, física, leyes).
- Se auto-actualizan desde lo escrito y desde los cambios del chat (patrón biblia viva).
- Consistencia cruzada: el canon checker también valida contra el world-building ("este personaje no puede estar en dos lugares").
- Editable a mano, no solo auto-generado (lección de Sudowrite en kanam-story).

**Release:** v0.5.0. **Éxito:** el mundo se mantiene consistente entre ramas sin que lo mantengas a mano.

## Slice 6 — Export a estándares

**Objetivo:** publicar o meter la historia en un juego.

- Twine HTML (publicable directo), Ink (scripting), JSON (datos crudos).
- Export solo historia o historia + world-building.

**Release:** v0.6.0. **Éxito:** exportás una historia a Twine HTML y se juega en el browser.

## Slice 7 — Simulación de rutas

**Objetivo:** testeo exhaustivo automático del grafo.

- Recorrer todas las rutas posibles (o muestreo inteligente) y reportar: finales alcanzables, ramas muertas, variables que nunca se usan, contradicciones.
- Complementa al canon checker con cobertura total.

**Release:** v0.7.0. **Éxito:** la simulación encuentra un final inalcanzable que el autor no había visto.

---

## Orden y dependencias

- 1 → 2 → 3 → 4 → 5 → 6 → 7. Cada slice depende del anterior (el grafo es la base de todo).
- 5 (world-building) podría adelantarse después de 3 si Gonzo lo pide: la IA de ramas y el world-building se retroalimentan.
- 6 y 7 son independientes entre sí, ambos dependen de 4/5.

## Decisiones abiertas (para resolver en el camino)

- **Visualización de grafo:** canvas propio vs librería (React Flow / d3). Decidir en Slice 1 con un spike corto.
- **Modelo de datos de condiciones:** DSL propio vs JSON estructurado. Decidir en Slice 1.
- **Público:** solo Gonzo (laboratorio) vs producto para autores de gamebooks. No bloquea slices; afecta polish final.
