"""Template model and factory for notes.html."""

from __future__ import annotations

from typing import ClassVar

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

from filare.models.hypertext import MultilineHypertext
from filare.models.templates.template_model import TemplateModel, TemplateModelFactory

faker = Faker()


class TemplateNotesOptions(BaseModel):
    """Layout options referenced by notes.html."""

    show_bom: bool = False
    notes_on_right: bool = False
    titleblock_rows: int = 3
    titleblock_row_height: float = 5.0
    bom_rows: int = 0
    bom_row_height: float = 5.0
    notes_width: str = "80mm"

    model_config = ConfigDict(extra="forbid")


class FakeTemplateNotesOptionsFactory:
    """faker-backed factory for TemplateNotesOptions."""

    @classmethod
    def create(
        cls,
        show_bom: bool = False,
        notes_on_right: bool = False,
        titleblock_rows: int = 3,
        titleblock_row_height: float = 5.0,
        bom_rows: int = 0,
        bom_row_height: float = 5.0,
        notes_width: str = "80mm",
        **overrides: object,
    ) -> TemplateNotesOptions:
        payload = {
            "show_bom": show_bom,
            "notes_on_right": notes_on_right,
            "titleblock_rows": titleblock_rows,
            "titleblock_row_height": titleblock_row_height,
            "bom_rows": bom_rows,
            "bom_row_height": bom_row_height,
            "notes_width": notes_width,
        }
        payload.update(overrides)
        return TemplateNotesOptions(**payload)


class NotesTemplateModel(TemplateModel):
    """Context model for rendering notes.html."""

    template_name: ClassVar[str] = "notes"
    notes: MultilineHypertext
    options: TemplateNotesOptions = Field(default_factory=TemplateNotesOptions)

    def to_render_dict(self) -> dict:
        return {
            "template_name": self.template_name,
            "notes": self.notes,
            "options": self.options,
        }


class FakeNotesTemplateFactory(TemplateModelFactory):
    """Factory for NotesTemplateModel with faker defaults."""

    class Meta:
        model = NotesTemplateModel

    def __init__(self, **kwargs):
        if "notes" not in kwargs:
            kwargs["notes"] = MultilineHypertext.to(faker.sentence(nb_words=6))
        if "options" not in kwargs:
            kwargs["options"] = FakeTemplateNotesOptionsFactory.create(
                show_bom=True,
                notes_on_right=False,
                titleblock_rows=3,
                titleblock_row_height=5.0,
                bom_rows=3,
                bom_row_height=5.0,
                notes_width="120mm",
            )
        super().__init__(**kwargs)
