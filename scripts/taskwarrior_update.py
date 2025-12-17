#!/usr/bin/env python
"""Update a Taskwarrior task in the exported JSON (status/annotations)."""

from __future__ import annotations

import argparse
import json
import pathlib
from datetime import datetime
from typing import Dict, List, Optional

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "outputs" / "workplan" / "taskwarrior.json"
VALID_STATUS = {"PENDING", "IN_PROGRESS", "BLOCKED", "DONE"}


def load_entries(path: pathlib.Path) -> List[Dict[str, object]]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_entries(path: pathlib.Path, entries: List[Dict[str, object]]) -> None:
    path.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    print(f"Wrote {len(entries)} tasks to {path}")


def find_entry(entries: List[Dict[str, object]], uid: str) -> Optional[Dict[str, object]]:
    for entry in entries:
        if entry.get("uid") == uid:
            return entry
    return None


def add_annotation(entry: Dict[str, object], text: str) -> None:
    annotations = entry.setdefault("annotations", [])
    annotations.append({"description": text})


def main() -> None:
    parser = argparse.ArgumentParser(description="Update a Taskwarrior task in exported JSON")
    parser.add_argument("--input", type=pathlib.Path, default=DEFAULT_INPUT, help=f"Taskwarrior JSON (default {DEFAULT_INPUT})")
    parser.add_argument("--uid", required=True, help="Task UID to update")
    parser.add_argument("--status", help="New status (PENDING, IN_PROGRESS, BLOCKED, DONE)")
    parser.add_argument("--note", help="Annotation/note to add")
    parser.add_argument("--done", action="store_true", help="Mark as done and stamp completion time")
    args = parser.parse_args()

    entries = load_entries(args.input)
    entry = find_entry(entries, args.uid)
    if not entry:
        raise SystemExit(f"UID {args.uid} not found in {args.input}")

    if args.status:
        status = args.status.upper()
        if status not in VALID_STATUS:
            raise SystemExit(f"Invalid status {args.status}; must be one of {sorted(VALID_STATUS)}")
        entry["status"] = status

    if args.done:
        entry["status"] = "DONE"
        add_annotation(entry, f"completed_at={datetime.utcnow().isoformat()}Z")

    if args.note:
        add_annotation(entry, args.note)

    save_entries(args.input, entries)


if __name__ == "__main__":
    main()
