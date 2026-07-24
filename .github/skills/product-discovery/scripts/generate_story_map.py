#!/usr/bin/env python3
"""generate_story_map.py — Generate interactive HTML user story map.

Usage:
  python3 generate_story_map.py --input data.json --output story_map.html
  echo '{"project":"demo",...}' | python3 generate_story_map.py --output story_map.html

Generates a self-contained HTML file with Epic → Feature → Story structure,
MoSCoW priority color coding, and Release swimlane grouping.
"""

import sys
import json
import html
from pathlib import Path


# ─── HTML Template ─────────────────────────────────────────────────

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; padding: 20px; }}
h1 {{ font-size: 24px; margin-bottom: 20px; color: #333; }}
.stats {{ display: flex; gap: 20px; margin-bottom: 20px; flex-wrap: wrap; }}
.stat {{ background: white; padding: 12px 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
.stat-label {{ font-size: 12px; color: #666; }}
.stat-value {{ font-size: 20px; font-weight: bold; color: #333; }}
.map-container {{ overflow-x: auto; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
.map {{ display: flex; gap: 0; min-width: 800px; }}
.epic-column {{ flex: 1; min-width: 200px; border-right: 1px solid #e0e0e0; }}
.epic-column:last-child {{ border-right: none; }}
.epic-header {{ padding: 12px; background: #f8f9fa; font-weight: bold; font-size: 14px; border-bottom: 2px solid #dee2e6; text-align: center; }}
.feature {{ border-bottom: 1px solid #eee; }}
.feature-header {{ padding: 8px 12px; font-size: 12px; font-weight: 600; color: #495057; background: #f8f9fa; }}
.story {{ padding: 6px 12px; font-size: 12px; border-bottom: 1px solid #f0f0f0; cursor: pointer; transition: background 0.2s; }}
.story:hover {{ background: #f0f0f0; }}
.story-must {{ border-left: 3px solid #dc3545; }}
.story-should {{ border-left: 3px solid #fd7e14; }}
.story-could {{ border-left: 3px solid #0d6efd; }}
.story-wont {{ border-left: 3px solid #adb5bd; opacity: 0.6; }}
.story-points {{ display: inline-block; background: #e9ecef; padding: 1px 6px; border-radius: 4px; font-size: 10px; margin-left: 4px; }}
.release-divider {{ height: 2px; background: #dee2e6; margin: 0; }}
.release-label {{ padding: 4px 12px; font-size: 10px; color: #6c757d; background: #f8f9fa; font-style: italic; }}
.tooltip {{ display: none; position: absolute; background: #333; color: white; padding: 8px 12px; border-radius: 6px; font-size: 12px; max-width: 300px; z-index: 100; }}
.story:hover .tooltip {{ display: block; }}
@media print {{ body {{ padding: 0; }} .map-container {{ box-shadow: none; }} }}
</style>
</head>
<body>
<h1>{title}</h1>
<div class="stats">
  <div class="stat"><div class="stat-label">Total Stories</div><div class="stat-value">{total_stories}</div></div>
  <div class="stat"><div class="stat-label">Must</div><div class="stat-value" style="color:#dc3545">{must_count}</div></div>
  <div class="stat"><div class="stat-label">Should</div><div class="stat-value" style="color:#fd7e14">{should_count}</div></div>
  <div class="stat"><div class="stat-label">Could</div><div class="stat-value" style="color:#0d6efd">{could_count}</div></div>
  <div class="stat"><div class="stat-label">Won't</div><div class="stat-value" style="color:#adb5bd">{wont_count}</div></div>
  <div class="stat"><div class="stat-label">Total Points</div><div class="stat-value">{total_points}</div></div>
</div>
<div class="map-container">
<div class="map">
{columns}
</div>
</div>
</body>
</html>"""


# ─── Story Map Builder ──────────────────────────────────────────────

PRIORITY_CLASS = {
    "must": "story-must",
    "should": "story-should",
    "could": "story-could",
    "wont": "story-wont",
}


def build_story_html(story: dict) -> str:
    """Build HTML for a single story."""
    priority = story.get("priority", "could")
    css_class = PRIORITY_CLASS.get(priority, "story-could")
    points = story.get("points", "")
    description = story.get("description", "")

    points_html = f'<span class="story-points">{points}pt</span>' if points else ""
    tooltip = f'<div class="tooltip">{html.escape(description)}</div>' if description else ""

    return f'<div class="story {css_class}">{html.escape(story["name"])}{points_html}{tooltip}</div>'


def build_feature_html(feature: dict, releases: list) -> str:
    """Build HTML for a feature with its stories grouped by release."""
    html_parts = [f'<div class="feature-header">{html.escape(feature["name"])}</div>']

    stories = feature.get("stories", [])

    # Group stories by release
    for release in releases:
        release_name = release["name"]
        release_stories = [s for s in stories if s.get("release") == release_name]

        if release_stories:
            html_parts.append(f'<div class="release-label">{html.escape(release_name)}</div>')
            for story in release_stories:
                html_parts.append(build_story_html(story))

    # Stories without release assignment
    unassigned = [s for s in stories if not s.get("release")]
    if unassigned:
        html_parts.append('<div class="release-label">Unassigned</div>')
        for story in unassigned:
            html_parts.append(build_story_html(story))

    return "".join(html_parts)


def build_epic_column(epic: dict, releases: list) -> str:
    """Build HTML column for an epic."""
    features = epic.get("features", [])
    features_html = "".join(build_feature_html(f, releases) for f in features)

    return f"""<div class="epic-column">
<div class="epic-header">{html.escape(epic["name"])}</div>
<div class="feature">{features_html}</div>
</div>"""


def generate_story_map(data: dict) -> str:
    """Generate complete HTML story map."""
    project = data.get("project", "Story Map")
    releases = data.get("releases", [])
    epics = data.get("epics", [])

    # Stats
    total_stories = 0
    must_count = 0
    should_count = 0
    could_count = 0
    wont_count = 0
    total_points = 0

    for epic in epics:
        for feature in epic.get("features", []):
            for story in feature.get("stories", []):
                total_stories += 1
                priority = story.get("priority", "could")
                if priority == "must":
                    must_count += 1
                elif priority == "should":
                    should_count += 1
                elif priority == "could":
                    could_count += 1
                elif priority == "wont":
                    wont_count += 1
                total_points += story.get("points", 0)

    columns = "".join(build_epic_column(epic, releases) for epic in epics)

    return HTML_TEMPLATE.format(
        title=html.escape(project),
        total_stories=total_stories,
        must_count=must_count,
        should_count=should_count,
        could_count=could_count,
        wont_count=wont_count,
        total_points=total_points,
        columns=columns,
    )


# ─── Main ───────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    input_file = ""
    output_file = ""

    args = sys.argv[1:]
    while args:
        if args[0] == "--input" and len(args) > 1:
            input_file = args[1]
            args = args[2:]
        elif args[0] == "--output" and len(args) > 1:
            output_file = args[1]
            args = args[2:]
        else:
            args = args[1:]

    if not output_file:
        print("❌ --output is required")
        sys.exit(1)

    # Read input
    if input_file:
        with open(input_file, encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    # Validate
    if "project" not in data:
        print("❌ JSON must contain 'project' field")
        sys.exit(1)
    if "epics" not in data:
        print("❌ JSON must contain 'epics' array")
        sys.exit(1)

    # Generate
    html_content = generate_story_map(data)

    Path(output_file).write_text(html_content, encoding="utf-8")
    print(f"✅ Story map generated: {output_file}")
    print(f"   Project: {data['project']}")
    print(f"   Epics: {len(data['epics'])}")
    print(f"   Stories: {sum(len(f.get('stories', [])) for e in data['epics'] for f in e.get('features', []))}")


if __name__ == "__main__":
    main()
