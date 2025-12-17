"""Shared flow to build page-like template models (titlepage, din, simple)."""

from __future__ import annotations

from typing import Optional, Union

from filare.errors import FilareFlowException
from filare.models.colors import SingleColor
from filare.models.metadata import Metadata, PageTemplateConfig, PageTemplateTypes
from filare.models.options import PageOptions
from filare.models.templates.din_6771_template_model import (
    Din6771TemplateModel,
    TemplateDin6771Options,
)
from filare.models.templates.page_template_model import (
    PageTemplateModel,
    TemplatePageMetadata,
    TemplatePageOptions,
)
from filare.models.templates.titlepage_template_model import (
    TemplateTitlePageOptions,
    TitlePageTemplateModel,
)


def _page_opts_to_template(opts: PageOptions) -> TemplatePageOptions:
    return TemplatePageOptions(
        fontname=getattr(opts, "fontname", "Arial"),
        bgcolor=getattr(opts, "bgcolor", SingleColor("#FFFFFF")),
        titleblock_rows=getattr(opts, "titleblock_rows", 3),
        titleblock_row_height=getattr(opts, "titleblock_row_height", 5.0),
    )


def _metadata_to_template(
    meta: Metadata, generator: str, title: Optional[str]
) -> TemplatePageMetadata:
    return TemplatePageMetadata(
        generator=generator,
        title=title or getattr(meta, "title", "") or getattr(meta, "name", ""),
        template=getattr(
            meta, "template", PageTemplateConfig(name=PageTemplateTypes.simple)
        ),
    )


def _din_options_from_page(opts: PageOptions, bom_rows: int) -> TemplateDin6771Options:
    base = _page_opts_to_template(opts)
    return TemplateDin6771Options(
        fontname=base.fontname,
        bgcolor=base.bgcolor,
        titleblock_rows=base.titleblock_rows,
        titleblock_row_height=base.titleblock_row_height,
        show_notes=getattr(opts, "show_notes", True),
        show_bom=getattr(opts, "show_bom", True),
        bom_rows=bom_rows,
        bom_row_height=getattr(opts, "bom_row_height", 5.0),
    )


def _titlepage_options_from_page(opts: PageOptions) -> TemplateTitlePageOptions:
    base = _page_opts_to_template(opts)
    return TemplateTitlePageOptions(
        fontname=base.fontname,
        bgcolor=base.bgcolor,
        titleblock_rows=base.titleblock_rows,
        titleblock_row_height=base.titleblock_row_height,
        show_notes=getattr(opts, "show_notes", True),
        show_bom=getattr(opts, "show_bom", True),
        show_index_table=getattr(opts, "show_index_table", True),
    )


PageModelType = Union[Din6771TemplateModel, TitlePageTemplateModel, PageTemplateModel]


def build_page_model(
    *,
    template_name: str,
    metadata: Metadata,
    options: PageOptions,
    titleblock_html: str,
    diagram_html: Optional[str],
    diagram_container_class: str,
    diagram_container_style: str,
    notes_html: str,
    bom_html: str,
    index_table_html: str,
    generator: str,
    title: str,
    bom_rows: int,
) -> PageModelType:
    """Build a page TemplateModel based on template name."""
    try:
        template_enum = PageTemplateTypes(template_name)
    except ValueError as exc:
        raise FilareFlowException(
            f"Unsupported page template '{template_name}'"
        ) from exc

    meta = _metadata_to_template(metadata, generator, title)
    if template_enum == PageTemplateTypes.din_6771:
        opts = _din_options_from_page(options, bom_rows)
        return Din6771TemplateModel(
            metadata=meta,
            options=opts,
            title=title or "DIN 6771 Diagram",
            diagram=diagram_html or "",
            notes=notes_html or None,
            bom=bom_html or None,
            diagram_container_class=diagram_container_class,
            diagram_container_style=diagram_container_style,
            titleblock=titleblock_html,
        )
    elif template_enum == PageTemplateTypes.titlepage:
        opts = _titlepage_options_from_page(options)
        return TitlePageTemplateModel(
            metadata=meta,
            options=opts,
            notes=notes_html or None,
            bom=bom_html or None,
            index_table=index_table_html or None,
            titleblock=titleblock_html,
        )
    if template_enum == PageTemplateTypes.simple:
        opts = _page_opts_to_template(options)
        return PageTemplateModel(
            metadata=meta,
            options=opts,
            titleblock=titleblock_html,
        )
    raise FilareFlowException(
        f"Page template '{template_enum.value}' is not handled in build_page_model"
    )
