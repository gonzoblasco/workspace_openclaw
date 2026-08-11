# SoporteML v3 - PRODUCT.md

> **Qué es:** definición completa del producto. Fuente de verdad para qué construimos y qué no.
> **Estado:** BORRADOR INICIAL (2026-08-11). Se refina a medida que definimos.
> **Relación con otros docs:** `BRIEF.md` (contexto de versiones), `ROADMAP.md` (cómo llegamos), `BACKEND-REFERENCE.md` (cómo funciona el backend actual), `DESIGN-TOKENS-LOVABLE.md` + `DESIGN-GUIDE.md` (cómo se ve).

---

## 1. Visión

**SoporteML** es un CRM multi-tenant para vendedores de Mercado Libre que centraliza la gestión de consultas de compradores, con asistencia de IA para responder rápido y bien.

**El problema que resuelve:** un vendedor de MeLi recibe decenas de consultas por día (precio, stock, envío, garantía, técnico). Responderlas a mano es lento, inconsistente y consume horas. SoporteML las centraliza, las categoriza, sugiere respuestas con IA y permite publicarlas de vuelta a MeLi en un clic.

**Para quién:** vendedores de Mercado Libre (individuales y equipos) que quieren gestionar sus consultas de forma profesional y escalable.

**Principio rector:** el sistema es **nuestro** — no depende de un vendor para existir. La primera alpha corre 100% local (SQLite + backend local). Supabase u otros servicios cloud son una opción futura solo si hay razones válidas, no el default.

---

## 2. Usuarios y roles

| Rol | Qué puede hacer | Límites |
|---|---|---|
| **agent** | Ver e interactuar con preguntas, clientes, productos, variantes y KB de su empresa. Responder y publicar respuestas a MeLi. | No toca settings, plantillas, tags, ni borra nada crítico. |
| **admin** | Todo lo del agent + settings de la empresa, plantillas, tags, conexión MeLi, invitaciones, billing, borrados, gestionar miembros. | Solo puede otorgar rol `agent` (no `admin`). |
| **super admin** | Acceso global: todas las empresas y usuarios, crear usuarios, otorgar rol `admin`, ver logs de MP y consultas de contacto, bypass de billing. | — |

**Multi-tenant:** un usuario puede pertenecer a varias empresas; `is_default` define la empresa activa. Todo el aislamiento se resuelve por membresía (`user_belongs_to_company`), nunca por confiar en el input del cliente.

---

## 3. Features core

### 3.0 El corazón: la bandeja de consultas

**SoporteML es, ante todo, una bandeja de consultas.** Todo lo demás (IA, KB, clientes, métricas) existe para servir a ese flujo de trabajo. El flujo del vendedor es:

```
Llega consulta de MeLi → se categoriza (IA) → se responde (IA o manual) → se publica a MeLi → se trackea SLA
```

Cada feature se evalúa contra esta pregunta: *¿ayuda al vendedor a responder consultas más rápido y mejor?* Si no, no es core.

### 3.1 Onboarding (primera vez)

El momento crítico donde el vendedor decide si el producto vale la pena. Si este flujo no es impecable, se va antes de ver el valor.

- Registro (email/password, o mock en alpha).
- **Conexión de la cuenta de MeLi (OAuth 2.0 + PKCE).**
- Primera sincronización: se traen productos y consultas existentes.
- El vendedor ve su bandeja poblada por primera vez.

### 3.2 Gestión de consultas
- Sincronización de preguntas de MeLi (webhook push en tiempo real + cron horario de respaldo).
- Bandeja central de consultas con estados (nueva, respondida, etc.) y categorías (precio, stock, tecnico, envio, garantia).
- Publicar respuesta de vuelta a MeLi en un clic.
- Blacklist de preguntas borradas definitivamente (`dismissed_meli_questions`).
- **Alcance:** las consultas incluyen preguntas de compradores y reclamos. Definir si los reclamos se manejan con el mismo flujo o uno distinto (ver preguntas abiertas).

### 3.3 IA (asistencia, no reemplazo)
- **Categorización automática** de preguntas (precio/stock/tecnico/envio/garantia).
- **Autopilot:** sugerencia de respuesta automática con IA.
- **Copiloto:** asistencia al redactar respuestas (tono, instrucciones custom).
- **Knowledge Base (RAG):** artículos + búsqueda semántica vectorial (embeddings) para responder con contexto de la empresa.
- **Resumen de hilos:** resumen de conversaciones largas por comprador/producto.

### 3.4 Productos y clientes
- Catálogo de productos sincronizado de MeLi (título, precio, permalink, categoría, descripción).
- Enriquecimiento de productos con IA.
- Detección de duplicados.
- CRM de compradores (`customers` + `customer_tags`).

#### Ficha proactiva de productos (feature central)

Cuando llega una consulta de un producto que aún no tiene ficha, el sistema **construye la ficha solo**, sin que el vendedor tenga que hacer nada. El flujo es:

```
Llega consulta de producto sin ficha
  → se crea la ficha automáticamente
  → scraping del post de MeLi se dispara SOLO (proactivo, sin botón)
  → la ficha se llena con la data publicada por el vendedor
  → IA llena los baches que el scraping no capturó (agregado)
  → la IA ya tiene contexto para generar la respuesta
  → el vendedor ve la respuesta lista (o casi), sin haber tocado nada
```

**Jerarquía de fuentes (la data publicada manda):**
1. Data publicada por el vendedor en el post de MeLi (scraping) = **fuente primaria**. Es lo más confiable y actualizado: es lo que el comprador está mirando en ese momento.
2. IA completa los baches que el scraping no pudo llenar.

**Por qué es central:** el sistema es **proactivo, no pasivo**. El vendedor no debería ir viendo si hay fichas nuevas ni clickear botones para que la IA pueda responder. La ficha se construye sola; el vendedor solo interviene si quiere corregir algo.

**Evolución desde v1:** en v1 el scraping era bajo demanda (botón en la ficha). En v3 es automático al crear la ficha. El llenado de baches con IA no existía en v1, es un agregado.

### 3.5 Métricas y operación
- Métricas de ventas y consultas.
- Alertas de vencimiento de SLA (email a `sla_alert_emails`).
- Notificaciones in-app (push del navegador en segundo plano).
- Logs operativos (`events`) y auditoría de entidades (`audit_logs`).

### 3.6 Billing (POST-MVP, no core)

Mercado Pago **nunca se probó** y es el mayor riesgo técnico. No es parte del core: un vendedor prueba el CRM por las consultas + IA, no por el sistema de suscripción.

- Suscripciones recurrentes vía Mercado Pago (preapproval).
- Crear / chequear / cancelar suscripción.
- Webhook IPN con HMAC.
- **En alpha: mockeado. No bloquea la validación del producto.**

---

## 4. Integraciones externas

| Integración | Estado | Uso |
|---|---|---|
| **Mercado Libre API** | ✅ **Funcional (probada)** | OAuth 2.0 + PKCE, sync de preguntas, publicar respuestas, catálogo de productos, clientes. |
| **IA (Lovable AI Gateway + OpenAI)** | Depende de API keys | Categorización, autopilot, copiloto, KB (embeddings), resúmenes. |
| **Mercado Pago** | ⚠️ **NUNCA probada** | Suscripciones recurrentes (preapproval) + webhook IPN. |
| **Email (Resend + Lovable Email)** | Depende de API keys | Alertas SLA (Resend), emails de auth (Lovable Email). |

**Regla:** en la alpha local, las integraciones no críticas se **mockean** (especialmente Mercado Pago, que nunca se probó). MeLi se integra real (es la referencia funcional).

---

## 5. Límites explícitos (qué NO es)

- **No sincroniza stock, envíos ni garantías como entidades propias.** Envíos/garantías existen solo como notas de texto en `products`. (Decisión de v1, se mantiene.)
- **No es un e-commerce** — no vende, no tiene carrito, no procesa pagos de compradores.
- **No es un ERP** — no gestiona inventario completo ni contabilidad.
- **No tiene storage buckets** (no aplica).
- **No usa Stripe** (eliminado del proyecto; billing es Mercado Pago).

---

## 6. Principios de arquitectura

1. **Independencia de vendor:** la lógica de negocio es nuestra. La primera alpha corre 100% local (SQLite + backend local). Supabase es opción futura solo con razones válidas.
2. **Capa de datos abstracta:** repositorios por entidad con implementación SQLite (alpha) y Postgres (prod futura). El cambio de DB es de implementación, no de arquitectura.
3. **Backend local primero:** las edge functions se recrean en un runtime local (a decidir: Deno / Node+Hono) y evolucionan desde ahí.
4. **Auth mock en alpha:** login de prueba con roles. El OAuth real de MeLi + auth real se integran después.
5. **Design system cerrado antes de código:** tokens de Lovable reconciliados contra v1 antes del scaffold.
6. **Multi-tenant por membresía, nunca por confianza en el input.**

---

## 7. Preguntas abiertas (para definir)

- [ ] ¿El autopilot publica respuestas automáticamente o siempre requiere aprobación humana? (seguridad/confianza)
- [ ] ¿Los reclamos se manejan con el mismo flujo que las preguntas o uno distinto? (alcance de la bandeja)
- [ ] ¿Qué métricas son las más valiosas para el vendedor? (para priorizar el dashboard)
- [ ] ¿El CRM de clientes necesita más que tags? (segmentación, historial)
- ~~¿Qué pasa con la KB cuando no hay artículos cargados?~~ → **RESUELTO:** ficha proactiva (ver 3.4). El producto se enriquece con scraping del post de MeLi (fuente primaria) + IA llena baches.
- [ ] ¿El onboarding necesita un modo demo (datos de ejemplo) para que el vendedor vea el valor antes de conectar MeLi? (reducción de fricción)
- [ ] Billing: confirmar que es post-MVP y no bloquea la alpha (MP nunca probado).
