# -*- coding: utf-8 -*-
"""
Shim module for rendering helpers.

Functions are implemented in:
- render.assets: embed_svg_images, embed_svg_images_file, get_mime_subtype
- render.pdf: generate_pdf_output
- render.html: generate_html_output, generate_shared_bom, generate_titlepage
"""

from wireviz.render.assets import embed_svg_images, embed_svg_images_file, get_mime_subtype
from wireviz.render.html import (
    generate_html_output,
    generate_shared_bom,
    generate_titlepage,
)
from wireviz.render.pdf import generate_pdf_output

__all__ = [
    "embed_svg_images",
    "embed_svg_images_file",
    "get_mime_subtype",
    "generate_html_output",
    "generate_shared_bom",
    "generate_titlepage",
    "generate_pdf_output",
]
