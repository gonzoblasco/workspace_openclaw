# Los 5 Cerebros de Kanam OS: Especialización Radical en Acción

**DEV, OPS, MIND, STUDIO y CORE: Cómo cada cerebro trabaja sin solapamiento** 🧠🔥

Después de explicar el *porqué* de la arquitectura multi-agente, ahora profundizamos en el **cómo**. ¿Qué hace exactamente cada cerebro especializado? ¿Cómo comparten información sin saturarse? ¿Dónde se cruzan sus caminos?

---

## 1. Kanam CORE: El Cerebro Orquestador 🧠

**Ubicación:** `/workspace/` (raíz del workspace)  
**Rol:** Orquestación, Memoria Global, Gobierno y Estrategia  
**Thinking Level:** `high` (max para decisiones complejas)

### Qué hace:
- ✅ **Recibe todas las tareas** - Punto único de entrada
- ✅ **Analiza intención** - Interpreta qué necesita el usuario
- ✅ **Evalúa complejidad** - Usa el [complexity-scorer](file:///Users/gonzoblasco/.openclaw/workspace/prompts/complexity-scorer.md#meta-prompt-evaluador-de-complejidad) para determinar nivel de pipeline
- ✅ **Despacha al especialista correcto** - `sessions_spawn` o `sessions_send` según sea necesario
- ✅ **Hace síntesis final** - Integra resultados de especialistas
- ❌ **NO ejecuta tareas operativas directamente** - Solo delega

### Ejemplo real de operación:

```
Usuario: "Crear un skill para generar componentes React con TDD"

CORE analiza → Score: 14 (medium-complex)
→ Pipeline: DEV escribe → MIND hace research → CORE aprueba
→ Despacha a Kanam DEV con contexto aislado
```

---

## 2. Kanam DEV: El Ingeniero 💻

**Ubicación:** `/workspace/agents/kanam-dev/`  
**Rol:** Ingeniería de Software, Producto, OpenSpec, TDD  
**Thinking Level:** `high` para implementación, off para trivial

### Qué hace:
- ✅ **Implementa specs técnicas** - De ADR a código funcional
- ✅ **Escribe tests con Vitest** - Antes de cada commit
- ✅ **Refactoriza código** - Con Biome como linter
- ✅ **Crea skills y plugins** - Para el ecosistema OpenClaw
- ✅ **Valida OpenSpec drafts** - CI valida antes de merge

### Stack preferido:
```typescript
React + TypeScript
Supabase (Backend as a Service)
Vitest (Testing)
Biome (Linting/formatting)
Create-stack (Scaffolding)
```

### Flujo de trabajo típico:

```
1. Recibe prompt delegados por CORE con contexto aislado
2. Escribe specs técnicas en OpenSpec
3. Genera código con Vitest tests
4. Biome valida formato
5. PR mergeado al repo del workspace
6. Devuelve resultado a CORE con "Context Handover"
```

---

## 3. Kanam OPS: El Ingeniero de Infraestructura 🛠️

**Ubicación:** `/workspace/agents/kanam-ops/`  
**Rol:** Infraestructura, Gateway, Seguridad, Tooling  
**Thinking Level:** `high` para configuraciones complejas

### Qué hace:
- ✅ **Configura el Gateway OpenClaw** - Channels, plugins, agentes
- ✅ **Gestiona despliegues CI/CD** - GitHub Actions workflows
- ✅ **Maneja seguridad de secrets** - `.env`, tokens, credentials
- ✅ **Administra herramientas del ecosistema** - Tools search, tool_call
- ✅ **Monitorea salud del sistema** - `openclaw status`, logs

### Configuración típica:

```yaml
# gateway/config.yaml (ejemplo)
channels:
  - webchat
  - telegram (Mini, Air)
  
plugins:
  - browser-automation
  - obsidian-vault-maintainer
  
agents:
  main: kanam-core
  
models:
  primary: ollama/qwen3.5:9b-mlx
```

### Operaciones comunes:

1. **Restart de Gateway** - Cuando se necesitan cambios de config
2. **Deploy de plugins nuevos** - Instalar y activar capabilities
3. **Configurar canales de comunicación** - Webchat, Telegram, etc.
4. **Gestionar secrets** - Tokens, API keys, credenciales

---

## 4. Kanam MIND: El Investigador 🧘

**Ubicación:** `/workspace/agents/kanam-mind/`  
**Rol:** Conocimiento, Research, Vida, Aprendizaje  
**Thinking Level:** `high` para análisis profundo

### Qué hace:
- ✅ **Investiga y resuelve información** - RAG sobre memoria.db
- ✅ **Hace minería de datos** - De corpus, repositorios, fuentes externas
- ✅ **Genera insights** - Resúmenes estratégicos de contextos complejos
- ✅ **Mantiene el conocimiento** - Ingesta en Obsidian vault
- ✅ **Analiza métricas y patrones** - Desde logs, usage data

### Técnicas:

```
RAG (Retrieval-Augmented Generation):
  → Busca fragmentos específicos en memory.db
  
Web Search:
  → Verifica afirmaciones técnicas en fuentes oficiales

Corpus Mining:
  → Extrae insights de miles de documentos
```

### Ejemplo real:

```
CORE delega: "Investigar las últimas tendencias en RAG para sistemas multi-agente"

MIND action plan:
1. Consultar memory.db por "multi-agent rag"
2. Buscar repos GitHub relevantes (gh api)
3. Leer papers de arxiv sobre el tema
4. Sintetizar insights con verificación de fuentes
5. Devolver resumen estructurado a CORE
```

---

## 5. Kanam STUDIO: El Comunicador ✍️

**Ubicación:** `/workspace/agents/kanam-studio/`  
**Rol:** Comunicación, Redacción, Marca Personal, OSS  
**Thinking Level:** `high` para narrativa compleja

### Qué hace:
- ✅ **Escribe posts y artículos** - Para LinkedIn, blog, newsletter
- ✅ **Diseña narrativa de marca** - Quién es Kanam OS públicamente
- ✅ **Genera activos creativos** - Ideas visuales, prompts para imágenes
- ✅ **Mantiene comunidad** - Engagement en redes sociales
- ✅ **Documenta casos de uso** - Stories del ecosistema

### Flujo de trabajo:

```
1. Recibe brief de CORE sobre qué comunicar
2. Consulta MIND si hay insights relevantes
3. Revisa DEV si hubo implementación reciente
4. Escribi articulo/narrativa
5. Devuelve a CORE para publicación final
```

---

## El "Context Handover" entre Agentes

Para evitar que un agente re-descubra lo que otro ya hizo, cada transferencia incluye **Estado de Contexto**:

```markdown
=== TRANSFERENCIA DE CONTEXTO: DEV → STUDIO ===

Summary:
Implementamos el sistema de autenticación JWT para la plataforma Kanam OS. 
El frontend usa react-router conProtectedRoute, el backend tiene middleware Express.

Status: ✅ Draft → ✅ Ready para publicación

Next Steps:
- Agregar refresh tokens y token refresh flow
- Publicar demo video del login
- Escribir guía de autenticación

Resources:
📁 /workspace/agents/kanam-dev/auth/jwt-system/
🔗 PR mergeado: https://github.com/gonzoblasco/workspace_openclaw/pull/10234
🧠 Insights MIND sobre seguridad auth en multi-agent systems
```

---

## Memoria Compartida: El Inconsciente Colectivo

Todos los agentes comparten una **fuente de verdad**: `memory.db` (SQLite). 

### Cómo funciona el RAG distribuido:

```javascript
// Cada agente consulta la memoria db según su rol
CORE.query("architectural decisions") → Devuelve ADRs relevantes
DEV.query("implementation patterns") → Devuelve código de patrones
OPS.query("infrastructure concerns") → Devuelve configs y setups
MIND.query("domain knowledge") → Devuelve insights investigados
STUDIO.query("narrative themes") → Devuelve ideas para comunicación
```

**Ventaja:** Ningún agente necesita cargar toda la memoria en su prompt. Solo lo que le importa.

---

## Conclusión: Sin Solapamiento, Sin Pérdida de Información

✅ **Especialización real** - Cada cerebro hace exactamente lo suyo  
✅ **Coordination sin fricción** - Protocolo claro de handover  
✅ **Memoria compartida** - RAG distribuido evita re-descubrimientos  
✅ **Versionado completo** - Git en cada workspace aislado  

---

Kanam OS no es un "todo hace todo". Es un sistema donde la especialización genera excelencia. Cada cerebro conoce su dominio, delega lo que necesita y comparte información de forma estructurada.

**Sígueme** para ver cómo exactamente Kanam DEV implementa specs técnicas en código real, qué tests escribe antes de cada commit y cómo el pipeline garantiza calidad técnica. 💻🔥

---

*Publicado 29/09/2026 | #KanamOS #MultiAgentSystem #Specialization #SoftwareEngineering #AI #DevOps #Architectur*
