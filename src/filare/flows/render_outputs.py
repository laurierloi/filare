"""Rendering flows that operate on models."""

import logging
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
    logging.debug(
        "Rendering harness outputs for %s to %s (formats=%s)",
        getattr(harness, "name", output_name),
        output_dir,
        list(output_formats),
    )
    harness.output(
        filename=output_dir / output_name, fmt=tuple(output_formats), view=False
    )
