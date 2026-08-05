"""
Decoding a Secret Message from a Published Google Doc

Reads a published Google Doc containing Unicode characters with x,y coordinates
in an HTML table, and prints the grid of characters which forms a secret message.

The document format is an HTML table with columns: x-coordinate, character, y-coordinate.
No external dependencies required - uses only Python standard library.
"""

import re
import urllib.request


def decode_secret_message(doc_url: str) -> None:
    """
    Fetches a published Google Doc, parses the character/coordinate table,
    and prints the resulting grid of characters.

    Args:
        doc_url: URL string for the published Google Doc.
    """
    # Fetch the document HTML
    with urllib.request.urlopen(doc_url) as response:
        html = response.read().decode("utf-8")

    # Parse the HTML table to extract (x, char, y) triples
    points = _extract_coordinates(html)

    if not points:
        print("No valid data found in the document.")
        return

    # Determine grid bounds
    max_x = max(p[0] for p in points)
    max_y = max(p[2] for p in points)

    # Build the grid: y increases downward, x increases rightward
    # (0, 0) is top-left corner
    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for x, char, y in points:
        grid[y][x] = char

    # Print the grid
    for row in grid:
        print("".join(row))


def _extract_coordinates(html: str) -> list[tuple[int, str, int]]:
    """
    Extract (x, char, y) triples from the HTML table.

    The published Google Doc contains a table where each data row has
    three cells: x-coordinate, character, y-coordinate.
    """
    points = []

    # Find all table rows
    row_pattern = re.compile(r"<tr[^>]*>(.*?)</tr>", re.DOTALL)
    # Find all table cells within a row
    cell_pattern = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL)
    # Strip HTML tags from cell content
    tag_pattern = re.compile(r"<[^>]+>")

    rows = row_pattern.findall(html)

    for row in rows:
        cells = cell_pattern.findall(row)

        # Skip rows that don't have exactly 3 cells (header row, etc.)
        if len(cells) != 3:
            continue

        # Strip HTML tags from each cell content
        cleaned = [tag_pattern.sub("", c).strip() for c in cells]

        # Parse as (x, char, y)
        # The first and third cells should be numeric (coordinates)
        # The middle cell is the character
        try:
            x = int(cleaned[0])
            y = int(cleaned[2])
            char = cleaned[1]
            if char:  # Skip empty characters
                points.append((x, char, y))
        except (ValueError, IndexError):
            continue

    return points
