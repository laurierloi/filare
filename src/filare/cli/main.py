"""Aggregate Typer app that exposes run/qty subcommands."""

from __future__ import annotations

import typer

from . import qty as qty_module
from . import render
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

cli = app
render_callback = render.render_callback
qty = qty_module.qty_app
settings = settings_module.settings_app
