#!/usr/bin/env python
"""Generate a Graphviz dependency/timeline graph from backlog headers."""

from __future__ import annotations

import argparse
import pathlib
import subprocess
from typing import Dict, Iterable, List

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
BACKLOG_DIRS = [REPO_ROOT / "docs" / "issues", REPO_ROOT / "docs" / "features"]
DOT_PATH = REPO_ROOT / "outputs" / "workplan" / "timeline.dot"
SVG_PATH = REPO_ROOT / "outputs" / "workplan" / "timeline.svg"
HEADER_KEYS = ["uid", "status", "priority", "owner_role", "estimate", "dependencies", "risk", "milestone"]

STATUS_COLORS = {
    "BACKLOG": "#d3d3d3",
    "IN_PROGRESS": "#ffdd57",
    "BLOCKED": "#f66",
    "DONE": "#8fce00",
}

PRIORITY_COLORS = {
    "low": "#cfe2ff",
    "medium": "#b8daff",
    "high": "#80bdff",
    "urgent": "#ff6b6b",
}


def find_files() -> List[pathlib.Path]:
    files: List[pathlib.Path] = []
    for base in BACKLOG_DIRS:
        files.extend(sorted(base.rglob("*.md")))
    return files


def parse_header(path: pathlib.Path) -> Dict[str, str]:
    header: Dict[str, str] = {}
    with path.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()
    started = False
    for line in lines[1:]:
        if not started and not line.strip():
            continue
        if ":" not in line:
            break
        key, value = line.split(":", 1)
        key = key.strip()
        if key not in HEADER_KEYS:
            break
        header[key] = value.strip()
        started = True
    return header


def title_from_file(path: pathlib.Path) -> str:
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip()
    return path.stem


def collect_items() -> List[Dict[str, str]]:
    items: List[Dict[str, str]] = []
    for path in find_files():
        header = parse_header(path)
        uid = header.get("uid")
        if not uid:
            continue
        items.append(
            {
                "uid": uid,
                "status": header.get("status", "BACKLOG"),
                "priority": header.get("priority", "medium"),
                "owner_role": header.get("owner_role", ""),
                "milestone": header.get("milestone", "backlog"),
                "dependencies": header.get("dependencies", ""),
                "title": title_from_file(path),
                "path": path.relative_to(REPO_ROOT),
            }
        )
    return items


def parse_dependencies(raw: str) -> List[str]:
    if not raw or raw == "[]":
        return []
    deps = []
    for token in raw.replace("[", "").replace("]", "").replace(",", " ").split():
        if token:
            deps.append(token)
    return deps


def node_color(item: Dict[str, str]) -> str:
    return STATUS_COLORS.get(item["status"], "#d3d3d3")


def label(item: Dict[str, str]) -> str:
    return f"{item['uid']}\\n{item['title']}\\n{item['milestone']}\\n{item['owner_role']}"


def generate_dot(items: Iterable[Dict[str, str]]) -> str:
    lines = ["digraph backlog {", '  rankdir=LR;', '  node [shape=box, style="filled,rounded"];']
    uid_map = {item["uid"]: item for item in items}
    # Nodes
    for item in items:
        color = node_color(item)
        lines.append(f'  "{item["uid"]}" [label="{label(item)}", fillcolor="{color}"];')
    # Edges
    for item in items:
        for dep in parse_dependencies(item["dependencies"]):
            if dep in uid_map:
                lines.append(f'  "{dep}" -> "{item["uid"]}";')
    # Milestone clusters
    milestones: Dict[str, List[str]] = {}
    for item in items:
        milestones.setdefault(item["milestone"], []).append(item["uid"])
    for milestone, ids in milestones.items():
        lines.append(f'  subgraph "cluster_{milestone}" {{ label="{milestone}"; style=dashed; color="#aaaaaa";')
        for uid in ids:
            lines.append(f'    "{uid}";')
        lines.append("  }")
    lines.append("}")
    return "\n".join(lines) + "\n"


def maybe_render_svg(dot_path: pathlib.Path, svg_path: pathlib.Path) -> None:
    try:
        subprocess.run(["dot", "-V"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception:
        print("dot not available; skipping SVG render")
        return
    try:
        subprocess.run(["dot", "-Tsvg", "-o", str(svg_path), str(dot_path)], check=True)
        print(f"Wrote SVG to {svg_path}")
    except Exception as exc:
        print(f"dot render failed: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Graphviz timeline/dependency graph from backlog")
    parser.add_argument("--no-svg", action="store_true", help="Do not render SVG")
    args = parser.parse_args()

    items = collect_items()
    DOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    dot_content = generate_dot(items)
    DOT_PATH.write_text(dot_content, encoding="utf-8")
    print(f"Wrote DOT to {DOT_PATH}")
    if not args.no_svg:
        maybe_render_svg(DOT_PATH, SVG_PATH)


if __name__ == "__main__":
    main()
