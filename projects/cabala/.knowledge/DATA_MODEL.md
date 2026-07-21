# DATA_MODEL — Cábala

## Entries

Tabla principal. Una entrada = una foto + metadata.

```sql
CREATE TABLE entries (
  id TEXT PRIMARY KEY,              -- UUID
  photo_path TEXT NOT NULL,          -- Ruta al archivo de foto comprimida
  title TEXT,                        -- Título opcional
  description TEXT,                  -- Texto descriptivo opcional
  latitude REAL,                     -- Latitud (nullable si modo incógnito)
  longitude REAL,                    -- Longitud (nullable si modo incógnito)
  address TEXT,                      -- Dirección reversa (cache)
  audio_path TEXT,                   -- Ruta al archivo de audio (nullable)
  is_incognito INTEGER DEFAULT 0,    -- 1 = sin ubicación guardada
  created_at TEXT NOT NULL,          -- ISO 8601
  updated_at TEXT NOT NULL           -- ISO 8601
);

CREATE INDEX idx_entries_created_at ON entries(created_at);
CREATE INDEX idx_entries_location ON entries(latitude, longitude);
```

## Tags

Tags libres, muchos-a-muchos con entries.

```sql
CREATE TABLE tags (
  id TEXT PRIMARY KEY,              -- UUID
  name TEXT NOT NULL UNIQUE,        -- Nombre del tag (lowercase)
  created_at TEXT NOT NULL
);

CREATE TABLE entry_tags (
  entry_id TEXT NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
  tag_id TEXT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (entry_id, tag_id)
);

CREATE INDEX idx_entry_tags_entry ON entry_tags(entry_id);
CREATE INDEX idx_entry_tags_tag ON entry_tags(tag_id);
```

## Notifications

Configuración de notificaciones del usuario.

```sql
CREATE TABLE notification_config (
  id INTEGER PRIMARY KEY DEFAULT 1,  -- Single row
  daily_count INTEGER NOT NULL DEFAULT 3,  -- Cantidad de notificaciones por día
  time_windows TEXT NOT NULL DEFAULT '["09:00-12:00","13:00-16:00","18:00-21:00"]',
    -- JSON array de ventanas de tiempo
  enabled INTEGER NOT NULL DEFAULT 1
);
```

## Challenges

Desafíos de fotografía.

```sql
CREATE TABLE challenges (
  id TEXT PRIMARY KEY,              -- UUID
  name TEXT NOT NULL,               -- "30 días en B/N"
  description TEXT NOT NULL,
  duration_days INTEGER NOT NULL,    -- Duración en días
  prompt_template TEXT,              -- Prompt opcional por día
  is_active INTEGER DEFAULT 0,
  started_at TEXT,
  created_at TEXT NOT NULL
);

CREATE TABLE challenge_entries (
  id TEXT PRIMARY KEY,
  challenge_id TEXT NOT NULL REFERENCES challenges(id) ON DELETE CASCADE,
  entry_id TEXT NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
  day_number INTEGER NOT NULL,       -- Día del desafío (1-indexed)
  created_at TEXT NOT NULL,
  UNIQUE(challenge_id, day_number)
);
```

## Settings

Configuración general de la app.

```sql
CREATE TABLE settings (
  id INTEGER PRIMARY KEY DEFAULT 1,  -- Single row
  photo_quality INTEGER NOT NULL DEFAULT 70,  -- 1-100, calidad JPEG
  photo_max_width INTEGER NOT NULL DEFAULT 1080,  -- Max width en px
  theme TEXT NOT NULL DEFAULT 'system',  -- 'light' | 'dark' | 'system'
  language TEXT NOT NULL DEFAULT 'es',
  backup_enabled INTEGER DEFAULT 0,
  backup_provider TEXT,              -- 'icloud' | 'googledrive'
  last_backup_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

## Relaciones

```
entries 1──* entry_tags *──1 tags
entries 1──* challenge_entries *──1 challenges
notification_config (single row)
settings (single row)
```

## Notas

- **IDs:** UUID v4 generados en cliente. No hay backend, no hay riesgo de colisión.
- **Fechas:** ISO 8601 en texto. SQLite no tiene tipo datetime nativo, y texto ISO es ordenable y portable.
- **Archivos multimedia:** Se guardan en el filesystem de la app (expo-file-system.documentDirectory). SQLite guarda rutas relativas.
- **Tags en lowercase:** Para evitar duplicados por capitalización.
- **Single row tables:** notification_config y settings usan `id INTEGER PRIMARY KEY DEFAULT 1` para forzar una sola fila.
