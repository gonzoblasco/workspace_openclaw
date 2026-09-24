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

### El Stack Tecnológico
- **Lenguaje:** Python 3.11+ (por madurez del ecosistema LLM).
- **Framework de IA:** LangChain (Core, Community, LangGraph).
- **API Server:** FastAPI (por su alta performance y soporte nativo de async/streaming).
- **Vector Store:** Supabase Vector (PGVector) para persistencia de conocimiento semántico.
- **Infraestructura:** Docker para aislamiento y despliegue en Mac Mini.

### Flujo de Datos (RAG Pipeline)
`Usuario` -> `FastAPI` -> `LangChain` -> `Vector Store (Búsqueda Semántica)` -> `Contexto recuperado + Prompt` -> `LLM` -> `Respuesta Streaming` -> `Usuario`.

### Gestión de Memoria
- **Memoria de Sesión (Corto Plazo):** Gestionada por LangChain (`ConversationBufferWindowMemory`) para mantener la coherencia del chat actual.
- **Memoria de Conocimiento (Largo Plazo):** Gestionada por OpenClaw y la Vector Store, alimentando el contexto del LLM mediante RAG.

---

## 3. Planificación por Fases (Roadmap)

### Fase 1: Cimientos (The Infrastructure)
**Objetivo:** Tener un entorno de desarrollo aislado y una conexión básica con el LLM.
- [ ] **1.1 Setup del Entorno:** Creación de repo `langchain-starter`, configuración de `venv` y estructura de carpetas (`app/`, `scripts/`, `config/`).
- [ ] **1.2 Gestión de Secretos:** Integración con `openclaw secrets` para inyección de API Keys.
- [ ] **1.3 Hello World:** Implementación de una cadena básica (`Prompt` $\rightarrow$ `LLM` $\rightarrow$ `OutputParser`) ejecutable via terminal.
- **Hito:** Script funcional que responda consultas simples usando la arquitectura de LangChain.

### Fase 2: El Conocimiento (RAG Implementation)
**Objetivo:** Que la IA responda basándose en datos propios.
- [ ] **2.1 Pipeline de Ingesta:** Desarrollo de scripts para carga de documentos (Markdown/PDF), *chunking* inteligente y generación de *embeddings*.
- [ ] **2.2 Conexión Vector Store:** Configuración de cliente Supabase Vector para almacenamiento y recuperación de vectores.
- [ ] **2.3 Retrieval Chain:** Implementación de la cadena de recuperación que inyecta el contexto encontrado en el prompt final.
- **Hito:** Sistema capaz de responder preguntas sobre un set de documentos específicos con citas de fuente.

### Fase 3: La Interfaz (API & Streaming)
**Objetivo:** Convertir la lógica de script en un servicio accesible.
- [x] **3.1 Servidor FastAPI:** `app/api.py` con rutas `/`, `/health`, `/chat`, `/ingest` (+ `/docs` autogenerada).
- [x] **3.2 Streaming de Tokens:** `StreamingResponse` con `chain.stream()`, verificado en vivo.
- [x] **3.3 Cliente de Prueba:** Verificado con curl (health, chat con respuesta RAG correcta).
- **Hito:** CUMPLIDO - API funcional en `127.0.0.1:8100`.

### Fase 4: Evolución y Operación (Agents & Ops)
**Objetivo:** Pasar de una cadena lineal a un agente autónomo y desplegado.
- [x] **4.1 Tool-Calling:** `scripts/agent.py` con LangGraph ReAct: `search_knowledge` (RAG) + `word_count`. Verificado: decide tools en paralelo y sintetiza.
- [x] **4.2 Despliegue:** RESUELTO por **LaunchAgent nativo** (decision de Gonzo 2026-09-22): Docker descartado para el Mac Mini, `Dockerfile` queda escrito para futuro. Incluye `service.sh` (start/stop/restart/status via launchctl) y `watchdog.sh`.
- [x] **4.3 Observabilidad:** Doble capa: (a) watchdog launchd cada 60s que recupera el servicio salvo apagado intencional (marcador `.intentional-stop`); (b) automation OpenClaw `langchain-starter-health-alert` cada 30 min que avisa por Telegram solo si el watchdog no pudo recuperar.
- **Hito:** CUMPLIDO (salvo contenedor) - agente con tools + servicio autorreparable + monitoreo.

---

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

Gap entre "funciona" y "sirve como herramienta". Nada de esto bloquea la demo, todo esto bloquea el uso diario y la comercialización:

| Item | Estado real | Por qué importa |
|---|---|---|
| `requirements.txt` | **VACÍO (0 bytes)** | Sin pinning, el entorno no es reproducible. Nadie puede clonar y correr esto. Primer bloqueante de exportabilidad. |
| Python | **3.9.6** en el venv (la estrategia dice 3.11+) | 3.9 está al final de su vida; varias libs modernas requieren 3.10+. Hay `python3.12` disponible en el sistema. |
| Repo git | **No existe** (solo carpeta + `.knowledge/` en el workspace) | Sin repo no hay portabilidad, ni CI, ni entrega a un cliente. |
| Base de conocimiento | **10 chunks de 1 solo documento** (`LANGCHAIN_STRATEGY.md`) | Es una demo, no una herramienta. Falta ingesta real. |
| Tests | **Ninguno** | Sin red de seguridad, cada cambio es a ciegas. |
| `README.md` | 8 bytes ("FastAPI") | Superficie de GitHub/proyecto vacía. |
| `.env.example` | **Vacío** | Sin contrato de configuración. |
| Secretos | No integrado con `openclaw secrets` | Hoy no se necesita (todo local via Ollama), pero será necesario al salir del Mac Mini. |

---

## 6. Plan de acción (Fases 5-7: de herramienta interna a producto)

### Fase 5: Solidez y uso real
**Objetivo:** Que el servicio deje de ser una demo y pase a usarse todos los días.
- [ ] **5.1 Cerrar deuda de base:** `requirements.txt` con versiones pinneadas, migrar a Python 3.12, repo git + README real, `.env.example` con contrato de config.
- [ ] **5.2 Ingesta real de conocimiento:** indexar memoria y docs del workspace (dailies, `docs/`, `skills/`) con chunking por secciones. Criterio de éxito: preguntar algo de una sesión pasada y que responda con cita de fuente.
- [ ] **5.3 Red de seguridad:** pytest para los 3 caminos críticos (chunking, retrieval, endpoint `/chat`).
- **Hito:** el servicio responde preguntas reales sobre nuestro propio historial y es reproducible en otra máquina.

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

