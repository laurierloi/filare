"""Template model and factory for titlepage.html."""

from __future__ import annotations

from typing import Any, ClassVar, Dict, Optional, cast

from faker import Faker
from pydantic import ConfigDict, Field

from filare.models.templates.bom_template_model import (
    BomTemplateModel,
    FakeBomTemplateFactory,
)
from filare.models.templates.index_table_template_model import (
    FakeIndexTableTemplateFactory,
)
from filare.models.templates.notes_template_model import (
    FakeNotesTemplateFactory,
    NotesTemplateModel,
)
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
                kwargs["titleblock"] = tb_model.render()
            else:
                kwargs["titleblock"] = "<div id='titleblock'>Titleblock</div>"

        if with_notes and "notes" not in kwargs:
            from filare.flows.templates.notes import build_notes_model

            notes_model = cast(NotesTemplateModel, FakeNotesTemplateFactory().create())
            built_notes = build_notes_model(
                notes_model.notes, options=notes_model.options
            )
            kwargs["notes"] = built_notes.render()
        if with_bom and "bom" not in kwargs:
            from filare.flows.templates.bom import build_bom_model

            bom_model = cast(BomTemplateModel, FakeBomTemplateFactory(rows=2)())
            built_bom = build_bom_model(
                headers=bom_model.bom.headers,
                columns_class=bom_model.bom.columns_class,
                content=bom_model.bom.content,
                options=bom_model.options,
            )
            kwargs["bom"] = built_bom.render()
        if with_index and "index_table" not in kwargs:
            index_model = FakeIndexTableTemplateFactory(row_count=2)()
            kwargs["index_table"] = index_model.render()

        super().__init__(**kwargs)
