# System: <Name>

## Goals
¿Qué problema resuelve este sistema? ¿Cuáles son los objetivos medibles?

## Actors
- **Usuario:** qué puede hacer
- **Admin:** qué puede hacer
- **Sistema:** qué hace automáticamente
- **Externo:** qué sistemas externos interactúan

## Components
| Componente | Responsabilidad | Tecnología |
|---|---|---|
| Frontend | UI, interacción | Next.js App Router |
| API | Lógica de negocio | Route Handlers / Edge Functions |
| DB | Persistencia | Supabase PostgreSQL |
| ... | ... | ... |

## Data Flow
1. Usuario hace X → Frontend llama a Y → Y procesa y guarda en Z
2. Evento externo → Webhook → Procesamiento → Notificación

## Deployment
- Hosting: Vercel / Fly / ...
- CI/CD: GitHub Actions
- Variables de entorno necesarias
- Secrets management

## Security Boundaries
- Auth: Supabase Auth / NextAuth / ...
- RLS policies necesarias
- API keys: solo server-side, nunca en cliente

## Failure Modes
| Escenario | Impacto | Mitigación |
|---|---|---|
| API de tercero caída | Datos no disponibles | Cache + fallback estático |
| Rate limiting | Lentitud | Cache + backoff |
| ... | ... | ... |

## Open Questions
- [ ] ¿Qué pasa cuando escalamos a X usuarios?
- [ ] ¿Necesitamos cola de procesamiento?
