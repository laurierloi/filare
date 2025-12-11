#!/usr/bin/env python
"""Export backlog items to Taskwarrior-compatible JSON with filtering."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
BACKLOG_DIRS = [REPO_ROOT / "docs" / "issues", REPO_ROOT / "docs" / "features"]
DEFAULT_OUT = REPO_ROOT / "outputs" / "workplan" / "taskwarrior.json"
REQUIRED_KEYS = [
    "uid",
    "status",
    "priority",
    "owner_role",
    "estimate",
    "dependencies",
    "risk",
    "milestone",
]


@dataclass
class BacklogItem:
    uid: str
    title: str
    path: pathlib.Path
    status: str
    priority: str
    owner_role: str
    milestone: str
    dependencies: List[str]


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
        if key not in REQUIRED_KEYS:
            break
        header[key] = value.strip()
        started = True
    return header


def parse_dependencies(raw: str) -> List[str]:
    if not raw or raw == "[]":
        return []
    tokens = re.split(r"[,\s\[\]]+", raw)
    return [t for t in tokens if t]


def title_from_file(path: pathlib.Path) -> str:
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip()
    return path.stem


def load_items() -> List[BacklogItem]:
    items: List[BacklogItem] = []
    for file_path in find_files():
        header = parse_header(file_path)
        if not header:
            continue
        items.append(
            BacklogItem(
                uid=header["uid"],
                title=title_from_file(file_path),
                path=file_path,
                status=header.get("status", "BACKLOG"),
                priority=header.get("priority", "medium"),
                owner_role=header.get("owner_role", ""),
                milestone=header.get("milestone", "backlog"),
                dependencies=parse_dependencies(header.get("dependencies", "")),
            )
        )
    return items


def filter_items(
    items: Iterable[BacklogItem],
    roles: Optional[Sequence[str]],
    priorities: Optional[Sequence[str]],
    milestones: Optional[Sequence[str]],
    statuses: Optional[Sequence[str]],
) -> List[BacklogItem]:
    filtered: List[BacklogItem] = []
    for item in items:
        if roles and item.owner_role not in roles:
            continue
        if priorities and item.priority not in priorities:
            continue
        if milestones and item.milestone not in milestones:
            continue
        if statuses and item.status not in statuses:
            continue
        filtered.append(item)
    return filtered


def to_taskwarrior(item: BacklogItem) -> Dict[str, object]:
    tags = [item.owner_role, item.milestone, item.status]
    if item.path.parts[-2] == "issues":
        tags.append("issue")
    else:
        tags.append("feature")
    return {
        "description": f"{item.uid} {item.title}",
        "project": "filare",
        "tags": tags,
        "depends": item.dependencies if item.dependencies else [],
        # preserve UID as an annotation for round-tripping/backfill
        "annotations": [{"description": f"uid={item.uid} path={item.path.relative_to(REPO_ROOT)}"}],
        "uid": item.uid,
        "status": item.status,
        "priority": item.priority,
        "milestone": item.milestone,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Export backlog to Taskwarrior JSON")
    parser.add_argument("--roles", nargs="*", help="Owner roles to include (FEATURE, REWORK, etc.)")
    parser.add_argument("--priorities", nargs="*", help="Priorities to include")
    parser.add_argument("--milestones", nargs="*", help="Milestones to include")
    parser.add_argument("--statuses", nargs="*", help="Statuses to include (BACKLOG, IN_PROGRESS, BLOCKED, DONE)")
    parser.add_argument(
        "--outfile",
        type=pathlib.Path,
        default=DEFAULT_OUT,
        help=f"Output file (default: {DEFAULT_OUT})",
    )
    args = parser.parse_args()

    items = filter_items(load_items(), args.roles, args.priorities, args.milestones, args.statuses)
    payload = [to_taskwarrior(item) for item in items]
    args.outfile.parent.mkdir(parents=True, exist_ok=True)
    args.outfile.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {len(payload)} tasks to {args.outfile}")


if __name__ == "__main__":
    main()
