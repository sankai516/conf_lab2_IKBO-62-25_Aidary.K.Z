"""Unit tests for Stage 3 non-recursive DFS and cycle handling."""

import unittest
from src.graph import build_dependency_graph


class TestGraphDFS(unittest.TestCase):
    """Test cases for graph construction and cycle detection."""

    def test_dfs_linear_graph(self) -> None:
        """Test transitive dependency resolution on DAG."""
        mock_repo = {
            "A": ["B", "C"],
            "B": ["D"],
            "C": ["D"],
            "D": [],
        }
        graph, cycles = build_dependency_graph(
            "A", lambda p: mock_repo.get(p, [])
        )
        self.assertEqual(len(cycles), 0)
        self.assertIn("D", graph)
        self.assertEqual(graph["A"], ["B", "C"])

    def test_dfs_cycle_detection(self) -> None:
        """Test non-recursive DFS does not enter infinite loop on cycle."""
        mock_repo = {
            "A": ["B"],
            "B": ["C"],
            "C": ["A", "D"],
            "D": [],
        }
        graph, cycles = build_dependency_graph(
            "A", lambda p: mock_repo.get(p, [])
        )
        self.assertGreater(len(cycles), 0)
        self.assertEqual(cycles[0], ("C", "A"))


if __name__ == "__main__":
    unittest.main()