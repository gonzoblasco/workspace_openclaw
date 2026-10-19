# Kanam OS - Evaluacion de la arquitectura por capas propuesta

**Fecha:** 2026-09-15
**Autor:** Kanam, a pedido de Gonzo
**Estado:** Evaluacion. No es una decision - lo que aca se acepte se convierte en ADR.
**Alcance:** Kanam OS = el conjunto del sistema (workspace + gateway + pipeline + memoria + constelacion de proyectos).

---

## Veredicto en una linea

**La arquitectura propuesta describe bien un producto SaaS multi-tenant. Kanam OS no es eso: es un sistema operativo personal, y 4 de sus 5 capas ya existen y funcionan.** El trabajo real no es construir la arquitectura - es **consolidar la capa de orquestacion** (hoy dispersa en 48 scripts sueltos) y **cerrar el unico gap que duele hoy: la ejecucion sin cola durable** (los SIGKILL de Qwen Code a ~3 min).

Adoptarla literalmente seria construir el proyecto numero 11 y violar dos reglas vigentes (`USER.md` 2026-09-14: el precedente no es motivo; `NORTH.md`: dispersion vs capacidad).

---

## Verificacion previa (fuentes reales, no memoria)

Todo lo que sigue se contrasto contra el estado real el 2026-09-15:

| Que se verifico | Fuente | Resultado |
|---|---|---|
| Gateway / auth / puerto | `~/.openclaw/openclaw.json` | `loopback`, puerto 18789, `auth.mode=token` |
| Proveedores LLM | config + `ollama list` | 9 declarados en config (2 locales + 7 cloud); 8 instalados en Ollama (3 locales + 5 cloud) |
| Compatibilidad OpenAI en Ollama | `curl 127.0.0.1:11434/v1/models` | Operativo: expone `/v1/models` |
| RAG / embeddings | `scripts/semantic-search.js`, `memory-search.py` | SQLite + `qwen3-embedding:0.6b`, 1024 dims, coseno |
| Memoria | `memory/memory.db`, `MEMORY.md`, `USER.md` | DB-first, 4 tablas, espejos `.md` regenerables |
| Ruteo de modelos | `model-router.json` + `scripts/model-router.sh` | 6 rutas + overrides sticky; fallback DeepSeek -> GLM -> Kimi |
| Colas / workers | busqueda en `scripts/` | **No hay.** Ejecucion sincrona, recuperacion manual |
| Prompts versionados | `prompts/` | **1 solo archivo** (`complexity-scorer.md`) |
| Keys en frontend | grep `NEXT_PUBLIC_*(KEY|TOKEN|SECRET)` en `projects/` | **0 resultados** |
| Observabilidad | `memory/todos.md` #18, ROADMAP 1.1 | Registrada como pendiente, sin implementar |
| Costos / tokens | config | `cost.input/output = 0` declarado; sin medicion real |

---

## Mapeo capa por capa

### Capa 1 - Frontend

| Propuesta | Estado en Kanam OS | Gap |
|---|---|---|
| Next.js/React con streaming | Control UI de OpenClaw + PWA de los proyectos | Ninguno. Streaming es nativo. |

**Nota:** la regla "nunca consumas la IA desde el frontend" **ya se cumple por construccion**, verificado con grep: cero keys expuestas en cliente. Los proyectos local-first (`kanam-mind`, `kanam-story`, `kanam-studio`) usan IndexedDB + Ollama local, sin keys en absoluto. Es una arquitectura valida y deliberada, no una deuda.

**Unica accion derivada:** dejar escrita la regla para cuando algun proyecto local-first quiera un modelo cloud. Hoy no hay caso.

---

### Capa 2 - API Gateway / BFF

| Propuesta | Estado en Kanam OS | Gap |
|---|---|---|
| Next API Routes / NestJS / FastAPI | **Gateway de OpenClaw** (loopback:18789, token) | La capa existe; la logica detras esta dispersa. |

El gateway ya es el BFF: autentica, rutea, expone tools, maneja sesiones y approval de exec. **No hay que construirlo.**

Lo que falta no es la capa, es la **interfaz**: hoy la logica de pipeline vive en 48 scripts bash/python sin contrato comun (`pipeline-track.sh`, `complexity-scorer.sh`, `model-router.sh`, `memory-*.py`). Se invocan de a uno, ad hoc.

---

### Capa 3 - AI Orchestration Layer

Esta es la capa donde la propuesta aporta mas, y donde el diagnostico real es el mas interesante: **Kanam OS ya tiene todos los componentes, pero desagregados.**

| Componente propuesto | Estado real | Veredicto |
|---|---|---|
| Proveedores (OpenAI/Anthropic/local) | Config OpenClaw + `model-router.json` + `model-router.sh` | **Ya existe, y es mas rico que la propuesta** (ruteo por tipo de tarea + overrides sticky + ADR-090) |
| Prompts versionados | `prompts/` con 1 archivo; el resto embebido en skills y AGENTS.md | **GAP REAL PARCIAL** |
| RAG / Vector DB | SQLite + `qwen3-embedding:0.6b` 1024 dims + busqueda coseno + clustering K-means (`memory-topics.py`) | **Ya existe.** Falta ingesta de fuentes externas (solo ingesta dailies) |
| Tools / function calling | Catalogo nativo de OpenClaw | **Ya existe** |
| Memoria | DB-first (`memory.db`) + capas (MEMORY, USER, dailies, learnings, `.knowledge/`) | **Ya existe. Es la parte mas madura del sistema.** |
| Guardrails / moderacion | Sandbox de contenido externo (AGENTS.md), approval gates de exec, secrets store | **Parcial.** Sin redaccion de PII ni moderacion formal |

**El hallazgo:** la propuesta sugiere construir de cero lo que ya esta construido, y deja sin nombrar lo que realmente falta (prompts versionados, ingesta RAG, guardrails).

---

### Capa 4 - Servicios de datos

| Propuesta | Estado real | Veredicto |
|---|---|---|
| Postgres | SQLite (`memory.db`, `openclaw-agent.sqlite` 499 MB) | **Rechazar el upgrade** |
| pgvector / Pinecone | Vector en SQLite con coseno en Python/JS | **Quedarse.** Correcto a esta escala |
| Redis (cache, rate limit, colas) | No hay | **Gap parcial** - pero Redis seria una dependencia pesada nueva |
| S3 | Archivos locales + git | **No aplica hoy** |

**Por que rechazar Postgres+pgvector:** el volumen es de una persona. SQLite + vector en la misma DB ya funciona y no tiene operacion. Migrar a Postgres seria adoptar una dependencia **porque la arquitectura la sugiere**, no porque resuelva un problema - exactamente el `precedente fabricado` que el ADR-048 y `USER.md` prohiben.

**Lo que si falta y es honesto documentar: el umbral de migracion.** Hoy nadie sabe cuando SQLite dejaria de alcanzar (¿100k vectores? ¿filtros combinados + joins pesados?). Escribir ese umbral es mas util que migrar.

---

### Capa 5 - Workers / Colas

| Propuesta | Estado real | Veredicto |
|---|---|---|
| BullMQ / Celery / RabbitMQ | No hay | **EL GAP MAS GRANDE, y el unico que duele hoy** |

**Por que duele:** el SIGKILL documentado de Qwen Code a ~3 min (`docs/SETUP.md`) es un problema de ejecucion sin cola. El pipeline corre **sincrono**: si el proceso muere, la recuperacion es manual (`pipeline-track.sh resume`). `pipeline-track.sh` ya nace de esto - su header dice literalmente *"Durable pipeline state ... survives crashes (SIGKILL), restarts, and evictions"*. Es un parche de estado, no una cola.

**Pero BullMQ/Celery/RabbitMQ es la respuesta equivocada:** serian tres dependencias de infraestructura nuevas para un sistema de una sola persona. Lo que ya existe y encaja es el **sistema de automations de OpenClaw**: jobs con estado, reintentos, pacing, triggers por evento y wake. Combinado con `pipeline-track.sh`, da una cola durable sin infraestructura nueva.

---

## Lo que se rechaza (y por que)

| Elemento de la propuesta | Por que NO |
|---|---|
| Estructura monorepo `/apps/web`, `/apps/api`, `/apps/ai-worker` | Contradice el modelo de proyectos vigente (ADR-098: *"Sin submodulos. GitHub es la fuente"*; cada proyecto es su propio repo). Kanam OS no es una app: es un workspace + repos independientes |
| Migrar a Postgres + pgvector | Dependencia nueva sin problema que resuelva (regla 2026-09-14) |
| Redis para cache/rate limit | Idem. A esta escala, un indice en SQLite cumple |
| BullMQ / Celery / RabbitMQ | Tres dependencias de infra para un usuario |
| Backend FastAPI separado | El gateway ya cumple ese rol |
| "Empezar con Next.js + API Routes + OpenAI" como MVP | Es un consejo de producto SaaS. Kanam OS **ya es** el sistema maduro, no un MVP |

**El concepto que SI se rescata de la propuesta estructural:** `/packages/ai-core` o `/lib/ai`. No como monorepo, sino como **modulo compartido** entre proyectos cuando 2+ lo necesiten.

---

## Arquitectura resultante para Kanam OS

```
Proyectos (Next.js / PWA / local-first)
        │
        ▼
Gateway de OpenClaw  [YA EXISTE]  <- BFF real: auth, sessions, tools, approval
        │
        ▼
Capa de Orquestacion IA  [EXISTE, DESAGREGADA -> CONSOLIDAR]
  ├─ Proveedores ......... model-router.json + ADR-090   [OK]
  ├─ Prompts versionados . prompts/ (1 archivo) -> [CONSTRUIR]
  ├─ RAG ................. SQLite + qwen3-embedding              [OK]
  │                        + ingesta externa -> [CONSTRUIR]
  ├─ Tools ............... catalogo OpenClaw                     [OK]
  ├─ Memoria ............. memory.db DB-first                    [OK - maduro]
  └─ Guardrails .......... sandbox + approvals                   [OK parcial]
        │
        ▼
Datos  [YA EXISTE -> NO MIGRAR]
  SQLite (memory.db + agent.sqlite) + vector en DB + archivos en git
        │
        ▼
Colas / Workers  [CONSTRUIR - unico gap que duele hoy]
  automations de OpenClaw + pipeline-track.sh (NO BullMQ/Celery)
```

---

## Plan por fases (ordenado por dolor resuelto / esfuerzo)

| # | Fase | Que resuelve | Esfuerzo | Horizonte NORTH |
|---|---|---|---|---|
| 0 | **Cola durable sobre automations** | SIGKILL de Qwen, recuperacion manual, pipeline interrumpido | Medio | H0/H1 - capacidad |
| 1 | **Observabilidad minima** | ROADMAP 1.1 lo pide; `pipeline-track` **ya captura** start/endTime, iterations, regressions - solo falta reportar | Bajo | H1 |
| 2 | **Prompts versionados** | Prompts hoy embebidos en skills/AGENTS.md; sin version ni eval | Medio | H1 |
| 3 | **Cache semantica** | Embeddings ya existen; el lookup previo a la llamada es barato | Bajo | H1 |
| 4 | **Ingesta RAG externa** | Hoy el RAG solo lee dailies | Medio | H1 |
| 5 | **Medicion de costos reales** | Config declara costo 0; no hay tokens/consumo | Bajo | H1 |
| 6 | **`lib/ai` compartido** | Solo cuando 2+ proyectos lo necesiten | Alto | H2 |

**Regla de la fase 6:** no se construye `lib/ai` de forma anticipada. Se extrae **despues** de que dos proyectos dupliquen el mismo codigo. Construirlo antes es la definicion de dispersion.

---

## Como pasa el filtro del NORTH

Las tres preguntas de `docs/NORTH.md`:

1. **¿A que horizonte sirve?** Fases 0-5 → H1 (Kanam como sistema que se sostiene). La fase 0 tambien sirve a H0: un pipeline que no se cae ahorra tiempo de trabajo real, que es el objetivo del Horizonte 0.
2. **¿Es nueva capacidad o dispersion?** Las fases 0-5 son **capacidad sobre el sistema existente** (consolidar lo que ya hay). Construir la arquitectura propuesta completa - monorepo, Postgres, Redis, BullMQ - seria **dispersion**: un proyecto nuevo de infraestructura.
3. **¿La puedo sostener?** Si, con una salvedad: son 6 fases, y la busqueda laboral sigue activa hasta el 01/10. Fase 0 y 1 son las unicas defendibles **antes** del arranque del trabajo (01/10). Las demas esperan.

**Veredicto del filtro:** no se abre proyecto nuevo. Se consolidan capas existentes, empezando por la cola.

---

## Decisiones abiertas (para ADR)

Ninguna de estas esta resuelta. Cada una, al cerrarse, merece un ADR:

1. **Cola durable:** ¿automations de OpenClaw como mecanismo oficial de la cola del pipeline A/B, o se mantiene el modelo sincrono? (bloquea fases 0-1)
2. **SQLite como capa de datos definitiva:** cerrar por ADR que Kanam OS **no** migra a Postgres/pgvector, y dejar escrito el umbral que si lo justificaria.
3. **Prompts como codigo:** formato, ubicacion (`prompts/` vs por proyecto) y si llevan evals asociadas.
4. **Umbral de extraccion de `lib/ai`:** la regla que dispara construir el paquete compartido.
5. **Observabilidad minima:** que se mide (latencia, SIGKILL, consumo por modelo) y donde se persiste.

---

## Notas de creacion

- El pedido original fue evaluar una arquitectura por capas generica (tipica de guias de producto con IA).
- La evaluacion se hizo contra fuentes reales del sistema el 2026-09-15, no contra la memoria de la sesion.
- Principio aplicado: **no inventar dependencias ni problemas**. Cada gap nombrado tiene su evidencia (grep, archivo, config, TODO existente).
- Lo que se rechaza se rechaza explicando **que problema no resuelve**, no porque sea "moderno de mas".
