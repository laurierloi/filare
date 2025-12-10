"""Aggregate Typer app that exposes run/qty/settings/metadata subcommands."""

from __future__ import annotations

import typer

import filare.cli.metadata as metadata_module
import filare.cli.qty as qty_module
import filare.cli.render as render
from . import settings as settings_module

app = typer.Typer(
    name="filare",
    add_completion=True,
    no_args_is_help=True,
    help="Filare command-line interface.",
)

app.add_typer(render.run_app, name="run")
app.add_typer(qty_module.qty_app, name="qty")
app.add_typer(settings_module.settings_app, name="settings")
app.add_typer(metadata_module.metadata_app, name="metadata")

cli = app
render_callback = render.render_callback
qty = qty_module.qty_app
settings = settings_module.settings_app
metadata = metadata_module.metadata_app
