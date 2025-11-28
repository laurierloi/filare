"""Flow helpers for titlepage and index page generation."""

from pathlib import Path
from typing import Dict, Iterable

from filare.parser import parse_metadata_files
from filare.render.html import generate_titlepage
from filare.render.pdf import generate_pdf_output


def build_titlepage(metadata_files: Iterable[Path], extra_metadata: Dict, shared_bom: Dict, for_pdf: bool = False):
    """Generate a titlepage (and optionally PDF variant) from metadata and shared BOM."""
    yaml_data = parse_metadata_files(tuple(metadata_files))
    generate_titlepage(yaml_data, extra_metadata, shared_bom, for_pdf=for_pdf)


def build_pdf_bundle(html_paths):
    """Generate a consolidated PDF from a list of HTML paths."""
    generate_pdf_output(html_paths)
