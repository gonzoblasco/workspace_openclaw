#!/usr/bin/env python3
"""unit_economics_simulator.py — Project SaaS metrics forward 12 months.

Usage:
  python3 unit_economics_simulator.py --mrr 50000 --growth 10 --churn 3 --cac 2000
  python3 unit_economics_simulator.py --mrr 50000 --growth 10 --churn 3 --cac 2000 --json
"""

import sys
import json
import argparse


def simulate(mrr: float, growth_pct: float, churn_pct: float, cac: float,
             gross_margin: float = 0.7, months: int = 12) -> list[dict]:
    """Project metrics forward N months."""
    projections = []
    current_mrr = mrr

    for month in range(1, months + 1):
        growth = current_mrr * (growth_pct / 100)
        churn = current_mrr * (churn_pct / 100)
        net = growth - churn
        current_mrr += net

        projections.append({
            "month": month,
            "mrr": round(current_mrr, 2),
            "arr": round(current_mrr * 12, 2),
            "growth": round(growth, 2),
            "churn": round(churn, 2),
            "net": round(net, 2),
        })

    return projections


def main():
    parser = argparse.ArgumentParser(description="Unit Economics Simulator")
    parser.add_argument("--mrr", type=float, required=True, help="Current MRR")
    parser.add_argument("--growth", type=float, required=True, help="Monthly growth %")
    parser.add_argument("--churn", type=float, required=True, help="Monthly churn %")
    parser.add_argument("--cac", type=float, default=0, help="CAC")
    parser.add_argument("--gross-margin", type=float, default=0.7, help="Gross margin")
    parser.add_argument("--months", type=int, default=12, help="Months to project")
    parser.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()
    projections = simulate(args.mrr, args.growth, args.churn, args.cac,
                           args.gross_margin, args.months)

    if args.json:
        print(json.dumps(projections, indent=2))
    else:
        print(f"📊 12-Month Projection (Growth: {args.growth}%, Churn: {args.churn}%)")
        print("=" * 60)
        print(f"{'Month':<8} {'MRR':<12} {'ARR':<12} {'Growth':<12} {'Churn':<12}")
        print("-" * 60)
        for p in projections:
            print(f"{p['month']:<8} ${p['mrr']:<9.0f} ${p['arr']:<9.0f} ${p['growth']:<9.0f} ${p['churn']:<9.0f}")


if __name__ == "__main__":
    main()
