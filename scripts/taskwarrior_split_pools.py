#!/usr/bin/env python
"""Split Taskwarrior tasks into dependency-safe pools."""

from __future__ import annotations

import argparse
import json
import pathlib
from collections import defaultdict
from typing import Dict, Iterable, List, Set, Tuple

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "outputs" / "workplan" / "taskwarrior.json"
DEFAULT_OUTDIR = REPO_ROOT / "outputs" / "workplan"


def load_entries(path: pathlib.Path) -> List[Dict[str, object]]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_components(entries: Iterable[Dict[str, object]]) -> List[Set[str]]:
    graph: Dict[str, Set[str]] = defaultdict(set)
    for entry in entries:
        uid = entry.get("uid")
        if not uid:
            continue
        deps = entry.get("depends") or []
        for dep in deps:
            graph[uid].add(dep)
            graph[dep].add(uid)
    visited: Set[str] = set()
    components: List[Set[str]] = []

    def dfs(node: str, acc: Set[str]) -> None:
        for neighbor in graph.get(node, []):
            if neighbor in visited:
                continue
            visited.add(neighbor)
            acc.add(neighbor)
            dfs(neighbor, acc)

    for uid in graph:
        if uid in visited:
            continue
        visited.add(uid)
        comp = {uid}
        dfs(uid, comp)
        components.append(comp)
    # include isolated nodes with no deps
    all_uids = {entry.get("uid") for entry in entries if entry.get("uid")}
    for uid in all_uids - set(graph):
        components.append({uid})
    return components


def assign_pools(components: List[Set[str]], pools: int) -> List[Set[str]]:
    assignments: List[Set[str]] = [set() for _ in range(pools)]
    sizes = [0] * pools
    # largest-first bin packing
    for comp in sorted(components, key=len, reverse=True):
        idx = sizes.index(min(sizes))
        assignments[idx].update(comp)
        sizes[idx] += len(comp)
    return assignments


def write_pools(
    entries: List[Dict[str, object]],
    pools: List[Set[str]],
    outdir: pathlib.Path,
    prefix: str = "taskwarrior-pool",
) -> None:
    by_uid: Dict[str, Dict[str, object]] = {e.get("uid"): e for e in entries if e.get("uid")}
    outdir.mkdir(parents=True, exist_ok=True)
    for idx, pool in enumerate(pools, start=1):
        payload = [by_uid[uid] for uid in pool if uid in by_uid]
        outfile = outdir / f"{prefix}-{idx}.json"
        outfile.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"Pool {idx}: {len(payload)} tasks -> {outfile}")


def summarize(pools: List[Set[str]]) -> None:
    for idx, pool in enumerate(pools, start=1):
        print(f"Pool {idx}: {len(pool)} tasks")


def main() -> None:
    parser = argparse.ArgumentParser(description="Split Taskwarrior backlog into dependency-safe pools")
    parser.add_argument("--input", type=pathlib.Path, default=DEFAULT_INPUT, help=f"Taskwarrior JSON (default {DEFAULT_INPUT})")
    parser.add_argument("--outdir", type=pathlib.Path, default=DEFAULT_OUTDIR, help=f"Output directory (default {DEFAULT_OUTDIR})")
    parser.add_argument("--pools", type=int, required=True, help="Number of pools to create")
    args = parser.parse_args()

    entries = load_entries(args.input)
    components = build_components(entries)
    pools = assign_pools(components, args.pools)
    summarize(pools)
    write_pools(entries, pools, args.outdir)


if __name__ == "__main__":
    main()
