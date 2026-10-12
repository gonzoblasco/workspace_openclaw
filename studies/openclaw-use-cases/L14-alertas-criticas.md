# Módulo 3 · Lección 14 de 30: Alertas Automatizadas Frente a Errores Críticos

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 3 - Ingesta Dirigida por Eventos
**Lección:** 14 de 30
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

Una alerta automatizada **no** es una retransmisión cruda de un log hacia un canal de chat. Reenviar la traza completa de un webhook colapsa los canales y genera **fatiga de alertas**. En OpenClaw, una alerta crítica es el resultado de un **pipeline reactivo**: filtrar ruido, determinar severidad real, **enriquecer** con contexto del workspace y notificar por canales de alta prioridad **solo** cuando se superan umbrales estrictos.

El objetivo: convertir excepciones crudas de sistemas de monitoreo (Sentry, Datadog, CloudWatch) en **decisiones accionables**. Si el agente no distingue un fallo transitorio de red de una caída de la DB transaccional, la guardia termina **ignorando todas** las notificaciones.

---

## Arquitectura de evaluación de severidad y enrutamiento

Cuatro fases consecutivas: **ingestión → clasificación de impacto → deduplicación contextual → despacho multicanal**. En la ingestión, en vez de asumir que todo error 500 despierta a un ingeniero, el agente contrasta metadatos: **número de usuarios afectados** en la ventana, **entorno** (production vs. staging) y **tasa de repetición**.

### Tres niveles de severidad

| Nivel | Descripción | Acción |
|---|---|---|
| **P3 (Informativo / Bajo)** | Excepciones controladas, fallos en tareas secundarias, errores aislados en entornos no productivos. | Se **archivan localmente** sin notificar. |
| **P2 (Advertencia / Medio)** | Degradación parcial, latencia anormal, picos moderados de 4xx/5xx sin interrupción total. | Mensaje al **canal general** de monitoreo, **sin** etiquetar guardia. |
| **P1 (Crítico / Alto)** | Caída de servicios core, bloqueos de DB, fallos de autenticación masivos en producción. | Alerta directa con **mención urgente** a la guardia + canales secundarios (llamada/SMS). |

---

## Control de tormentas de alertas y deduplicación en memoria

La deduplicación y el control de **alert storms** son la pieza técnica más delicada. Si una DB colapsa 2 minutos, Sentry puede emitir **4.500 webhooks idénticos**; procesarlos todos bloquearía al personal y saturaría las cuotas.

**Ventana deslizante basada en huellas (fingerprints).** Al recibir la carga, el agente extrae una **clave canónica**:

```text
IncidentFingerprint = SHA256(service + exception_class + source_location)
```

Reglas de la lógica:

- **Primera ocurrencia:** si el fingerprint no existe en la ventana activa (p. ej. 15 min), se inicializa el contador en 1, se clasifica la severidad y se envía la alerta.
- **Ocurrencias subsecuentes en ventana:** se incrementa el contador **sin** despachar mensajes individuales.
- **Resumen de saturación:** si el contador supera un umbral (p. ej. 50) o la ventana expira, se genera **un único** mensaje de consolidación: *"Incidente recurrente: 54 eventos adicionales detectados en los últimos 15m"*.

> **PITFALL del curso (correcto):** **no** uses huellas basadas solo en el mensaje de error textual. Muchas excepciones incluyen IDs dinámicos, timestamps o parámetros (`Database connection failed for user_id=9812`). Hashear el mensaje en bruto **rompe la deduplicación** y genera cientos de alertas paralelas para el mismo fallo raíz.

---

## Enriquecimiento del incidente con contexto del workspace

La ventaja de un agente sobre un bot de chat estático: **inspección del contexto local**. Confirmado un P1, antes de notificar, el agente ejecuta:

1. **Lectura de despliegues recientes:** registro local del workspace o historial Git → ¿hubo release en los últimos 30 min?
2. **Inspección de runbooks internos:** si el error es `DeadlockDetected`, busca el procedimiento en `runbooks/db-deadlocks.md`.
3. **Generación de informe sintetizado:** combina datos del webhook + commit sospechoso + enlace al runbook.

### Controlador del webhook handler

```javascript
import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';

// Almacén en memoria para control de deduplicación
const incidentWindowMs = 15 * 60 * 1000;
const incidentCache = new Map();

export async function handleCriticalAlertWebhook(req, res, agentContext) {
  const payload = req.body;
  const { service, exception, environment, location, affectedUsers } = payload;

  // 1. Filtrado inmediato de entornos no productivos de bajo impacto
  if (environment !== 'production' && affectedUsers < 5) {
    return res.status(200).json({ status: 'ignored', reason: 'non-prod low impact' });
  }

  // 2. Cálculo canónico del fingerprint
  const rawKey = `${service}:${exception.name}:${location.file}:${location.line}`;
  const fingerprint = crypto.createHash('sha256').update(rawKey).digest('hex').slice(0, 12);
  const now = Date.now();
  const existing = incidentCache.get(fingerprint);

  // 3. Manejo de deduplicación en ráfaga
  if (existing && (now - existing.firstSeen) < incidentWindowMs) {
    existing.occurrences += 1;
    existing.lastSeen = now;
    return res.status(200).json({
      status: 'deduplicated',
      fingerprint,
      count: existing.occurrences
    });
  }

  // Registrar nueva entrada en la ventana activa
  incidentCache.set(fingerprint, { firstSeen: now, lastSeen: now, occurrences: 1 });

  // 4. Determinación de severidad
  const isP1 = affectedUsers > 50 || exception.name === 'DatabaseConnectionError';
  const severity = isP1 ? 'P1-CRITICAL' : 'P2-WARNING';

  // 5. Enriquecimiento contextual desde el workspace
  let runbookExcerpt = 'Sin runbook específico encontrado.';
  try {
    const runbookPath = path.join(agentContext.workspaceRoot, 'docs', 'runbooks', `${service.toLowerCase()}.md`);
    const content = await fs.readFile(runbookPath, 'utf-8');
    runbookExcerpt = content.slice(0, 200).trim() + '...';
  } catch {
    // Si no existe runbook local, se mantiene el texto por defecto
  }

  // 6. Formateo y despacho de la alerta estructurada
  const alertPayload = {
    severity,
    fingerprint,
    service,
    message: exception.message,
    runbook: runbookExcerpt,
    occurrences: 1,
    mentionTarget: isP1 ? '@on-call-team' : null
  };
  await agentContext.channels.dispatch('incident-alerts', alertPayload);
  return res.status(200).json({ status: 'dispatched', fingerprint, severity });
}
```

Respuesta del endpoint con un evento real (DB caída en producción, 120 usuarios afectados):

```json
{
  "status": "dispatched",
  "fingerprint": "a9f3b8c210e4",
  "severity": "P1-CRITICAL"
}
```

En el canal destino, el mensaje es una **ficha estructurada**, no un volcado de 80 líneas:

```text
🚨 [P1-CRITICAL] PostgresPool - Conexión agotada en producción
Huella: a9f3b8c210e4 | Usuarios afectados: 120 | Destinatario: @on-call-team
Error: Timeout waiting for connection from pool after 30000ms
Guía rápida (docs/runbooks/postgrespool.md):
"1. Comprobar métricas de conexiones activas en Grafana.
2. Reiniciar los workers auxiliares si el bloqueo persiste..."
```

### Check your understanding
**¿Qué estrategia al calcular el fingerprint evita tormentas de alertas ante una caída masiva?**
- [x] **Calcular la huella solo con el nombre del servicio, la clase de la excepción y la ubicación en código (archivo y línea).**

---

## Protocolos de escalado y derivación multicanal

Escalado **progresivo**: un P2 que persiste >45 min sin confirmación humana **asciende** de severidad. Combina el receptor de eventos con un **temporizador de escalado diferido**. Al despachar un P1/P2 a un canal interactivo, se adjuntan botones como `[Confirmar recepción]` o `[Silenciar 1h]`. Si nadie interactúa (p. ej. 10 min para P1), el agente activa el siguiente nivel:

1. **Primer salto:** mención directa individual al ingeniero de guardia principal.
2. **Segundo salto:** webhook saliente hacia un servicio telefónico de llamadas/SMS corporativo.
3. **Registro de falta de respuesta:** documentar en el log de auditoría que la alerta no fue atendida.

> **REMEMBER del curso (correcto):** todo escalado automático debe ser **idempotente** y contar con un **disyuntor (circuit breaker) global**. Si el proveedor de red falla, debe detener los reintentos tras un número **finito** de ciclos para no saturar las APIs externas.

---

## Ejercicios

**Ejercicio 1 - Deduplicación con ventana deslizante.** `shouldAlert(incident, cache, windowMinutes)` con `{ service, errorType, file, line, timestamp }`: clave = service+errorType+file+line. Si no ocurrió en los últimos `windowMinutes` → registra y devuelve `{ alert: true, count: 1 }`; si ya ocurrió en ventana → actualiza última aparición, incrementa contador y devuelve `{ alert: false, count: N }`.

**Ejercicio 2 - Enriquecimiento contextual.** Dada una alerta P1, verificar `workspace/runbooks/<service>.md`; si existe, extraer las **primeras dos líneas útiles** (excluyendo títulos `#`) e incrustarlas en `actionPlan`; si no, usar `"Sin guía local. Comunicar de inmediato al lead del servicio."`.

---

## Resumen

El tratamiento automatizado de errores transforma la avalancha de excepciones en un canal ordenado: **filtrado por severidad real**, **deduplicación por huellas canónicas** y **enriquecimiento con runbooks locales**. La próxima lección reutiliza este flujo para **abrir y asignar tickets de soporte** en plataformas externas.

**UP NEXT · Lección 15 de 30:** *Creación Rápida de Tickets de Soporte*. **Queda 1 lección** para cerrar el Módulo 3 (*Ingesta Dirigida por Eventos*).

---

## Preguntas abiertas del propio curso ("Can you answer these?")

1. ¿Cómo manejar la expiración de la ventana de deduplicación si un fallo se repite **ininterrumpidamente durante horas**?
2. ¿Qué impacto tiene no incluir el **entorno** (staging vs. producción) en la evaluación de severidad?
3. ¿Cómo confirma OpenClaw que un operador **ya tomó posesión** del incidente para cancelar el escalado telefónico?
4. ¿Qué precauciones de seguridad al extraer **fragmentos de stack traces** para que no se filtren contraseñas o tokens en los canales?

(Anotadas para profundizar. La #4 es crítica y real: las trazas suelen contener secretos.)

---

## Notas de verificación (Kanam)

**Núcleo de ingeniería: sólido y correcto** (estilo L08/L12). Lo metodológico aplica:

- ✅ **Fingerprint canónico** (`service + exception_class + source_location`) para deduplicar: patrón real y correcto.
- ✅ **PITFALL de hashear el mensaje crudo** (con IDs dinámicos/timestamps): correcto y crítico - rompe la dedup y multiplica alertas.
- ✅ **Ventana deslizante + umbral de consolidación**: correcto ("N eventos adicionales en 15m").
- ✅ **Severidad por impacto real** (usuarios afectados + entorno), no "todo 500 es crítico": criterio profesional.
- ✅ **Escalado idempotente + circuit breaker** con reintentos finitos: correcto y anti-saturación.
- ✅ **Enriquecimiento con runbook local** antes de notificar: buena práctica.
- ✅ **La pregunta #4** (no filtrar secretos en stack traces) es un riesgo real y bien puesto.
- ✅ Los **dos ejercicios corren tal cual** (Node estándar): verifiqué el 1 → `alert:true,count:1` / `false,2` / `false,3`; y el 2 → extrae 2 líneas útiles del runbook o el fallback.

**Inconsistencia interna detectada (mía, del material):**
- ⚠️ El **handler** usa `firstSeen` para la ventana (`now - existing.firstSeen < incidentWindowMs`), mientras el **Ejercicio 1** especifica la ventana desde la **última ocurrencia** (`lastSeen`). Son semánticas distintas: con `firstSeen`, la dedup se resetea 15 min después del primer evento aunque siga repitiéndose; con `lastSeen`, se extiende indefinidamente. El material **no aclara cuál es la canónica** (y su pregunta #1 apunta justo a ese caso de fallo ininterrumpido).

**Lo que NO coincide con la instalación real:**
- ❌ **`agentContext` con `channels.dispatch` / `workspaceRoot`**: no existe tal API de handler en OpenClaw. El hook real recibe el payload y **despierta un turno de agente**; no hay `res.json()` ni un objeto `agentContext.channels`. (Coherente con L11: el mecanismo real son `hooks.mappings`/transforms + turno de agente.)
- ❌ **`docs/runbooks/` no existe** en este workspace (ni la convención `workspace/runbooks/<service>.md`). Es una ruta inventada.
- ⚠️ **Escalado telefónico/SMS nativo:** OpenClaw **sí** tiene telefonía vía el **plugin `voice-call`** (y canales), pero **no** una "matriz de escalado P1/P2/P3" integrada. Lo real es que uno la construye combinando automations + webhooks salientes + el plugin de voz.
- ⚠️ **Taxonomía P1/P2/P3 y umbrales (50 usuarios, 45 min, 10 min):** plausibles y razonables, pero **inventados como valores del producto**; son parámetros de diseño, no defaults de OpenClaw.
- ⚠️ **Cache en memoria (`Map`)**: para dedup real, un `Map` local **falla en multi-réplica** (cada instancia dedup por su cuenta) - el mismo tipo de trampa que el PITFALL de estado local de la L05. El material no lo señala.

**Verificación ejecutable:**
- ✅ Node v26.8.1 con `node:crypto` disponible: `createHash('sha256')` funciona tal cual.
- ✅ Ejercicios 1 y 2 corren sin dependencias externas y producen el resultado prometido.

**Patrón (decimocuarto caso, consistente):** **buena ingeniería** (fingerprint canónico, dedup por ventana, severidad por impacto, escalation idempotente con circuit breaker, no filtrar secretos) montada sobre una **API/fachada inventada** (`agentContext.channels`, `docs/runbooks/`). El *qué* es correcto y valioso; el *cómo* se escribe contra `hooks.*` + automations + `message`, no contra ese handler ficticio. **Acierta el quiz** y el ejercicio corre; y, fiel al patrón del curso, su propia pregunta #1 expone el agujero de la ventana no aclarada.

**Nota de contexto (Módulo 3):** tras esta L14 el propio curso indica *"1 lesson left in Ingesta Dirigida por Eventos"* → Módulo 3 = 5 lecciones (L11-L15). Lección 15: *Creación Rápida de Tickets de Soporte*.
