#!/usr/bin/env python3
"""quick_ratio_calculator.py — Calculate Quick Ratio (growth efficiency).

Usage:
  python3 quick_ratio_calculator.py --new-mrr 10000 --expansion 2000 --churned 3000 --contraction 500
  python3 quick_ratio_calculator.py --new-mrr 10000 --expansion 2000 --churned 3000 --json
"""

import sys
import json
import argparse


def calculate(new_mrr: float, expansion: float, churned: float, contraction: float) -> dict:
    """Calculate Quick Ratio."""
    numerator = new_mrr + expansion
    denominator = churned + contraction

    if denominator == 0:
        ratio = float("inf")
        status = "EXCELLENT"
    else:
        ratio = numerator / denominator
        if ratio < 1:
            status = "CRITICAL"
        elif ratio < 2:
            status = "WATCH"
        elif ratio < 4:
            status = "HEALTHY"
        else:
            status = "EXCELLENT"

    return {
        "quick_ratio": round(ratio, 2),
        "new_mrr": new_mrr,
        "expansion_mrr": expansion,
        "churned_mrr": churned,
        "contraction_mrr": contraction,
        "status": status,
    }


def main():
    parser = argparse.ArgumentParser(description="Quick Ratio Calculator")
    parser.add_argument("--new-mrr", type=float, required=True, help="New MRR")
    parser.add_argument("--expansion", type=float, required=True, help="Expansion MRR")
    parser.add_argument("--churned", type=float, required=True, help="Churned MRR")
    parser.add_argument("--contraction", type=float, required=True, help="Contraction MRR")
    parser.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    results = calculate(args.new_mrr, args.expansion, args.churned, args.contraction)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"📊 Quick Ratio: {results['quick_ratio']} — {results['status']}")


if __name__ == "__main__":
    main()
