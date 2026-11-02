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
  2. Los codigos HTTP que cuentan como "vivo" son POR HERRAMIENTA (un 401
     de una herramienta con auth es vivo; un 502 de openhands es caido).
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
    # NO se afirma un NUMERO de herramientas: el registro cambia (una
    # herramienta se descarto, se sumo, se borro) y un conteo fijo rompe el
    # CI sin que nadie haya roto nada. Lo que importa es que el registro
    # NO este vacio y que las herramientas CORE esten. El mismo criterio
    # que rompio el CI dos veces con rutas del host (ver CHANGELOG 2026-10-20).
    assert mod.TOOLS, "el registro de herramientas esta vacio"
    ids = [t["id"] for t in mod.TOOLS]
    assert len(ids) == len(set(ids)), "hay ids repetidos"
    for t in mod.TOOLS:
        assert t.get("name"), f"{t['id']} sin nombre"
        assert t.get("what"), f"{t['id']} sin descripcion"
        assert t.get("runtime"), f"{t['id']} sin runtime"
        assert t.get("note"), f"{t['id']} sin nota"


def test_las_herramientas_core_estan():
    """El nucleo del stack. Si algo falta, es un bug real, no un cambio de catalogo."""
    mod = load()
    for hid in ("ollama", "vane"):
        assert hid in mod.BY_ID, f"falta la herramienta core '{hid}'"


def test_browser_use_no_esta_y_no_quedan_ramas_muertas():
    """browser-use salio del stack el 2026-11-02: ni la entrada ni el codigo.

    Se borro de verdad, no se desregistro: la imagen y los repos no existian.
    La tabla no puede listar una herramienta que no se puede levantar, y el
    codigo no puede conservar ramas para un `kind` que ya no tiene entradas.
    """
    mod = load()
    ids = [t["id"] for t in mod.TOOLS]
    assert "browser-use" not in ids, "browser-use volvio a la tabla"
    assert "browser-use-ui" not in ids, "browser-use-ui volvio a la tabla"
    assert not any(t["kind"] == "mcp" for t in mod.TOOLS), (
        "quedan entradas kind=mcp: browser-use era la unica, si vuelve el kind "
        "hay que devolver tambien sus ramas en ai-toolbox.py"
    )


def test_ollama_esta_y_es_nativo():
    mod = load()
    assert "ollama" in mod.BY_ID
    assert mod.BY_ID["ollama"]["kind"] == "native"
    assert mod.BY_ID["ollama"]["port"] == 11434


def test_vane_esta_con_sonda_y_compose():
    mod = load()
    vane = mod.BY_ID.get("vane")
    assert vane is not None, "vane no esta en la tabla"
    assert vane["port"] == 3005
    assert vane["compose"], "vane sin compose"
    assert vane["health"], "vane sin sonda de salud"


def test_las_retiradas_no_estan_en_el_catalogo():
    """Onyx (2026-10-27) y LiteLLM (2026-10-22) se retiraron del stack.

    Que no reaparezcan es parte del contrato: una entrada que vuelve sola
    reinstala el stack en el proximo `up`.
    """
    mod = load()
    for hid in ("onyx", "litellm"):
        assert hid not in mod.BY_ID, f"la herramienta retirada '{hid}' volvio al catalogo"


def test_cada_herramienta_docker_declara_un_compose():
    """FORMA, no existencia.

    POR QUE (2026-10-20). Esta asercion afirmaba `Path(f).exists()` sobre las
    rutas absolutas de la Mac Mini, y eso ROMPIO el CI: el CI corre en Linux, en
    un checkout distinto, y `projects/` esta ignorado por `.gitignore`. 378
    tests pasaron y ese fallo. El commit que lo arreglo (3387a58f65) termino
    borrando el registro entero, cuando el defecto era del test, no del
    registro.

    Un compose puede estar ausente en la maquina donde corre el test (la
    herramienta no esta instalada) y el registro seguir siendo correcto: la
    tabla declara COMO se levanta, y el estado real lo decide la sonda. Lo que
    el test tiene que afirmar es que la DECLARACION es coherente: si declara
    compose, la ruta tiene que ser plausible y el archivo tiene que nombrarse
    como un compose.
    """
    mod = load()
    for t in mod.TOOLS:
        if t["kind"] != "docker":
            continue
        assert t["compose"], f"{t['id']} sin compose"
        for f in t["compose"]:
            assert f.endswith((".yml", ".yaml")), (
                f"{t['id']} apunta a algo que no parece un compose: {f}"
            )
            assert Path(f).is_absolute(), (
                f"{t['id']} declara una ruta relativa: {f}"
            )


def test_cada_herramienta_declara_como_se_levanta():
    """Toda entrada tiene un camino para levantarse: compose, `paths` o `up`."""
    mod = load()
    for t in mod.TOOLS:
        if t["kind"] == "docker":
            assert t["compose"], f"{t['id']} sin compose"
        elif t["kind"] == "native":
            assert t.get("up"), f"{t['id']} nativo sin comando `up`"
            assert t.get("down"), f"{t['id']} nativo sin comando `down`"
        else:
            raise AssertionError(f"{t['id']} con kind desconocido: {t['kind']}")


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


def test_herramienta_bajo_demanda_apagada_no_parece_como_falla(tmp_path, monkeypatch):
    """Una herramienta bajo demanda apagada es el estado NORMAL, no una caida.

    Sin esto, un `list` mostra "apagado" y no se distingue de un servicio que
    deberia estar vivo y no lo esta.
    """
    mod = load()
    stub, state_file = write_stub(
        tmp_path,
        {"projects": [], "containers": {}},
    )
    monkeypatch.setenv("PATH", f"{tmp_path}:{os.environ['PATH']}")
    monkeypatch.setenv("STUB_STATE", str(state_file))
    tool = {
        "id": "bd",
        "name": "Bajo demanda",
        "kind": "docker",
        "runtime": "docker compose",
        "port": 1,
        "compose": [str(tmp_path / "nada.yml")],
        "health": None,
        "on_demand": True,
    }
    original = mod.TOOLS
    try:
        mod.TOOLS = [tool]
        mod.BY_ID = {"bd": tool}
        state = mod.tool_state(tool)
    finally:
        mod.TOOLS = original
    assert state["status"] == "bajo demanda"
    assert "up" in state["detail"]


def test_nativa_sin_instalacion_dice_no_instalado(tmp_path, monkeypatch):
    """Una nativa cuyo clon no esta NO puede decir 'apagado'.

    'apagado' significa que deberia estar corriendo y no esta. Una herramienta
    cuya instalacion no esta en el disco es 'no instalado': son clases distintas
    y confundirlas hace que un clon borrado parezca una falla.
    """
    mod = load()
    stub, state_file = write_stub(tmp_path, {"projects": [], "containers": {}})
    monkeypatch.setenv("PATH", f"{tmp_path}:{os.environ['PATH']}")
    monkeypatch.setenv("STUB_STATE", str(state_file))
    tool = {
        "id": "nat",
        "name": "Nativa",
        "kind": "native",
        "runtime": "nativo",
        "port": 1,
        "compose": None,
        "paths": [str(tmp_path / "no-existe")],
        "health": None,
    }
    original = mod.TOOLS
    try:
        mod.TOOLS = [tool]
        mod.BY_ID = {"nat": tool}
        state = mod.tool_state(tool)
    finally:
        mod.TOOLS = original
    assert state["status"] == "no instalado"
    assert "falta" in state["detail"]


def test_nativa_sin_paths_no_se_declara_no_instalada(tmp_path, monkeypatch):
    """Sin `paths` no se puede afirmar que no este instalada (Ollama es una app)."""
    mod = load()
    stub, state_file = write_stub(tmp_path, {"projects": [], "containers": {}})
    monkeypatch.setenv("PATH", f"{tmp_path}:{os.environ['PATH']}")
    monkeypatch.setenv("STUB_STATE", str(state_file))
    tool = {
        "id": "nat",
        "name": "Nativa",
        "kind": "native",
        "runtime": "nativo",
        "port": 1,
        "compose": None,
        "health": None,
    }
    original = mod.TOOLS
    try:
        mod.TOOLS = [tool]
        mod.BY_ID = {"nat": tool}
        state = mod.tool_state(tool)
    finally:
        mod.TOOLS = original
    assert state["status"] != "no instalado"


def test_bajo_demanda_hace_down_real_y_no_stop(tmp_path, monkeypatch):
    """`down` de una bajo demanda tiene que ser `docker compose down`.

    `stop` deja la politica de restart intacta: la herramienta vuelve sola en el
    proximo reinicio de Docker. Para una bajo demanda, `down` es lo unico que
    la deja apagada de verdad.
    """
    mod = load()
    calls = []
    monkeypatch.setattr(mod, "run", lambda cmd, timeout=60: (calls.append(cmd), (0, ""))[1])
    tool = {
        "id": "bd",
        "name": "Bajo demanda",
        "kind": "docker",
        "runtime": "docker compose",
        "port": 1,
        "compose": [str(tmp_path / "c.yml")],
        "health": None,
        "on_demand": True,
    }
    mod.do_down(tool)
    assert calls, "no se ejecuto ningun comando"
    assert "down" in calls[0], f"se esperaba 'down', se ejecuto: {calls[0]}"
    assert "stop" not in calls[0], f"se ejecuto 'stop' en vez de 'down': {calls[0]}"


def test_down_normal_conserva_la_politica_de_restart(tmp_path, monkeypatch):
    """Una herramienta normal sigue usando `stop`: conserva containers y volumenes.

    El `down` real es solo para las bajo demanda, que son las que se apagan
    de verdad.
    """
    mod = load()
    calls = []
    monkeypatch.setattr(mod, "run", lambda cmd, timeout=60: (calls.append(cmd), (0, ""))[1])
    tool = {
        "id": "normal",
        "name": "Normal",
        "kind": "docker",
        "runtime": "docker compose",
        "port": 1,
        "compose": [str(tmp_path / "c.yml")],
        "health": None,
    }
    mod.do_down(tool)
    assert calls and "stop" in calls[0], f"se esperaba 'stop', se ejecuto: {calls}"


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
    assert "vane" in ids
    assert "ollama" in ids


def test_status_de_herramienta_inexistente_falla():
    r = run_script(["status", "no-existe-esta"])
    assert r.returncode != 0
    assert "conocidas" in (r.stderr + r.stdout).lower()


def test_health_sale_con_codigo_de_salida():
    r = run_script(["health"])
    # Puede ser 1 si alguna sonda falla: lo importante es que responde.
    assert r.returncode in (0, 1)
    assert "vane" in r.stdout


def test_ids_no_vacio():
    r = run_script(["ids"])
    assert r.returncode == 0
    ids = r.stdout.split()
    assert "vane" in ids
    assert len(ids) == len(set(ids))


# --------------------------------------------------------------------------
# 5. `up` dice DONDE queda la herramienta y comprueba que de verdad sirva.
#    Pedido real de Gonzo: "no me dice en que puerto esta corriendo".
# --------------------------------------------------------------------------
def test_service_url_se_deriva_de_la_sonda_sin_path():
    """La URL de la UI no es la de la sonda: /api/health vive en otra ruta."""
    mod = load()
    tool = {
        "id": "x",
        "name": "X",
        "kind": "docker",
        "runtime": "docker compose",
        "port": 3005,
        "compose": [],
        "health": ("http://localhost:3005/api/health", [200]),
    }
    assert mod.service_url(tool) == "http://localhost:3005"


def test_service_url_cae_al_puerto_cuando_no_hay_sonda():
    mod = load()
    tool = {
        "id": "x",
        "name": "X",
        "kind": "docker",
        "runtime": "docker compose",
        "port": 3005,
        "compose": [],
        "health": None,
    }
    assert mod.service_url(tool) == "http://localhost:3005"


def test_service_url_none_sin_puerto_ni_sonda():
    mod = load()
    tool = {
        "id": "x",
        "name": "X",
        "kind": "docker",
        "runtime": "docker compose",
        "port": None,
        "compose": [],
        "health": None,
    }
    assert mod.service_url(tool) is None


def test_report_started_imprime_puerto_url_y_sonda(capsys, monkeypatch):
    """`up` tiene que decir el puerto, la URL y el estado real de la sonda."""
    mod = load()
    monkeypatch.setattr(
        mod,
        "wait_for_health",
        lambda tool, **kw: {
            "url": "http://localhost:3005/",
            "code": 200,
            "ok": True,
            "detail": None,
        },
    )
    tool = {
        "id": "vane",
        "name": "Vane",
        "kind": "docker",
        "runtime": "docker compose",
        "port": 3005,
        "compose": [],
        "health": ("http://localhost:3005/", [200]),
    }
    mod.report_started(tool)
    out = capsys.readouterr().out
    assert "3005" in out, f"no dice el puerto: {out}"
    assert "http://localhost:3005" in out, f"no dice la url: {out}"
    assert "HTTP 200" in out, f"no dice el estado de la sonda: {out}"


def test_report_started_avisa_cuando_la_sonda_no_responde(capsys, monkeypatch):
    """Si la sonda no responde, lo dice: 'corriendo' no es 'sirviendo'."""
    mod = load()
    monkeypatch.setattr(
        mod,
        "wait_for_health",
        lambda tool, **kw: {
            "url": "http://localhost:3005/",
            "code": None,
            "ok": False,
            "detail": "ConnectionRefusedError",
        },
    )
    tool = {
        "id": "vane",
        "name": "Vane",
        "kind": "docker",
        "runtime": "docker compose",
        "port": 3005,
        "compose": [],
        "health": ("http://localhost:3005/", [200]),
    }
    mod.report_started(tool)
    out = capsys.readouterr().out
    assert "AUN NO RESPONDE" in out, f"no advierte que no responde: {out}"


def test_wait_for_health_reintenta_hasta_que_responde(monkeypatch):
    """Un servicio recien arrancado tarda: la sonda se reintenta."""
    mod = load()
    monkeypatch.setattr(mod.time, "sleep", lambda s: None)
    calls = {"n": 0}

    def fake_probe(tool):
        calls["n"] += 1
        return {
            "url": "http://x/",
            "code": 200 if calls["n"] >= 3 else None,
            "ok": calls["n"] >= 3,
            "detail": None if calls["n"] >= 3 else "ConnectionRefusedError",
        }

    monkeypatch.setattr(mod, "probe_health", fake_probe)
    tool = {
        "id": "x",
        "name": "X",
        "kind": "docker",
        "runtime": "docker compose",
        "port": 1,
        "compose": [],
        "health": ("http://x/", [200]),
    }
    result = mod.wait_for_health(tool, attempts=5, delay=0)
    assert result["ok"] is True
    assert calls["n"] == 3, f"no reintento: {calls['n']} intentos"
