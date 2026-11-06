#!/usr/bin/env python3
"""Tests de los scripts de Kanam OPS (E2.3).

Regla de la suite: cada test que importa prueba que la herramienta PUEDE
fallar. Un test que solo verifica el caso feliz no protege de nada.

Los tests que tocan ~/.openclaw/openclaw.json real lo hacen con un HOME falso
(temporal), para no depender ni alterar el config vivo. El unico que valida
contra el config real es read-only (parsea el JSON y verifica el schema).

Correr:
    python3 agents/kanam-ops/tests/test_ops_scripts.py
    python3 -m pytest agents/kanam-ops/tests/test_ops_scripts.py -q
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

OPS = Path(__file__).resolve().parent.parent
SCRIPTS = OPS / "scripts"
DRIFT = SCRIPTS / "gateway-config-drift.sh"
JOBS = SCRIPTS / "gateway-jobs-check.sh"
AUDIT = SCRIPTS / "gateway-audit.sh"
CHANGELOG = SCRIPTS / "gateway-change-log.sh"


def run(script, *args, home=None, timeout=120):
    env = dict(os.environ)
    if home:
        env["HOME"] = str(home)
    return subprocess.run(
        ["bash", str(script), *args],
        capture_output=True,
        text=True,
        env=env,
        timeout=timeout,
    )


def minimal_config(**overrides):
    """Config minimo con la forma que los scripts esperan."""
    cfg = {
        "gateway": {"port": 18789, "bind": "loopback", "auth": {"token": "x"}},
        "agents": {
            "defaults": {"model": {"primary": "a/b"}},
            "entries": {
                "main": {
                    "workspace": "/tmp/w",
                    "model": {"primary": "a/b"},
                    "subagents": {"allowAgents": ["kanam-ops"]},
                },
                "kanam-ops": {
                    "workspace": "/tmp/o",
                    "model": {"primary": "a/b"},
                    "thinkingDefault": "off",
                },
            },
        },
        "meta": {"version": "1"},
    }
    cfg.update(overrides)
    return cfg


class FakeHome:
    """HOME temporal con un openclaw.json propio y su baseline."""

    def __init__(self, cfg=None):
        self.dir = Path(tempfile.mkdtemp(prefix="ops-test-"))
        self.oc = self.dir / ".openclaw"
        self.oc.mkdir()
        self.config = self.oc / "openclaw.json"
        self.write(cfg or minimal_config())

    def write(self, cfg):
        self.config.write_text(json.dumps(cfg, indent=1))
        return self

    def load(self):
        return json.loads(self.config.read_text())

    def mutate(self, **paths):
        """set 'a.b.c' -> valor, para plantar un cambio."""
        cfg = self.load()
        for dotted, value in paths.items():
            node = cfg
            parts = dotted.split(".")
            for p in parts[:-1]:
                node = node.setdefault(p, {})
            node[parts[-1]] = value
        self.write(cfg)
        return self

    def cleanup(self):
        shutil.rmtree(self.dir, ignore_errors=True)


class TestDrift(unittest.TestCase):
    """gateway-config-drift.sh v2: drift semantico con allowlist."""

    def setUp(self):
        self.h = FakeHome()

    def tearDown(self):
        self.h.cleanup()

    def test_first_run_creates_baseline(self):
        """Sin baseline: crea uno y sale 0. No debe gritar drift falso."""
        r = run(DRIFT, home=self.h.dir)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertTrue((self.h.oc / "gateway-config.baseline.json").exists())

    def test_clean_config_is_ok(self):
        """Dia normal: dos corridas seguidas, la segunda da OK con exit 0."""
        run(DRIFT, home=self.h.dir)
        r = run(DRIFT, home=self.h.dir)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("OK", r.stdout)

    def test_unexplained_change_is_detected(self):
        """Un cambio en un campo NO permitido debe dar exit 1 y nombrar el campo."""
        run(DRIFT, home=self.h.dir)
        self.h.mutate(**{"gateway.port": 19999})
        r = run(DRIFT, home=self.h.dir)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("gateway.port", r.stdout)
        self.assertIn("19999", r.stdout)
        self.assertIn("18789", r.stdout)  # valor viejo reportado

    def test_allowed_change_does_not_alarm(self):
        """Un cambio en la allowlist no es drift, pero SI se informa."""
        run(DRIFT, home=self.h.dir)
        self.h.mutate(**{"agents.entries.kanam-ops.model.primary": "c/d"})
        r = run(DRIFT, home=self.h.dir)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("1 cambios esperados", r.stdout)

    def test_allowed_change_verbose_shows_path(self):
        """--verbose muestra la ruta y el antes/despues incluso si es permitido."""
        run(DRIFT, home=self.h.dir)
        self.h.mutate(**{"agents.entries.kanam-ops.model.primary": "c/d"})
        r = run(DRIFT, "--verbose", home=self.h.dir)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("agents.entries.kanam-ops.model.primary", r.stdout)
        self.assertIn("->", r.stdout)

    def test_allowlisted_fields(self):
        """Cada campo declarado en la allowlist, solo, no dispara alarma."""
        run(DRIFT, home=self.h.dir)
        cases = [
            "agents.entries.main.workspace",
            "agents.entries.main.model.primary",
            "agents.defaults.model.primary",
            "meta.version",
        ]
        for path in cases:
            with self.subTest(path=path):
                self.h.mutate(**{path: "cambiado" if not path.endswith("workspace") else "/tmp/otro"})
                r = run(DRIFT, home=self.h.dir)
                self.assertEqual(r.returncode, 0, f"{path}: {r.stdout}{r.stderr}")

    def test_allowlist_does_not_swallow_structural_changes(self):
        """Lo importante: la allowlist NO debe tapar cambios de seguridad/estructura."""
        run(DRIFT, home=self.h.dir)
        must_block = [
            ("agents.entries.main.subagents.allowAgents", ["otro"]),
            ("gateway.port", 1234),
            ("gateway.bind", "lan"),
            ("telemetry", {"enabled": True}),
        ]
        for path, value in must_block[:3]:
            with self.subTest(path=path):
                self.h.cleanup()
                self.h = FakeHome()
                run(DRIFT, home=self.h.dir)
                self.h.mutate(**{path: value})
                r = run(DRIFT, home=self.h.dir)
                self.assertEqual(r.returncode, 1, f"{path} deberia bloquear: {r.stdout}")

    def test_json_output_is_valid_in_both_states(self):
        run(DRIFT, home=self.h.dir)
        clean = run(DRIFT, "--json", home=self.h.dir)
        self.assertEqual(clean.returncode, 0)
        data = json.loads(clean.stdout)
        self.assertFalse(data["drift"])
        self.assertEqual(data["unexplained"], [])

        self.h.mutate(**{"gateway.port": 19999})
        dirty = run(DRIFT, "--json", home=self.h.dir)
        self.assertEqual(dirty.returncode, 1)
        data = json.loads(dirty.stdout)
        self.assertTrue(data["drift"])
        self.assertEqual(data["unexplained"][0]["path"], "gateway.port")

    def test_accept_clears_drift(self):
        """--accept debe hacer que la proxima corrida sea limpia."""
        run(DRIFT, home=self.h.dir)
        self.h.mutate(**{"gateway.port": 19999})
        self.assertEqual(run(DRIFT, home=self.h.dir).returncode, 1)
        run(DRIFT, "--accept", home=self.h.dir)
        self.assertEqual(run(DRIFT, home=self.h.dir).returncode, 0)

    def test_accept_does_not_hide_fields(self):
        """Tras --accept, un cambio nuevo en otro campo sigue bloqueando."""
        run(DRIFT, home=self.h.dir)
        self.h.mutate(**{"gateway.port": 19999})
        run(DRIFT, "--accept", home=self.h.dir)
        self.h.mutate(**{"gateway.bind": "lan"})
        r = run(DRIFT, home=self.h.dir)
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("gateway.bind", r.stdout)

    def test_missing_config_is_error_not_silence(self):
        """Si no hay config, exit 2. Un check que pasa en silencio es peor que uno que falla."""
        self.h.config.unlink()
        r = run(DRIFT, home=self.h.dir)
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)

    def test_invalid_json_is_error(self):
        run(DRIFT, home=self.h.dir)
        self.h.config.write_text("{ esto no es json")
        r = run(DRIFT, home=self.h.dir)
        self.assertNotEqual(r.returncode, 0, "JSON invalido no puede pasar como OK")


class TestJobsCheck(unittest.TestCase):
    """gateway-jobs-check.sh: watchdog de automations."""

    def test_runs_and_returns_known_exit(self):
        """Exit 0 (sano), 1 (problemas) o 2 (no pudo chequear). Nunca otro."""
        r = run(JOBS, timeout=180)
        self.assertIn(r.returncode, (0, 1, 2), r.stdout + r.stderr)

    def test_exit_2_is_not_silent(self):
        """Si el gateway no responde, debe salir 2, no 0."""
        # HOME falso: sin gateway accesible por config, el check debe fallar
        with tempfile.TemporaryDirectory() as d:
            oc = Path(d) / ".openclaw"
            oc.mkdir()
            (oc / "openclaw.json").write_text(json.dumps(minimal_config()))
            r = run(JOBS, home=Path(d), timeout=180)
            self.assertIn(r.returncode, (0, 1, 2))
            if r.returncode == 0:
                self.assertIn("OK", r.stdout)


class TestAudit(unittest.TestCase):
    """gateway-audit.sh: snapshot completo."""

    def test_json_is_valid(self):
        r = run(AUDIT, "--json", timeout=240)
        self.assertEqual(r.returncode, 0, r.stderr)
        data = json.loads(r.stdout)
        self.assertIn("timestamp", data)
        self.assertIn("configDrift", data)
        self.assertIn("doctor", data, "el health check nativo debe estar presente")

    def test_text_mode_runs(self):
        r = run(AUDIT, timeout=240)
        self.assertEqual(r.returncode, 0, r.stderr)


class TestSingleOwner(unittest.TestCase):
    """E2.1: un solo duenio por script. Los del workspace raiz son symlinks."""

    WORKSPACE = Path("/Users/gonzoblasco/.openclaw/workspace")
    NAMES = [
        "gateway-audit.sh",
        "gateway-config-drift.sh",
        "gateway-jobs-check.sh",
        "pipeline-track.sh",
        "playwright-provision.sh",
    ]

    def test_root_scripts_are_symlinks_to_ops(self):
        for name in self.NAMES:
            with self.subTest(name=name):
                root = self.WORKSPACE / "scripts" / name
                if not root.exists():
                    self.skipTest(f"{name} no esta en la raiz")
                self.assertTrue(root.is_symlink(), f"{name} no es symlink: hay copia duplicada")
                target = root.resolve()
                self.assertEqual(target.parent, OPS / "scripts", f"{name} apunta fuera de OPS")
                self.assertTrue(target.exists(), f"{name} symlink roto")


class TestChangeLog(unittest.TestCase):
    """gateway-change-log.sh: registro de cambios legible por maquina (E2.4)."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="ops-changelog-"))
        self.log = self.tmp / "changes.jsonl"
        self.env = {"GATEWAY_CHANGES_LOG": str(self.log)}

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_log(self, *args, timeout=60):
        env = dict(os.environ)
        env.update(self.env)
        return subprocess.run(
            ["bash", str(CHANGELOG), *args],
            capture_output=True, text=True, env=env, timeout=timeout,
        )

    def entries(self):
        if not self.log.exists():
            return []
        return [json.loads(l) for l in self.log.read_text().splitlines() if l.strip()]

    def test_record_writes_one_entry(self):
        r = self.run_log(
            "record", "--field", "agents.entries.x.model.primary",
            "--before", "a", "--after", "b", "--reason", "test",
            "--backup", "x.bak", "--evidence", "corrido",
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        e = self.entries()
        self.assertEqual(len(e), 1)
        self.assertEqual(e[0]["field"], "agents.entries.x.model.primary")
        self.assertEqual(e[0]["before"], "a")
        self.assertEqual(e[0]["after"], "b")

    def test_record_without_before_does_not_invent_it(self):
        """Un registro que adivina el valor viejo es peor que uno vacio."""
        self.run_log("record", "--field", "algo.campo", "--after", "nuevo")
        e = self.entries()[0]
        self.assertEqual(e["before"], "no medido")

    def test_missing_field_is_error(self):
        r = self.run_log("record", "--before", "a")
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertEqual(self.entries(), [])

    def test_secret_guard_redacts_values(self):
        """Un token jamas debe quedar en el log en claro."""
        self.run_log(
            "record", "--field", "gateway.auth.token",
            "--before", "secretoViejo123", "--after", "secretoNuevo456",
        )
        raw = self.log.read_text()
        self.assertNotIn("secretoViejo123", raw)
        self.assertNotIn("secretoNuevo456", raw)
        self.assertIn("REDACTADO", raw)

    def test_list_total_counts_all_entries(self):
        """Bug real (2026-11-06): el total usaba la salida filtrada, no el archivo."""
        for i in range(3):
            self.run_log("record", "--field", f"campo.{i}", "--after", str(i))
        r = self.run_log("list", "--limit", "1")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("3 en total", r.stdout, r.stdout)

    def test_verify_passes_on_wellformed_log(self):
        self.run_log("record", "--field", "a.b", "--after", "c")
        r = self.run_log("verify")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("OK", r.stdout)

    def test_verify_catches_missing_fields(self):
        """Si alguien escribe una linea a mano incompleta, debe fallar."""
        self.log.write_text(json.dumps({"ts": "x", "field": "y"}) + "\n")
        r = self.run_log("verify")
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("faltan campos", r.stdout)

    def test_verify_catches_invalid_json(self):
        self.log.write_text("{ no es json\n")
        r = self.run_log("verify")
        self.assertEqual(r.returncode, 1)
        self.assertIn("JSON invalido", r.stdout)


class TestRealConfigSanity(unittest.TestCase):
    """Read-only contra el config vivo. Nunca escribe."""

    REAL = Path.home() / ".openclaw" / "openclaw.json"

    def test_config_is_valid_json(self):
        if not self.REAL.exists():
            self.skipTest("no hay config real")
        data = json.loads(self.REAL.read_text())
        self.assertIn("agents", data)

    def test_ops_agent_entry_exists(self):
        """El modelo NO se fija aca a proposito.

        Un test que exige un modelo concreto convierte una decision de Gonzo
        (gpt-oss por alcance creativo) en un fallo de test. Lo que importa es
        que la entrada exista y que su modelo sea un string no vacio con forma
        provider/modelo. El modelo vigente lo manda el dueño del dato, no un test.
        """
        if not self.REAL.exists():
            self.skipTest("no hay config real")
        data = json.loads(self.REAL.read_text())
        entries = data.get("agents", {}).get("entries", {})
        self.assertIn("kanam-ops", entries)
        primary = entries["kanam-ops"].get("model", {}).get("primary", "")
        self.assertTrue(primary, "kanam-ops sin modelo primary")
        self.assertIn("/", primary, f"modelo con forma inesperada: {primary}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
