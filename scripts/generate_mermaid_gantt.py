#!/usr/bin/env python
"""Generate Mermaid Gantt from backlog headers in docs/issues and docs/features."""

from __future__ import annotations

import datetime
import pathlib
import re
from typing import Dict, Iterable, List, Optional, Tuple

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
BACKLOG_DIRS = [REPO_ROOT / "docs" / "issues", REPO_ROOT / "docs" / "features"]
OUTPUT_PATH = REPO_ROOT / "outputs" / "workplan" / "gantt.md"
DOCS_OUTPUT_PATH = REPO_ROOT / "docs" / "workplan" / "gantt.md"
ALLOWED_KEYS = {
    "uid",
    "status",
    "priority",
    "owner_role",
    "estimate",
    "dependencies",
    "risk",
    "milestone",
}


def find_backlog_files() -> List[pathlib.Path]:
    files: List[pathlib.Path] = []
    for base in BACKLOG_DIRS:
        files.extend(sorted(base.rglob("*.md")))
    return files


def parse_header(path: pathlib.Path) -> Optional[Dict[str, str]]:
    header: Dict[str, str] = {}
    with path.open("r", encoding="utf-8") as fh:
        lines = fh.readlines()
    # Expect title on first line; header follows as key: value pairs until blank line.
    for line in lines[1:]:
        stripped = line.strip()
        if not stripped:
            break
        if ":" not in stripped:
            break
        key, value = stripped.split(":", 1)
        key = key.strip()
        if key not in ALLOWED_KEYS:
            break
        header[key] = value.strip()
    if "uid" not in header:
        return None
    header.setdefault("milestone", "backlog")
    header.setdefault("dependencies", "")
    return header


def sanitize_id(uid: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", uid)


def title_from_file(path: pathlib.Path) -> str:
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            stripped = line.strip()
            if stripped.startswith("#"):
                return stripped.lstrip("#").strip()
    return path.stem


def build_tasks(files: Iterable[pathlib.Path]) -> List[Dict[str, str]]:
    tasks: List[Dict[str, str]] = []
    for path in files:
        header = parse_header(path)
        if not header:
            continue
        uid = header["uid"]
        tasks.append(
            {
                "uid": uid,
                "id": sanitize_id(uid),
                "milestone": header.get("milestone", "backlog"),
                "dependencies": header.get("dependencies", "").strip(),
                "title": title_from_file(path),
            }
        )
    tasks.sort(key=lambda t: t["uid"])
    return tasks


def generate_mermaid(tasks: List[Dict[str, str]]) -> str:
    base_date = datetime.date(2025, 1, 1)
    lines: List[str] = ["```mermaid", "gantt", "  dateFormat  YYYY-MM-DD", "  title Filare Backlog Gantt", "  excludes    weekends"]
    # Group tasks by milestone (section).
    milestones: Dict[str, List[Dict[str, str]]] = {}
    for task in tasks:
        milestones.setdefault(task["milestone"], []).append(task)
    idx = 0
    id_map = {t["uid"]: t["id"] for t in tasks}
    for milestone, section_tasks in sorted(milestones.items()):
        lines.append(f"  section {milestone}")
        for task in section_tasks:
            start_date = base_date + datetime.timedelta(days=idx)
            display = f"{task['uid']} ({task['title']})"
            dep = task["dependencies"]
            if dep:
                # Take the first dependency if multiple are listed.
                dep_uid = dep.split(",")[0].strip(" []")
                dep_id = id_map.get(dep_uid, sanitize_id(dep_uid))
                lines.append(f"  {display} :{task['id']}, after {dep_id}, 1d")
            else:
                lines.append(f"  {display} :{task['id']}, {start_date.isoformat()}, 1d")
            idx += 1
    lines.append("```")
    return "\n".join(lines) + "\n"


def main() -> None:
    tasks = build_tasks(find_backlog_files())
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOCS_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    content = generate_mermaid(tasks)
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    DOCS_OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"Wrote Mermaid Gantt with {len(tasks)} tasks to {OUTPUT_PATH} and {DOCS_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
