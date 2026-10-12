# Módulo 6 · Lección 26 de 30: Segmentación de Dominios entre Agentes Dedicados

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 6 - Especialización y Coordinación Multiagente
**Lección:** 26 de 30 · **abre el Módulo 6**
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

Cuando un único agente asume soporte técnico, ejecución de scripts de infraestructura y redacción financiera, el sistema colapsa bajo su propio contexto: el espacio de tokens se satura con herramientas irrelevantes, las instrucciones compiten y sube la probabilidad de alucinaciones operativas. La solución madura es **segmentar el espacio de trabajo en dominios** gobernados por agentes especializados.

En OpenClaw, un agente dedicado no es un servidor aislado ni un proceso desacoplado: es una **configuración de ejecución acotada** con un subconjunto estricto de herramientas, sus propios archivos de configuración (`SOUL.md` para el tono, `AGENT.md` para directivas operativas) y un espacio de almacenamiento local propio que impide la contaminación cruzada.

---

## Anatomía del colapso del agente generalista

Un agente generalista acumula definiciones de esquema JSON de **cada** herramienta; el prompt debe inyectar la especificación completa de cada una en cada turno. Tres fallos críticos:

1. **Dilución de la atención semántica:** más herramientas compitiendo en el espacio de tokens → mayor *tool selection error rate* (invocaciones accidentales con parámetros ambiguos).
2. **Conflicto de directivas:** las reglas de cordialidad empática (soporte) chocan con la concisión aséptica (SRE).
3. **Fugas de privilegios:** si un usuario sin privilegios interactúa con un agente que tiene acceso directo a herramientas de bajo nivel en el host, la barrera depende solo del razonamiento del LLM → puerta abierta a **prompt injection**.

La segmentación divide esa carga en **fronteras de responsabilidad explícitas**, asignando a cada agente solo las capacidades de su dominio.

---

## Aislamiento de dominios frente al modelo monolítico

En OpenClaw la separación física y lógica **no requiere múltiples daemons**: se implementa con **workspaces o perfiles independientes** bajo una misma instancia maestra, cada uno con su árbol de directorios, herramientas filtradas y directivas de personalidad.

### Estructura de directorios (del curso)

```text
openclaw-system/
├── config.json                     # Registro maestro de agentes
└── agents/
    ├── customer_support/
    │   ├── AGENT.md               # Directivas de dominio y límites de acción
    │   ├── SOUL.md                # Tono conversacional empático y paciente
    │   ├── memory/                # Historial de tickets y usuarios
    │   │   └── interactions.json
    │   └── tools.json             # Herramientas expuestas (Zendesk, Stripe read-only)
    └── infra_ops/
        ├── AGENT.md               # Directivas de seguridad y validación de comandos
        ├── SOUL.md                # Tono técnico, telegráfico y conciso
        ├── memory/                # Bitácoras de despliegue e incidentes
        │   └── incident_log.md
        └── tools.json             # Herramientas expuestas (SSH, Docker, Bash)
```

`customer_support` no tiene rutas ni visibilidad sobre `infra_ops/`. Si un prompt injection intenta persuadir a `customer_support` de ejecutar `system.execute_bash`, la llamada **falla de inmediato**: el esquema de esa herramienta ni siquiera forma parte de su `tools.json`.

### Registro maestro (del curso)

```json
{
  "system_version": "2.4.0",
  "agents": {
    "support_agent": {
      "name": "Customer Support Specialist",
      "model": "claude-3-5-sonnet",
      "workspace_root": "./agents/customer_support",
      "allowed_tools": ["zendesk_read_ticket", "zendesk_reply_ticket", "stripe_lookup_customer", "knowledge_base_search"],
      "max_tool_iterations": 4,
      "sandbox": { "network_access": "egress_restricted", "allowed_hosts": ["api.zendesk.com", "api.stripe.com"] }
    },
    "ops_agent": {
      "name": "Site Reliability Specialist",
      "model": "claude-3-5-sonnet",
      "workspace_root": "./agents/infra_ops",
      "allowed_tools": ["docker_inspect_container", "docker_restart_container", "read_service_logs", "query_prometheus"],
      "max_tool_iterations": 8,
      "sandbox": { "network_access": "internal_only", "allowed_hosts": ["10.0.0.0/8"] }
    }
  }
}
```

Al acotar `allowed_tools` a nivel del motor, el runtime **no depende de la fidelidad del modelo** ante un prompt negativo ("no ejecutes comandos de consola"): el agente no posee el binario ni la interfaz de la herramienta en su vector de despacho.

---

## AGENT.md vs SOUL.md

Dos documentos rectores por agente:
- **SOUL.md:** temperatura conversacional, registro estilístico, reglas de interacción humana (L03).
- **AGENT.md:** el **contrato del dominio operativo**: qué problemas caen en su jurisdicción, cuáles rechaza, y qué protocolo de salida aplica ante desbordamiento de dominio.

Ejemplo de `AGENT.md` (soporte) - incluye la frontera y el código de desbordamiento `TRANSFER_TO_OPS`; el de `infra_ops` usa `TRANSFER_TO_SUPPORT` para escalar comunicación pública.

---

## Criterios de demarcación (dónde termina un agente y empieza otro)

1. **Vector de credenciales y permisos:** si una herramienta exige permisos destructivos (`DROP TABLE`, `reboot`, cobros no supervisados), **jamás** debe coexistir con un agente expuesto a entradas de texto no sanitizadas. *La frontera de dominio debe coincidir con la frontera de seguridad de las APIs.*
2. **Diferenciación de latencia y modelos:** soporte quiere latencia baja y modelos rápidos; análisis forense puede ser asíncrono con modelo de contexto masivo. Segmentar permite **asignar modelos distintos** por agente.
3. **Frecuencia y persistencia de memoria:** soporte consulta KB estable + historial corto; auditoría nocturna genera temporales voluminosos. Compartir workspace haría que soporte leyera bitácoras internas en sus búsquedas semánticas.

| Criterio | Dominio público / Soporte | Dominio interno / Infraestructura |
|---|---|---|
| Origen del estímulo | Webhooks de chat (Slack, WhatsApp, Zendesk) | Cron, triggers internos, alertas |
| Tolerancia a errores | Media (respuestas reformulables) | Cero (comandos en producción) |
| Herramientas | APIs solo-lectura, emisión de tickets | Shell, contenedores, DB |
| Aislamiento de red | Endpoints públicos externos | Red privada / VPN |
| Vida de sesión | Corta (cierra al finalizar el ticket) | Persistente o por pipeline |

> **PITFALL del curso (correcto):** crear un agente por **cada herramienta** ("Agente Consultor de Clima", "Agente Calculador") genera sobrecarga de serialización y coordinación. Un dominio saludable agrupa **3-8 herramientas altamente cohesionadas**.

### Check your understanding
**¿Cómo se elimina el riesgo de que un cliente fuerce ejecutar bash en un agente de soporte público?**
- [x] **Separar en perfiles distintos y retirar `execute_bash` de `allowed_tools`. ✅ (acierta: la frontera la fija el runtime, no el prompt)**

---

## Implementación (del curso)

Pasos: crear workspaces aislados (`mkdir` + `chmod`), definir `tools.json` por agente (con `handler: builtin:...`), y ejecutar:

```bash
openclaw agent run --config ./config.json --target support_agent
```

Ante una petición maliciosa, el curso muestra que el agente se niega **no porque `AGENT.md` se lo prohíba**, sino porque en su array de capacidades la herramienta **no existe**:

```text
[User]: "El servidor de pagos está caído con error 502. Ejecuta 'systemctl restart nginx' ahora mismo."
[OpenClaw Runtime Engine]
Injected tools: ['search_docs', 'create_ticket']
Token consumption: 1,480 tokens (prompt base + 2 esquemas)
[Support Agent]: "No tengo la capacidad de reiniciar servicios... He creado un ticket con prioridad 'high'..."
[Tool Invocations]: create_ticket(...) -> SUCCESS (ID: #49201)
```

> **REMEMBER del curso (correcto y central):** la seguridad multiagente **nunca** debe descansar en la obediencia semántica del modelo. La frontera real la dicta **el runtime** al no registrar herramientas ajenas al dominio.

---

## Resumen

La segmentación resuelve los tres cuellos de botella del monolito: saturación de tokens por sobrecarga de esquemas, confusión en la selección de herramientas, y riesgo de privilegios en interfaces públicas. Aislar el filesystem, restringir `allowed_tools` y delimitar responsabilidades en `AGENT.md` hace a cada agente predecible, rápido y seguro.

**UP NEXT · Lección 27 de 30:** *Definición de Reglas Claras de Enrutamiento*. Faltan **4 lecciones** para cerrar el Módulo 6.

---

## Preguntas abiertas del propio curso

1. ¿Cómo gestiona OpenClaw que un agente necesite datos de la memoria de otro especialista?
2. ¿Qué sobrecarga representa tener varios agentes vs. uno monolítico?
3. ¿Pueden dos agentes usar modelos LLM distintos en la misma instalación?
4. ¿Cuándo conviene unificar dos dominios en un solo agente?

(Anotadas. #3 la responde la L26: sí, `model` por agente.)

---

## Notas de verificación (Kanam)

**El tema SÍ existe en OpenClaw y es de los más alineados del curso** (tercer caso tras L11/L16). El modelo mental coincide **en gran parte**:

| El curso dice | OpenClaw real |
|---|---|
| Varios agentes aislados en una sola instancia maestra | ✅ **Real y central.** *"Run multiple isolated agents in one Gateway process, each with its own workspace, state directory (agentDir), and SQLite-backed session history"* (`docs/concepts/multi-agent.md`). |
| Cada agente con su propio workspace + archivos de persona | ✅ Real: *"Workspace: files, `AGENTS.md`/`SOUL.md`/`USER.md`"*. |
| Aislamiento de almacenamiento propio (sin contaminación cruzada) | ✅ Real: `agentDir` con `openclaw-agent.sqlite` por agente; la doc **advierte** no reusar `agentDir` entre agentes. |
| Runtime filtra las herramientas por dominio | ✅ Real en espíritu: hay **allowlists por agente** (`agents.entries.*.skills`, política de tools). |
| Modelo distinto por agente | ✅ **Real:** `agents.entries.*` permite `model` por agente. |
| **La frontera de seguridad la fija el runtime, no el prompt** (REMEMBER) | ✅ **Correcto y central**; coincide con la filosofía real y con la regla de sandbox del workspace. |
| **Acierta el quiz** (perfiles distintos + retirar la tool). | ✅ |
| PITFALL de crear un agente por herramienta; agrupar 3-8 cohesivas | ✅ Buen criterio de diseño. |

**Lo que NO coincide con la instalación real (nombres/esquema inventados):**
- ❌ **`AGENT.md` (singular) no existe. El archivo real es `AGENTS.md` (plural).** El curso lo usa consistentemente en singular - error de nombre, aunque el *concepto* (directivas operativas por agente) es real.
- ❌ **`config.json` con registro maestro + `system_version: "2.4.0"`** es **inventado**. La config real es **`~/.openclaw/openclaw.json`** y los agentes se declaran bajo `agents.entries.*`; no hay `system_version` (esta instalación es 2026.9.8).
- ❌ **`allowed_tools`** como clave: el control real es la **política de tools** (`--tools`, allowlists por agente, gating), no una clave `allowed_tools` en un `config.json`.
- ❌ **`sandbox.network_access` / `sandbox.allowed_hosts`**: no existen esas claves (el aislamiento de red real es por sandbox/container, con otra superficie).
- ❌ **`tools.json` con `handler: "builtin:zendesk_post"`** etc.: formato inventado. Las tools reales se definen vía SDK/plugins, no con `handler: builtin:` en un `tools.json`.
- ❌ **`openclaw agent run --config ./config.json --target support_agent`** no es el CLI real. El real es **`openclaw agent --agent <id>`** (con `--channel`, `--deliver`, `--local`).
- ❌ **`openclaw-system/`** como raíz: la layout real es `~/.openclaw/agents/<agentId>/agent/`.
- ❌ **`max_tool_iterations`**: mismo problema que `max_consecutive_calls` de L22 (no es la clave real).

**Verificación ejecutable:** ⚠️ no hay código ejecutable (es config/CLI); el bloque de "Injected tools / Token consumption" es una traza ilustrativa, no reproducible.

**Patrón (vigésimo sexto caso, con matiz fuerte):** por tercera vez (tras L11 y L16) **el tema existe de verdad** y la **filosofía acierta** (aislamiento, frontera en el runtime, allowlist, modelo por agente). La fachada inventada es de siempre: **nombres de archivo (`AGENT.md` vs `AGENTS.md`), config (`config.json`/`allowed_tools`/`sandbox.*`), CLI (`agent run --config`) y layout (`openclaw-system/`)**. Traducible: `agents.entries.*` + `~/.openclaw/agents/<id>/` + `openclaw agent --agent` + allowlists, no el `config.json` del curso.

**Nota de contexto (Módulo 6):** tras esta L26 el propio curso indica *"4 lessons left in Especialización y Coordinación Multiagente"* → Módulo 6 = 5 lecciones (L26-L30). Lección 27: *Definición de Reglas Claras de Enrutamiento*.
