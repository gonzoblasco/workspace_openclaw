# Gateway Operations - Mapa operativo (Mac Mini)

> La Mac Mini es el **servidor 24/7** (Telegram + gateway). La MacBook Air es máquina de trabajo secundaria.
> Creado: 2026-09-08. Origen: auditoría del SDLC con Gonzo - la parte OPERATIVA del gateway no estaba cubierta.

## Qué corre en el gateway

| Componente | Estado | Cómo verificar |
|---|---|---|
| Gateway service | LaunchAgent `ai.openclaw.gateway` | `openclaw status` (línea "Gateway service") |
| Telegram canal | ON, polling, token por SecretRef | `openclaw channels status` |
| Heartbeat | **disabled** (`agents.defaults.heartbeat.every = 0m`) - decisión 2026-09-07/08: reemplazado por scripts de vigilancia | `openclaw status` (línea "Heartbeat") |
| Memory Dreaming Promotion | cron diario 03:00 (job built-in de memory-core) | `openclaw automations list` |
| Skill collection review | cada 7 días (job built-in) | `openclaw automations list` |

## Scripts (en `scripts/`)

| Script | Qué hace | Exit codes |
|---|---|---|
| `gateway-audit.sh` | Snapshot completo: status + channels + jobs + drift. `--json` para automatizar | 0 ok, 2 error interno |
| `gateway-jobs-check.sh` | Vigilante de jobs: existen, enabled, nextRun vencido (>1h), status error | 0 sano, **1 problema** (usable por un futuro watcher), 2 error |
| `gateway-config-drift.sh` | SHA256 de `openclaw.json` vs baseline `~/.openclaw/gateway-config.baseline` | 0 sin drift, 1 drift, 2 error |
| `gateway-config-drift.sh --accept` | Acepta la config actual como nuevo baseline (SOLO cuando el cambio es esperado) | - |

## Cómo auditar (ritual)

1. **Snapshot rápido:** `./scripts/gateway-audit.sh` - muestra todo en una pasada.
2. **Si hay drift:** decidir si el cambio fue esperado (algún `config set`/update/restart lo tocó). Si es esperado: `./scripts/gateway-config-drift.sh --accept`. Si NO es esperado: investigar antes de aceptar (comparar con `~/.openclaw/openclaw.json.bak-*` más reciente).
3. **Si un job falla:** `openclaw automations list` para ver el detalle, `openclaw automations runs <id>` para el historial.

## Backups de config

Convención: `~/.openclaw/openclaw.json.bak-<motivo>-<fecha>`. Antes de cualquier cambio de config: hacer backup. Existentes: `bak-telegram-off-20260908` (MacBook Air), `bak-gatewayops-20260908` (Mini).

## Secretos

- El botToken de Telegram vive en el store de secretos (`TELEGRAM_BOT_TOKEN`), referenciado desde la config por SecretRef. Nunca en texto plano en el JSON ni en chat.
- `openclaw secrets list` para ver metadatos (no valores).

## Automations de Fase 2 (activos desde 2026-09-08)

| Job | Schedule | Qué hace | Delivery |
|---|---|---|---|
| `gateway-jobs-watcher` | cada 2h | Trigger headless corre `gateway-jobs-check.sh`; dispara solo si exit 1 | Alerta por Telegram a `7921100122` (solo en fallo; silencio = sano) |
| `gateway-daily-audit` | cron 09:00 ART | Corre `gateway-audit.sh` y anexa a `~/.openclaw/gateway-audit.log` | none (silencioso por diseño) |

Contrato del trigger: el runner de `kind:script` exige que la última expresión retorne un objeto (`return {done: true}`) - sin eso el run marca error aunque el comando haya corrido. Lección de la primera corrida (2026-09-08).

## Reindex de memoria vs restarts del gateway (2026-09-08)

- Los reindex via CLI (`openclaw memory index`) son frágiles a restarts del gateway: quedan huérfanos con `reindex-lock.sqlite` residual y bloquentan intentos siguientes.
- Ritual de recovery: (1) `lsof` sobre el lock para identificar el holder real, (2) matar procesos `openclaw-memory` huérfanos a 0% CPU, (3) borrar `openclaw-agent.sqlite.reindex-lock.sqlite` (+ journal) y los scratch `memory-reindex-*` de intentos muertos, (4) reintentar.
- Señal de progreso real durante un reindex: scratch DB `memory-reindex-<uuid>` creciendo + CPU de Ollama activa. El proceso CLI a ~0% CPU es normal (el trabajo lo hace Ollama).

## Pendiente (Fase 3 - requiere OK explícito de Gonzo)

- Endurecer la alerta: failure routes por Telegram si el propio watcher falla 2 veces seguidas (hoy la cadena watcher->alerta ya está activa; falta revisar el umbral `failureAlert`).