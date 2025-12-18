"""Typer subcommand wrapping src/filare/tools/text_overlap.py."""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

import typer

from filare.tools import text_overlap

overlap_app = typer.Typer(
    add_completion=True,
    no_args_is_help=True,
    context_settings={
        "help_option_names": ["-h", "--help"],
        "allow_interspersed_args": True,
    },
    help="Check rendered HTML for overlapping text.",
)


@overlap_app.callback(invoke_without_command=True)
def overlap(
    paths: List[str] = typer.Argument(
        ...,
        help="HTML files or glob patterns to check.",
    ),
    viewport: str = typer.Option(
        f"{text_overlap.DEFAULT_VIEWPORT[0]}x{text_overlap.DEFAULT_VIEWPORT[1]}",
        "--viewport",
        help="Viewport size WIDTHxHEIGHT.",
    ),
    warn_threshold: float = typer.Option(
        text_overlap.DEFAULT_WARN_THRESHOLD,
        "--warn-threshold",
        help="Warn when overlap depth exceeds this value in px.",
        show_default=True,
    ),
    error_threshold: float = typer.Option(
        text_overlap.DEFAULT_ERROR_THRESHOLD,
        "--error-threshold",
        help="Error when overlap depth exceeds this value in px.",
        show_default=True,
    ),
    json_path: Optional[Path] = typer.Option(
        None,
        "--json",
        help="Write JSON report to this path.",
        resolve_path=True,
    ),
    ignore_selector: List[str] = typer.Option(
        [],
        "--ignore-selector",
        help="CSS selector to ignore (can be repeated).",
    ),
    ignore_text: List[str] = typer.Option(
        [],
        "--ignore-text",
        help="Regex for text to ignore (can be repeated).",
    ),
    config: Path = typer.Option(
        Path(text_overlap.DEFAULT_IGNORE_CONFIG),
        "--config",
        help="Path to overlap ignore config (YAML).",
        resolve_path=True,
    ),
) -> None:
    """Proxy to the text overlap checker while reusing its parsing/formatting."""
    argv = list(paths)
    argv.extend(["--viewport", viewport])
    argv.extend(["--warn-threshold", str(warn_threshold)])
    argv.extend(["--error-threshold", str(error_threshold)])
    if json_path:
        argv.extend(["--json", str(json_path)])
    for selector in ignore_selector:
        argv.extend(["--ignore-selector", selector])
    for pattern in ignore_text:
        argv.extend(["--ignore-text", pattern])
    if config != Path(text_overlap.DEFAULT_IGNORE_CONFIG):
        argv.extend(["--config", str(config)])

    exit_code = text_overlap.main(argv)
    if exit_code != 0:
        raise typer.Exit(code=exit_code)
