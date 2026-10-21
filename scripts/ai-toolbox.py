#!/usr/bin/env python3
"""
ai-toolbox.py - Registro vivo de las herramientas IA instaladas en esta maquina.

POR QUE EXISTE (2026-10-20). Gonzo tiene stacks de IA corriendo en la Mac Mini
y el inventario vivia en el chat: cada vez que preguntaba "cuales apps tengo"
habia que re-derivar la respuesta mirando `docker ps`. Peor: una lista escrita a
mano seerve. Onyx estaba instalado y funcionando, y no estaba en ningun registro.

QUE RESUELVE. Un unico lugar que responde tres preguntas:
  1. QUE HAY INSTALADO (la tabla TOOLS, con como se levanta cada cosa).
  2. QUE ESTA CORRIENDO AHORA (docker + sondas HTTP reales, no configuracion).
  3. COMO SE LEVANTA / SE BAJA (comando concreto por herramienta).

El estado NUNCA sale de la tabla: sale de Docker y de una sonda HTTP. La tabla
solo dice COMO se levanta. Por eso el registro no puede mentir por aging.

La tabla es la fuente de verdad de los DATOS (nombre, puerto, comando, sonda).
`docs/tools/REGISTRY.md` es la VISTA humana de esos datos (la tabla se regenera
con `catalog --write`) mas la prosa que un script no puede guardar: credenciales,
trampas, para que sirve cada cosa. Mismo patron que `memory.db` -> `memory/*.md`.

Uso:
  ai-toolbox.py list                 # tabla de todo con estado real
  ai-toolbox.py list --json          # lo mismo, para maquinas
  ai-toolbox.py status <id>          # detalle de una herramienta
  ai-toolbox.py health               # sondas HTTP de todas
  ai-toolbox.py up <id>              # levantar
  ai-toolbox.py down <id>            # parar (conserva volumenes)
  ai-toolbox.py restart <id>         # reiniciar
  ai-toolbox.py catalog --write      # regenera la tabla de docs/tools/REGISTRY.md
  ai-toolbox.py catalog --check      # verifica que la vista no seerve

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
REGISTRY_DOC = WORKSPACE / "docs" / "tools" / "REGISTRY.md"

HOME = Path(os.path.expanduser("~"))
PROJECTS = HOME / "projects"


def _p(*parts: str) -> str:
    """Ruta expandida con ~ y con el symlink de projects resuelto."""
    raw = Path(*parts).expanduser()
    return str(raw)


# --------------------------------------------------------------------------
# LA TABLA: que hay instalado y como se levanta.
#
# `compose` son los archivos de compose, en orden de capas. `None` = no es
# docker (nativo del host). `health` es la sonda HTTP con los codigos que
# cuentan como "vivo": un 401 (pide bearer) o un 308 (redirect) NO son caidas.
# --------------------------------------------------------------------------
TOOLS: List[Dict[str, Any]] = [
    {
        "id": "ollama",
        "name": "Ollama",
        "what": "Motor LLM. Nativo del host. Sirve los modelos :cloud por proxy y los locales en MLX.",
        "kind": "native",
        "runtime": "nativo (host)",
        "port": 11434,
        "compose": None,
        "health": ("http://127.0.0.1:11434/api/tags", [200]),
        "up": ["open", "-a", "Ollama"],
        "down": ["osascript", "-e", 'quit app "Ollama"'],
        "note": "Todos los stacks de abajo lo consumen via host.docker.internal:11434.",
    },
    {
        "id": "onyx",
        "name": "Onyx",
        "what": "Capa de contexto/RAG de equipo: chat, agents, MCP server y sandbox de codigo.",
        "kind": "docker",
        "runtime": "docker compose (Lite: 6 servicios)",
        "port": 3000,
        "compose": [
            _p(PROJECTS / "onyx" / "deployment" / "docker_compose" / "docker-compose.yml"),
            _p(PROJECTS / "onyx" / "deployment" / "docker_compose" / "docker-compose.onyx-lite.yml"),
        ],
        "health": ("http://localhost:3000/api/health", [200]),
        "up": None,
        "down": None,
        "note": "LLM via provider ollama_chat apuntando al Ollama del host. Solo modelos cloud.",
    },
    {
        "id": "browser-use",
        "name": "browser-use",
        "what": "Agente de navegacion web. Se expone como server MCP (16 tools) para OpenClaw.",
        "kind": "mcp",
        "runtime": "docker (stdio, bajo demanda)",
        "port": None,
        "compose": [_p(PROJECTS / "browser-use" / "docker-compose.yml")],
        "health": None,
        "up": None,
        "down": None,
        "note": "No tiene puerto propio: OpenClaw lo lanza con docker run por el MCP registrado.",
    },
    {
        "id": "anythingllm",
        "name": "AnythingLLM",
        "what": "Chat con documentos. RAG basico con Ollama como LLM y como embeddings.",
        "kind": "docker",
        "runtime": "docker compose",
        "port": 3001,
        "compose": [_p(HOME / "anythingllm-data" / "docker-compose.yml")],
        "health": ("http://localhost:3001/api/health", [200]),
        "up": None,
        "down": None,
        "note": "Datos y config viven en ~/anythingllm-data (fuera del workspace).",
    },
    {
        "id": "litellm",
        "name": "LiteLLM",
        "what": "Proxy OpenAI-compatible que sirve modelos del daemon Ollama del host.",
        "kind": "docker",
        "runtime": "docker compose",
        "port": 4000,
        "compose": [_p(HOME / "experiments" / "litellm-ollama" / "docker-compose.yml")],
        "health": ("http://localhost:4000/health/liveliness", [200]),
        "up": None,
        "down": None,
        "note": "Clon del repo BerriAI/litellm en ~/experiments/litellm (fuera del workspace).",
    },
    {
        "id": "milvus",
        "name": "Milvus",
        "what": "Base vectorial. Embeddings via el endpoint OpenAI-compatible de Ollama.",
        "kind": "docker",
        "runtime": "docker compose (standalone embebido)",
        "port": 19530,
        "compose": [_p(PROJECTS / "milvus-ollama" / "docker-compose.yml")],
        "health": ("http://localhost:9091/healthz", [200]),
        "up": None,
        "down": None,
        "note": "Modo embebido (etcd + storage dentro del container) por el limite de RAM de Docker.",
    },
    {
        "id": "vane",
        "name": "Vane",
        "what": "Motor de busqueda con respuestas citadas. Privacy-first, web + local.",
        "kind": "docker",
        "runtime": "docker compose",
        "port": 3005,
        "compose": [_p(PROJECTS / "vane" / "docker-compose.yml")],
        "health": ("http://localhost:3005/", [200]),
        "up": None,
        "down": None,
        "note": "El puerto 3000 lo tiene onyx-nginx; por eso Vane usa 3005.",
    },
    {
        "id": "opencode",
        "name": "opencode",
        "what": "Servidor de agente de codigo. Sesiones, DB y logs persistidos.",
        "kind": "docker",
        "runtime": "docker compose",
        "port": 4096,
        "compose": [_p(PROJECTS / "opencode" / "docker" / "docker-compose.yml")],
        "health": ("http://localhost:4096/health", [200]),
        "up": None,
        "down": None,
        "note": "Build local (opencode-local:dev). Puerto en loopback, con usuario y password.",
    },
    {
        "id": "openhands",
        "name": "OpenHands",
        "what": "Agent Canvas: agente que ejecuta tareas con su propia interfaz web.",
        "kind": "docker",
        "runtime": "docker compose",
        "port": 8000,
        "compose": [_p(PROJECTS / "openhands" / "docker-compose.ollama.yml")],
        "health": ("http://localhost:8000/", [200, 301, 302, 307, 308]),
        "up": None,
        "down": None,
        "note": "Su backend interno escucha en 18000; el 8000 es el proxy estatico.",
    },
    {
        "id": "cline",
        "name": "Cline",
        "what": "Agente de codigo open source. CLI + Hub dashboard. Usa el provider ollama.",
        "kind": "native",
        "runtime": "nativo (host, Bun 1.4.2)",
        "port": 8787,
        "compose": None,
        "paths": [
            _p(PROJECTS / "cline" / "apps" / "cli"),
            str(WORKSPACE / "scripts" / "cline-tool.sh"),
        ],
        "health": ("http://127.0.0.1:8787/health", [200]),
        "up": ["bash", str(WORKSPACE / "scripts" / "cline-tool.sh"), "up"],
        "down": ["bash", str(WORKSPACE / "scripts" / "cline-tool.sh"), "down"],
        "note": "El dashboard (8787) es la UI; el daemon del hub (25466) ejecuta las sesiones.",
    },
]

BY_ID = {t["id"]: t for t in TOOLS}


# --------------------------------------------------------------------------
# Estado real. Nunca sale de la tabla.
# --------------------------------------------------------------------------
def run(cmd: List[str], timeout: int = 60) -> Tuple[int, str]:
    try:
        p = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout, check=False
        )
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except FileNotFoundError:
        return 127, f"no encontrado: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 124, f"timeout: {' '.join(cmd)}"


def compose_files(tool: Dict[str, Any]) -> List[str]:
    return list(tool.get("compose") or [])


def compose_cmd(tool: Dict[str, Any], action: str, extra: List[str]) -> List[str]:
    files = compose_files(tool)
    cmd = ["docker", "compose"]
    for f in files:
        cmd += ["-f", f]
    return cmd + [action] + extra


def compose_projects() -> List[Dict[str, str]]:
    """Los stacks de compose que Docker ve, con los archivos que los definen.

    Se empareja por ARCHIVO, no por el `name:` del compose: la mayoria de estos
    compose no declaran `name:`, y el nombre del proyecto lo deriva Docker del
    directorio (por eso opencode es "docker" y litellm-ollama es "litellm-ollama").
    Buscar el `name:` en el archivo daba 6 herramientas como "apagado" mientras
    estaban corriendo. La fuente de verdad es `docker compose ls`, que ya sabe
    el emparejamiento.
    """
    code, out = run(["docker", "compose", "ls", "--format", "json"], timeout=30)
    if code != 0:
        return []
    try:
        projects = json.loads(out or "[]")
    except json.JSONDecodeError:
        return []
    rows = []
    for p in projects:
        cfg = p.get("ConfigFiles", "") or ""
        rows.append(
            {
                "name": p.get("Name", ""),
                "status": p.get("Status", ""),
                "config_files": [c for c in cfg.split(",") if c],
            }
        )
    return rows


def _same_path(a: str, b: str) -> bool:
    try:
        return os.path.realpath(a) == os.path.realpath(b)
    except OSError:
        return a == b


def container_state(tool: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """Estado del container de la herramienta, segun el stack de compose.

    Devuelve dict con name/status/image, o None si el stack no esta corriendo.
    """
    files = compose_files(tool)
    if not files:
        return None
    for project in compose_projects():
        if not any(_same_path(f, c) for f in files for c in project["config_files"]):
            continue
        code, out = run(
            [
                "docker",
                "ps",
                "-a",
                "--filter",
                f"label=com.docker.compose.project={project['name']}",
                "--format",
                "{{.Names}}\t{{.Status}}\t{{.Image}}",
            ]
        )
        if code != 0 or not out.strip():
            return None
        lines = out.strip().split("\n")
        name, status, image = lines[0].split("\t")
        return {
            "project": project["name"],
            "name": name,
            "status": status,
            "image": image,
            "containers": len(lines),
        }
    return None


def probe_health(tool: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Sonda HTTP contra el endpoint de salud. None = la herramienta no expone uno."""
    health = tool.get("health")
    if not health:
        return None
    url, accept = health
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=8) as r:
            code = r.getcode()
    except urllib.error.HTTPError as e:
        code = e.code
    except Exception as e:  # noqa: BLE001 - el objetivo es reportar, no fallar
        return {"url": url, "code": None, "ok": False, "detail": type(e).__name__}
    return {
        "url": url,
        "code": code,
        "ok": code in accept,
        "detail": None if code in accept else "codigo fuera de lo esperado",
    }


def _installed(tool: Dict[str, Any]) -> bool:
    """Si la herramienta esta instalada en esta maquina.

    Un nativo no tiene compose: se declara con `paths` (el clone y el script de
    arranque). Sin `paths` y sin compose, no hay nada que verificar.
    """
    paths = list(tool.get("paths") or [])
    if paths:
        return all(Path(p).exists() for p in paths)
    files = compose_files(tool)
    return bool(files) and all(Path(f).exists() for f in files)


def tool_state(tool: Dict[str, Any]) -> Dict[str, Any]:
    """Estado real de una herramienta: proceso + sonda."""
    state: Dict[str, Any] = {
        "id": tool["id"],
        "name": tool["name"],
        "runtime": tool["runtime"],
        "port": tool["port"],
        "kind": tool["kind"],
        "installed": _installed(tool),
        "status": "desconocido",
        "detail": "",
    }
    if tool["kind"] == "native":
        probe = probe_health(tool)
        if probe and probe["ok"]:
            state["status"] = "corriendo"
            state["detail"] = f"HTTP {probe['code']}"
        elif probe:
            state["status"] = "apagado"
            state["detail"] = f"HTTP {probe['code']}"
        else:
            state["status"] = "desconocido"
        return state

    if tool["kind"] == "mcp":
        # No hay puerto: el server MCP lo lanza OpenClaw bajo demanda.
        image = tool["compose"][0] if tool["compose"] else ""
        image_name = image.split("/")[-1] if image else ""
        has_image = bool(run(["docker", "image", "inspect", "browseruse:local"])[0] == 0)
        state["installed"] = has_image
        state["status"] = "bajo demanda" if has_image else "no instalado"
        state["detail"] = "MCP stdio: lo lanza OpenClaw por sesion" if has_image else ""
        return state

    cont = container_state(tool)
    if cont is None:
        state["status"] = "apagado" if state["installed"] else "no instalado"
        state["detail"] = "sin container" if state["installed"] else "falta el compose"
        return state
    state["container"] = cont
    state["status"] = "corriendo" if cont["status"].startswith("Up") else "apagado"
    state["detail"] = cont["status"]
    probe = probe_health(tool)
    if probe:
        state["health"] = probe
        if not probe["ok"] and state["status"] == "corriendo":
            state["status"] = "corriendo (sonda falla)"
            state["detail"] = f"{cont['status']} / HTTP {probe['code']}"
    return state


def all_states() -> List[Dict[str, Any]]:
    return [tool_state(t) for t in TOOLS]


def unknown_projects() -> List[Dict[str, str]]:
    """Stacks de compose corriendo que no estan en la tabla.

    Si alguien instala algo nuevo, el registro lo tiene que mostrar: una tabla
    que solo conoce lo que ya sabia no es un registro.
    """
    extra = []
    for p in compose_projects():
        known = False
        for t in TOOLS:
            if any(_same_path(f, c) for f in compose_files(t) for c in p["config_files"]):
                known = True
                break
        if not known:
            extra.append(
                {
                    "name": p["name"],
                    "config": ", ".join(p["config_files"]),
                    "status": p["status"],
                }
            )
    return extra


# --------------------------------------------------------------------------
# Acciones
# --------------------------------------------------------------------------
def do_up(tool: Dict[str, Any]) -> int:
    if tool["kind"] == "native":
        code, out = run(tool["up"], timeout=60)
        print(out.strip() or ("abierto" if code == 0 else "fallo"))
        return code
    if tool["kind"] == "mcp":
        print(
            f"{tool['name']} corre bajo demanda: lo lanza OpenClaw como server MCP\n"
            f"  (imagen: browseruse:local, MCP registrado en openclaw.json)"
        )
        return 0
    code, out = run(compose_cmd(tool, "up", ["-d"]), timeout=600)
    print(out.strip()[-2000:])
    return code


def do_down(tool: Dict[str, Any]) -> int:
    if tool["kind"] == "native":
        code, out = run(tool["down"], timeout=60)
        print(out.strip() or ("detenido" if code == 0 else "fallo"))
        return code
    if tool["kind"] == "mcp":
        print(f"{tool['name']} no tiene proceso que parar: se lanza por sesion.")
        return 0
    # stop y no down: conserva los containers y los volumenes.
    code, out = run(compose_cmd(tool, "stop", []), timeout=300)
    print(out.strip()[-2000:])
    return code


def do_restart(tool: Dict[str, Any]) -> int:
    if tool["kind"] == "native":
        do_down(tool)
        return do_up(tool)
    if tool["kind"] == "mcp":
        print(f"{tool['name']} no tiene proceso que reiniciar.")
        return 0
    code, out = run(compose_cmd(tool, "restart", []), timeout=300)
    print(out.strip()[-2000:])
    return code


# --------------------------------------------------------------------------
# Vista
# --------------------------------------------------------------------------
CATALOG_BEGIN = "<!-- BEGIN:ai-toolbox-table -->"
CATALOG_END = "<!-- END:ai-toolbox-table -->"


def render_table(states: List[Dict[str, Any]]) -> str:
    rows = [
        "| Herramienta | ID | Runtime | Puerto | Estado |",
        "|---|---|---|---|---|",
    ]
    for s in states:
        t = BY_ID[s["id"]]
        port = str(t["port"]) if t["port"] else "-"
        rows.append(
            f"| {t['name']} | `{t['id']}` | {t['runtime']} | {port} | {s['status']} |"
        )
    extra = unknown_projects()
    if extra:
        rows.append("")
        rows.append("Stacks de compose corriendo que no tienen ficha:")
        rows.append("")
        for e in extra:
            rows.append(f"- `{e['name']}` ({e['status']})")
    return "\n".join(rows)


def write_catalog(states: List[Dict[str, Any]]) -> int:
    if not REGISTRY_DOC.exists():
        print(f"no existe {REGISTRY_DOC}", file=sys.stderr)
        return 1
    text = REGISTRY_DOC.read_text(encoding="utf-8")
    if CATALOG_BEGIN not in text or CATALOG_END not in text:
        print("el doc no tiene los marcadores de la tabla", file=sys.stderr)
        return 1
    head, rest = text.split(CATALOG_BEGIN, 1)
    _, tail = rest.split(CATALOG_END, 1)
    new = head + CATALOG_BEGIN + "\n" + render_table(states) + "\n" + CATALOG_END + tail
    if new == text:
        print("la vista ya estaba al dia")
        return 0
    REGISTRY_DOC.write_text(new, encoding="utf-8")
    try:
        shown = REGISTRY_DOC.relative_to(WORKSPACE)
    except ValueError:
        shown = REGISTRY_DOC
    print(f"tabla regenerada en {shown}")
    return 0


def check_catalog(states: List[Dict[str, Any]]) -> int:
    if not REGISTRY_DOC.exists():
        print(f"no existe {REGISTRY_DOC}", file=sys.stderr)
        return 1
    text = REGISTRY_DOC.read_text(encoding="utf-8")
    if CATALOG_BEGIN not in text:
        print("el doc no tiene los marcadores de la tabla", file=sys.stderr)
        return 1
    current = render_table(states)
    block = text.split(CATALOG_BEGIN, 1)[1].split(CATALOG_END, 1)[0].strip()
    if current.strip() != block:
        print("la vista seerve: correr  ai-toolbox.py catalog --write")
        return 1
    print("la vista esta al dia")
    return 0


def print_table(states: List[Dict[str, Any]]) -> None:
    if not sys.stdout.isatty():
        for s in states:
            print(f"{s['id']}\t{s['status']}\t{s['detail']}")
        return
    w = max(len(s["id"]) for s in states)
    print(f"{'ID'.ljust(w)}  {'ESTADO'.ljust(24)} DETALLE")
    for s in states:
        print(f"{s['id'].ljust(w)}  {s['status'].ljust(24)} {s['detail']}")
    extra = unknown_projects()
    if extra:
        print()
        print("Stacks de compose corriendo sin ficha en el registro:")
        for e in extra:
            print(f"  - {e['name']} ({e['status']})")


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", nargs="?", default="list")
    ap.add_argument("target", nargs="?", help="id de la herramienta")
    ap.add_argument("--json", action="store_true", help="salida JSON")
    ap.add_argument("--write", action="store_true", help="escribir la vista")
    ap.add_argument("--check", action="store_true", help="verificar la vista")
    args = ap.parse_args(argv)

    cmd = args.command

    if cmd == "list":
        states = all_states()
        if args.json:
            print(json.dumps(states, indent=2, ensure_ascii=False))
        else:
            print_table(states)
        return 0

    if cmd == "status":
        if not args.target:
            print("falta el id de la herramienta", file=sys.stderr)
            return 2
        tool = BY_ID.get(args.target)
        if not tool:
            print(f"desconocida: {args.target}", file=sys.stderr)
            print("conocidas: " + ", ".join(sorted(BY_ID)), file=sys.stderr)
            return 2
        state = tool_state(tool)
        if args.json:
            print(json.dumps({"tool": tool, "state": state}, indent=2, ensure_ascii=False))
            return 0
        print(f"{tool['name']} ({tool['id']})")
        print(f"  que es:     {tool['what']}")
        print(f"  runtime:    {tool['runtime']}")
        print(f"  puerto:     {tool['port'] if tool['port'] else '-'}")
        print(f"  estado:     {state['status']} ({state['detail']})")
        if tool.get("note"):
            print(f"  nota:       {tool['note']}")
        for f in compose_files(tool):
            print(f"  compose:    {f} ({'existe' if Path(f).exists() else 'FALTA'})")
        probe = state.get("health")
        if probe:
            print(f"  sonda:      {probe['url']} -> HTTP {probe['code']} "
                  f"({'ok' if probe['ok'] else probe['detail']})")
        return 0

    if cmd == "health":
        states = all_states()
        if args.json:
            print(json.dumps(states, indent=2, ensure_ascii=False))
            return 0
        bad = 0
        for s in states:
            probe = s.get("health")
            if not probe:
                print(f"  {s['id']:<14} {s['status']}")
                continue
            mark = "ok" if probe["ok"] else "FALLA"
            if not probe["ok"]:
                bad += 1
            print(f"  {s['id']:<14} {s['status']:<24} HTTP {probe['code']} {mark}")
        return 1 if bad else 0

    if cmd in ("up", "down", "restart"):
        if not args.target:
            print(f"falta el id de la herramienta (usa: ai-toolbox.py {cmd} <id>)",
                  file=sys.stderr)
            return 2
        tool = BY_ID.get(args.target)
        if not tool:
            print(f"desconocida: {args.target}", file=sys.stderr)
            print("conocidas: " + ", ".join(sorted(BY_ID)), file=sys.stderr)
            return 2
        print(f"==> {cmd} {tool['name']}")
        if cmd == "up":
            return do_up(tool)
        if cmd == "down":
            return do_down(tool)
        return do_restart(tool)

    if cmd == "catalog":
        states = all_states()
        if args.write:
            return write_catalog(states)
        if args.check:
            return check_catalog(states)
        print(render_table(states))
        return 0

    if cmd == "ids":
        for t in TOOLS:
            print(t["id"])
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
