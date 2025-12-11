#!/usr/bin/env python
"""Validate backlog headers in docs/issues and docs/features."""

from __future__ import annotations

import pathlib
import re
import sys
from typing import Dict, List, Tuple

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
BACKLOG_DIRS = [REPO_ROOT / "docs" / "issues", REPO_ROOT / "docs" / "features"]
REQUIRED_KEYS = ["uid", "status", "priority", "owner_role", "estimate", "dependencies", "risk", "milestone"]
STATUS_VALUES = {"BACKLOG", "IN_PROGRESS", "BLOCKED", "DONE"}
PRIORITY_VALUES = {"low", "medium", "high", "urgent"}
OWNER_VALUES = {"FEATURE", "REWORK", "TOOLS", "DOCUMENTATION", "COVERAGE", "UI", "EXPLORATOR", "VALIDATOR", "JUDGE"}
RISK_VALUES = {"low", "medium", "high"}


def collect_files() -> List[pathlib.Path]:
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
            continue  # skip leading blanks before header
        if ":" not in line:
            break
        key, value = line.split(":", 1)
        key = key.strip()
        if key not in REQUIRED_KEYS:
            break
        header[key] = value.strip()
        started = True
        if not value.strip():
            # allow parsing to continue; empty values will be validated later
            continue
    if not header:
        return {}
    return header


def validate_uid(uid: str, path: pathlib.Path) -> str | None:
    if path.parts[-2] == "issues":
        if not re.fullmatch(r"ISS-\d{4}", uid):
            return "uid must match ISS-<4 digits>"
    else:
        if not re.fullmatch(r"FEAT-[A-Z]+-\d{4}", uid):
            return "uid must match FEAT-<AREA>-<4 digits>"
    return None


def validate_header(path: pathlib.Path, header: Dict[str, str]) -> List[str]:
    errors: List[str] = []
    missing = [k for k in REQUIRED_KEYS if k not in header]
    if missing:
        errors.append(f"missing keys: {', '.join(missing)}")
        return errors

    uid_error = validate_uid(header["uid"], path)
    if uid_error:
        errors.append(uid_error)

    if header["status"] not in STATUS_VALUES:
        errors.append(f"status must be one of {sorted(STATUS_VALUES)}")

    if header["priority"] not in PRIORITY_VALUES:
        errors.append(f"priority must be one of {sorted(PRIORITY_VALUES)}")

    if header["owner_role"] not in OWNER_VALUES:
        errors.append(f"owner_role must be one of {sorted(OWNER_VALUES)}")

    if header["risk"] not in RISK_VALUES:
        errors.append(f"risk must be one of {sorted(RISK_VALUES)}")

    deps = header.get("dependencies", "")
    if deps and deps != "[]":
        # allow comma or bracketed list; validate uid-like tokens.
        dep_tokens = re.split(r"[,\s\[\]]+", deps)
        dep_tokens = [d for d in dep_tokens if d]
        for dep in dep_tokens:
            if not (re.fullmatch(r"ISS-\d{4}", dep) or re.fullmatch(r"FEAT-[A-Z]+-\d{4}", dep)):
                errors.append(f"dependency '{dep}' is not a valid UID")
    return errors


def main() -> int:
    files = collect_files()
    errors: List[Tuple[pathlib.Path, List[str]]] = []
    seen_uids: Dict[str, pathlib.Path] = {}
    for path in files:
        header = parse_header(path)
        if not header:
            errors.append((path, ["no header detected"]))
            continue
        errs = validate_header(path, header)
        uid = header.get("uid")
        if uid:
            if uid in seen_uids:
                errors.append((path, [f"duplicate uid also used in {seen_uids[uid]}"]))
            else:
                seen_uids[uid] = path
        if errs:
            errors.append((path, errs))

    if errors:
        print("Header validation failed:", file=sys.stderr)
        for path, errs in errors:
            for err in errs:
                print(f"- {path}: {err}", file=sys.stderr)
        return 1

    print(f"All headers valid in {len(files)} backlog files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
