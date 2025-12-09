"""Higher-level parsing helpers for harness YAML files."""

from pathlib import Path
from typing import Iterable, Sequence

from filare.parser.yaml_loader import parse_concat_merge_files, parse_merge_files


def parse_harness_files(
    component_files: Sequence[Path],
    harness_files: Sequence[Path],
    metadata_files: Sequence[Path],
):
    """Parse component + harness YAML into a merged dict."""
    concatenated_files = list(component_files) + list(harness_files)
    return parse_concat_merge_files(concatenated_files, list(metadata_files))


def parse_metadata_files(metadata_files: Iterable[Path]):
    """Parse metadata-only YAML files."""
    if not metadata_files:
        return {}
    return parse_merge_files(list(metadata_files))
