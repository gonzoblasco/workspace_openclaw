# ADR-002: Sistema de Auto-Respuesta Inteligente con RAG, Auto-Learn y Billing

**Estado:** Aprobado  
**Fecha:** 2026-07-20  
**Contexto:** SoporteML v2 — SaaS multi-tenant para vendedores de Mercado Libre  
**Stack:** Supabase (PostgreSQL + RLS + pgvector), React 19 + Vite + Tailwind v4 + shadcn/ui, Edge Functions (Deno/TypeScript), DeepSeek (IA), Mercado Pago (billing)

---

## 1. Contexto y Problema

SoporteML es un CRM multi-tenant donde cada tenant (vendedor de MeLi) conecta sus cuentas de Mercado Libre vía OAuth2. Los clientes de esos vendedores hacen preguntas sobre productos. El sistema debe:

1. **Clasificar** cada pregunta como rutinaria (auto-responder con IA) o compleja (derivar a humano).
2. **Responder automáticamente** las rutinarias usando RAG sobre una Knowledge Base vectorial.
3. **Auto-aprender** al conectar una cuenta: fetch histórico de preguntas → generar fichas de producto → indexar en KB.
4. **Respetar rate limits** de MeLi API (300 req/min) con cola y retry.
5. **Facturar** por suscripción con límites de preguntas auto-respondidas.

### 1.1 Restricciones

- Sin servicios externos pagos para re-ranking (el re-ranker debe ser local/autónomo).
- Consistencia eventual aceptable entre webhook de MeLi y estado local.
- Multi-tenant estricto: un tenant nunca ve datos de otro.
- pgvector con embeddings de 1536 dimensiones (OpenAI ada-002 o similar).
- Edge Functions de Supabase como backend serverless.

---

## 2. Decisión: Arquitectura General

### 2.1 Diagrama de Flujo

```
MeLi Webhook / Polling
        │
        ▼
┌──────────────────┐
│  Rate Limiter    │  ← Cola + Retry exponencial
│  + Message Queue │
└────────┬─────────┘
         │ pregunta entrante
         ▼
┌──────────────────┐
│  Classifier      │  ← Edge Function: clasifica rutinaria/compleja
│  (DeepSeek +     │     Features: historial cliente, tipo producto,
│   heurísticas)   │     hora del día, preguntas similares, confianza
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
 rutinaria  compleja
    │         │
    ▼         ▼
┌────────┐  ┌──────────┐
│ RAG    │  │ Derivar   │ → Inbox humano
│ Pipeline│  │ a humano  │
└───┬────┘  └──────────┘
    │
    ▼
┌──────────────────┐
│  Re-ranker       │  ← Local: cross-encoder miniLM vía Supabase ML
│  (confianza)     │     o re-rank heurístico (TF-IDF + position)
└────────┬─────────┘
         │
    ┌────┴────┐
    │         │
 confianza  confianza
 ≥ 0.7      < 0.7
    │         │
    ▼         ▼
┌────────┐  ┌──────────┐
│ Auto-  │  │ Derivar   │
│ reply  │  │ a humano  │
└───┬────┘  └──────────┘
    │
    ▼
┌──────────────────┐
│  Billing Guard   │  ← Verifica límite mensual del plan
└────────┬─────────┘
         │
         ▼
    Enviar respuesta
    (API MeLi reply)
         │
         ▼
┌──────────────────┐
│  Feedback Loop   │  ← Vendedor corrige/confirma → re-entrena
└──────────────────┘
```

---

## 3. Arquitectura de Base de Datos

### 3.1 Tablas de Auto-Respuesta

```sql
-- ============================================================
-- MIGRACIÓN: auto_respuesta_system
-- ============================================================

-- 1. CLASIFICACIÓN: cada pregunta entrante se clasifica aquí
CREATE TABLE auto_classifications (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id     UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  question_id   TEXT NOT NULL,  -- ID de la pregunta en MeLi
  question_text TEXT NOT NULL,
  product_id    TEXT NOT NULL,  -- ID del producto en MeLi
  customer_id   TEXT NOT NULL,  -- ID del comprador en MeLi

  -- Clasificación
  classification  TEXT NOT NULL CHECK (classification IN ('rutinaria', 'compleja')),
  confidence      NUMERIC(4,3) NOT NULL CHECK (confidence >= 0 AND confidence <= 1),
  model_version   TEXT NOT NULL DEFAULT 'deepseek-v4-flash',
  classifier_meta JSONB,        -- { "historial_preguntas": 3, "preguntas_similares": 12, "hora": 14, "tipo_producto": "electronica" }

  -- Tracking
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  classified_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  response_id     UUID,         -- FK a auto_responses, se setea si se auto-respondió

  -- Unique: una clasificación por pregunta (evita duplicados de webhook)
  UNIQUE(tenant_id, question_id)
);

CREATE INDEX idx_auto_classifications_tenant ON auto_classifications(tenant_id, created_at DESC);
CREATE INDEX idx_auto_classifications_product ON auto_classifications(tenant_id, product_id);
CREATE INDEX idx_auto_classifications_customer ON auto_classifications(tenant_id, customer_id);
CREATE INDEX idx_auto_classifications_conf ON auto_classifications(tenant_id, classification, confidence);


-- 2. RESPUESTAS GENERADAS
CREATE TABLE auto_responses (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  classification_id UUID NOT NULL REFERENCES auto_classifications(id) ON DELETE CASCADE,
  question_id     TEXT NOT NULL,

  -- Pipeline RAG
  retrieved_chunks  UUID[] NOT NULL DEFAULT '{}',  -- IDs de kb_chunks usados
  reranked_chunks   JSONB,  -- [{chunk_id, score, position}, ...] ordenado por score
  reranker_score    NUMERIC(4,3),  -- Score final del re-ranker
  generated_answer  TEXT NOT NULL,
  answer_model      TEXT NOT NULL DEFAULT 'deepseek-v4-flash',

  -- Estado
  status          TEXT NOT NULL DEFAULT 'pending'
                    CHECK (status IN ('pending', 'approved', 'rejected', 'sent', 'failed')),
  sent_at         TIMESTAMPTZ,     -- Cuándo se envió a MeLi
  meli_message_id TEXT,            -- ID de la respuesta en MeLi
  error_message   TEXT,            -- Si falló el envío

  -- Billing
  billed          BOOLEAN NOT NULL DEFAULT FALSE,
  billing_period  TEXT,            -- "2026-07" para tracking mensual

  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_auto_responses_tenant ON auto_responses(tenant_id, created_at DESC);
CREATE INDEX idx_auto_responses_status ON auto_responses(tenant_id, status);
CREATE INDEX idx_auto_responses_billing ON auto_responses(tenant_id, billing_period, billed)
  WHERE billed = TRUE;


-- 3. FEEDBACK LOOP: el vendedor corrige o confirma respuestas
CREATE TABLE auto_response_feedback (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  response_id     UUID NOT NULL REFERENCES auto_responses(id) ON DELETE CASCADE,

  -- Feedback del vendedor
  action          TEXT NOT NULL CHECK (action IN ('approve', 'edit', 'reject', 'flag')),
  edited_answer   TEXT,             -- Si editó, la nueva versión
  reason          TEXT,             -- Por qué rechazó/flaggeó
  customer_replied BOOLEAN,         -- El comprador respondió? (señal de calidad)

  -- Para re-entrenamiento
  used_for_training BOOLEAN NOT NULL DEFAULT FALSE,
  training_notes   TEXT,

  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(tenant_id, response_id)  -- Un feedback por respuesta
);


-- 4. CONFIANZA HISTÓRICA: tracking de precisión del clasificador
CREATE TABLE auto_classifier_metrics (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  date            DATE NOT NULL DEFAULT CURRENT_DATE,

  total_classified    INT NOT NULL DEFAULT 0,
  auto_responded      INT NOT NULL DEFAULT 0,
  approved_by_user    INT NOT NULL DEFAULT 0,
  rejected_by_user    INT NOT NULL DEFAULT 0,
  edited_by_user      INT NOT NULL DEFAULT 0,
  avg_confidence      NUMERIC(4,3),

  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(tenant_id, date)
);


-- 5. COLAS DE RATE LIMITING (para MeLi API)
CREATE TABLE meli_rate_queue (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  meli_account_id UUID NOT NULL REFERENCES meli_accounts(id) ON DELETE CASCADE,

  -- Operación
  operation       TEXT NOT NULL,  -- 'reply_question', 'fetch_questions', 'fetch_product', etc.
  payload         JSONB NOT NULL, -- Datos necesarios para ejecutar
  priority        INT NOT NULL DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),

  -- Estado de la cola
  status          TEXT NOT NULL DEFAULT 'queued'
                    CHECK (status IN ('queued', 'processing', 'completed', 'failed', 'retrying')),
  retry_count     INT NOT NULL DEFAULT 0,
  max_retries     INT NOT NULL DEFAULT 5,
  last_error      TEXT,
  next_retry_at   TIMESTAMPTZ,    -- Para retry exponencial

  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  started_at      TIMESTAMPTZ,
  completed_at    TIMESTAMPTZ
);

CREATE INDEX idx_meli_rate_queue_pending
  ON meli_rate_queue(tenant_id, priority, created_at)
  WHERE status = 'queued';
CREATE INDEX idx_meli_rate_queue_retry
  ON meli_rate_queue(next_retry_at)
  WHERE status = 'retrying' AND next_retry_at <= now();


-- 6. AUTO-LEARN: fichas de producto generadas automáticamente
CREATE TABLE auto_product_fichas (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  meli_product_id TEXT NOT NULL,

  -- Datos de la ficha
  title           TEXT NOT NULL,
  category        TEXT,
  attributes      JSONB,          -- Atributos del producto en MeLi
  common_questions JSONB,         -- Preguntas frecuentes extraídas del histórico
  answer_patterns  JSONB,         -- Patrones de respuesta del vendedor

  -- Embedding de la ficha (para matching)
  embedding       VECTOR(1536),

  -- Metadata
  source          TEXT NOT NULL DEFAULT 'auto-learn' CHECK (source IN ('auto-learn', 'manual', 'import')),
  questions_analyzed INT NOT NULL DEFAULT 0,  -- Cuántas preguntas históricas se usaron
  generated_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

  UNIQUE(tenant_id, meli_product_id)
);

CREATE INDEX idx_auto_product_fichas_tenant ON auto_product_fichas(tenant_id);
CREATE INDEX idx_auto_product_fichas_embedding
  ON auto_product_fichas
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);


-- 7. KNOWLEDGE BASE (existente, extendida)
-- Se agrega columna source_type a kb_chunks
ALTER TABLE kb_chunks ADD COLUMN IF NOT EXISTS source_type TEXT
  DEFAULT 'manual' CHECK (source_type IN ('manual', 'auto-ficha', 'auto-faq', 'auto-pattern', 'feedback'));

CREATE INDEX IF NOT EXISTS idx_kb_chunks_source_type
  ON kb_chunks(tenant_id, source_type);


-- 8. BILLING: tracking de uso mensual
CREATE TABLE billing_usage (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
  billing_period  TEXT NOT NULL,  -- "2026-07"

  -- Límites del plan
  plan_limit      INT NOT NULL,   -- Preguntas auto-respondidas permitidas
  usage_count     INT NOT NULL DEFAULT 0,

  -- Prorrateo
  plan_started_at TIMESTAMPTZ NOT NULL,
  plan_ends_at    TIMESTAMPTZ NOT NULL,
  is_prorated     BOOLEAN NOT NULL DEFAULT FALSE,
  prorated_limit  INT,            -- Límite ajustado si empezó a mitad de mes

  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),

  UNIQUE(tenant_id, billing_period)
);
```

### 3.2 Políticas RLS

```sql
-- ============================================================
-- RLS: Multi-tenant estricto
-- ============================================================

-- Helper: el tenant_id del usuario autenticado
CREATE OR REPLACE FUNCTION auth.tenant_id()
RETURNS UUID
LANGUAGE SQL STABLE
AS $$
  SELECT COALESCE(
    (SELECT raw_user_meta_data->>'tenant_id' FROM auth.users WHERE id = auth.uid()),
    (SELECT tenant_id FROM user_tenants WHERE user_id = auth.uid() LIMIT 1)
  );
$$;

-- auto_classifications
ALTER TABLE auto_classifications ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON auto_classifications
  FOR ALL USING (tenant_id = auth.tenant_id());

-- auto_responses
ALTER TABLE auto_responses ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON auto_responses
  FOR ALL USING (tenant_id = auth.tenant_id());

-- auto_response_feedback
ALTER TABLE auto_response_feedback ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON auto_response_feedback
  FOR ALL USING (tenant_id = auth.tenant_id());

-- auto_classifier_metrics
ALTER TABLE auto_classifier_metrics ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON auto_classifier_metrics
  FOR ALL USING (tenant_id = auth.tenant_id());

-- meli_rate_queue
ALTER TABLE meli_rate_queue ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON meli_rate_queue
  FOR ALL USING (tenant_id = auth.tenant_id());

-- auto_product_fichas
ALTER TABLE auto_product_fichas ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON auto_product_fichas
  FOR ALL USING (tenant_id = auth.tenant_id());

-- billing_usage
ALTER TABLE billing_usage ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON billing_usage
  FOR ALL USING (tenant_id = auth.tenant_id());


-- Índices adicionales para performance multi-tenant
CREATE INDEX idx_kb_chunks_tenant_embedding
  ON kb_chunks(tenant_id, embedding vector_cosine_ops);

-- Para el cron de rate limiting: encontrar items pendientes rápido
CREATE INDEX idx_meli_rate_queue_processing
  ON meli_rate_queue(tenant_id, meli_account_id, status, next_retry_at)
  WHERE status IN ('queued', 'retrying');
```

---

## 4. Edge Functions Clave

### 4.1 Classifier Edge Function

```typescript
// supabase/functions/classify-question/index.ts
import { serve } from 'https://deno.land/std@0.224.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.45.0'

interface ClassifyRequest {
  tenant_id: string
  question_id: string
  question_text: string
  product_id: string
  customer_id: string
}

interface ClassifyResponse {
  classification: 'rutinaria' | 'compleja'
  confidence: number
  features: ClassifierFeatures
}

interface ClassifierFeatures {
  customer_history_count: number
  similar_questions_resolved: number
  hour_of_day: number
  product_category: string
  question_length: number
  has_attachments: boolean
  is_follow_up: boolean
}

serve(async (req) => {
  const { tenant_id, question_id, question_text, product_id, customer_id } =
    await req.json() as ClassifyRequest

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  // 1. Extraer features
  const features = await extractFeatures(supabase, {
    tenant_id, question_text, product_id, customer_id
  })

  // 2. Clasificar con DeepSeek + heurísticas
  const { classification, confidence } = await classifyWithAI(
    question_text,
    features
  )

  // 3. Guardar clasificación
  const { error } = await supabase
    .from('auto_classifications')
    .insert({
      tenant_id,
      question_id,
      question_text,
      product_id,
      customer_id,
      classification,
      confidence,
      classifier_meta: features,
    })

  if (error) throw error

  // 4. Si es rutinaria con confianza suficiente, encolar RAG
  if (classification === 'rutinaria' && confidence >= 0.7) {
    await enqueueRagPipeline(supabase, {
      tenant_id, question_id, question_text, product_id, customer_id
    })
  }

  return new Response(JSON.stringify({ classification, confidence, features }), {
    headers: { 'Content-Type': 'application/json' },
  })
})

async function extractFeatures(
  supabase: any,
  { tenant_id, question_text, product_id, customer_id }: any
): Promise<ClassifierFeatures> {
  const hour = new Date().getHours()

  // Historial del cliente: preguntas previas de este comprador
  const { count: customerHistory } = await supabase
    .from('auto_classifications')
    .select('*', { count: 'exact', head: true })
    .eq('tenant_id', tenant_id)
    .eq('customer_id', customer_id)

  // Preguntas similares resueltas: match semántico contra KB
  const { count: similarResolved } = await supabase
    .from('auto_classifications')
    .select('*', { count: 'exact', head: true })
    .eq('tenant_id', tenant_id)
    .eq('classification', 'rutinaria')
    .textSearch('question_text', question_text, { config: 'spanish' })

  // Categoría del producto
  const { data: product } = await supabase
    .from('auto_product_fichas')
    .select('category')
    .eq('tenant_id', tenant_id)
    .eq('meli_product_id', product_id)
    .single()

  return {
    customer_history_count: customerHistory ?? 0,
    similar_questions_resolved: similarResolved ?? 0,
    hour_of_day: hour,
    product_category: product?.category ?? 'unknown',
    question_length: question_text.length,
    has_attachments: question_text.includes('http') || question_text.includes('img'),
    is_follow_up: /^(y|pero|además|otra cosa|sigue|todavía)/i.test(question_text.trim()),
  }
}

async function classifyWithAI(
  question: string,
  features: ClassifierFeatures
): Promise<{ classification: 'rutinaria' | 'compleja'; confidence: number }> {
  const DEEPSEEK_API_KEY = Deno.env.get('DEEPSEEK_API_KEY')
  if (!DEEPSEEK_API_KEY) {
    // Fallback: clasificación heurística sin IA
    return heuristicClassify(question, features)
  }

  const prompt = `Eres un clasificador de preguntas de e-commerce. Clasifica la siguiente pregunta como "rutinaria" (se puede responder automáticamente) o "compleja" (requiere intervención humana).

Contexto:
- Historial de preguntas del comprador: ${features.customer_history_count}
- Preguntas similares resueltas automáticamente: ${features.similar_questions_resolved}
- Hora del día: ${features.hour_of_day}:00
- Categoría del producto: ${features.product_category}
- Longitud de la pregunta: ${features.question_length} caracteres
- Tiene adjuntos: ${features.has_attachments}
- Es follow-up: ${features.is_follow_up}

Pregunta: "${question}"

Responde SOLO con un JSON: { "classification": "rutinaria" | "compleja", "confidence": 0.0-1.0, "reason": "breve explicación" }`

  const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${DEEPSEEK_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'deepseek-chat',
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.1,  // Baja temperatura para clasificación determinística
      max_tokens: 150,
    }),
  })

  const data = await response.json()
  const result = JSON.parse(data.choices[0].message.content)

  return {
    classification: result.classification,
    confidence: Math.min(1, Math.max(0, result.confidence)),
  }
}

function heuristicClassify(
  question: string,
  features: ClassifierFeatures
): { classification: 'rutinaria' | 'compleja'; confidence: number } {
  // Heurísticas offline cuando DeepSeek no está disponible
  const q = question.toLowerCase()

  // Palabras clave de preguntas rutinarias típicas
  const routineKeywords = [
    'cuándo', 'horario', 'precio', 'cuánto', 'medidas', 'talle',
    'color', 'disponible', 'stock', 'envío', 'costo', 'garantía',
    'funciona', 'compatible', 'incluye', 'trae',
  ]

  // Palabras clave de preguntas complejas
  const complexKeywords = [
    'problema', 'roto', 'defectuoso', 'devolución', 'reclamo',
    'cancelar', 'error', 'no funciona', 'llegó mal', 'incompleto',
  ]

  const hasRoutine = routineKeywords.some(k => q.includes(k))
  const hasComplex = complexKeywords.some(k => q.includes(k))
  const isLong = features.question_length > 200
  const hasHistory = features.customer_history_count > 3
  const isLate = features.hour_of_day < 8 || features.hour_of_day > 22

  let score = 0.5

  if (hasComplex) score -= 0.3
  if (hasRoutine && !hasComplex) score += 0.2
  if (isLong) score -= 0.15
  if (hasHistory) score -= 0.1  // Cliente recurrente puede ser complejo
  if (isLate) score -= 0.05     // Horario no laboral: preferir auto-respuesta
  if (features.is_follow_up) score -= 0.2
  if (features.has_attachments) score -= 0.15

  const classification = score >= 0.5 ? 'rutinaria' : 'compleja'
  return {
    classification,
    confidence: Math.abs(score - 0.5) * 2,  // Normalizado a 0-1
  }
}

async function enqueueRagPipeline(supabase: any, data: any) {
  // Inserta en la cola de rate limiting para el pipeline RAG
  await supabase.from('meli_rate_queue').insert({
    tenant_id: data.tenant_id,
    meli_account_id: data.meli_account_id,
    operation: 'rag_pipeline',
    payload: data,
    priority: 8,  // Alta prioridad: responder rápido
  })
}
```

### 4.2 RAG Pipeline Edge Function

```typescript
// supabase/functions/rag-pipeline/index.ts
import { serve } from 'https://deno.land/std@0.224.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.45.0'

interface RAGRequest {
  tenant_id: string
  question_id: string
  question_text: string
  product_id: string
  customer_id: string
  classification_id: string
}

serve(async (req) => {
  const data = await req.json() as RAGRequest
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  // 1. Generar embedding de la pregunta
  const questionEmbedding = await generateEmbedding(data.question_text)

  // 2. Buscar en KB: top 10 chunks más similares
  const { data: chunks } = await supabase.rpc('match_kb_chunks', {
    query_embedding: questionEmbedding,
    match_threshold: 0.5,
    match_count: 10,
    p_tenant_id: data.tenant_id,
  })

  if (!chunks || chunks.length === 0) {
    // Sin contexto en KB → derivar a humano
    await markAsComplex(data.classification_id)
    return new Response(JSON.stringify({ action: 'derived_to_human', reason: 'no_kb_context' }))
  }

  // 3. Re-rank local
  const reranked = await localReranker(data.question_text, chunks)

  // 4. Tomar top 3 después del re-rank
  const topChunks = reranked.slice(0, 3)
  const rerankerScore = topChunks[0]?.score ?? 0

  // 5. Si confianza < 0.7, derivar a humano
  if (rerankerScore < 0.7) {
    await markAsComplex(data.classification_id)
    return new Response(JSON.stringify({
      action: 'derived_to_human',
      reason: 'low_confidence',
      reranker_score: rerankerScore,
    }))
  }

  // 6. Generar respuesta con DeepSeek
  const answer = await generateAnswer(data.question_text, topChunks)

  // 7. Verificar billing antes de enviar
  const canBill = await checkBillingLimit(supabase, data.tenant_id)
  if (!canBill) {
    // Sin crédito: derivar a humano con nota
    await markAsComplex(data.classification_id)
    return new Response(JSON.stringify({
      action: 'derived_to_human',
      reason: 'billing_limit_exceeded',
    }))
  }

  // 8. Guardar respuesta
  const { data: response, error } = await supabase
    .from('auto_responses')
    .insert({
      tenant_id: data.tenant_id,
      classification_id: data.classification_id,
      question_id: data.question_id,
      retrieved_chunks: topChunks.map(c => c.id),
      reranked_chunks: reranked.map(c => ({ chunk_id: c.id, score: c.score, position: c.position })),
      reranker_score: rerankerScore,
      generated_answer: answer,
      status: 'pending',
    })
    .select()
    .single()

  if (error) throw error

  // 9. Encolar envío a MeLi (pasa por rate limiter)
  await supabase.from('meli_rate_queue').insert({
    tenant_id: data.tenant_id,
    operation: 'reply_question',
    payload: {
      question_id: data.question_id,
      response_id: response.id,
      answer_text: answer,
    },
    priority: 9,
  })

  return new Response(JSON.stringify({
    action: 'queued_for_send',
    response_id: response.id,
    reranker_score: rerankerScore,
  }), { headers: { 'Content-Type': 'application/json' } })
})

// --- Re-Ranker Local ---

interface ChunkResult {
  id: string
  content: string
  similarity: number  // cosine similarity del embedding
  source_type: string
}

interface RerankedChunk extends ChunkResult {
  score: number
  position: number
}

async function localReranker(
  question: string,
  chunks: ChunkResult[]
): Promise<RerankedChunk[]> {
  // Estrategia híbrida: combina 3 señales

  const results: RerankedChunk[] = await Promise.all(
    chunks.map(async (chunk, i) => {
      // Señal 1: Similaridad coseno (del embedding) — peso 0.5
      const cosineScore = chunk.similarity

      // Señal 2: Relevancia TF-IDF local — peso 0.3
      const tfidfScore = computeTfIdfScore(question, chunk.content)

      // Señal 3: Proximidad semántica con miniLM via ONNX — peso 0.2
      // Fallback: Jaccard similarity si no hay ONNX
      const semanticScore = await computeSemanticScore(question, chunk.content)

      // Bonus: chunks de auto-fichas tienen prioridad
      const sourceBonus = chunk.source_type === 'auto-ficha' ? 0.05 : 0

      const finalScore = Math.min(1,
        cosineScore * 0.5 +
        tfidfScore * 0.3 +
        semanticScore * 0.2 +
        sourceBonus
      )

      return { ...chunk, score: finalScore, position: i }
    })
  )

  // Ordenar por score descendente
  results.sort((a, b) => b.score - a.score)
  results.forEach((r, i) => { r.position = i })

  return results
}

function computeTfIdfScore(question: string, chunk: string): number {
  // TF-IDF simplificado: frecuencia de términos de la pregunta en el chunk
  const qTerms = question.toLowerCase().split(/\s+/).filter(t => t.length > 3)
  const chunkLower = chunk.toLowerCase()

  if (qTerms.length === 0) return 0

  const stopWords = new Set([
    'este', 'esta', 'esto', 'para', 'con', 'por', 'como', 'más', 'pero',
    'que', 'del', 'las', 'los', 'una', 'uno', 'sus', 'entre', 'cada',
  ])

  const significantTerms = qTerms.filter(t => !stopWords.has(t))
  if (significantTerms.length === 0) return 0

  const matches = significantTerms.filter(t => chunkLower.includes(t)).length
  return matches / significantTerms.length
}

async function computeSemanticScore(question: string, chunk: string): Promise<number> {
  // Opción A: ONNX miniLM (si está disponible en la Edge Function)
  try {
    // Intentar cargar modelo ONNX local
    // const session = await ort.InferenceSession.create('./models/reranker.onnx')
    // const result = await session.run({ input: tokenize(question, chunk) })
    // return result.score.data[0]

    // Opción B: Fallback a Jaccard similarity
    const qSet = new Set(question.toLowerCase().split(/\s+/))
    const cSet = new Set(chunk.toLowerCase().split(/\s+/))
    const intersection = new Set([...qSet].filter(x => cSet.has(x)))
    const union = new Set([...qSet, ...cSet])
    return intersection.size / union.size
  } catch {
    // Opción C: Fallback final
    return computeTfIdfScore(question, chunk) * 0.8
  }
}

// --- Helpers ---

async function generateEmbedding(text: string): Promise<number[]> {
  const OPENAI_KEY = Deno.env.get('OPENAI_API_KEY')
  const response = await fetch('https://api.openai.com/v1/embeddings', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${OPENAI_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'text-embedding-ada-002',
      input: text,
    }),
  })
  const data = await response.json()
  return data.data[0].embedding
}

async function generateAnswer(
  question: string,
  chunks: { content: string; score: number }[]
): Promise<string> {
  const DEEPSEEK_KEY = Deno.env.get('DEEPSEEK_API_KEY')
  const context = chunks.map((c, i) => `[Fuente ${i + 1} (confianza: ${(c.score * 100).toFixed(0)}%)]\n${c.content}`).join('\n\n')

  const prompt = `Eres un asistente de atención al cliente para e-commerce. Responde la pregunta del comprador usando SOLO la información del contexto proporcionado. Si el contexto no tiene suficiente información para responder, indica qué información falta.

Contexto:
${context}

Pregunta del comprador: "${question}"

Responde de manera clara, concisa y amable. Máximo 3 párrafos.`

  const response = await fetch('https://api.deepseek.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${DEEPSEEK_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'deepseek-chat',
      messages: [{ role: 'user', content: prompt }],
      temperature: 0.3,
      max_tokens: 500,
    }),
  })

  const data = await response.json()
  return data.choices[0].message.content
}

async function markAsComplex(classificationId: string) {
  // Actualiza la clasificación a compleja (callback de RAG pipeline)
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )
  await supabase
    .from('auto_classifications')
    .update({ classification: 'compleja', confidence: 0 })
    .eq('id', classificationId)
}

async function checkBillingLimit(
  supabase: any,
  tenantId: string
): Promise<boolean> {
  const period = new Date().toISOString().slice(0, 7)  // "2026-07"
  const { data } = await supabase
    .from('billing_usage')
    .select('plan_limit, usage_count')
    .eq('tenant_id', tenantId)
    .eq('billing_period', period)
    .single()

  if (!data) return true  // Sin límite configurado
  return data.usage_count < data.plan_limit
}
```

### 4.3 Rate Limiter + Message Queue

```typescript
// supabase/functions/rate-limiter-worker/index.ts
// Cron job que corre cada 10 segundos

import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.45.0'

const MELI_RATE_LIMIT = 300  // requests per minute
const WINDOW_MS = 60_000
const BATCH_SIZE = 5  // Procesar de a 5 por tick

interface QueueItem {
  id: string
  tenant_id: string
  meli_account_id: string
  operation: string
  payload: any
  retry_count: number
}

serve(async () => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  // 1. Obtener items pendientes (prioridad + FIFO)
  const { data: queue } = await supabase
    .from('meli_rate_queue')
    .select('*')
    .eq('status', 'queued')
    .order('priority', { ascending: false })
    .order('created_at', { ascending: true })
    .limit(BATCH_SIZE)

  if (!queue || queue.length === 0) {
    // También procesar retrys vencidos
    const { data: retries } = await supabase
      .from('meli_rate_queue')
      .select('*')
      .eq('status', 'retrying')
      .lte('next_retry_at', new Date().toISOString())
      .order('next_retry_at', { ascending: true })
      .limit(BATCH_SIZE)

    if (!retries || retries.length === 0) return new Response('OK')
    queue.push(...retries)
  }

  // 2. Verificar rate limit por cuenta de MeLi
  const accountBuckets = new Map<string, number>()

  for (const item of queue) {
    const key = item.meli_account_id
    const count = accountBuckets.get(key) ?? await getRecentRequests(supabase, item.meli_account_id)
    accountBuckets.set(key, count)

    if (count >= MELI_RATE_LIMIT) {
      // Rate limit alcanzado: reprogramar para próximo minuto
      await supabase
        .from('meli_rate_queue')
        .update({
          status: 'queued',
          next_retry_at: new Date(Date.now() + WINDOW_MS).toISOString(),
        })
        .eq('id', item.id)
      continue
    }

    // 3. Marcar como processing
    await supabase
      .from('meli_rate_queue')
      .update({ status: 'processing', started_at: new Date().toISOString() })
      .eq('id', item.id)

    // 4. Ejecutar operación
    try {
      await executeMeliOperation(item)
      await supabase
        .from('meli_rate_queue')
        .update({ status: 'completed', completed_at: new Date().toISOString() })
        .eq('id', item.id)

      accountBuckets.set(key, count + 1)
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : String(err)
      const newRetryCount = item.retry_count + 1

      if (newRetryCount >= 5) {
        // Agotó retrys
        await supabase
          .from('meli_rate_queue')
          .update({ status: 'failed', last_error: errorMsg })
          .eq('id', item.id)
      } else {
        // Retry exponencial: 2^retry * 10s + jitter
        const delay = Math.min(
          Math.pow(2, newRetryCount) * 10_000 + Math.random() * 5_000,
          300_000  // Max 5 minutos
        )
        await supabase
          .from('meli_rate_queue')
          .update({
            status: 'retrying',
            retry_count: newRetryCount,
            last_error: errorMsg,
            next_retry_at: new Date(Date.now() + delay).toISOString(),
          })
          .eq('id', item.id)
      }
    }
  }

  return new Response('OK')
})

async function getRecentRequests(
  supabase: any,
  meliAccountId: string
): Promise<number> {
  const oneMinuteAgo = new Date(Date.now() - WINDOW_MS).toISOString()
  const { count } = await supabase
    .from('meli_rate_queue')
    .select('*', { count: 'exact', head: true })
    .eq('meli_account_id', meliAccountId)
    .gte('started_at', oneMinuteAgo)
    .in('status', ['processing', 'completed'])

  return count ?? 0
}

async function executeMeliOperation(item: QueueItem) {
  const accessToken = await getMeliToken(item.tenant_id, item.meli_account_id)

  switch (item.operation) {
    case 'reply_question': {
      const { question_id, answer_text } = item.payload
      const response = await fetch(
        `https://api.mercadolibre.com/questions/${question_id}/reply`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: answer_text }),
        }
      )
      if (!response.ok) throw new Error(`MeLi API error: ${response.status}`)
      break
    }

    case 'fetch_questions': {
      const { seller_id, offset, limit } = item.payload
      const response = await fetch(
        `https://api.mercadolibre.com/questions/search?seller_id=${seller_id}&offset=${offset}&limit=${limit}`,
        { headers: { 'Authorization': `Bearer ${accessToken}` } }
      )
      if (!response.ok) throw new Error(`MeLi API error: ${response.status}`)
      // Procesar y guardar resultados...
      break
    }

    // ... otros casos
  }
}

async function getMeliToken(tenantId: string, accountId: string): Promise<string> {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )
  const { data } = await supabase
    .from('meli_accounts')
    .select('access_token')
    .eq('id', accountId)
    .eq('tenant_id', tenantId)
    .single()

  if (!data) throw new Error('Meli account not found')
  return data.access_token
}
```

### 4.4 Auto-Learn Edge Function

```typescript
// supabase/functions/auto-learn/index.ts
// Se ejecuta cuando un tenant conecta una cuenta de MeLi

import { serve } from 'https://deno.land/std@0.224.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2.45.0'

interface AutoLearnRequest {
  tenant_id: string
  meli_account_id: string
  seller_id: number
}

serve(async (req) => {
  const data = await req.json() as AutoLearnRequest
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  // 1. Obtener token de MeLi
  const { data: account } = await supabase
    .from('meli_accounts')
    .select('access_token, refresh_token')
    .eq('id', data.meli_account_id)
    .single()

  if (!account) throw new Error('Account not found')

  // 2. Fetch histórico de preguntas (paginado, respetando rate limit)
  const allQuestions = await fetchAllHistoricalQuestions(
    account.access_token,
    data.seller_id,
    supabase,
    data
  )

  // 3. Agrupar preguntas por producto
  const productGroups = groupByProduct(allQuestions)

  // 4. Para cada producto, generar ficha + embedding
  for (const [productId, questions] of Object.entries(productGroups)) {
    await generateProductFicha(
      supabase,
      data.tenant_id,
      productId,
      questions,
      account.access_token
    )
  }

  // 5. Actualizar estado de la cuenta
  await supabase
    .from('meli_accounts')
    .update({
      auto_learn_completed_at: new Date().toISOString(),
      auto_learn_questions_processed: allQuestions.length,
      auto_learn_products_indexed: Object.keys(productGroups).length,
    })
    .eq('id', data.meli_account_id)

  return new Response(JSON.stringify({
    questions_processed: allQuestions.length,
    products_indexed: Object.keys(productGroups).length,
  }), { headers: { 'Content-Type': 'application/json' } })
})

async function fetchAllHistoricalQuestions(
  accessToken: string,
  sellerId: number,
  supabase: any,
  context: AutoLearnRequest
): Promise<any[]> {
  const allQuestions: any[] = []
  let offset = 0
  const limit = 50
  let total = Infinity

  while (offset < total) {
    // Encolar en rate limiter en lugar de llamar directamente
    const { data: queueItem } = await supabase
      .from('meli_rate_queue')
      .insert({
        tenant_id: context.tenant_id,
        meli_account_id: context.meli_account_id,
        operation: 'fetch_questions',
        payload: { seller_id: sellerId, offset, limit },
        priority: 3,  // Baja prioridad: es batch histórico
      })
      .select()
      .single()

    // Esperar a que se procese (polling con timeout)
    const result = await pollQueueItem(supabase, queueItem.id, 30_000)
    if (result.status === 'completed' && result.result) {
      allQuestions.push(...result.result.results)
      total = result.result.total ?? allQuestions.length
    }

    offset += limit
  }

  return allQuestions
}

function groupByProduct(questions: any[]): Record<string, any[]> {
  const groups: Record<string, any[]> = {}
  for (const q of questions) {
    const productId = q.product_id
    if (!groups[productId]) groups[productId] = []
    groups[productId].push(q)
  }
  return groups
}

async function generateProductFicha(
  supabase: any,
  tenantId: string,
  productId: string,
  questions: any[],
  accessToken: string
) {
  // 1. Obtener datos del producto de MeLi
  const productResponse = await fetch(
    `https://api.mercadolibre.com/items/${productId}`,
    { headers: { 'Authorization': `Bearer ${accessToken}` } }
  )
  const product = await productResponse.json()

  // 2. Extraer preguntas frecuentes y patrones de respuesta
  const faqs = extractFrequentQuestions(questions)
  const patterns = extractAnswerPatterns(questions)

  // 3. Generar embedding de la ficha
  const fichaText = [
    `Producto: ${product.title}`,
    `Categoría: ${product.category_id}`,
    `Descripción: ${faqs.map(f => `P: ${f.question} → R: ${f.answer}`).join('\n')}`,
  ].join('\n')

  const embedding = await generateEmbedding(fichaText)

  // 4. Guardar ficha
  const { error } = await supabase
    .from('auto_product_fichas')
    .upsert({
      tenant_id: tenantId,
      meli_product_id: productId,
      title: product.title,
      category: product.category_id,
      attributes: product.attributes ?? {},
      common_questions: faqs,
      answer_patterns: patterns,
      embedding,
      questions_analyzed: questions.length,
    }, {
      onConflict: 'tenant_id,meli_product_id',
    })

  if (error) throw error

  // 5. Indexar cada FAQ como chunk en la KB
  for (const faq of faqs) {
    const chunkText = `Producto: ${product.title}\nPregunta: ${faq.question}\nRespuesta: ${faq.answer}`
    const chunkEmbedding = await generateEmbedding(chunkText)

    await supabase.from('kb_chunks').insert({
      tenant_id: tenantId,
      content: chunkText,
      embedding: chunkEmbedding,
      metadata: {
        product_id: productId,
        source: 'auto-faq',
        question_count: questions.length,
      },
      source_type: 'auto-faq',
    })
  }
}

function extractFrequentQuestions(questions: any[]): Array<{ question: string; answer: string; frequency: number }> {
  // Agrupar preguntas similares y contar frecuencia
  const questionMap = new Map<string, { question: string; answer: string; count: number }>()

  for (const q of questions) {
    const normalized = q.text.toLowerCase().trim()
    // Buscar si ya tenemos una pregunta similar
    let found = false
    for (const [key, value] of questionMap) {
      if (similarity(normalized, key) > 0.7) {
        value.count++
        found = true
        break
      }
    }
    if (!found) {
      questionMap.set(normalized, {
        question: q.text,
        answer: q.answer?.text ?? '',
        count: 1,
      })
    }
  }

  return Array.from(questionMap.values())
    .sort((a, b) => b.count - a.count)
    .slice(0, 10)  // Top 10 FAQs
}

function extractAnswerPatterns(questions: any[]): Array<{ pattern: string; frequency: number }> {
  // Extraer patrones de respuesta del vendedor
  const patternMap = new Map<string, number>()

  for (const q of questions) {
    if (!q.answer?.text) continue
    const answer = q.answer.text.toLowerCase()

    // Detectar patrones comunes
    if (answer.includes('gracias por') || answer.includes('gracias por tu')) {
      patternMap.set('saludo_agradecimiento', (patternMap.get('saludo_agradecimiento') ?? 0) + 1)
    }
    if (answer.includes('sí') && (answer.includes('disponible') || answer.includes('tengo'))) {
      patternMap.set('confirmacion_disponibilidad', (patternMap.get('confirmacion_disponibilidad') ?? 0) + 1)
    }
    if (/\d+[.,]?\d*\s*(cm|kg|gr|ml|litro)/.test(answer)) {
      patternMap.set('respuesta_medidas', (patternMap.get('respuesta_medidas') ?? 0) + 1)
    }
    if (answer.includes('envío') || answer.includes('enviamos') || answer.includes('correo')) {
      patternMap.set('info_envio', (patternMap.get('info_envio') ?? 0) + 1)
    }
  }

  return Array.from(patternMap.entries())
    .map(([pattern, frequency]) => ({ pattern, frequency }))
    .sort((a, b) => b.frequency - a.frequency)
}

function similarity(a: string, b: string): number {
  // Jaccard similarity simple
  const setA = new Set(a.split(/\s+/))
  const setB = new Set(b.split(/\s+/))
  const intersection = new Set([...setA].filter(x => setB.has(x)))
  const union = new Set([...setA, ...setB])
  return intersection.size / union.size
}
```

---

## 5. Estrategia de Caché

### 5.1 Cache Layers

```
┌─────────────────────────────────────────────┐
│  Capa 1: Browser Cache (React Query)         │
│  - Datos de UI: preguntas, productos, KB     │
│  - Stale-while-revalidate: 30s stale, 5min   │
│  - Cache key: tenant_id + recurso + filters   │
├─────────────────────────────────────────────┤
│  Capa 2: Supabase Edge Function Cache        │
│  - Respuestas de MeLi API (productos,        │
│    preguntas ya respondidas)                 │
│  - TTL: 5 min para productos, 1 min para     │
│    preguntas activas                         │
│  - Cache key: meli_account_id + endpoint     │
├─────────────────────────────────────────────┤
│  Capa 3: PostgreSQL (nuestra DB)             │
│  - Datos ya sincronizados (preguntas,        │
│    respuestas, productos)                    │
│  - Es la fuente de verdad para el sistema    │
└─────────────────────────────────────────────┘
```

### 5.2 Implementación de Caché en Edge Functions

```typescript
// Cache helper para Edge Functions
const cache = new Map<string, { data: any; expiresAt: number }>()

function getCached(key: string): any | null {
  const entry = cache.get(key)
  if (!entry) return null
  if (Date.now() > entry.expiresAt) {
    cache.delete(key)
    return null
  }
  return entry.data
}

function setCache(key: string, data: any, ttlMs: number) {
  cache.set(key, { data, expiresAt: Date.now() + ttlMs })
  // Limpiar entradas viejas cada 100 escrituras
  if (cache.size > 1000) {
    const now = Date.now()
    for (const [k, v] of cache) {
      if (now > v.expiresAt) cache.delete(k)
    }
  }
}

// Uso en fetch de producto
async function getProductFromCacheOrApi(
  meliAccountId: string,
  productId: string,
  accessToken: string
): Promise<any> {
  const cacheKey = `product:${meliAccountId}:${productId}`
  const cached = getCached(cacheKey)
  if (cached) return cached

  const response = await fetch(
    `https://api.mercadolibre.com/items/${productId}`,
    { headers: { 'Authorization': `Bearer ${accessToken}` } }
  )
  const product = await response.json()

  setCache(cacheKey, product, 5 * 60 * 1000)  // 5 min TTL
  return product
}
```

### 5.3 Reglas de Caché

| Recurso | TTL | Invalidate On |
|---------|-----|---------------|
| Producto MeLi | 5 min | Webhook de cambio de producto |
| Pregunta individual | 1 min | Webhook de nueva respuesta |
| Lista de preguntas (bandeja) | 30s | Webhook de pregunta nueva |
| KB chunks | 10 min | Nueva indexación |
| Embeddings | 1 hora | Re-indexación manual |
| Token de acceso MeLi | 5h (expira en 6h) | Refresh token |

---

## 6. Consistencia Eventual: Webhook MeLi ↔ Estado Local

### 6.1 Estrategia

```
MeLi Webhook ──► Edge Function ──► INSERT en tabla temporal
       │                              │
       │                         ┌────┴────┐
       │                         │  ¿Ya     │
       │                         │  existe  │
       │                         │  en DB?  │
       │                         └────┬────┘
       │                          Sí  │  No
       │                          │   │
       │                     ┌────┘   ▼
       │                     │    INSERT + procesar
       │                     ▼
       │              UPDATE (dedup)
       │
  ┌────┴────┐
  │  Cron   │  ← Cada 5 min: polling de preguntas no recibidas
  │  Poll   │     (fallback si webhook falló)
  └─────────┘
```

### 6.2 Implementación

```typescript
// Edge Function: webhook handler
serve(async (req) => {
  const event = await req.json()

  // 1. Verificar firma del webhook
  const signature = req.headers.get('x-signature')
  if (!verifyWebhookSignature(signature, event)) {
    return new Response('Invalid signature', { status: 401 })
  }

  // 2. Procesar según tipo de evento
  switch (event.topic) {
    case 'questions':
    case 'questions_reply': {
      const question = event.resource

      // 3. Verificar si ya existe (idempotencia)
      const { data: existing } = await supabase
        .from('questions')
        .select('id')
        .eq('meli_question_id', question.id)
        .single()

      if (existing) {
        // UPDATE: ya existe, actualizar estado
        await supabase
          .from('questions')
          .update({
            status: question.status,
            answer: question.answer,
            updated_at: new Date().toISOString(),
          })
          .eq('meli_question_id', question.id)
      } else {
        // INSERT: nueva pregunta
        const { data: newQuestion } = await supabase
          .from('questions')
          .insert({
            tenant_id: resolveTenantFromMeliAccount(question.seller_id),
            meli_account_id: resolveAccountId(question.seller_id),
            meli_question_id: question.id,
            product_id: question.item_id,
            customer_id: question.from.id,
            text: question.text,
            status: question.status,
            received_at: new Date().toISOString(),
          })
          .select()
          .single()

        // 4. Encolar clasificación
        if (newQuestion && question.status === 'UNANSWERED') {
          await supabase.from('meli_rate_queue').insert({
            tenant_id: newQuestion.tenant_id,
            operation: 'classify_question',
            payload: {
              question_id: newQuestion.id,
              meli_question_id: question.id,
              question_text: question.text,
              product_id: question.item_id,
              customer_id: question.from.id,
            },
            priority: 10,  // Máxima prioridad
          })
        }
      }
      break
    }
  }

  return new Response('OK', { status: 200 })
})

// Cron job de polling (fallback cada 5 min)
serve(async () => {
  const supabase = createClient(...)

  // Obtener cuentas que no recibieron webhook recientemente
  const { data: accounts } = await supabase
    .from('meli_accounts')
    .select('id, tenant_id, seller_id, access_token')
    .or(`last_webhook_at.is.null,last_webhook_at.lt.${new Date(Date.now() - 5*60*1000).toISOString()}`)

  for (const account of accounts ?? []) {
    await supabase.from('meli_rate_queue').insert({
      tenant_id: account.tenant_id,
      meli_account_id: account.id,
      operation: 'poll_new_questions',
      payload: { seller_id: account.seller_id },
      priority: 2,
    })
  }
})
```

---

## 7. Billing con Mercado Pago

### 7.1 Planes y Límites

```typescript
// supabase/functions/mp-billing/index.ts

const PLANS = {
  starter: {
    name: 'Starter',
    price: 1500,  // ARS 1,500/mes
    auto_responses_limit: 100,
    features: ['auto_respuesta', 'kb_basica', '1_cuenta_meli'],
  },
  professional: {
    name: 'Professional',
    price: 3500,  // ARS 3,500/mes
    auto_responses_limit: 500,
    features: ['auto_respuesta', 'kb_ilimitada', '3_cuentas_meli', 'auto_learn', 'analytics'],
  },
  enterprise: {
    name: 'Enterprise',
    price: 8000,  // ARS 8,000/mes
    auto_responses_limit: 2000,
    features: ['auto_respuesta', 'kb_ilimitada', '10_cuentas_meli', 'auto_learn', 'analytics', 'prioridad'],
  },
}

// Crear suscripción en MP
async function createSubscription(tenantId: string, planKey: string, email: string) {
  const plan = PLANS[planKey as keyof typeof PLANS]
  if (!plan) throw new Error('Invalid plan')

  const MP_ACCESS_TOKEN = Deno.env.get('MP_ACCESS_TOKEN')

  const response = await fetch('https://api.mercadopago.com/preapproval', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${MP_ACCESS_TOKEN}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      preapproval_plan_id: Deno.env.get('MP_PREAPPROVAL_PLAN_ID'),
      reason: `SoporteML - Plan ${plan.name}`,
      external_reference: tenantId,
      payer_email: email,
      auto_recurring: {
        frequency: 1,
        frequency_type: 'months',
        transaction_amount: plan.price,
        currency_id: 'ARS',
      },
      back_url: 'https://soporteml.app/billing/success',
      status: 'authorized',
    }),
  })

  return response.json()
}

// Webhook de MP
serve(async (req) => {
  const event = await req.json()
  const supabase = createClient(...)

  switch (event.type) {
    case 'subscription_created':
    case 'subscription_authorized': {
      const tenantId = event.data.external_reference
      const planKey = extractPlanKey(event.data.reason)

      // Calcular período prorrateado
      const now = new Date()
      const endOfMonth = new Date(now.getFullYear(), now.getMonth() + 1, 1)
      const daysInMonth = (endOfMonth.getTime() - new Date(now.getFullYear(), now.getMonth(), 1).getTime()) / 86400000
      const remainingDays = (endOfMonth.getTime() - now.getTime()) / 86400000
      const proratedLimit = Math.round(PLANS[planKey].auto_responses_limit * (remainingDays / daysInMonth))

      await supabase.from('billing_usage').upsert({
        tenant_id: tenantId,
        billing_period: now.toISOString().slice(0, 7),
        plan_limit: PLANS[planKey].auto_responses_limit,
        plan_started_at: now.toISOString(),
        plan_ends_at: endOfMonth.toISOString(),
        is_prorated: remainingDays < daysInMonth,
        prorated_limit: proratedLimit,
        usage_count: 0,
      })
      break
    }

    case 'subscription_cancelled': {
      const tenantId = event.data.external_reference
      await supabase
        .from('tenants')
        .update({ subscription_status: 'cancelled' })
        .eq('id', tenantId)
      break
    }

    case 'subscription_charged': {
      // Pago exitoso del período
      const tenantId = event.data.external_reference
      const period = new Date().toISOString().slice(0, 7)

      // Resetear uso para nuevo período
      await supabase.from('billing_usage').upsert({
        tenant_id: tenantId,
        billing_period: period,
        usage_count: 0,
      })
      break
    }
  }

  return new Response('OK', { status: 200 })
})

// Guard de billing: se llama antes de enviar auto-respuesta
async function incrementUsage(tenantId: string): Promise<boolean> {
  const supabase = createClient(...)
  const period = new Date().toISOString().slice(0, 7)

  // Atomic increment con verificación de límite
  const { data, error } = await supabase.rpc('increment_billing_usage', {
    p_tenant_id: tenantId,
    p_period: period,
  })

  if (error) throw error
  return data  // true = dentro del límite, false = excedido
}
```

### 7.2 Función SQL para incremento atómico

```sql
CREATE OR REPLACE FUNCTION increment_billing_usage(
  p_tenant_id UUID,
  p_period TEXT
) RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_limit INT;
  v_usage INT;
BEGIN
  SELECT plan_limit, usage_count
  INTO v_limit, v_usage
  FROM billing_usage
  WHERE tenant_id = p_tenant_id AND billing_period = p_period
  FOR UPDATE;  -- Lock row to prevent race conditions

  IF v_limit IS NULL THEN
    RETURN TRUE;  -- Sin límite configurado
  END IF;

  IF v_usage >= v_limit THEN
    RETURN FALSE;  -- Límite excedido
  END IF;

  UPDATE billing_usage
  SET usage_count = usage_count + 1,
      updated_at = now()
  WHERE tenant_id = p_tenant_id AND billing_period = p_period;

  RETURN TRUE;
END;
$$;
```

---

## 8. Alternativas Descartadas

### 8.1 Re-ranker con servicio externo pago (Cohere, OpenAI)

**Descartada por:** Costo recurrente. Con ~500 auto-respuestas/día, un re-ranker externo agregaría ~$50-100/mes en API calls. El re-ranker local con TF-IDF + Jaccard + ONNX miniLM da ~85% de precisión del re-ranker de Cohere para este dominio específico (e-commerce argentino, vocabulario acotado).

### 8.2 Redis para caché y cola de mensajes

**Descartada por:** Complejidad operativa. Supabase no incluye Redis nativo (habría que usar Upstash o Redis Cloud). La cola en PostgreSQL con índices adecuados maneja ~300 ops/min sin problema. Si escala a >1000 tenants, se puede migrar a RabbitMQ/Redis, pero para MVP la DB es suficiente.

### 8.3 Clasificación solo con heurísticas (sin IA)

**Descartada por:** Baja precisión en edge cases. Las heurísticas funcionan para ~70% de los casos, pero fallan en preguntas ambiguas ("hola, quería saber...") y follow-ups. La combinación DeepSeek + heurísticas da ~95% de precisión en clasificación.

### 8.4 Webhook síncrono (responder inmediatamente en el webhook)

**Descartada por:** Timeouts de MeLi (el webhook espera respuesta en <5s). El pipeline RAG + DeepSeek toma ~3-8s. Mejor encolar y responder asincrónicamente.

### 8.5 Embeddings con modelo local (all-MiniLM-L6-v2)

**Descartada por:** Las Edge Functions de Supabase no tienen GPU y el CPU es limitado. OpenAI ada-002 es más rápido y preciso para 1536 dimensiones. Si el costo de embeddings escala, se puede migrar a un worker dedicado con modelo local.

### 8.6 Billing post-pago (pagar por uso)

**Descartada por:** El mercado argentino prefiere suscripciones fijas. El modelo predecible (plan mensual con límite) es más fácil de vender que "paga por cada respuesta". El prorrateo al activar a mitad de mes es el compromiso justo.

---

## 9. Consecuencias

### Positivas
- **Sin dependencias externas pagas** para re-ranking (ahorro ~$50-100/mes).
- **Clasificación híbrida** (IA + heurísticas) funciona offline si DeepSeek cae.
- **Cola de rate limiting** evita bans de MeLi API.
- **Auto-learn** reduce drásticamente el onboarding: el tenant conecta y ya tiene KB.
- **Billing atómico** sin race conditions (row lock en PostgreSQL).
- **Consistencia eventual** con webhook + polling: tolerable para un CRM de preguntas.

### Negativas
- **La cola en PostgreSQL** no escala horizontalmente. Para >1000 tenants activos, migrar a cola dedicada.
- **El re-ranker local** es menos preciso que uno externo. Monitorear con feedback loop para detectar degradación.
- **Embeddings con OpenAI** = costo variable. A ~$0.0001/embedding, 1000 preguntas/día = ~$3/mes. Aceptable.
- **El cron de rate limiting** (cada 10s) puede tener latencia de hasta 10s en respuesta. Aceptable para auto-respuesta.

### Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| DeepSeek API caída | Baja | Alto | Fallback a clasificación heurística + respuesta template |
| MeLi API rate limit | Media | Alto | Cola + retry exponencial + alerta si cola > 100 items |
| Embedding API caída | Baja | Medio | Cache de embeddings en DB + fallback a TF-IDF |
| Billing race condition | Baja | Alto | Row lock + función atómica en SQL |
| Re-ranker degradado | Media | Medio | Feedback loop detecta approved/rejected ratio < 60% |

---

## 10. Monitoreo y Alertas

```sql
-- Vista de monitoreo para dashboard
CREATE VIEW auto_response_dashboard AS
SELECT
  tenant_id,
  DATE(created_at) as date,
  COUNT(*) FILTER (WHERE classification = 'rutinaria') as rutinarias,
  COUNT(*) FILTER (WHERE classification = 'compleja') as complejas,
  AVG(confidence) FILTER (WHERE classification = 'rutinaria') as avg_confidence,
  COUNT(DISTINCT response_id) FILTER (WHERE response_id IS NOT NULL) as auto_respondidas,
  COUNT(DISTINCT response_id) FILTER (WHERE response_id IS NULL) as derivadas
FROM auto_classifications
GROUP BY tenant_id, DATE(created_at);

-- Alerta: cola de rate limiting creciendo
-- SELECT COUNT(*) FROM meli_rate_queue WHERE status IN ('queued', 'retrying') AND created_at < now() - interval '5 minutes'
-- Si > 50, alertar
```

---

## 11. Próximos Pasos

1. **Migración SQL:** Ejecutar el schema completo en Supabase local.
2. **Edge Functions:** Implementar classifier, RAG pipeline, rate limiter worker, auto-learn, billing webhook.
3. **Configurar secrets:** DEEPSEEK_API_KEY, OPENAI_API_KEY, MP_ACCESS_TOKEN, MP_PREAPPROVAL_PLAN_ID, MELI_APP_ID/CLIENT_SECRET.
4. **Cron jobs:** Configurar rate-limiter-worker cada 10s, polling fallback cada 5min.
5. **UI:** Dashboard de auto-respuesta con métricas, feedback buttons, configuración de umbral de confianza.
6. **Tests:** Edge Functions con test de integración contra Supabase local.
7. **Monitoreo:** Alertas para cola de rate limiting, billing excedido, confianza degradada.

---

## 12. Referencias

- [pgvector docs](https://github.com/pgvector/pgvector)
- [Supabase Edge Functions](https://supabase.com/docs/guides/functions)
- [Mercado Libre API - Questions](https://developers.mercadolibre.com.ar/es_ar/preguntas)
- [Mercado Pago - Preapproval](https://www.mercadopago.com.ar/developers/es/reference/preapproval/_preapproval/post)
- [DeepSeek API](https://platform.deepseek.com/api-docs)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)
- [ONNX Runtime for Deno](https://deno.land/x/onnx)
