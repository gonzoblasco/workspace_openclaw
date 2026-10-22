# ADR-103: LiteLLM se descarta - la capa de router ya existe en el stack propio

**Fecha:** 2026-10-22
**Estado:** Aceptado (ejecutado 2026-10-22)
**Decisores:** Gonzo / Kanam
**Origen:** sesión 2026-10-20 → 2026-10-22. Gonzo pidió clonar y probar LiteLLM con Ollama; al entender qué era, preguntó *"para qué es LiteLLM? acaso es un modo en el que creamos nuestro propio LLM optimizado?"* y al ver el alcance, *"de lite le veo poco"*.
**Relacionado:** ADR-090 (asignación de modelos por rol), ADR-077/088/089 (pipeline A/B), ADR-099 (LangChain es capa de ejecución, no orquestador), ADR-067 (los ADRs no son de un proyecto)

---

## Contexto

Se clonó `BerriAI/litellm` (v1.107.0) en `~/experiments/litellm`, se configuró con el provider Ollama y se corrió el server en Docker (`localhost:4000`) con Postgres para el dashboard. Se verificó end-to-end: chat completion sobre 4 modelos, streaming SSE, tool calling nativo, SDK de OpenAI con `base_url`, dashboard web con login y generación de virtual keys.

El server funcionaba. La pregunta era si **servía**.

### Lo que LiteLLM es

Un **proxy/gateway**: traduce el formato OpenAI al de cada proveedor y aplica gobernanza (virtual keys, budgets, spend tracking, routing con retry/fallback, guardrails, dashboard). **No entrena, no afina, no crea agentes ni skills.** El `fine_tuning` del repo es un esquema que reenvía a la API de OpenAI/Azure, no training local. El LLM que corre detrás es el mismo, con los mismos pesos.

### Lo medido contra el stack propio

| Capacidad de LiteLLM | Equivalente propio | Estado |
|---|---|---|
| `model_list` + routing | `scripts/model-router.sh` + bloque managed `model-operativo` (ADR-090) | Ya existe, más fino |
| Retry / fallback / balanceo | Pipeline A/B con dos modelos distintos (ADR-077/088/089) | Ya existe |
| Virtual keys y spend tracking | `memory.db` + `docs/CHANGELOG.md` | Ya existe |
| Guardrails y gates | Reglas duras de `AGENTS.md` + scripts de pre-commit | Ya existe |
| Dashboard de admins | `docs/` + dailies | Ya existe |
| Endpoint OpenAI-compatible | El gateway de OpenClaw llama **directo a Ollama** | No usado por nada propio |
| Multi-tenant (key por cliente/proyecto) | - | **Ausente** en el stack propio |

**Verificado:** ningún componente del workspace pasa por LiteLLM. `~/.openclaw/openclaw.json` no lo referencia; el gateway llama directo a `http://localhost:11434`.

**La única dependencia real era potencial:** Onyx declara `LITELLM_PROXY` como provider (`backend/onyx/llm/constants.py:28`), y el pendiente #82 era usar LiteLLM como camino de embeddings contra `/v1/embeddings` de Ollama (`qwen3-embedding:0.6b`, dim 1024). Pero Onyx también acepta `openai_compatible` y `ollama` directo: **el proxy era opcional, no necesario**. Además ese pendiente ya estaba bloqueado por otra causa (límite de RAM de Docker Desktop, 8 GB), con o sin LiteLLM.

## Decisión

**Se descarta LiteLLM. No se adopta en el stack.** Se borra la instalación completa y se registra el descarte.

Justificación, en orden de peso:

1. **Redundancia.** El 90% de lo que ofrece ya existe en el stack, con más detalle y mejor ajuste al proceso propio (ADR-090 + pipeline A/B). Adopting un gateway genérico sería reemplazar control fino por control genérico.
2. **El nombre engaña y cuesta tiempo.** "LiteLLM" invita a pensar "un LLM mejor" o "una IA que crea IAs". La realidad (un proxy) está a un README de distancia. Ese costo de comprensión se paga cada vez que alguien del equipo lo toca.
3. **Costo de operación desproporcionado.** 1,82 GB de imagen + 70 MB de Postgres + 2 containers permanentes por una capa que no se usa.
4. **Fricción real en el build.** Compilar desde el clon exige compilar el crate Rust `litellm-python-bridge` (pyo3) y falló dos veces por `cannot allocate memory` (la VM de Docker tiene 8 GB asignados de 24 GB de host). El build local nunca se completó.
5. **La curva de aprendizaje sí se quedó.** Saber qué es un gateway LLM, cómo se configuran virtual keys y budgets, y dónde están las trampas (login form-encoded, Postgres obligatorio, `host.docker.internal`) es conocimiento transferible a cualquier otro proxy. Eso no se pierde al borrar el repo.

### Lo que se conserva

- El **aprendizaje** (capa de gateway, virtual keys, routing con fallback), registrado acá.
- La **referencia** a Onyx: el camino de embeddings ya verificado es `/v1/embeddings` de Ollama directo, sin proxy intermedio. El pendiente #82 se actualiza en consecuencia.

### Lo que se descarta explícitamente

El multi-tenant (darle una key y un budget a cada cliente/proyecto) queda como **deuda conocida sin cubrir**. Cuando aparezca un cliente real que necesite aislamiento de costos, se re-evalúa la idea desde cero - con la ventaja de saber ahora qué falta y cuánto cuesta.

## Consecuencias

**Positivas:**
- 2 containers y 1,82 GB de imagen menos en una máquina que ya competía por RAM (ver el incidente de milvus del 2026-10-20: `panic: etcdserver: request timed out` por saturación).
- Un pendiente (embeddings de Onyx) queda **desbloqueado de una dependencia**: ya no hace falta un proxy para embeddings.
- Menos superficie que alguien pueda confundir con "la capa de modelos".

**Negativas / deuda:**
- El multi-tenant queda sin resolver (re-evaluar cuando haya un cliente real).
- Si en el futuro hace falta exponer un endpoint OpenAI-compatible con budgets, hay que reconstruirlo (o elegir otro proxy) desde cero. El costo de reconstruir es bajo: un gateway de este tipo es un `if` con reintentos.

**Sobre la caché de build:** `docker buildx du` seguía reportando 32,52 GB de build cache **compartida** (`Shared: true`) con las capas base de los otros 22 proyectos del host. Docker la marca como `Reclaimable: 0B` y `docker builder prune --all` no libera nada. **No se forzó el borrado**: reclaimar esas capas rompería el cache de los demás proyectos. La cache queda como está, y es la lesson: el costo real del build fallido no fue el caché, fue el tiempo y la saturación del host.

## Evidencia

- Sesión 2026-10-20 → 2026-10-22: clonado, configuración, 7 pruebas end-to-end OK (health, `/v1/models`, chat x4, streaming, tool calling, SDK OpenAI, dashboard web).
- Verificación de que nada propio lo usa: `grep -rni litellm` sobre el workspace → sólo menciones en dailies; `~/.openclaw/openclaw.json` → 0 referencias.
- Onyx: `backend/onyx/llm/constants.py:28` (`LITELLM_PROXY = "litellm_proxy"`), `backend/onyx/llm/well_known_providers/llm_provider_options.py:64` (lista dinámica, una opción entre varias).
- Code de LiteLLM: `litellm/proxy/auth/login_utils.py:120-150` (credenciales de UI y fallback al master key), `litellm/proxy/proxy_server.py:18350-18395` (login form-encoded, `DATABASE_URL` obligatorio para la sesión).

## Lecciones

1. **El nombre de una herramienta define el modelo mental que se trae a la primera lectura.** "LiteLLM" suena a modelo; es un proxy. Leer el README antes de la primera decisión es barato.
2. **Un playground puede ser útil sin ser adoptable.** El server funcionó y las 7 pruebas pasaron. Eso no lo convierte en parte del stack. Un descarte bien registrado vale tanto como una adopción.
3. **Lo que un proxy aporta de verdad es multi-tenancy, no inteligencia.** Si el problema es "hablar con varios modelos", ya está resuelto; si el problema es "darle a cada cliente su key y su presupuesto", eso es lo único que faltaba.
4. **Verificar el build temprano.** El `uv sync` con Rust consumió ~45 min en dos intentos fallidos. Un build de humo al principio (o una imagen oficial) habría detectado el costo antes.
