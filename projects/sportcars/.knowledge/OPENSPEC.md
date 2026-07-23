# OpenSpec — Sport Cars Jeep (Reinvención Digital)

## Información del documento

- **Proyecto:** Sport Cars Jeep
- **Versión:** 1.0.0 — MVP
- **Fecha:** 2026-07-23
- **Estado:** Draft — Fase 0.2 de Product Discovery
- **Autor:** Gonzo + Kanam

## 1. Resumen

Reemplazo del sitio web estático `sportcarsjeep.com.ar` por una plataforma de generación de leads para concesionario oficial Jeep/Ram. El MVP incluye catálogo dinámico (alimentado por Mercado Libre), chatbot custom con RAG, captura de leads, y agendamiento de test drive. Integración con Pilot CRM se implementa en Post-MVP por restricción de acceso.

## 2. Alcance

### Incluido en MVP
- F1: Catálogo dinámico de vehículos
- F2: Chatbot de consultas con RAG
- F3: Captura de leads (Supabase, sync manual/export)
- F4: Integración Mercado Libre (inventario público)
- F5: Sucursales y contacto
- F6: Agendamiento de Test Drive
- F7: Cotizador de usados

### Excluido de MVP
- Integración automática con Pilot CRM (se hace manual/export en MVP)
- Panel administrativo completo
- WhatsApp Business API oficial (se usa click-to-chat)
- CMS (contenido hardcodeado)
- Simulador de financiación
- Comparador de modelos
- Blog / SEO local avanzado
- Reserva de turnos de postventa

## 3. Features detalladas

### F1 — Catálogo dinámico de vehículos

**Propósito:** Permitir a los visitantes explorar modelos Jeep/Ram e inventario real.

**Historias de usuario:**
- HU1.1: Como comprador, quiero ver todos los modelos disponibles para elegir uno.
- HU1.2: Como comprador, quiero ver el inventario real de usados con precio y fotos.
- HU1.3: Como comprador, quiero filtrar por tipo de vehículo y rango de precio.

**Criterios de aceptación:**
- Página `/vehiculos` con grid de modelos
- Página `/usados` con listings de MeLi cacheados
- Filtros funcionales en cliente
- Cada vehículo tiene página de detalle
- Si MeLi falla, mostrar mensaje de "consultar stock" y CTA a WhatsApp

**Dependencias:** Mercado Libre Search API pública.

### F2 — Chatbot de consultas con RAG

**Propósito:** Responder preguntas frecuentes 24/7 y capturar leads calificados.

**Historias de usuario:**
- HU2.1: Como comprador, quiero hacer preguntas sobre modelos sin llamar.
- HU2.2: Como comprador, quiero que el bot me derive a un vendedor si no resuelve.
- HU2.3: Como vendedor, quiero recibir los datos del interesado sin tener que preguntar todo de nuevo.

**Criterios de aceptación:**
- Widget flotante en todas las páginas
- El bot saluda y ofrece opciones rápidas (modelos, precios, test drive, usados)
- Usa RAG sobre knowledge base para responder
- Captura nombre y teléfono antes de derivar
- Derivación a WhatsApp del vendedor con mensaje pre-cargado
- Persiste conversación en Supabase

**Dependencias:** LLM API, embeddings, Supabase.

### F3 — Captura de leads

**Propósito:** Convertir visitantes en contactos accionables para el concesionario.

**Historias de usuario:**
- HU3.1: Como comprador, quiero dejar mis datos para que me contacten.
- HU3.2: Como vendedor, quiero ver los leads organizados por interés.

**Criterios de aceptación:**
- Formularios validados con Zod
- Lead guardado en Supabase con source y metadata
- Notificación por email/WhatsApp al vendedor (Webhook/IFTT/Zapier o mensaje manual)
- Panel simple `/admin/leads` para ver leads (protegido por password simple en MVP)

**Dependencias:** Supabase, servicio de notificación.

### F4 — Integración Mercado Libre

**Propósito:** Mostrar inventario real sin duplicar data entry.

**Historias de usuario:**
- HU4.1: Como comprador, quiero ver autos reales con precio y fotos.
- HU4.2: Como comprador, quiero clickear un auto y consultar por él.

**Criterios de acción:**
- Sync periódico (cada 30 min) desde `/sites/MLA/search?nickname=sportcarsjeep`
- Cache en Supabase tabla `vehicles`
- Detalle de cada auto con galería, specs y precio
- CTA "Consultar por este auto" que abre formulario/chat con `meli_item_id`

**Dependencias:** MeLi Search API.

### F5 — Sucursales y contacto

**Propósito:** Facilitar el contacto directo según ubicación.

**Historias de usuario:**
- HU5.1: Como comprador, quiero saber dónde queda cada sucursal y sus horarios.
- HU5.2: Como comprador, quiero llamar o escribir a la sucursal más cercana.

**Criterios de aceptación:**
- Página `/sucursales` con 3 ubicaciones
- Mapa embebido de Google Maps por sucursal
- Click-to-call y click-to-WhatsApp
- Horarios de showroom y taller

**Dependencias:** Ninguna (hardcode inicial).

### F6 — Agendamiento de Test Drive

**Propósito:** Permitir reservar una prueba de manejo sin fricción.

**Historias de usuario:**
- HU6.1: Como comprador, quiero elegir modelo, sucursal y fecha para un test drive.
- HU6.2: Como vendedor, quiero recibir el pedido de test drive con datos completos.

**Criterios de aceptación:**
- Formulario en `/test-drive` y modal desde catálogo
- Campos: nombre, teléfono, email, modelo, sucursal, fecha/hora preferida
- Lead guardado con `source: form_test_drive`
- Confirmación visual + mensaje por WhatsApp al vendedor

**Dependencias:** Supabase, WhatsApp click-to-chat.

### F7 — Cotizador de usados

**Propósito:** Capturar interesados en vender su auto al concesionario.

**Historias de usuario:**
- HU7.1: Como dueño de un usado, quiero saber cuánto me pueden dar por mi auto.
- HU7.2: Como vendedor, quiero recibir la info del usado para evaluarlo.

**Criterios de aceptación:**
- Formulario con marca, modelo, año, km, versión, estado aproximado
- Lead guardado con `interest_type: used_quote`
- No da precio automático (el concesionario evalúa)

**Dependencias:** Supabase.

## 4. Requisitos no funcionales

### Performance
- Time to First Byte (TTFB) < 600ms
- Largest Contentful Paint (LCP) < 2.5s en 4G
- Interacción del chatbot < 2s de respuesta promedio

### SEO
- URLs semánticas: `/vehiculos`, `/usados`, `/sucursales`, `/test-drive`
- Meta tags dinámicas por página
- Sitemap XML
- Structured data (Vehicle, LocalBusiness, FAQ)

### Accesibilidad
- WCAG 2.1 AA mínimo
- Chatbot accesible por teclado
- Formularios con labels y errores claros

### Seguridad
- No exponer secrets al cliente
- Validación de inputs con Zod
- Rate limiting en endpoints públicos
- RLS en Supabase

### Disponibilidad
- Target: 99.5% uptime (Vercel + Supabase)

## 5. Interfaz de usuario (boceto funcional)

### Navegación principal
- Logo Sport Cars
- Vehículos 0km
- Usados
- Sucursales
- Test Drive
- Contacto
- Botón "Hablar con asesor" → WhatsApp

### Home
- Hero con slogan y CTA principal
- Modelos destacados (6 de Jeep + Ram)
- Inventario de usados (últimos 6)
- Sucursales preview
- Chatbot widget flotante

### Página de vehículo 0km
- Galería de imágenes oficiales
- Specs destacadas
- Precio referencial / "Consultar precio"
- CTA: Test drive / Cotizar / Hablar con asesor

### Página de usado
- Fotos de MeLi
- Precio real
- Atributos (año, km, color, transmisión)
- CTA: Consultar por este auto

## 6. Integraciones técnicas

### Mercado Libre
```
GET https://api.mercadolibre.com/sites/MLA/search?nickname=sportcarsjeep
GET https://api.mercadolibre.com/items/{item_id}
GET https://api.mercadolibre.com/users/{seller_id}
```

### LLM para chatbot
```
POST /api/chat  
Body: { messages: [...] }
Response: Streaming text (Vercel AI SDK)
```

### Leads
```
POST /api/leads
Body: { name, phone, email, source, ... }
Response: { success: true, lead_id }
```

### Pilot CRM (Post-MVP)
```
POST https://<dominio_pilot>/pilot/leadcreation/webhook
Headers: Pilot auth token
Body: { id, otros_datos }
```

## 7. Modelo de datos

Ver `DATA_MODEL.md` para el esquema completo.

## 8. Métricas

Ver `DEFINITION.md` sección Métricas de éxito.

## 9. Lanzamiento

### MVP v1.0.0
- Home + catálogo 0km + usados + sucursales + test drive + cotizador + chatbot + captura leads
- Sin sync automático a Pilot
- Sin CMS

### v1.1.0
- Sync automático de leads a Pilot CRM (cuando haya credenciales)
- Panel admin de leads mejorado
- Notificaciones automáticas a vendedores

### v1.2.0
- Simulador de financiación
- WhatsApp Business API
- SEO local por sucursal

## 10. Glosario

- **MeLi:** Mercado Libre
- **Pilot:** Pilot CRM / Pilot Solution
- **RAG:** Retrieval-Augmented Generation
- **Lead:** Potencial cliente que deja datos de contacto
- **CTA:** Call to Action
- **TTFB / LCP / CLS:** Métricas de performance web

## 11. Decisiones pendientes

- Proveedor de LLM final (OpenAI vs DeepSeek vs Anthropic)
- Si usar Payload CMS o Sanity en v1.1
- Mecanismo de notificación de leads (email, WhatsApp webhook, o manual)