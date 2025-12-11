#!/usr/bin/env python
"""Backfill backlog headers from a Taskwarrior JSON export (uid-based)."""

from __future__ import annotations

import argparse
import json
import pathlib
from typing import Dict, List, Tuple

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
BACKLOG_DIRS = [REPO_ROOT / "docs" / "issues", REPO_ROOT / "docs" / "features"]
HEADER_KEYS = ["uid", "status", "priority", "owner_role", "estimate", "dependencies", "risk", "milestone"]
UPDATE_KEYS = {"status", "priority", "milestone"}


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


def replace_header(path: pathlib.Path, new_header: Dict[str, str]) -> None:
    with path.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()
    out = [lines[0].rstrip("\n")]
    i = 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    # skip old header
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            break
        if ":" in line and line.split(":", 1)[0].strip() in HEADER_KEYS:
            i += 1
            continue
        break
    out.append("")
    for key in HEADER_KEYS:
        out.append(f"{key}: {new_header.get(key, '')}")
    out.append("")
    out.extend(l.rstrip("\n") for l in lines[i:])
    path.write_text("\n".join(out).rstrip("\n") + "\n", encoding="utf-8")


def load_backlog() -> Dict[str, Tuple[pathlib.Path, Dict[str, str]]]:
    mapping: Dict[str, Tuple[pathlib.Path, Dict[str, str]]] = {}
    for path in find_files():
        header = parse_header(path)
        uid = header.get("uid")
        if uid:
            mapping[uid] = (path, header)
    return mapping


def main() -> None:
    parser = argparse.ArgumentParser(description="Backfill backlog headers from Taskwarrior JSON")
    parser.add_argument("input", type=pathlib.Path, help="Taskwarrior JSON export with uid fields")
    parser.add_argument("--apply", action="store_true", help="Apply updates instead of dry-run")
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    backlog = load_backlog()
    updates: List[str] = []
    for entry in data:
        uid = entry.get("uid")
        if not uid or uid not in backlog:
            continue
        path, header = backlog[uid]
        new_header = dict(header)
        changed = False
        for key in UPDATE_KEYS:
            if key in entry and entry[key] and entry[key] != header.get(key):
                new_header[key] = entry[key]
                updates.append(f"{uid}: {path} {key} {header.get(key)} -> {entry[key]}")
                changed = True
        if args.apply and changed:
            replace_header(path, new_header)

    if updates:
        print("Planned updates:")
        for line in updates:
            print(f"- {line}")
    else:
        print("No updates found.")

    if args.apply:
        print("Applied updates above (if any).")
    else:
        print("Dry-run only. Re-run with --apply to write changes.")


if __name__ == "__main__":
    main()
