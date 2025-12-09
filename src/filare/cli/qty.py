"""Typer-based CLI for managing quantity multipliers."""

from __future__ import annotations

from pathlib import Path
from typing import List

import typer

from filare.models.harness_quantity import HarnessQuantity

app = typer.Typer(
    add_completion=True,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Collect or regenerate harness quantity multipliers.",
)


@app.callback(invoke_without_command=True)
def qty_multipliers(
    files: List[Path] = typer.Argument(
        ...,
        exists=True,
        readable=True,
        dir_okay=False,
        help="Harness YAML files to associate with quantity multipliers.",
    ),
    multiplier_file_name: str = typer.Option(
        "quantity_multipliers.txt",
        "-m",
        "--multiplier-file-name",
        help="Name of file used to fetch or save the qty_multipliers.",
    ),
    force_new: bool = typer.Option(
        False,
        "-f",
        "--force-new",
        help="If set, will always ask for new multipliers.",
    ),
):
    """Collect per-harness quantity multipliers, prompting when missing."""
    harnesses = HarnessQuantity(files, multiplier_file_name)
    if force_new:
        harnesses.qty_multipliers.unlink(missing_ok=True)

    harnesses.fetch_qty_multipliers_from_file()
    return harnesses.multipliers


cli = app
