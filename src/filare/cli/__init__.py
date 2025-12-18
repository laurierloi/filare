"""Filare CLI package powered by Typer."""

# Pre-load submodules to avoid circular imports when initializing the CLI.
import filare.cli.drawio as _drawio  # noqa: F401
import filare.cli.interface as _interface  # noqa: F401
import filare.cli.interface_config as _interface_config  # noqa: F401
import filare.cli.metadata as _metadata  # noqa: F401
import filare.cli.overlap as _overlap  # noqa: F401
import filare.cli.qty as _qty  # noqa: F401
import filare.cli.render as _render  # noqa: F401
import filare.cli.examples as _examples  # noqa: F401
from filare.cli.main import (
    app,
    cli,
    drawio,
    examples,
    interface,
    interface_config,
    metadata,
    overlap,
    qty,
    render_callback,
    settings,
)

__all__ = [
    "app",
    "cli",
    "qty",
    "render_callback",
    "settings",
    "metadata",
    "drawio",
    "examples",
    "interface",
    "interface_config",
    "overlap",
]
