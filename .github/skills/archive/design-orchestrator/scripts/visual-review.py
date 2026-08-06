#!/usr/bin/env python3
"""
visual-review.py — visual review of UI changes using Playwright + OpenAI Vision
Usage modes:
  1. Screenshot + review a local URL:
     python3 visual-review.py --url http://localhost:3000 --edit-request "..." --out-dir ./.superdesign/assets

  2. Review existing screenshot files:
     python3 visual-review.py --before before.png --after after.png --edit-request "..."

Output: JSON with {verdict: "yes"|"no", explanation: "..."}
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

OPENAI_KEY_PATH = os.path.expanduser("~/.openclaw/secrets/openai-api-key")

def read_key():
    try:
        return Path(OPENAI_KEY_PATH).read_text().strip()
    except FileNotFoundError:
        print(f"Missing OpenAI API key at {OPENAI_KEY_PATH}", file=sys.stderr)
        sys.exit(1)


def take_screenshot(url, out_path):
    script = f"""
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={{'width': 1280, 'height': 900}})
        await page.goto('{url}', wait_until='networkidle')
        await page.screenshot(path='{out_path}', full_page=True)
        await browser.close()
asyncio.run(main())
"""
    subprocess.run([sys.executable, "-c", script], check=True)


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


import ssl
import urllib.request

def create_ssl_context():
    # macOS Python from python.org often lacks updated certs; use certifi if available,
    # otherwise fall back to unverified context for local/dev use.
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl._create_unverified_context()


def review_with_openai(before_path, after_path, edit_request, api_key):
    before_b64 = encode_image(before_path)
    after_b64 = encode_image(after_path)

    prompt = f"""You are a strict UI/UX reviewer. A developer was asked to make this UI edit:

"{edit_request}"

You are shown two screenshots: BEFORE the edit and AFTER the edit.

Decide whether the AFTER screenshot visually satisfies the edit request.

Respond in JSON format only:
{{
  "verdict": "yes" or "no",
  "explanation": "short, specific reason"
}}

Be critical but fair. If the change is not visible or not correct, return "no" and explain what is missing or wrong."""

    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{before_b64}"}},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{after_b64}"}},
                ],
            }
        ],
        "max_tokens": 500,
        "response_format": {"type": "json_object"},
    }

    import urllib.request
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    context = create_ssl_context()
    with urllib.request.urlopen(req, timeout=120, context=context) as resp:
        data = json.loads(resp.read())
        content = data["choices"][0]["message"]["content"]
        return json.loads(content)


def main():
    parser = argparse.ArgumentParser(description="Visual review of UI edits")
    parser.add_argument("--before", help="Path to before screenshot")
    parser.add_argument("--after", help="Path to after screenshot")
    parser.add_argument("--url", help="URL to screenshot for review (takes single current screenshot)")
    parser.add_argument("--edit-request", required=True, help="Description of the UI edit request")
    parser.add_argument("--out-dir", default="/tmp", help="Directory to save screenshots when using --url")
    args = parser.parse_args()

    api_key = read_key()

    if args.url:
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        after_path = out_dir / "review_current.png"
        take_screenshot(args.url, str(after_path))
        if args.before:
            before_path = args.before
        else:
            # If no before, we can only describe the current state, not compare
            print(json.dumps({
                "verdict": "unknown",
                "explanation": "Only current screenshot captured. Provide --before for a before/after review."
            }, indent=2))
            print(str(after_path))
            return
    else:
        if not args.before or not args.after:
            print("Provide both --before and --after, or --url", file=sys.stderr)
            sys.exit(1)
        before_path = args.before
        after_path = args.after

    result = review_with_openai(before_path, after_path, args.edit_request, api_key)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
