#!/usr/bin/env python3
"""Capacidad del Crew: sesiones activas por agente.

Heuristica de dispatch: antes de spawnear, el CORE mira si ya hay una sesion
activa del mismo agente (para no duplicar) y cuanta actividad reciente hay.
No reemplaza el juicio del CORE; es una foto, no una cuota.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

AGENTS = [
    "main",
    "kanam-dev",
    "kanam-ops",
    "kanam-mind",
    "kanam-studio",
    "kanam-auditor",
    "kanam-critic",
    "kanam-planner",
]


def load_sessions() -> list[dict]:
    try:
        out = subprocess.run(
            ["openclaw", "sessions", "list", "--all-agents", "--limit", "all", "--json"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"⚠️ No pude consultar sesiones: {exc}", file=sys.stderr)
        return []
    if out.returncode != 0:
        print(f"⚠️ openclaw sessions fallo: {out.stderr.strip()[:300]}", file=sys.stderr)
        return []
    try:
        payload = json.loads(out.stdout)
    except json.JSONDecodeError:
        print("⚠️ Respuesta de sesiones no es JSON.", file=sys.stderr)
        return []
    return payload.get("sessions") or []


def main() -> None:
    parser = argparse.ArgumentParser(description="Sesiones activas por agente.")
    parser.add_argument("--minutes", type=int, default=30, help="Ventana de actividad.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    sessions = load_sessions()
    cutoff = datetime.now(timezone.utc).timestamp() * 1000 - args.minutes * 60_000
    active = Counter()
    last: dict[str, int] = {}
    for session in sessions:
        agent = session.get("agentId") or "?"
        updated = session.get("updatedAt") or 0
        if updated >= cutoff:
            active[agent] += 1
        if updated > last.get(agent, 0):
            last[agent] = updated

    rows = []
    for agent in AGENTS:
        ts = last.get(agent)
        last_iso = (
            datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
            if ts
            else "—"
        )
        rows.append(
            {
                "agent": agent,
                "active_sessions": active.get(agent, 0),
                "last_activity": last_iso,
            }
        )

    if args.json:
        print(
            json.dumps(
                {
                    "window_minutes": args.minutes,
                    "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "agents": rows,
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return

    print(f"Actividad en los últimos {args.minutes} min")
    print(f"{'Agente':16} {'Activas':>8} {'Última actividad':>20}")
    for row in rows:
        print(
            f"{row['agent']:16} {row['active_sessions']:>8} {row['last_activity']:>20}"
        )
    if active.get("kanam-planner", 0) > 0:
        print("\n⚠️ Ya hay una sesión activa del Planner: evitar spawn duplicado.")
    busy = [agent for agent, count in active.items() if count >= 3]
    if busy:
        print(f"\n⚠️ Agentes con 3+ sesiones activas: {', '.join(busy)}")


if __name__ == "__main__":
    main()
