# 🌿 Kanam's Crew: Catálogo de Soluciones

> **📌 Este es el catálogo de CASOS DE USO** (por problema, independiente de repos). Para decisiones y estado consolidado, ver **`DECISIONS.md`**. Para la ficha de cada repo analizado, ver **`crew-resources.md`**.

**No es un directorio de links. Es un registro de soluciones por necesidad.**

Cada entrada responde a: *"¿qué problema resuelve?"*, *"¿cómo se aplica en nuestro setup?"* y *"¿nos sirve?"*. Cuando surja una necesidad futura, se busca acá por el **problema** (columna Necesidad), no por el nombre del repo.

**Fuente primaria:** [hesamsheikh/awesome-openclaw-usecases](https://github.com/hesamsheikh/awesome-openclaw-usecases) (42 casos) - filtrado y traducido a nuestro contexto.

**Leyenda:**
- 🟢 **Aplicable ya** - tenemos el contexto para implementarlo cuando lo necesitemos.
- 🟡 **A futuro** - requiere una condición previa (un proyecto, una herramienta, un canal).
- ⚪ **Descartado** - no aplica a nuestro perfil (con la razón).

---

## 1. Orquestación de Agentes y Proyectos

### 🟢 Factory de Investigación / Contenido
- **Origen:** *Multi-Agent Content Factory* + *Multi-Agent Specialized Team*
- **Necesidad que resuelve:** Producir trabajo complejo sin que un solo agente simplifique o se salte pasos.
- **Mecanismo:** Cadena de subagentes donde el output de uno alimenta al siguiente (`research → análisis → síntesis`). Cada eslabón tiene una misión estrecha. Se revisa por canal/carpeta, no todo mezclado.
- **Aplicación Kanam:** Es el patrón que ya usamos parcialmente en el pipeline A/B. Extensible a "Investigation Factories" (Explorador → Analista → Sintetizador) para temas complejos.

### 🟢 Estado de Proyecto Dirigido por Eventos
- **Origen:** *Autonomous Project Management (STATE.yaml)* + *Project State Management*
- **Necesidad que resuelve:** Saber el estado real de un proyecto sin planillas estáticas que se desactualizan.
- **Mecanismo:** Un archivo de estado machine-readable (`.yaml`) que los subagentes leen y actualizan. Reemplaza el Kanban: el tablero se genera del estado, no al revés.
- **Aplicación Kanam:** Es exactamente lo que hace `scripts/pipeline-track.sh` pero como contrato entre agentes. Candidato a formalizar el handoff DEV↔OPS↔CORE.

### 🟢 Pre-Build Idea Validator (Preflight)
- **Origen:** *Pre-Build Idea Validator*
- **Necesidad que resuelve:** No construir algo que ya existe y está mantenido (regla OSS Preflight de AGENTS.md).
- **Mecanismo:** Antes de escribir código, escanear GitHub, HN, npm, PyPI y Product Hunt. Si el espacio está saturado → parar; si está abierto → seguir.
- **Aplicación Kanam:** Automatiza una regla que hoy aplicamos a mano. Encaja como skill previa a cualquier `sdd-agent-loop` o arranque de proyecto.

### 🟡 n8n Workflow Orchestration
- **Origen:** *n8n Workflow Orchestration*
- **Necesidad que resuelve:** Llamar APIs externas sin que el agente toque credenciales.
- **Mecanismo:** El agente dispara webhooks a workflows de n8n; las credenciales viven en n8n, visuales y desconectables.
- **Aplicación Kanam:** Isolación de secretos para integraciones. Relevante si sumamos APIs de terceros (pagos, mail). Requiere levantar n8n.

---

## 2. Investigación y Conocimiento

### 🟢 Knowledge Base (RAG) personal
- **Origen:** *Personal Knowledge Base (RAG)* + *Second Brain*
- **Necesidad que resuelve:** Recuperar lo que leímos tirando URLs/notas al chat, con búsqueda semántica.
- **Mecanismo:** Ingesta de URLs/tweets/artículos → embeddings → consulta en lenguaje natural.
- **Aplicación Kanam:** Puente directo con Kanam Mind. Nuestro `memory.db` es SQL; esto le agrega capa vectorial.

### 🟢 Semantic Memory Search
- **Origen:** *Semantic Memory Search*
- **Necesidad que resuelve:** Encontrar recuerdos por significado, no por texto exacto.
- **Mecanismo:** Embeddings sobre los `.md` de memoria + retrieval híbrido + auto-sync.
- **Aplicación Kanam:** Mejora directa de `memory_search`. Complementa (no reemplaza) la DB SQLite como fuente de verdad.

### 🟡 Research Discovery académico
- **Origen:** *arXiv Paper Reader* + *HF Papers Research Discovery* + *LaTeX Paper Writing*
- **Necesidad que resuelve:** Seguir papers sin abrir cinco pestañas.
- **Mecanismo:** Fetch por ID, triage por upvotes, deep-read, y escritura de papers con preview PDF.
- **Aplicación Kanam:** A futuro, si arrancamos una línea de investigación formal o un proyecto con base académica.

### 🟡 Market/Product Research Factory
- **Origen:** *Market Research & Product Factory*
- **Necesidad que resuelve:** Validar demanda real antes de construir un producto.
- **Mecanismo:** Minar Reddit/X por pain points ("Last 30 Days" skill) → construir MVP que los resuelva.
- **Aplicación Kanam:** Se activa con el ciclo `product-definition-cycle`. Complementa al Pre-Build Validator.

---

## 3. Memoria y Contexto
Ver sección 2 (Knowledge Base + Semantic Memory). Son las dos piezas que apuntan a Kanam Mind.

---

## 4. Automatización de Contenido

### 🟢 Content Factory (pipeline de 3 eslabones)
- **Origen:** *Multi-Agent Content Factory* (ver sección 1)
- **Aplicación Kanam:** Research → Writing → Visual. Adaptable a cualquier formato (hilos, newsletters, guiones, docs).

### 🟡 Content Pipelines específicos
- **Origen:** *YouTube Content Pipeline* + *Podcast Production Pipeline* + *AI Video Editing*
- **Necesidad:** Scout de ideas, research, show notes, edición de video por lenguaje natural.
- **Aplicación Kanam:** Solo si STUDIO arranca un canal/podcast. Hoy no hay ese proyecto.

### ⚪ X / Twitter
- **Origen:** *X Account Analysis* + *X/Twitter Automation*
- **Descartado:** No gestionamos una cuenta de X como canal operativo hoy.

---

## 5. Productividad Personal / Asistente

### 🟢 Digest de información
- **Origen:** *Daily Reddit Digest* + *Daily YouTube Digest* + *Multi-Source Tech News Digest* + *Custom Morning Brief*
- **Necesidad:** Consumir info relevante sin entrar a cada app.
- **Mecanismo:** Cron que escanea fuentes, puntúa por calidad/relevancia, entrega un briefing.
- **Aplicación Kanam:** Fácil de montar. Decime qué fuentes y a qué hora, y queda como job.

### 🟢 Automatización de reuniones
- **Origen:** *Automated Meeting Notes & Action Items* + *Second Brain*
- **Necesidad:** Convertir transcripts en resumen + tareas asignadas.
- **Mecanismo:** Transcript → estructura → crear tareas en el tracker.
- **Aplicación Kanam:** Encaja con los transcripts y el `todos` de `memory.db`. Requiere que haya reuniones grabadas.

### 🟡 Inbox De-clutter + Personal CRM
- **Origen:** *Inbox De-clutter* + *Personal CRM* + *Local CRM Framework*
- **Necesidad:** Resumir mails/newsletters y trackear contactos desde mail/calendario.
- **Aplicación Kanam:** Requiere acceso a mail/calendario. Útil si conectamos esos canales.

### 🟡 Dashboard dinámico + Todoist
- **Origen:** *Dynamic Dashboard* + *Todoist Task Manager*
- **Necesidad:** Visibilidad en tiempo real del estado de agentes/tareas (transparencia).
- **Aplicación Kanam:** Ya tenemos `dashboard` y widgets. Todoist sería un sink de logs de progreso - evaluar si vale sobre nuestra DB.

### ⚪ Descartados (perfil personal, no de trabajo)
- *Health & Symptom Tracker*, *Habit Tracker*, *Family Calendar & Household Assistant*, *Event Guest Confirmation*, *Phone-Based Assistant*, *Phone Call Notifications*.

---

## 6. Ops e Infraestructura

### 🟢 Self-Healing Home Server
- **Origen:** *Self-Healing Home Server*
- **Necesidad:** Mantener la Mac Mini sana (SSH, cron, auto-reparación).
- **Mecanismo:** Agente always-on con acceso SSH que monitorea y repara servicios.
- **Aplicación Kanam:** Alineado al rol OPS. Cuidado: máximo cuidado con accesos SSH (Red Lines).

### 🟡 Multi-Channel Asistente / Customer Service
- **Origen:** *Multi-Channel Personal Assistant* + *Multi-Channel AI Customer Service*
- **Necesidad:** Rutear tareas por Telegram/Slack/mail desde un solo agente.
- **Aplicación Kanam:** Parcial - ya operamos por webchat. Se activa si sumamos más canales o si un proyecto necesita atención al cliente.

### 🟡 OpenClaw as Desktop Cowork
- **Origen:** *OpenClaw as Desktop Cowork*
- **Necesidad:** UI unificada + reparación remota del Gateway.
- **Aplicación Kanam:** Referencia para el setup del Gateway. Ya cubierto en gran parte por la Control UI.

### ⚪ Polymarket Autopilot
- **Descartado:** Trading en mercados de predicción. Fuera de objetivo y de perfil de riesgo.

---

## 7. Tooling, Memoria y Gobernanza (capa infraestructura)

Filtrado de [vincentkoc/awesome-openclaw](https://github.com/vincentkoc/awesome-openclaw) - el índice técnico. Acá el criterio es: *¿esta herramienta cubre un hueco que tenemos hoy?*

> ⚠️ **Todos son comunitarios (no oficiales).** Tratar como untrusted: revisar código y permisos antes de instalar. Los `🎖️` del índice original son los únicos oficiales.

### 🟢 Gobernanza y Seguridad
- **[DNYoussef/guardspine-openclaw](https://github.com/DNYoussef/guardspine-openclaw)**
  - **Necesidad:** Enforcement de las Red Lines con tiers de riesgo y deny-by-default.
  - **Por qué nos sirve:** Nuestro `AGENTS.md` tiene reglas duras pero el enforcement es manual + `check-agent-skill-boundary.py`. Esto agrega una capa de gating declarativa. Candidato serio.
- **[onecli/onecli](https://github.com/onecli/onecli)**
  - **Necesidad:** Manejar credenciales sin exponerlas al agente.
  - **Por qué nos sirve:** Gateway HTTP en Rust que inyecta secrets sin exponer las API keys. Alinea con la regla "datos locales nunca al git" y con `secrets`.
- **[pors/skill-audit](https://github.com/pors/skill-audit)**
  - **Necesidad:** Validar y endurecer la calidad de las skills.
  - **Por qué nos sirve:** Tenemos `skills-collection-integrity` y el `skill-catalog-budget`. Esto es el toolkit complementario para auditar.

### 🟢 Memoria y Contexto
- **[tobi/qmd](https://github.com/tobi/qmd)**
  - **Necesidad:** Memoria markdown-native con workflows.
  - **Por qué nos sirve:** Es el más cercano a nuestro modelo híbrido (`.md` + `memory.db`). Complementa lo de `Semantic Memory Search`.
- **[MemTensor/MemOS](https://github.com/MemTensor/MemOS)** + **[NevaMind-AI/memU](https://github.com/NevaMind-AI/memU)**
  - **Necesidad:** Capa de memoria persistente con retrieval.
  - **Por qué nos sirve:** Alternativas a evaluar si Kanam Mind necesita más que SQLite + embeddings.
- **[vincentkoc/openamnesia](https://github.com/vincentkoc/openamnesia)**
  - **Necesidad:** Cold-starts fuertes extrayendo memoria de actividad real.
  - **Por qué nos sirve:** Ataca justo el problema de "despierto fresco cada sesión".

### 🟢 Observabilidad y Costos
- **[bokonon23/clawdbot-cost-monitor](https://github.com/bokonon23/clawdbot-cost-monitor)**
  - **Necesidad:** Ver en qué se va el gasto de tokens.
  - **Por qué nos sirve:** Coherente con ADR-053 ("no gastar recursos innecesarios").
- **[crshdn/mission-control](https://github.com/crshdn/mission-control)** + **[clawdeckio/clawdeck](https://github.com/clawdeckio/clawdeck)**
  - **Necesidad:** Visibilidad de orquestación multi-agente.
  - **Por qué nos sirve:** Nuestro pipeline A/B y los spawns corren a ciegas. Un dashboard ayuda a debuggear.

### 🟡 Expansión de capacidades
- **[lekt9/unbrowse-openclaw](https://github.com/lekt9/unbrowse-openclaw)**
  - **Necesidad:** Convertir una web/API en una skill capturando el tráfico.
  - **Por qué nos sirve:** Genera skills desde tráfico real, sin escribir el scraper a mano. Útil pero a validar.
- **[Helms-AI/openclaw-mcp-server](https://github.com/Helms-AI/openclaw-mcp-server)**
  - **Necesidad:** Exponer las tools del Gateway por MCP.
  - **Por qué nos sirve:** Abre la puerta a conectar otros clientes al Gateway.
- **[Enderfga/openclaw-claude-code-skill](https://github.com/Enderfga/openclaw-claude-code-skill)**
  - **Necesidad:** Integrar Claude Code por MCP.
  - **Por qué nos sirve:** Usamos Claude Code vía Ollama en el pipeline; esto formaliza el puente.

### ⚪ Descartados (con razón)
- **Alternative Architectures** (nanoclaw, tinyclaw, picoclaw, microclaw, supaclaw, ironclaw, carapace...): implementaciones alternativas. Nosotros corremos el core oficial; migrar no es un objetivo.
- **Community Channels** (Moltbook, Clawk, 4claw, Shellmates...): redes de agentes. Solo lectura por regla de sandbox; no integramos.
- **Plugin de canales regionales** (WeCom, QQ, DingTalk, Feishu): no usamos esas plataformas.
- **OuraClaw / HomeAssistant**: integraciones personales, fuera del scope de trabajo.
- **Managed hosting (💵)**: corremos self-hosted en la Mac Mini.

> **[VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills)** - índice comunitario de skills. Se suma a la lista como fuente de consulta, junto a los otros 3 repos.

---

## 🎯 Roadmap sugerido (orden de valor)

| Prioridad | Solución | Disparador |
|-----------|----------|------------|
| 1 | **Pre-Build Validator** | Antes del próximo proyecto nuevo |
| 2 | **Digest de información** | Cuando definas fuentes + horario |
| 3 | **Semantic Memory Search** | Cuando `memory.db` justifique capa vectorial |
| 4 | **State-driven Project Mgmt** | Al formalizar el handoff entre roles |
| 5 | **Content Factory** | Cuando haya un canal de contenido activo |

> Los ítems ⚪ quedan listados como "vistos y descartados" para no reanalizarlos en el futuro.
