"""Unit tests for Stage 2 Alpine APKINDEX parser."""

import unittest
from src.apk_parser import parse_apkindex_content


class TestApkParser(unittest.TestCase):
    """Test cases for parsing APKINDEX blocks and virtual provides."""

    def test_parse_dependencies_and_provides(self) -> None:
        """Test extraction of direct and virtual dependencies."""
        sample_index = (
            "P:musl\nV:1.2.5\np:so:libc.musl-x86_64.so.1=1\n\n"
            "P:zlib\nV:1.3.1\nD:so:libc.musl-x86_64.so.1\n"
            "p:so:libz.so.1=1.3.1\n\n"
            "P:curl\nV:8.9.0\n"
            "D:so:libc.musl-x86_64.so.1 so:libz.so.1 ca-certs\n"
        )
        parsed = parse_apkindex_content(sample_index)
        self.assertEqual(parsed["musl"], [])
        self.assertEqual(parsed["zlib"], ["musl"])
        self.assertEqual(parsed["curl"], ["musl", "zlib", "ca-certs"])


if __name__ == "__main__":
    unittest.main()