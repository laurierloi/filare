"""Typer-based CLI for working with interface models."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Type, TypeVar

import typer
import yaml

from filare.flows.interface import (
    InterfaceFlowError,
    load_connector,
    save_connector_yaml,
)
from filare.flows.interface.cable import load_cable, save_cable_yaml
from filare.flows.interface.connection import load_connection, save_connection_yaml
from filare.flows.interface.harness import load_harness, save_harness_yaml
from filare.flows.interface.metadata import load_metadata, save_metadata_yaml
from filare.flows.interface.options import load_options, save_options_yaml
from filare.models.interface.base import FilareInterfaceModel
from filare.models.interface.cable import (
    CableConfigurationInterfaceModel,
    CableInterfaceModel,
)
from filare.models.interface.connection import (
    ConnectionConfigurationInterfaceModel,
    ConnectionInterfaceModel,
)
from filare.models.interface.connector import (
    ConnectorConfigurationInterfaceModel,
    ConnectorInterfaceModel,
)
from filare.models.interface.harness import (
    HarnessConfigurationInterfaceModel,
    HarnessInterfaceModel,
)
from filare.models.interface.metadata import (
    MetadataConfigurationInterfaceModel,
    MetadataInterfaceModel,
)
from filare.models.interface.options import (
    OptionsConfigurationInterfaceModel,
    OptionsInterfaceModel,
)
from filare.settings import typer_kwargs

interface_app = typer.Typer(
    help="Load, edit, save, check, and generate Filare interface models.",
    context_settings={"help_option_names": ["-h", "--help"]},
    **typer_kwargs(),
)

connector_app = typer.Typer(
    help="Work with connector interface definitions.",
    context_settings={"help_option_names": ["-h", "--help"]},
    **typer_kwargs(),
)

cable_app = typer.Typer(
    help="Work with cable interface definitions.",
    context_settings={"help_option_names": ["-h", "--help"]},
    **typer_kwargs(),
)

connection_app = typer.Typer(
    help="Work with connection interface definitions.",
    context_settings={"help_option_names": ["-h", "--help"]},
    **typer_kwargs(),
)

options_app = typer.Typer(
    help="Work with options interface definitions.",
    context_settings={"help_option_names": ["-h", "--help"]},
    **typer_kwargs(),
)

metadata_app = typer.Typer(
    help="Work with metadata interface definitions.",
    context_settings={"help_option_names": ["-h", "--help"]},
    **typer_kwargs(),
)

harness_app = typer.Typer(
    help="Work with harness interface definitions.",
    context_settings={"help_option_names": ["-h", "--help"]},
    **typer_kwargs(),
)

interface_app.add_typer(connector_app, name="connector")
interface_app.add_typer(cable_app, name="cable")
interface_app.add_typer(connection_app, name="connection")
interface_app.add_typer(options_app, name="options")
interface_app.add_typer(metadata_app, name="metadata")
interface_app.add_typer(harness_app, name="harness")

ConfigModel = TypeVar("ConfigModel", bound=FilareInterfaceModel)


def _load_yaml_content(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _load_yaml_map(path: Path) -> Mapping[str, Any]:
    data = _load_yaml_content(path)
    if not isinstance(data, Mapping):
        raise InterfaceFlowError(f"{path} must contain a mapping.")
    return data


def _load_config(
    config_path: Optional[Path],
    config_key: Optional[str],
    model_cls: Type[ConfigModel],
) -> Optional[ConfigModel]:
    if not config_path:
        return None
    loaded = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    if config_key:
        if not isinstance(loaded, Mapping) or config_key not in loaded:
            raise InterfaceFlowError(
                f"Config key '{config_key}' not found in {config_path}."
            )
        loaded = loaded[config_key]
    return model_cls.model_validate(loaded)


def _dump_connector_model(model: ConnectorInterfaceModel, format: str) -> str:
    if format == "json":
        return model.model_dump_json(indent=2)
    return save_connector_yaml(model)


def _dump_cable_model(model: CableInterfaceModel, format: str) -> str:
    if format == "json":
        return model.model_dump_json(indent=2)
    return save_cable_yaml(model)


def _dump_connection_model(model: ConnectionInterfaceModel, format: str) -> str:
    if format == "json":
        return model.model_dump_json(indent=2)
    return save_connection_yaml(model)


def _dump_options_model(model: OptionsInterfaceModel, format: str) -> str:
    if format == "json":
        return model.model_dump_json(indent=2)
    return save_options_yaml(model)


def _dump_metadata_model(model: MetadataInterfaceModel, format: str) -> str:
    if format == "json":
        return model.model_dump_json(indent=2)
    return save_metadata_yaml(model)


def _dump_harness_model(model: HarnessInterfaceModel, format: str) -> str:
    if format == "json":
        return model.model_dump_json(indent=2)
    return save_harness_yaml(model)


def _write_output(content: str, output: Optional[Path], force: bool) -> None:
    if not output:
        typer.echo(content)
        return
    if output.exists() and not force:
        raise InterfaceFlowError(f"{output} exists; use --force to overwrite.")
    output.write_text(content, encoding="utf-8")


def _apply_set(payload: Dict[str, Any], expression: str) -> None:
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


def _merge_maps(paths: List[Path]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    for path in paths:
        fragment = _load_yaml_map(path)
        merged.update(fragment)
    return merged


def _load_connector_models_from_files(
    files: List[Path],
) -> Optional[Dict[str, ConnectorInterfaceModel]]:
    if not files:
        return None
    merged = _merge_maps(files)
    models: Dict[str, ConnectorInterfaceModel] = {}
    for key in merged:
        models[key] = load_connector(merged, key)
    return models


def _load_cable_models_from_files(
    files: List[Path],
) -> Optional[Dict[str, CableInterfaceModel]]:
    if not files:
        return None
    merged = _merge_maps(files)
    models: Dict[str, CableInterfaceModel] = {}
    for key in merged:
        models[key] = load_cable(merged, key)
    return models


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


@connector_app.command("load")
def load_connector_command(
    interfaces_file: Path = typer.Option(
        ...,
        "--interfaces-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of connectors.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Connector key to load."),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional connector configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Load and validate a connector entry, emitting normalized output."""
    connectors = _load_yaml_map(interfaces_file)
    config_obj = _load_config(config, config_key, ConnectorConfigurationInterfaceModel)
    model = load_connector(connectors, key, config=config_obj)
    typer.echo(_dump_connector_model(model, format.lower()))


@connector_app.command("check")
def check_connector_command(
    interfaces_file: Path = typer.Option(
        ...,
        "--interfaces-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of connectors.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Connector key to check."),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional connector configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
) -> None:
    """Validate a connector entry without writing output."""
    connectors = _load_yaml_map(interfaces_file)
    config_obj = _load_config(config, config_key, ConnectorConfigurationInterfaceModel)
    try:
        load_connector(connectors, key, config=config_obj)
    except InterfaceFlowError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)
    typer.echo(f"Connector '{key}' is valid.")


@connector_app.command("edit")
def edit_connector_command(
    interfaces_file: Path = typer.Option(
        ...,
        "--interfaces-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of connectors.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Connector key to edit."),
    set_values: List[str] = typer.Option(
        [],
        "--set",
        help="Set a value using path=value (e.g., pinlabels[0]=A).",
    ),
    patch_files: List[Path] = typer.Option(
        [],
        "--patch",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML patch files to shallow-merge into the connector payload.",
    ),
    editor: bool = typer.Option(
        False,
        "--editor",
        help="Open the connector payload in $EDITOR/$VISUAL for editing.",
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
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional connector configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Edit a connector entry, validate it, and emit the result."""
    connectors = dict(_load_yaml_map(interfaces_file))
    if key not in connectors:
        raise InterfaceFlowError(f"Connector '{key}' not found.")
    payload = connectors[key] or {}
    if not isinstance(payload, dict):
        raise InterfaceFlowError(f"Connector '{key}' must be a mapping.")
    for patch in patch_files:
        patch_data = yaml.safe_load(patch.read_text(encoding="utf-8")) or {}
        if isinstance(patch_data, dict):
            payload.update(patch_data)
    for expression in set_values:
        _apply_set(payload, expression)
    if editor:
        edited_text = _launch_editor(yaml.safe_dump(payload, sort_keys=False))
        payload = yaml.safe_load(edited_text) or {}
    connectors[key] = payload
    config_obj = _load_config(config, config_key, ConnectorConfigurationInterfaceModel)
    model = load_connector(connectors, key, config=config_obj)
    rendered = _dump_connector_model(model, format.lower())
    _write_output(rendered, output, force)


@connector_app.command("save")
def save_connector_command(
    interfaces_file: Path = typer.Option(
        ...,
        "--interfaces-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of connectors.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Connector key to save."),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        dir_okay=False,
        help="Destination path for the validated connector YAML/JSON.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite output path if it exists.",
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional connector configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Validate and save a connector entry to a file."""
    connectors = _load_yaml_map(interfaces_file)
    config_obj = _load_config(config, config_key, ConnectorConfigurationInterfaceModel)
    model = load_connector(connectors, key, config=config_obj)
    rendered = _dump_connector_model(model, format.lower())
    _write_output(rendered, output, force)


@connector_app.command("generate")
def generate_connector_command(
    count: int = typer.Option(
        1,
        "--count",
        "-n",
        min=1,
        help="Number of connector entries to generate.",
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
    """Generate sample connector entries using the fake factory."""
    from filare.models.interface.factories import FakeConnectorInterfaceFactory

    entries: Dict[str, Dict[str, Any]] = {}
    for _ in range(count):
        model: ConnectorInterfaceModel = FakeConnectorInterfaceFactory.build()
        entries[model.designator] = model.model_dump()
    if format.lower() == "json":
        rendered = json.dumps(entries, indent=2)
    else:
        rendered = yaml.safe_dump(entries, sort_keys=False)
    _write_output(rendered, output, force)


@cable_app.command("load")
def load_cable_command(
    interfaces_file: Path = typer.Option(
        ...,
        "--interfaces-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of cables.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Cable key to load."),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional cable configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Load and validate a cable entry, emitting normalized output."""
    cables = _load_yaml_map(interfaces_file)
    config_obj = _load_config(config, config_key, CableConfigurationInterfaceModel)
    model = load_cable(cables, key, config=config_obj)
    typer.echo(_dump_cable_model(model, format.lower()))


@cable_app.command("check")
def check_cable_command(
    interfaces_file: Path = typer.Option(
        ...,
        "--interfaces-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of cables.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Cable key to check."),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional cable configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
) -> None:
    """Validate a cable entry without writing output."""
    cables = _load_yaml_map(interfaces_file)
    config_obj = _load_config(config, config_key, CableConfigurationInterfaceModel)
    try:
        load_cable(cables, key, config=config_obj)
    except InterfaceFlowError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)
    typer.echo(f"Cable '{key}' is valid.")


@cable_app.command("edit")
def edit_cable_command(
    interfaces_file: Path = typer.Option(
        ...,
        "--interfaces-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of cables.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Cable key to edit."),
    set_values: List[str] = typer.Option(
        [],
        "--set",
        help="Set a value using path=value.",
    ),
    patch_files: List[Path] = typer.Option(
        [],
        "--patch",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML patch files to shallow-merge into the cable payload.",
    ),
    editor: bool = typer.Option(
        False,
        "--editor",
        help="Open the cable payload in $EDITOR/$VISUAL for editing.",
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
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional cable configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Edit a cable entry, validate it, and emit the result."""
    cables = dict(_load_yaml_map(interfaces_file))
    if key not in cables:
        raise InterfaceFlowError(f"Cable '{key}' not found.")
    payload = cables[key] or {}
    if not isinstance(payload, dict):
        raise InterfaceFlowError(f"Cable '{key}' must be a mapping.")
    for patch in patch_files:
        patch_data = yaml.safe_load(patch.read_text(encoding="utf-8")) or {}
        if isinstance(patch_data, dict):
            payload.update(patch_data)
    for expression in set_values:
        _apply_set(payload, expression)
    if editor:
        edited_text = _launch_editor(yaml.safe_dump(payload, sort_keys=False))
        payload = yaml.safe_load(edited_text) or {}
    cables[key] = payload
    config_obj = _load_config(config, config_key, CableConfigurationInterfaceModel)
    model = load_cable(cables, key, config=config_obj)
    rendered = _dump_cable_model(model, format.lower())
    _write_output(rendered, output, force)


@cable_app.command("save")
def save_cable_command(
    interfaces_file: Path = typer.Option(
        ...,
        "--interfaces-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of cables.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Cable key to save."),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        dir_okay=False,
        help="Destination path for the validated cable YAML/JSON.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite output path if it exists.",
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional cable configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Validate and save a cable entry to a file."""
    cables = _load_yaml_map(interfaces_file)
    config_obj = _load_config(config, config_key, CableConfigurationInterfaceModel)
    model = load_cable(cables, key, config=config_obj)
    rendered = _dump_cable_model(model, format.lower())
    _write_output(rendered, output, force)


@cable_app.command("generate")
def generate_cable_command(
    count: int = typer.Option(
        1,
        "--count",
        "-n",
        min=1,
        help="Number of cable entries to generate.",
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
    """Generate sample cable entries using the fake factory."""
    from filare.models.interface.factories import FakeCableInterfaceFactory

    entries: Dict[str, Dict[str, Any]] = {}
    for _ in range(count):
        model: CableInterfaceModel = FakeCableInterfaceFactory.build()
        entries[model.designator] = model.model_dump()
    if format.lower() == "json":
        rendered = json.dumps(entries, indent=2)
    else:
        rendered = yaml.safe_dump(entries, sort_keys=False)
    _write_output(rendered, output, force)


@options_app.command("load")
def load_options_command(
    options_file: Path = typer.Option(
        ...,
        "--options-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of options entries.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Options key to load."),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional options configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Load and validate an options entry, emitting normalized output."""
    options_map = _load_yaml_map(options_file)
    config_obj = _load_config(config, config_key, OptionsConfigurationInterfaceModel)
    model = load_options(options_map, key, config=config_obj)
    typer.echo(_dump_options_model(model, format.lower()))


@options_app.command("check")
def check_options_command(
    options_file: Path = typer.Option(
        ...,
        "--options-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of options entries.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Options key to check."),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional options configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
) -> None:
    """Validate an options entry without writing output."""
    options_map = _load_yaml_map(options_file)
    config_obj = _load_config(config, config_key, OptionsConfigurationInterfaceModel)
    try:
        load_options(options_map, key, config=config_obj)
    except InterfaceFlowError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)
    typer.echo(f"Options '{key}' is valid.")


@options_app.command("edit")
def edit_options_command(
    options_file: Path = typer.Option(
        ...,
        "--options-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of options entries.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Options key to edit."),
    set_values: List[str] = typer.Option(
        [],
        "--set",
        help="Set a value using path=value.",
    ),
    patch_files: List[Path] = typer.Option(
        [],
        "--patch",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML patch files to shallow-merge into the options payload.",
    ),
    editor: bool = typer.Option(
        False,
        "--editor",
        help="Open the options payload in $EDITOR/$VISUAL for editing.",
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
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional options configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Edit an options entry, validate it, and emit the result."""
    options_map = dict(_load_yaml_map(options_file))
    if key not in options_map:
        raise InterfaceFlowError(f"Options '{key}' not found.")
    payload = options_map[key] or {}
    if not isinstance(payload, dict):
        raise InterfaceFlowError(f"Options '{key}' must be a mapping.")
    for patch in patch_files:
        patch_data = yaml.safe_load(patch.read_text(encoding="utf-8")) or {}
        if isinstance(patch_data, dict):
            payload.update(patch_data)
    for expression in set_values:
        _apply_set(payload, expression)
    if editor:
        edited_text = _launch_editor(yaml.safe_dump(payload, sort_keys=False))
        payload = yaml.safe_load(edited_text) or {}
    options_map[key] = payload
    config_obj = _load_config(config, config_key, OptionsConfigurationInterfaceModel)
    model = load_options(options_map, key, config=config_obj)
    rendered = _dump_options_model(model, format.lower())
    _write_output(rendered, output, force)


@options_app.command("save")
def save_options_command(
    options_file: Path = typer.Option(
        ...,
        "--options-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of options entries.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Options key to save."),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        dir_okay=False,
        help="Destination path for the validated options YAML/JSON.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite output path if it exists.",
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional options configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Validate and save an options entry to a file."""
    options_map = _load_yaml_map(options_file)
    config_obj = _load_config(config, config_key, OptionsConfigurationInterfaceModel)
    model = load_options(options_map, key, config=config_obj)
    if format.lower() == "json":
        rendered = model.model_dump_json(indent=2)
    else:
        rendered = _dump_options_model(model, format.lower())
    _write_output(rendered, output, force)


@options_app.command("generate")
def generate_options_command(
    count: int = typer.Option(
        1,
        "--count",
        "-n",
        min=1,
        help="Number of options entries to generate.",
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
    """Generate sample options entries using the fake factory."""
    from filare.models.interface.factories import FakeOptionsInterfaceFactory

    entries: Dict[str, Dict[str, Any]] = {}
    for idx in range(count):
        model: OptionsInterfaceModel = FakeOptionsInterfaceFactory.build()
        entries[f"options_{idx}"] = model.model_dump()
    if format.lower() == "json":
        rendered = json.dumps(entries, indent=2)
    else:
        rendered = yaml.safe_dump(entries, sort_keys=False)
    _write_output(rendered, output, force)


@metadata_app.command("load")
def load_metadata_command(
    metadata_file: Path = typer.Option(
        ...,
        "--metadata-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of metadata entries.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Metadata key to load."),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional metadata configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Load and validate a metadata entry, emitting normalized output."""
    metadata_map = _load_yaml_map(metadata_file)
    config_obj = _load_config(config, config_key, MetadataConfigurationInterfaceModel)
    model = load_metadata(metadata_map, key, config=config_obj)
    typer.echo(_dump_metadata_model(model, format.lower()))


@metadata_app.command("check")
def check_metadata_command(
    metadata_file: Path = typer.Option(
        ...,
        "--metadata-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of metadata entries.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Metadata key to check."),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional metadata configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
) -> None:
    """Validate a metadata entry without writing output."""
    metadata_map = _load_yaml_map(metadata_file)
    config_obj = _load_config(config, config_key, MetadataConfigurationInterfaceModel)
    try:
        load_metadata(metadata_map, key, config=config_obj)
    except InterfaceFlowError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)
    typer.echo(f"Metadata '{key}' is valid.")


@metadata_app.command("edit")
def edit_metadata_command(
    metadata_file: Path = typer.Option(
        ...,
        "--metadata-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of metadata entries.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Metadata key to edit."),
    set_values: List[str] = typer.Option(
        [],
        "--set",
        help="Set a value using path=value.",
    ),
    patch_files: List[Path] = typer.Option(
        [],
        "--patch",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML patch files to shallow-merge into the metadata payload.",
    ),
    editor: bool = typer.Option(
        False,
        "--editor",
        help="Open the metadata payload in $EDITOR/$VISUAL for editing.",
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
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional metadata configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Edit a metadata entry, validate it, and emit the result."""
    metadata_map = dict(_load_yaml_map(metadata_file))
    if key not in metadata_map:
        raise InterfaceFlowError(f"Metadata '{key}' not found.")
    payload = metadata_map[key] or {}
    if not isinstance(payload, dict):
        raise InterfaceFlowError(f"Metadata '{key}' must be a mapping.")
    for patch in patch_files:
        patch_data = yaml.safe_load(patch.read_text(encoding="utf-8")) or {}
        if isinstance(patch_data, dict):
            payload.update(patch_data)
    for expression in set_values:
        _apply_set(payload, expression)
    if editor:
        edited_text = _launch_editor(yaml.safe_dump(payload, sort_keys=False))
        payload = yaml.safe_load(edited_text) or {}
    metadata_map[key] = payload
    config_obj = _load_config(config, config_key, MetadataConfigurationInterfaceModel)
    model = load_metadata(metadata_map, key, config=config_obj)
    rendered = _dump_metadata_model(model, format.lower())
    _write_output(rendered, output, force)


@metadata_app.command("save")
def save_metadata_command(
    metadata_file: Path = typer.Option(
        ...,
        "--metadata-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of metadata entries.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Metadata key to save."),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        dir_okay=False,
        help="Destination path for the validated metadata YAML/JSON.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite output path if it exists.",
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional metadata configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Validate and save a metadata entry to a file."""
    metadata_map = _load_yaml_map(metadata_file)
    config_obj = _load_config(config, config_key, MetadataConfigurationInterfaceModel)
    model = load_metadata(metadata_map, key, config=config_obj)
    rendered = _dump_metadata_model(model, format.lower())
    _write_output(rendered, output, force)


@metadata_app.command("generate")
def generate_metadata_command(
    count: int = typer.Option(
        1,
        "--count",
        "-n",
        min=1,
        help="Number of metadata entries to generate.",
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
    """Generate sample metadata entries using the fake factory."""
    from filare.models.interface.factories import FakeMetadataInterfaceFactory

    entries: Dict[str, Dict[str, Any]] = {}
    for idx in range(count):
        model: MetadataInterfaceModel = FakeMetadataInterfaceFactory.build()
        entries[f"metadata_{idx}"] = model.model_dump()
    if format.lower() == "json":
        rendered = json.dumps(entries, indent=2)
    else:
        rendered = yaml.safe_dump(entries, sort_keys=False)
    _write_output(rendered, output, force)


@harness_app.command("load")
def load_harness_command(
    harness_file: Path = typer.Option(
        ...,
        "--harness-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of harness entries.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Harness key to load."),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional harness configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Load and validate a harness entry, emitting normalized output."""
    harness_map = _load_yaml_map(harness_file)
    config_obj = _load_config(config, config_key, HarnessConfigurationInterfaceModel)
    model = load_harness(harness_map, key, config=config_obj)
    typer.echo(_dump_harness_model(model, format.lower()))


@harness_app.command("check")
def check_harness_command(
    harness_file: Path = typer.Option(
        ...,
        "--harness-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of harness entries.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Harness key to check."),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional harness configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
) -> None:
    """Validate a harness entry without writing output."""
    harness_map = _load_yaml_map(harness_file)
    config_obj = _load_config(config, config_key, HarnessConfigurationInterfaceModel)
    try:
        load_harness(harness_map, key, config=config_obj)
    except InterfaceFlowError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)
    typer.echo(f"Harness '{key}' is valid.")


@harness_app.command("edit")
def edit_harness_command(
    harness_file: Path = typer.Option(
        ...,
        "--harness-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of harness entries.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Harness key to edit."),
    set_values: List[str] = typer.Option(
        [],
        "--set",
        help="Set a value using path=value.",
    ),
    patch_files: List[Path] = typer.Option(
        [],
        "--patch",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML patch files to shallow-merge into the harness payload.",
    ),
    editor: bool = typer.Option(
        False,
        "--editor",
        help="Open the harness payload in $EDITOR/$VISUAL for editing.",
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
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional harness configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Edit a harness entry, validate it, and emit the result."""
    harness_map = dict(_load_yaml_map(harness_file))
    if key not in harness_map:
        raise InterfaceFlowError(f"Harness '{key}' not found.")
    payload = harness_map[key] or {}
    if not isinstance(payload, dict):
        raise InterfaceFlowError(f"Harness '{key}' must be a mapping.")
    for patch in patch_files:
        patch_data = yaml.safe_load(patch.read_text(encoding="utf-8")) or {}
        if isinstance(patch_data, dict):
            payload.update(patch_data)
    for expression in set_values:
        _apply_set(payload, expression)
    if editor:
        edited_text = _launch_editor(yaml.safe_dump(payload, sort_keys=False))
        payload = yaml.safe_load(edited_text) or {}
    harness_map[key] = payload
    config_obj = _load_config(config, config_key, HarnessConfigurationInterfaceModel)
    model = load_harness(harness_map, key, config=config_obj)
    rendered = _dump_harness_model(model, format.lower())
    _write_output(rendered, output, force)


@harness_app.command("save")
def save_harness_command(
    harness_file: Path = typer.Option(
        ...,
        "--harness-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping of harness entries.",
    ),
    key: str = typer.Option(..., "--key", "-k", help="Harness key to save."),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        dir_okay=False,
        help="Destination path for the validated harness YAML/JSON.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite output path if it exists.",
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional harness configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Validate and save a harness entry to a file."""
    harness_map = _load_yaml_map(harness_file)
    config_obj = _load_config(config, config_key, HarnessConfigurationInterfaceModel)
    model = load_harness(harness_map, key, config=config_obj)
    rendered = _dump_harness_model(model, format.lower())
    _write_output(rendered, output, force)


@harness_app.command("generate")
def generate_harness_command(
    count: int = typer.Option(
        1,
        "--count",
        "-n",
        min=1,
        help="Number of harness entries to generate.",
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
    """Generate sample harness entries using the fake factory."""
    from filare.models.interface.factories import FakeHarnessInterfaceFactory

    entries: Dict[str, Dict[str, Any]] = {}
    for idx in range(count):
        model: HarnessInterfaceModel = FakeHarnessInterfaceFactory.build()
        entries[f"harness_{idx}"] = model.model_dump()
    if format.lower() == "json":
        rendered = json.dumps(entries, indent=2)
    else:
        rendered = yaml.safe_dump(entries, sort_keys=False)
    _write_output(rendered, output, force)


@connection_app.command("load")
def load_connection_command(
    connections_file: Path = typer.Option(
        ...,
        "--connections-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping or list of connections.",
    ),
    key: str = typer.Option(
        ..., "--key", "-k", help="Connection key or index to load."
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional connection configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    connectors_file: List[Path] = typer.Option(
        [],
        "--connectors-file",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Connector YAML files used as context (can be repeated).",
    ),
    cables_file: List[Path] = typer.Option(
        [],
        "--cables-file",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Cable YAML files used as context (can be repeated).",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Load and validate a connection entry, emitting normalized output."""
    connections = _load_yaml_content(connections_file)
    config_obj = _load_config(config, config_key, ConnectionConfigurationInterfaceModel)
    connector_models = _load_connector_models_from_files(connectors_file) or {}
    cable_models = _load_cable_models_from_files(cables_file) or {}
    model = load_connection(
        connections,
        key,
        config=config_obj,
        connectors=connector_models,
        cables=cable_models,
    )
    typer.echo(_dump_connection_model(model, format.lower()))


@connection_app.command("check")
def check_connection_command(
    connections_file: Path = typer.Option(
        ...,
        "--connections-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping or list of connections.",
    ),
    key: str = typer.Option(
        ..., "--key", "-k", help="Connection key or index to check."
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional connection configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    connectors_file: List[Path] = typer.Option(
        [],
        "--connectors-file",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Connector YAML files used as context (can be repeated).",
    ),
    cables_file: List[Path] = typer.Option(
        [],
        "--cables-file",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Cable YAML files used as context (can be repeated).",
    ),
) -> None:
    """Validate a connection entry without writing output."""
    connections = _load_yaml_content(connections_file)
    config_obj = _load_config(config, config_key, ConnectionConfigurationInterfaceModel)
    connector_models = _load_connector_models_from_files(connectors_file) or {}
    cable_models = _load_cable_models_from_files(cables_file) or {}
    try:
        load_connection(
            connections,
            key,
            config=config_obj,
            connectors=connector_models,
            cables=cable_models,
        )
    except InterfaceFlowError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)
    typer.echo(f"Connection '{key}' is valid.")


@connection_app.command("edit")
def edit_connection_command(
    connections_file: Path = typer.Option(
        ...,
        "--connections-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping or list of connections.",
    ),
    key: str = typer.Option(
        ..., "--key", "-k", help="Connection key or index to edit."
    ),
    set_values: List[str] = typer.Option(
        [],
        "--set",
        help="Set a value using path=value.",
    ),
    patch_files: List[Path] = typer.Option(
        [],
        "--patch",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML patch files to shallow-merge into the connection payload.",
    ),
    editor: bool = typer.Option(
        False,
        "--editor",
        help="Open the connection payload in $EDITOR/$VISUAL for editing.",
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
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional connection configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    connectors_file: List[Path] = typer.Option(
        [],
        "--connectors-file",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Connector YAML files used as context (can be repeated).",
    ),
    cables_file: List[Path] = typer.Option(
        [],
        "--cables-file",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Cable YAML files used as context (can be repeated).",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Edit a connection entry, validate it, and emit the result."""
    connections = _load_yaml_content(connections_file)
    resolved_payload: Any
    if isinstance(connections, Mapping):
        if key not in connections:
            raise InterfaceFlowError(f"Connection '{key}' not found.")
        resolved_payload = connections[key] or {}
        if not isinstance(resolved_payload, dict):
            raise InterfaceFlowError(f"Connection '{key}' must be a mapping.")
        connections = dict(connections)
    elif isinstance(connections, list):
        try:
            index = int(key)
        except ValueError as exc:
            raise InterfaceFlowError(
                f"Connection key '{key}' is not a valid index."
            ) from exc
        if index < 0 or index >= len(connections):
            raise InterfaceFlowError(f"Connection index {index} out of range.")
        resolved_payload = connections[index] or {}
        if not isinstance(resolved_payload, dict):
            raise InterfaceFlowError(f"Connection '{key}' must be a mapping.")
    else:
        raise InterfaceFlowError("Connections input must be a mapping or list.")
    for patch in patch_files:
        patch_data = yaml.safe_load(patch.read_text(encoding="utf-8")) or {}
        if isinstance(patch_data, dict):
            resolved_payload.update(patch_data)
    for expression in set_values:
        _apply_set(resolved_payload, expression)
    if editor:
        edited_text = _launch_editor(yaml.safe_dump(resolved_payload, sort_keys=False))
        resolved_payload = yaml.safe_load(edited_text) or {}
    if isinstance(connections, Mapping):
        connections[key] = resolved_payload
    else:
        connections[int(key)] = resolved_payload
    config_obj = _load_config(config, config_key, ConnectionConfigurationInterfaceModel)
    connector_models = _load_connector_models_from_files(connectors_file) or {}
    cable_models = _load_cable_models_from_files(cables_file) or {}
    model = load_connection(
        connections,
        key,
        config=config_obj,
        connectors=connector_models,
        cables=cable_models,
    )
    rendered = _dump_connection_model(model, format.lower())
    _write_output(rendered, output, force)


@connection_app.command("save")
def save_connection_command(
    connections_file: Path = typer.Option(
        ...,
        "--connections-file",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="YAML file containing a mapping or list of connections.",
    ),
    key: str = typer.Option(
        ..., "--key", "-k", help="Connection key or index to save."
    ),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        dir_okay=False,
        help="Destination path for the validated connection YAML/JSON.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Overwrite output path if it exists.",
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Optional connection configuration YAML.",
    ),
    config_key: Optional[str] = typer.Option(
        None,
        "--config-key",
        help="Optional config key to select a sub-config within --config.",
    ),
    connectors_file: List[Path] = typer.Option(
        [],
        "--connectors-file",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Connector YAML files used as context (can be repeated).",
    ),
    cables_file: List[Path] = typer.Option(
        [],
        "--cables-file",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Cable YAML files used as context (can be repeated).",
    ),
    format: str = typer.Option(
        "yaml",
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format (yaml or json).",
    ),
) -> None:
    """Validate and save a connection entry to a file."""
    connections = _load_yaml_content(connections_file)
    config_obj = _load_config(config, config_key, ConnectionConfigurationInterfaceModel)
    connector_models = _load_connector_models_from_files(connectors_file) or {}
    cable_models = _load_cable_models_from_files(cables_file) or {}
    model = load_connection(
        connections,
        key,
        config=config_obj,
        connectors=connector_models,
        cables=cable_models,
    )
    rendered = _dump_connection_model(model, format.lower())
    _write_output(rendered, output, force)


@connection_app.command("generate")
def generate_connection_command(
    count: int = typer.Option(
        1,
        "--count",
        "-n",
        min=1,
        help="Number of connection entries to generate.",
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
    """Generate sample connection entries using the fake factory."""
    from filare.models.interface.factories import FakeConnectionInterfaceFactory

    entries: Dict[str, Dict[str, Any]] = {}
    for idx in range(count):
        model: ConnectionInterfaceModel = FakeConnectionInterfaceFactory.build()
        entries[str(idx)] = model.model_dump()
    if format.lower() == "json":
        rendered = json.dumps(entries, indent=2)
    else:
        rendered = yaml.safe_dump(entries, sort_keys=False)
    _write_output(rendered, output, force)
