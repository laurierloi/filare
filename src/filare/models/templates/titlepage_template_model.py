"""Template model and factory for titlepage.html."""

from __future__ import annotations

from typing import Any, ClassVar, Dict, Optional

from faker import Faker
from pydantic import ConfigDict, Field

from filare.models.templates.bom_template_model import FakeBomTemplateFactory
from filare.models.templates.index_table_template_model import (
    FakeIndexTableTemplateFactory,
)
from filare.models.templates.notes_template_model import FakeNotesTemplateFactory
from filare.models.templates.page_template_model import (
    FakeTemplatePageMetadataFactory,
    FakeTemplatePageOptionsFactory,
    PageTemplateModel,
    TemplatePageMetadata,
    TemplatePageOptions,
)
from filare.models.templates.template_model import TemplateModelFactory
from filare.models.templates.titleblock_template_model import (
    FakeTitleblockTemplateFactory,
    TitleblockTemplateModel,
)
from filare.render.templates import get_template

faker = Faker()


class TemplateTitlePageOptions(TemplatePageOptions):
    """Layout options referenced by titlepage.html."""

    show_notes: bool = True
    show_bom: bool = True
    show_index_table: bool = True

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)


class FakeTemplateTitlePageOptionsFactory(FakeTemplatePageOptionsFactory):
    """faker-backed factory for TemplateTitlePageOptions."""

    @classmethod
    def create(
        cls,
        show_notes: bool = True,
        show_bom: bool = True,
        show_index_table: bool = True,
        **overrides: Any,
    ) -> TemplateTitlePageOptions:
        base_keys = {"fontname", "bgcolor", "titleblock_rows", "titleblock_row_height"}
        base_overrides: Dict[str, Any] = {
            key: overrides.pop(key)
            for key in list(overrides.keys())
            if key in base_keys
        }
        base_options = FakeTemplatePageOptionsFactory.create(**base_overrides)
        payload: Dict[str, Any] = base_options.model_dump()
        payload.update(
            {
                "show_notes": show_notes,
                "show_bom": show_bom,
                "show_index_table": show_index_table,
            }
        )
        payload.update(overrides)
        return TemplateTitlePageOptions(**payload)


class TitlePageTemplateModel(PageTemplateModel):
    """Context model for rendering titlepage.html (extends page.html)."""

    template_name: ClassVar[str] = "titlepage"
    metadata: TemplatePageMetadata
    options: TemplateTitlePageOptions
    notes: Optional[str] = None
    bom: Optional[str] = None
    index_table: Optional[str] = None
    titleblock: str = "<div id='titleblock'></div>"

    def to_render_dict(self) -> dict:
        return {
            "template_name": self.template_name,
            "metadata": self.metadata,
            "options": self.options,
            "notes": self.notes,
            "bom": self.bom,
            "index_table": self.index_table,
            "titleblock": self.titleblock,
        }


class FakeTitlePageTemplateFactory(TemplateModelFactory):
    """Factory for TitlePageTemplateModel with rendered child templates."""

    class Meta:
        model = TitlePageTemplateModel

    def __init__(
        self,
        with_notes: bool = True,
        with_bom: bool = True,
        with_index: bool = True,
        render_titleblock: bool = True,
        titleblock_model: Optional[TitleblockTemplateModel] = None,
        **kwargs,
    ):
        metadata = kwargs.get("metadata") or FakeTemplatePageMetadataFactory.create(
            title=kwargs.pop("title", None)
        )
        kwargs["metadata"] = metadata

        provided_options = kwargs.get("options")
        options = provided_options or FakeTemplateTitlePageOptionsFactory.create(
            show_notes=with_notes, show_bom=with_bom, show_index_table=with_index
        )
        kwargs["options"] = options
        # Align section toggles with the actual options used.
        with_notes = options.show_notes
        with_bom = options.show_bom
        with_index = options.show_index_table

        if "titleblock" not in kwargs:
            if render_titleblock:
                tb_model = titleblock_model or FakeTitleblockTemplateFactory()()
                kwargs["titleblock"] = get_template("titleblock.html").render(
                    tb_model.to_render_dict()
                )
            else:
                kwargs["titleblock"] = "<div id='titleblock'>Titleblock</div>"

        if with_notes and "notes" not in kwargs:
            notes_model = FakeNotesTemplateFactory().create()
            kwargs["notes"] = get_template("notes.html").render(
                notes_model.to_render_dict()
            )
        if with_bom and "bom" not in kwargs:
            bom_model = FakeBomTemplateFactory(rows=2)()
            kwargs["bom"] = get_template("bom.html").render(bom_model.to_render_dict())
        if with_index and "index_table" not in kwargs:
            index_model = FakeIndexTableTemplateFactory(row_count=2)()
            kwargs["index_table"] = get_template("index_table.html").render(
                index_model.to_render_dict()
            )

        super().__init__(**kwargs)
