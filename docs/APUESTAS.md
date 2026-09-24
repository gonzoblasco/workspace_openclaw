# APUESTAS.md - Registro de apuestas sobre la mesa

**Registrado:** 2026-09-24 (sesión webchat)
**Contexto:** decisión tomada al cerrar la Fase 4 de `langchain-starter`. Gonzo pidió registrar la lista de apuestas con su orden de prioridad y poder volver a esta etapa sin perder estado.
**Razonamiento completo:** `LANGCHAIN_STRATEGY.md` (sección 6) + el análisis del 2026-09-24.

---

## Qué es este documento

- Es el **registro durable** de las apuestas evaluadas, su orden de prioridad y el estado del mundo al momento de decidir.
- **No** es el backlog: los items accionables viven en `memory/memory.db` (tabla `todos`, espejo `memory/todos.md`).
- **No** es el roadmap del sistema: eso es `docs/ROADMAP.md`. Esto es la lista de apuestas de producto/herramienta y su orden.
- **Cómo se mantiene:** se agrega una fila cuando aparece una apuesta nueva. El orden se cambia con fecha y motivo, nunca en silencio.

---

## Las cuatro capas (para leer la tabla sin confusión)

| Capa | Qué es | Se vende? | Ejemplo |
|---|---|---|---|
| **Infraestructura** | Habilita lo demás. No es producto. | No | `langchain-starter` |
| **Uso interno** | Mejora cómo trabajamos. Riesgo bajo. | No (valor = tiempo) | `kanam-insight`, `kanam-os` |
| **Producto** | Alguien paga. Riesgo real de mercado. | Si | `soporteml-v4`, `kanam-fixer` |
| **Personal** | Vale por sí mismo, no por facturar. | No | `kanam-story`, `kanam-studio` |

---

## Apuestas, en orden de prioridad

**Prioridad confirmada por Gonzo el 2026-09-24: 1 a 3.** El resto queda listado sin lugar asignado, a decidir cuando lleguemos.

| # | Apuesta | Capa | Capacidad que usa | Activo que ya existe | Quién paga |
|---|---|---|---|---|---|
| **1** | **kanam-insight** | Uso interno | RAG multi-fuente sobre `.knowledge/` | 12+ proyectos con ADRs, HANDOFF, STATUS | Nosotros (tiempo) |
| **2** | **soporteml-v4** | Producto | RAG + agentes sobre KB | backend de v3 verificado, KB y autopilot ya en el MVP | Vendedores de MeLi |
| **3** | **kanam-fixer** | Producto | Agentes consultando el historial de anuncios | aserción sobre el anuncio real, ciclo 0.0.2 (MCP) abierto | Equipos con a11y en CI |
| - | kanam-os | Uso interno | RAG + NL a SQL | `memory.db` con toda la memoria | Nosotros (tiempo) |
| - | Servicio de KB a medida | Producto | `langchain-starter` generalizado | Fase 7 (template) no iniciada | Pymes con documentación |
| - | kanam-story / kanam-studio | Personal | Co-writer con memoria larga | v0.17.0, 440 tests, roadmap completo | B2C (muy competido) |

### Por qué ese orden

**1. kanam-insight.** Es la que mejor relación valor/riesgo tiene y la que valida la capacidad construida. Su propio BRIEF define el problema: *"Gonzo tiene ~12 proyectos activos. Cada uno tiene su `.knowledge/` con ADRs y decisiones. El problema: nadie cruza esa información. Patrones viven y mueren en silos."* Eso es RAG multi-fuente, y ya tenemos ingesta, chunking y retrieval funcionando: solo hay que apuntarlos a los `.knowledge/`. El "Pattern Radar" es retrieval + síntesis; el "Handoff Synthesizer" lo hacemos a mano hoy. Riesgo cero, valor inmediato, y mejora nuestro trabajo (el objetivo declarado).

**2. soporteml-v4.** La apuesta comercial más sólida por un motivo frío: el MVP ya incluye bandeja, KB y autopilot, y el backend de v3 está verificado de punta a punta. Un copiloto que responde al comprador usando la KB del vendedor no es una feature nueva, es activar lo que ya está modelado. Mercado que paga, no solo tecnología.

**3. kanam-fixer.** El diferenciador más defendible y el menos explotado como producto. La distinción técnica es real: axe-core mira atributos en el DOM; kanam-fixer mira **lo que el lector de pantalla efectivamente anuncia**. El ciclo 0.0.1 cerró con un hallazgo valioso (radix #4109: DOM correcto, tests unitarios verdes, anuncio ausente), algo que ninguna herramienta genérica detecta.

### Por qué el resto no está arriba

- **kanam-story / kanam-studio:** el producto está mejor terminado que el promedio, pero su BRIEF registra tres intentos fallidos de clonar Sudowrite. Eso no es fracaso técnico, es señal de mercado: es B2C, muy competido, y el ganador no suele ser el mejor software. Como proyecto personal tiene todo el sentido; como apuesta comercial, no va primera.
- **Servicio de KB genérico:** es el camino más rápido a construir diez cosas que nadie pidió. Requiere primero uso interno y estabilización.

---

## Descartado explicitamente

**La "enciclopedia de accesibilidad" como encuadre.** Se descartó el 2026-09-24: un RAG que responde sobre WCAG ya existe repetidas veces, no es defendible. El encuadre correcto del dominio a11y es **servicio de auditoría sobre el anuncio real**, que es exactamente `kanam-fixer` (prioridad 3), no un chatbot de documentación.

**Nota de método:** la sección 6 de `LANGCHAIN_STRATEGY.md` había titulado esto como "primera apuesta comercial", lo que sugería que era la única o la principal. No lo era. Corregido en ese documento.

---

## Principio rector (aplica a todas)

**No construimos un producto de IA genérico.** Primero la herramienta que mejora nuestro trabajo; cada capacidad que se estabiliza internamente, se empaqueta. El orden es: uso interno -> estabilización -> aislamiento multi-cliente -> exportación. Saltearse el uso interno produce productos que nadie probó.

---

## Punto de retorno (restore point)

Esta etapa quedó sellada para poder volver sin perder nada del estado actual.

- **Tag git:** `etapa-2026-09-24-pre-kanam-insight`

Para volver a este estado exacto:

```bash
cd ~/.openclaw/workspace
git fetch --tags
git checkout etapa-2026-09-24-pre-kanam-insight   # inspeccionar (modo detached)
git switch -c volver-a-etapa-2026-09-24            # o crear rama desde el tag para trabajar
```

Para volver sin perder el trabajo posterior: `git checkout` del tag es solo lectura; el trabajo nuevo vive en `main`, asi que inspeccionar el tag no borra nada. Para ver que cambio despues: `git log --oneline etapa-2026-09-24-pre-kanam-insight..main`.

**Qué cubre el tag:** todo lo trackeado por el repo del workspace (memoria, docs, skills, scripts, `.knowledge/` de cada proyecto).
**Qué NO cubre:** el codigo de los proyectos (viven en sus propios repos de GitHub; `langchain-starter` aun no tiene repo propio) y los datos locales (`.env`, `*.db` fuera de memoria, `venv/`).

---

*Registrado el 2026-09-24. Primera ejecucion: `kanam-insight`, prioridad 1.*
