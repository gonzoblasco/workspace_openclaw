# Módulo 3 · Lección 12 de 30: Extracción de Datos Críticos desde Notificaciones

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 3 - Ingesta Dirigida por Eventos
**Lección:** 12 de 30
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

Un webhook entrega un cuerpo HTTP sin procesar: un JSON voluminoso, anidado y repleto de metadatos irrelevantes. Si inyectás la carga útil completa en la ventana de contexto, agotás la cuota de tokens, diluís la atención del modelo y subís la latencia. La **extracción de datos críticos** aísla exclusivamente las variables operativas indispensables (identificadores, estados, marcas temporales, importes) **antes** de invocar la lógica agéntica.

OpenClaw lo implementa con **esquemas de transformación intermedia** en el punto de entrada: en lugar de procesar los 500 campos de un evento de GitHub/Stripe/Datadog, proyecta la notificación en un **payload mínimo validado**. Esa reducción decide qué información merece alterar la memoria de trabajo y qué se descarta en el perímetro de red.

---

## Arquitectura de filtrado y proyección

Tres fases **deterministas** antes de que intervenga cualquier LLM:
1. **Valida** integridad criptográfica y procedencia.
2. **Aplica una máscara de campos / selector** que poda ramas innecesarias del árbol de datos.
3. **Asigna tipos estrictos** a los valores, garantizando estructuras predecibles.

El objetivo es **erradicar el ruido sintáctico**. Una alerta de PagerDuty puede traer IDs de asignación interna, links a UI, telemetría y configs de escalado. Para la decisión inmediata, solo importan tres cosas: **servicio afectado, severidad y mensaje de error canónico**.

Los datos brutos descartados **no se pierden**: se persisten en registros secundarios fríos para auditoría, pero **aislados del bucle de razonamiento activo**. Esto evita que el agente deambule procesando avatares, listas de URLs o cabeceras de depuración.

---

## Especificación declarativa de esquemas

OpenClaw usa **descriptores declarativos** para extraer variables atómicas sin acoplar código a cada proveedor. Cada extractor formaliza tres propiedades: **ruta** en el objeto original, **tipo** destino, y **estrategia de recuperación** si falta o está vacío.

```json
{
  "source_event": "github.deployment_status",
  "critical_fields": {
    "deployment_id": { "path": "deployment.id", "type": "integer", "required": true },
    "environment": { "path": "deployment.environment", "type": "string", "required": true },
    "state": { "path": "deployment_status.state", "type": "string",
      "enum": ["success", "failure", "error", "pending"], "required": true },
    "initiator": { "path": "sender.login", "type": "string",
      "required": false, "default": "system" },
    "target_commit": { "path": "deployment.sha", "type": "string",
      "transform": "slice:0:7", "required": true }
  }
}
```

El procesador perimetral evalúa la directiva en memoria. Si un campo `required: true` no existe o no cumple el tipo, el evento **se rechaza** antes de emitir cualquier tarea al agente.

> **PITFALL del curso (correcto):** confiar en fallbacks silenciosos o sustituir tipos incorrectos por vacíos **degrada la fiabilidad**. Si un ID de despliegue llega `null`, la ejecución debe detenerse en el extractor; si no, el agente llamará herramientas con identificadores inexistentes.

---

## Compresión y ratios de reducción

Tabla del curso (JSON crudo vs. payload filtrado):

| Fuente del Evento | Tamaño Bruto | Tokens en Bruto | Payload Filtrado | Tokens Filtrados | Ratio |
|---|---|---|---|---|---|
| GitHub Webhook | ~42 KB | ~10.500 | 185 B | ~45 | 99.5% |
| Stripe Invoice | ~18 KB | ~4.500 | 120 B | ~30 | 99.3% |
| PagerDuty Incident | ~28 KB | ~7.000 | 210 B | ~52 | 99.2% |
| Datadog Alert | ~12 KB | ~3.000 | 140 B | ~35 | 98.8% |

La reducción no solo baja el costo por llamada: elimina de raíz **alucinaciones por información colateral** compitiendo en la ventana de contexto.

---

## Implementación de un procesador de notificaciones

```python
import hmac
import hashlib
import json
from typing import Any, Dict, Optional

class CriticalPayloadExtractor:
    def __init__(self, webhook_secret: str):
        self.secret = webhook_secret.encode("utf-8")

    def verify_signature(self, raw_body: bytes, header_signature: str) -> bool:
        """Verifica la firma SHA256 para evitar inyección de eventos ilegítimos."""
        expected_sig = "sha256=" + hmac.new(
            self.secret, raw_body, hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected_sig, header_signature)

    def extract_incident_data(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae de forma determinista únicamente las dimensiones críticas."""
        try:
            incident = payload["incident"]
            critical_record = {
                "incident_id": str(incident["id"]),
                "service_name": str(incident["service"]["name"]),
                "urgency": str(incident["urgency"]).lower(),
                "summary": str(incident["title"]).strip(),
                "created_at": str(incident["created_at"]),
                "impacted_hosts": [
                    host["hostname"]
                    for host in incident.get("impacted_entities", [])
                    if host.get("type") == "host"
                ],
            }
            if not critical_record["incident_id"] or not critical_record["service_name"]:
                raise ValueError("Campos obligatorios vacíos en el origen.")
            return critical_record
        except (KeyError, TypeError) as err:
            raise ValueError(f"Estructura del payload incompatible: {err}") from err
```

Salida (7 campos, concisa y tipada):
```json
{
  "incident_id": "INC-88912",
  "service_name": "payments-database",
  "urgency": "high",
  "summary": "High memory consumption on db-worker-04",
  "created_at": "2025-05-18T14:32:01Z",
  "impacted_hosts": ["db-worker-04.internal"]
}
```

> **REMEMBER del curso (correcto y central):** **nunca** delegues el filtrado/resumen de un JSON gigante al propio LLM. El filtrado determinista cuesta <1 ms de CPU y **cero tokens**; pasar el crudo al LLM añade latencia y riesgo.

### Check your understanding
**Un webhook envía 45 KB de telemetría anidada. ¿Estrategia recomendada?**
- [x] **Procesar con un extractor determinista (código o JMESPath) que envíe solo un objeto mínimo al agente.**

---

## Normalización y enriquecimiento contextual mínimo

Emisores distintos nombran el mismo concepto con vocabularios heterogéneos: Stripe `charge.failed`, PayPal `PAYMENT.CAPTURE.DENIED`, propio `tx_declined`. OpenClaw usa una **tabla de asignación canónica** acoplada al extractor:

```text
Stripe: "charge.failed"      -> event_type: "payment_failed"
PayPal: "PAYMENT.CAPTURE..." -> event_type: "payment_failed"
GitHub: "check_suite.rereq"  -> event_type: "ci_build_triggered"
GitLab: "Pipeline Hook"      -> event_type: "ci_build_triggered"
```

Además, **enriquecimiento atómico**: si un error solo trae `cus_9881a`, el extractor puede consultar una **caché local** para añadir `tier: "enterprise"`, y el agente sabe de inmediato si escalar sin consultar herramientas externas dentro del bucle.

> **TIP del curso (correcto):** si una consulta de enriquecimiento tarda **>50 ms** o depende de una red inestable, **no la ejecutes en el extractor perimetral**: añadila como **herramienta explícita** que el agente invoca solo cuando lo necesita.

---

## Preguntas abiertas del propio curso ("Can you answer these?")

1. ¿Cómo gestiona OpenClaw un cambio inesperado en el esquema JSON de un proveedor externo?
2. ¿Conviene procesar la firma criptográfica antes o después de parsear el JSON?
3. ¿Qué impacto tiene en la latencia global hacer enriquecimiento en el extractor perimetral?
4. ¿Cómo se auditan los campos descartados si luego se detecta que un incidente requería información omitida?

(Anotadas para profundizar. La #3 la responde el propio TIP; la #2 la responde la L11: se verifica sobre bytes crudos, antes de parsear.)

---

## Notas de verificación (Kanam)

**La filosofía es de las más valiosas y correctas del curso.** Todo lo metodológico aplica:

- ✅ **Filtrar en el perímetro con código determinista, no con el LLM**: correcto y central. Cuesta ~0 tokens vs. miles. Coincide con la disciplina del workspace (no meter crudo ajeno al contexto).
- ✅ **Tipado estricto + `required`**: rechazar el evento si falta un campo crítico, en vez de fallback silencioso. Correcto (evita llamadas a herramientas con IDs inexistentes).
- ✅ **Datos descartados → registro frío aislado**: buena práctica de auditoría.
- ✅ **Normalización canónica** de vocabularios externos: patrón real y sano.
- ✅ **TIP del enriquecimiento** (>50 ms o red inestable → herramienta explícita, no en el perímetro): criterio correcto de diseño.
- ✅ **PITFALL de fallbacks silenciosos**: correcto.
- ✅ El **ejercicio corre tal cual** (Python estándar): verifiqué la salida → exactamente los 6 campos (incident_id, service_name, urgency, summary, created_at, impacted_hosts) con `urgency` en minúscula y solo el host (no el cluster). `verify_signature` funciona (ok/mala).

**Lo que NO coincide con la instalación real:**
- ❌ **No existe un "motor de esquemas declarativos" con `critical_fields`/`path`/`type`/`enum`/`transform` en OpenClaw.** Ese JSON es **inventado**. El mapeo real de hooks es **`hooks.mappings`** (+ `hooks.presets`, `transformsDir`), con **transforms en JS/TS** (template o transform local), **no** un descriptor declarativo de campos por proveedor.
- ❌ **JMESPath no es el mecanismo de OpenClaw** (el curso lo ofrece como "como JMESPath o selectores de rutas JSON"). Además, **`jmespath` no está instalado** aquí; el ejemplo no correría vía JMESPath.
- ⚠️ **La firma SHA256 se reusa de la L11** - OpenClaw autentica hooks con **Bearer token** (`hooks.token`), no con HMAC (mismo matiz que la L11).
- ⚠️ **La tabla de ratios** (tamaños/tokens) es **plausible pero no verificable**: son estimaciones redondas del curso, no medidas de esta instalación. El *concepto* de reducción es correcto; los números, ilustrativos.

**Verificación ejecutable:**
- ✅ `CriticalPayloadExtractor` corre sin dependencias y produce el resultado prometido (exit 0).
- ⚠️ El secreto del ejemplo (`claw_secret_prod_key`) es un **placeholder**, no una credencial real.

**Patrón (duodécimo caso):** el **concepto es de lo mejor del curso** (perímetro determinista, tipado, cero-token filtering, no meter crudo al LLM) y el **ejercicio corre de verdad**. La fachada inventada es el **motor de esquemas declarativos** (`critical_fields` + JMESPath), que en el producto real es **`hooks.mappings` con transforms JS/TS**. Traducir: el *qué* (podar en el perímetro) se implementa con la superficie real de mappings/transforms, no con un descriptor YAML/JSON ficticio.

**Nota de contexto (Módulo 3):** tras esta L12 el propio curso indica *"3 lessons left in Ingesta Dirigida por Eventos"* → Módulo 3 = 5 lecciones (L11-L15). Lección 13: *Actualización Reactiva de Documentación Interna*.
