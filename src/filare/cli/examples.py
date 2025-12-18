"""Typer subcommand that proxies src/filare/tools/build_examples.py."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import typer

from filare.tools import build_examples

_DEFAULT_GROUPS = list(build_examples.groups.keys())
_ACTIONS = {"build", "clean", "compare", "diff", "restore"}

examples_app = typer.Typer(
    add_completion=True,
    no_args_is_help=True,
    context_settings={
        "help_option_names": ["-h", "--help"],
        "allow_interspersed_args": True,
    },
    help="Build or clean Filare example outputs.",
)


def _validate_action(action: str) -> str:
    action_lower = action.lower()
    if action_lower not in _ACTIONS:
        raise typer.BadParameter(
            f"Unsupported action '{action}'. Choose from: {', '.join(sorted(_ACTIONS))}."
        )
    return action_lower


def _validate_groups(groups: List[str]) -> List[str]:
    invalid = [g for g in groups if g not in build_examples.groups]
    if invalid:
        raise typer.BadParameter(
            f"Unknown group(s): {', '.join(invalid)}. "
            f"Valid groups: {', '.join(sorted(build_examples.groups.keys()))}"
        )
    return groups


@examples_app.callback(invoke_without_command=True)
def examples(
    action: str = typer.Option(
        "build",
        "-a",
        "--action",
        help="Action to perform (build, clean; other values are reserved).",
        show_default=True,
    ),
    groups: List[str] = typer.Option(
        _DEFAULT_GROUPS,
        "-g",
        "--groups",
        help="Groups to process.",
        show_default=False,
    ),
    output_dir: Optional[Path] = typer.Option(
        None,
        "-o",
        "--output-dir",
        file_okay=False,
        dir_okay=True,
        writable=True,
        readable=True,
        resolve_path=True,
        help="Optional base directory for generated outputs (defaults to in-place).",
    ),
) -> None:
    """Invoke the example builder with the same semantics as the tooling script."""
    validated_action = _validate_action(action)
    selected_groups = _validate_groups(groups or _DEFAULT_GROUPS)

    if validated_action == "build":
        build_examples.build_generated(selected_groups, output_base=output_dir)
    elif validated_action == "clean":
        build_examples.clean_generated(selected_groups)
    # The other actions (compare/diff/restore) are accepted for compatibility
    # but intentionally perform no work to mirror the legacy script behavior.
