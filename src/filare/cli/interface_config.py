"""Typer CLI for interface configuration files."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Mapping, Optional

import typer
import yaml

from filare.flows.interface import (
    InterfaceFlowError,
    generate_interface_config,
    load_interface_config,
    save_interface_config_yaml,
)
from filare.models.interface.config import (
    InterfaceConfigCollection,
    InterfaceConfigurationModel,
)
from filare.settings import typer_kwargs

interface_config_app = typer.Typer(
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Load, edit, save, check, and generate interface configuration files.",
    **typer_kwargs(),
)


def _load_yaml_content(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _write_output(content: str, output: Optional[Path], force: bool) -> None:
    if not output:
        typer.echo(content)
        return
    if output.exists() and not force:
        raise InterfaceFlowError(f"{output} exists; use --force to overwrite.")
    output.write_text(content, encoding="utf-8")


def _launch_editor(initial: str) -> str:
    editor = os.environ.get("VISUAL") or os.environ.get("EDITOR")
    if not editor:
        raise InterfaceFlowError("No $EDITOR or $VISUAL set for --editor use.")
    with tempfile.NamedTemporaryFile(suffix=".yml", delete=False) as handle:
        handle.write(initial.encode("utf-8"))
        handle.flush()
        path = Path(handle.name)
    try:
        subprocess.run([editor, str(path)], check=True)
        return path.read_text(encoding="utf-8")
    finally:
        path.unlink(missing_ok=True)


def _apply_set(payload: dict[str, Any], expression: str) -> None:
    if "=" not in expression:
        raise InterfaceFlowError(f"--set requires key=value (got {expression}).")
    path, raw_value = expression.split("=", 1)
    value = yaml.safe_load(raw_value)
    segments = path.replace("[", ".").replace("]", "").split(".")
    target: Any = payload
    for segment in segments[:-1]:
        if segment == "":
            continue
        if segment not in target or not isinstance(target[segment], dict):
            target[segment] = {}
        target = target[segment]
    final_key = segments[-1]
    if final_key == "":
        raise InterfaceFlowError(f"Invalid target path in --set: {expression}")
    target[final_key] = value


def _dump_section(section: Any, format: str) -> str:
    if isinstance(section, InterfaceConfigurationModel):
        payload = section.model_dump(by_alias=True)
    elif isinstance(section, InterfaceConfigCollection):
        payload = section.model_dump(by_alias=True)
    else:
        payload = section
    if format == "json":
        return json.dumps(payload, indent=2)
    return yaml.safe_dump(payload, sort_keys=False)


def _select_section(
    model: InterfaceConfigurationModel,
    key: Optional[str],
    interface_type: Optional[str],
    config_key: Optional[str],
) -> Any:
    if key is None:
        return model
    if key == "global":
        return model.global_config
    if key == "default":
        if interface_type:
            return getattr(model.default, interface_type, {})
        return model.default
    if key == "type":
        if not interface_type:
            raise InterfaceFlowError("--interface-type is required when key=type.")
        type_section = getattr(model.type, interface_type, {})
        if config_key:
            if config_key not in type_section:
                raise InterfaceFlowError(
                    f"Config key '{config_key}' not found under type.{interface_type}."
                )
            return type_section[config_key]
        return type_section
    if key == "item":
        if not interface_type:
            raise InterfaceFlowError("--interface-type is required when key=item.")
        item_section = getattr(model.item, interface_type, {})
        if config_key:
            if config_key not in item_section:
                raise InterfaceFlowError(
                    f"Config key '{config_key}' not found under item.{interface_type}."
                )
            return item_section[config_key]
        return item_section
    raise InterfaceFlowError(f"Unknown key '{key}'. Use global|default|type|item.")


@interface_config_app.command("load")
def load_config_command(
    config_file: Path = typer.Option(
        ...,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Interface configuration YAML to load.",
    ),
    key: Optional[str] = typer.Option(
        None,
        "--key",
        "-k",
        help="Optional section to output: global|default|type|item.",
    ),
    interface_type: Optional[str] = typer.Option(
        None,
        "--interface-type",
        help="Interface type filter when --key is default/type/item.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key when selecting type/item entries.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Load and validate an interface configuration file."""
    content = _load_yaml_content(config_file)
    model = load_interface_config(content)
    section = _select_section(model, key, interface_type, config_key)
    typer.echo(_dump_section(section, format.lower()))


@interface_config_app.command("check")
def check_config_command(
    config_file: Path = typer.Option(
        ...,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Interface configuration YAML to validate.",
    ),
) -> None:
    """Validate an interface configuration file."""
    content = _load_yaml_content(config_file)
    try:
        load_interface_config(content)
    except InterfaceFlowError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)
    typer.echo("Interface configuration is valid.")


@interface_config_app.command("edit")
def edit_config_command(
    config_file: Path = typer.Option(
        ...,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Interface configuration YAML to edit.",
    ),
    set_values: list[str] = typer.Option(
        [],
        "--set",
        help="Set a value using path=value (supports dotted paths).",
    ),
    patch_files: list[Path] = typer.Option(
        [],
        "--patch",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML patch files to shallow-merge into the config.",
    ),
    editor: bool = typer.Option(
        False,
        "--editor",
        help="Open the config in $EDITOR/$VISUAL for editing.",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        dir_okay=False,
        help="Optional output path; defaults to stdout.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite output path if it exists.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Edit an interface configuration file, validate, and emit the result."""
    payload = _load_yaml_content(config_file)
    if not isinstance(payload, Mapping):
        raise InterfaceFlowError("Interface config must be a mapping.")
    payload = dict(payload)
    for patch in patch_files:
        patch_data = _load_yaml_content(patch)
        if isinstance(patch_data, Mapping):
            payload.update(patch_data)
    for expression in set_values:
        _apply_set(payload, expression)
    if editor:
        edited_text = _launch_editor(yaml.safe_dump(payload, sort_keys=False))
        payload = yaml.safe_load(edited_text) or {}
    model = load_interface_config(payload)
    rendered = _dump_section(model, format.lower())
    _write_output(rendered, output, force)


@interface_config_app.command("save")
def save_config_command(
    config_file: Path = typer.Option(
        ...,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Interface configuration YAML to validate and save.",
    ),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        dir_okay=False,
        help="Destination path for the validated config.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite output path if it exists.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Validate and save an interface configuration file."""
    payload = _load_yaml_content(config_file)
    model = load_interface_config(payload)
    if format.lower() == "json":
        rendered = json.dumps(model.model_dump(by_alias=True), indent=2)
    else:
        rendered = save_interface_config_yaml(model)
    _write_output(rendered, output, force)


@interface_config_app.command("generate")
def generate_config_command(
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        dir_okay=False,
        help="Optional output path; defaults to stdout.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite output path if it exists.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Generate an empty interface configuration file."""
    model = generate_interface_config()
    if format.lower() == "json":
        rendered = json.dumps(model.model_dump(by_alias=True), indent=2)
    else:
        rendered = save_interface_config_yaml(model)
    _write_output(rendered, output, force)
