# LANGCHAIN STRATEGY: Integration with OpenClaw Ecosystem

## 1. Manifiesto Estratégico

### Visión
La integración de LangChain en el ecosistema de OpenClaw no busca reemplazar la orquestación actual, sino dotarla de una **capa de ejecución estandarizada**. Mientras que OpenClaw actúa como el "Sistema Operativo" (gestionando memoria, archivos, contexto y tiempo), LangChain funciona como la "Suite de Aplicaciones Profesionales" que permite construir flujos de IA complejos, robustos y exportables.

### Sinergia OpenClaw $\leftrightarrow$ LangChain
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
`Usuario` $\rightarrow$ `FastAPI` $\rightarrow$ `LangChain` $\rightarrow$ `Supabase Vector (Búsqueda Semántica)` $\rightarrow$ `Contexto recuperado + Prompt` $\rightarrow$ `LLM` $\rightarrow$ `Respuesta Streaming` $\rightarrow$ `Usuario`.

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
- [ ] **3.1 Servidor FastAPI:** Montaje de la estructura de servidor y definición de rutas (`/chat`, `/ingest`, `/health`).
- [ ] **3.2 Streaming de Tokens:** Implementación de `StreamingResponse` para entrega de texto en tiempo real.
- [ ] **3.3 Cliente de Prueba:** Creación de un cliente simple (curl/web) para validar la interacción.
- **Hito:** API funcional que permite chatear con el "conocimiento" de la Fase 2 en tiempo real.

### Fase 4: Evolución y Operación (Agents & Ops)
**Objetivo:** Pasar de una cadena lineal a un agente autónomo y desplegado.
- [x] **4.1 Tool-Calling:** Implementación de herramientas personalizadas que el agente puede decidir ejecutar (ej: buscar en web, leer archivo). Implementado con LangGraph ReAct: `search_knowledge` (RAG) + `word_count`, verificado con decisión de tools en paralelo.
- [ ] **4.2 Dockerización:** Creación de `Dockerfile` y `docker-compose.yml` para despliegue estable en Mac Mini. BLOQUEADO: Docker no está instalado en el Mac Mini (decisión pendiente con Gonzo: Docker Desktop vs OrbStack vs LaunchAgent nativo).
- [x] **4.3 Observabilidad:** Automation OpenClaw `langchain-starter-health-watch` (cada 15 min, GET /health en 127.0.0.1:8100; silencioso si sano, alerta si cae).
- **Hito:** Agente autónomo desplegado en contenedor, capaz de usar herramientas y monitoreado por OpenClaw.

---

## 4. Matriz de Riesgos y Mitigación

| Riesgo | Impacto | Mitigación |
|---|---|---|
| **Conflictos de dependencias Python** | Medio | Uso estricto de `venv` y congelación de versiones en `requirements.txt`. |
| **Latencia en RAG** | Bajo | Implementación de caché de consultas comunes y optimización de índices en Supabase. |
| **Costo de Tokens (Embeddings)** | Bajo | Uso de modelos de embedding eficientes y control de tamaño de chunks. |
| **Desincronización de Memoria** | Medio | Definición clara de qué vive en la Vector Store vs. qué vive en el contexto de sesión. |
