#!/usr/bin/env python3
"""
skill-router.py - Suggest which skill(s) to use for a given task.

Ported concept from the skill-ai-inject plugin (ClawHub), adapted to our
workspace. Two-tier matching:
  L1: keyword match (free, no LLM) - task terms hit skill descriptions.
  L2: embedding match (Ollama qwen3-embedding:0.6b) - semantic cosine similarity.

Usage:
  ./skill-router.py "<task description>"
  ./skill-router.py --top 5 "<task>"
  ./skill-router.py --list          # list available skills

Requires: Ollama running with qwen3-embedding:0.6b (embedding model).
Outputs top-N skill suggestions with score and match type.
"""

import argparse
import json
import os
import re
import sys
import urllib.request

# --- Config ---
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
SKILLS_DIR = os.path.join(WORKSPACE, "skills")
OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "qwen3-embedding:0.6b"
TOP_N = 3
L1_THRESHOLD = 1  # min keyword hits for L1 match
L2_THRESHOLD = 0.5  # cosine threshold for L2 match


def get_embedding(text: str):
    """Get embedding vector from local Ollama."""
    payload = json.dumps({"model": EMBED_MODEL, "prompt": text}).encode()
    req = urllib.request.Request(OLLAMA_URL, data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    return data.get("embedding", [])


def cosine(a, b):
    """Cosine similarity between two vectors."""
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(x * x for x in b) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)


def load_skills():
    """Load skills from SKILL.md files: {name, description, dir}."""
    skills = []
    if not os.path.isdir(SKILLS_DIR):
        return skills
    for entry in sorted(os.listdir(SKILLS_DIR)):
        skill_dir = os.path.join(SKILLS_DIR, entry)
        skmd = os.path.join(skill_dir, "SKILL.md")
        if not os.path.isdir(skill_dir) or not os.path.isfile(skmd):
            continue
        name = entry
        description = ""
        try:
            with open(skmd, "r", encoding="utf-8") as f:
                content = f.read()
            # parse YAML frontmatter description
            m = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
            if m:
                fm = m.group(1)
                dm = re.search(r"description:\s*[\"']?(.*?)[\"']?\s*$", fm, re.MULTILINE)
                if dm:
                    description = dm.group(1).strip()
            if not description:
                # fallback: first heading line
                first_h = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                description = first_h.group(1) if first_h else entry
        except Exception:
            continue
        skills.append({"name": name, "description": description, "dir": entry})
    return skills


def tokenize(text):
    """Lowercase and extract meaningful word tokens."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def keyword_match(task, skill):
    """L1: count task keyword hits in skill name+description."""
    task_tokens = tokenize(task)
    skill_text = (skill["name"] + " " + skill["description"]).lower()
    # significant tokens (ignore tiny stopwords)
    stop = {"the", "and", "for", "with", "this", "that", "use", "using",
            "when", "your", "you", "are", "how", "what", "code", "of"}
    hits = 0
    for tok in task_tokens:
        if tok in stop or len(tok) < 4:
            continue
        if tok in skill_text:
            hits += 1
    return hits


def main():
    parser = argparse.ArgumentParser(description="Suggest skills for a task")
    parser.add_argument("--task", type=str, help="Task description")
    parser.add_argument("--list", action="store_true", help="List skills")
    parser.add_argument("-n", "--top", type=int, default=TOP_N, help="Top N results")
    parser.add_argument("task_args", nargs="*", help="Task description (positional)")
    args = parser.parse_args()

    task = args.task or " ".join(args.task_args)
    skills = load_skills()

    if args.list:
        for s in skills:
            print(f"- {s['name']}: {s['description'][:80]}")
        return 0

    if not task:
        parser.error("task required")

    if not skills:
        print("No skills found in " + SKILLS_DIR, file=sys.stderr)
        return 1

    # --- L1: keyword match ---
    l1_results = []
    for s in skills:
        hits = keyword_match(task, s)
        if hits > 0:
            l1_results.append((hits, s))

    # --- L2: embedding match ---
    l2_results = []
    try:
        task_emb = get_embedding(task)
        for s in skills:
            # embed skill name + description (first 500 chars for speed)
            desc = (s["name"] + " " + s["description"])[:500]
            s_emb = get_embedding(desc)
            score = cosine(task_emb, s_emb)
            if score >= L2_THRESHOLD:
                l2_results.append((score, score, s))
    except Exception as e:
        print(f"[skill-router] L2 embedding fallo (Ollama?): {e}", file=sys.stderr)
        l2_results = []

    # --- Merge: L2 primary (semantic), L1 as tiebreak bonus ---
    merged = []
    l2_by_name = {r[2]["name"]: r[0] for r in l2_results}
    for s in skills:
        l2_score = l2_by_name.get(s["name"])
        l1_hits = next((r[0] for r in l1_results if r[1]["name"] == s["name"]), 0)
        if l2_score is not None:
            # L2 dominates; L1 keyword adds a small semantic confirmation bonus
            bonus = 0.1 if l1_hits > 0 else 0.0
            merged.append((l2_score + bonus, l2_score, l1_hits, "embed", s))
        elif l1_hits >= L1_THRESHOLD:
            # only L1 match (no semantic hit) - lower priority
            merged.append((0.3 + l1_hits * 0.05, 0, l1_hits, "keyword", s))

    merged.sort(key=lambda x: x[0], reverse=True)

    # --- Output ---
    print(f"# Skill suggestions ({len(merged)} matches, top {min(args.top, len(merged))})")
    print(f"Task: {task}\n")
    if not merged:
        print("_Sin coincidencias claras._ Considera:\n- describir la tarea con mas detalle\n- ver `--list` para skills disponibles")
        return 0
    for i, (score, l2, l1, mtype, s) in enumerate(merged[:args.top], 1):
        print(f"{i}. {s['name']}  (score={score:.2f}, {mtype}, L1={l1})")
        print(f"   {s['description'][:110]}")
        print()


if __name__ == "__main__":
    main()
