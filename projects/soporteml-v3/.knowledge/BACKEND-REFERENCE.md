# SoporteML — Referencia técnica del backend

> Documento generado a partir del estado **real** de la base de datos y del código de las Edge Functions.
> Base URL de funciones: `https://<PROJECT_REF>.supabase.co/functions/v1/<nombre-función>`
> Todas las funciones aceptan `OPTIONS` (CORS `*`) y responden JSON.

---

## 1. Base de datos (PostgreSQL / Supabase)

### 1.1 Extensiones requeridas
`pgcrypto` (gen_random_uuid, gen_random_bytes), `vector` (pgvector, en schema `extensions`), `pg_trgm`, `pg_cron`, `pg_net`, `supabase_vault`.

### 1.2 Tipos custom (enums)

| Enum | Valores | Uso real |
|---|---|---|
| `app_role` | `agent`, `admin` | `memberships.role`, `user_roles.role` |
| `question_category` | `Precio`, `Stock`, `Técnico`, `Envío`, `Garantía` | legacy — hoy `questions.ai_category` es `text` |
| `question_status` | `pending`, `answered`, `discarded` | legacy — hoy `questions.status` es `text` validado por trigger |

Estados válidos por trigger (no por CHECK):
- `questions.status`: `pending`, `published`, `archived`, `error`, `deleted`, `queued_auto`, `auto_published`, `needs_human`
- `products.status`: `active`, `archived`
- `memberships.status`: `active`, `invited`, `disabled`

### 1.3 Tablas

Convención: todas las tablas de negocio llevan `company_id uuid NOT NULL REFERENCES companies(id) ON DELETE CASCADE` y RLS por pertenencia (`user_belongs_to_company`).

#### companies
| Columna | Tipo | Notas |
|---|---|---|
| id | uuid PK | default `gen_random_uuid()` |
| name | text NOT NULL | |
| created_at | timestamptz NOT NULL | default `now()` |
| mp_preapproval_id | text | ID de suscripción Mercado Pago |
| billing_status | text NOT NULL | default `'free'` — free/pending/active/paused/cancelled |
| plan | text NOT NULL | default `'free'` — free/base |
| billing_period_end | timestamptz | |
| deleted_at | timestamptz | soft delete; índice parcial `WHERE deleted_at IS NULL` |

#### profiles
`id uuid PK → auth.users(id) ON DELETE CASCADE`, `company_id uuid → companies(id)` *(deprecado, usar memberships)*, `full_name text`, `created_at timestamptz NOT NULL default now()`.

#### memberships (fuente de verdad multi-tenant)
`id uuid PK`, `user_id uuid NOT NULL → auth.users(id) CASCADE`, `company_id uuid NOT NULL → companies(id) CASCADE`, `role app_role NOT NULL default 'agent'`, `status text NOT NULL default 'active'`, `is_default bool NOT NULL default false`, `created_at`, `updated_at`.
- UNIQUE `(user_id, company_id)`
- UNIQUE parcial `idx_memberships_one_default_per_user (user_id) WHERE is_default`

#### user_roles (roles globales legacy)
`id uuid PK`, `user_id uuid NOT NULL → auth.users(id) CASCADE`, `role app_role NOT NULL default 'agent'`. UNIQUE `(user_id, role)`.

#### super_admins
`user_id uuid PK → auth.users(id) CASCADE`, `created_at timestamptz NOT NULL`.

#### company_invites
`company_id uuid PK → companies(id) CASCADE`, `invite_code text NOT NULL default encode(gen_random_bytes(6),'hex')`, `created_at`, `updated_at`.

#### company_settings
`company_id uuid PK → companies(id) CASCADE` + configuración:
`ai_tone text NOT NULL default 'profesional'`, `ai_custom_instructions text`, `auto_reply_enabled bool default false`, `auto_reply_categories jsonb default '[]'`, `auto_reply_exclusion_rules text`, `auto_reply_mode text default 'off'`, `business_hours jsonb default '{"days":[...],"start_time":"09:00","end_time":"18:00"}'`, `sync_interval_minutes int default 15`, `last_synced_at timestamptz`, `features_ai_suggestions bool default true`, `features_autopilot_in_hours bool default false`, `features_autopilot_after_hours bool default false`, `autopilot_confidence_threshold numeric default 0.85`, `kb_top_k int default 5`, `kb_similarity_threshold numeric default 0.45`, `sla_target_minutes int default 60` (CHECK 5–1440), `sla_escalation_enabled bool default true`, `sla_alert_emails text[] default '{}'`, `created_at`, `updated_at`.

#### products
`id uuid PK`, `company_id uuid NOT NULL → companies CASCADE`, `meli_item_id text`, `title text NOT NULL`, `price numeric`, `permalink text`, `meli_category_id text`, `meli_category_name text`, `sku text`, `status text NOT NULL default 'active'`, `source text NOT NULL default 'meli'`, `external_id text`, `external_url text`, `support_summary text`, `key_points jsonb default '[]'`, `shipping_notes text`, `returns_notes text`, `warranty_notes text`, `faq_bullets jsonb default '[]'`, `do_not_say jsonb default '[]'`, `meli_cache jsonb`, `meli_cache_fetched_at timestamptz`, `updated_by uuid`, `created_at`, `updated_at`.
- UNIQUE `(company_id, meli_item_id)`; UNIQUE parcial `(company_id, source, external_id) WHERE external_id IS NOT NULL`
- Índices: GIN trigram sobre `title`, btree parciales por `sku`, `meli_item_id`, `external_id`

#### product_variants
`id uuid PK`, `company_id uuid NOT NULL → companies`, `product_id uuid NOT NULL → products CASCADE`, `variant_name text NOT NULL`, `variant_sku text`, `attributes jsonb default '{}'`, `support_notes text`, `archived_at timestamptz`, `updated_by uuid`, `created_at`, `updated_at`.

#### questions (tabla central)
`id uuid PK`, `company_id uuid NOT NULL → companies CASCADE`, `product_id uuid → products CASCADE`, `meli_question_id text NOT NULL UNIQUE`, `buyer_id text`, `buyer_nickname text`, `product_meli_id text`, `question_text text NOT NULL`, `status text NOT NULL default 'pending'`, `ai_suggested_answer text`, `ai_category text`, `ai_confidence numeric`, `ai_decision_reason text`, `auto_action text default 'none'`, `answered_by_ai bool default false`, `final_answer text`, `answered_by uuid → profiles(id)`, `requires_human bool NOT NULL default false`, `requires_human_reason text`, `meli_status text`, `meli_permalink text`, `sla_alert_sent_at timestamptz`, `created_at`, `answered_at`.
- Índices: `(product_meli_id)`; parcial SLA `(company_id, created_at) WHERE status='pending' AND answered_at IS NULL AND sla_alert_sent_at IS NULL`

#### customers / customer_tags (CRM de compradores)
- `customers`: `id uuid PK`, `company_id → companies CASCADE`, `buyer_id text NOT NULL`, `buyer_nickname text`, `notes text`, `tags text[] default '{}'`, `total_questions int default 0`, `last_interaction_at timestamptz`, `created_at`, `updated_at`. UNIQUE `(company_id, buyer_id)`.
- `customer_tags`: `id uuid PK`, `company_id → companies CASCADE`, `name text NOT NULL`, `color text default '#888888'`, `created_at`. UNIQUE `(company_id, name)`.

#### kb_articles / kb_chunks (Knowledge Base vectorial)
- `kb_articles`: `id uuid PK`, `company_id → companies CASCADE`, `title text` (CHECK 1–200), `source_type text default 'text'` (CHECK `text|markdown`), `raw_content text` (CHECK 1–50000), `status text default 'pending'` (CHECK `pending|processing|ready|error`), `error_message text`, `created_by uuid`, `created_at`, `updated_at`.
- `kb_chunks`: `id uuid PK`, `article_id → kb_articles CASCADE`, `company_id → companies CASCADE`, `chunk_index int`, `content text`, `tokens int default 0`, `embedding vector(1536)`, `hit_count int default 0`, `created_at`. Índice `ivfflat (embedding vector_cosine_ops) lists=100`.

#### knowledge_entries (CRM knowledge legacy)
`id uuid PK`, `company_id → companies CASCADE`, `title text`, `content text`, `type text`, `scope text default 'global'` (`global`|`categoria`), `scope_ref text`, `ai_visible bool default true`, `is_active bool default true`, `priority int default 0`, `created_by`, `updated_by`, `created_at`, `updated_at`.

#### thread_summaries
`id uuid PK`, `company_id → companies CASCADE`, `buyer_id text`, `product_id → products CASCADE`, `summary text`, `questions_hash text`, `model text`, `created_at`, `updated_at`. UNIQUE `(company_id, buyer_id, product_id)`.

#### templates
`id uuid PK`, `company_id → companies CASCADE`, `title text`, `content text`, `category text default 'general'`, `variables jsonb default '[]'`, `created_at`, `updated_at`. Índice `(company_id, category)`.

#### meli_tokens (nunca expuesta al frontend)
`id uuid PK`, `company_id uuid NOT NULL UNIQUE → companies CASCADE`, `access_token text NOT NULL`, `refresh_token text`, `meli_user_id text NOT NULL`, `expires_at timestamptz NOT NULL`, `created_at`, `updated_at`.
Vista/consulta segura: RPC `get_meli_connection_status` (no devuelve tokens).

#### notifications
`id uuid PK`, `user_id uuid NOT NULL`, `company_id uuid → companies CASCADE`, `type text`, `title text`, `message text`, `link text`, `read bool default false`, `created_at`.

#### events (log operativo) / audit_logs (auditoría de entidades)
- `events`: `id uuid PK`, `company_id → companies CASCADE`, `type text`, `entity_type text`, `entity_id text`, `payload jsonb default '{}'`, `created_at`.
- `audit_logs`: `id uuid PK`, `company_id → companies`, `actor_user_id uuid`, `entity_type text`, `entity_id uuid`, `action text`, `before_snapshot jsonb`, `after_snapshot jsonb`, `created_at`. Índices `(entity_type, entity_id)` y `(company_id, created_at DESC)`.

#### dismissed_meli_questions (blacklist de borrados definitivos)
`id uuid PK`, `meli_question_id text`, `company_id uuid`, `dismissed_at timestamptz`. UNIQUE `(meli_question_id, company_id)`.

#### mp_webhook_events / contact_inquiries
- `mp_webhook_events`: `id uuid PK`, `event_type text`, `payload jsonb`, `processed_at timestamptz`. Append-only, lectura solo super admin.
- `contact_inquiries`: `id uuid PK`, `name`, `email`, `message`, `created_at`. Insert público (anon), lectura solo super admin.

### 1.4 Relaciones (FK) — resumen
```
auth.users ─< profiles, memberships, user_roles, super_admins
companies  ─< memberships, profiles, company_invites, company_settings, products,
              product_variants, questions, customers, customer_tags, kb_articles,
              kb_chunks, knowledge_entries, thread_summaries, templates, meli_tokens,
              notifications, events, audit_logs
products   ─< product_variants, questions, thread_summaries
kb_articles─< kb_chunks
profiles   ─< questions.answered_by
```
Casi todas las FK son `ON DELETE CASCADE`, excepto `audit_logs.company_id`, `product_variants.company_id` y `questions.answered_by` (sin acción).

### 1.5 RLS — políticas por tabla

RLS habilitado en **todas** las tablas de `public`. Patrón general:

| Tabla | SELECT | INSERT | UPDATE | DELETE |
|---|---|---|---|---|
| companies | miembro o super admin | super admin | admin de la company | super admin |
| profiles | propio, misma company o super admin | propio | propio o super admin | — |
| memberships | propias, admin de company, super admin | admin (solo rol `agent`) o super admin | admin (solo `agent`) o super admin | admin de company o super admin |
| user_roles | propias | super admin (ALL) | super admin | super admin |
| super_admins | super admin | super admin | — | super admin |
| company_invites | admin de company o super admin | — (RPC) | — (RPC) | — |
| company_settings | admin | admin | admin | — |
| products / product_variants / kb_articles | miembro | admin o agent | admin o agent | admin (variants: admin o agent) |
| kb_chunks | miembro | admin o agent | — | admin |
| knowledge_entries | miembro | admin o agent | admin o agent | admin |
| questions | miembro | miembro | miembro | admin |
| customers | miembro | miembro | miembro | — |
| customer_tags | miembro | admin | admin | admin |
| templates | miembro | admin | admin | admin |
| thread_summaries | miembro | miembro | miembro | — |
| meli_tokens | super admin (tokens nunca al cliente) | — | — | admin de company |
| notifications | dueño (`user_id = auth.uid()`) | — (service role) | dueño (marcar leída) | — |
| events / audit_logs | miembro | — (service role) | — | — |
| dismissed_meli_questions | admin | admin | — | admin |
| mp_webhook_events | super admin | — | — | — |
| contact_inquiries | super admin | anon + authenticated | — | super admin |

Grants: `authenticated` en tablas de usuario, `anon` solo para `contact_inquiries` (INSERT), `service_role` en todo lo que tocan las Edge Functions.

### 1.6 Funciones SQL (todas `SECURITY DEFINER`, `search_path=public` salvo aclaración)

**Helpers de tenancy / roles**
- `is_super_admin() → bool`
- `has_role(_user_id, _role app_role) → bool`
- `has_membership_role(_user_id, _company_id, _role) → bool`
- `user_belongs_to_company(_user_id, _company_id) → bool`
- `get_user_company_id(_user_id) → uuid` · `get_user_default_company(_user_id)` · `get_user_company_ids(_user_id)` · `get_user_active_companies(_user_id)`

**Onboarding / equipo**
- `handle_new_user()` (trigger en `auth.users` AFTER INSERT): crea company + invite + profile + membership admin, o une por `invite_code`.
- `create_company_for_user(_company_name) → jsonb`
- `join_company_by_invite(_invite_code) → jsonb`
- `get_company_invite_code(_company_id) → text` (admin/super admin)
- `regenerate_company_invite_code(_company_id) → text`
- `get_company_members(_company_id)` · `add_company_membership(...)` (super admin) · `update_membership_role(...)` · `remove_company_membership(...)`

**Negocio**
- `get_company_analytics(_company_id, _days) → jsonb`: KPIs, SLA, volumen diario, categorías, top productos y compradores.
- `get_admin_company_metrics()` / `get_admin_users()` (super admin).
- `match_kb_chunks(_company_id, _query_embedding vector, _match_threshold, _match_count)`: búsqueda coseno en `kb_chunks`.
- `increment_chunk_hit_counts(chunk_ids uuid[])`
- `find_similar_products(_company_id, _product_id, _title, _threshold, _limit)` (pg_trgm)
- `backfill_customers(_company_id) → jsonb` · `increment_customer_questions(_company_id, _buyer_id)`
- `get_meli_connection_status(_company_id)`: estado de conexión MeLi sin exponer tokens.
- `get_cron_secret() → text`: lee `cron_secret` desde `vault.decrypted_secrets`.

**Triggers utilitarios**
- `update_updated_at_column()`, `validate_question_status()`, `validate_product_status()`, `validate_membership_status()`, `validate_knowledge_scope()`, `reset_sla_alert_on_reopen()`, `auto_create_company_invite()`.

### 1.7 Triggers

| Tabla | Trigger | Momento | Función |
|---|---|---|---|
| auth.users | on_auth_user_created | AFTER INSERT | handle_new_user |
| companies | trg_auto_create_company_invite | AFTER INSERT | auto_create_company_invite |
| company_settings, customers, kb_articles, knowledge_entries, memberships, products, product_variants, templates, thread_summaries | *_updated_at | BEFORE UPDATE | update_updated_at_column |
| knowledge_entries | validate_knowledge_scope_trigger | BEFORE INSERT/UPDATE | validate_knowledge_scope |
| memberships | validate_membership_status_trigger | BEFORE INSERT/UPDATE | validate_membership_status |
| products | trg_validate_product_status | BEFORE INSERT/UPDATE | validate_product_status |
| questions | trg_validate_question_status | BEFORE INSERT/UPDATE | validate_question_status |
| questions | trg_reset_sla_alert | BEFORE UPDATE | reset_sla_alert_on_reopen |

### 1.8 Jobs programados (pg_cron + pg_net)

| Job | Schedule | Acción |
|---|---|---|
| `sync-meli-questions-hourly-backup` | `0 * * * *` | POST a `/functions/v1/sync-meli-questions` con `{"source":"cron"}` + header `X-Cron-Secret` |
| `sla-breach-notifier-15min` | `*/15 * * * *` | POST a `/functions/v1/sla-breach-notifier` con `{"source":"cron"}` + `X-Cron-Secret` |

El secreto vive en `vault.secrets` bajo el nombre `cron_secret` y se lee con `get_cron_secret()`.

---

## 2. Edge Functions (Deno / Supabase)

Patrón de auth interno: `verify_jwt = false` en `config.toml` + validación manual (`supabaseAdmin.auth.getUser(token)`) + chequeo de membresía con `user_belongs_to_company`. El `company_id` siempre se deriva de la base, nunca del body sin validar.

| Función | Método | Input | Output | Auth | Integraciones |
|---|---|---|---|---|---|
| `ai-copilot` | POST | `{question_text, product_title, product_price, buyer_nickname, ai_category, ai_suggested_answer, ai_tone, ai_custom_instructions, product_id}` | `{answer, sources[], confidence}` | JWT usuario | Lovable AI Gateway (Gemini) + OpenAI embeddings (RAG sobre kb_chunks) |
| `sync-meli-questions` | POST | `{source:"cron"\|"manual", company_id?, resource?, meli_user_id?}` | `{synced, autopublished, ...}` | JWT usuario o `X-Cron-Secret` | MeLi API + Lovable AI Gateway |
| `publish-meli-answer` | POST | `{question_id, answer}` | `{ok:true}` / `{error}` | JWT + membresía | MeLi `POST /answers` |
| `meli-oauth-callback` | GET/POST | `code`, `state`, `code_verifier` (PKCE) | HTML/postMessage al popup | pública (state) | MeLi `POST /oauth/token` |
| `meli-webhook` | GET (verificación) / POST | `{topic, resource, user_id, application_id}` | `{received:true}` (siempre 200) | `?secret=` opcional (`MELI_WEBHOOK_SECRET`) | reenvía a `sync-meli-questions` |
| `meli-item-proxy` | POST | `{item_id}` | item + description de MeLi | JWT + membresía | MeLi `/items/{id}`, `/items/{id}/description` |
| `disconnect-meli` | POST | `{company_id}` | `{success:true}` | JWT + admin | — |
| `debug-meli` | POST | — | grants de la app | JWT + super admin | MeLi `/applications/{app_id}/grants` |
| `enrich-product` | POST | `{product_id, force_refresh?}` | producto enriquecido | JWT + membresía derivada del producto | MeLi items/categories + Lovable AI |
| `detect-duplicates` | POST | `{product_id}` | `{duplicates:[{id,title,similarity}]}` | JWT + membresía | RPC `find_similar_products` |
| `kb-process-article` | POST | `{article_id, company_id}` | `{ok:true, chunks:n}` | JWT + membresía | OpenAI `text-embedding-3-small` |
| `kb-search` | POST | `{company_id, query, match_count=5, match_threshold=0.5}` | `{matches:[...]}` | JWT + membresía | OpenAI embeddings + RPC `match_kb_chunks` |
| `kb-delete-article` | POST | `{article_id, company_id}` | `{ok:true}` | JWT + admin | — |
| `summarize-thread` | POST | `{company_id, buyer_id, product_id, force?}` | `{summary, cached?}` | JWT + membresía | Lovable AI Gateway (gemini-2.5-flash-lite), cache por hash SHA-256 |
| `sla-breach-notifier` | POST | `{source:"cron"}` | `{ok:true, totalSent, perCompany}` | `X-Cron-Secret` | Resend (email HTML) |
| `notify` | POST | `{type, company_id, title, message, link}` | `{created:n}` | service role interno | — |
| `audit-log` | POST | `{company_id, entity_type, entity_id, action, before_snapshot, after_snapshot}` | `{ok:true}` | JWT + membresía | — |
| `admin-create-user` | POST | `{email, password, full_name, company_id?, role?, plan?}` | `{success:true, user_id}` | JWT + `is_super_admin()` | Supabase Admin API |
| `auth-email-hook` | POST | payload de Auth Hook (HMAC) | `{success:true, message_id}` | HMAC del hook | Lovable Email (plantillas React Email) |
| `mp-create-subscription` | POST | `{company_id}` | `{checkout_url}` / `{already_subscribed:true}` | JWT + admin | Mercado Pago `POST /preapproval` |
| `mp-check-subscription` | POST | `{company_id}` | `{billing_status, plan, period_end}` | JWT + membresía | MP `GET /preapproval/{id}` |
| `mp-cancel-subscription` | POST | `{company_id}` (derivado de DB) | `{success:true, billing_status:"paused"}` | JWT + admin | MP `PUT /preapproval/{id}` (`status: paused`) |
| `mp-webhook` | POST | IPN `subscription_preapproval` | `{received:true}` (siempre 200) | HMAC SHA-256 `MP_WEBHOOK_SECRET` | MP API |
| `health-check` | GET | — | `{status:"healthy"\|"degraded", latency_ms, timestamp}` | pública | — |
| `mcp` | POST | JSON-RPC MCP | respuesta MCP | OAuth Supabase | Servidor MCP con 5 tools |

---

## 3. Integraciones externas

### 3.1 Mercado Libre
- **OAuth 2.0 + PKCE**: `POST https://api.mercadolibre.com/oauth/token` (grant `authorization_code` y `refresh_token`). Un token por empresa (`meli_tokens`, UNIQUE `company_id`). Refresh automático cuando faltan ≤5 minutos (`_shared/refreshMeliToken.ts`).
- **Endpoints consumidos**:
  - `GET /my/received_questions/search` — preguntas recibidas (sync general)
  - `GET {resource}` — pregunta puntual notificada por webhook
  - `POST /answers` — publicar respuesta
  - `GET /items`, `GET /items/{id}`, `GET /items/{id}/description` — catálogo y ficha
  - `GET /categories/{id}` — nombre de categoría
  - `GET /users/{id}` — nickname del comprador
  - `GET /applications/{app_id}/grants` — diagnóstico
- **Datos sincronizados**: preguntas (texto, comprador, ítem, estado, permalink), productos (título, precio, permalink, categoría, descripción, cache en `products.meli_cache`), clientes (`customers`). **No** se sincronizan stock, envíos ni garantías como entidades propias: envíos/garantías existen solo como notas de texto en `products`.
- **Frecuencia**: webhook push en tiempo real (vía `meli-webhook`) + cron horario de respaldo.

### 3.2 IA
- **Lovable AI Gateway** (`https://ai.gateway.lovable.dev/v1/chat/completions`, header `Authorization: Bearer LOVABLE_API_KEY`): categorización de preguntas, autopilot, copiloto, enriquecimiento de productos, resúmenes de hilo (`google/gemini-2.5-flash-lite`).
- **OpenAI** (`https://api.openai.com/v1/embeddings`): `text-embedding-3-small` (1536 dims) para KB y búsqueda semántica.

### 3.3 Mercado Pago
Suscripciones recurrentes con Preapproval (`external_reference = company_id`). Webhook IPN con HMAC SHA-256 (manifest `id:DATA_ID;request-id:REQ_ID;ts:TS;`). Log en `mp_webhook_events`. Cancelar = pausar.

### 3.4 Email
- **Resend** (`https://api.resend.com/emails`): alertas de vencimiento de SLA a `company_settings.sla_alert_emails`.
- **Lovable Email**: emails de autenticación (signup, recovery, magic link, invite, email change, reauth) vía `auth-email-hook`.

### 3.5 Notificaciones in-app
Tabla `notifications` + Supabase Realtime (`postgres_changes` filtrado por company activa). Push del navegador con Web Notifications API cuando la pestaña está en segundo plano.

---

## 4. Autenticación y roles

### 4.1 Login
- **Supabase Auth** con email/password (`signInWithPassword`, `signUp` con `user_metadata: {full_name, company_name | invite_code}`).
- **Google OAuth** vía `@lovable.dev/cloud-auth-js` (capa sobre Supabase Auth; sustituible por `supabase.auth.signInWithOAuth({provider:'google'})`). El resultado se inyecta con `supabase.auth.setSession(tokens)`.
- Sesión persistida en `localStorage`, `autoRefreshToken: true`. El JWT viaja como `Authorization: Bearer <access_token>` en toda llamada a PostgREST y Edge Functions.
- HIBP (contraseñas filtradas) activado. Signups anónimos deshabilitados.
- Trigger `handle_new_user` crea company/profile/membership al registrarse.

### 4.2 Roles

| Rol | Dónde vive | Puede |
|---|---|---|
| **agent** | `memberships.role = 'agent'` | Ver e interactuar con preguntas, clientes, productos, variantes y KB de sus empresas; responder y publicar; no toca settings, plantillas, tags ni borra nada crítico |
| **admin** | `memberships.role = 'admin'` | Todo lo del agent + settings de la empresa, plantillas, tags, conexión MeLi, invitaciones, billing, borrados, gestionar miembros (solo puede otorgar rol `agent`) |
| **super admin** | fila en `public.super_admins` | Acceso global: todas las empresas y usuarios, crear usuarios, otorgar rol `admin`, ver logs de MP y consultas de contacto, bypass de billing |

Un usuario puede pertenecer a varias empresas; `is_default` define la empresa activa inicial. Todo el aislamiento se resuelve con `user_belongs_to_company` / `has_membership_role` dentro de las políticas RLS y de funciones `SECURITY DEFINER`.

---

## 5. Variables de entorno

### 5.1 Frontend (públicas, prefijo `VITE_`)
| Nombre | Para qué |
|---|---|
| `VITE_SUPABASE_URL` | URL del proyecto Supabase |
| `VITE_SUPABASE_PUBLISHABLE_KEY` | anon/publishable key del cliente |
| `VITE_SUPABASE_PROJECT_ID` | ref del proyecto (utilitario) |

### 5.2 Edge Functions (secretos del servidor)
| Nombre | Para qué | Usado por |
|---|---|---|
| `SUPABASE_URL` | URL interna del proyecto | todas |
| `SUPABASE_SERVICE_ROLE_KEY` | cliente admin (bypass RLS) | todas |
| `SUPABASE_ANON_KEY` | cliente en contexto del caller (RPC con su JWT) | funciones con auth de usuario |
| `LOVABLE_API_KEY` | AI Gateway (Gemini) y Lovable Email | ai-copilot, sync-meli-questions, enrich-product, summarize-thread, auth-email-hook |
| `OPENAI_API_KEY` | embeddings `text-embedding-3-small` | kb-process-article, kb-search, ai-copilot |
| `MELI_APP_ID` | client_id de la app de Mercado Libre | oauth-callback, sync, publish, item-proxy, enrich, debug |
| `MELI_SECRET_KEY` | client_secret de MeLi | ídem |
| `MELI_WEBHOOK_SECRET` | valida `?secret=` del webhook de MeLi (opcional) | meli-webhook |
| `MP_ACCESS_TOKEN` | token de Mercado Pago | mp-webhook |
| `MP_TEST_SECRET` | token MP usado en create/check/cancel | mp-* |
| `MP_PREAPPROVAL_PLAN_ID` | ID del plan de suscripción | mp-create-subscription |
| `MP_WEBHOOK_SECRET` | clave HMAC del IPN de MP | mp-webhook |
| `RESEND_API_KEY` | envío de alertas SLA | sla-breach-notifier |
| `CRON_SECRET` | valida `X-Cron-Secret` de los jobs | sla-breach-notifier, sync-meli-questions |
| `SUPABASE_DB_URL`, `SUPABASE_JWKS` | provistos por la plataforma | infraestructura |

> El secreto de cron también se guarda en `vault.secrets` como `cron_secret` y se lee con la RPC `get_cron_secret()` desde `pg_cron` y `meli-webhook`.

### 5.3 No aplica
- Storage buckets: **no aplica** (no hay buckets creados).
- Stripe: **no aplica** (eliminado del proyecto).
- Sincronización de stock, envíos y reclamos de MeLi: **no aplica** (no implementado).
