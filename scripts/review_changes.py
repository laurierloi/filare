#!/usr/bin/env python
"""
Interactive review command for Filare agents.

This tool walks through changed files step by step, tracks progress in:

    outputs/review/<agent_role>-<task_id>-<step_index>/

For each step it:
- prints the full file path
- shows a short summary of changes
- prompts the operator for feedback
- allows multiple feedback cycles per file, until the operator explicitly types 'next'

Intended usage example:

    python tools/review_changes.py \
        --agent-role FILARE-FIXER \
        --task-id 1234

By default it uses `git diff` to detect changed files relative to a base.
You can adjust the base via --diff-base.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple

# ---------- Helpers for git ----------


def run_cmd(cmd: List[str], cwd: Optional[Path] = None) -> Tuple[int, str, str]:
    """Run a command and return (returncode, stdout, stderr)."""
    proc = subprocess.Popen(
        cmd,
        cwd=str(cwd) if cwd else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = proc.communicate()
    return proc.returncode, out, err


def get_changed_files(diff_base: str, cwd: Path) -> List[str]:
    """
    Return a list of changed file paths (relative) compared to diff_base.

    Default strategy: git diff --name-only <diff_base>...HEAD
    """
    code, out, err = run_cmd(["git", "diff", "--name-only", f"{diff_base}...HEAD"], cwd)
    if code != 0:
        print(f"[review] WARNING: git diff failed ({code}): {err}", file=sys.stderr)
        return []

    files = [line.strip() for line in out.splitlines() if line.strip()]
    return files


def get_diff_summary_for_file(diff_base: str, file_path: str, cwd: Path) -> str:
    """
    Produce a short summary for a file:
    - count added/removed lines (numstat)
    - show a small tail of the diff for context
    """
    # numstat: added removed file
    code, out, err = run_cmd(
        ["git", "diff", "--numstat", f"{diff_base}...HEAD", "--", file_path], cwd
    )
    if code != 0 or not out.strip():
        return f"No diff summary available for {file_path} (git diff issue)."

    line = out.splitlines()[0]
    parts = line.split("\t")
    if len(parts) >= 3:
        added, removed, _fname = parts[:3]
        summary = f"+{added} / -{removed} lines"
    else:
        summary = line.strip()

    # small tail of the unified diff
    code2, out2, err2 = run_cmd(
        [
            "git",
            "diff",
            "--unified=5",
            f"{diff_base}...HEAD",
            "--",
            file_path,
        ],
        cwd,
    )
    diff_tail = "\n".join(out2.splitlines()[-20:]) if out2 else ""

    return f"{summary}\n\nDiff tail:\n{diff_tail}"


# ---------- Review logic ----------


def ensure_review_step_dir(
    base_dir: Path, agent_role: str, task_id: str, step_index: int
) -> Path:
    """
    Create and return a directory like:
        outputs/review/<agent_role>-<task_id>-<step_index>
    """
    base_dir.mkdir(parents=True, exist_ok=True)
    dirname = f"{agent_role}-{task_id}-{step_index}"
    step_dir = base_dir / dirname
    step_dir.mkdir(parents=True, exist_ok=True)
    return step_dir


def prompt_feedback_loop(
    file_path: Path,
    summary: str,
    step_dir: Path,
    cwd: Path,
) -> None:
    """
    Interactive feedback loop for a single file.

    - Prints file info + summary
    - Repeatedly asks for feedback
    - If input is 'next' (exact, case-insensitive), break
    - If input is 'quit', exit the entire review
    - Otherwise treat the input as feedback, append to feedback.txt,
    """
    meta_file = step_dir / "meta.txt"
    meta_file.write_text(
        f"file_path: {file_path}\n" f"summary:\n{summary}\n",
        encoding="utf-8",
    )

    feedback_file = step_dir / "feedback.txt"

    print("\n" + "=" * 80)
    print(f"[REVIEW] File: {file_path}")
    print("-" * 80)
    print(summary)
    print("-" * 80)
    print(
        "Enter feedback for this file.\n"
        "  - Type 'next' to accept and move to the next file.\n"
        "  - Type 'quit' to stop the review entirely.\n"
        "You can provide multiple feedback messages; 'next' must be explicit.\n"
    )

    while True:
        try:
            user_input = input("review> ").strip()
        except EOFError:
            print("\n[review] EOF received, stopping review.")
            sys.exit(0)

        lower = user_input.lower()

        if lower == "next":
            print("[review] Moving to next file.")
            break

        if lower == "quit":
            print("[review] Quitting review.")
            sys.exit(0)

        if not user_input:
            print("[review] Empty input; please type feedback, 'next', or 'quit'.")
            continue

        # Append feedback
        with feedback_file.open("a", encoding="utf-8") as f:
            f.write(user_input + "\n")

        print(f"[review] Recorded feedback in {feedback_file}.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Interactive review command for Filare agents."
    )
    parser.add_argument(
        "--agent-role",
        required=True,
        help="Agent role name (e.g. FILARE-FIXER, REFACTOR, DOCS).",
    )
    parser.add_argument(
        "--task-id",
        required=True,
        help="Task identifier (e.g. issue number, PR id, custom id).",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path("."),
        help="Repository root (default: current directory).",
    )
    parser.add_argument(
        "--diff-base",
        default="origin/main",
        help="Git base for diff comparison (default: origin/main).",
    )

    args = parser.parse_args()
    repo_root: Path = args.repo_root.resolve()

    # Ensure we're in a git repo
    code, out, err = run_cmd(["git", "rev-parse", "--show-toplevel"], repo_root)
    if code != 0:
        print(
            "[review] ERROR: Not inside a git repository " "or git is not available.",
            file=sys.stderr,
        )
        sys.exit(1)

    git_root = Path(out.strip())
    if repo_root != git_root:
        # Align to git root (safer for diff commands)
        repo_root = git_root

    changed_files = get_changed_files(args.diff_base, repo_root)
    if not changed_files:
        print(
            f"[review] No changed files detected relative to {args.diff_base}. "
            "Nothing to review."
        )
        sys.exit(0)

    review_base_dir = repo_root / "outputs" / "review"
    review_base_dir.mkdir(parents=True, exist_ok=True)

    print(
        f"[review] Starting review for agent_role={args.agent_role}, "
        f"task_id={args.task_id}"
    )
    print(f"[review] Found {len(changed_files)} changed file(s) to review.")

    for idx, rel_path in enumerate(changed_files, start=1):
        file_path = repo_root / rel_path
        step_dir = ensure_review_step_dir(
            review_base_dir, args.agent_role, args.task_id, idx
        )

        summary = get_diff_summary_for_file(args.diff_base, rel_path, repo_root)
        prompt_feedback_loop(
            file_path=file_path,
            summary=summary,
            step_dir=step_dir,
            cwd=repo_root,
        )

    print("[review] Review complete.")


if __name__ == "__main__":
    main()
