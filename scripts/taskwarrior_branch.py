#!/usr/bin/env python
"""Generate a branch name from a Taskwarrior task UID/title."""

from __future__ import annotations

import argparse
import json
import pathlib
import re

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "outputs" / "workplan" / "taskwarrior.json"


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")[:40]


def load_task(path: pathlib.Path, uid: str) -> tuple[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    for entry in data:
        if entry.get("uid") == uid:
            role = entry.get("owner_role") or ""
            desc = entry.get("description") or ""
            title = desc.split(" ", 1)[1] if " " in desc else desc
            return role, title
    raise SystemExit(f"UID {uid} not found in {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate branch name from Taskwarrior task")
    parser.add_argument("--input", type=pathlib.Path, default=DEFAULT_INPUT, help=f"Taskwarrior JSON (default {DEFAULT_INPUT})")
    parser.add_argument("--uid", required=True, help="Task UID to base the branch name on")
    parser.add_argument("--index", type=int, default=1, help="Suffix index to avoid collisions (default: 1)")
    args = parser.parse_args()

    role, title = load_task(args.input, args.uid)
    role_slug = role.lower() if role else "task"
    name_slug = slugify(title) or "task"
    branch = f"{role_slug}/{name_slug}-{args.index}"
    print(branch)


if __name__ == "__main__":
    main()
