"""Filare CLI package powered by Typer."""

# Pre-load submodules to avoid circular imports when initializing the CLI.
import filare.cli.metadata as _metadata  # noqa: F401
import filare.cli.qty as _qty  # noqa: F401
import filare.cli.render as _render  # noqa: F401

from filare.cli.main import app, cli, metadata, qty, render_callback, settings

__all__ = ["app", "cli", "qty", "render_callback", "settings", "metadata"]
