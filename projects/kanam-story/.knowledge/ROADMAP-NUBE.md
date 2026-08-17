# ROADMAP — Kanam Story: Salto a la Nube (Supabase → Vercel)

> **Estado:** PLANIFICADO (2026-08-17). No se ejecuta todavía. Kanam Story sigue local-first.
> Este documento es referencia para cuando Gonzo decida dar el salto.

## Decisión (2026-08-17)

**Kanam Story NO será open source.** Se trabaja en local (solo Gonzo + Kanam) hasta que sea el
momento de evolucionar a la nube. El open source queda descartado (o se reconsidera mucho más
adelante, si aporta).

**Implicaciones:**
- El feature flag del co-writer (`NEXT_PUBLIC_ENABLE_COWRITER`) ya no es urgente (era para
  diferenciar open source vs pago). Se deja habilitado siempre por ahora.
- El README no necesita la sección BYOK para público externo (sirve como doc interna).
- La estrategia de 3 públicos se simplifica: por ahora es solo "producto local".

## El camino (por pasos, sin saltos)

> Orden definido por Gonzo: DB → middleware → auth → después Vercel.

### Paso 1 — Pasar las bases de datos a Supabase
- Migrar el data model de IndexedDB a Supabase (Postgres).
- El schema ya está definido en `.knowledge/DATA_MODEL.md`:
  Project, Chapter, Scene, Beat, Character, WorldEntity, StoryBible, Conversation, Message, ContentAction.
- **Decisión pendiente:** ¿Supabase reemplaza a IndexedDB (todo en la nube), o conviven
  (IndexedDB como cache local + Supabase como fuente de verdad con sync)?
  - **Recomendación de Kanam:** conviven. El local-first es el diferenciador (offline, privacidad);
    Supabase agrega el sync. Pero es decisión de Gonzo.

### Paso 2 — Crear el middleware
- La capa de API / Edge Functions que conecta el frontend con Supabase.
- Reemplaza/convive con las rutas API actuales (`/api/ollama`, `/api/ollama/models`).

### Paso 3 — Modo login
- Supabase Auth: registro, login, sesión.
- Multi-usuario (cada usuario con sus proyectos aislados).

### Paso 4 — Después (a otra cosa)
- Vercel para deploy.
- Monetización (cuando corresponda).

## Estado actual del proyecto (referencia)

- **v0.17.0** (2026-08-17) - Fase A completa + OpenSpec inicializado + 9 specs auditados.
- **382 tests**, build + tsc + lint verdes.
- **9 specs de OpenSpec** (47 requirements): co-writer, editor, outline, biblia, brújula,
  persistencia, personajes, mundo, brainstorm. Todos auditados.
- **Pendiente único:** filtros de outline por POV/tense (decisión de diseño).

## Notas

- Este roadmap es de **referencia futura**. No se ejecuta hasta que Gonzo lo indique.
- Cuando se arranque el Paso 1, actualizar este documento con el progreso.
