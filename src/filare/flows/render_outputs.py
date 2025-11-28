"""Rendering flows that operate on models."""

from pathlib import Path
from typing import Iterable

from filare.models.harness import Harness


def render_harness_outputs(
    harness: Harness,
    output_dir: Path,
    output_name: str,
    output_formats: Iterable[str],
) -> None:
    """Render harness outputs using the harness model."""
    harness.output(
        filename=output_dir / output_name, fmt=tuple(output_formats), view=False
    )
