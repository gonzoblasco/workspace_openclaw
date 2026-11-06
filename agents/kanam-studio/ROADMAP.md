# ROADMAP.md - Kanam STUDIO 🎨

**Versión actual:** v0.2.1
**Objetivo:** v0.6 - Comunicadora con demanda propia
**Última revisión:** 2026-11-06
**Dueño:** kanam-studio (autoría) · Kanam CORE (gobierno)

---

## Principio rector

> **Antes de agregar una capacidad, se pregunta: ¿esto pertenece a un pipeline
> que ya existe?** El default es extender. Crear una skill nueva exige justificar
> por qué ningún pipeline existente puede absorberla.

Este principio reemplaza la lógica del v0.1 (acumular). Nació de la corrección
de Gonzo el 2026-11-06 y de un error mío que queda registrado abajo.

---

## Corrección de ruta (2026-11-06)

Propuse una skill nueva, `voice-calibrator`, para convertir "suena a Gonzo" en
reglas medibles. **Ya existe.** `docs/voz-gonzo.md` tiene:

| Lo que propuse crear | Lo que ya existe |
|---|---|
| Corpus etiquetado | 3 casos con borrador / edición final / qué cambió / patrón |
| Reglas medibles | 13 reglas consolidadas |
| Loop de aprendizaje | Paso 7 de `voz-gonzo`: registrar cada edición de Gonzo |
| Validación | Criterio de "reglas aplicadas o motivo explícito" |

Además, `content-serializer` tiene su propio **Phase 0: Personal brand voice**
con reglas de tono duras, y `copy-editing` un Sweep 2 de Voice and Tone.
**Tres lugares definen la voz, ninguno se referencia entre sí.**

Ese es el problema real: no falta una cuarta definición, sobran tres sin dueño.

---

## Diagnóstico medido (2026-11-06)

| Dato | Valor | Implicancia |
|---|---|---|
| Sesiones en disco | 3 (30/9, 7/10, 28/10) | Última actividad hace 9 días |
| Archivos en `memory/` | 0 | Sin memoria entre sesiones |
| `editorial-guidelines.md` | No existe | Prometido en v0.1, nunca ejecutado |
| Skills operativas | 7 | Todas con `user-invocable: false` |
| Definiciones de voz | 3 (voz-gonzo, serializer Phase 0, copy-editing Sweep 2) | Duplicadas, sin jerarquía |
| Skills que se referencian entre sí | 0 de 7 | Ningún pipeline real |
| `thinkingDefault` | `off` | Copy fino sin reflexión |

**Causa raíz:** no faltan capacidades. Faltan **handoffs entre ellas** y una
**jerarquía de verdad**. Cada skill es una isla que arranca de cero.

---

## Arquitectura objetivo: 3 pipelines, 7 skills

En vez de skills nuevas, se conectan las que existen en tres flujos con
entrada, etapas y salida verificable. Toda capacidad futura entra como etapa.

```
PIPELINE A - Comunicación externa de marca
  material aprobado -> [voz-gonzo: reglas] -> [content-serializer: adaptación
  y calendario] -> [copy-editing: 7 sweeps] -> BORRADOR -> aprobación humana

PIPELINE B - Técnico hacia afuera (GitHub, docs, soporte técnico)
  problema / issue -> [oss-issue-preflight] -> [oss-contribution] ->
  [oss-pr-verification] -> [i18n-expert si hay UI] -> BORRADOR -> aprobación

PIPELINE C - Carrera
  JD -> [cv-tailor] -> [mock-interview-drill] -> material de carrera
```

Cada pipeline tiene **una fuente única de voz**, **etapas con criterio de
entrada/salida**, y **una sola puerta de aprobación al final**.

---

## Fase 0 - Memoria mínima (esta semana, costo cero)

Sin memoria, todo lo demás se reescribe. Es lo único que va primero sí o sí.

| # | Entregable | Criterio de listo |
|---|---|---|
| 0.1 | `memory/editorial-guidelines.md` | Palabras vetadas, tono aprobado y ejemplos por proyecto |
| 0.2 | `memory/editorial-log.md` | Una entrada por pieza: qué elegí, por qué, qué cambió Gonzo |
| 0.3 | `AGENTS.md` lo lee al arrancar | Primera instrucción del paso 1 |

**No crear nada más en memoria.** `voz-gonzo` ya cubre la voz; esto cubre
lo específico de proyecto, que es otra cosa.

---

## Fase 1 - Unificar la voz (CONSOLIDAR, no crear) ✅ 2026-11-06

**Objetivo:** una sola fuente de verdad, y que las demás la referencien.

| # | Acción | Estado | Resultado |
|---|---|---|---|
| 1.1 | `docs/voz-gonzo.md` se declara canónico | ✅ | Nota en AGENTS.md paso 1 lo nombra "fuente única y canónica" |
| 1.2 | `content-serializer` Phase 0 referencia, no duplica | ✅ | "Where the voice lives" apunta a `voz-gonzo`; conserva solo la modulación por tipo de post |
| 1.3 | `copy-editing` Sweep 2 referencia | ✅ | Sweep 2 deja de definir tono; apunta a `voz-gonzo` + `editorial-guidelines` |
| 1.4 | Extender `voz-gonzo` a posts públicos | ✅ | Alcance ampliado 2026-11-06 con tabla de modulación de marca (deep-dive / anuncio / opinión / CTA) |
| 1.5 | Cargar casos con texto ya escrito | ⚪ pendiente | Tus artículos y READMEs como casos nuevos, si los aprobás |

**Decisión 1.4 resuelta con Gonzo (2026-11-06):** los posts públicos usan la
voz global modulada, no un registro aparte. Fundamento: el contenido de
branding sale de artículos, READMEs y PRs, que ya están en esa voz.

**Regla de precedencia instalada:** `voz-gonzo` gana sobre cualquier duplicado.
Si un skill contradice el canónico, se corrige el skill.

## Fase 2 - Conectar los pipelines (handoffs, no capacidades)

Acá está el retorno real. Hoy ninguna skill sabe qué recibe ni qué entrega.

| # | Entregable | Criterio de listo |
|---|---|---|
| 2.1 | Contrato de entrada/salida por skill | Cada SKILL.md declara: qué recibe, qué produce, quién lo consume |
| 2.2 | Pipeline A conectado | Un material -> posts -> edición -> borrador, sin reexplicar contexto |
| 2.3 | Pipeline B conectado | `oss-issue-preflight` -> `oss-contribution` -> `oss-pr-verification` con estado pasándose |
| 2.4 | Router en AGENTS.md | Qué frase dispara qué pipeline, con casos concretos |
| 2.5 | `user-invocable: true` | Donde corresponda, para que aparezcan en el menú |

**Pipeline C** (carrera) no se conecta ahora: no hay uso demandado.

---

## Fase 3 - Disparador autónomo

| # | Entregable | Criterio de listo |
|---|---|---|
| 3.1 | Heartbeat propio | Reviso `projects/`, `oss/`, `docs/OSS-TRACKER.md` y propongo |
| 3.2 | Salida con filtro | Brief de 3 líneas, pasa por `voz-gonzo` antes de salir. Propongo, no publico |
| 3.3 | Cosecha automática | Artículos y READMEs existentes entran solos a Pipeline A como candidatos |

**Bloqueado por Fase 1:** un heartbeat sin voz unificada propone ruido.

---

## Fase 4 - Capacidad nueva (sólo si un pipeline no la absorbe)

Se evalúa una por una. Cada una exige decir **qué pipeline no puede absorberla**.

| Candidata | ¿Pipeline que la absorbe? | Veredicto |
|---|---|---|
| `post-ship-brief` | Pipeline A, como disparador de entrada | **Etapa, no skill** |
| `doc-polish` | Pipeline A sobre READMEs, con `copy-editing` | **Etapa, no skill** |
| `inbox-triage` | Pipeline B, como entrada programada | **Etapa, no skill** |
| `support-response-writer` v2 | Pipeline propio de soporte, hoy sin volumen | **No tocar** |

**Resultado: 0 skills nuevas.** Las tres candidatas del v0.2 se convierten en
etapas de pipeline. Eso es exactamente lo que pediste.

---

## Decisiones de config (requieren tu sí, separadas)

| # | Cambio | Mi recomendación |
|---|---|---|
| C1 | `thinkingDefault: off` -> `high` | **Sí.** Cuello de botella declarado en AGENTS.md |
| C2 | `subagents.allowAgents: []` -> `["kanam-mind"]` | **No.** Rompe el contrato de handoff que escribiste |
| C3 | Heartbeat en `kanam-studio` | **Después de Fase 1**, no antes |

Ninguna se ejecuta sin aprobación explícita para esa acción.

---

## Red lines (sin cambios)

- No publico, envío ni posteo hacia afuera sin tu aprobación para esa acción.
- No invento citas, estadísticas ni fechas. Verifico con `web_fetch`.
- No cruzo a investigación (MIND) ni a código (DEV).
- No diseño.

---

## Cómo se mide

| Métrica | Hoy | Meta v0.6 |
|---|---|---|
| Skills nuevas creadas | — | **0** |
| Skills referenciando la voz canónica | 0 de 7 | 7 de 7 |
| Pipelines con contrato entrada/salida | 0 de 3 | 2 de 3 |
| Sesiones activas por semana | 0 | >=3 |
| Veces que reexplicás el tono | Cada tarea | 0 |
| Piezas publicadas desde material existente | 0 | >=4 |

---

## Próximo paso concreto

Fase 0.1: escribir `memory/editorial-guidelines.md` como **borrador para
corrección**. Cero scripts, cero config, reversible. Es el insumo de todo
lo demás.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
