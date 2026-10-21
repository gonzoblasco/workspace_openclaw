#!/usr/bin/env python3
"""
onyx-tool.py - Levanta, baja y verifica Onyx (self-hosted, LLM via Ollama).

POR QUE EXISTE (2026-10-20). Onyx corre en Docker Compose desde
`projects/onyx/deployment/docker_compose`, en modo Lite (6 servicios, ~1 GB
RAM) porque Docker Desktop tiene 8 GB asignados en esta maquina. Para
levantarlo habia que acordarse de la combinacion exacta de dos archivos de
compose y del orden de los flags: `docker compose -f A.yml -f B.yml up -d`.
Un `docker compose up` a secas levanta el stack COMPLETO (OpenSearch, Redis,
model servers) y no entra en la RAM.

QUE RESUELVE. Cuatro preguntas, con el estado real y no de memoria:
  1. Esta corriendo? (sonda HTTP real, no el estado del container)
  2. Como se levanta / se para?
  3. Que modelo esta de default y responde el LLM?
  4. Que queda fuera de Lite y como se activa?

DISEÑO (lo que evita romper el CI). Las rutas son RELATIVAS al repositorio y se
resuelven en tiempo de ejecucion, nunca absolutas: el CI corre en Linux, en un
checkout distinto, y `projects/` ni siquiera esta versionado en este repo (lo
ignora .gitignore). Un test que afirme "el compose existe" con una ruta
absoluta de la Mac Mini pasa en local y falla en CI. Por eso:
  - el path del proyecto se busca porCandidates y se reporta si no esta;
  - los tests no afirman la EXISTENCIA de rutas del host: afirman la forma de
    la configuracion, que es lo que el repo si controla.

Sin dependencias externas: solo stdlib.
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

WORKSPACE = Path(__file__).resolve().parent.parent
PROJECT = "onyx"
PROJECT_DIRNAME = "onyx"

# Donde puede estar el clone de Onyx. El primero que exista gana.
PROJECT_CANDIDATES = [
    WORKSPACE / "projects" / PROJECT_DIRNAME,
    Path(os.path.expanduser("~")) / "projects" / PROJECT_DIRNAME,
]

COMPOSE_DIR_REL = Path("deployment") / "docker_compose"

# Los nombres de archivo, RELATIVOS al directorio de compose. `compose_paths`
# les antepone COMPOSE_DIR_REL una sola vez: declararlos aqui con el
# subdirectorio dentro y despues agregarlo otra vez duplicaba la ruta
# (deployment/docker_compose/deployment/docker_compose/...).
COMPOSE_FILES = [
    "docker-compose.yml",
    "docker-compose.onyx-lite.yml",
]

# Servicio y puerto de la UI (nginx mapea 80 y 3000 al host).
UI_PORT = 3000
HEALTH_URL = f"http://localhost:{UI_PORT}/api/health"

# El provider LLM y el modelo por default, para poder verificar que el stack
# sigue apuntando a donde debe.
PROVIDER_PATH = f"/api/admin/llm/provider"
CHAT_PATH = "/api/chat/create-chat-session"
SEND_PATH = "/api/chat/send-chat-message"


def find_project() -> Optional[Path]:
    """La raiz del clone de Onyx, o None.

    Devuelve la raiz del PROYECTO, no el directorio donde esta el compose:
    `compose_paths` le agrega `deployment/docker_compose` y, si(find_project)
    devolviera ese subdirectorio, la ruta saldria duplicada.
    """
    for cand in PROJECT_CANDIDATES:
        if (cand / COMPOSE_DIR_REL).is_dir():
            return cand
    return None


def compose_paths(project: Path) -> List[Path]:
    base = project / COMPOSE_DIR_REL
    return [base / f for f in COMPOSE_FILES]


def run(cmd: List[str], timeout: int = 300) -> Tuple[int, str]:
    try:
        p = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False
        )
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except FileNotFoundError:
        return 127, f"no encontrado: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 124, f"timeout: {' '.join(cmd)}"


def compose_cmd(project: Path, action: str, extra: List[str]) -> List[str]:
    cmd = ["docker", "compose"]
    for f in compose_paths(project):
        cmd += ["-f", str(f)]
    return cmd + [action] + extra


# --------------------------------------------------------------------------
# Estado
# --------------------------------------------------------------------------
def http_get(url: str, cookie: str = "", timeout: int = 8) -> Tuple[Optional[int], str]:
    try:
        req = urllib.request.Request(url, method="GET")
        if cookie:
            req.add_header("Cookie", cookie)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.getcode(), r.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")
    except Exception as e:  # noqa: BLE001 - el objetivo es reportar, no fallar
        return None, f"{type(e).__name__}: {e}"


def http_post(
    url: str, payload: Dict[str, Any], cookie: str = "", timeout: int = 240
) -> Tuple[Optional[int], str]:
    data = json.dumps(payload).encode()
    try:
        req = urllib.request.Request(
            url, data=data, method="POST",
            headers={"Content-Type": "application/json"},
        )
        if cookie:
            req.add_header("Cookie", cookie)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.getcode(), r.read().decode(errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")
    except Exception as e:  # noqa: BLE001
        return None, f"{type(e).__name__}: {e}"


def containers(project: Path) -> List[Dict[str, str]]:
    """Los containers del stack de Onyx, por etiqueta de compose."""
    code, out = run(
        [
            "docker", "ps", "-a",
            "--filter", "label=com.docker.compose.service",
            "--format", "{{.Label \"com.docker.compose.project\"}}\t"
                        "{{.Label \"com.docker.compose.service\"}}\t"
                        "{{.Names}}\t{{.Status}}",
        ],
        timeout=30,
    )
    if code != 0:
        return []
    rows = []
    for line in out.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("\t")
        # project, service, name, status: cuatro campos.
        if len(parts) < 4:
            continue
        project_name, service, name, status = parts[0], parts[1], parts[2], parts[3]
        if project_name != "onyx":
            continue
        rows.append({"service": service, "name": name, "status": status})
    return rows


def health() -> Dict[str, Any]:
    code, body = http_get(HEALTH_URL)
    ok = code == 200
    return {
        "url": HEALTH_URL,
        "code": code,
        "ok": ok,
        "detail": None if ok else (body[:200] if body else "sin respuesta"),
    }


def state() -> Dict[str, Any]:
    project = find_project()
    st: Dict[str, Any] = {
        "project_found": project is not None,
        "project_path": str(project) if project else None,
        "containers": [],
        "health": health(),
    }
    if project:
        st["containers"] = containers(project)
    st["running"] = bool(st["health"]["ok"])
    return st


# --------------------------------------------------------------------------
# Sesion admin (para verificar el provider y probar el chat)
# --------------------------------------------------------------------------
def credentials() -> Dict[str, str]:
    """Credenciales del admin, del archivo local (fuera de git)."""
    project = find_project()
    if project is None:
        return {}
    path = project / ".local" / "credentials.md"
    if not path.exists():
        return {}
    import re

    text = path.read_text(encoding="utf-8", errors="replace")
    out: Dict[str, str] = {}
    m = re.search(r"Email:\s*`([^`]+)`", text)
    if m:
        out["email"] = m.group(1)
    m = re.search(r"Password:\s*`([^`]+)`", text)
    if m:
        out["password"] = m.group(1)
    return out


def login() -> Tuple[str, str]:
    """Devuelve (cookie, error). El login de Onyx tarda 15-80 s (bcrypt)."""
    creds = credentials()
    if not creds.get("email") or not creds.get("password"):
        return "", "no hay credenciales en projects/onyx/.local/credentials.md"
    import urllib.parse

    data = urllib.parse.urlencode(
        {"username": creds["email"], "password": creds["password"]}
    ).encode()
    try:
        req = urllib.request.Request(
            f"http://localhost:{UI_PORT}/api/auth/login",
            data=data,
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        with urllib.request.urlopen(req, timeout=180) as r:
            cookie = r.headers.get("set-cookie", "").split(";")[0]
            if r.getcode() != 204 or not cookie:
                return "", f"login devolvio {r.getcode()} sin cookie"
            return cookie, ""
    except urllib.error.HTTPError as e:
        return "", f"login fallo: HTTP {e.code}"
    except Exception as e:  # noqa: BLE001
        return "", f"login fallo: {type(e).__name__}: {e}"


def provider(cookie: str) -> Dict[str, Any]:
    code, body = http_get(
        f"http://localhost:{UI_PORT}{PROVIDER_PATH}", cookie=cookie, timeout=60
    )
    if code != 200:
        return {"error": f"HTTP {code}"}
    try:
        d = json.loads(body)
    except json.JSONDecodeError:
        return {"error": "respuesta no JSON"}
    provs = d.get("providers") or []
    default = d.get("default_text") or {}
    return {
        "name": provs[0].get("name") if provs else None,
        "provider": provs[0].get("provider") if provs else None,
        "api_base": provs[0].get("api_base") if provs else None,
        "models": len(provs[0].get("model_configurations", [])) if provs else 0,
        "default_model": default.get("model_name"),
    }


def chat_test(cookie: str, model: str = "") -> Dict[str, Any]:
    """Prueba de ida y vuelta: un mensaje real al LLM."""
    code, body = http_post(
        f"http://localhost:{UI_PORT}{CHAT_PATH}", {"persona_id": 0}, cookie=cookie
    )
    if code != 200:
        return {"error": f"create-chat-session: HTTP {code}"}
    try:
        session = json.loads(body)["chat_session_id"]
    except (json.JSONDecodeError, KeyError):
        return {"error": "respuesta de create-chat-session inesperada"}

    payload: Dict[str, Any] = {
        "chat_session_id": session,
        "message": "Respond with exactly: ONYX_OK",
        "stream": False,
    }
    if model:
        payload["llm_override"] = {"model_name": model}
    code, body = http_post(
        f"http://localhost:{UI_PORT}{SEND_PATH}", payload, cookie=cookie
    )
    if code != 200:
        return {"error": f"send-chat-message: HTTP {code}"}
    try:
        d = json.loads(body)
    except json.JSONDecodeError:
        return {"error": "respuesta no JSON"}
    return {
        "answer": d.get("answer"),
        "error_msg": d.get("error_msg"),
        "model": model or "(default del stack)",
    }


# --------------------------------------------------------------------------
# Acciones
# --------------------------------------------------------------------------
def do_up(project: Path) -> int:
    code, out = run(compose_cmd(project, "up", ["-d"]), timeout=900)
    print(out.strip()[-2000:])
    return code


def do_down(project: Path) -> int:
    # stop y no down: conserva containers y volumenes.
    code, out = run(compose_cmd(project, "stop", []), timeout=300)
    print(out.strip()[-2000:])
    return code


def do_restart(project: Path) -> int:
    code, out = run(compose_cmd(project, "restart", []), timeout=300)
    print(out.strip()[-2000:])
    return code


def do_logs(project: Path, service: str = "") -> int:
    cmd = compose_cmd(project, "logs", ["-f"] if not service else ["-f", service])
    code, out = run(cmd, timeout=60)
    print(out[-4000:])
    return code


# --------------------------------------------------------------------------
# Vista
# --------------------------------------------------------------------------
def print_state(st: Dict[str, Any]) -> None:
    print("Onyx")
    if not st["project_found"]:
        print("  proyecto: NO ENCONTRADO")
        for cand in PROJECT_CANDIDATES:
            print(f"    buscado: {cand}")
        return
    print(f"  proyecto: {st['project_path']}")
    h = st["health"]
    print(f"  UI:       http://localhost:{UI_PORT}")
    print(f"  salud:    {h['url']} -> {h['code']} ({'ok' if h['ok'] else h['detail']})")
    if st["containers"]:
        print("  servicios:")
        for c in st["containers"]:
            print(f"    - {c['service']:<18} {c['status']}")


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Onyx: levantar, bajar y verificar")
    ap.add_argument(
        "command",
        nargs="?",
        default="status",
        choices=["status", "up", "down", "restart", "logs", "provider", "chat", "json"],
    )
    ap.add_argument("--model", default="", help="modelo para la prueba de chat")
    ap.add_argument("--service", default="", help="servicio para los logs")
    ap.add_argument("--json", action="store_true", help="salida JSON")
    args = ap.parse_args(argv)

    project = find_project()

    if args.command == "json":
        print(json.dumps(state(), indent=2, ensure_ascii=False))
        return 0

    if args.command == "status":
        st = state()
        if args.json:
            print(json.dumps(st, indent=2, ensure_ascii=False))
        else:
            print_state(st)
        return 0 if st["running"] else 1

    if args.command in ("up", "down", "restart", "logs"):
        if project is None:
            print("no encuentro el proyecto Onyx", file=sys.stderr)
            for cand in PROJECT_CANDIDATES:
                print(f"  buscado: {cand}", file=sys.stderr)
            return 1
        if args.command == "up":
            return do_up(project)
        if args.command == "down":
            return do_down(project)
        if args.command == "restart":
            return do_restart(project)
        return do_logs(project, args.service)

    if args.command in ("provider", "chat"):
        cookie, err = login()
        if err:
            print(f"no puedo verificar: {err}", file=sys.stderr)
            return 1
        if args.command == "provider":
            p = provider(cookie)
            if p.get("error"):
                print(f"error: {p['error']}", file=sys.stderr)
                return 1
            print(f"  provider:    {p['name']} ({p['provider']})")
            print(f"  api_base:    {p['api_base']}")
            print(f"  modelos:     {p['models']}")
            print(f"  default:     {p['default_model']}")
            return 0
        r = chat_test(cookie, args.model)
        if r.get("error"):
            print(f"error: {r['error']}", file=sys.stderr)
            return 1
        print(f"  modelo:  {r['model']}")
        print(f"  answer:  {r['answer']}")
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
