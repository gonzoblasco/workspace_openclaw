# ARCHITECTURE.md — Quedamos

> Decisiones arquitectónicas tempranas. Output de Fase 0.2.

## Stack Definitivo

| Capa | Tecnología | Justificación |
|---|---|---|
| Frontend | Next.js 15 (App Router) + Tailwind + shadcn/ui | Stack conocido, PWA nativa, SSR para SEO, RSC para performance |
| PWA | next-pwa + Service Worker + Web Push API | Instalación en home screen, notificaciones push, offline básico |
| Backend | Supabase | Auth, PostgreSQL, Realtime, Edge Functions — todo en uno |
| Base de datos | PostgreSQL (via Supabase) | Relacional, maduro, row-level security, funciones nativas |
| Matching engine | Supabase Edge Function (Deno/TypeScript) | Mismo lenguaje que frontend, cerca de la DB, serverless |
| Notificaciones | Supabase Realtime + Web Push API | Tiempo real sin infra adicional |
| Hosting | Vercel (frontend) + Supabase (backend) | Gratis para empezar, escalable después |
| CI/CD | GitHub Actions | Linting, type-check, tests, deploy automático |

## Patrones Arquitectónicos

### Frontend
- **App Router** con layout anidado (auth, app, admin)
- **Server Components** para datos públicos (feed de salidas)
- **Client Components** para interactividad (unirse, crear, feedback)
- **Server Actions** para mutaciones (crear salida, enviar feedback)
- **Route Handlers** para webhooks y endpoints de matching

### Backend (Edge Functions)
- **Arquitectura hexagonal** en cada Edge Function
  - **Domain:** Lógica de negocio pura (matching, sugerencias)
  - **Infrastructure:** Acceso a DB, servicios externos
  - **API:** Handlers HTTP
- **Row Level Security (RLS)** en Supabase para control de acceso a nivel DB

### Base de Datos
- **Esquema relacional** con migraciones versionadas
- **RLS policies** para que cada usuario vea solo lo que debe
- **Funciones PostgreSQL** para cálculos pesados (distancia coseno de vectores)

## Diagrama C4

### Contexto (Nivel 1)

```
[Usuario con celular] ←→ [PWA Quedamos (Next.js)]
                              ↕
                       [Supabase]
                        ↕     ↕
                   [PostgreSQL] [Edge Functions]
                        ↕
                   [Vercel Hosting]
```

### Contenedores (Nivel 2)

```
[PWA - Next.js 15]
  ├── App Router (páginas, layouts)
  ├── Server Components (feed, perfiles)
  ├── Client Components (forms, interactividad)
  ├── Service Worker (PWA, push, offline)
  └── Server Actions (mutaciones)

[Supabase]
  ├── Auth (email, Google OAuth)
  ├── PostgreSQL (datos + RLS)
  ├── Realtime (notificaciones en vivo)
  └── Edge Functions
       ├── weekly-suggester
       ├── matching-engine
       ├── feedback-processor
       └── notifications

[Externo]
  ├── Vercel (hosting + deploy)
  └── Web Push API (notificaciones)
```

### Componentes (Nivel 3) — Frontend

```
Pages:
  / → Landing (si no autenticado) o Feed
  /feed → Salidas disponibles + sugerencias semanales
  /salidas/[id] → Detalle de salida + participantes
  /perfil/[apodo] → Perfil público
  /perfil/mi → Mi perfil (editable)
  /onboarding → Test de personalidad + preferencias
  /admin → Panel de administración (programar salidas, gestionar lugares)

Components core:
  SalidaCard → Preview de salida en feed
  ParticipantList → Lista con compatibility scores
  CompatibilityBadge → Score visual (0-100%)
  WeeklySuggestions → Las 5 sugeridas
  FeedbackModal → Post-salida feedback
  PersonalityTest → Test de Big Five
  AdminPanel → Programar salidas (solo admins)
```

### Componentes (Nivel 3) — Edge Functions

```
weekly-suggester:
  Input: user_id, semana_iso
  Process:
    1. Obtener perfil + historial del usuario
    2. Filtrar salidas activas de la semana
    3. Calcular compatibility score para cada salida
    4. Rankear top 5 con diversidad de actividades
  Output: 5 salidas sugeridas

matching-engine:
  Input: user_id_a, user_id_b
  Process:
    1. Obtener vectores Big Five
    2. Calcular distancia coseno
    3. Ajustar por feedback histórico
    4. Ajustar por actividades compartidas
  Output: compatibility_score (0-100)

feedback-processor:
  Input: feedback {de_user_id, para_user_id, score, salida_id}
  Process:
    1. Almacenar feedback
    2. Actualizar pesos del perfil Big Five del usuario
    3. Recalcular compatibilidades afectadas
  Output: perfiles actualizados
```

## Decisiones Técnicas Clave

### ¿Por qué PWA y no React Native?
- Stack conocido (Next.js), cero fricción de aprendizaje
- Sin pasar por app stores (aprobación, actualizaciones)
- MVP más rápido
- Si iOS push es blocker, se migra a React Native después

### ¿Por qué Supabase y no backend propio?
- Auth, DB, Realtime, Edge Functions en un solo servicio
- RLS elimina necesidad de API middleware para consultas simples
- Gratis para empezar (500MB DB, 50K usuarios, 2M edge function requests)
- Migración a backend propio es posible si escala

### ¿Por qué Edge Functions y no serverless tradicional?
- Mismo runtime que Supabase (Deno)
- Latencia mínima (cerca de la DB)
- Sin cold starts significativos
- TypeScript nativo

## Riesgos Técnicos y Mitigaciones

| Riesgo | Mitigación |
|---|---|
| iOS PWA push notifications limitadas | Fallback a email; considerar migración a React Native si es blocker |
| Cold start del algoritmo de matching | Matching inicial por Big Five + actividades; feedback loop arranca después |
| Edge Functions timeout (10s limit) | Operaciones pesadas (weekly-suggester) asíncronas con cola |
| RLS complejidad (permisos granulares) | Testing exhaustivo de policies; auditoría periódica |
| Escalado de matching (muchos usuarios) | Cache de vectores Big Five; pre-cálculo nocturno de sugerencias |
