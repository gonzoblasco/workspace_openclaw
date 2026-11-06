#!/usr/bin/env python3
"""check-skill-overlap.py - Detecta skills que se solapan (misma tarea = dos duenos).

Uso:
  python3 scripts/check-skill-overlap.py                  # todas las skills, modo aviso
  python3 scripts/check-skill-overlap.py --all           # igual (alias explicito)
  python3 scripts/check-skill-overlap.py --staged        # solo las SKILL.md staged vs el resto
  python3 scripts/check-skill-overlap.py --threshold 0.88
  python3 scripts/check-skill-overlap.py --blocking      # exit 1 si hay pares (usar solo tras calibrar)

Por defecto es AVISO: imprime pares por encima del umbral y sale 0.
 --blocking convierte en gate duro (para el pre-commit, mas adelante).

Dueno unico: el catalogo del runtime via `openclaw skills list --agent`.
"""
import argparse, json, os, subprocess, sys

SIM_THRESHOLD = 0.87
EMBED_MODEL = "qwen3-embedding:0.6b"
OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")


def load_catalog():
    try:
        out = subprocess.run(
            ["openclaw", "skills", "list", "--agent", os.environ.get("SKILL_ROUTER_AGENT", "main"), "--json"],
            capture_output=True, text=True, timeout=90,
        )
        if out.returncode == 0 and out.stdout.strip():
            data = json.loads(out.stdout)
            arr = data if isinstance(data, list) else data.get("skills", [])
            return [it for it in (arr or []) if it.get("name") and it.get("description")]
    except Exception as e:
        print(f"[check-skill-overlap] catalog error: {e}", file=sys.stderr)
    return None


def embed(text):
    import urllib.request
    body = json.dumps({"model": EMBED_MODEL, "prompt": text[:500]}).encode()
    req = urllib.request.Request(f"{OLLAMA}/api/embeddings", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r).get("embedding", [])


def cosine(a, b):
    if not a or not b:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = (sum(x * x for x in a) ** 0.5)
    nb = (sum(x * x for x in b) ** 0.5)
    return dot / (na * nb) if na and nb else 0.0


def staged_skill_names():
    """Skills touched in the staged diff (SKILL.md changed)."""
    try:
        out = subprocess.run(["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
                             capture_output=True, text=True, timeout=20)
    except Exception:
        return set()
    names = set()
    for line in out.stdout.splitlines():
        parts = line.strip().split("/")
        if parts and parts[-1] == "SKILL.md" and len(parts) >= 2:
            names.add(parts[-2])
    return names


def main():
    ap = argparse.ArgumentParser(description="Detect skill overlap")
    ap.add_argument("--all", action="store_true", help="Scan the whole catalog (default)")
    ap.add_argument("--staged", action="store_true", help="Only skills touched in staged diff")
    ap.add_argument("--threshold", type=float, default=SIM_THRESHOLD)
    ap.add_argument("--blocking", action="store_true", help="Exit 1 when overlaps found")
    args = ap.parse_args()

    catalog = load_catalog()
    if catalog is None:
        print("[check-skill-overlap] no catalog; skip", file=sys.stderr)
        return 0
    if len(catalog) < 2:
        return 0

    # embed once per skill
    items = []
    for it in catalog:
        try:
            vec = embed(it["name"] + " " + (it.get("description") or ""))
        except Exception as e:
            print(f"[check-skill-overlap] embed failed for {it['name']}: {e}", file=sys.stderr)
            vec = []
        items.append((it, vec))

    focus = None
    if args.staged:
        focus = staged_skill_names()

    pairs = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, va = items[i]
            b, vb = items[j]
            if focus is not None and (a["name"] not in focus and b["name"] not in focus):
                continue
            if not va or not vb:
                continue
            sim = cosine(va, vb)
            if sim >= args.threshold:
                pairs.append((sim, a["name"], b["name"]))

    pairs.sort(reverse=True)

    if pairs:
        print(f"# Skill overlap scan: {len(pairs)} pair(s) >= {args.threshold:.2f}")
        for sim, a, b in pairs[:40]:
            print(f"  {sim:.3f}  {a}  <->  {b}")
        if len(pairs) > 40:
            print(f"  ... ({len(pairs)-40} mas)")
    else:
        print(f"# Skill overlap scan: 0 pairs >= {args.threshold:.2f}")

    if args.blocking and pairs:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
