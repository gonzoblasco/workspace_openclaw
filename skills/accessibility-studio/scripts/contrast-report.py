#!/usr/bin/env python3
"""contrast-report.py — Analyze Tailwind config colors and verify contrast ratios.

Usage:
  python3 contrast-report.py <tailwind-config> [--backgrounds "#fff,#f8f9fa"]

Analyzes all colors in tailwind.config and checks contrast against
specified background colors. Generates a markdown report.
"""

import sys
import json
import re
import math
from pathlib import Path


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    """Calculate relative luminance per WCAG 2.1."""
    vals = []
    for c in rgb:
        srgb = c / 255.0
        if srgb <= 0.04045:
            vals.append(srgb / 12.92)
        else:
            vals.append(((srgb + 0.055) / 1.055) ** 2.4)
    return 0.2126 * vals[0] + 0.7152 * vals[1] + 0.0722 * vals[2]


def contrast_ratio(l1: float, l2: float) -> float:
    """Calculate contrast ratio between two luminances."""
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def extract_colors(config_path: str) -> dict[str, str]:
    """Extract color values from tailwind.config.* files."""
    content = Path(config_path).read_text()

    # Try parsing as JS/TS with regex (handles both .js and .ts)
    colors = {}

    # Match theme.extend.colors or theme.colors objects
    # Simple extraction for common patterns
    color_patterns = [
        r"['\"]?(\w+)['\"]?\s*:\s*['\"](#[0-9a-fA-F]{3,8})['\"]",
        r"['\"]?(\w+)['\"]?\s*:\s*['\"](rgba?\([^)]+\))['\"]",
    ]

    for pattern in color_patterns:
        for match in re.finditer(pattern, content):
            name, value = match.groups()
            if value.startswith("#"):
                colors[name] = value

    return colors


def parse_backgrounds(bg_str: str) -> list[str]:
    """Parse comma-separated background colors."""
    return [bg.strip() for bg in bg_str.split(",")]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    config_path = sys.argv[1]
    backgrounds = ["#ffffff"]
    if len(sys.argv) >= 3:
        backgrounds = parse_backgrounds(sys.argv[2])

    colors = extract_colors(config_path)
    if not colors:
        print("⚠️  No colors found in config file")
        sys.exit(1)

    print("# Contrast Report\n")
    print(f"**Config:** {config_path}")
    print(f"**Backgrounds tested:** {', '.join(backgrounds)}\n")

    all_pass = True

    for bg_hex in backgrounds:
        bg_rgb = hex_to_rgb(bg_hex)
        bg_lum = relative_luminance(bg_rgb)
        print(f"## Background: {bg_hex}\n")
        print("| Color | Hex | Ratio | AA Text | AA Large | AAA Text |")
        print("|-------|-----|-------|---------|----------|----------|")

        for name, hex_color in sorted(colors.items()):
            rgb = hex_to_rgb(hex_color)
            lum = relative_luminance(rgb)
            ratio = contrast_ratio(lum, bg_lum)

            aa_text = "✅" if ratio >= 4.5 else "❌"
            aa_large = "✅" if ratio >= 3.0 else "❌"
            aaa_text = "✅" if ratio >= 7.0 else "❌"

            print(f"| {name} | {hex_color} | {ratio:.2f}:1 | {aa_text} | {aa_large} | {aaa_text} |")

            if ratio < 4.5:
                all_pass = False

        print()

    if not all_pass:
        print("\n⚠️  Some colors do not meet AA text contrast requirements.")
        print("Consider adjusting for accessibility compliance.")
    else:
        print("\n✅ All colors meet AA text contrast requirements.")


if __name__ == "__main__":
    main()
