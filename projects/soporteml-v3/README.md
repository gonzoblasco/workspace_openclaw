# SoporteML v3

CRM multi-tenant para vendedores de Mercado Libre, con asistencia de IA. Gestiona consultas, productos, stock, envíos, garantías y métricas.

**Alpha local:** corre 100% en tu máquina, sin servicios cloud (ADR-001). SQLite + backend Hono + frontend Vite + IA con Ollama.

## Stack

- **Monorepo:** Turborepo + pnpm
- **Frontend:** Vite + React + TypeScript + Tailwind (design system de Lovable, ADR-003)
- **Backend:** Node + Hono (ADR-002)
- **DB:** SQLite con capa de repositorios abstracta (`packages/db`)
- **IA:** Ollama local (modelos cloud)
- **Billing:** mock (Mercado Pago nunca probado, post-MVP)

## Requisitos

- Node.js ≥ 20
- pnpm ≥ 10
- Ollama corriendo en `localhost:11434` (para la IA; si no está, la app usa un fallback mock)

## Arranque

```bash
# 1. Instalar dependencias (desde la raíz)
pnpm install

# 2. Terminal 1 - backend (puerto 3001)
cd apps/api && pnpm dev

# 3. Terminal 2 - frontend (puerto 5173)
cd apps/web && pnpm dev
```

Abrí http://localhost:5173 y entrá con el botón "Entrar (modo demo)".

## Estructura

```
soporteml-v3/
├── apps/
│   ├── web/          # Frontend Vite + React + Tailwind
│   └── api/          # Backend Hono (MeLi, IA, billing, auth mock)
├── packages/
│   └── db/           # Capa de datos SQLite (schema + repositorios)
├── docs/adr/         # Decisiones de arquitectura (ADR-001..003)
└── .knowledge/       # Memoria institucional (producto, roadmap, referencias)
```

## Endpoints del backend

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/auth/dev/setup` | Crea usuario + empresa de prueba (modo demo) |
| GET | `/questions` | Bandeja de consultas |
| GET | `/questions/pending-sla` | Conteo de consultas pendientes de SLA |
| GET | `/products` | Catálogo de productos |
| POST | `/meli/sync` | Sincroniza preguntas de MeLi |
| POST | `/meli/publish` | Publica una respuesta a MeLi |
| GET | `/meli/status` | Estado de conexión MeLi |
| POST | `/ai/suggest` | Sugiere respuesta con IA (copiloto) |
| GET | `/billing/status` | Estado de suscripción |
| POST | `/billing/subscribe` | Crea suscripción (mock) |
| POST | `/billing/confirm` | Confirma pago (mock IPN) |
| POST | `/billing/cancel` | Cancela suscripción |

## Configuración (env)

| Variable | Default | Uso |
|---|---|---|
| `PORT` | `3001` | Puerto del backend |
| `DB_PATH` | `soporteml.db` | Ruta de la base SQLite |
| `OLLAMA_URL` | `http://localhost:11434` | Endpoint de Ollama |
| `OLLAMA_MODEL` | `deepseek-v4-flash:cloud` | Modelo de IA |
| `MELI_APP_ID` | — | App ID de Mercado Libre (para conectar MeLi) |
| `MELI_SECRET_KEY` | — | Secret de la app de MeLi |

## Estado

- **Fase 1 (alpha local):** COMPLETA ✅ — la app corre completa en local.
- **Fase 2 (validación de integraciones):** pendiente — probar Mercado Pago en sandbox, email.
- **Fase 3 (despliegue):** pendiente — decidir dónde corre en producción.

Ver `ROADMAP.md` en `.knowledge/` para el detalle.
