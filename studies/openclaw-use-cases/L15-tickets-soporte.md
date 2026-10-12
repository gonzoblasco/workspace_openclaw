# Módulo 3 · Lección 15 de 30: Creación Rápida de Tickets de Soporte

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 3 - Ingesta Dirigida por Eventos
**Lección:** 15 de 30 · **cierra el Módulo 3**
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

La creación rápida de tickets transforma alertas ruidosas e inconexas en **incidencias estructuradas, priorizadas y asignadas** al equipo correcto. Un error de base de datos o una queja en Slack no debe quedar en notificación efímera: requiere **persistencia** en un gestor (Jira, GitHub Issues, Linear) con metadatos contextuales, etiquetas precisas y severidad justificada.

OpenClaw actúa como **puente inteligente** entre la recepción del evento y el gestor: evalúa la carga útil, extrae contexto operativo, descarta duplicados por **idempotencia** y sintetiza una descripción accionable - en vez de un script rígido que crea un ticket idéntico por cada traza.

---

## Anatomía del flujo de triage y creación automática

Tubería estricta de **cuatro fases**:

1. **Ingesta e idempotencia:** hash/identificador único desde la firma del error (`error_fingerprint` o `session_id`) para evitar 50 tickets ante una ráfaga.
2. **Evaluación de severidad:** el agente analiza impacto (usuarios afectados, entorno, código HTTP, palabras clave de SLA) y asigna **P1-P4**.
3. **Enriquecimiento del contexto:** recolecta stack traces, IDs de cliente y variables relevantes, **descartando credenciales y PII**.
4. **Despacho transaccional:** ejecuta la mutación en el gestor y devuelve la **URL del ticket** para vincularla a la alerta original.

---

## Esquema y extracción con tipado estricto

La salida **no puede ser prosa libre**: debe ser un objeto JSON validado contra un esquema estricto **antes** de invocar la herramienta del gestor. Seis campos elementales:

```json
{
  "title": "[AUTH] JWT signature verification failed on /v1/checkout",
  "severity": "P1",
  "component": "auth-service",
  "fingerprint": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "summary": "Múltiples clientes reportan HTTP 401 intermitente durante el checkout. Las claves públicas del proveedor OIDC fallaron al rotar a las 14:02 UTC.",
  "labels": ["backend", "auth", "checkout-blocker"],
  "reproduction_steps": [
    "Enviar POST a /v1/checkout con un token emitido en los últimos 10 minutos",
    "Observar error 'RS256 invalid signature' en la respuesta del gateway"
  ]
}
```

La severidad **no** se deja al arbitrio subjetivo del modelo: se rige por criterios objetivos inyectados en la directiva:

- **P1 (Crítico):** pérdida directa de transacciones, degradación del servicio principal en producción o compromiso de seguridad.
- **P2 (Alto):** funcionalidad crítica dañada sin alternativa directa para un segmento relevante.
- **P3 (Medio):** funcionalidad secundaria afectada o degradación con workaround viable.
- **P4 (Bajo):** defectos estéticos menores, advertencias de depuración, mejoras solicitadas.

> **PITFALL del curso (correcto):** crear tickets sin huella criptográfica de idempotencia genera **duplicados en cascada** durante tormentas. Si un microservicio emite 400 excepciones/seg, el webhook satura la cuota de la API de Jira y bloquea a soporte.

---

## Implementación: del webhook al despacho con deduplicación

Handler en TypeScript que intercepta el payload, consulta tickets recientes **en memoria** y decide entre abrir una incidencia nueva o **anexar** a la existente (Linear):

```typescript
import { createHash } from "crypto";
interface IncomingWebhookEvent {
  service: string; environment: string; error_name: string; message: string;
  stack_trace: string; affected_user_id?: string; timestamp: string;
}
interface TicketDraft {
  title: string; severity: "P1" | "P2" | "P3" | "P4";
  component: string; fingerprint: string; summary: string; labels: string[];
}
export class TicketAutomationHandler {
  private activeFingerprints = new Map<string, { ticketId: string; count: number }>();
  public computeFingerprint(event: IncomingWebhookEvent): string {
    // Normalizar la traza omitiendo líneas volátiles como timestamps o números de línea dinámicos
    const normalizedTrace = event.stack_trace
      .split("\n").slice(0, 3).join("")
      .replace(/:\d+:\d+/g, "");
    const seed = `${event.service}:${event.environment}:${event.error_name}:${normalizedTrace}`;
    return createHash("sha256").update(seed).digest("hex");
  }
  public async processEvent(event: IncomingWebhookEvent, agentRunner: any): Promise<string> {
    const fingerprint = this.computeFingerprint(event);
    const existing = this.activeFingerprints.get(fingerprint);
    if (existing) {
      existing.count += 1;
      await this.appendOccurrence(existing.ticketId, event, existing.count);
      return `Actualizado ticket existente ${existing.ticketId} (Ocurrencia #${existing.count})`;
    }
    const draft: TicketDraft = await agentRunner.evaluate({
      task: "generate_support_ticket",
      context: { event, fingerprint,
        rules: "Si environment == 'production' y afecta checkout o pagos, severidad es P1" }
    });
    const newTicketId = await this.dispatchToLinear(draft);
    this.activeFingerprints.set(fingerprint, { ticketId: newTicketId, count: 1 });
    return `Creado nuevo ticket ${newTicketId} con severidad ${draft.severity}`;
  }
  private async appendOccurrence(ticketId: string, event: IncomingWebhookEvent, count: number): Promise<void> {
    console.log(`[Linear API] Anexando log a ${ticketId}: ${event.message} (total: ${count})`);
  }
  private async dispatchToLinear(draft: TicketDraft): Promise<string> {
    console.log(`[Linear API] Creando issue: ${draft.title} [${draft.severity}]`);
    return `LIN-${Math.floor(1000 + Math.random() * 9000)}`;
  }
}
```

Con un evento de fallo de pasarela en producción se crea el ticket (P1); si el mismo evento llega 2 s después por reintento, se **anexa** la ocurrencia en vez de duplicar.

---

## Sanitización de cargas útiles antes del despacho

Los reportes de excepciones contienen a menudo información sensible: cabeceras `Authorization`, cookies de sesión, emails o claves de conexión. Enviar eso a sistemas de tickets de terceros **vulnera privacidad** y amplía la superficie de ataque. Fase de sanitización antes de construir el resumen:

```python
import re
from typing import Dict, Any
REDACTED = "[REDACTED]"
PATTERNS = {
    "bearer_token": r"Bearer\s+[A-Za-z0-9\-._~+/]+=*",
    "api_key": r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?([A-Za-z0-9_\-]{16,})['\"]?",
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "credit_card": r"\b(?:\d[ -]*?){13,16}\b"
}
def sanitize_payload(raw_text: str) -> str:
    sanitized = raw_text
    sanitized = re.sub(PATTERNS["bearer_token"], f"Bearer {REDACTED}", sanitized)
    def redact_kv(match):
        key = match.group(1)
        return f"{key}={REDACTED}"
    sanitized = re.sub(PATTERNS["api_key"], redact_kv, sanitized)
    sanitized = re.sub(PATTERNS["email"], f"user_{REDACTED}@domain.com", sanitized)
    sanitized = re.sub(PATTERNS["credit_card"], f"CARD_{REDACTED}", sanitized)
    return sanitized
```

Entrada sucia → salida con `Bearer [REDACTED]`, `user_[REDACTED]@domain.com`, `CARD_[REDACTED]`, `api_key=[REDACTED]`.

> **REMEMBER del curso (correcto y central):** la sanitización de credenciales y PII debe hacerse **en memoria antes** de evaluar el prompt con el LLM, **no después**. Evita que los secretos queden registrados en el historial del proveedor o en cachés de inferencia.

### Check your understanding
**¿Qué medida de seguridad primero antes de procesar el ticket?**
- [x] **Sanitizar en memoria los encabezados y campos sensibles antes de construir el prompt del agente.**

---

## Ejercicio: motor de triage para Linear

`IncidentTriageEngine` (Python): recibe `service`, `status_code`, `error_type`, `raw_log`; sanitiza tokens `Bearer` y emails; clasifica severidad -
- **P1:** 500 o fallo de conexión en `service == 'billing'`.
- **P2:** 502/503 en servicios no de facturación, o 401 recurrentes en `auth`.
- **P3:** validación (400/422) o microservicios no críticos.
Genera el payload listo para la API de tickets.

```python
import hashlib
import re
from typing import Dict, Any
class IncidentTriageEngine:
    def __init__(self):
        self.seen_signatures = set()
    def sanitize(self, text: str) -> str:
        text = re.sub(r"Bearer\s+[A-Za-z0-9\-._~+/]+", "Bearer [REDACTED]", text)
        text = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[USER_EMAIL]", text)
        return text
    def compute_hash(self, event: Dict[str, Any]) -> str:
        seed = f"{event['service']}:{event.get('status_code', 0)}:{event['error_type']}"
        return hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16]
    def evaluate_severity(self, event: Dict[str, Any]) -> str:
        svc = event.get("service", "").lower()
        code = event.get("status_code", 0)
        if svc == "billing" and (code >= 500 or "timeout" in event.get("error_type", "").lower()):
            return "P1"
        if (code in (502, 503)) or (svc == "auth" and code == 401):
            return "P2"
        return "P3"
    def process(self, event: Dict[str, Any]) -> Dict[str, Any]:
        sig = self.compute_hash(event)
        is_duplicate = sig in self.seen_signatures
        if is_duplicate:
            return {"action": "UPDATE_OCCURRENCE", "signature": sig,
                    "message": f"Incidencia repetida detectada para {event['service']}. Ocurrencia sumada."}
        self.seen_signatures.add(sig)
        cleaned_log = self.sanitize(event.get("raw_log", ""))
        severity = self.evaluate_severity(event)
        return {"action": "CREATE_TICKET", "signature": sig,
                "ticket": {"title": f"[{severity}][{event['service'].upper()}] {event['error_type']}",
                    "severity": severity,
                    "team": "On-Call Engineering" if severity in ("P1", "P2") else "Product Support",
                    "body": f"### Resumen del fallo\n\n**Servicio:** {event['service']}\n**Código:** {event.get('status_code')}\n\n**Log sanitizado:**\n```\n{cleaned_log}\n```"}}
```

Bifurcación esperada: el primer evento sanitiza y crea (P1); el segundo, idéntico, es interceptado por la firma de idempotencia.

---

## Resumen

Combinación de velocidad de ingesta (webhook) con criterio analítico: **idempotencia por firma** (evita tormentas de tickets), **sanitización temprana en memoria** (impide fuga de claves/PII) y **matrices de severidad objetivas** (lo crítico llega a guardia; lo menor al backlog). La próxima etapa gestiona el **ciclo de vida local** con sincronizaciones en archivos de memoria del workspace.

**UP NEXT · Lección 16 de 30:** *Sincronización Proactiva en Archivos de Memoria* - **inicia el Módulo 4: Gestión Proactiva del Workspace.**

---

## Preguntas abiertas del propio curso ("Can you answer these?")

1. ¿Cómo manejar la idempotencia cuando un microservicio emite excepciones **ligeramente distintas** pero del mismo problema raíz?
2. ¿Qué estrategia usar si el gestor externo (Jira/Linear) devuelve **HTTP 429** por cuota durante una crisis?
3. ¿Por qué sanitizar **antes** de pasar el contexto al LLM en lugar de pedirle al modelo que oculte secretos?
4. ¿Cómo determina OpenClaw a qué equipo asignar el ticket cuando la alerta proviene de un servicio con **dependencias compartidas**?

(Anotadas para profundizar. La #1 y la #2 son los agujeros reales: fingerprint demasiado rígido, y 429 sin backoff.)

---

## Notas de verificación (Kanam)

**Núcleo de ingeniería: sólido y correcto** (estilo L14). Lo metodológico aplica:

- ✅ **Idempotencia por firma** antes de crear el ticket: correcto y central (anti-tormenta).
- ✅ **Sanitización en memoria ANTES del LLM**: correcto y crítico - evita que secretos entren al historial del proveedor. Es exactamente la disciplina del workspace (contenido externo = dato; no filtrar secretos).
- ✅ **Normalizar la traza** (omitir timestamps/números de línea dinámicos) antes de hashear: correcto.
- ✅ **Matriz de severidad objetiva** (P1-P4 por criterios), no "todo error es P1": criterio profesional.
- ✅ **Esquema estricto** para el borrador del ticket, no prosa libre.
- ✅ **PITFALL** (sin huella → duplicados en cascada) y **REMEMBER** (sanitizar antes del LLM): correctos.
- ✅ **Acierta el quiz** (sanitizar primero).
- ✅ El **ejercicio corre tal cual** (Python estándar): verifiqué la bifurcación → `CREATE_TICKET` (P1, billing 500) y luego `UPDATE_OCCURRENCE`. La sanitización funciona (`[USER_EMAIL]`, `Bearer [REDACTED]`).

**Discrepancia detectada (firma fabricada):**
- ❌ **El output del curso está MAL.** Promete `'signature': '2c8c4e532b26090a'` para `sha256("billing:500:GatewayTimeoutException")[:16]`, pero el valor real es **`2af43d9ebb55c38b`**. Corrí el código del curso textualmente: la firma no coincide. **El print del ejemplo no sale de ejecutar el código que el propio curso muestra** - mismo patrón que L01/L02/L04. (El resto de la salida sí coincide.)

**Lo que NO es feature nativa de OpenClaw (el curso lo presenta como "OpenClaw actúa/debe"):**
- ❌ **No hay integración nativa de tickets** con Jira/Linear/GitHub Issues como "puente" del producto. Hay un plugin **`workboard`** relacionado, pero la creación de tickets vía Linear es un pipeline que **se construye encima** (herramientas propias), no una capacidad de OpenClaw. Coherente con L11/L14: la superficie real son `hooks.mappings` + transforms + turno de agente.
- ❌ **`TicketAutomationHandler` / `agentRunner.evaluate` / `dispatchToLinear`**: API inventada (no existe en el SDK).
- ⚠️ **`activeFingerprints = new Map(...)` en memoria:** para idempotencia real, un `Map` local **falla en multi-réplica** (cada instancia dedup por su cuenta → sigue habiendo duplicados). El mismo hueco que L05/L08/L14; el material no lo señala (aunque su pregunta #1 roza el tema).
- ⚠️ **P1-P4, umbrales y reglas de severidad:** plausibles, pero son **parámetros de diseño**, no defaults del producto.
- ⚠️ La **caché de idempotencia sin TTL/ventana** explota en memoria en un servicio de larga vida (el material no lo acota, a diferencia de L14).

**Verificación ejecutable:**
- ✅ Node/Python estándar; el ejercicio Python corre sin dependencias.
- ⚠️ `createHash` de `node:crypto` disponible (el handler TS correría, salvo que `agentRunner`/Linear son simulados).

**Patrón (decimoquinto caso, consistente):** **buena ingeniería** (idempotencia por firma, sanitización pre-LLM, severidad objetiva, esquema estricto) montada sobre una **integración que el producto no tiene** (`TicketAutomationHandler`, Linear nativo) y con un **output fabricado** (la firma `2c8c…`). El *qué* es correcto y valioso; el *cómo* se escribe contra herramientas propias + `hooks.*`. **Cierra el Módulo 3.**

**Cierre del Módulo 3.** Con esta lección se completan las 5 lecciones prometidas de *Ingesta Dirigida por Eventos* (L11-L15). La Lección 16 abre el **Módulo 4: Gestión Proactiva del Workspace** (arranca con *Sincronización Proactiva en Archivos de Memoria*).
