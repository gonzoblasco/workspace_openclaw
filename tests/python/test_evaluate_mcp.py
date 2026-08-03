from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader, module_from_spec
from pathlib import Path

SCRIPT_PATH = Path.home() / ".openclaw/workspace/skills/mcp-orchestrator/scripts/evaluate-mcp.py"
loader = SourceFileLoader("evaluate_mcp", str(SCRIPT_PATH))
spec = spec_from_loader("evaluate_mcp", loader)
evaluate_mcp = module_from_spec(spec)
spec.loader.exec_module(evaluate_mcp)


def test_evaluate_install_decision():
    answers = {
        "native": "no",
        "open_source": "yes",
        "maintained": "yes",
        "free_tier": "yes",
        "api_key_ok": "yes",
        "stable": "yes",
        "redundant": "no",
        "risk": "no",
    }
    result = evaluate_mcp.evaluate(answers)
    assert result["decision"] == "install"


def test_evaluate_discard_on_native_coverage():
    answers = {"native": "yes"}
    result = evaluate_mcp.evaluate(answers)
    assert result["decision"] == "discard"


def test_evaluate_discard_on_free_tier_fail():
    answers = {"free_tier": "no"}
    result = evaluate_mcp.evaluate(answers)
    assert result["decision"] == "discard"


def test_evaluate_absorb_on_redundant():
    answers = {"redundant": "yes"}
    result = evaluate_mcp.evaluate(answers)
    assert result["decision"] == "absorb"


def test_evaluate_ask_on_risk():
    answers = {"risk": "yes"}
    result = evaluate_mcp.evaluate(answers)
    assert result["decision"] == "ask"
