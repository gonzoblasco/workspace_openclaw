#!/usr/bin/env bash
# cline-tool.sh - Levantar, parar y verificar Cline (agente de codigo + Hub dashboard).
#
# POR QUE EXISTE (2026-10-20). Cline esta instalado en `projects/cline` (clone de
# github.com/cline/cline) y corre el agente a traves del provider `ollama` de
# Ollama del host. El registro de herramientas (`scripts/ai-toolbox.py`) necesita
# un comando CONCRETO para levantarlo y pararlo: el `up` de un nativo no puede
# ser un comando que no termine nunca.
#
# COMANDOS
#   up            Levanta el dashboard (Hub) en background. Idempotente.
#   down          Para el dashboard y el daemon del hub. Conserva todo.
#   status        Estado real: puerto, salud HTTP, PID, workspace activo.
#   run <prompt>  Un turno de agente, headless, con --json. Acepta --cwd <dir>.
#   logs [n]      Ultimas lineas del log del dashboard.
#
# NOTAS MEDIDAS (no re-verificar a ciegas)
#   - El dashboard escucha en 8787; el daemon del hub, en 25466. Son DOS procesos:
#     el dashboard es la UI, el daemon es quien ejecuta las sesiones.
#   - El workspace del chat NO sale de WORKSPACE_ROOT sino de la sesion mas
#     reciente que el Hub conoce (`apps/cline-hub/src/server/providers.ts:38`).
#     Si ya hay sesiones, su cwd gana. Para cambiar de proyecto: borrar las
#     sesiones (UI: Sessions -> eliminar) y reiniciar.
#   - `CLINE_DIR` aislado: la config real de Cline del usuario (`~/.cline`, con su
#     sesion OAuth) NO se toca. La de prueba vive en `projects/cline/.cline-local`.
set -uo pipefail

WORKSPACE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLINE_REPO="$WORKSPACE/projects/cline"
CLINE_DIR="${CLINE_DIR:-$CLINE_REPO/.cline-local}"
DASHBOARD_PORT="${CLINE_HUB_DASHBOARD_PORT:-8787}"
HUB_PORT=25466
LOG_DIR="$CLINE_REPO/.cline-local/logs"
LOG_FILE="$LOG_DIR/dashboard.log"

export CLINE_DIR

# ---------------------------------------------------------------- utilidades
port_pid() { lsof -nP -iTCP:"$1" -sTCP:LISTEN 2>/dev/null | awk 'NR>1 {print $2}' | head -1; }
health()   { curl -sf --max-time 4 "http://127.0.0.1:${DASHBOARD_PORT}/health" 2>/dev/null; }

wait_healthy() {
	local tries="${1:-40}"
	for _ in $(seq 1 "$tries"); do
		[ -n "$(health)" ] && return 0
		sleep 0.5
	done
	return 1
}

# ------------------------------------------------------------------ up
cmd_up() {
	if [ -n "$(health)" ]; then
		echo "Cline ya esta corriendo (dashboard en :${DASHBOARD_PORT})."
		return 0
	fi
	if [ ! -d "$CLINE_REPO/apps/cli" ]; then
		echo "no encuentro el clone de Cline en $CLINE_REPO" >&2
		return 1
	fi
	if ! curl -sf --max-time 3 http://localhost:11434/api/tags >/dev/null 2>&1; then
		echo "Ollama no responde en localhost:11434 (el provider ollama lo necesita)." >&2
		return 1
	fi
	mkdir -p "$LOG_DIR"
	cd "$CLINE_REPO"
	nohup ./start-dashboard.sh >"$LOG_FILE" 2>&1 &
	echo "dashboard arrancando (pid $!), log en $LOG_FILE"
	if wait_healthy 40; then
		echo "Cline arriba: http://127.0.0.1:${DASHBOARD_PORT}  (chat: /chat)"
		return 0
	fi
	echo "el dashboard no respondio en 20s. Ultimas lineas del log:" >&2
	tail -15 "$LOG_FILE" >&2
	return 1
}

# ---------------------------------------------------------------- down
cmd_down() {
	local stopped=0
	for port in "$DASHBOARD_PORT" "$HUB_PORT"; do
		local pid
		pid="$(port_pid "$port")"
		if [ -n "$pid" ]; then
			kill "$pid" 2>/dev/null && { echo "parado :$port (pid $pid)"; stopped=1; }
		fi
	done
	[ "$stopped" = "1" ] || echo "no habia nada corriendo en :${DASHBOARD_PORT} ni :${HUB_PORT}"
	echo "Se conservan la config (.cline-local) y las sesiones."
	return 0
}

# -------------------------------------------------------------- status
cmd_status() {
	local dash hub
	dash="$(port_pid "$DASHBOARD_PORT")"
	hub="$(port_pid "$HUB_PORT")"
	printf "  dashboard:  "
	if [ -n "$dash" ]; then printf "corriendo (pid %s) en :%s\n" "$dash" "$DASHBOARD_PORT"
	else printf "apagado (puerto %s libre)\n" "$DASHBOARD_PORT"; fi
	printf "  hub daemon: "
	if [ -n "$hub" ]; then printf "corriendo (pid %s) en :%s\n" "$hub" "$HUB_PORT"
	else printf "apagado (puerto %s libre)\n" "$HUB_PORT"; fi
	local h
	h="$(health)"
	if [ -n "$h" ]; then
		printf "  salud:      %s\n" "$h"
	else
		printf "  salud:      sin respuesta\n"
	fi
	printf "  config:     %s\n" "$CLINE_DIR"
	printf "  workspace:  %s\n" "${WORKSPACE_ROOT:-<heredado de la ultima sesion>}"
	if [ -n "$dash" ] && [ -z "$h" ]; then return 1; fi
	return 0
}

# ------------------------------------------------------------------ run
cmd_run() {
	local cwd_arg="" prompt=""
	while [ $# -gt 0 ]; do
		case "$1" in
			--cwd) cwd_arg="$2"; shift 2 ;;
			*) prompt="$1"; shift ;;
		esac
	done
	if [ -z "$prompt" ]; then
		echo "uso: cline-tool.sh run [--cwd <dir>] \"<prompt>\"" >&2
		return 2
	fi
	[ -n "$cwd_arg" ] || cwd_arg="$PWD"
	cd "$CLINE_REPO"
	exec bun --conditions=development --cwd apps/cli src/index.ts \
		--cwd "$cwd_arg" --json --yolo "$prompt"
}

# ----------------------------------------------------------------- logs
cmd_logs() { tail -n "${1:-40}" "$LOG_FILE" 2>/dev/null || echo "(sin log)"; }

case "${1:-status}" in
	up) shift; cmd_up "$@" ;;
	down) shift; cmd_down "$@" ;;
	status) shift; cmd_status "$@" ;;
	run) shift; cmd_run "$@" ;;
	logs) shift; cmd_logs "$@" ;;
	*) sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//' ;;
esac
