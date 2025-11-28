"""Higher-level parsing helpers for harness YAML files."""

from pathlib import Path
from typing import Iterable, Tuple

from filare.parser.yaml_loader import parse_concat_merge_files, parse_merge_files


def parse_harness_files(
    component_files: Tuple[Path, ...],
    harness_files: Tuple[Path, ...],
    metadata_files: Tuple[Path, ...],
):
    """Parse component + harness YAML into a merged dict."""
    return parse_concat_merge_files(component_files + harness_files, metadata_files)


def parse_metadata_files(metadata_files: Iterable[Path]):
    """Parse metadata-only YAML files."""
    if not metadata_files:
        return {}
    return parse_merge_files(tuple(metadata_files))
