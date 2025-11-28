"""Flow helpers for shared BOM generation."""

from pathlib import Path
from typing import Dict, Iterable, Optional, Tuple

from wireviz.render.html import generate_shared_bom


def build_shared_bom(
    output_dir: Path,
    shared_bom: Dict,
    use_qty_multipliers: bool = False,
    files: Optional[Iterable[Path]] = None,
    multiplier_file_name: Optional[str] = None,
):
    """Generate a shared BOM using the rendering helper."""
    return generate_shared_bom(
        output_dir=output_dir,
        shared_bom=shared_bom,
        use_qty_multipliers=use_qty_multipliers,
        files=files,
        multiplier_file_name=multiplier_file_name,
    )
