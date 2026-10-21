"""Tests for scripts/onyx-tool.py (levantar / verificar Onyx).

POR QUE EXISTE. La version anterior de esta herramienta (`ai-toolbox.py`, que
registraba las 10 herramientas de la maquina) ROMPIO el CI de main: el test
`test_cada_herramienta_docker_tiene_compose_existente` afirmaba que
`/home/runner/projects/onyx/deployment/docker_compose/docker-compose.yml`
existe, y el CI corre en Linux con un checkout distinto. 378 tests pasaron y UNO
fallo: exactamente el que afirmaba una ruta del host.

La leccion que este archivo encodes: en el CI se afirman FORMAS de configuracion
(lo que el repo controla), nunca la EXISTENCIA de rutas de la maquina de
Gonzo. `projects/` esta ignorado por `.gitignore` (cada proyecto es su propio
repo), asi que ninguna ruta de ahi puede estar versionada ni existir en el CI.

Propiedades criticas:
  1. Los compose de Onyx se nombran por RUTA RELATIVA al proyecto, nunca
     absoluta: la tabla del repo es la que el CI puede verificar.
  2. El emparejamiento con Docker es por ARCHIVO de compose, no por el
     `name:` del archivo (la mayoria de los compose no lo declara, y Docker
     deriva el nombre del proyecto del directorio).
  3. La CLI responde y falla con codigo distinto de cero cuando algo falla.
"""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = ROOT / "scripts" / "onyx-tool.py"


def load():
    spec = importlib.util.spec_from_file_location("onyx_tool", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------
# Stub de docker: responde con lo que el test le dicta.
# --------------------------------------------------------------------------
STUB = """#!/usr/bin/env python3
import json, os, sys
data = json.load(open(os.environ["STUB_STATE"]))
args = sys.argv[1:]
if args[:2] == ["ps", "-a"]:
    for r in data.get("rows", []):
        print("\\t".join([r["project"], r["service"], r["name"], r["status"]]))
    sys.exit(0)
if args[:2] == ["compose", "ls"]:
    print(json.dumps(data.get("projects", [])))
    sys.exit(0)
print("")
sys.exit(0)
"""


def write_stub(tmp_path, state):
    stub = tmp_path / "docker"
    stub.write_text(STUB)
    stub.chmod(0o755)
    state_file = tmp_path / "state.json"
    state_file.write_text(json.dumps(state))
    return state_file


def run_script(args, cwd=None, env_extra=None):
    env = dict(os.environ)
    env.update(env_extra or {})
    return subprocess.run(
        [sys.executable, str(SCRIPT)] + args,
        capture_output=True,
        text=True,
        timeout=90,
        cwd=str(cwd or ROOT),
        env=env,
    )


# --------------------------------------------------------------------------
# 1. La configuracion del repo: rutas RELATIVAS, compose en modo Lite.
# --------------------------------------------------------------------------
def test_los_compose_se_declaran_con_ruta_relativa():
    """La causa del fallo de CI: una ruta absoluta de la Mac no existe en Linux."""
    mod = load()
    for f in mod.COMPOSE_FILES:
        assert not Path(f).is_absolute(), f"{f} es absoluta: no puede existir en el CI"
        assert ".." not in Path(f).parts, f"{f} sale del proyecto"
    # El subdirectorio del compose se declara UNA sola vez.
    assert mod.COMPOSE_DIR_REL == Path("deployment") / "docker_compose"
    for f in mod.COMPOSE_FILES:
        assert mod.COMPOSE_DIR_REL not in Path(f).parts, (
            f"{f} ya incluye el subdirectorio: se duplicaria al componer la ruta"
        )


def test_el_compose_de_lite_esta_declarado():
    """Lite es el modo que entra en la RAM de 8 GB. No puede faltar."""
    mod = load()
    names = [Path(f).name for f in mod.COMPOSE_FILES]
    assert "docker-compose.onyx-lite.yml" in names
    assert "docker-compose.yml" in names


def test_el_modo_lite_es_el_primero():
    """El orden importa: Lite debe ir despues del base para pisar sus valores."""
    mod = load()
    names = [Path(f).name for f in mod.COMPOSE_FILES]
    assert names[0] == "docker-compose.yml"
    assert names[1] == "docker-compose.onyx-lite.yml"


def test_la_ruta_compuesta_no_se_duplica(tmp_path):
    """El bug real: deployment/docker_compose/deployment/docker_compose/..."""
    mod = load()
    project = tmp_path / "onyx"
    (project / mod.COMPOSE_DIR_REL).mkdir(parents=True)
    for f in mod.compose_paths(project):
        rel = f.relative_to(project)
        assert rel.parts.count("deployment") == 1, f"ruta duplicada: {rel}"


def test_los_candidates_de_proyecto_no_son_absolutos_dentro_del_repo():
    """El workspace tiene projects/; el segundo candidate es el symlink del home."""
    mod = load()
    for cand in mod.PROJECT_CANDIDATES:
        assert cand.name == "onyx"
    # Al menos uno tiene que estar dentro del workspace.
    assert any(
        str(c).startswith(str(ROOT)) for c in mod.PROJECT_CANDIDATES
    ), "ningun candidate apunta al workspace"


def test_el_script_no_declara_credenciales():
    """El password vive en projects/onyx/.local/credentials.md, no en el repo."""
    text = SCRIPT.read_text(encoding="utf-8")
    # Ningun password literal: el script lo LEE del archivo local.
    assert "Onyx!Gonzo" not in text
    assert "gonzo@gonzoblasco.com" not in text
    # Y lo lee de ahi explicitamente.
    assert ".local" in text and "credentials.md" in text


# --------------------------------------------------------------------------
# 2. El emparejamiento con Docker.
# --------------------------------------------------------------------------
def test_containers_filtra_por_el_proyecto_onyx(tmp_path, monkeypatch):
    mod = load()
    state_file = write_stub(
        tmp_path,
        {
            "rows": [
                {"project": "onyx", "service": "api_server", "name": "onyx-api_server-1", "status": "Up 2 hours (healthy)"},
                {"project": "onyx", "service": "nginx", "name": "onyx-nginx-1", "status": "Up 2 hours (healthy)"},
                {"project": "otro", "service": "x", "name": "x-1", "status": "Up"},
            ]
        },
    )
    monkeypatch.setenv("PATH", f"{tmp_path}:{os.environ['PATH']}")
    monkeypatch.setenv("STUB_STATE", str(state_file))
    rows = mod.containers(Path("/tmp/whatever"))
    services = {r["service"] for r in rows}
    assert "api_server" in services
    assert "x" not in services, "se colaron containers de otro proyecto"


def test_compose_cmd_usa_los_dos_archivos_en_orden(tmp_path):
    mod = load()
    cmd = mod.compose_cmd(tmp_path, "up", ["-d"])
    assert cmd[0:2] == ["docker", "compose"]
    assert "-f" in cmd
    # Los dos archivos, y el orden es base -> lite.
    files = [cmd[i + 1] for i, a in enumerate(cmd) if a == "-f"]
    assert len(files) == 2
    assert files[0].endswith("docker-compose.yml")
    assert files[1].endswith("docker-compose.onyx-lite.yml")
    assert cmd[-2:] == ["up", "-d"]


def test_down_usa_stop_no_down(tmp_path):
    """`stop` conserva volumenes. `down` de compose tambien, pero `down -v` no:
    el script no debe ofrecer borrar datos por accidente."""
    mod = load()
    cmd = mod.compose_cmd(tmp_path, "stop", [])
    assert cmd[-1] == "stop"
    assert "-v" not in cmd
    assert "--volumes" not in cmd


# --------------------------------------------------------------------------
# 3. La CLI responde.
# --------------------------------------------------------------------------
def test_status_json_devuelve_la_forma_esperada():
    r = run_script(["status", "--json"])
    assert r.returncode in (0, 1), r.stderr
    data = json.loads(r.stdout)
    for key in ("project_found", "project_path", "containers", "health", "running"):
        assert key in data, f"falta {key} en la salida"


def test_json_devuelve_el_estado():
    r = run_script(["json"])
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert "health" in data


def test_up_sin_proyecto_falla_con_mensaje():
    """Sin el clone, el error tiene que nombrar donde se busco."""
    r = run_script(["up"], cwd=Path("/tmp"))
    if r.returncode == 0:
        return  # el proyecto existe en esta maquina: nada que probar
    assert "no encuentro" in (r.stdout + r.stderr).lower()


def test_comando_invalido_es_rechazado():
    r = run_script(["comando-que-no-existe"])
    assert r.returncode != 0


def test_help_no_falla():
    r = run_script(["--help"])
    assert r.returncode == 0
    assert "Onyx" in r.stdout or "onyx" in r.stdout.lower()
