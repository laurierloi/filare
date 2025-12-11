#!/usr/bin/env python3
"""
get_structured_review.py

Prints the contents of review directories in a structured, agent-friendly format.

Expected directory layout (as created by tools/review_changes.py):

    outputs/review/<agent_role>-<task_id>-<step_index>/
        meta.txt
        feedback.txt

Usage example:

    uv run python scripts/get_structured_review.py \
        --agent-role FILARE-FIXER \
        --task-id 42
"""

import argparse
import sys
from pathlib import Path
from typing import List


def find_step_dirs(base_dir: Path, agent_role: str, task_id: str) -> List[Path]:
    """
    Find review step directories matching:
        <base_dir>/<agent_role>-<task_id>-*
    Return them sorted by step index if possible.
    """
    pattern = f"{agent_role}-{task_id}-*"
    step_dirs = sorted(base_dir.glob(pattern))

    # Try to sort by numeric step index at the end
    def step_key(p: Path):
        name = p.name
        # Expect suffix after last '-'
        if "-" in name:
            last = name.rsplit("-", 1)[-1]
            try:
                return int(last)
            except ValueError:
                return name
        return name

    step_dirs.sort(key=step_key)
    return step_dirs


def print_step(step_dir: Path, agent_role: str, task_id: str) -> None:
    """
    Print one review step in a structured format.
    """
    name = step_dir.name
    # Extract step index from last '-' part if possible
    if "-" in name:
        step_index = name.rsplit("-", 1)[-1]
    else:
        step_index = "unknown"

    meta_file = step_dir / "meta.txt"
    feedback_file = step_dir / "feedback.txt"

    print("=== REVIEW-STEP-BEGIN ===")
    print(f"step_dir: {step_dir}")
    print(f"agent_role: {agent_role}")
    print(f"task_id: {task_id}")
    print(f"step_index: {step_index}")

    print("--- META-BEGIN ---")
    if meta_file.is_file():
        try:
            print(meta_file.read_text(encoding="utf-8").rstrip("\n"))
        except Exception as e:
            print(f"(error reading meta.txt: {e})")
    else:
        print("(no meta.txt found)")
    print("--- META-END ---")

    print("--- FEEDBACK-BEGIN ---")
    if feedback_file.is_file():
        try:
            print(feedback_file.read_text(encoding="utf-8").rstrip("\n"))
        except Exception as e:
            print(f"(error reading feedback.txt: {e})")
    else:
        print("(no feedback.txt found)")
    print("--- FEEDBACK-END ---")

    print("=== REVIEW-STEP-END ===")
    print()  # blank line between steps


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print structured review data for an agent/task."
    )
    parser.add_argument(
        "--agent-role",
        required=True,
        help="Agent role (e.g. FIXER, REFACTOR, DOCS).",
    )
    parser.add_argument(
        "--task-id",
        required=True,
        help="Task identifier used in the review (e.g. issue or PR id).",
    )
    parser.add_argument(
        "--base-dir",
        type=Path,
        default=Path("outputs/review"),
        help="Base review directory (default: outputs/review).",
    )

    args = parser.parse_args()

    base_dir: Path = args.base_dir
    agent_role: str = args.agent_role
    task_id: str = args.task_id

    if not base_dir.is_dir():
        print(
            f"[get_structured_review] No review base directory found at {base_dir}",
            file=sys.stderr,
        )
        sys.exit(0)

    step_dirs = find_step_dirs(base_dir, agent_role, task_id)
    if not step_dirs:
        print(
            f"[get_structured_review] No review steps found for "
            f"{agent_role}-{task_id} under {base_dir}",
            file=sys.stderr,
        )
        sys.exit(0)

    for step_dir in step_dirs:
        print_step(step_dir, agent_role, task_id)


if __name__ == "__main__":
    main()
