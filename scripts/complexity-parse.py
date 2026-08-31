#!/usr/bin/env python3
"""Parse complexity scores from LLM output (JSON or prose/thinking text).

Reads raw text from stdin, tries strict JSON keys first, then falls back to
extracting scores from prose like 'A: 2', 'Score: 2', 'A (Scope): 2'.

Output: JSON {"A":..,"B":..,"C":..,"D":..,"justification":".."} or ERROR:<msg>
"""
import sys
import re
import json


def grab(text, label):
    # Matches 'A: 2', 'A (Scope): 2', 'Score: 2', 'A = 2', 'A 2'
    # label is a regex like r'\bA\b' or r'Scope'
    m = re.search(label + r'[^\d]{0,20}?(\d)', text)
    return int(m.group(1)) if m else None


def main():
    text = sys.stdin.read()

    # Attempt 1: strict JSON keys
    a = re.search(r'"A"\s*:\s*(\d+)', text)
    b = re.search(r'"B"\s*:\s*(\d+)', text)
    c = re.search(r'"C"\s*:\s*(\d+)', text)
    d = re.search(r'"D"\s*:\s*(\d+)', text)
    j = re.search(r'"justification"\s*:\s*"([^"]+)"', text)
    if a and b and c and d:
        print(json.dumps({
            "A": int(a.group(1)),
            "B": int(b.group(1)),
            "C": int(c.group(1)),
            "D": int(d.group(1)),
            "justification": j.group(1) if j else "scored via LLM",
        }))
        return

    # Attempt 2: prose scores from thinking text
    a2 = grab(text, r'\bA\b') or grab(text, r'Scope')
    b2 = grab(text, r'\bB\b') or grab(text, r'Abstraction')
    c2 = grab(text, r'\bC\b') or grab(text, r'Risk')
    d2 = grab(text, r'\bD\b') or grab(text, r'Ambiguity')
    if a2 and b2 and c2 and d2:
        print(json.dumps({
            "A": a2, "B": b2, "C": c2, "D": d2,
            "justification": "parsed from thinking text",
        }))
        return

    print("ERROR: could not extract A/B/C/D from output")


if __name__ == "__main__":
    main()
