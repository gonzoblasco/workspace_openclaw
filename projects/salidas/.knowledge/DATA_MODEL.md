# DATA_MODEL.md — Quedamos

> Esquemas de base de datos. Output de Fase 0.2.

## Convenciones

- **Timestamps:** Siempre `created_at` y `updated_at` con `DEFAULT now()`
- **IDs:** UUID v4 generados por `gen_random_uuid()`
- **Soft delete:** `deleted_at TIMESTAMPTZ` nullable en lugar de DELETE
- **RLS:** Row Level Security habilitado en todas las tablas

## Tablas

### users

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  apodo VARCHAR(30) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  bio TEXT DEFAULT '',
  actividades_fav TEXT[] DEFAULT '{}', -- array de strings: 'cine', 'bar', 'cafe', 'baile', 'almuerzo', 'caminata', 'teatro', etc.
  big_five_vector REAL[5] NOT NULL, -- [apertura, responsabilidad, extraversion, amabilidad, neuroticismo]
  onboarding_completo BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  deleted_at TIMESTAMPTZ
);

-- Índices
CREATE INDEX idx_users_apodo ON users(apodo);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_actividades ON users USING GIN(actividades_fav);
```

### lugares

```sql
CREATE TABLE lugares (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre VARCHAR(255) NOT NULL,
  direccion VARCHAR(255) NOT NULL,
  tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('restaurante', 'cine', 'bar', 'cafe', 'teatro', 'otro')),
  capacidad_comida SMALLINT DEFAULT 0, -- cupo máximo para salidas de comida
  capacidad_cine SMALLINT DEFAULT 0,   -- cupo máximo para salidas de cine
  capacidad_general SMALLINT DEFAULT 0, -- cupo máximo para otros tipos
  ubicacion GEOGRAPHY(POINT), -- coordenadas para mapa
  activo BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_lugares_tipo ON lugares(tipo);
CREATE INDEX idx_lugares_activo ON lugares(activo);
CREATE INDEX idx_lugares_ubicacion ON lugares USING GIST(ubicacion);
```

### salidas

```sql
CREATE TABLE salidas (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lugar_id UUID NOT NULL REFERENCES lugares(id),
  actividad VARCHAR(50) NOT NULL, -- 'cine', 'bar', 'cafe', 'baile', 'almuerzo', 'caminata', 'teatro', 'reunion', 'otro'
  actividad_personalizada VARCHAR(100), -- si actividad = 'otro'
  fecha DATE NOT NULL,
  hora TIME NOT NULL,
  cupo_max SMALLINT NOT NULL CHECK (cupo_max BETWEEN 2 AND 100),
  asistentes_actuales SMALLINT DEFAULT 0,
  descripcion TEXT DEFAULT '',
  etiquetas TEXT[] DEFAULT '{}', -- tags libres: 'musica', 'cerveza-artesanal', 'chill', etc.
  precio_estimado VARCHAR(50), -- 'gratis', '$$', '$$$', etc.
  estado VARCHAR(20) DEFAULT 'abierta' CHECK (estado IN ('abierta', 'cerrada', 'cancelada', 'completada')),
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now(),
  deleted_at TIMESTAMPTZ
);

-- Índices
CREATE INDEX idx_salidas_fecha ON salidas(fecha);
CREATE INDEX idx_salidas_actividad ON salidas(actividad);
CREATE INDEX idx_salidas_estado ON salidas(estado);
CREATE INDEX idx_salidas_lugar ON salidas(lugar_id);
CREATE INDEX idx_salidas_etiquetas ON salidas USING GIN(etiquetas);
```

### participantes

```sql
CREATE TABLE participantes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  salida_id UUID NOT NULL REFERENCES salidas(id) ON DELETE CASCADE,
  user_id UUID NOT NULL REFERENCES users(id),
  estado VARCHAR(20) DEFAULT 'confirmado' CHECK (estado IN ('confirmado', 'no_show', 'cancelado')),
  joined_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(salida_id, user_id) -- un usuario por salida
);

-- Índices
CREATE INDEX idx_participantes_salida ON participantes(salida_id);
CREATE INDEX idx_participantes_user ON participantes(user_id);
```

### feedback

```sql
CREATE TABLE feedback (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  salida_id UUID NOT NULL REFERENCES salidas(id) ON DELETE CASCADE,
  de_user_id UUID NOT NULL REFERENCES users(id),
  para_user_id UUID NOT NULL REFERENCES users(id),
  compatibility_score SMALLINT NOT NULL CHECK (compatibility_score BETWEEN 1 AND 10),
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(salida_id, de_user_id, para_user_id) -- un feedback por par por salida
);

-- Índices
CREATE INDEX idx_feedback_salida ON feedback(salida_id);
CREATE INDEX idx_feedback_de ON feedback(de_user_id);
CREATE INDEX idx_feedback_para ON feedback(para_user_id);
```

### user_activity_history

```sql
CREATE TABLE user_activity_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  actividad VARCHAR(50) NOT NULL,
  salida_id UUID REFERENCES salidas(id),
  rating SMALLINT CHECK (rating BETWEEN 1 AND 5), -- implícito: qué tan bien la pasó
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Índices
CREATE INDEX idx_uah_user ON user_activity_history(user_id);
CREATE INDEX idx_uah_actividad ON user_activity_history(actividad);
```

### weekly_suggestions

```sql
CREATE TABLE weekly_suggestions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  semana VARCHAR(7) NOT NULL, -- ISO week: '2026-W30'
  salida_ids UUID[] NOT NULL, -- array de hasta 5 salidas
  generada_en TIMESTAMPTZ DEFAULT now(),
  vista_en TIMESTAMPTZ, -- cuándo el usuario vio las sugerencias
  UNIQUE(user_id, semana)
);

-- Índices
CREATE INDEX idx_ws_user_semana ON weekly_suggestions(user_id, semana);
```

### trust_scores

```sql
CREATE TABLE trust_scores (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) UNIQUE,
  asistencia_rate REAL DEFAULT 1.0, -- 0.0 a 1.0
  total_salidas SMALLINT DEFAULT 0,
  no_shows SMALLINT DEFAULT 0,
  reportes_recibidos SMALLINT DEFAULT 0,
  reportes_hechos SMALLINT DEFAULT 0,
  updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_trust_user ON trust_scores(user_id);
```

### reportes

```sql
CREATE TABLE reportes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  reportador_id UUID NOT NULL REFERENCES users(id),
  reportado_id UUID NOT NULL REFERENCES users(id),
  salida_id UUID REFERENCES salidas(id),
  motivo VARCHAR(50) NOT NULL CHECK (motivo IN ('comportamiento_inapropiado', 'no_show', 'spam', 'acoso', 'otro')),
  descripcion TEXT,
  estado VARCHAR(20) DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'revisado', 'desestimado')),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_reportes_estado ON reportes(estado);
CREATE INDEX idx_reportes_reportado ON reportes(reportado_id);
```

## Vistas Útiles

### vista_salidas_con_asistentes

```sql
CREATE VIEW vista_salidas_con_asistentes AS
SELECT
  s.*,
  l.nombre as lugar_nombre,
  l.direccion as lugar_direccion,
  l.tipo as lugar_tipo,
  COUNT(p.id) FILTER (WHERE p.estado = 'confirmado') as asistentes_confirmados,
  s.cupo_max - COUNT(p.id) FILTER (WHERE p.estado = 'confirmado') as cupo_disponible
FROM salidas s
JOIN lugares l ON l.id = s.lugar_id
LEFT JOIN participantes p ON p.salida_id = s.id
WHERE s.estado = 'abierta'
GROUP BY s.id, l.nombre, l.direccion, l.tipo;
```

## RLS Policies (conceptual)

```sql
-- users: cada uno ve su propio perfil, ve apodos de otros
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "usuarios_ven_su_perfil_completo"
  ON users FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "usuarios_ven_apodos_publicos"
  ON users FOR SELECT
  USING (true)
  WITH CHECK (false); -- solo lectura, no pueden ver datos sensibles

-- lugares: todos ven lugares activos
ALTER TABLE lugares ENABLE ROW LEVEL SECURITY;

CREATE POLICY "todos_ven_lugares_activos"
  ON lugares FOR SELECT
  USING (activo = true);

-- salidas: todos ven salidas abiertas
ALTER TABLE salidas ENABLE ROW LEVEL SECURITY;

CREATE POLICY "todos_ven_salidas_abiertas"
  ON salidas FOR SELECT
  USING (estado = 'abierta');

-- participantes: todos ven, solo el usuario se agrega/elimina
ALTER TABLE participantes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "todos_ven_participantes"
  ON participantes FOR SELECT
  USING (true);

CREATE POLICY "usuario_se_agrega"
  ON participantes FOR INSERT
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "usuario_se_elimina"
  ON participantes FOR DELETE
  USING (user_id = auth.uid());
```

## Funciones PostgreSQL

### calcular_compatibilidad (base)

```sql
CREATE OR REPLACE FUNCTION calcular_compatibilidad(
  vector_a REAL[5],
  vector_b REAL[5]
) RETURNS REAL AS $$
DECLARE
  dot_product REAL;
  norm_a REAL;
  norm_b REAL;
BEGIN
  -- Distancia coseno: 1 - cos(θ)
  -- Más cercano a 1 = más compatible
  dot_product := vector_a[1]*vector_b[1] + vector_a[2]*vector_b[2]
               + vector_a[3]*vector_b[3] + vector_a[4]*vector_b[4]
               + vector_a[5]*vector_b[5];
  norm_a := sqrt(vector_a[1]^2 + vector_a[2]^2 + vector_a[3]^2 + vector_a[4]^2 + vector_a[5]^2);
  norm_b := sqrt(vector_b[1]^2 + vector_b[2]^2 + vector_b[3]^2 + vector_b[4]^2 + vector_b[5]^2);
  RETURN (dot_product / (norm_a * norm_b) + 1) / 2; -- normalizado a 0-1
END;
$$ LANGUAGE plpgsql IMMUTABLE;
```
