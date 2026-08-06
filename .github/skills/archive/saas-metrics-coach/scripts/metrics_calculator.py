#!/usr/bin/env python3
"""metrics_calculator.py — Calculate core SaaS metrics from raw business numbers.

Usage:
  python3 metrics_calculator.py --mrr 50000 --customers 100 --churned 5
  python3 metrics_calculator.py --mrr 50000 --customers 100 --churned 5 --json
"""

import sys
import json
import argparse


def calculate(mrr: float, customers: int, churned: int, new_customers: int = 0,
              expansion_mrr: float = 0, churned_mrr: float = 0, contraction_mrr: float = 0,
              sales_marketing_spend: float = 0, gross_margin: float = 0.7,
              mrr_last_month: float = None, json_output: bool = False) -> dict:
    """Calculate SaaS metrics."""
    results = {}

    # ARR
    arr = mrr * 12
    results["arr"] = round(arr, 2)

    # MRR Growth
    if mrr_last_month and mrr_last_month > 0:
        mrr_growth = ((mrr - mrr_last_month) / mrr_last_month) * 100
        results["mrr_growth_pct"] = round(mrr_growth, 2)

    # Monthly Churn Rate
    if customers > 0:
        churn_rate = (churned / customers) * 100
        results["monthly_churn_pct"] = round(churn_rate, 2)

    # ARPA (Average Revenue Per Account)
    if customers > 0:
        arpa = mrr / customers
        results["arpa"] = round(arpa, 2)

    # CAC
    if new_customers > 0 and sales_marketing_spend > 0:
        cac = sales_marketing_spend / new_customers
        results["cac"] = round(cac, 2)

    # LTV
    if churn_rate > 0 and arpa > 0:
        ltv = (arpa * gross_margin) / (churn_rate / 100)
        results["ltv"] = round(ltv, 2)

    # LTV:CAC
    if results.get("ltv") and results.get("cac"):
        results["ltv_cac_ratio"] = round(results["ltv"] / results["cac"], 2)

    # CAC Payback
    if results.get("cac") and arpa > 0:
        cac_payback = results["cac"] / (arpa * gross_margin)
        results["cac_payback_months"] = round(cac_payback, 1)

    # NRR
    if mrr > 0 and (expansion_mrr > 0 or churned_mrr > 0 or contraction_mrr > 0):
        nrr = ((mrr + expansion_mrr - churned_mrr - contraction_mrr) / mrr) * 100
        results["nrr_pct"] = round(nrr, 2)

    return results


def main():
    parser = argparse.ArgumentParser(description="SaaS Metrics Calculator")
    parser.add_argument("--mrr", type=float, required=True, help="Current MRR")
    parser.add_argument("--customers", type=int, required=True, help="Total active customers")
    parser.add_argument("--churned", type=int, default=0, help="Churned customers this month")
    parser.add_argument("--new-customers", type=int, default=0, help="New customers this month")
    parser.add_argument("--mrr-last-month", type=float, help="MRR last month")
    parser.add_argument("--expansion-mrr", type=float, default=0, help="Expansion MRR")
    parser.add_argument("--churned-mrr", type=float, default=0, help="Churned MRR")
    parser.add_argument("--contraction-mrr", type=float, default=0, help="Contraction MRR")
    parser.add_argument("--sales-marketing-spend", type=float, default=0, help="Sales & marketing spend")
    parser.add_argument("--gross-margin", type=float, default=0.7, help="Gross margin (0.0-1.0)")
    parser.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()

    results = calculate(
        mrr=args.mrr,
        customers=args.customers,
        churned=args.churned,
        new_customers=args.new_customers,
        expansion_mrr=args.expansion_mrr,
        churned_mrr=args.churned_mrr,
        contraction_mrr=args.contraction_mrr,
        sales_marketing_spend=args.sales_marketing_spend,
        gross_margin=args.gross_margin,
        mrr_last_month=args.mrr_last_month,
    )

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("📊 SaaS Metrics")
        print("=" * 40)
        for key, value in results.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()
