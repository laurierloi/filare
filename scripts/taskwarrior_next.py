#!/usr/bin/env python
"""List next ready Taskwarrior tasks for a given role, respecting dependencies."""

from __future__ import annotations

from __future__ import annotations

import argparse
import json
import pathlib
from typing import Dict, Iterable, List, Optional, Sequence

from pydantic import BaseModel

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "outputs" / "workplan" / "taskwarrior.json"
DONE_STATUSES = {"DONE", "COMPLETED", "SUCCESS", "CLOSED"}
PRIORITY_ORDER = {"H": 0, "high": 0, "M": 1, "medium": 1, "L": 2, "low": 2}


class Task(BaseModel):
    uid: str
    title: str
    role: str
    status: str
    priority: str
    depends: List[str]
    path: str = ""


Task.model_rebuild()


def load_tasks(path: pathlib.Path) -> List[Task]:
    data = json.loads(path.read_text(encoding="utf-8"))
    tasks: List[Task] = []
    for entry in data:
        uid = entry.get("uid") or ""
        description = entry.get("description") or ""
        title = description.split(" ", 1)[1] if " " in description else description
        depends = entry.get("depends") or []
        annotations = entry.get("annotations") or []
        path_ann = ""
        for ann in annotations:
            text = ann.get("description", "")
            if "path=" in text:
                path_ann = text.split("path=", 1)[1]
                break
        tasks.append(
            Task(
                uid=uid,
                title=title,
                role=extract_role(entry),
                status=str(entry.get("status", "")).upper(),
                priority=str(entry.get("priority", "M")),
                depends=depends,
                path=path_ann,
            )
        )
    return tasks


def extract_role(entry: Dict[str, object]) -> str:
    if entry.get("owner_role"):
        return str(entry["owner_role"])
    for tag in entry.get("tags") or []:
        if isinstance(tag, str) and tag.isupper():
            return tag
    return ""


def ready_tasks(tasks: Iterable[Task], roles: Optional[Sequence[str]]) -> List[Task]:
    by_uid: Dict[str, Task] = {t.uid: t for t in tasks if t.uid}
    done = {t.uid for t in tasks if t.uid and t.status in DONE_STATUSES}

    ready: List[Task] = []
    for task in tasks:
        if not task.uid:
            continue
        if task.status in DONE_STATUSES:
            continue
        if roles and task.role not in roles:
            continue
        if any(dep not in done for dep in task.depends):
            continue
        ready.append(task)
    return sorted(ready, key=lambda t: (PRIORITY_ORDER.get(t.priority, 3), t.uid))


def main() -> None:
    parser = argparse.ArgumentParser(description="List next ready Taskwarrior tasks for a role")
    parser.add_argument(
        "--input",
        type=pathlib.Path,
        default=DEFAULT_INPUT,
        help=f"Taskwarrior JSON export (default: {DEFAULT_INPUT})",
    )
    parser.add_argument("--roles", nargs="*", help="Owner roles to include (FEATURE, TOOLS, etc.)")
    parser.add_argument("--limit", type=int, default=10, help="Number of tasks to show (default: 10)")
    args = parser.parse_args()

    tasks = load_tasks(args.input)
    ready = ready_tasks(tasks, args.roles)
    print(f"Ready tasks (limit {args.limit}) from {args.input}:")
    for task in ready[: args.limit]:
        print(
            f"- {task.uid} [{task.role or 'UNKNOWN'}] pri={task.priority} status={task.status}"
            f" deps={len(task.depends)} title={task.title}"
            + (f" ({task.path})" if task.path else "")
        )


if __name__ == "__main__":
    main()
