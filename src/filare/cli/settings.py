"""Typer-based settings command group."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Literal, Mapping, Optional

import typer
import yaml

from filare.settings import (
    FilareSettingsModel,
    SettingsStore,
    resolve_settings,
    typer_kwargs,
)

settings_app = typer.Typer(
    help="Inspect and manage Filare settings (YAML-backed).",
    context_settings={"help_option_names": ["-h", "--help"]},
    **typer_kwargs(),
)


FormatChoice = Literal["table", "yaml"]
ScopeChoice = Literal["user", "project"]
TypeChoice = Literal["string", "bool", "int", "list"]


def _parse_bool(value: str) -> bool:
    truthy = {"1", "true", "yes", "on", "y"}
    falsy = {"0", "false", "no", "off", "n"}
    lowered = value.strip().lower()
    if lowered in truthy:
        return True
    if lowered in falsy:
        return False
    raise typer.BadParameter(
        "Boolean values must be one of: true/false/yes/no/on/off/1/0."
    )


def _parse_list(value: str) -> List[str]:
    # Split on commas and strip whitespace; ignore empty segments.
    return [segment.strip() for segment in value.split(",") if segment.strip()]


def _parse_value(raw: str, value_type: str) -> object:
    if value_type == "bool":
        return _parse_bool(raw)
    if value_type == "int":
        try:
            return int(raw)
        except ValueError as exc:
            raise typer.BadParameter("Expected an integer for --type int.") from exc
    if value_type == "list":
        return _parse_list(raw)
    return raw


def _format_table(data: Mapping[str, object]) -> str:
    if not data:
        return "No settings set."
    width = max(len(key) for key in data.keys())
    lines = [f"{key.ljust(width)}  {data[key]}" for key in sorted(data.keys())]
    return "\n".join(lines)


@settings_app.command("path")
def path_command(
    scope: Optional[ScopeChoice] = typer.Option(
        None, "--scope", "-s", help="Scope to show (default: both)."
    ),
    create: bool = typer.Option(
        False,
        "--create",
        help="Create config directory/file if missing.",
    ),
) -> None:
    """Show or create the settings file path(s)."""
    store = SettingsStore()
    scopes = [scope] if scope else ("user", "project")
    for item in scopes:
        path = store.path_for_scope(item)
        if create:
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.write_text("", encoding="utf-8")
        typer.echo(f"{item}: {path}")


@settings_app.command("show")
def show_command(
    format: FormatChoice = typer.Option(
        "table",
        "--format",
        "-f",
        help="Output format (table or yaml).",
    ),
    include_defaults: bool = typer.Option(
        False,
        "--include-defaults",
        help="Include settings that are still using default values.",
    ),
) -> None:
    """Display resolved settings."""
    resolved = resolve_settings()
    resolved_data = resolved.model_dump()
    resolved_data = {
        k: str(v) if isinstance(v, Path) else v for k, v in resolved_data.items()
    }
    defaults = FilareSettingsModel().model_dump()
    if not include_defaults:
        resolved_data = {
            key: value
            for key, value in resolved_data.items()
            if defaults.get(key) != value
        }
    if format == "yaml":
        typer.echo(yaml.safe_dump(resolved_data, sort_keys=True))
    else:
        typer.echo(_format_table(resolved_data))


@settings_app.command("set")
def set_command(
    key: str = typer.Argument(..., help="Setting key to update."),
    value: str = typer.Argument(..., help="New value for the setting."),
    scope: ScopeChoice = typer.Option(
        "user",
        "--scope",
        "-s",
        help="Scope to write to.",
    ),
    value_type: TypeChoice = typer.Option(
        "string",
        "--type",
        "-t",
        help="Force type parsing for the value.",
    ),
    append: bool = typer.Option(
        False,
        "--append",
        help="Append to list values (requires --type list).",
    ),
) -> None:
    """Update a setting value in the specified scope."""
    if key == "config_dir":
        raise typer.BadParameter(
            "config_dir is managed by FIL_CONFIG_PATH/XDG and cannot be set via CLI."
        )
    parsed_value = _parse_value(value, value_type)
    store = SettingsStore()
    scope_data = store.load_scope(scope)

    if append:
        if value_type != "list":
            raise typer.BadParameter("--append requires --type list.")
        existing = scope_data.get(key)
        if existing is None:
            scope_data[key] = parsed_value
        elif isinstance(existing, list):
            scope_data[key] = existing + parsed_value  # type: ignore[arg-type]
        else:
            raise typer.BadParameter(
                f"Cannot append to '{key}' because it is not a list in {scope} scope."
            )
    else:
        scope_data[key] = parsed_value

    store.write_scope(scope, scope_data)
    typer.echo(f"Updated {key} in {scope} scope: {scope_data[key]}")


@settings_app.command("reset")
def reset_command(
    key: Optional[str] = typer.Argument(
        None, help="Setting key to reset. Resets all if omitted."
    ),
    scope: ScopeChoice = typer.Option(
        "user",
        "--scope",
        "-s",
        help="Scope to modify.",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Confirm resetting all settings in the scope when no key is provided.",
    ),
) -> None:
    """Reset one or all settings in a scope."""
    store = SettingsStore()
    scope_data = store.load_scope(scope)

    if key:
        if key in scope_data:
            scope_data.pop(key, None)
            store.write_scope(scope, scope_data)
            typer.echo(f"Reset {key} in {scope} scope.")
        else:
            typer.echo(f"No '{key}' found in {scope} scope; nothing to reset.")
        return

    if not yes:
        typer.echo("Use --yes to reset all settings in the chosen scope.", err=True)
        raise typer.Exit(code=1)

    store.write_scope(scope, {})
    typer.echo(f"Reset all settings in {scope} scope.")
