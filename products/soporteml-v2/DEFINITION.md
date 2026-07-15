# Product Definition: SoporteML v2

**Fecha:** 2026-07-15
**Fase:** 2 — Definition

---

## Core value

Un vendedor de Mercado Libre puede gestionar todas sus preguntas y mensajes en un solo lugar, con un copiloto de IA que le sugiere respuestas basadas en el conocimiento de su producto, y cobrar una suscripción mensual con el mismo Mercado Pago que ya usa.

---

## MVP Scope

### In scope (MVP)

1. **Auth multi-tenant con Supabase** — registro, login, empresas aisladas, roles (admin/operador), sin Lovable Cloud. Reemplaza `@lovable.dev/cloud-auth-js` para siempre.
2. **Integración Mercado Libre (OAuth + Sync + Auto-learn)** — conectar cuenta MeLi via OAuth, sincronizar preguntas y mensajes via API + webhooks, realtime en el inbox. **Al conectar por primera vez, el sistema hace un fetch inicial de publicaciones + preguntas históricas + respuestas pasadas para construir automáticamente la ficha de cada producto y pre-poblar la KB.** El vendedor no arranca de cero — el sistema aprende de su historia en MeLi. Sin esto no hay producto.
3. **Inbox centralizado** — bandeja de preguntas agrupadas por hilo (comprador + producto), filtros por estado (Pendientes, Por vencer, Publicadas, Auto IA, Archivadas), búsqueda, SLA tracking, navegación teclado, Supabase Realtime.
4. **AI Copilot con RAG** — copiloto que genera borradores de respuesta usando contexto CRM + KB de la empresa (pgvector), tono configurable, instrucciones custom del vendedor, sugerencias CRM, manejo de errores, modo autopilot opcional. Devuelve JSON estructurado (summary, draft, missing_data, kb_sources).
5. **Knowledge Base (auto-poblada + manual)** — al conectar MeLi, el sistema genera KB inicial desde el historial: extrae patrones de preguntas frecuentes, respuestas que funcionaron, info de publicaciones (título, descripción, atributos, policies de envío). El vendedor puede editar/ampliar manualmente después. Embedding automático con OpenAI `text-embedding-3-small`, búsqueda semántica via `match_kb_chunks` (umbral 0.45, top 5). Cada empresa tiene su KB aislada.
6. **Billing Mercado Pago (operativo real)** — suscripción mensual via MP Preapproval. Crear, verificar, pausar, webhook IPN con validación HMAC. Plan de preapproval creado en MP desde el inicio. Secrets configurados. Esto es **la diferencia #1 con v1**.
7. **Settings consolidado** — gestión de empresa, operadores, tono del copiloto, instrucciones custom, conexión MeLi, plan/billing, danger zone.
8. **Resumen IA de hilos** — resumen auto-generado para hilos con 2+ preguntas, cacheado por hash, regeneración automática cuando llegan nuevas preguntas.
9. **Analytics básico** — métricas de volumen de preguntas, tiempos de respuesta, tasa de resolución. No un dashboard complejo, pero sí visibilidad.
10. **Auto-respuesta inteligente (opt-in)** — la IA clasifica cada pregunta entrante como rutinaria o compleja. Las rutinarias (ej: "¿hacen envíos a X?", "¿qué medidas tiene?") se auto-responden usando la KB + contexto CRM, sin intervención humana. Las complejas o sensibles se elevan al inbox para que el vendedor las maneje. **Totalmente optativo:** el vendedor activa/desactiva la feature desde Settings, y puede configurar criterios de clasificación (qué tipos de preguntas se auto-responden, cuáles no). Todo auto-respondido queda visible en el inbox con badge "Auto IA" para auditoría y revertir si hace falta.

### Out of scope (post-MVP)

- **Multi-marketplace** (Mercado Libre only para MVP, otros marketplaces después)
- **Notificaciones WhatsApp** (sueño de v1, pero no esencial para reemplazo)
- **Templates con variables dinámicas** (mejora de productividad, no core value)
- **App móvil** (web responsive primero)
- **Integración con KanamAI** (v2 usa OpenAI directo, enrutamiento de modelos viene después)
- **Import de datos históricos de v1** (los 3 clientes empiezan limpio o se hace migración manual puntual)

### Explicit non-goals

- **No reutilizar código de v1** — se aprende de los specs, se reescribe todo
- **No usar Lovable Cloud** — ni auth, ni deploy, ni secrets. Cero dependencia
- **No Next.js** — React + Vite para compatibilidad potencial con Lovable como deploy futuro (sin casarse)
- **No auto-respuesta a ciegas** — la auto-respuesta es opt-in, clasifica antes de responder, y todo queda visible para auditoría. El vendedor puede revertir cualquier auto-respuesta.

---

## User personas

### Persona 1: "El Vendedor" (Marcela, 38)

**Quién es:** Vendedora de Mercado Libre con 200+ publicaciones, 50-100 preguntas/día. Vende electrónica. Ya tiene operación seria, no es hobbyista.

**Qué necesita:** No perder ventas por responder tarde. Tener contexto de cada comprador. Respuestas consistentes (no depende de qué ánimo esté). Saber qué preguntas son urgentes.

**Qué hace con el producto:** Abre el inbox por la mañana, ve las urgentes primero, usa el copiloto para sugerir respuestas, edita rápido, envía. Carga su KB (policies de envío, FAQ de cada producto) una vez y el copiloto las usa siempre.

**Success:** Tiempo de respuesta promedio baja de 2h a 30min. Ya no pierde ventas por demora. Las respuestas son consistentes.

### Persona 2: "El Admin del Equipo" (Diego, 45)

**Quién es:** Maneja una empresa con 3-5 operadores respondiendo en MeLi. Necesita visibilidad, control, y que la KB de la empresa esté centralizada.

**Qué necesita:** Que todos los operadores respondan con el mismo tono y la misma info. Ver métricas. Asignar roles. Gestionar la suscripción.

**Qué hace con el producto:** Configura la KB de la empresa, setea el tono del copiloto, invita operadores, monitorea métricas en Analytics, gestiona billing en Settings.

**Success:** Todos los operadores responden consistente. Tiene visibilidad del volumen y tiempos. La suscripción se cobra sola cada mes.

---

## User flows

### Flow 1: Onboarding inicial
- **Trigger:** vendedor se registra
- **Steps:** registro → crear empresa → conectar cuenta MeLi (OAuth) → **sistema hace fetch inicial: descarga publicaciones activas + preguntas históricas + respuestas pasadas** → **genera KB automática: extrae patrones, FAQ frecuentes, info de productos, policies** → **genera fichas de producto: support_summary, key_points, shipping_notes por cada publicación** → elegir plan (billing MP) → land en inbox con datos ya cargados
- **Outcome:** cuenta activa, MeLi conectada, KB pre-poblada, fichas de producto generadas, suscripción activa, inbox mostrando preguntas
- **Errores:** OAuth MeLi falla → mensaje claro + retry; MP rechaza → mensaje + plan alternativo; sin KB inicial → el copiloto funciona sin RAG (se completa manualmente después); fetch inicial lento → loading state claro con progreso ("Aprendiendo de tus publicaciones...")

### Flow 2: Responder una pregunta con el copiloto
- **Trigger:** vendedor abre una pregunta en el inbox
- **Steps:** selecciona pregunta → copiloto genera borrador (con KB + contexto CRM) → vendedor edita → envía → pregunta pasa a "Publicada"
- **Outcome:** respuesta enviada a MeLi, estado actualizado, SLA detenido
- **Errores:** API MeLi falla al enviar → mensaje + retry; copiloto sin API key → respuesta manual sin IA; sin KB relevante → copiloto responde con contexto CRM solo

### Flow 3: Gestión de hilos con resumen IA
- **Trigger:** vendedor abre un hilo con 2+ preguntas
- **Steps:** abre hilo → resumen IA se genera (o carga de cache) → ve temas, intención del comprador, pendientes → decide acción
- **Outcome:** contexto rápido sin leer todas las preguntas
- **Errores:** LLM no disponible → sin resumen, no bloquea el flujo; hilo de 1 pregunta → no se muestra resumen

### Flow 4: Gestionar KB de la empresa
- **Trigger:** admin va a Settings → Knowledge Base
- **Steps:** ve KB auto-generada (marcada como "Auto") → puede editar artículos auto-generados → puede crear artículos nuevos → texto se splitea en chunks → embedding automático → guardado en pgvector → disponible para copiloto
- **Outcome:** KB enriquecida, copiloto responde mejor, auto-mejora con cada nueva pregunta
- **Errores:** texto muy corto → warning; sin API key → no se puede embedear, mensaje claro; artículo auto-generado editable sin restricciones

### Flow 5: Gestionar billing
- **Trigger:** admin va a Settings → Plan
- **Steps:** ve plan actual → upgrade/downgrade → MP redirige a checkout → webhook IPN confirma → estado de billing actualizado
- **Outcome:** suscripción activa o actualizada
- **Errores:** webhook no llega → polling de verificación como fallback; MP rechaza → mensaje + retry

### Flow 6: Sincronización continua con MeLi
- **Trigger:** webhook de MeLi (nueva pregunta, mensaje, cambio de estado)
- **Steps:** MeLi envía webhook → Edge Function procesa → guarda en Supabase → Realtime actualiza inbox → vendedor ve la pregunta nueva sin refresh
- **Outcome:** inbox siempre actualizado
- **Errores:** webhook perdido → polling periódico como fallback; rate limit MeLi → backoff exponencial

### Flow 7: Auto-respuesta inteligente (opt-in)
- **Trigger:** llega una pregunta nueva y la auto-respuesta está activada en Settings
- **Steps:** la IA clasifica la pregunta (rutinaria vs compleja) → si es rutinaria y matchea criterios configurados → genera respuesta con KB + contexto CRM → envía a MeLi automáticamente → marca en inbox con badge "Auto IA" → notifica al vendedor → si es compleja → queda en inbox como pendiente normal
- **Outcome:** pregunta rutinaria respondida al instante, vendedor solo ve las que importan
- **Errores:** IA no confidente (score < umbral) → no auto-responde, queda pendiente; API MeLi falla al enviar → reintenta 3x, si no pasa queda pendiente para humano; feature desactivada → todo funciona como Flow 2 normal

---

## Success metrics

| Métrica | Target MVP | Cómo se mide |
|---|---|---|
| **Clientes activos** | 3 (heredados de v1) + 1 nuevo | Count de empresas con billing_status=active |
| **Tiempo de respuesta promedio** | < 30 min (vs 2h en v1) | Delta entre received_at y answered_at en questions |
| **Preguntas respondidas con copiloto** | > 70% | Count de preguntas con ai_assisted=true / total |
| **Billing operativo** | 100% de clientes pagando | billing_status=active para todos |
| **Preguntas auto-respondidas** | 40-60% de las rutinarias | Count de preguntas con auto_answered=true / total rutinarias detectadas |
| **NPS implícito** | Los 3 Beta migran y se quedan | Retención a 30 días post-migración |

---

## Notas

- El MVP es **completo por decisión** — Gonzo quiere todas las features necesarias, no un recorte. Billing es prioridad.
- Los 4 specs as-built de v1 son la base de los requirements de v2. Se reescriben, no se copian.
- El stack es React+Vite (no Next.js) para mantener compatibilidad potencial con Lovable como deploy futuro, sin casarse.
- create-stack-next provee la estructura metodológica (OpenSpec, ADRs, HANDOFF, CHANGELOG) pero el scaffold técnico se adapta a React+Vite.