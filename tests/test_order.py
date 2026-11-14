"""Unit tests for Stage 4 load order computation."""

import unittest
from src.graph import compute_load_order


class TestLoadOrder(unittest.TestCase):
    """Test cases for topological load order traversal."""

    def test_simple_dag_order(self) -> None:
        """Verify leaf dependencies are ordered before dependent packages."""
        graph = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }
        order = compute_load_order(graph, "A")
        self.assertEqual(order[-1], "A")
        self.assertEqual(order[0], "D")
        self.assertLess(order.index("B"), order.index("A"))
        self.assertLess(order.index("C"), order.index("A"))

    def test_cyclic_graph_order(self) -> None:
        """Verify cyclic graphs produce complete non-crashing load order."""
        graph = {
            "A": ["B"],
            "B": ["C"],
            "C": ["A", "D"],
            "D": [],
        }
        order = compute_load_order(graph, "A")
        self.assertEqual(len(order), 4)
        self.assertEqual(order[-1], "A")
        self.assertIn("D", order)


if __name__ == "__main__":
    unittest.main()