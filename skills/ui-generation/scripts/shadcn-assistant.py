#!/usr/bin/env python3
"""
shadcn-assistant.py — helper for shadcn/ui component selection and installation
Usage:
  shadcn-assistant.py --project-dir ./my-app --check
  shadcn-assistant.py --project-dir ./my-app --suggest "datepicker inside a form"
  shadcn-assistant.py --project-dir ./my-app --install button card dialog
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

POPULAR_COMPONENTS = [
    "accordion", "alert", "alert-dialog", "aspect-ratio", "avatar", "badge",
    "breadcrumb", "button", "calendar", "card", "carousel", "chart", "checkbox",
    "collapsible", "combobox", "command", "context-menu", "data-table",
    "date-picker", "dialog", "direction", "drawer", "dropdown-menu", "empty",
    "field", "hover-card", "input", "input-group", "input-otp", "kbd", "label",
    "menubar", "navigation-menu", "pagination", "popover", "progress",
    "radio-group", "resizable", "scroll-area", "select", "separator", "sheet",
    "sidebar", "skeleton", "slider", "sonner", "switch", "table", "tabs",
    "textarea", "toast", "toggle", "toggle-group", "tooltip", "typography",
]

POPULAR_BLOCKS = [
    "dashboard-01", "dashboard-02", "dashboard-03", "dashboard-04", "dashboard-05",
    "dashboard-06", "dashboard-07", "sidebar-01", "sidebar-02", "sidebar-03",
    "sidebar-04", "sidebar-05", "sidebar-06", "sidebar-07", "sidebar-08",
    "login-01", "login-02", "login-03", "login-04", "login-05",
]

SUGGESTIONS = {
    "button": ["button"],
    "form input": ["input", "label", "button"],
    "form": ["form", "input", "label", "button", "select", "textarea", "checkbox", "radio-group", "switch"],
    "modal": ["dialog", "button"],
    "dialog": ["dialog", "button"],
    "dropdown": ["dropdown-menu", "button"],
    "select": ["select"],
    "navigation": ["navigation-menu", "breadcrumb", "tabs"],
    "table": ["table"],
    "data table": ["data-table"],
    "chart": ["chart"],
    "datepicker": ["date-picker", "calendar", "popover"],
    "date picker": ["date-picker", "calendar", "popover"],
    "calendar": ["calendar"],
    "tabs": ["tabs"],
    "sidebar": ["sidebar", "button", "separator"],
    "toast": ["toast", "sonner"],
    "notification": ["toast", "sonner"],
    "accordion": ["accordion"],
    "alert": ["alert"],
    "card": ["card"],
    "carousel": ["carousel"],
    "slider": ["slider"],
    "dashboard": ["sidebar", "card", "chart", "table", "tabs"],
    "login": ["card", "input", "label", "button"],
}


def detect_runtime(project_dir: Path):
    if (project_dir / "bun.lockb").exists() or (project_dir / "bun.lock").exists():
        return "bunx"
    if (project_dir / "pnpm-lock.yaml").exists():
        return "pnpm dlx"
    if (project_dir / "yarn.lock").exists():
        return "yarn dlx"
    return "npx"


def check_shadcn(project_dir: Path):
    components_json = project_dir / "components.json"
    if not components_json.exists():
        return {"initialized": False, "message": "No components.json found. Run: npx shadcn@latest init"}
    try:
        data = json.loads(components_json.read_text())
        return {"initialized": True, "data": data}
    except Exception as e:
        return {"initialized": False, "message": f"Error reading components.json: {e}"}


def suggest_components(description: str):
    desc = description.lower()
    matches = []
    # Specific multi-word matches first
    specific_keywords = ["date picker", "datepicker", "data table", "input group", "radio group", "toggle group", "alert dialog", "context menu", "dropdown menu", "hover card", "navigation menu", "scroll area"]
    for keyword in specific_keywords:
        if keyword in desc:
            matches.extend(SUGGESTIONS.get(keyword, []))
    # Then single-word matches
    for keyword, components in SUGGESTIONS.items():
        if keyword not in specific_keywords and keyword in desc:
            matches.extend(components)
    if not matches:
        matches = ["button", "card", "dialog", "input", "tabs"]
    return list(dict.fromkeys(matches))  # dedupe preserving order


def install_command(runtime: str, components: list, blocks: list):
    parts = []
    if components:
        parts.append(f"{runtime} shadcn@latest add {' '.join(components)}")
    if blocks:
        parts.append(f"{runtime} shadcn@latest add {' '.join(f'block/{b}' for b in blocks)}")
    return parts


def run_command(project_dir: Path, commands: list, dry_run: bool):
    if dry_run:
        return {"dry_run": True, "commands": commands}
    results = []
    for cmd in commands:
        result = subprocess.run(cmd, cwd=project_dir, shell=True, capture_output=True, text=True)
        results.append({"command": cmd, "returncode": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
    return {"dry_run": False, "results": results}


def main():
    parser = argparse.ArgumentParser(description="shadcn/ui assistant")
    parser.add_argument("--project-dir", default=".", help="Project root directory")
    parser.add_argument("--check", action="store_true", help="Check shadcn initialization")
    parser.add_argument("--list-components", action="store_true", help="List popular components")
    parser.add_argument("--list-blocks", action="store_true", help="List popular blocks")
    parser.add_argument("--suggest", help="Suggest components for a use case")
    parser.add_argument("--install", nargs="+", help="Install one or more components/blocks")
    parser.add_argument("--dry-run", action="store_true", help="Print install commands without running")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()

    if args.check:
        print(json.dumps(check_shadcn(project_dir), indent=2))
        return

    if args.list_components:
        print(json.dumps({"components": POPULAR_COMPONENTS}, indent=2))
        return

    if args.list_blocks:
        print(json.dumps({"blocks": POPULAR_BLOCKS}, indent=2))
        return

    if args.suggest:
        components = suggest_components(args.suggest)
        runtime = detect_runtime(project_dir)
        commands = install_command(runtime, components, [])
        print(json.dumps({
            "suggestion": args.suggest,
            "components": components,
            "runtime": runtime,
            "commands": commands,
            "note": "Review before running. Use --install to execute."
        }, indent=2))
        return

    if args.install:
        runtime = detect_runtime(project_dir)
        components = [c for c in args.install if not c.startswith("block/")]
        blocks = [c.replace("block/", "") for c in args.install if c.startswith("block/")]
        commands = install_command(runtime, components, blocks)
        status = check_shadcn(project_dir)
        if not status["initialized"]:
            print(json.dumps({"error": "shadcn not initialized", "details": status}, indent=2))
            sys.exit(1)
        result = run_command(project_dir, commands, args.dry_run)
        print(json.dumps(result, indent=2))
        return

    print("Use --check, --list-components, --list-blocks, --suggest, or --install", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
