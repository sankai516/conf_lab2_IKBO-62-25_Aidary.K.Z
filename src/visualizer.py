"""Mermaid diagram generation and SVG rendering for Stage 5."""

from typing import Dict, List

INDENT = "    "
HEADER = "graph TD\n"
ARROW = " --> "
SVG_MIME = "image/svg+xml"


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
    svg_height = max(400, node_count * 35 + 150)
    lines: List[str] = [
        '<svg xmlns="http://www.w3.org/2000/svg" ',
        f'width="900" height="{svg_height}" viewBox="0 0 900 {svg_height}">\n',
        '<style>\n',
        '  .bg { fill: #1e1e2e; }\n',
        '  .title { fill: #cdd6f4; font-family: monospace; font-size: 16px; }\n',
        '  .code { fill: #a6adc8; font-family: monospace; font-size: 12px; }\n',
        '</style>\n',
        f'<rect width="100%" height="100%" class="bg"/>\n',
        '<text x="20" y="35" class="title">Alpine Dependency Graph (Mermaid)</text>\n',
    ]

    y_coord = 70
    for code_line in mermaid_code.strip().splitlines():
        escaped = code_line.replace("&", "&amp;").replace("<", "&lt;")
        lines.append(f'<text x="25" y="{y_coord}" class="code">{escaped}</text>\n')
        y_coord += 20

    lines.append("</svg>\n")
    with open(output_path, "w", encoding="utf-8") as svg_file:
        svg_file.writelines(lines)