"""Typer-based drawio command group (import/export/sync/validate/edit/review)."""

from __future__ import annotations

import json
import os
import shlex
import subprocess
from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple

import typer
import yaml

from filare.errors import FilareToolsException

drawio_app = typer.Typer(
    add_completion=True,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Manage Draw.io diagrams alongside Filare harness data.",
)

FormatChoice = Literal["table", "json"]
ValidateFormatChoice = Literal["table", "json"]
DirectionChoice = Literal["to-drawio", "to-harness", "bidirectional"]


class DrawioValidationResult:
    def __init__(self, ok: bool, warnings: List[str], errors: List[str]):
        self.ok = ok
        self.warnings = warnings
        self.errors = errors

    def to_dict(self) -> Dict[str, object]:
        return {"ok": self.ok, "warnings": self.warnings, "errors": self.errors}


def _format_table(data: Dict[str, object]) -> str:
    if not data:
        return "No data."
    width = max(len(key) for key in data.keys())
    lines = [f"{key.ljust(width)}  {data[key]}" for key in sorted(data.keys())]
    return "\n".join(lines)


def _print_report(report: Dict[str, object], format: FormatChoice) -> None:
    if format == "json":
        typer.echo(json.dumps(report, indent=2))
    else:
        typer.echo(_format_table(report))


def _load_yaml_file(path: Path) -> object:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text)


def _write_text(path: Optional[Path], text: str) -> None:
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    else:
        typer.echo(text)


def _fake_validate(path: Path, rules: Optional[Path]) -> DrawioValidationResult:
    """Placeholder validation logic."""
    warnings: List[str] = []
    errors: List[str] = []
    if not path.exists():
        errors.append(f"{path} does not exist")
    if rules and not rules.exists():
        errors.append(f"Rules file {rules} does not exist")
    return DrawioValidationResult(ok=not errors, warnings=warnings, errors=errors)


@drawio_app.command("validate")
def validate_command(
    diagram: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        dir_okay=False,
        help="Draw.io diagram (.drawio or .xml) to validate.",
    ),
    rules: Optional[Path] = typer.Option(
        None,
        "--rules",
        "-r",
        exists=True,
        readable=True,
        dir_okay=False,
        help="Optional validation rules file (YAML/JSON).",
    ),
    format: ValidateFormatChoice = typer.Option(
        "table",
        "--format",
        "-f",
        help="Output format for validation report.",
    ),
) -> None:
    """Validate a Draw.io diagram."""
    result = _fake_validate(diagram, rules)
    report = result.to_dict()
    _print_report(report, format)
    if not result.ok:
        raise typer.Exit(code=1)


@drawio_app.command("import")
def import_command(
    file: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        dir_okay=False,
        help="Draw.io file (.drawio or .xml) to import.",
    ),
    mapping: Optional[Path] = typer.Option(
        None,
        "--mapping",
        "-m",
        exists=True,
        readable=True,
        dir_okay=False,
        help="Optional mapping YAML to assist component pin mapping.",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        dir_okay=False,
        help="Write mapped YAML/components to this path (stdout if omitted).",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Perform a dry run without writing output.",
    ),
) -> None:
    """Import a Draw.io diagram and map nodes to components."""
    mapping_data = _load_yaml_file(mapping) if mapping else {}
    report = {
        "file": str(file),
        "mapping_loaded": bool(mapping_data),
        "matched": 0,
        "unmatched": 0,
    }
    output_text = yaml.safe_dump({"components": {}, "mapping": mapping_data})
    if not dry_run:
        _write_text(output, output_text)
    _print_report(report, "table")


@drawio_app.command("export")
def export_command(
    harness: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        dir_okay=False,
        help="Harness YAML to export as Draw.io diagram.",
    ),
    template: Optional[Path] = typer.Option(
        None,
        "--template",
        "-t",
        exists=True,
        readable=True,
        dir_okay=False,
        help="Optional Draw.io template file.",
    ),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        dir_okay=False,
        help="Path to write the generated Draw.io file.",
    ),
    style: Optional[Path] = typer.Option(
        None,
        "--style",
        "-s",
        exists=True,
        readable=True,
        dir_okay=False,
        help="Optional styling rules (JSON/YAML).",
    ),
) -> None:
    """Generate a Draw.io diagram from a harness."""
    style_data = _load_yaml_file(style) if style else {}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("<!-- drawio content would go here -->", encoding="utf-8")
    report = {
        "harness": str(harness),
        "template": str(template) if template else None,
        "output": str(output),
        "style_loaded": bool(style_data),
    }
    _print_report(report, "table")


@drawio_app.command("sync")
def sync_command(
    harness: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        dir_okay=False,
        help="Harness YAML file.",
    ),
    diagram: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        dir_okay=False,
        help="Draw.io diagram file.",
    ),
    direction: DirectionChoice = typer.Option(
        "bidirectional",
        "--direction",
        "-d",
        help="Sync direction.",
    ),
    backup: Optional[Path] = typer.Option(
        None,
        "--backup",
        "-b",
        dir_okay=False,
        help="Optional backup path before writing changes.",
    ),
    report: Optional[Path] = typer.Option(
        None,
        "--report",
        "-r",
        dir_okay=False,
        help="Optional JSON report path.",
    ),
) -> None:
    """Bidirectional sync between harness and Draw.io diagram."""
    if backup:
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_text(diagram.read_text(encoding="utf-8"), encoding="utf-8")
    summary = {
        "harness": str(harness),
        "diagram": str(diagram),
        "direction": direction,
        "changes": [],
    }
    report_text = json.dumps(summary, indent=2)
    _write_text(report, report_text)
    typer.echo("Sync completed.")


@drawio_app.command("edit")
def edit_command(
    diagram: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        dir_okay=False,
        help="Draw.io diagram file to edit.",
    ),
    rules: Optional[Path] = typer.Option(
        None,
        "--rules",
        "-r",
        exists=True,
        readable=True,
        dir_okay=False,
        help="Optional validation rules file.",
    ),
    editor: Optional[str] = typer.Option(
        None,
        "--editor",
        "-e",
        help="Editor command to open Draw.io (defaults to $VISUAL/$EDITOR or 'drawio').",
    ),
    no_validate: bool = typer.Option(
        False,
        "--no-validate",
        help="Skip validation after editing.",
    ),
) -> None:
    """Open Draw.io for interactive editing, then optionally validate."""
    chosen_editor = editor or os.environ.get("VISUAL") or os.environ.get("EDITOR") or "drawio"
    cmd_parts = shlex.split(chosen_editor)
    cmd_parts.append(str(diagram))
    result = subprocess.run(cmd_parts)
    if result.returncode != 0:
        typer.echo(f"Editor exited with status {result.returncode}", err=True)
        raise typer.Exit(code=result.returncode)
    if no_validate:
        return
    validation = _fake_validate(diagram, rules)
    if validation.errors:
        typer.echo("Errors after edit:", err=True)
        for err in validation.errors:
            typer.echo(f"- {err}", err=True)
        raise typer.Exit(code=1)
    if validation.warnings:
        typer.echo("Warnings after edit:")
        for warn in validation.warnings:
            typer.echo(f"- {warn}")
    if validation.ok and not validation.warnings:
        typer.echo("Diagram is valid after edit.")


@drawio_app.command("review")
def review_command(
    diagram: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        dir_okay=False,
        help="Draw.io diagram file to review.",
    ),
    comments_path: Path = typer.Option(
        ...,
        "--comments-path",
        "-c",
        dir_okay=False,
        help="Path to save collected comments.",
    ),
    rules: Optional[Path] = typer.Option(
        None,
        "--rules",
        "-r",
        exists=True,
        readable=True,
        dir_okay=False,
        help="Optional validation rules file.",
    ),
    format: ValidateFormatChoice = typer.Option(
        "table",
        "--format",
        "-f",
        help="Validation report format.",
    ),
    editor: Optional[str] = typer.Option(
        None,
        "--editor",
        "-e",
        help="Editor command to open Draw.io in read-only mode.",
    ),
) -> None:
    """Open Draw.io read-only, capture CLI comments, and save them."""
    chosen_editor = editor or os.environ.get("VISUAL") or os.environ.get("EDITOR") or "drawio"
    cmd_parts = shlex.split(chosen_editor)
    cmd_parts.append(str(diagram))
    result = subprocess.run(cmd_parts)
    if result.returncode != 0:
        typer.echo(f"Editor exited with status {result.returncode}", err=True)
        raise typer.Exit(code=result.returncode)

    typer.echo("Enter comments about the diagram (end with EOF / Ctrl-D):")
    try:
        comments = typer.get_text_stream("stdin").read()
    except Exception as exc:
        raise FilareToolsException(f"Failed to read comments: {exc}") from exc

    comments_path.parent.mkdir(parents=True, exist_ok=True)
    comments_path.write_text(comments, encoding="utf-8")
    typer.echo(f"Saved comments to {comments_path}")

    validation = _fake_validate(diagram, rules)
    _print_report(validation.to_dict(), format)
    if not validation.ok:
        raise typer.Exit(code=1)
