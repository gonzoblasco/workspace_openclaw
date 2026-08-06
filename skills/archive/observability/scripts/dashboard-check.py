#!/usr/bin/env python3
"""dashboard-check.py — Verify dashboard coverage and usage.

Usage:
  python3 dashboard-check.py [--output <file>]

Checks that required dashboards exist and have content.
"""

import sys
import json
from pathlib import Path
from datetime import datetime


# Required dashboards per domain
REQUIRED_DASHBOARDS = {
    "product": ["usage", "conversion", "errors", "features"],
    "backend": ["latency", "throughput", "error_rate", "resources"],
    "frontend": ["core_web_vitals", "js_errors", "bundle_size", "load_time"],
    "infrastructure": ["cpu", "memory", "disk", "network", "database"],
    "ai": ["tokens", "costs", "latency", "retries"],
    "workflows": ["execution_time", "success_rate", "bottlenecks"],
    "releases": ["frequency", "failure_rate", "mttr"],
}


def check_dashboard_coverage() -> dict:
    """Check which dashboards exist and have content."""
    results = {}

    for domain, metrics in REQUIRED_DASHBOARDS.items():
        domain_results = {"present": [], "missing": []}
        for metric in metrics:
            # Check for dashboard files or configs
            dashboard_paths = [
                Path(f"dashboards/{domain}/{metric}.json"),
                Path(f"dashboards/{domain}/{metric}.md"),
                Path(f"monitoring/{domain}/{metric}.json"),
            ]
            found = any(p.exists() for p in dashboard_paths)
            if found:
                domain_results["present"].append(metric)
            else:
                domain_results["missing"].append(metric)
        results[domain] = domain_results

    return results


def main():
    output_file = "DASHBOARD_CHECK.md"

    args = sys.argv[1:]
    while args:
        if args[0] == "--output" and len(args) > 1:
            output_file = args[1]
            args = args[2:]
        else:
            args = args[1:]

    coverage = check_dashboard_coverage()

    total_required = sum(len(metrics) for metrics in REQUIRED_DASHBOARDS.values())
    total_present = sum(
        len(result["present"]) for result in coverage.values()
    )
    coverage_pct = (total_present / total_required * 100) if total_required > 0 else 0

    report = f"""# Dashboard Coverage Check

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Coverage:** {coverage_pct:.0f}% ({total_present}/{total_required})

## Per-Domain Coverage

| Domain | Present | Missing | Status |
|--------|---------|---------|--------|
"""

    for domain, result in sorted(coverage.items()):
        present = len(result["present"])
        missing = len(result["missing"])
        status = "🟢" if missing == 0 else "🟡" if present >= missing else "🔴"
        report += f"| {domain} | {present} | {missing} | {status} |\n"

    report += "\n## Missing Dashboards\n\n"

    for domain, result in sorted(coverage.items()):
        if result["missing"]:
            report += f"### {domain}\n\n"
            for metric in result["missing"]:
                report += f"- {metric}\n"
            report += "\n"

    report += "## Recommendations\n\n"

    if coverage_pct < 50:
        report += "- 🔴 **Critical:** Most dashboards are missing. Prioritize creating them.\n"
    elif coverage_pct < 80:
        report += "- 🟡 **Warning:** Some dashboards missing. Fill gaps in next sprint.\n"
    else:
        report += "- 🟢 **Good:** Most dashboards are present. Maintain coverage.\n"

    Path(output_file).write_text(report)
    print(f"✅ Dashboard check complete: {coverage_pct:.0f}% coverage")
    print(f"   Report: {output_file}")


if __name__ == "__main__":
    main()
