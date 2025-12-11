#!/usr/bin/env python
"""
Generate filare_commands.yaml from the Justfile plus optional extra commands.

Usage:
    python tools/generate_filare_commands.py \
        --justfile Justfile \
        --output filare_commands.yaml \
        [--extra extra_commands.yaml]

The generated YAML is meant to be consumed by agents (Codex, etc.) as a
high-level command catalog: each command has metadata + actions describing
validation, error handling, and user-facing behavior.
"""

import argparse
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# ---------- Justfile parsing ----------


RE_RECIPE = re.compile(r"^([A-Za-z0-9_-]+):\s*$")


class Recipe:
    def __init__(self, name: str):
        self.name = name
        self.body: List[str] = []
        self.description_lines: List[str] = []

    @property
    def description(self) -> Optional[str]:
        if not self.description_lines:
            return None
        # Strip leading "# " and join
        cleaned = []
        for line in self.description_lines:
            line = line.strip()
            if line.startswith("#"):
                line = line[1:].lstrip()
            cleaned.append(line)
        text = " ".join(cleaned).strip()
        return text or None


def parse_justfile(justfile_path: Path) -> Dict[str, Recipe]:
    """
    Very small parser for a Justfile:
    - recipe lines look like: "name:"
    - comments immediately above a recipe become its description
    - we keep the body lines in case they're useful later
    """
    text = justfile_path.read_text(encoding="utf-8").splitlines()

    recipes: Dict[str, Recipe] = {}
    pending_comment_block: List[str] = []
    current_recipe: Optional[Recipe] = None
    current_indent: Optional[int] = None

    for raw_line in text:
        line = raw_line.rstrip("\n")

        # Blank line: keep separating blocks, but don't clear comments yet
        if not line.strip():
            # Preserve spacing between comment lines
            if pending_comment_block:
                pending_comment_block.append(line)
            continue

        # Comment line
        if line.lstrip().startswith("#"):
            pending_comment_block.append(line)
            continue

        # Check for start of a recipe
        match = RE_RECIPE.match(line)
        if match:
            name = match.group(1)
            current_recipe = Recipe(name)
            current_recipe.description_lines = pending_comment_block[:]
            pending_comment_block = []
            recipes[name] = current_recipe
            # Determine indent for body lines (first non-empty after this)
            current_indent = None
            continue

        # Body lines for the current recipe
        if current_recipe is not None:
            # Determine indentation on first body line
            if current_indent is None and line.strip():
                current_indent = len(line) - len(line.lstrip(" "))

            current_recipe.body.append(line)
        else:
            # Non-comment, non-recipe line outside a recipe; ignore.
            pending_comment_block = []

    return recipes


# ---------- Heuristics for categories & actions ----------


def infer_category(name: str) -> str:
    """Heuristic category from recipe name."""

    # Unified project_management group
    project_mgmt_keywords = [
        "taskwarrior",
        "mermaid-gantt",
        "check-backlog-headers",
        "timeline-graphviz",
        "test-mermaid",
    ]
    if any(key in name for key in project_mgmt_keywords):
        return "project_management"
    if name in {"review", "get-structured-review"}:
        return "project_management"

    if name in {"lint", "pre-commit", "git-status", "check-tools"}:
        return "lint"

    if name.startswith("test-") or name in {"test-all", "test-fast"}:
        return "test"

    if name.startswith("build-") or name in {"build-docs", "build-examples"}:
        return "build"

    if any(
        key in name
        for key in [
            "example-",
            "demo-",
            "filare-settings",
            "check-overlap",
            "bom-check",
        ]
    ):
        return "filare"

    if name == "version":
        return "meta"

    if name == "install-deps":
        return "env"

    return "misc"


def is_safe_for_agents(name: str, category: str) -> bool:
    """Decide if agents are allowed to run this command automatically."""
    # Explicitly forbidden
    if name == "install-deps":
        return False

    # Review is interactive with a human; agents should not auto-run it
    if name == "review":
        return False

    # get-structured-review is read-only and safe
    if name == "get-structured-review":
        return True

    # Some meta commands may be okay but not super useful
    if category == "meta":
        return True

    # For now, everything else is allowed
    return True


def default_actions_for_category(category: str) -> List[Dict[str, Any]]:
    """
    Generic action pipeline. These 'actions' are *declarative*:
    your agent framework can decide how to implement them.
    """
    base_run = {
        "name": "run-shell-command",
        "stage": "main",
        "params": {
            "capture_output": True,
            "print_live": False,
        },
    }

    summarize_success = {
        "name": "summarize-output",
        "stage": "on_success",
        "params": {
            "show_tail_lines": 40,
            "include_suggestions": False,
        },
    }

    summarize_error = {
        "name": "summarize-error",
        "stage": "on_error",
        "params": {
            "show_tail_lines": 80,
            "classify_error": True,
            "suggest_next_actions": True,
        },
    }

    if category == "lint":
        return [
            {
                "name": "validate-env",
                "stage": "before",
                "params": {"checks": ["repo-present", "python-available"]},
            },
            base_run,
            {
                "name": "parse-lint-output",
                "stage": "on_error",
                "params": {"group_by_file": True},
            },
            summarize_success,
            summarize_error,
        ]

    if category == "test":
        return [
            {
                "name": "validate-env",
                "stage": "before",
                "params": {"checks": ["repo-present", "python-available"]},
            },
            base_run,
            {
                "name": "parse-test-output",
                "stage": "on_error",
                "params": {"framework": "pytest"},
            },
            summarize_success,
            summarize_error,
        ]

    if category == "build":
        return [
            {
                "name": "validate-env",
                "stage": "before",
                "params": {"checks": ["repo-present"]},
            },
            base_run,
            summarize_success,
            summarize_error,
        ]

    if category == "filare":
        return [
            {
                "name": "validate-env",
                "stage": "before",
                "params": {
                    "checks": ["repo-present", "python-available", "filare-installed"]
                },
            },
            base_run,
            {
                "name": "validate-filare-output",
                "stage": "on_success",
                "params": {},
            },
            summarize_success,
            summarize_error,
        ]

    if category == "project_management":
        # Generic project-management commands (taskwarrior, timeline, mermaid, review tools)
        return [
            {
                "name": "validate-env",
                "stage": "before",
                "params": {
                    "checks": [
                        "repo-present",
                        "python-available",
                    ]
                },
            },
            base_run,
            summarize_success,
            summarize_error,
        ]

    if category == "env":
        return [
            {
                "name": "validate-env",
                "stage": "before",
                "params": {"checks": ["user-confirmation-required"]},
            },
            base_run,
            summarize_success,
            summarize_error,
        ]

    # Default / misc
    return [
        {
            "name": "validate-env",
            "stage": "before",
            "params": {"checks": ["repo-present"]},
        },
        base_run,
        summarize_success,
        summarize_error,
    ]


def build_command_entry(recipe: Recipe) -> Dict[str, Any]:
    """
    Convert a Recipe object into a command entry for filare_commands.yaml.
    """
    name = recipe.name
    category = infer_category(name)

    # Special handling for review-related commands
    if name == "review":
        run_command = 'just review agent_role="{agent_role}" task_id="{task_id}"'
        safe = is_safe_for_agents(name, category)
        entry: Dict[str, Any] = {
            "name": name,
            "origin": "justfile",
            "run": run_command,
            "category": category,
            "safe_for_agents": safe,
            "actions": [
                {
                    "name": "validate-env",
                    "stage": "before",
                    "params": {
                        "checks": [
                            "repo-present",
                            "python-available",
                        ],
                        "require_agent_role": True,
                        "require_task_id": True,
                    },
                },
                {
                    # Interactive review, so we expect TTY and no capture
                    "name": "run-shell-command",
                    "stage": "main",
                    "params": {
                        "capture_output": False,
                        "print_live": True,
                    },
                },
                {
                    "name": "summarize-review-log",
                    "stage": "on_success",
                    "params": {
                        "review_dir_pattern": (
                            "outputs/review/{agent_role}-{task_id}-*"
                        )
                    },
                },
            ],
        }
        if recipe.description:
            entry["description"] = recipe.description
        return entry

    if name == "get-structured-review":
        run_command = (
            'just get-structured-review agent_role="{agent_role}" task_id="{task_id}"'
        )
        safe = is_safe_for_agents(name, category)
        entry = {
            "name": name,
            "origin": "justfile",
            "run": run_command,
            "category": category,
            "safe_for_agents": safe,
            "actions": [
                {
                    "name": "validate-env",
                    "stage": "before",
                    "params": {
                        "checks": [
                            "repo-present",
                            "python-available",
                        ],
                        "require_agent_role": True,
                        "require_task_id": True,
                    },
                },
                {
                    # This is read-only structured output; capture is helpful
                    "name": "run-shell-command",
                    "stage": "main",
                    "params": {
                        "capture_output": True,
                        "print_live": False,
                    },
                },
                {
                    "name": "parse-structured-review",
                    "stage": "on_success",
                    "params": {
                        "format": "review-steps-v1",
                    },
                },
            ],
        }
        if recipe.description:
            entry["description"] = recipe.description
        return entry

    # Default command: "just <recipe>"
    run_command = f"just {name}"
    safe = is_safe_for_agents(name, category)

    entry = {
        "name": name,
        "origin": "justfile",
        "run": run_command,
        "category": category,
        "safe_for_agents": safe,
        "actions": default_actions_for_category(category),
    }

    if recipe.description:
        entry["description"] = recipe.description

    return entry


# ---------- Extra commands merging ----------


def load_extra_commands(path: Path) -> Dict[str, Any]:
    """
    Load extra commands from a YAML file.

    Supported formats:
      commands:
        my-command:
          run: "some shell"
          description: "..."
          category: "..."
          safe_for_agents: true
          actions: [...]
    or:
      extra_commands:
        my-command: {...}
    """
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    cmds = {}

    if "commands" in data and isinstance(data["commands"], dict):
        cmds.update(data["commands"])
    if "extra_commands" in data and isinstance(data["extra_commands"], dict):
        cmds.update(data["extra_commands"])

    return cmds


def merge_commands(base: Dict[str, Any], extra: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge extra commands into base. Extra entries override base.
    """
    merged = dict(base)
    for name, cmd in extra.items():
        merged[name] = cmd
    return merged


# ---------- Main ----------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate filare_commands.yaml from Justfile + optional extras."
    )
    parser.add_argument(
        "--justfile",
        type=Path,
        default=Path("Justfile"),
        help="Path to the Justfile (default: ./Justfile)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("filare_commands.yaml"),
        help="Output YAML file (default: filare_commands.yaml)",
    )
    parser.add_argument(
        "--extra",
        type=Path,
        default=None,
        help="Optional YAML file with additional/custom command definitions.",
    )

    args = parser.parse_args()

    if not args.justfile.is_file():
        raise SystemExit(f"Justfile not found at: {args.justfile}")

    recipes = parse_justfile(args.justfile)

    # Build base command entries from Justfile
    base_commands: Dict[str, Any] = {}
    for name, recipe in recipes.items():
        # You can skip default here if you don't want it as a runnable command
        # but keeping it is harmless as a 'meta' command.
        cmd_entry = build_command_entry(recipe)
        base_commands[name] = cmd_entry

    # Merge extra/custom commands if provided
    if args.extra:
        if not args.extra.is_file():
            raise SystemExit(f"Extra commands file not found at: {args.extra}")
        extra_commands = load_extra_commands(args.extra)
        base_commands = merge_commands(base_commands, extra_commands)

    output_data = {
        "version": 1,
        "commands": base_commands,
    }

    yaml_text = yaml.safe_dump(
        output_data,
        sort_keys=True,
        default_flow_style=False,
    )
    args.output.write_text(yaml_text, encoding="utf-8")
    print(f"Wrote {args.output} with {len(base_commands)} commands.")


if __name__ == "__main__":
    main()
