"""CLI interface supporting Stage 4 dependency load order output."""

import argparse
import os
import sys
from typing import Dict

from src.apk_parser import fetch_apkindex, parse_apkindex_content
from src.graph import (
    build_dependency_graph,
    compute_load_order,
    parse_test_repo,
)

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


def print_order_summary(load_order: list, cycles: list) -> None:
    """Display computed load order and real package manager notes."""
    print("Computed load/install order:")
    for idx, pkg in enumerate(load_order, start=1):
        print(f"  {idx}. {pkg}")

    print("\nComparison with Alpine apk manager:")
    print(" - apk uses a SAT/heuristic solver with package priority levels.")
    print(" - apk breaks mutual cycle dependencies via pre-install triggers.")
    if cycles:
        print(" - Cyclic dependencies were detected and bypassed in ordering.")


def main() -> None:
    """Run Stage 4 workflow: graph build and load order computation."""
    parser = build_parser()
    args = parser.parse_args()
    try:
        config = validate_args(args)
        fetcher = resolve_fetcher(config)
        graph, cycles = build_dependency_graph(config["package"], fetcher)
        load_order = compute_load_order(graph, config["package"])
    except ValueError as err:
        print(err, file=sys.stderr)
        sys.exit(EXIT_FAILURE)

    print(f"Package: {config['package']}\n")
    print_order_summary(load_order, cycles)


if __name__ == "__main__":
    main()