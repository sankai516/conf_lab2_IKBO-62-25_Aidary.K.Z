"""CLI interface supporting Stage 3 graph building and cycle detection."""

import argparse
import os
import sys
from typing import Dict, List

from src.apk_parser import fetch_apkindex, parse_apkindex_content
from src.graph import build_dependency_graph, parse_test_repo

MIN_STR_LEN = 1
EXIT_FAILURE = 1
SVG_EXT = ".svg"


def build_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Dependency graph visualizer for Alpine apk."
    )
    parser.add_argument(
        "--package",
        required=True,
        help="Name of the analyzed package",
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="Repository URL or path to test repository file",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Enable test repository mode",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output SVG file name",
    )
    return parser


def validate_args(args: argparse.Namespace) -> Dict[str, str]:
    """Validate parsed CLI arguments and return config dictionary."""
    pkg = args.package.strip()
    repo = args.repo.strip()
    output = args.output.strip()

    if len(pkg) < MIN_STR_LEN:
        raise ValueError("Error: package name cannot be empty.")
    if len(repo) < MIN_STR_LEN:
        raise ValueError("Error: repository URL or path cannot be empty.")
    if args.test_mode and not os.path.isfile(repo):
        raise ValueError(f"Error: test file not found: {repo}")
    if not output.endswith(SVG_EXT):
        raise ValueError("Error: output file must have .svg extension.")

    return {
        "package": pkg,
        "repo": repo,
        "test_mode": str(args.test_mode),
        "output": output,
    }


def resolve_fetcher(config: Dict[str, str]):
    """Return dependency provider depending on execution mode."""
    if config["test_mode"] == "True":
        repo_data = parse_test_repo(config["repo"])
        return lambda p: repo_data.get(p, [])

    index_text = fetch_apkindex(config["repo"])
    repo_data = parse_apkindex_content(index_text)
    return lambda p: repo_data.get(p, [])


def main() -> None:
    """Run CLI tool, build dependency graph and display edges and cycles."""
    parser = build_parser()
    args = parser.parse_args()
    try:
        config = validate_args(args)
        fetcher = resolve_fetcher(config)
        graph, cycles = build_dependency_graph(config["package"], fetcher)
    except ValueError as err:
        print(err, file=sys.stderr)
        sys.exit(EXIT_FAILURE)

    print(f"Graph for '{config['package']}':")
    for src, deps in graph.items():
        deps_str = ", ".join(deps) if deps else "(none)"
        print(f"  {src} -> {deps_str}")

    if cycles:
        print("Cycles detected:")
        for src, dst in cycles:
            print(f"  Cycle edge: {src} -> {dst}")
    else:
        print("No cycles detected.")


if __name__ == "__main__":
    main()