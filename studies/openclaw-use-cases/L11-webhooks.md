# Módulo 3 · Lección 11 de 30: Recepción de Disparadores Externos vía Webhooks

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 3 - Ingesta Dirigida por Eventos
**Lección:** 11 de 30 · **abre el Módulo 3**
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.
> **Nota de seguridad:** el material incluye una "secret" hardcodeada (`k9J#mP2$vL8@zQ5!`). Se registra como **placeholder pedagógico**; no es una credencial ni se usa.

---

## Idea central

Las tareas cron y heartbeats **consultan** el entorno por sondeo. Cuando ocurre un despliegue fallido en GitHub, un pago bloqueado en Stripe o una alerta en Grafana, esperar al siguiente ciclo introduce latencia inaceptable y quema cómputo. Un **webhook invierte la dinámica**: el servicio externo toma la iniciativa y envía un `POST` directamente a un endpoint de OpenClaw **en el instante** de la mutación.

Para actuar en tiempo real, el agente debe exponer una **superficie de red segura** capaz de autenticar la procedencia, transformar el cuerpo del mensaje en un **evento estructurado** y despertar el bucle agéntico con **contexto aislado**.

---

## Anatomía de un endpoint de entrada

Los webhooks **no se inyectan directamente** en la ventana de contexto del LLM: eso saturaría la memoria con cabeceras HTTP irrelevantes y expondría al agente a inyección de instrucciones. El subsistema opera en una **capa desacoplada** que valida el transporte antes de alertar al planificador.

Tres fases secuenciales:

1. **Terminación HTTP y verificación criptográfica:** el servidor intercepta la solicitud, comprueba que sea `POST` y valida la **firma criptográfica** contra un secreto compartido local.
2. **Normalización del evento:** el cuerpo JSON se transforma en un evento estandarizado con **identificador único**, **sello de tiempo** y **etiqueta de origen** (`github.push`, `stripe.charge_failed`).
3. **Despacho al canal de eventos:** el evento entra en la **cola interna de tareas reactivas**; puede interrumpir el reposo o encolarse según la política de concurrencia.

El receptor debe confirmar con **`200 OK` o `202 Accepted` en menos de 2 s**. Si la invocación del modelo retrasara la respuesta HTTP, GitHub/Stripe considerarían la entrega fallida y **reintentarían**, introduciendo duplicados en cascada.

---

## Verificación de firmas criptográficas (HMAC)

Exponer un puerto público convierte al agente en objetivo. Cargas falsas podrían inducir a ejecutar comandos o publicar mensajes no deseados. Por eso el curso hace **obligatoria** la verificación de integridad **HMAC-SHA256**: el emisor firma el **cuerpo binario** con una clave compartida y adjunta el resultado en una cabecera (`X-Hub-Signature-256` en GitHub, `Stripe-Signature` en Stripe). El receptor recalcula el hash sobre los **bytes originales** y compara en **tiempo constante** para mitigar ataques de temporización.

```python
import hmac
import hashlib
from typing import Optional

def verify_webhook_signature(raw_payload: bytes, received_signature: Optional[str], secret_key: str) -> bool:
    if not received_signature:
        return False
    expected_prefix = "sha256="
    if received_signature.startswith(expected_prefix):
        clean_signature = received_signature[len(expected_prefix):]
    else:
        clean_signature = received_signature
    computed_hmac = hmac.new(
        key=secret_key.encode("utf-8"),
        msg=raw_payload,
        digestmod=hashlib.sha256,
    ).hexdigest()
    # compare_digest evita timing attacks comparando byte a byte en tiempo fijo
    return hmac.compare_digest(computed_hmac, clean_signature)
```

> **PITFALL del curso (correcto y crítico):** **nunca** uses `json.dumps(request.json)` para reconstruir la carga útil antes de calcular la firma. Los serializadores **reordenan claves** y alteran espacios, cambiando los bytes exactos y provocando fallos de verificación. Captura los **bytes puros** del flujo de red (`request.get_data()` o el socket crudo).

---

## Implementación de un ingress server

El curso propone un **micro-servicio de ingesta** (puerto secundario o detrás de un proxy inverso: Nginx, Cloudflare Tunnels) con **FastAPI**:

```python
import os
import uuid
import time
from fastapi import FastAPI, Request, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="OpenClaw Webhook Ingress")
WEBHOOK_SECRET = os.getenv("OPENCLAW_WEBHOOK_SECRET", "k9J#mP2$vL8@zQ5!")  # placeholder

class IngressEvent(BaseModel):
    event_id: str
    source: str
    timestamp: float
    payload: dict

@app.post("/api/v1/ingress/{source}")
async def receive_webhook(source: str, request: Request):
    raw_body = await request.body()                       # bytes exactos
    signature = request.headers.get("X-Hub-Signature-256")
    if not verify_webhook_signature(raw_body, signature, WEBHOOK_SECRET):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Firma digital inválida o ausente.")
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Cuerpo no convertible a JSON.")
    normalized_event = IngressEvent(
        event_id=f"evt_{uuid.uuid4().hex[:12]}",
        source=source,
        timestamp=time.time(),
        payload=data,
    )
    await dispatch_to_agent_queue(normalized_event)       # sin bloquear la respuesta
    return {"status": "accepted", "event_id": normalized_event.event_id}

async def dispatch_to_agent_queue(event: IngressEvent):
    print(f"[OpenClaw] Encolado evento {event.event_id} desde origen '{event.source}'")
```

Prueba con `curl` calculando la firma con `openssl`:

```bash
PAYLOAD='{"action":"opened","issue":{"number":42,"title":"Base de datos saturada"}}'
SECRET="k9J#mP2$vL8@zQ5!"
SIGNATURE=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | sed 's/^.* //')
curl -X POST http://localhost:8000/api/v1/ingress/github \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: sha256-$SIGNATURE" \
  -d "$PAYLOAD"
```

---

## Idempotencia y ventana de entrega

Los webhooks operan con garantía **at-least-once**. Un reintento tras una demora de red duplicaría incidencias y saturaría el workspace. Solución: un **registro de idempotencia con ventana deslizante**.

```python
import time

class IdempotencyRegistry:
    def __init__(self, ttl_seconds: int = 3600):
        self._seen_events: dict[str, float] = {}
        self.ttl = ttl_seconds

    def is_duplicate(self, idempotency_key: str) -> bool:
        now = time.time()
        self._purge_expired(now)
        if idempotency_key in self._seen_events:
            return True
        self._seen_events[idempotency_key] = now + self.ttl
        return False

    def _purge_expired(self, current_time: float):
        expired = [k for k, exp in self._seen_events.items() if exp <= current_time]
        for k in expired:
            del self._seen_events[k]
```

La **clave de idempotencia** debe usar identificadores intrínsecos del emisor (`X-GitHub-Delivery`, el `id` de Stripe), **no** la marca de llegada.

> **REMEMBER del curso (correcto):** un webhook repetido se reconoce con **`200 OK`** inmediato, pero su carga se **descarta antes de despertar al agente**. Responder con error provocaría que el emisor reintente indefinidamente.

---

## Inyección del disparador en el workspace

Un webhook **carece de interlocutor humano**, así que el sistema crea una **sesión de ejecución efímera**. Tres componentes en el contexto del agente:

- **`source_tag`:** canal técnico de origen (`github/issue_comment`, `stripe/invoice_payment_failed`, `pagerduty/incident`).
- **`event_payload`:** cuerpo JSON **simplificado**, restringido a campos relevantes para minimizar el uso de contexto.
- **Instrucción de enrutamiento inmediato:** un **metaprompt** que define la meta de la sesión **sin alterar** `SOUL.md`.

Según el curso, un archivo `triggers.json` (o equivalente) mapea tipo de evento → perfil de agente:

```json
{
  "webhooks": {
    "github.issues.opened": {
      "agent_profile": "triage_engineer",
      "priority": "normal",
      "context_injection": { "memory_namespace": "external_triggers", "timeout_seconds": 60 }
    },
    "datadog.alert.critical": {
      "agent_profile": "ops_incident_responder",
      "priority": "high",
      "context_injection": { "memory_namespace": "incidents", "timeout_seconds": 180 }
    }
  }
}
```

El despachador instancia el agente asignado, carga sus herramientas permitidas y despierta el bucle con un prompt de sistema ajustado:

```text
[SISTEMA - DISPARADOR EXTERNO]
Origen: github.issues.opened
Identificador de evento: evt_9b1a8f34d10c
Datos de entrada:
{
  "issue_id": 42,
  "title": "Base de datos saturada",
  "author": "devops-team"
}
Acción requerida: Evalúa la entrada y determina si se requiere intervención según las reglas operativas locales.
```

---

## Ejercicio: validador y despachador de webhooks

`handle_incoming_webhook(headers, raw_body, secret, registry) -> (int, str)`: extrae `X-Signature-SHA256` y `X-Event-ID`; devuelve **401** si la firma no coincide, **200** si el ID ya fue visto, **202** si es válido y nuevo.

```python
import hmac
import hashlib

class MemoryIdempotencyRegistry:
    def __init__(self):
        self.seen = set()
    def exists(self, event_id: str) -> bool:
        return event_id in self.seen
    def record(self, event_id: str):
        self.seen.add(event_id)

def handle_incoming_webhook(headers: dict, raw_body: bytes, secret: str,
                            registry: MemoryIdempotencyRegistry) -> tuple[int, str]:
    received_sig = headers.get("X-Signature-SHA256", "")
    event_id = headers.get("X-Event-ID")
    if not event_id:
        return 400, "Cabecera X-Event-ID requerida"
    computed_sig = hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(computed_sig, received_sig):
        return 401, "Firma no autorizada"
    if registry.exists(event_id):
        return 200, "Evento ignorado por duplicado"
    registry.record(event_id)
    return 202, "Evento encolado para OpenClaw"
```

Batería de aserciones: válido → 202; reintento idéntico → 200; firma falsa → 401.

---

## Resumen

La ingesta por webhooks da a OpenClaw capacidad **reactiva inmediata** sin la sobrecarga del sondeo. La seguridad depende de **desacoplar la respuesta HTTP de la inferencia**, verificar **firmas criptográficas en tiempo constante** y aplicar **idempotencia** contra duplicados. Lo siguiente: depurar qué partes del JSON merecen ocupar la memoria de trabajo.

**UP NEXT · Lección 12 de 30:** *Extracción de Datos Críticos desde Notificaciones*. Faltan **4 lecciones** para cerrar el Módulo 3 (*Ingesta Dirigida por Eventos*).

---

## Preguntas abiertas del propio curso ("Can you answer these?")

1. ¿Cómo gestionar **rotaciones de secretos HMAC** sin caídas de servicio?
2. ¿Qué estrategia de red usar para exponer el puerto del webhook si el agente corre en una máquina local?
3. ¿Cómo afecta un volumen masivo de webhooks concurrentes a la cola de inferencia?
4. ¿Por qué no almacenar el payload completo de todos los webhooks en el contexto principal?

(Anotadas para profundizar.)

---

## Notas de verificación (Kanam)

**Acá hay un giro importante: el webhook SÍ es una feature real de OpenClaw** (a diferencia de las fachadas inventadas de otras lecciones). Pero la **pieza central del curso (HMAC) no es como OpenClaw autentica**.

| El curso dice | OpenClaw real |
|---|---|
| OpenClaw expone endpoints HTTP para webhooks entrantes | ✅ **Real.** `hooks.enabled`, `hooks.token`, `hooks.path` (default `/hooks`). Rutas: `POST /hooks/agent`, `POST /hooks/wake`, `POST /hooks/<name>` (mapped). Deshabilitados por defecto. |
| Puerto local para el receptor | ✅ El Gateway escucha en **`127.0.0.1:18789`** (coincide con el `18789` ya visto en L06). |
| **Autenticación por firma HMAC-SHA256** como mecanismo obligatorio | ❌ **OpenClaw usa `Authorization: Bearer <token>`**, no HMAC. El curso hace de HMAC el corazón del diseño; en el producto, la autenticación es un **hook token** dedicado. HMAC aplica a *cómo GitHub/Stripe firman sus propios webhooks*, no a cómo OpenClaw los autentica. |
| **Idempotencia con ventana** para duplicados | ✅ **Real y alineado.** El doc pide reusar un **`Idempotency-Key`** en reintentos: *"a replayed 200 does not run the agent again"*. El concepto del curso mapea bien. |
| Despertar al agente con contexto **aislado** | ✅ **Real:** `sessionMode: "isolated"` (vs `"persistent"` con `sessionKey`). |
| Responder rápido (`2xx`) y no bloquear en la inferencia | ✅ Alineado: el hook admite la corrida y responde; `deliver` controla el anuncio. |
| **Contenido externo = dato; no inyectar en el contexto crudo** | ✅ **La doc lo dice casi igual:** *"Treat external event content as data. Agent hook content is safety-wrapped by default… Use a restricted agent for untrusted inputs"*. Coincide con la regla de sandbox del workspace. |
| Payload restringido a campos relevantes | ✅ Buena práctica; la doc recomienda restringir herramientas/agente para input no confiable. |

**Lo que NO existe en la instalación real (inventado):**
- ❌ **La ruta `/api/v1/ingress/{source}` es inventada.** Las reales son `/hooks/agent`, `/hooks/wake` y `/hooks/<name>`.
- ❌ **El `ingress server` FastAPI como parte de OpenClaw no existe.** OpenClaw **ya sirve** los hooks desde el Gateway; no se levanta un micro-servicio propio. (El patrón FastAPI es válido como *tu* integración externa, pero no es "la arquitectura de OpenClaw".)
- ❌ **`OPENCLAW_WEBHOOK_SECRET` no es una variable real.** La credencial del hook es `hooks.token` en `openclaw.json` (Bearer), no una env var HMAC.
- ❌ **`triggers.json` no existe.** El mapeo real es **`hooks.mappings`** en la config, con templates o transforms JS/TS locales - no un `triggers.json` en la raíz.
- ⚠️ **El secreto hardcodeado `k9J#mP2$vL8@zQ5!`** aparece en el código; registrado como **placeholder**, jamás como valor real.
- ⚠️ **`X-Hub-Signature-256` / `X-Signature-SHA256`:** válidos como cabeceras *de GitHub/tus emisores*, pero OpenClaw **no** las verifica por defecto (usa el token).

**Verificación ejecutable:**
- ✅ El ejercicio **corre tal cual** (Python estándar): verifiqué las tres aserciones → `202` / `200 "duplicado"` / `401`, salida *"Todas las validaciones del ingress server pasaron exitosamente."* (exit 0). `verify_webhook_signature` también funciona (con y sin prefijo `sha256=`).
- ✅ `hmac.compare_digest` para comparación en tiempo constante: correcto.

**Patrón (undécimo caso, con matiz nuevo):** por primera vez el **tema sí existe** en el producto (webhooks). El curso acierta la **filosofía** (reactivo > sondeo, desacople HTTP/inferencia, idempotencia, evento como dato, sesión aislada) y **yerra la superficie**: inventa HMAC como auth de OpenClaw (es Bearer token), una ruta `/api/v1/ingress`, un `triggers.json` y un micro-servicio propio cuando el Gateway ya lo trae. Buena lección para el *porqué*; la *implementación* se escribe contra `hooks.*` reales.

**Nota de contexto (Módulo 3):** tras esta L11 el propio curso indica *"4 lessons left in Ingesta Dirigida por Eventos"* → Módulo 3 = 5 lecciones (L11-L15). Lección 12: *Extracción de Datos Críticos desde Notificaciones*.
