# SoporteML v3

Multi-tenant CRM for Mercado Libre sellers with AI assistance. Manages questions, products, stock, shipping, warranties, and metrics.

**Local alpha:** runs 100% on your machine with no cloud services (ADR-001). SQLite + Hono backend + Vite frontend + Ollama AI.

## Stack

- **Monorepo:** Turborepo + pnpm
- **Frontend:** Vite + React + TypeScript + Tailwind (Lovable design system, ADR-003)
- **Backend:** Node + Hono (ADR-002)
- **DB:** SQLite with an abstract repository layer (`packages/db`)
- **AI:** local Ollama (cloud models)
- **Billing:** mock (Mercado Pago never tested, post-MVP)

## Requirements

- Node.js ≥ 20
- pnpm ≥ 10
- Ollama running on `localhost:11434` (for the AI; if missing, the app falls back to a mock)

## Getting started

```bash
# 1. Install dependencies (from the root)
pnpm install

# 2. Terminal 1 - backend (port 3001)
cd apps/api && pnpm dev

# 3. Terminal 2 - frontend (port 5173)
cd apps/web && pnpm dev
```

Open http://localhost:5173 and log in with the "Entrar (modo demo)" button (demo mode).

## Structure

```
soporteml-v3/
├── apps/
│   ├── web/          # Vite + React + Tailwind frontend
│   └── api/          # Hono backend (MeLi, AI, billing, mock auth)
├── packages/
│   └── db/           # SQLite data layer (schema + repositories)
├── docs/adr/         # Architecture decisions (ADR-001..003)
└── .knowledge/       # Institutional memory (product, roadmap, references)
```

## Backend endpoints

| Method | Route | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/auth/dev/setup` | Creates a test user + company (demo mode) |
| GET | `/questions` | Questions inbox |
| GET | `/questions/pending-sla` | Count of pending-SLA questions |
| GET | `/products` | Product catalog |
| POST | `/meli/sync` | Syncs MeLi questions |
| POST | `/meli/publish` | Publishes an answer to MeLi |
| GET | `/meli/status` | MeLi connection status |
| POST | `/ai/suggest` | Suggests an AI answer (copilot) |
| GET | `/billing/status` | Subscription status |
| POST | `/billing/subscribe` | Creates a subscription (mock) |
| POST | `/billing/confirm` | Confirms payment (mock IPN) |
| POST | `/billing/cancel` | Cancels subscription |

## Configuration (env)

| Variable | Default | Purpose |
|---|---|---|
| `PORT` | `3001` | Backend port |
| `DB_PATH` | `soporteml.db` | SQLite database path |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama endpoint |
| `OLLAMA_MODEL` | `deepseek-v4-flash:cloud` | AI model |
| `MELI_APP_ID` | — | Mercado Libre app ID (to connect MeLi) |
| `MELI_SECRET_KEY` | — | MeLi app secret |

## Status

- **Phase 1 (local alpha):** COMPLETE ✅ — the app runs fully on local.
- **Phase 2 (integration validation):** Mercado Libre integration working (OAuth + sync + publish). Pending: Mercado Pago sandbox, email.
- **Phase 3 (deployment):** pending — decide where it runs in production.

See `ROADMAP.md` in `.knowledge/` for details.
