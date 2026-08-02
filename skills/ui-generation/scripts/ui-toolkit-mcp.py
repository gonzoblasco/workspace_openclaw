#!/usr/bin/env python3
"""
ui-toolkit-mcp.py — wrapper para llamar al MCP server @elsahafy/ui-toolkit-mcp
Uso: python3 ui-toolkit-mcp.py {init|list|call} [tool_name] [json_args]
"""

import subprocess
import sys
import json
import os
import threading
import queue

MCP_CMD = ["npx", "-y", "@elsahafy/ui-toolkit-mcp"]

def start_server():
    env = os.environ.copy()
    env["PATH"] = "/usr/local/bin:/usr/bin:/bin:" + env.get("PATH", "")
    return subprocess.Popen(
        MCP_CMD,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
        text=True,
        env=env,
    )

def read_responses(stream, q):
    for line in stream:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        q.put(msg)
    q.put(None)

def wait_for_response(q, req_id, timeout=30):
    import time
    start = time.time()
    while time.time() - start < timeout:
        try:
            msg = q.get(timeout=0.5)
        except queue.Empty:
            continue
        if msg is None:
            break
        if msg.get("id") == req_id:
            return msg
    return None

def send(proc, msg):
    proc.stdin.write(json.dumps(msg) + "\n")
    proc.stdin.flush()

def main():
    if len(sys.argv) < 2:
        print("Uso: ui-toolkit-mcp.py {init|list|call} [tool_name] [json_args]", file=sys.stderr)
        sys.exit(1)

    method = sys.argv[1]
    proc = start_server()
    q = queue.Queue()
    reader = threading.Thread(target=read_responses, args=(proc.stdout, q), daemon=True)
    reader.start()

    # Initialize
    send(proc, {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "openclaw", "version": "1.0"},
        },
    })
    init_resp = wait_for_response(q, 1)

    # Send initialized notification
    send(proc, {"jsonrpc": "2.0", "method": "notifications/initialized"})

    if method == "init":
        result = init_resp
    elif method == "list":
        send(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        result = wait_for_response(q, 2)
    elif method == "call":
        if len(sys.argv) < 3:
            print("Uso: ui-toolkit-mcp.py call <tool_name> [json_args]", file=sys.stderr)
            proc.terminate()
            sys.exit(1)
        tool = sys.argv[2]
        args = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
        send(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": tool, "arguments": args}})
        result = wait_for_response(q, 2)
    else:
        print(f"Método desconocido: {method}", file=sys.stderr)
        proc.terminate()
        sys.exit(1)

    proc.terminate()
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()

    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
