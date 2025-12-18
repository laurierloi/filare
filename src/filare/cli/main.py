"""Aggregate Typer app that exposes run/qty/settings/metadata/drawio subcommands."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

import filare.cli.drawio as drawio_module
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


@app.callback()
def main_callback(
    ctx: typer.Context,
    document_config: Optional[Path] = typer.Option(
        None,
        "--document-config",
        "-D",
        exists=True,
        readable=True,
        dir_okay=False,
        help="Optional DocumentRepresentation YAML to drive document/page commands.",
    ),
) -> None:
    ctx.obj = ctx.obj or {}
    ctx.obj["document_config"] = document_config


app.add_typer(render.run_app, name="run")
app.add_typer(render.harness_app, name="harness")
app.add_typer(
    render.document_app,
    name="document",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
app.add_typer(
    render.page_app,
    name="page",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
app.add_typer(qty_module.qty_app, name="qty")
app.add_typer(settings_module.settings_app, name="settings")
app.add_typer(metadata_module.metadata_app, name="metadata")
app.add_typer(drawio_module.drawio_app, name="drawio")

cli = app
render_callback = render.render_callback
qty = qty_module.qty_app
settings = settings_module.settings_app
metadata = metadata_module.metadata_app
drawio = drawio_module.drawio_app
harness = render.harness_app
document = render.document_app
page = render.page_app
