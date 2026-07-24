#!/usr/bin/env python3
"""generate_timeline.py — Generate interactive HTML timeline from JSON data.

Usage:
  python3 generate_timeline.py --config data.json --output timeline.html
  cat data.json | python3 generate_timeline.py --stdin --output timeline.html
"""

import sys
import json
import html
from pathlib import Path


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: {font_family}; background: {bg_color}; color: {text_color}; padding: 40px 20px; }}
h1 {{ text-align: center; font-size: 28px; margin-bottom: 40px; color: {primary_color}; }}
.timeline {{ position: relative; max-width: 1200px; margin: 0 auto; }}
.timeline::after {{ content: ''; position: absolute; width: 4px; background: {line_color}; top: 0; bottom: 0; left: 50%; margin-left: -2px; }}
.event {{ padding: 10px 40px; position: relative; width: 50%; }}
.event:nth-child(odd) {{ left: 0; }}
.event:nth-child(even) {{ left: 50%; }}
.event::after {{ content: attr(data-icon); position: absolute; width: 20px; height: 20px; background: {primary_color}; border-radius: 50%; top: 15px; right: -10px; text-align: center; line-height: 20px; font-size: 12px; }}
.event:nth-child(even)::after {{ left: -10px; }}
.event-content {{ padding: 16px 20px; background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); cursor: pointer; transition: box-shadow 0.2s; }}
.event-content:hover {{ box-shadow: 0 4px 16px rgba(0,0,0,0.15); }}
.event-date {{ font-size: 12px; color: {secondary_color}; margin-bottom: 4px; }}
.event-title {{ font-size: 16px; font-weight: bold; margin-bottom: 4px; }}
.event-summary {{ font-size: 14px; color: #666; }}
.event-details {{ display: none; margin-top: 8px; font-size: 13px; color: #555; line-height: 1.5; }}
.event-details.open {{ display: block; }}
.event-category {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; margin-top: 4px; }}
@media (max-width: 768px) {{ .timeline::after {{ left: 20px; }} .event {{ width: 100%; padding-left: 50px; padding-right: 20px; }} .event:nth-child(odd), .event:nth-child(even) {{ left: 0; }} .event::after {{ left: 10px !important; }} }}
</style>
</head>
<body>
<h1>{title}</h1>
<div class="timeline">
{events}
</div>
<script>
document.querySelectorAll('.event-content').forEach(el => {{
  el.addEventListener('click', () => {{
    const details = el.querySelector('.event-details');
    details.classList.toggle('open');
  }});
}});
</script>
</body>
</html>"""


def generate_timeline(data: dict) -> str:
    title = data.get("title", "Timeline")
    theme = data.get("theme", {})
    events = data.get("events", [])

    event_html = []
    for event in events:
        date = html.escape(event.get("date", ""))
        ev_title = html.escape(event.get("title", ""))
        summary = html.escape(event.get("summary", ""))
        details = html.escape(event.get("details", ""))
        icon = event.get("icon", "●")
        category = html.escape(event.get("category", ""))
        color = event.get("color", theme.get("primaryColor", "#2563eb"))

        cat_html = f'<span class="event-category" style="background:{color}20;color:{color}">{category}</span>' if category else ""
        details_html = f'<div class="event-details">{details}</div>' if details else ""

        event_html.append(f"""<div class="event" data-icon="{icon}">
<div class="event-content" style="border-left:3px solid {color}">
<div class="event-date">{date}</div>
<div class="event-title">{ev_title}</div>
<div class="event-summary">{summary}</div>
{cat_html}
{details_html}
</div>
</div>""")

    return HTML_TEMPLATE.format(
        title=html.escape(title),
        events="\n".join(event_html),
        font_family=theme.get("fontFamily", "system-ui, -apple-system, sans-serif"),
        bg_color=theme.get("backgroundColor", "#ffffff"),
        text_color=theme.get("textColor", "#1f2937"),
        primary_color=theme.get("primaryColor", "#2563eb"),
        secondary_color=theme.get("secondaryColor", "#7c3aed"),
        line_color=theme.get("lineColor", "#d1d5db"),
    )


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Timeline Builder")
    parser.add_argument("--config", "-c", help="JSON config file")
    parser.add_argument("--stdin", action="store_true", help="Read JSON from stdin")
    parser.add_argument("--output", "-o", required=True, help="Output HTML file")
    args = parser.parse_args()

    if args.config:
        with open(args.config) as f:
            data = json.load(f)
    elif args.stdin:
        data = json.load(sys.stdin)
    else:
        print("❌ Provide --config or --stdin")
        sys.exit(1)

    html_content = generate_timeline(data)
    Path(args.output).write_text(html_content)
    print(f"✅ Timeline generated: {args.output}")


if __name__ == "__main__":
    main()
