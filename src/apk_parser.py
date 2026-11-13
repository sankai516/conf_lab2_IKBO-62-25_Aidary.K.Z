"""Alpine Linux APKINDEX parser module for Stage 2."""

import io
import tarfile
import urllib.request
from typing import Dict, List, Set

INDEX_ARCHIVE = "APKINDEX.tar.gz"
INDEX_FILE = "APKINDEX"
PKG_PREFIX = "P:"
DEP_PREFIX = "D:"
PROVIDES_PREFIX = "p:"
PREFIX_LEN = 2
VERSION_SEPS = ("=", "<", ">", "~")


def clean_dep_token(token: str) -> str:
    """Strip version constraints from a dependency token."""
    cleaned = token.strip()
    if cleaned.startswith("!"):
        return ""
    for sep in VERSION_SEPS:
        if sep in cleaned:
            cleaned = cleaned.split(sep)[0]
    return cleaned


def parse_apkindex_content(content: str) -> Dict[str, List[str]]:
    """Parse raw APKINDEX text and map packages to dependencies."""
    blocks = content.strip().split("\n\n")
    pkg_deps: Dict[str, List[str]] = {}
    provides_map: Dict[str, str] = {}

    for block in blocks:
        pkg_name = ""
        raw_deps: List[str] = []
        provided: List[str] = []
        for line in block.splitlines():
            if line.startswith(PKG_PREFIX):
                pkg_name = line[PREFIX_LEN:].strip()
            elif line.startswith(DEP_PREFIX):
                raw_deps = line[PREFIX_LEN:].strip().split()
            elif line.startswith(PROVIDES_PREFIX):
                provided = line[PREFIX_LEN:].strip().split()
        if pkg_name:
            pkg_deps[pkg_name] = [
                clean_dep_token(tok) for tok in raw_deps if clean_dep_token(tok)
            ]
            for prov in provided:
                prov_name = clean_dep_token(prov)
                if prov_name:
                    provides_map[prov_name] = pkg_name

    return resolve_virtual_deps(pkg_deps, provides_map)


def resolve_virtual_deps(
    pkg_deps: Dict[str, List[str]],
    provides_map: Dict[str, str],
) -> Dict[str, List[str]]:
    """Resolve virtual dependencies like so:lib.so to package names."""
    resolved: Dict[str, List[str]] = {}
    for pkg, deps in pkg_deps.items():
        clean_list: List[str] = []
        seen: Set[str] = set()
        for dep in deps:
            target = provides_map.get(dep, dep)
            if target != pkg and target not in seen:
                seen.add(target)
                clean_list.append(target)
        resolved[pkg] = clean_list
    return resolved


def fetch_apkindex(repo_url: str) -> str:
    """Download and extract APKINDEX text from remote repository URL."""
    base_url = repo_url.rstrip("/")
    if not base_url.endswith(INDEX_ARCHIVE):
        url = f"{base_url}/{INDEX_ARCHIVE}"
    else:
        url = base_url

    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            archive_bytes = response.read()
    except Exception as exc:
        raise ValueError(f"Error downloading APKINDEX: {exc}") from exc

    try:
        byte_stream = io.BytesIO(archive_bytes)
        with tarfile.open(fileobj=byte_stream, mode="r:gz") as tar:
            member = tar.extractfile(INDEX_FILE)
            if member is None:
                raise ValueError("Error: APKINDEX not found in archive.")
            return member.read().decode("utf-8", errors="replace")
    except Exception as exc:
        raise ValueError(f"Error extracting APKINDEX: {exc}") from exc


def get_direct_dependencies(repo_url: str, package: str) -> List[str]:
    """Fetch repository index and return direct dependencies of a package."""
    content = fetch_apkindex(repo_url)
    all_deps = parse_apkindex_content(content)
    if package not in all_deps:
        raise ValueError(f"Error: package '{package}' not found in repo.")
    return all_deps[package]