from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader, module_from_spec
from pathlib import Path

# Load the script dynamically because its filename contains a hyphen
REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "skills/mcp-orchestrator/scripts/discover-mcp.py"
loader = SourceFileLoader("discover_mcp", str(SCRIPT_PATH))
spec = spec_from_loader("discover_mcp", loader)
discover_mcp = module_from_spec(spec)
spec.loader.exec_module(discover_mcp)


SAMPLE_README = """
# Awesome MCP Servers

## Official
- [Filesystem MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) - Access the filesystem
- [GitHub MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/github) - GitHub integration

## Community
- [Puppeteer MCP](https://github.com/anthropics/servers/tree/main/src/puppeteer) - Browser automation
"""


def test_discover_finds_match():
    results = discover_mcp.discover("github", SAMPLE_README)
    assert len(results) == 1
    assert results[0]["title"] == "GitHub MCP"
    assert "github.com" in results[0]["url"]


def test_discover_returns_empty_when_no_match():
    results = discover_mcp.discover("nonexistent-xyz", SAMPLE_README)
    assert results == []


def test_discover_case_insensitive():
    results = discover_mcp.discover("GITHUB", SAMPLE_README)
    assert len(results) == 1
