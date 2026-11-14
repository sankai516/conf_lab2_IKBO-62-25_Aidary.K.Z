"""Mermaid diagram generation and SVG rendering for Stage 5."""

from typing import Dict, List

INDENT = "    "
HEADER = "graph TD\n"
ARROW = " --> "
SVG_MIME = "image/svg+xml"
BASE_HEIGHT = 400
HEIGHT_PER_NODE = 35
HEIGHT_PADDING = 150
VIEWBOX_WIDTH = 900
STEP_Y = 20
START_Y = 70


def generate_mermaid(graph: Dict[str, List[str]]) -> str:
    """Generate Mermaid markup from dependency graph adjacency list."""
    lines: List[str] = [HEADER]
    for src, deps in sorted(graph.items()):
        if not deps:
            lines.append(f"{INDENT}{src}\n")
        for dep in deps:
            lines.append(f"{INDENT}{src}{ARROW}{dep}\n")
    return "".join(lines)


def render_svg_diagram(
    graph: Dict[str, List[str]],
    mermaid_code: str,
    output_path: str,
) -> None:
    """Write standalone valid SVG visualization containing Mermaid graph."""
    node_count = len(graph)
    extra_height = node_count * HEIGHT_PER_NODE + HEIGHT_PADDING
    svg_height = max(BASE_HEIGHT, extra_height)
    lines: List[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" ',
        f'width="{VIEWBOX_WIDTH}" height="{svg_height}" ',
        f'viewBox="0 0 {VIEWBOX_WIDTH} {svg_height}">\n',
        "<style>\n",
        "  .bg { fill: #1e1e2e; }\n",
        "  .title { fill: #cdd6f4; font-family: monospace; }\n",
        "  .code { fill: #a6adc8; font-family: monospace; }\n",
        "</style>\n",
        '<rect width="100%" height="100%" class="bg"/>\n',
        '<text x="20" y="35" class="title">Alpine Graph (Mermaid)</text>\n',
    ]

    y_coord = START_Y
    for code_line in mermaid_code.strip().splitlines():
        escaped = code_line.replace("&", "&amp;").replace("<", "&lt;")
        line_tag = (
            f'<text x="25" y="{y_coord}" font-size="12px" '
            f'class="code">{escaped}</text>\n'
        )
        lines.append(line_tag)
        y_coord += STEP_Y

    lines.append("</svg>\n")
    with open(output_path, "w", encoding="utf-8") as svg_file:
        svg_file.writelines(lines)