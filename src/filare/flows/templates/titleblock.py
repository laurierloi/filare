"""Helpers to build Titleblock template models from metadata/options."""

from __future__ import annotations

from typing import Any, Iterable, List, Optional

from filare.models.metadata import Metadata
from filare.models.options import PageOptions
from filare.models.templates.titleblock_template_model import (
    TemplateAuthorEntry,
    TemplateRevisionEntry,
    TemplateTitleblockMetadata,
    TemplateTitleblockOptions,
    TitleblockTemplateModel,
)


def _coerce_authors(source: Any) -> List[TemplateAuthorEntry]:
    if not source:
        return []
    authors: List[TemplateAuthorEntry] = []
    for entry in source:
        if isinstance(entry, TemplateAuthorEntry):
            authors.append(entry)
        elif isinstance(entry, dict):
            authors.append(TemplateAuthorEntry(**entry))
    return authors


def _coerce_revisions(source: Any) -> List[TemplateRevisionEntry]:
    if not source:
        return []
    revisions: List[TemplateRevisionEntry] = []
    for entry in source:
        if isinstance(entry, TemplateRevisionEntry):
            revisions.append(entry)
        elif isinstance(entry, dict):
            revisions.append(TemplateRevisionEntry(**entry))
    return revisions


def build_titleblock_model(
    metadata: Metadata,
    options: PageOptions,
    partno: str,
) -> TitleblockTemplateModel:
    """Construct a TitleblockTemplateModel from core metadata and page options."""
    tb_metadata = TemplateTitleblockMetadata(
        company=getattr(metadata, "company", "") or getattr(metadata, "name", ""),
        address=getattr(metadata, "address", ""),
        title=getattr(metadata, "title", "") or getattr(metadata, "name", ""),
        name=getattr(metadata, "name", None),
        logo=getattr(metadata, "logo", None),
        revision=getattr(metadata, "revision", "")
        or getattr(metadata, "rev", "")
        or "",
        git_status=getattr(metadata, "git_status", "clean"),
        sheet_current=getattr(metadata, "sheet_current", 1),
        sheet_total=getattr(metadata, "sheet_total", 1),
        sheet_suffix=getattr(metadata, "sheet_suffix", ""),
        authors_list=_coerce_authors(getattr(metadata, "authors_list", [])),
        revisions_list=_coerce_revisions(getattr(metadata, "revisions_list", [])),
    )
    tb_options = TemplateTitleblockOptions(
        titleblock_row_height=getattr(options, "titleblock_row_height", 5.0)
    )
    return TitleblockTemplateModel(
        metadata=tb_metadata, options=tb_options, partno=partno
    )
