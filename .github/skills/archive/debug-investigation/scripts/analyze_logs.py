#!/usr/bin/env python3
"""analyze_logs.py — Analyze log files: error clustering, frequency, time distribution.

Usage:
  python3 analyze_logs.py /var/log/app.log
  python3 analyze_logs.py /var/log/nginx/error.log --format nginx --top 10
  python3 analyze_logs.py app.log --level ERROR --output report.json

Supports JSON, syslog, and Nginx formats with auto-detection.
"""

import sys
import json
import re
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime


# ─── Format Detection ───────────────────────────────────────────────

def detect_format(line: str) -> str | None:
    """Auto-detect log format from first line."""
    line = line.strip()
    if line.startswith("{"):
        return "json"
    if re.match(r"^[A-Z][a-z]{2}\s+\d+", line):
        return "syslog"
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line):
        return "nginx"
    if re.match(r"^\d{4}-\d{2}-\d{2}", line):
        return "iso"
    return None


def parse_json_line(line: str) -> dict | None:
    try:
        return json.loads(line)
    except json.JSONDecodeError:
        return None


def parse_syslog_line(line: str) -> dict | None:
    """Parse RFC 3164 syslog format."""
    m = re.match(
        r"^([A-Z][a-z]{2}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\S+)\[(\d+)\]:\s+(.*)",
        line,
    )
    if m:
        return {
            "timestamp": m.group(1),
            "host": m.group(2),
            "process": m.group(3),
            "pid": m.group(4),
            "message": m.group(5),
        }
    return None


def parse_iso_line(line: str) -> dict | None:
    """Parse ISO timestamp format."""
    m = re.match(r"^(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})\s+(\w+)\s+(.*)", line)
    if m:
        return {
            "timestamp": m.group(1),
            "level": m.group(2),
            "message": m.group(3),
        }
    return None


PARSERS = {
    "json": parse_json_line,
    "syslog": parse_syslog_line,
    "iso": parse_iso_line,
}


# ─── Error Clustering ──────────────────────────────────────────────

def normalize_message(message: str) -> str:
    """Normalize dynamic parts of error messages for clustering."""
    # Replace IPs
    message = re.sub(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "{ip}", message)
    # Replace UUIDs
    message = re.sub(
        r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
        "{uuid}",
        message,
    )
    # Replace numbers
    message = re.sub(r"\b\d+\b", "{n}", message)
    # Replace hex
    message = re.sub(r"\b0x[0-9a-fA-F]+\b", "{hex}", message)
    return message


def extract_level(entry: dict) -> str:
    """Extract log level from entry."""
    for key in ("level", "severity", "lvl", "L"):
        val = entry.get(key, "")
        if val:
            return str(val).upper()
    return "INFO"


def extract_timestamp(entry: dict) -> str | None:
    """Extract timestamp from entry."""
    for key in ("timestamp", "time", "ts", "date", "datetime", "@timestamp"):
        val = entry.get(key)
        if val:
            return str(val)
    return None


# ─── Main Analysis ─────────────────────────────────────────────────

def analyze_logs(log_file: str, log_format: str = "auto", top: int = 20,
                 level_filter: str = "", since: str = "", until: str = ""):
    """Analyze log file and produce report."""
    path = Path(log_file)
    if not path.exists():
        print(f"❌ File not found: {log_file}")
        sys.exit(1)

    content = path.read_text(encoding="utf-8", errors="ignore")
    lines = content.split("\n")

    # Detect format
    if log_format == "auto":
        for line in lines[:50]:
            fmt = detect_format(line)
            if fmt:
                log_format = fmt
                break
        if log_format == "auto":
            print("⚠️  Could not detect log format, trying ISO format")
            log_format = "iso"

    parser = PARSERS.get(log_format)
    if not parser:
        print(f"❌ Unknown format: {log_format}")
        sys.exit(1)

    # Parse entries
    entries = []
    parse_failures = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        entry = parser(line)
        if entry:
            entries.append(entry)
        else:
            parse_failures += 1

    # Filter by level
    if level_filter:
        entries = [e for e in entries if extract_level(e).upper() == level_filter.upper()]

    # Filter by time range
    if since or until:
        filtered = []
        for e in entries:
            ts = extract_timestamp(e)
            if ts:
                if since and ts < since:
                    continue
                if until and ts > until:
                    continue
            filtered.append(e)
        entries = filtered

    # Cluster errors
    error_clusters = Counter()
    time_by_hour = Counter()
    time_by_date = Counter()
    first_seen = {}
    last_seen = {}

    for entry in entries:
        msg = entry.get("message", "") or entry.get("msg", "") or str(entry)
        normalized = normalize_message(msg)
        error_clusters[normalized] += 1

        if normalized not in first_seen:
            first_seen[normalized] = extract_timestamp(entry) or "unknown"
        last_seen[normalized] = extract_timestamp(entry) or "unknown"

        # Time distribution
        ts = extract_timestamp(entry)
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00").replace("T", " "))
                time_by_hour[dt.hour] += 1
                time_by_date[dt.date().isoformat()] += 1
            except (ValueError, TypeError):
                pass

    # Generate report
    print("=" * 55)
    print("          Log Analysis Report")
    print("=" * 55)
    print()
    print(f"📊 Overview")
    print(f"  Detected format: {log_format}")
    print(f"  Total lines:     {len(lines)}")
    print(f"  Parsed:          {len(entries)} (parse failures: {parse_failures})")
    print(f"  Error clusters:  {len(error_clusters)}")
    print()

    # Top error clusters
    print(f"🔴 Top Error Clusters ({len(error_clusters)} total)")
    for i, (cluster, count) in enumerate(error_clusters.most_common(top), 1):
        print(f"  #{i:<4} [×{count:<5}] {cluster[:80]}")
        print(f"       First: {first_seen.get(cluster, '?')}  Last: {last_seen.get(cluster, '?')}")
    print()

    # Time distribution by hour
    print("⏰ Time Distribution (by hour)")
    max_count = max(time_by_hour.values()) if time_by_hour else 1
    for hour in range(24):
        count = time_by_hour.get(hour, 0)
        bar = "█" * (count * 20 // max_count) if max_count > 0 else ""
        print(f"  {hour:02d}:00  {bar} {count}")
    print()

    # Time distribution by date
    print("📅 Time Distribution (by date)")
    for date, count in sorted(time_by_date.items()):
        bar = "█" * (count * 20 // max_count) if max_count > 0 else ""
        print(f"  {date}  {bar} {count}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    log_file = sys.argv[1]
    log_format = "auto"
    top = 20
    output = ""
    level_filter = ""
    since = ""
    until = ""

    args = sys.argv[2:]
    while args:
        if args[0] == "--format" and len(args) > 1:
            log_format = args[1]
            args = args[2:]
        elif args[0] == "--top" and len(args) > 1:
            top = int(args[1])
            args = args[2:]
        elif args[0] == "--output" and len(args) > 1:
            output = args[1]
            args = args[2:]
        elif args[0] == "--level" and len(args) > 1:
            level_filter = args[1]
            args = args[2:]
        elif args[0] == "--since" and len(args) > 1:
            since = args[1]
            args = args[2:]
        elif args[0] == "--until" and len(args) > 1:
            until = args[1]
            args = args[2:]
        else:
            args = args[1:]

    analyze_logs(log_file, log_format, top, level_filter, since, until)


if __name__ == "__main__":
    main()
