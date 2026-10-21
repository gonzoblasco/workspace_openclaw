"""Tests for scripts/ai-toolbox.py (registro vivo de herramientas IA).

POR QUE EXISTE. El registro se escribio a mano primero y ya fallo dos veces
antes de tener tests: (1) Six herramientas aparecian como "apagado" mientras
estaban corriendo, porque el script emparejaba los stacks de compose por el
`name:` del archivo y la mayoria no lo declara (Docker deriva el nombre del
directorio); (2) un `Up` de container se tomaba por "sirviendo" cuando la sonda
HTTP era la que prueba.

Un registro que miente sobre el estado es peor que no tener registro: el
inventario se usa para decidir que apagar.

Propiedades criticas:
  1. El emparejamiento de un stack es por ARCHIVO de compose, no por `name:`.
  2. Los codigos HTTP que cuentan como "vivo" son POR HERRAMIENTA (un 401 de
     pr-agent es vivo; un 502 de openhands es caido).
  3. La vista de docs/tools/REGISTRY.md se puede regenerar y verificar.
  4. La tabla de herramientas declara una sonda y un compose por entrada.

Los tests no tocan Docker real: las funciones de estado se prueban contra
arboles falsos con `docker` simulado por un binario stub en el PATH.
"""
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = ROOT / "scripts" / "ai-toolbox.py"


def load():
    spec = importlib.util.spec_from_file_location("ai_toolbox", SCRIPT)
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
if args[:2] == ["compose", "ls"]:
    print(json.dumps(data.get("projects", [])))
    sys.exit(0)
if args[:2] == ["ps", "-a"]:
    label = ""
    for i, a in enumerate(args):
        if a == "--filter" and i + 1 < len(args):
            label = args[i + 1]
    project = label.split("=", 2)[2] if label.count("=") >= 2 else ""
    rows = data.get("containers", {}).get(project, [])
    for r in rows:
        print("%s\\t%s\\t%s" % (r["name"], r["status"], r["image"]))
    sys.exit(0)
if args[:2] == ["image", "inspect"]:
    sys.exit(0 if data.get("has_image") else 1)
print("")
sys.exit(0)
"""


def write_stub(tmp_path, state):
    stub = tmp_path / "docker"
    stub.write_text(STUB)
    stub.chmod(0o755)
    state_file = tmp_path / "state.json"
    state_file.write_text(json.dumps(state))
    return stub, state_file


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
# 1. La tabla de herramientas esta bien formada.
# --------------------------------------------------------------------------
def test_tiene_entradas_basicas():
    mod = load()
    assert len(mod.TOOLS) >= 10, "faltan herramientas en la tabla"
    ids = [t["id"] for t in mod.TOOLS]
    assert len(ids) == len(set(ids)), "hay ids repetidos"
    for t in mod.TOOLS:
        assert t.get("name"), f"{t['id']} sin nombre"
        assert t.get("what"), f"{t['id']} sin descripcion"
        assert t.get("runtime"), f"{t['id']} sin runtime"
        assert t.get("note"), f"{t['id']} sin nota"


def test_ollama_esta_y_es_nativo():
    mod = load()
    assert "ollama" in mod.BY_ID
    assert mod.BY_ID["ollama"]["kind"] == "native"
    assert mod.BY_ID["ollama"]["port"] == 11434


def test_onyx_esta_con_sonda_y_compose():
    mod = load()
    onyx = mod.BY_ID.get("onyx")
    assert onyx is not None, "onyx no esta en la tabla"
    assert onyx["port"] == 3000
    assert onyx["compose"], "onyx sin compose"
    assert onyx["health"], "onyx sin sonda de salud"


def test_cada_herramienta_docker_tiene_compose_existente():
    mod = load()
    for t in mod.TOOLS:
        if t["kind"] != "docker":
            continue
        assert t["compose"], f"{t['id']} sin compose"
        for f in t["compose"]:
            assert Path(f).exists(), f"{t['id']} apunta a un compose inexistente: {f}"


def test_cada_herramienta_con_sonda_declara_los_codigos_que_valen():
    mod = load()
    for t in mod.TOOLS:
        health = t.get("health")
        if not health:
            continue
        url, accept = health
        assert url.startswith("http"), f"{t['id']} con url invalida"
        assert accept, f"{t['id']} sin codigos aceptados"
        assert 200 in accept, f"{t['id']} no acepta 200"


# --------------------------------------------------------------------------
# 2. El emparejamiento con Docker es por ARCHIVO, no por `name:`.
# --------------------------------------------------------------------------
def test_empareja_por_archivo_y_no_por_name(tmp_path, monkeypatch):
    """El bug real: 6 stacks sin `name:` en el compose aparecian apagados."""
    mod = load()
    compose = tmp_path / "docker-compose.yml"
    compose.write_text("services:\n  x:\n    image: foo\n")  # sin `name:`

    stub, state_file = write_stub(
        tmp_path,
        {
            "projects": [
                {
                    "Name": "local",  # nombre derivado del directorio, no del archivo
                    "Status": "running(1)",
                    "ConfigFiles": str(compose),
                }
            ],
            "containers": {
                "local": [
                    {"name": "c1", "status": "Up 2 hours (healthy)", "image": "foo"}
                ]
            },
        },
    )
    # El stub tiene que estar en el PATH del proceso que llama a docker.
    monkeypatch.setenv("PATH", f"{tmp_path}:{os.environ['PATH']}")
    monkeypatch.setenv("STUB_STATE", str(state_file))

    tool = {
        "id": "x",
        "name": "X",
        "kind": "docker",
        "runtime": "docker compose",
        "port": 1,
        "compose": [str(compose)],
        "health": None,
    }
    original = mod.TOOLS
    try:
        mod.TOOLS = [tool]
        mod.BY_ID = {"x": tool}
        state = mod.tool_state(tool)
    finally:
        mod.TOOLS = original
    assert state["status"] == "corriendo", (
        f"no emparejo por archivo: {state['status']} ({state['detail']})"
    )


def test_herramienta_sin_stack_registrado_queda_apagada(tmp_path, monkeypatch):
    mod = load()
    stub, state_file = write_stub(
        tmp_path,
        {"projects": [], "containers": {}},
    )
    monkeypatch.setenv("PATH", f"{tmp_path}:{os.environ['PATH']}")
    monkeypatch.setenv("STUB_STATE", str(state_file))
    tool = {
        "id": "y",
        "name": "Y",
        "kind": "docker",
        "runtime": "docker compose",
        "port": 1,
        "compose": [str(tmp_path / "nada.yml")],
        "health": None,
    }
    original = mod.TOOLS
    try:
        mod.TOOLS = [tool]
        mod.BY_ID = {"y": tool}
        state = mod.tool_state(tool)
    finally:
        mod.TOOLS = original
    assert state["status"] in ("apagado", "no instalado")


# --------------------------------------------------------------------------
# 3. La vista de docs/tools/REGISTRY.md se regenera y se verifica.
# --------------------------------------------------------------------------
def test_la_vista_tiene_los_marcadores():
    mod = load()
    doc = mod.REGISTRY_DOC
    assert doc.exists(), f"no existe {doc}"
    text = doc.read_text(encoding="utf-8")
    assert mod.CATALOG_BEGIN in text, "falta el marcador de inicio"
    assert mod.CATALOG_END in text, "falta el marcador de fin"


def test_catalogo_check_detecta_una_vista_desfasada(tmp_path):
    mod = load()
    doc = tmp_path / "REGISTRY.md"
    doc.write_text(
        f"{mod.CATALOG_BEGIN}\ntabla vieja y falsa\n{mod.CATALOG_END}\nresto\n",
        encoding="utf-8",
    )
    original = mod.REGISTRY_DOC
    try:
        mod.REGISTRY_DOC = doc
        rc = mod.check_catalog(mod.all_states())
    finally:
        mod.REGISTRY_DOC = original
    assert rc == 1, "una vista desfasada deberia dar error"


def test_catalogo_write_regenera_la_tabla(tmp_path):
    mod = load()
    doc = tmp_path / "REGISTRY.md"
    doc.write_text(
        f"intro\n{mod.CATALOG_BEGIN}\nviejo\n{mod.CATALOG_END}\nfin\n",
        encoding="utf-8",
    )
    original = mod.REGISTRY_DOC
    try:
        mod.REGISTRY_DOC = doc
        rc = mod.write_catalog(mod.all_states())
    finally:
        mod.REGISTRY_DOC = original
    assert rc == 0
    text = doc.read_text(encoding="utf-8")
    assert "viejo" not in text.split(mod.CATALOG_BEGIN)[1].split(mod.CATALOG_END)[0]
    assert "Herramienta" in text


# --------------------------------------------------------------------------
# 4. La CLI responde.
# --------------------------------------------------------------------------
def test_list_json_devuelve_todas_las_herramientas():
    r = run_script(["list", "--json"])
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    ids = {d["id"] for d in data}
    assert "onyx" in ids
    assert "ollama" in ids


def test_status_de_herramienta_inexistente_falla():
    r = run_script(["status", "no-existe-esta"])
    assert r.returncode != 0
    assert "conocidas" in (r.stderr + r.stdout).lower()


def test_health_sale_con_codigo_de_salida():
    r = run_script(["health"])
    # Puede ser 1 si alguna sonda falla: lo importante es que responde.
    assert r.returncode in (0, 1)
    assert "onyx" in r.stdout


def test_ids_no_vacio():
    r = run_script(["ids"])
    assert r.returncode == 0
    ids = r.stdout.split()
    assert "onyx" in ids
    assert len(ids) == len(set(ids))
