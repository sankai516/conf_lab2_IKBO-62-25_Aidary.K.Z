"""Unit tests for Stage 1 CLI validation."""

import argparse
import unittest
from src.cli import validate_args


class TestCliValidation(unittest.TestCase):
    """Test cases for CLI argument validation."""

    def test_valid_remote_args(self) -> None:
        """Test valid arguments in remote repository mode."""
        ns = argparse.Namespace(
            package="curl",
            repo="https://dl-cdn.alpinelinux.org/alpine/v3.20/main/x86_64",
            test_mode=False,
            output="graph.svg",
        )
        config = validate_args(ns)
        self.assertEqual(config["package"], "curl")

    def test_invalid_output_extension(self) -> None:
        """Test error raised when output is not an SVG file."""
        ns = argparse.Namespace(
            package="curl",
            repo="https://example.com",
            test_mode=False,
            output="graph.png",
        )
        with self.assertRaises(ValueError):
            validate_args(ns)


if __name__ == "__main__":
    unittest.main()