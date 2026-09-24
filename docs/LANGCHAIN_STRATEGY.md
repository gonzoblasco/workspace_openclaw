# LANGCHAIN STRATEGY: Integration with OpenClaw Ecosystem

## 1. Manifiesto Estratégico

### Visión
La integración de LangChain en el ecosistema de OpenClaw no busca reemplazar la orquestación actual, sino dotarla de una **capa de ejecución estandarizada**. Mientras que OpenClaw actúa como el "Sistema Operativo" (gestionando memoria, archivos, contexto y tiempo), LangChain funciona como la "Suite de Aplicaciones Profesionales" que permite construir flujos de IA complejos, robustos y exportables.

### Sinergia OpenClaw <-> LangChain
| Entidad | Rol Principal | Responsabilidades |
|---|---|---|
| **OpenClaw** | OS / Orquestador | Gestión de identidad, memoria a largo plazo, acceso a archivos, automatizaciones y control de subagentes. |
| **LangChain** | Framework de Ejecución | Implementación de patrones RAG, gestión de cadenas de razonamiento, conectores de Vector DBs y estandarización de prompts. |

### Objetivos
- **Corto Plazo:** Establecer un "Starter Kit" funcional en Python que permita prototipar flujos de IA rápidamente.
- **Medio Plazo:** Implementar un sistema de RAG industrial conectado a Supabase Vector para consultas sobre conocimiento propio.
- **Largo Plazo:** Crear micro-servicios de IA independientes y exportables, manteniendo el "estilo de razonamiento" desarrollado en OpenClaw.

---

## 2. Análisis Técnico y Arquitectura

### El Stack Tecnológico (real, verificado 2026-09-24)
- **Lenguaje:** Python **3.12.14** (migrado desde 3.9.6 el 2026-09-24).
- **Framework de IA:** LangChain (Core, Community, LangGraph).
- **API Server:** FastAPI + uvicorn (async/streaming nativo).
- **Vector Store:** **ChromaDB local** (sin servidor, embebido). Supabase Vector (PGVector) queda para la Fase 6, cuando haya que compartir conocimiento entre maquinas.
- **Infraestructura:** **LaunchAgent nativo de macOS** para el Mac Mini (decision 2026-09-22). Docker queda escrito (`Dockerfile`) para la Fase 7, al desplegar fuera del Mac Mini.
- **Motor de IA:** **Ollama local** para LLM y embeddings. Sin proveedores cloud, sin API keys.

> **Correccion de deriva (2026-09-24):** esta seccion declaraba Supabase Vector y Docker como el stack, y Python 3.11+. Era el **plan**, no lo construido: se implemento ChromaDB local (mas simple, cero infraestructura) y LaunchAgent (Docker no estaba instalado). Supabase y Docker siguen siendo el destino, pero en fases posteriores.

### Flujo de Datos (RAG Pipeline)
`Usuario` -> `FastAPI` -> `LangChain` -> `Vector Store (Búsqueda Semántica)` -> `Contexto recuperado + Prompt` -> `LLM` -> `Respuesta Streaming` -> `Usuario`.

### Gestión de Memoria
- **Memoria de Sesión (Corto Plazo):** Gestionada por LangChain (`ConversationBufferWindowMemory`) para mantener la coherencia del chat actual.
- **Memoria de Conocimiento (Largo Plazo):** Gestionada por OpenClaw y la Vector Store, alimentando el contexto del LLM mediante RAG.

---

## 3. Planificación por Fases (Roadmap)

### Fase 1: Cimientos (The Infrastructure) - COMPLETA
**Objetivo:** Tener un entorno de desarrollo aislado y una conexión básica con el LLM.
- [x] **1.1 Setup del Entorno:** `projects/langchain-starter` con `venv` (hoy 3.12.14) y estructura `app/`, `scripts/`, `config/`. Repo git creado el 2026-09-24.
- [~] **1.2 Gestión de Secretos:** **NO aplica hoy.** El proyecto usa Ollama local: no hay API keys que gestionar. Queda pendiente para cuando se integre un proveedor cloud (Fase 6/7). El contrato de configuracion vive en `.env.example`.
- [x] **1.3 Hello World:** `app/main.py` con cadena `Prompt -> LLM -> OutputParser` via LangChain + Ollama (`gemma4:cloud`), verificado.
- **Hito:** ✅ CUMPLIDO - script funcional respondiendo consultas simples.

> **Nota sobre 1.2:** no es deuda, es una decision: no se integran secretos que no existen. Cuando aparezca el primer proveedor cloud, va al gestor de secretos (nunca en texto plano).

### Fase 2: El Conocimiento (RAG Implementation) - COMPLETA
**Objetivo:** Que la IA responda basándose en datos propios.
- [x] **2.1 Pipeline de Ingesta:** `projects/langchain-starter/scripts/ingest.py` (chunking semantico) + `projects/langchain-starter/scripts/store.py` (embeddings + persistencia). Embeddings via Ollama `qwen3-embedding:0.6b` (1024 dim).
- [x] **2.2 Vector Store:** **implementado con ChromaDB local**, no Supabase. Mismo rol, menos infraestructura; la migracion a Supabase es la Fase 6.1.
- [x] **2.3 Retrieval Chain:** `projects/langchain-starter/scripts/query.py` con prompt restringido a responder SOLO con el contexto recuperado (garantia anti-alucinacion, fijada por test).
- **Hito:** ✅ CUMPLIDO - el sistema responde sobre documentos propios y cita la fuente.

### Fase 3: La Interfaz (API & Streaming)
**Objetivo:** Convertir la lógica de script en un servicio accesible.
- [x] **3.1 Servidor FastAPI:** `app/api.py` con rutas `/`, `/health`, `/chat`, `/ingest` (+ `/docs` autogenerada).
- [x] **3.2 Streaming de Tokens:** `StreamingResponse` con `chain.stream()`, verificado en vivo.
- [x] **3.3 Cliente de Prueba:** Verificado con curl (health, chat con respuesta RAG correcta).
- **Hito:** CUMPLIDO - API funcional en `127.0.0.1:8100`.

### Fase 4: Evolución y Operación (Agents & Ops)
**Objetivo:** Pasar de una cadena lineal a un agente autónomo y desplegado.
- [x] **4.1 Tool-Calling:** `projects/langchain-starter/scripts/agent.py` con LangGraph ReAct: `search_knowledge` (RAG) + `word_count`. Verificado: decide tools en paralelo y sintetiza.
- [x] **4.2 Despliegue:** RESUELTO por **LaunchAgent nativo** (decision de Gonzo 2026-09-22): Docker descartado para el Mac Mini, `Dockerfile` queda escrito para futuro. Incluye `service.sh` (start/stop/restart/status via launchctl) y `watchdog.sh`.
- [x] **4.3 Observabilidad:** Doble capa: (a) watchdog launchd cada 60s que recupera el servicio salvo apagado intencional (marcador `.intentional-stop`); (b) automation OpenClaw `langchain-starter-health-alert` cada 30 min que avisa por Telegram solo si el watchdog no pudo recuperar.
- **Hito:** CUMPLIDO (salvo contenedor) - agente con tools + servicio autorreparable + monitoreo.

---

## 4. Matriz de Riesgos y Mitigación

| Riesgo | Impacto | Mitigación |
|---|---|---|
| **Conflictos de dependencias Python** | Medio | Uso estricto de `venv` y congelación de versiones en `requirements.txt`. |
| **Latencia en RAG** | Bajo | Implementación de caché de consultas comunes y optimización de índices en Supabase. |
| **Costo de Tokens (Embeddings)** | Bajo | Uso de modelos de embedding eficientes y control de tamaño de chunks. |
| **Desincronización de Memoria** | Medio | Definición clara de qué vive en la Vector Store vs. qué vive en el contexto de sesión. |

---

## 5. Deuda técnica detectada (auditoría 2026-09-24)

Gap entre "funciona" y "sirve como herramienta". Estado **al cierre del 2026-09-24** (los items de la deuda base se cerraron ese día):

| Item | Estado | Por qué importa |
|---|---|---|
| `requirements.txt` | ✅ **CERRADO:** 16 deps pinneadas (era 0 bytes) | Sin pinning el entorno no es reproducible. |
| Python | ✅ **CERRADO:** 3.12.14 (era 3.9.6) | 3.9 estaba al final de su vida. |
| Repo git | ✅ **CERRADO:** `gonzoblasco/langchain-starter` (era "no existe") | Sin repo no hay portabilidad, ni CI, ni entrega. |
| `README.md` | ✅ **CERRADO:** 4.371 bytes (eran 8) | Superficie del proyecto. |
| `.env.example` | ✅ **CERRADO:** contrato de config (era vacío) | Sin contrato no se sabe qué configurar. |
| Tests | ✅ **CERRADO:** 10 tests en el starter + 18 en kanam-insight | Verificados por mutación: romper una propiedad hace fallar su test. |
| **Base de conocimiento** | ❌ **ABIERTO:** 10 chunks de 1 solo documento | Sigue siendo demo, no herramienta. Es la Fase 5.2. |
| **`kanam-insight` sin `requirements.txt` propio** | ❌ **ABIERTO** (hallazgo de esta auditoría) | Depende del venv del starter. Como repo independiente **no se puede reproducir solo**: clonarlo y correr `pip install` no alcanza. |
| Secretos | ⚪ **NO APLICA hoy:** todo local via Ollama | No hay API keys que gestionar. Se integra cuando aparezca el primer proveedor cloud. |

---

## 5b. Causa raíz de la deriva (hallazgo de la auditoría 2026-09-24)

**Este documento vive en la raíz del workspace, y el Debt Detector solo escanea `projects/*/.knowledge/`.**

Consecuencia medida: las Fases 1 y 2 quedaron sin marcar aunque estaban completas desde el 2026-09-22, la sección 2 declaraba Supabase + Docker + Python 3.11 cuando lo construido era ChromaDB + LaunchAgent + Python 3.9, y la sección 5 listaba como deuda items ya cerrados. **Ninguna de esas tres derivas fue detectada por la herramienta que construimos para detectar derivas.**

Es el mismo patrón que apareció tres veces en el día: documentación que declara un estado que ya no es cierto, sin nada que lo verifique.

**Lección:** un verificador con alcance limitado da una falsa sensación de cobertura. El Debt Detector escanea 26 proyectos pero es ciego a la documentación de nivel workspace, que es justamente la más estratégica.

---

## 6. Plan de acción (Fases 5-7: de herramienta interna a producto)

### Fase 5: Solidez y uso real
**Objetivo:** Que el servicio deje de ser una demo y pase a usarse todos los días.
- [x] **5.1 Cerrar deuda de base:** `requirements.txt` con versiones pinneadas ✅, Python 3.12 ✅ (2026-09-24), repo git ✅, README real ✅, `.env.example` ✅. **Deuda base cerrada.**
- [x] **5.2 Ingesta real de conocimiento:** ✅ HECHO (2026-09-24). El scanner ahora cubre **3 fuentes: proyectos + `docs/` + `skills/`** (eran 122 archivos, son 445). Índice: **4423 vectores** (eran 1243).
  - Los **dailies y las sesiones ya los cubría `memory.db`** (1144 secciones `daily` + 843 `session`), asi que no se duplicaron: el criterio de exito "preguntar algo de una sesion pasada" ya estaba cumplido por esa via.
  - Se indexa lo que faltaba de verdad: los docs estrategicos (`docs/`) y las skills.
  - Excluidos: `docs/insights/` (reportes del propio detector: ruido auto-referencial y quedan vencidos) y `docs/archives/` (historico).
  - **Criterio verificado:** el radar ahora cruza las tres fuentes y trae cruces que antes eran imposibles. Ejemplo real: SQLite local con BLOB float32 (`docs/ADR-057`) vs Postgres con ivfflat (`soporteml-v3`) para el mismo problema de vectores, resuelto distinto segun escala.
- [x] **5.3 Red de seguridad:** ✅ HECHO (2026-09-24): 10 tests en el starter (chunking, overlap, prompt anti-alucinacion, `/health`, endpoints, RAG end-to-end) + 25 en kanam-insight. Verificados por mutacion.
- **Hito:** ✅ CUMPLIDO (2026-09-24) - el servicio responde preguntas reales sobre nuestro propio historial, con cita de fuente, y es reproducible en otra maquina. **Fase 5 cerrada.**

### Fase 6: Producto multi-cliente
**Objetivo:** Pasar de "una base de conocimiento" a "varias, aisladas, con acceso controlado".
- [ ] **6.1 Vector store compartida:** migrar Chroma local -> Supabase Vector (PGVector). Habilita acceso desde las dos máquinas y desde servicios externos.
- [ ] **6.2 Namespaces por cliente:** cada base de conocimiento etiquetada por `tenant` / `project`, con filtro obligatorio en el retrieval. Sin esto, un cliente ve datos de otro.
- [ ] **6.3 Auth y límites:** API keys por cliente, rate limiting, y registro de consumo por tenant.
- [ ] **6.4 Memoria de conversación:** `ConversationBufferWindowMemory` por sesión, separada de la memoria de conocimiento.
- **Hito:** dos clientes distintos con bases de conocimiento separadas, accediendo con credenciales propias.

### Fase 7: Comercialización
**Objetivo:** Empaquetar esto como oferta concreta.
- [ ] **7.1 Template de proyecto:** repo plantilla (este starter, generalizado) que sirva de punto de partida para cualquier cliente.
- [ ] **7.2 Despliegue fuera del Mac Mini:** Docker en VPS/cloud (el `Dockerfile` ya existe, sin probar).
- [ ] **7.3 Telemetría y costos:** tracking de tokens/latencia por request y por tenant. Precio sostenible.
- [ ] **7.4 Documentación de cliente:** onboarding, contrato de API, límites.
- **Hito:** primer servicio entregable y facturable a un tercero.

### Apuestas posibles (registro completo y orden)

Las apuestas evaluadas, con su orden de prioridad y el razonamiento, viven en **`docs/APUESTAS.md`**. Ese es el registro durable; esta seccion solo lo referencia para no duplicar.

Orden confirmado por Gonzo (2026-09-24): **1. kanam-insight** (uso interno, valida la capacidad), **2. soporteml-v4** (producto, mercado que paga), **3. kanam-fixer** (producto, diferenciador defendible).

> **Correccion (2026-09-24):** esta seccion titulaba antes una "primera apuesta comercial" centrada en una base de conocimiento de accesibilidad. Eso fue un error de encuadre: sugeria que era la unica o la principal apuesta, y ademas era la mas debil (un RAG sobre WCAG ya existe repetidas veces). El encuadre correcto del dominio a11y es auditoria sobre el anuncio real, que es `kanam-fixer`, no un chatbot de documentacion.

---

## 7. Principio rector

**No construimos un producto de IA genérico.** Construimos primero la herramienta que mejora nuestro trabajo; cada capacidad que sirve internamente y se estabiliza, se empaqueta. El orden importa: uso interno -> estabilización -> aislamiento multi-cliente -> exportación. Saltarse el uso interno produce productos que nadie probó.

