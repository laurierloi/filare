"""Aggregate Typer app that exposes run/qty/settings/metadata/drawio subcommands."""

from __future__ import annotations

import typer

import filare.cli.drawio as drawio_module
import filare.cli.examples as examples_module
import filare.cli.interface as interface_module
import filare.cli.interface_config as interface_config_module
import filare.cli.metadata as metadata_module
import filare.cli.overlap as overlap_module
import filare.cli.qty as qty_module
import filare.cli.render as render
from filare.settings import typer_kwargs

from . import settings as settings_module

app = typer.Typer(
    name="filare",
    help="Filare command-line interface.",
    **typer_kwargs(),
)

app.add_typer(render.run_app, name="run")
app.add_typer(qty_module.qty_app, name="qty")
app.add_typer(settings_module.settings_app, name="settings")
app.add_typer(metadata_module.metadata_app, name="metadata")
app.add_typer(drawio_module.drawio_app, name="drawio")
app.add_typer(examples_module.examples_app, name="ex")
app.add_typer(overlap_module.overlap_app, name="overlap")
app.add_typer(interface_module.interface_app, name="interface")
app.add_typer(interface_config_module.interface_config_app, name="interface-config")

cli = app
render_callback = render.render_callback
qty = qty_module.qty_app
settings = settings_module.settings_app
metadata = metadata_module.metadata_app
drawio = drawio_module.drawio_app
examples = examples_module.examples_app
overlap = overlap_module.overlap_app
interface = interface_module.interface_app
interface_config = interface_config_module.interface_config_app
