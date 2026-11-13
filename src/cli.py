"""CLI configuration and direct dependency display for Stage 2."""

import argparse
import os
import sys
from typing import Dict

from src.apk_parser import get_direct_dependencies

MIN_STR_LEN = 1
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


def main() -> None:
    """Run CLI tool and display direct dependencies for Stage 2."""
    parser = build_parser()
    args = parser.parse_args()
    try:
        config = validate_args(args)
        if not args.test_mode:
            deps = get_direct_dependencies(config["repo"], config["package"])
            print(f"Direct dependencies for '{config['package']}':")
            for dep in deps:
                print(f" - {dep}")
    except ValueError as err:
        print(err, file=sys.stderr)
        sys.exit(MIN_STR_LEN)


if __name__ == "__main__":
    main()