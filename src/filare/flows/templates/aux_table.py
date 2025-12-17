"""Helpers to build auxiliary cut/termination page template models."""

from __future__ import annotations

from typing import Mapping, Optional, Sequence, Union

from filare.flows.templates import build_cut_table_model, build_termination_table_model
from filare.models.colors import SingleColor
from filare.models.metadata import Metadata, PageTemplateConfig, PageTemplateTypes
from filare.models.options import PageOptions
from filare.models.templates.cut_template_model import CutTemplateModel
from filare.models.templates.page_template_model import (
    TemplatePageMetadata,
    TemplatePageOptions,
)
from filare.models.templates.termination_template_model import TerminationTemplateModel
from filare.render.templates import get_template


def _bgcolor_from_options(options: PageOptions) -> SingleColor:
    bg_candidates = [
        getattr(options, "bgcolor", None),
        getattr(options, "bgcolor_node", None),
        getattr(options, "bgcolor_connector", None),
        getattr(options, "bgcolor_cable", None),
        getattr(options, "bgcolor_bundle", None),
    ]
    for candidate in bg_candidates:
        if isinstance(candidate, SingleColor):
            return candidate
    return SingleColor("#FFFFFF")


def build_aux_table_model(
    suffix: str,
    rows: Optional[Sequence[Mapping[str, object]]],
    default_html: str,
    metadata: Metadata,
    options: PageOptions,
    *,
    page_suffix: str = "",
    generator: str = "Filare",
    partno: str = "",
    title: str = "",
    titleblock_html: Optional[str] = None,
) -> Union[CutTemplateModel, TerminationTemplateModel]:
    """Construct a cut/termination TemplateModel for auxiliary pages."""
    page_metadata = (
        metadata.model_copy(update={"sheet_suffix": page_suffix})
        if hasattr(metadata, "model_copy")
        else metadata
    )
    template_metadata = TemplatePageMetadata(
        generator=generator,
        title=title or getattr(page_metadata, "title", "") or suffix.title(),
        template=PageTemplateConfig(name=PageTemplateTypes.simple),
    )
    template_options = TemplatePageOptions(
        fontname=getattr(options, "fontname", "Arial"),
        bgcolor=_bgcolor_from_options(options),
        titleblock_rows=getattr(options, "titleblock_rows", 3),
        titleblock_row_height=getattr(options, "titleblock_row_height", 5.0),
    )
    table_html = default_html
    if rows:
        if suffix == "cut":
            table_html = build_cut_table_model(rows).render()
        else:
            table_html = build_termination_table_model(rows).render()

    if titleblock_html is None:
        titleblock_html = get_template("titleblock.html").render(
            {
                "metadata": page_metadata,
                "options": options,
                "partno": partno,
            }
        )

    if suffix == "cut":
        return CutTemplateModel(
            metadata=template_metadata,
            options=template_options,
            titleblock=titleblock_html,
            cut_table=table_html,
        )
    return TerminationTemplateModel(
        metadata=template_metadata,
        options=template_options,
        titleblock=titleblock_html,
        termination_table=table_html,
    )
