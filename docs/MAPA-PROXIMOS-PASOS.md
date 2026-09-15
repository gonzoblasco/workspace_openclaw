# MAPA - Próximos pasos

> Foto del horizonte de trabajo al **2026-09-14**, armada sobre fuentes reales (tabla `todos` de
> `memory/memory.db`, `.knowledge/BRIEF.md` de cada proyecto, estado de git), no sobre lo que
> creíamos recordar. Es un **mapa de ruta**, no un backlog: los items accionables viven en la DB.

**Qué NO es este documento:**
- No es el "para qué" de largo plazo: eso es `docs/NORTH.md`.
- No reemplaza `docs/ROADMAP.md`: el ROADMAP describe la **evolución del sistema** por capas
  (infraestructura, pipeline, portfolio). Este mapa ordena **el trabajo pendiente concreto** por
  horizonte de tiempo y por decisión pendiente.
- No es la lista de tareas: eso es `memory/memory.db` (tabla `todos`). Acá los TODOs se citan por
  número para trazabilidad.

**Cómo se mantiene:** al cerrar un ciclo grande o cuando cambia una decisión de fondo. Si un item
se vuelve tarea fechada, vive en la DB y este mapa solo lo referencia.

---

## Horizonte 0 - El retorno inmediato

Lo que está listo para arrancar en la próxima sesión de trabajo, sin decisiones previas.

| Frente | Qué es | Fuente |
|---|---|---|
| **kanam-lab Fase 5** | Juez automático (un modelo tercero evalúa cuál respondió mejor, en lugar del veredicto por extensión) o comparador con estadísticas por modelo | TODO #51 (bifurcación del 2026-09-14) |
| **Formalizar el ciclo de diseño** | Convertir en skill del workspace el método entrenado el 2026-09-14: generar -> iterar -> justificar, con los criterios de verificación (contraste WCAG, tokens, jerarquía) | Idea del cierre del training de diseño, no está en la DB |
| **Portfolio de diseño** | Decidir si las 6 piezas de `projects/kanam-lab/design/propuestas/` (Terrario, 3 direcciones comerciales, copy PLAZA con 7 sweeps, sistema de identidad PLAZA) entran al portfolio como material mostrable | Derivado del ejercicio del 2026-09-14 |

**Señal de listo (Fase 5):** el veredicto de un duelo se registra con un modelo juez, no con la
heurística de extensión.

---

## Horizonte 1 - Profundizar lo que ya anda

Antes de abrir frentes nuevos: dar profundidad a lo que está funcionando.

- **kanam-lab Fase 6** (candidatas): RAG sobre `learnings_enriquecido` completo, exportar duelos a
  markdown para la memoria, métricas agregadas por modelo.
- **Diseño aplicado**: llevar la dirección PLAZA + su copy a un caso real. El ejercicio tiene dueño
  natural (soporteml), pero es decisión de Gonzo convertirlo en trabajo de producto.

---

## Horizonte 2 - Deuda técnica identificada

Items ya diagnosticados, con contexto. Son "quick wins" de higiene y seguridad.

| # | Qué | Por qué importa |
|---|---|---|
| #41 | Verificar `.env` de soporteml (repo público lo trackea en HEAD, desapareció del disco) | Seguridad - credenciales potencialmente expuestas |
| #43 | Fix `memory-catalog-v2.py`: IndexError en `categorize_learning` | Bug en la categorización automática de learnings - toca el núcleo de la memoria |
| #37 | Reparar o quarantinar los scripts `spin-review` (2026-08-30) | Deuda que arrastra desde agosto |
| #42 | Desarchivar `create-with-ai` para pushear commit local legítimo | Higiene de repos |

---

## Horizonte 3 - Proyectos grandes

Los que piden meses de trabajo sostenido, no días. Necesitan foco exclusivo.

- **kanam-studio** (#39, #40): roadmap de slices - grafo -> jugar -> IA de ramas -> canon checker ->
  export. World-building con IA como capa viva durante todo el desarrollo. El proyecto más ambicioso
  del tablero.
- **soporteml** (#36): clonar desde GitHub y mudar el puente Lovable MCP. Producto real con tracción.
- **kanam-pulse** (#33, #35): traer `system-health-check` del MacBook Air; evaluar wrapper nativo
  (Electron/Tauri/RN) solo después de que la web esté sólida.
- **kanam-mind**: la memoria como producto (hoy es infraestructura interna).

---

## Horizonte 4 - Infraestructura y estrategia

Decisiones de fondo que cambian la arquitectura de todo lo demás.

| # | Qué | Decisión de fondo |
|---|---|---|
| #44 | Gateway OpenClaw 24/7 en la Mini + bot Telegram `@kanam_ai_bot` | ¿El bot vive siempre encendido? Cambia la arquitectura operativa |
| #52 | Destino de Radix/shadcn en el stack UI | **CERRADO 2026-09-14.** Estudio `studies/radix-primitives/` completo (5 niveles, 46 topics) y **ADR-048** escrito: adopcion con criterio, reglas de uso y disparadores de revision. Queda como seguimiento del ADR, no como decision abierta. |
| #38 | Cliente MCP real para Lovable (OAuth) | Evaluar integración nativa vs mantener el puente actual |
| #47 | Actualizar skill `model-cata` para cubrir tests de código ejecutables | Trazabilidad de la evaluación de modelos |

---

## Decisiones que son de Gonzo

No se resuelven con más información - son de dirección.

1. **¿kanam-lab sigue siendo laboratorio o se convierte en producto?** El lab ya cumplió su ciclo de
   exploración (4 fases + diseño). Fase 5 puede ser "más experimentos" o "empezar a portar".
2. **¿El diseño se queda como entrenamiento o se vuelve activo (portfolio / servicio)?** El
   2026-09-14 se generaron 6 piezas de nivel agencia - puede ser práctica o un activo.
3. **¿Cuál es el proyecto del próximo trimestre?** kanam-studio (ambición), soporteml (tracción), o
   la infraestructura 24/7 (base para todo lo demás).

---

## Lo que NO haría (criterio explícito)

- **Abrir un proyecto nuevo en paralelo.** kanam-studio necesita foco, no arranque simultáneo con
  todo lo demás. El costo de la dispersión ya está medido en el ROADMAP (capas y prioridad).
- **Sumar features al lab sin cerrar la deuda de la memoria** (#43): la memoria es la base de todo
  lo que sigue, incluido el propio lab.

---

_Actualizado 2026-09-14. Origen: cierre de la sesión de kanam-lab + training de diseño._
