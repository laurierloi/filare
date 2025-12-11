#!/usr/bin/env python
"""Generate a branch name from a Taskwarrior task UID/title and optionally check it out."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
from typing import Optional

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "outputs" / "workplan" / "taskwarrior.json"


def run_git(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=REPO_ROOT, check=False, capture_output=True, text=True)


def git_fetch_origin() -> None:
    subprocess.run(["git", "fetch", "origin"], cwd=REPO_ROOT, check=False)


def branch_exists(name: str) -> bool:
    local = run_git(["rev-parse", "--verify", "--quiet", f"refs/heads/{name}"]).returncode == 0
    remote = run_git(["rev-parse", "--verify", "--quiet", f"refs/remotes/origin/{name}"]).returncode == 0
    return local or remote


def current_branch() -> str:
    proc = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    return proc.stdout.strip() if proc.returncode == 0 else ""


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


def next_branch_name(role: str, title: str) -> str:
    role_slug = role.lower() if role else "task"
    name_slug = slugify(title) or "task"
    i = 1
    while True:
        candidate = f"{role_slug}/{name_slug}-{i}"
        if not branch_exists(candidate):
            return candidate
        i += 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate/checkout branch from Taskwarrior task")
    parser.add_argument("--input", type=pathlib.Path, default=DEFAULT_INPUT, help=f"Taskwarrior JSON (default {DEFAULT_INPUT})")
    parser.add_argument("--uid", required=True, help="Task UID to base the branch name on")
    parser.add_argument("--checkout", action="store_true", help="If set, git checkout -b <branch>")
    args = parser.parse_args()

    git_fetch_origin()
    role, title = load_task(args.input, args.uid)
    branch = next_branch_name(role, title)
    print(branch)

    if args.checkout:
        current = current_branch()
        if current == branch:
            print(f"Already on branch {branch}; nothing to do.")
            return
        subprocess.run(["git", "checkout", "-b", branch], cwd=REPO_ROOT, check=False)


if __name__ == "__main__":
    main()
