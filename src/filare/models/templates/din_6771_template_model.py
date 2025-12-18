"""Template model and factory for din-6771.html."""

from __future__ import annotations

from typing import ClassVar, Optional, cast

from faker import Faker
from pydantic import ConfigDict, Field

from filare.models.colors import SingleColor
from filare.models.templates.bom_template_model import (
    BomTemplateModel,
    FakeBomTemplateFactory,
)
from filare.models.templates.notes_template_model import (
    FakeNotesTemplateFactory,
    NotesTemplateModel,
)
from filare.models.templates.page_template_model import (
    FakePageTemplateFactory,
    FakeTemplatePageMetadataFactory,
    FakeTemplatePageOptionsFactory,
    PageTemplateModel,
    TemplatePageMetadata,
    TemplatePageOptions,
)
from filare.render.templates import get_template

faker = Faker()


class TemplateDin6771Options(TemplatePageOptions):
    """Layout options referenced by din-6771.html."""

    show_notes: bool = True
    show_bom: bool = True
    bom_rows: int = 3
    bom_row_height: float = 5.0

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)


class FakeTemplateDin6771OptionsFactory(FakeTemplatePageOptionsFactory):
    """faker-backed factory for TemplateDin6771Options."""

    @classmethod
    def create(
        cls,
        show_notes: bool = True,
        show_bom: bool = True,
        bom_rows: int = 3,
        bom_row_height: float = 5.0,
        fontname: str = "Arial",
        bgcolor: SingleColor = SingleColor("#FFFFFF"),
        titleblock_rows: int = 3,
        titleblock_row_height: float = 5.0,
        **overrides: object,
    ) -> TemplateDin6771Options:
        base_options = super().create(
            fontname=fontname,
            bgcolor=bgcolor,
            titleblock_rows=titleblock_rows,
            titleblock_row_height=titleblock_row_height,
            **overrides,
        )
        payload = base_options.model_dump()
        payload.update(
            {
                "show_notes": show_notes,
                "show_bom": show_bom,
                "bom_rows": bom_rows,
                "bom_row_height": bom_row_height,
            }
        )
        return TemplateDin6771Options(**payload)


class Din6771TemplateModel(PageTemplateModel):
    """Context model for rendering din-6771.html (extends page.html)."""

    template_name: ClassVar[str] = "din-6771"
    metadata: TemplatePageMetadata
    options: TemplateDin6771Options
    title: str = "DIN 6771 Diagram"
    diagram: str = "<svg></svg>"
    notes: Optional[str] = None
    bom: Optional[str] = None
    diagram_container_class: Optional[str] = None
    diagram_container_style: Optional[str] = None
    titleblock: str = "<div id='titleblock'></div>"

    def to_render_dict(self) -> dict:
        return {
            "template_name": self.template_name,
            "metadata": self.metadata,
            "options": self.options,
            "title": self.title,
            "diagram": self.diagram,
            "notes": self.notes,
            "bom": self.bom,
            "diagram_container_class": self.diagram_container_class,
            "diagram_container_style": self.diagram_container_style,
            "titleblock": self.titleblock,
        }


class FakeDin6771TemplateFactory(FakePageTemplateFactory):
    """Factory for Din6771TemplateModel with rendered notes and BOM segments."""

    class Meta:
        model = Din6771TemplateModel

    def __init__(
        self,
        with_notes: bool = True,
        with_bom: bool = True,
        bom_rows: int = 3,
        bom_row_height: float = 5.0,
        diagram: Optional[str] = None,
        diagram_container_class: Optional[str] = None,
        diagram_container_style: Optional[str] = None,
        title: Optional[str] = None,
        **kwargs,
    ):
        metadata = kwargs.get("metadata") or FakeTemplatePageMetadataFactory.create()
        chosen_title = title or metadata.title or "DIN 6771 Diagram"
        metadata.title = chosen_title
        kwargs["metadata"] = metadata

        if "title" not in kwargs:
            kwargs["title"] = chosen_title

        if "options" not in kwargs:
            base_page_options = FakeTemplatePageOptionsFactory.create()
            kwargs["options"] = FakeTemplateDin6771OptionsFactory.create(
                show_notes=with_notes,
                show_bom=with_bom,
                bom_rows=bom_rows,
                bom_row_height=bom_row_height,
                fontname=base_page_options.fontname,
                bgcolor=base_page_options.bgcolor,
                titleblock_rows=base_page_options.titleblock_rows,
                titleblock_row_height=base_page_options.titleblock_row_height,
            )

        if with_notes and "notes" not in kwargs:
            from filare.flows.templates.notes import build_notes_model

            notes_model = cast(NotesTemplateModel, FakeNotesTemplateFactory()())
            built_notes = build_notes_model(
                notes_model.notes, options=notes_model.options
            )
            kwargs["notes"] = built_notes.render()
        if with_bom and "bom" not in kwargs:
            from filare.flows.templates.bom import build_bom_model

            bom_model = cast(BomTemplateModel, FakeBomTemplateFactory(rows=bom_rows)())
            built_bom = build_bom_model(
                headers=bom_model.bom.headers,
                columns_class=bom_model.bom.columns_class,
                content=bom_model.bom.content,
                options=bom_model.options,
            )
            kwargs["bom"] = built_bom.render()
        if "diagram" not in kwargs:
            kwargs["diagram"] = diagram or "<svg><text>Diagram</text></svg>"
        if (
            diagram_container_class is not None
            and "diagram_container_class" not in kwargs
        ):
            kwargs["diagram_container_class"] = diagram_container_class
        if (
            diagram_container_style is not None
            and "diagram_container_style" not in kwargs
        ):
            kwargs["diagram_container_style"] = diagram_container_style
        super().__init__(**kwargs)
