"""Dependency graph traversal and test repository parsing for Stage 3."""

from typing import Callable, Dict, List, Set, Tuple

DELIMITER = ":"
MIN_SPLIT_PARTS = 2
FIRST_PART_IDX = 0
SECOND_PART_IDX = 1


def parse_test_repo(filepath: str) -> Dict[str, List[str]]:
    """Parse test repository file where packages are uppercase letters."""
    graph: Dict[str, List[str]] = {}
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if not stripped:
                continue
            if DELIMITER in stripped:
                parts = stripped.split(DELIMITER, 1)
                pkg = parts[FIRST_PART_IDX].strip()
                deps_raw = parts[SECOND_PART_IDX].strip()
                deps = deps_raw.split() if deps_raw else []
                graph[pkg] = deps
    return graph


def build_dependency_graph(
    root_pkg: str,
    fetch_deps: Callable[[str], List[str]],
) -> Tuple[Dict[str, List[str]], List[Tuple[str, str]]]:
    """Build full dependency graph using iterative DFS without recursion."""
    graph: Dict[str, List[str]] = {}
    cycles: List[Tuple[str, str]] = []
    visited: Set[str] = set()
    stack: List[str] = [root_pkg]
    path_set: Set[str] = set()

    while stack:
        node = stack[-1]

        if node not in graph:
            graph[node] = fetch_deps(node)

        if node not in path_set and node not in visited:
            path_set.add(node)

        unvisited_neighbor = None
        for dep in graph[node]:
            if dep in path_set:
                edge = (node, dep)
                if edge not in cycles:
                    cycles.append(edge)
            elif dep not in visited:
                unvisited_neighbor = dep
                break

        if unvisited_neighbor is not None:
            stack.append(unvisited_neighbor)
        else:
            path_set.remove(node)
            visited.add(node)
            stack.pop()

    return graph, cycles