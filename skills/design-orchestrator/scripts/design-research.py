#!/usr/bin/env python3
"""
design-research.py — search UI/UX Pro design knowledge for styles, colors, typography, patterns, stack guidelines.
Usage:
  python3 design-research.py --query "fintech color palette" --domain all --max 3
  python3 design-research.py --query "form validation" --stack nextjs --max 3
  python3 design-research.py --query "minimal dashboard" --domain styles --max 3
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

MCP_URL = "http://127.0.0.1:3456/mcp"
SESSION_FILE = "/tmp/uiuxpro-session.txt"

def ensure_server_running():
    """Start the UI/UX Pro HTTP server if not already running."""
    import urllib.request
    try:
        urllib.request.urlopen(MCP_URL.replace("/mcp", "/health"), timeout=2)
        return False
    except Exception:
        pass
    proc = subprocess.Popen(
        ["npx", "-y", "ui-ux-pro-mcp", "--http"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    # Wait for health
    for _ in range(30):
        try:
            urllib.request.urlopen(MCP_URL.replace("/mcp", "/health"), timeout=1)
            return True
        except Exception:
            time.sleep(0.5)
    print("Failed to start UI/UX Pro server", file=sys.stderr)
    sys.exit(1)


def get_session_id():
    if Path(SESSION_FILE).exists():
        sid = Path(SESSION_FILE).read_text().strip()
        # Test if still valid
        import urllib.request
        try:
            req = urllib.request.Request(
                MCP_URL,
                data=json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/list"}).encode(),
                headers={"Content-Type": "application/json", "Accept": "application/json", "mcp-session-id": sid},
            )
            urllib.request.urlopen(req, timeout=3)
            return sid
        except Exception:
            pass
    # Initialize new session
    import urllib.request
    req = urllib.request.Request(
        MCP_URL,
        data=json.dumps({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
    )
    resp = urllib.request.urlopen(req, timeout=10)
    sid = resp.headers.get("mcp-session-id", "")
    if not sid:
        # Try to extract from SSE response headers
        headers = str(resp.info())
        for line in headers.split("\n"):
            if "mcp-session-id" in line.lower():
                sid = line.split(":")[-1].strip()
                break
    if not sid:
        print("Failed to get MCP session ID", file=sys.stderr)
        sys.exit(1)
    Path(SESSION_FILE).write_text(sid)
    # Send initialized notification
    notify = urllib.request.Request(
        MCP_URL,
        data=json.dumps({"jsonrpc":"2.0","method":"notifications/initialized"}).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json", "mcp-session-id": sid},
    )
    try:
        urllib.request.urlopen(notify, timeout=5)
    except Exception:
        pass
    return sid


def call_tool(tool_name, arguments, session_id):
    import urllib.request
    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments},
    }
    req = urllib.request.Request(
        MCP_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream", "mcp-session-id": session_id},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        text = resp.read().decode()
        # Parse SSE data: lines
        results = []
        for line in text.split("\n"):
            line = line.strip()
            if line.startswith("data: "):
                try:
                    msg = json.loads(line[6:])
                    if "result" in msg:
                        results.append(msg["result"])
                except json.JSONDecodeError:
                    continue
        return results[-1] if results else None


def main():
    parser = argparse.ArgumentParser(description="Search UI/UX Pro design knowledge")
    parser.add_argument("--query", required=True, help="Search query")
    parser.add_argument("--domain", default="all", help="Domain: all, styles, components, patterns, stack, platforms")
    parser.add_argument("--stack", help="Stack name for stack-specific search (react, nextjs, shadcn, vue, etc.)")
    parser.add_argument("--max", type=int, default=3, help="Max results")
    args = parser.parse_args()

    ensure_server_running()
    sid = get_session_id()

    # Map domain to tool name
    domain_tool_map = {
        "all": "search_all",
        "styles": "search_styles",
        "components": "search_components",
        "patterns": "search_patterns",
        "stack": "search_stack",
        "platforms": "search_platforms",
    }
    tool = domain_tool_map.get(args.domain, "search_all")

    arguments = {"query": args.query, "max_results": args.max}
    if tool == "search_stack":
        arguments["stack_name"] = args.stack or "react"

    result = call_tool(tool, arguments, sid)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
