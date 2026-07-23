# DATA MODEL — Sport Cars Jeep

## Nota de alcance

Modelo de datos para el MVP. Diseñado para ser simple pero extensible. Algunas tablas son para funcionalidad post-MVP (marcadas como `[Post-MVP]`).

---

## 1. `leads`

Contactos capturados desde el sitio web. Es la tabla más crítica para el negocio.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | uuid PK | Identificador único |
| `created_at` | timestamptz | Fecha de creación |
| `updated_at` | timestamptz | Última modificación |
| `source` | text | Origen: `chatbot`, `form_contact`, `form_test_drive`, `form_used_quote`, `meli_card`, `page_contact` |
| `status` | text | Estado: `new`, `contacted`, `qualified`, `converted`, `discarded` |
| `name` | text | Nombre del interesado |
| `phone` | text | Teléfono (obligatorio) |
| `email` | text nullable | Email |
| `preferred_branch` | text nullable | Sucursal preferida: `quilmes`, `la_plata`, `belgrano` |
| `interest_type` | text nullable | `0km`, `usado`, `plan_ahorro`, `postventa`, `test_drive` |
| `vehicle_model` | text nullable | Modelo de interés: `compass`, `renegade`, etc. |
| `vehicle_year` | int nullable | Año del usado (si aplica) |
| `budget_range` | text nullable | Rango de presupuesto (ej. "5-8M ARS") |
| `has_trade_in` | boolean nullable | ¿Tiene auto para entregar? |
| `trade_in_details` | text nullable | Detalle del usado a entregar |
| `message` | text nullable | Mensaje libre del usuario |
| `conversation_id` | uuid nullable FK → `conversations.id` | Si el lead vino del chatbot |
| `meli_item_id` | text nullable | Si consultó un vehículo específico de MeLi |
| `pilot_sync_status` | text | `pending`, `synced`, `failed`, `not_applicable` |
| `pilot_sync_attempts` | int | Contador de intentos de sync |
| `pilot_last_error` | text nullable | Último error si falló sync |

**Indexes:**
- `created_at DESC` (para panel de vendedores)
- `status` (filtrado por estado)
- `phone` (evitar duplicados)
- `pilot_sync_status` (para el sync worker)

---

## 2. `conversations`

Historial de conversaciones del chatbot.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | uuid PK | Identificador único |
| `created_at` | timestamptz | Inicio de conversación |
| `updated_at` | timestamptz | Último mensaje |
| `session_id` | text | ID anónimo de sesión (cookie/localStorage) |
| `status` | text | `active`, `handoff_requested`, `completed`, `abandoned` |
| `source_page` | text | Página donde inició el chat |
| `user_phone` | text nullable | Teléfono capturado durante la conversación |
| `user_email` | text nullable | Email capturado |
| `summary` | text nullable | Resumen generado por LLM de la intención |
| `lead_id` | uuid nullable FK → `leads.id` | Lead generado a partir de esta conversación |
| `handoff_reason` | text nullable | Por qué se derivó a humano |
| `metadata` | jsonb | Datos extra: modelo de interés, sucursal, etc. |

**Indexes:**
- `session_id`
- `created_at DESC`
- `status`

---

## 3. `messages`

Mensajes individuales dentro de una conversación.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | uuid PK | Identificador único |
| `conversation_id` | uuid FK → `conversations.id` | Conversación padre |
| `created_at` | timestamptz | Timestamp |
| `role` | text | `user`, `assistant`, `system`, `tool` |
| `content` | text | Contenido del mensaje |
| `model` | text nullable | Modelo de LLM usado |
| `tokens_input` | int nullable | Tokens de entrada (para cost tracking) |
| `tokens_output` | int nullable | Tokens de salida |
| `latency_ms` | int nullable | Tiempo de respuesta |

**Indexes:**
- `(conversation_id, created_at)`

---

## 4. `knowledge_chunks`

Base de conocimiento para RAG del chatbot. Cargada manualmente al inicio, actualizable por panel admin.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | uuid PK | Identificador único |
| `created_at` | timestamptz | Fecha de creación |
| `updated_at` | timestamptz | Última modificación |
| `source` | text | Origen: `model_specs`, `pricing`, `financing`, `branch_info`, `faq`, `promotions`, `policy` |
| `title` | text | Título del chunk |
| `content` | text | Contenido semántico |
| `embedding` | vector(1536) | Embedding del contenido (OpenAI text-embedding-3-small o similar) |
| `metadata` | jsonb | Tags, modelo asociado, sucursal, etc. |
| `is_active` | boolean | ¿Visible para el chatbot? |
| `priority` | int | Orden de prioridad para retrieval |

**Indexes:**
- HNSW en `embedding` para búsqueda por similitud
- `source` (filtrado por tipo)
- `is_active`

---

## 5. `vehicles`

Cache local del inventario de Mercado Libre. Se refresca periódicamente.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | text PK | MeLi item ID (ej. `MLA1234567890`) |
| `created_at` | timestamptz | Fecha de primer importación |
| `updated_at` | timestamptz | Última actualización desde MeLi |
| `title` | text | Título de la publicación |
| `price` | numeric | Precio en ARS |
| `currency_id` | text | `ARS` |
| `condition` | text | `new`, `used` |
| `category_id` | text | Categoría MeLi |
| `seller_id` | int | ID del vendedor en MeLi |
| `permalink` | text | Link original en MeLi |
| `thumbnail` | text | URL de imagen principal |
| `pictures` | jsonb | Array de URLs de imágenes |
| `attributes` | jsonb | Atributos de MeLi (brand, model, year, km, color, etc.) |
| `status` | text | `active`, `paused`, `closed`, `not_found` |
| `last_synced_at` | timestamptz | Última sincronización |

**Indexes:**
- `status`
- `condition`
- `price`
- `updated_at`

---

## 6. `events`

Eventos de analytics para medir conversión y engagement.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | uuid PK | Identificador único |
| `created_at` | timestamptz | Timestamp |
| `session_id` | text | Sesión anónima |
| `event_type` | text | `page_view`, `click`, `form_start`, `form_submit`, `chat_open`, `chat_message`, `lead_created`, `vehicle_view`, `whatsapp_click` |
| `page_path` | text nullable | Ruta de la página |
| `payload` | jsonb | Datos del evento |

**Indexes:**
- `created_at DESC`
- `event_type`
- `session_id`

---

## 7. `branches` [Post-MVP o hardcode]

Sucursales del concesionario. Probablemente se hardcodeen en JSON inicial por ser pocas.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | text PK | `quilmes`, `la_plata`, `belgrano` |
| `name` | text | Nombre de sucursal |
| `address` | text | Dirección |
| `city` | text | Ciudad |
| `phone` | text | Teléfono |
| `whatsapp` | text | WhatsApp de ventas |
| `postventa_whatsapp` | text nullable | WhatsApp de postventa |
| `sales_hours` | text | Horario showroom |
| `service_hours` | text nullable | Horario taller |
| `map_url` | text nullable | Link Google Maps |
| `is_active` | boolean | ¿Activa? |

---

## 8. `model_specs` [Post-MVP o hardcode]

Especificaciones de modelos Jeep/Ram. Inicialmente JSON; si crece, se migra a tabla.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | text PK | `jeep_compass`, `jeep_renegade`, etc. |
| `brand` | text | `Jeep`, `Ram` |
| `model` | text | Nombre comercial |
| `category` | text | `SUV`, `pickup`, etc. |
| `starting_price` | numeric nullable | Precio referencial desde |
| `description` | text | Descripción comercial |
| `specs` | jsonb | Motor, transmisión, equipamiento, etc. |
| `gallery` | jsonb | URLs de imágenes oficiales |
| `is_active` | boolean | ¿Mostrar en catálogo? |

---

## 9. `pilot_sync_log` [Post-MVP]

Log de sincronización de leads hacia Pilot CRM.

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | uuid PK | Identificador |
| `created_at` | timestamptz | Timestamp |
| `lead_id` | uuid FK → `leads.id` | Lead sincronizado |
| `status` | text | `success`, `failed` |
| `request_payload` | jsonb | Payload enviado |
| `response_status` | int nullable | HTTP status |
| `response_body` | jsonb nullable | Respuesta de Pilot |
| `error_message` | text nullable | Mensaje de error |

---

## Relaciones

```
conversations ||--o{ messages : tiene
conversations ||--o| leads : genera
leads }o--|| meli_items (vehicles) : consulta
leads ||--o{ pilot_sync_log : intenta sync
vehicles }o--|| sellers (implícito en MeLi) : publicado por
knowledge_chunks }|--|| embeddings : usa
```

## Políticas RLS (Supabase)

- `leads`: solo lectura/escritura desde service role (Next.js server). Sin acceso público directo.
- `conversations`, `messages`: acceso por `session_id` para el frontend anónimo; service role para admin.
- `knowledge_chunks`: solo service role.
- `vehicles`: lectura pública; escritura solo service role.
- `events`: inserción anónima permitida; lectura service role.

## Convenciones

- Todas las tablas tienen `created_at` y `updated_at`.
- JSONB para campos dinámicos/atributos externos.
- Textos enum usan `check` constraints o aplicación-level validation con Zod.
- UUIDv7 preferido para IDs temporales (opcional).