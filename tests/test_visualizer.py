"""Unit tests for Stage 5 Mermaid diagram generation and SVG export."""

import os
import unittest
from src.visualizer import generate_mermaid, render_svg_diagram


class TestVisualizer(unittest.TestCase):
    """Test cases for Mermaid and SVG generation."""

    def test_mermaid_generation(self) -> None:
        """Test Mermaid output formatting."""
        graph = {"A": ["B"], "B": []}
        code = generate_mermaid(graph)
        self.assertIn("graph TD", code)
        self.assertIn("A --> B", code)

    def test_svg_export(self) -> None:
        """Test SVG file creation on disk."""
        graph = {"A": ["B"], "B": []}
        code = generate_mermaid(graph)
        out_file = "test_out.svg"
        render_svg_diagram(graph, code, out_file)
        self.assertTrue(os.path.exists(out_file))
        if os.path.exists(out_file):
            os.remove(out_file)


if __name__ == "__main__":
    unittest.main()