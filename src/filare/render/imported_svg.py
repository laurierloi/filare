# -*- coding: utf-8 -*-

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from filare.models.options import ImportedSVGOptions
from filare.render.assets import embed_svg_images

SVG_DECLARATION_PATTERN = re.compile(
    r"(?mis)^<[?]xml[^>]*>\s*|^<!DOCTYPE[^>]*>\s*", re.MULTILINE
)
SVG_TAG_PATTERN = re.compile(r"<svg(?P<attrs>[^>]*)>", re.IGNORECASE)


def strip_svg_declarations(svg_text: str) -> str:
    """Remove XML/doctype headers so the markup can be embedded safely."""
    return SVG_DECLARATION_PATTERN.sub("", svg_text or "").lstrip()


def _maybe_add_viewbox(attrs: str) -> str:
    """Add a viewBox if width/height are numeric and no viewBox is present."""
    if "viewBox=" in attrs or "viewbox=" in attrs:
        return attrs
    width_match = re.search(r'width="([\d.]+)', attrs)
    height_match = re.search(r'height="([\d.]+)', attrs)
    if not width_match or not height_match:
        return attrs
    try:
        width = float(width_match.group(1))
        height = float(height_match.group(1))
    except ValueError:
        return attrs
    return f'{attrs} viewBox="0 0 {width} {height}"'


def _merge_style_attr(attrs: str, style: str) -> str:
    if not style:
        return attrs
    style_re = re.compile(r'style="([^"]*)"')
    match = style_re.search(attrs)
    if match:
        existing = match.group(1).strip()
        merged = "; ".join([s for s in [existing, style] if s]).strip("; ")
        return style_re.sub(f'style="{merged}"', attrs)
    return f'{attrs} style="{style}"'


def _apply_svg_root_styles(
    svg_text: str, style: str, preserve_aspect_ratio: Optional[bool]
) -> str:
    """Apply sizing/style and preserveAspectRatio overrides to the root <svg>."""
    if not style and preserve_aspect_ratio is None:
        return svg_text

    def repl(match: re.Match) -> str:
        attrs = match.group("attrs") or ""
        attrs = _merge_style_attr(attrs, style)
        attrs = _maybe_add_viewbox(attrs)
        if preserve_aspect_ratio is False:
            if 'preserveAspectRatio="' in attrs:
                attrs = re.sub(
                    r'preserveAspectRatio="[^"]*"', 'preserveAspectRatio="none"', attrs
                )
            else:
                attrs = f'{attrs} preserveAspectRatio="none"'
        return f"<svg{attrs}>"

    return SVG_TAG_PATTERN.sub(repl, svg_text, count=1)


def prepare_imported_svg(spec: ImportedSVGOptions) -> str:
    """Load, inline assets, and normalize style for an imported SVG."""
    svg_path = Path(spec.src)
    svg_text = strip_svg_declarations(svg_path.read_text(encoding="utf-8"))
    if not SVG_TAG_PATTERN.search(svg_text):
        raise ValueError(f"File {svg_path} does not contain a root <svg> element.")
    svg_text = embed_svg_images(svg_text, svg_path.parent)

    style_bits = []
    if spec.width:
        style_bits.append(f"width: {spec.width}")
        style_bits.append(f"max-width: {spec.width}")
    else:
        style_bits.append("max-width: 95%")

    if spec.height:
        style_bits.append(f"height: {spec.height}")
        style_bits.append(f"max-height: {spec.height}")
    else:
        style_bits.append("max-height: 100%")

    style = "; ".join(style_bits)
    preserve_aspect_ratio = None if spec.preserve_aspect_ratio else False

    return _apply_svg_root_styles(svg_text, style, preserve_aspect_ratio)


def build_import_container_style(spec: ImportedSVGOptions) -> str:
    """Compute inline style for the diagram container."""
    justify = {"left": "flex-start", "center": "center", "right": "flex-end"}[
        spec.align
    ]
    styles = [
        "display: flex",
        f"justify-content: {justify}",
        "align-items: flex-start",
        "width: 100%",
        "height: 100%",
    ]
    return "; ".join(styles)


def build_import_inner_style(spec: ImportedSVGOptions) -> str:
    """Inline style for the inner wrapper to offset the SVG."""
    offset_x = spec.offset_x or "0"
    offset_y = spec.offset_y or "0"
    zero_pattern = re.compile(r"^0(?:[a-zA-Z%]+)?$")
    if zero_pattern.match(offset_x) and zero_pattern.match(offset_y):
        return ""
    return f"transform: translate({offset_x}, {offset_y});"
