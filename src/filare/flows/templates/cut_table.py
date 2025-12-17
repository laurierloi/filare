"""Helpers to build Cut Table template models from explicit inputs."""

from __future__ import annotations

from typing import Iterable, Mapping, Sequence, Union

from filare.models.colors import SingleColor
from filare.models.templates.cut_table_template_model import (
    CutTableTemplateModel,
    TemplateCutTableRow,
)


def _coerce_row(
    row: Union[TemplateCutTableRow, Mapping[str, object]]
) -> TemplateCutTableRow:
    """Normalize a row into TemplateCutTableRow."""
    if isinstance(row, TemplateCutTableRow):
        return row
    color_value = row.get("color", "")
    color = (
        color_value
        if isinstance(color_value, SingleColor)
        else SingleColor(inp=str(color_value or ""))
    )
    return TemplateCutTableRow(
        wire=str(row.get("wire", "")),
        partno=str(row.get("partno", "")),
        color=color,
        length=str(row.get("length", "")),
    )


def build_cut_table_model(
    rows: Sequence[Union[TemplateCutTableRow, Mapping[str, object]]]
) -> CutTableTemplateModel:
    """Construct a CutTableTemplateModel from row data."""
    normalized = [_coerce_row(row) for row in rows]
    return CutTableTemplateModel(rows=normalized)
