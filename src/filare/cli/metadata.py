"""Typer-based metadata command group (validate/merge/describe/edit)."""

from __future__ import annotations

import json
import os
import shlex
import subprocess
from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple

import typer
import yaml
from pydantic import BaseModel, ValidationError, field_validator

from filare.errors import MetadataValidationError
from filare.parser.yaml_loader import merge_item, parse_merge_files

metadata_app = typer.Typer(
    add_completion=True,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Inspect, validate, merge, describe, and edit Filare metadata files.",
)

FormatChoice = Literal["table", "json", "yaml"]
MergeFormatChoice = Literal["yaml", "json"]


class AuthorLite(BaseModel):
    """Minimal author entry."""

    name: str = ""
    date: Optional[object] = None
    changelog: Optional[str] = None
    role: Optional[str] = None

    model_config = {"extra": "allow"}

    @field_validator("date", mode="before")
    def _coerce_date(cls, value):
        if value is None:
            return None
        if isinstance(value, (str,)):
            return value
        # Accept datetime/date objects produced by YAML loaders.
        if hasattr(value, "isoformat"):
            return value.isoformat()
        return value


class MetadataLite(BaseModel):
    """Lightweight metadata schema for validation purposes."""

    title: Optional[str] = None
    pn: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    template: Dict[str, object] = {}
    authors: Dict[str, AuthorLite] = {}
    revisions: Dict[str, AuthorLite] = {}

    model_config = {"extra": "allow"}

    @field_validator("template", mode="before")
    def _coerce_template(cls, value):
        return value or {}


def _load_yaml_file(path: Path) -> object:
    text = path.read_text(encoding="utf-8")
    data = yaml.safe_load(text)
    return data


def _merge_with_sources(paths: List[Path]) -> Tuple[Dict[str, object], Dict[str, Path]]:
    merged: Dict[str, object] = {}
    sources: Dict[str, Path] = {}
    for path in paths:
        loaded = _load_yaml_file(path) or {}
        if not isinstance(loaded, dict):
            raise MetadataValidationError(
                f"{path} must contain a mapping at the top level."
            )
        for key, value in loaded.items():
            if key in merged:
                merged[key] = merge_item(merged[key], value)
            else:
                merged[key] = value
            sources[key] = path
    return merged, sources


def _load_metadata(paths: List[Path]) -> Dict[str, object]:
    """Merge YAML files using existing merge semantics."""
    merged = parse_merge_files(paths)
    if merged is None:
        merged = {}
    if not isinstance(merged, dict):
        raise MetadataValidationError("Merged metadata must be a mapping.")
    return merged


def _validate_payload(
    payload: object, strict: bool
) -> Tuple[bool, List[str], List[str]]:
    if not isinstance(payload, dict):
        return False, [], ["Metadata must be a mapping at the top level."]

    warnings: List[str] = []
    errors: List[str] = []

    try:
        MetadataLite(**payload)
    except ValidationError as exc:
        errors.append(str(exc))

    if not payload.get("pn"):
        warnings.append("Missing part number (pn).")
    if not payload.get("title"):
        warnings.append("Missing title.")
    if strict and warnings:
        errors.extend(warnings)
        warnings = []

    return not errors, warnings, errors


def _format_table(data: Dict[str, object]) -> str:
    if not data:
        return "No data."
    width = max(len(key) for key in data.keys())
    lines = [f"{key.ljust(width)}  {data[key]}" for key in sorted(data.keys())]
    return "\n".join(lines)


def _describe_payload(payload: Dict[str, object]) -> Dict[str, object]:
    return {
        "title": payload.get("title"),
        "pn": payload.get("pn"),
        "company": payload.get("company"),
        "address": payload.get("address"),
        "authors": list(payload.get("authors", {}).keys()),
        "revisions": list(payload.get("revisions", {}).keys()),
        "template": payload.get("template"),
        "keys": sorted(payload.keys()),
    }


def _print_output(data: Dict[str, object], format: FormatChoice) -> None:
    if format == "json":
        typer.echo(json.dumps(data, indent=2))
    elif format == "yaml":
        typer.echo(yaml.safe_dump(data, sort_keys=True))
    else:
        typer.echo(_format_table(data))


@metadata_app.command("validate")
def validate_command(
    files: List[Path] = typer.Argument(
        ...,
        exists=True,
        readable=True,
        dir_okay=False,
        help="Metadata YAML files to validate (merged in order).",
    ),
    schema: Optional[Path] = typer.Option(
        None,
        "--schema",
        "-s",
        exists=True,
        readable=True,
        dir_okay=False,
        help="Optional schema path (reserved for future use).",
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Treat warnings as errors.",
    ),
    json_report: bool = typer.Option(
        False,
        "--json",
        help="Emit validation report as JSON.",
    ),
) -> None:
    """Validate metadata files."""
    _ = schema  # schema override reserved for future use
    try:
        merged = _load_metadata(files)
    except MetadataValidationError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)
    payload = merged.get("metadata", merged)
    ok, warnings, errors = _validate_payload(payload, strict)

    report = {"ok": ok, "warnings": warnings, "errors": errors}

    if json_report:
        typer.echo(json.dumps(report, indent=2))
    else:
        if errors:
            typer.echo("Errors:", err=True)
            for err in errors:
                typer.echo(f"- {err}", err=True)
        if warnings:
            typer.echo("Warnings:")
            for warn in warnings:
                typer.echo(f"- {warn}")
        if not errors and not warnings:
            typer.echo("Metadata is valid.")

    if not ok:
        raise typer.Exit(code=1)


@metadata_app.command("merge")
def merge_command(
    files: List[Path] = typer.Argument(
        ...,
        exists=True,
        readable=True,
        dir_okay=False,
        help="Metadata YAML files to merge in order.",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        dir_okay=False,
        writable=True,
        help="Write merged metadata to this file.",
    ),
    format: MergeFormatChoice = typer.Option(
        "yaml",
        "--format",
        "-f",
        help="Output format for merged metadata.",
    ),
    show_source: bool = typer.Option(
        False,
        "--show-source",
        help="Annotate top-level keys with their source file.",
    ),
) -> None:
    """Merge metadata files and optionally write to disk."""
    try:
        merged = _load_metadata(files)
    except MetadataValidationError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)
    sources: Dict[str, Path] = {}
    if show_source:
        _, sources = _merge_with_sources(files)
        merged["__source__"] = {k: str(v) for k, v in sources.items()}

    if format == "json":
        output_text = json.dumps(merged, indent=2)
    else:
        output_text = yaml.safe_dump(merged, sort_keys=True)

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(output_text, encoding="utf-8")
        typer.echo(f"Wrote merged metadata to {output}")
    else:
        typer.echo(output_text)


@metadata_app.command("describe")
def describe_command(
    file: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        dir_okay=False,
        help="Metadata YAML file to describe.",
    ),
    format: FormatChoice = typer.Option(
        "table",
        "--format",
        "-f",
        help="Output format.",
    ),
) -> None:
    """Show a summary of key metadata fields."""
    try:
        merged = _load_metadata([file])
    except MetadataValidationError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)
    payload = merged.get("metadata", merged)
    summary = _describe_payload(payload)
    _print_output(summary, format)


@metadata_app.command("edit")
def edit_command(
    file: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        dir_okay=False,
        help="Metadata YAML file to edit.",
    ),
    schema: Optional[Path] = typer.Option(
        None,
        "--schema",
        "-s",
        exists=True,
        readable=True,
        dir_okay=False,
        help="Optional schema path (reserved for future use).",
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Treat warnings as errors when re-validating.",
    ),
    editor: Optional[str] = typer.Option(
        None,
        "--editor",
        "-e",
        help="Editor command to use (overrides $VISUAL/$EDITOR).",
    ),
    no_validate: bool = typer.Option(
        False,
        "--no-validate",
        help="Skip validation after editing.",
    ),
) -> None:
    """Open metadata file in editor, then re-validate."""
    _ = schema  # schema override reserved for future use
    chosen_editor = editor or os.environ.get("VISUAL") or os.environ.get("EDITOR")
    if not chosen_editor:
        chosen_editor = "vi"

    cmd_parts = shlex.split(chosen_editor)
    cmd_parts.append(str(file))

    result = subprocess.run(cmd_parts)
    if result.returncode != 0:
        typer.echo(f"Editor exited with status {result.returncode}", err=True)
        raise typer.Exit(code=result.returncode)

    if no_validate:
        return

    try:
        merged = _load_metadata([file])
    except MetadataValidationError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)
    payload = merged.get("metadata", merged)
    ok, warnings, errors = _validate_payload(payload, strict)

    if errors:
        typer.echo("Errors after edit:", err=True)
        for err in errors:
            typer.echo(f"- {err}", err=True)
    if warnings:
        typer.echo("Warnings after edit:")
        for warn in warnings:
            typer.echo(f"- {warn}")
    if ok and not warnings:
        typer.echo("Metadata is valid after edit.")

    if not ok:
        raise typer.Exit(code=1)
