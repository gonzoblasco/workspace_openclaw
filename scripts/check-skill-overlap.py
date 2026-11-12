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
import argparse, hashlib, json, os, subprocess, sys

SIM_THRESHOLD = 0.87
EMBED_MODEL = "qwen3-embedding:0.6b"
OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

# Cache de embeddings (2026-11-12). Medido: este check tardaba 9,65 s de los
# 10,44 s del pre-commit, porque re-embeddea las 39 skills contra Ollama EN CADA
# COMMIT. El embedding depende sólo de (nombre + descripción truncada), así que
# la clave es el hash de ese texto: si nada cambió, no hay llamada.
# Ubicación: dentro de .git/ (estado del repo, no del árbol de trabajo, no se
# commitea) y se cae con `--no-cache`. Un caché que enmascara un cambio sería peor
# que la lentitud: por eso el hash cubre EXACTAMENTE el texto que se embebe.
CACHE_PATH = os.path.join(
    os.environ.get("OPENCLAW_SKILL_OVERLAP_CACHE", ""),
) if os.environ.get("OPENCLAW_SKILL_OVERLAP_CACHE") else None


def _cache_file():
    if CACHE_PATH:
        return CACHE_PATH
    try:
        git_dir = subprocess.run(["git", "rev-parse", "--git-dir"],
                                 capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:
        git_dir = ""
    base = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(base)
    if not git_dir:
        git_dir = os.path.join(root, ".git")
    return os.path.join(git_dir, "skill-overlap-cache.json")


def load_cache():
    try:
        with open(_cache_file(), encoding="utf-8") as fh:
            data = json.load(fh)
        if isinstance(data, dict) and data.get("model") == EMBED_MODEL:
            return data.get("vectors", {})
    except Exception:
        pass
    return {}


def save_cache(vectors):
    try:
        path = _cache_file()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump({"model": EMBED_MODEL, "vectors": vectors}, fh)
    except Exception as e:
        print(f"[check-skill-overlap] cache write failed: {e}", file=sys.stderr)


def text_key(text):
    return hashlib.sha256(text[:500].encode("utf-8")).hexdigest()


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


def _norm(vec):
    return sum(x * x for x in vec) ** 0.5


def cosine_pairs(items, threshold):
    """Todos los pares con similitud >= threshold, sin recomputar normas.

    La versión ingenua llamaba a `cosine()` por par (n²/2 = 15.400 pares con 176
    skills) y recalculaba la norma de CADA vector en CADA par: 47,4 M llamadas a
    `sum()` y 2,5 s de los 3,5 s del check. Normalizar una vez y usar producto
    punto baja el mismo resultado a una fracción.
    """
    norms = [_norm(v) for _, v in items]
    out = []
    n = len(items)
    for i in range(n):
        if not norms[i]:
            continue
        ai, vi = items[i][0], items[i][1]
        for j in range(i + 1, n):
            if not norms[j]:
                continue
            bj, vj = items[j][0], items[j][1]
            dot = sum(x * y for x, y in zip(vi, vj))
            sim = dot / (norms[i] * norms[j])
            if sim >= threshold:
                out.append((sim, ai["name"], bj["name"]))
    return out


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


def main(argv=None):
    import sys as _sys
    _sys.argv = [_sys.argv[0]] + (list(argv) if argv else [])
    ap = argparse.ArgumentParser(description="Detect skill overlap")
    ap.add_argument("--all", action="store_true", help="Scan the whole catalog (default)")
    ap.add_argument("--staged", action="store_true", help="Only skills touched in staged diff")
    ap.add_argument("--threshold", type=float, default=SIM_THRESHOLD)
    ap.add_argument("--blocking", action="store_true", help="Exit 1 when overlaps found")
    ap.add_argument("--own-only", action="store_true", help="Limitar a skills propias (excluir bundled/extra/custodian)")
    ap.add_argument("--no-cache", action="store_true",
                    help="Ignorar el cache de embeddings y re-embeber todo")
    args = ap.parse_args()

    catalog = load_catalog()
    if catalog is None:
        # Sin catálogo no hay nada que comparar: NO es verde (regla 1 de
        # skills/verification-gates). Antes devolvía 0 y el pre-commit no
        # distinguía "el runtime no respondió" de "no hay solapamiento".
        print("[check-skill-overlap] ERROR no se pudo cargar el catálogo; "
              "no se pudo correr (exit 3)", file=sys.stderr)
        return 3
    if args.own_only:
        catalog = [it for it in catalog
                   if not any(it.get("source", "").endswith(x)
                              for x in ("-bundled", "-extra", "-custodian"))]
    if len(catalog) < 2:
        print(f"[check-skill-overlap] ERROR catálogo con {len(catalog)} skill(s); "
              f"no hay pares que comparar (exit 3)", file=sys.stderr)
        return 3

    cache = {} if args.no_cache else load_cache()
    next_cache = {}
    reused = 0
    embedded = 0

    for it in catalog:
        text = it["name"] + " " + (it.get("description") or "")
        key = text_key(text)
        if key in cache:
            next_cache[key] = cache[key]
            reused += 1

    # embed only the ones missing from the cache
    items = []
    for it in catalog:
        text = it["name"] + " " + (it.get("description") or "")
        key = text_key(text)
        if key in next_cache:
            vec = next_cache[key]
        else:
            try:
                vec = embed(text)
                embedded += 1
            except Exception as e:
                print(f"[check-skill-overlap] embed failed for {it['name']}: {e}",
                      file=sys.stderr)
                vec = []
            next_cache[key] = vec
        items.append((it, vec))

    if not args.no_cache and embedded:
        save_cache(next_cache)
    if os.environ.get("SKILL_OVERLAP_STATS"):
        print(f"[check-skill-overlap] embebidos={embedded} reusados={reused}",
              file=sys.stderr)

    if not any(v for _, v in items):
        print("[check-skill-overlap] ERROR ningún embedding válido; "
              "no se pudo correr (exit 3)", file=sys.stderr)
        return 3

    focus = None
    if args.staged:
        focus = staged_skill_names()

    pairs = []
    if focus is None:
        pairs = cosine_pairs(items, args.threshold)
    else:
        # --staged: sólo los pares que tocan una skill staged. Acá la lista es
        # chica y el doble bucle no cuesta, pero se normaliza igual.
        norms = [_norm(v) for _, v in items]
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                a, va = items[i]
                b, vb = items[j]
                if a["name"] not in focus and b["name"] not in focus:
                    continue
                if not norms[i] or not norms[j]:
                    continue
                dot = sum(x * y for x, y in zip(va, vb))
                sim = dot / (norms[i] * norms[j])
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
