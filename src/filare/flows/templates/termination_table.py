"""Helpers to build Termination Table template models from explicit inputs."""

from __future__ import annotations

from typing import Mapping, Sequence, Union

from filare.models.templates.termination_table_template_model import (
    TemplateTerminationRow,
    TerminationTableTemplateModel,
)


def _coerce_row(
    row: Union[TemplateTerminationRow, Mapping[str, object]]
) -> TemplateTerminationRow:
    if isinstance(row, TemplateTerminationRow):
        return row
    return TemplateTerminationRow(
        source=str(row.get("source", "")),
        target=str(row.get("target", "")),
        source_termination=str(row.get("source_termination", "")),
        target_termination=str(row.get("target_termination", "")),
    )


def build_termination_table_model(
    rows: Sequence[Union[TemplateTerminationRow, Mapping[str, object]]]
) -> TerminationTableTemplateModel:
    """Construct a TerminationTableTemplateModel from row data."""
    normalized = [_coerce_row(row) for row in rows]
    return TerminationTableTemplateModel(rows=normalized)
