"""Helpers to build BOM template models from explicit inputs."""

from __future__ import annotations

from typing import List, Optional, Sequence

from filare.models.templates.bom_template_model import (
    BomTemplateModel,
    TemplateBomOptions,
    TemplateBomPayload,
)


def build_bom_model(
    headers: Sequence[str],
    columns_class: Sequence[str],
    content: Sequence[Sequence[str]],
    options: Optional[TemplateBomOptions] = None,
    *,
    reverse: Optional[bool] = None,
    bom_row_height: Optional[float] = None,
    bom_updated_position: Optional[str] = None,
    titleblock_rows: Optional[int] = None,
    titleblock_row_height: Optional[float] = None,
) -> BomTemplateModel:
    """Construct a BomTemplateModel from explicit inputs."""
    opts = options or TemplateBomOptions()
    # Override provided fields when supplied.
    if reverse is not None:
        opts.reverse = reverse
    if bom_row_height is not None:
        opts.bom_row_height = bom_row_height
    if bom_updated_position is not None:
        opts.bom_updated_position = bom_updated_position
    if titleblock_rows is not None:
        opts.titleblock_rows = titleblock_rows
    if titleblock_row_height is not None:
        opts.titleblock_row_height = titleblock_row_height

    payload = TemplateBomPayload(
        headers=list(headers),
        columns_class=list(columns_class),
        content=[[str(cell) for cell in row] for row in content],
        options=opts,
    )
    return BomTemplateModel(bom=payload, options=opts)
