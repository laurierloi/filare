"""Helpers to build IndexTable template models from explicit inputs."""

from __future__ import annotations

from typing import Optional, Sequence, Union

from filare.index_table import IndexTable, IndexTableRow
from filare.models.options import PageOptions
from filare.models.templates.index_table_template_model import (
    IndexTableTemplateModel,
    TemplateIndexTable,
    TemplateIndexTableOptions,
    TemplateIndexTableRow,
)


def _coerce_rows(
    rows: Union[Sequence[IndexTableRow], Sequence[TemplateIndexTableRow]]
) -> Sequence[TemplateIndexTableRow]:
    """Convert index table rows into TemplateIndexTableRow objects."""
    if not rows:
        return []
    if isinstance(rows[0], TemplateIndexTableRow):  # type: ignore[index]
        return rows  # type: ignore[return-value]
    coerced: list[TemplateIndexTableRow] = []
    for row in rows:  # type: ignore[assignment]
        items_html = [str(item) for item in row.get_items(for_pdf=False)]
        items_pdf = [str(item) for item in row.get_items(for_pdf=True)]
        coerced.append(
            TemplateIndexTableRow(items=list(items_html), pdf_items=list(items_pdf))
        )
    return coerced


def build_index_table_model(
    index_table: Union[IndexTable, TemplateIndexTable],
    options: PageOptions,
    *,
    index_table_title: str = "INDEX TABLE",
    index_table_on_right: Optional[bool] = None,
    index_table_updated_position: Optional[str] = None,
    show_bom: Optional[bool] = None,
    bom_rows: Optional[int] = None,
    bom_row_height: Optional[float] = None,
    index_table_row_height: Optional[float] = None,
    for_pdf: Optional[bool] = None,
) -> IndexTableTemplateModel:
    """Construct an IndexTableTemplateModel from the domain IndexTable plus page options."""
    opts = TemplateIndexTableOptions(
        index_table_row_height=(
            index_table_row_height
            if index_table_row_height is not None
            else options.index_table_row_height
        ),
        index_table_on_right=(
            index_table_on_right
            if index_table_on_right is not None
            else options.index_table_on_right
        ),
        index_table_updated_position=(
            index_table_updated_position
            if index_table_updated_position is not None
            else options.index_table_updated_position
        ),
        show_bom=show_bom if show_bom is not None else options.show_bom,
        bom_rows=bom_rows if bom_rows is not None else options.bom_rows,
        bom_row_height=(
            bom_row_height if bom_row_height is not None else options.bom_row_height
        ),
        for_pdf=for_pdf if for_pdf is not None else options.for_pdf,
        index_table_title=index_table_title,
    )

    payload = (
        index_table
        if isinstance(index_table, TemplateIndexTable)
        else TemplateIndexTable(
            header=list(index_table.header),
            rows=list(_coerce_rows(index_table.rows)),
        )
    )

    return IndexTableTemplateModel(index_table=payload, options=opts)
