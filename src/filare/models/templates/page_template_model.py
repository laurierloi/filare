"""Template model and factory for page.html."""

from __future__ import annotations

from typing import ClassVar, Optional

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

from filare.models.colors import SingleColor
from filare.models.metadata import PageTemplateConfig
from filare.models.templates.template_model import TemplateModel, TemplateModelFactory

faker = Faker()


class TemplatePageOptions(BaseModel):
    """Page-level styling options shared by many templates."""

    fontname: str = "Arial"
    bgcolor: SingleColor = Field(default_factory=lambda: SingleColor("#FFFFFF"))
    titleblock_rows: int = 3
    titleblock_row_height: float = 5.0

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)


class FakeTemplatePageOptionsFactory:
    """faker-backed factory for TemplatePageOptions."""

    @classmethod
    def create(
        cls,
        fontname: str = "Arial",
        bgcolor: SingleColor = SingleColor("#FFFFFF"),
        titleblock_rows: int = 3,
        titleblock_row_height: float = 5.0,
        **overrides: object,
    ) -> TemplatePageOptions:
        payload = {
            "fontname": fontname,
            "bgcolor": bgcolor,
            "titleblock_rows": titleblock_rows,
            "titleblock_row_height": titleblock_row_height,
        }
        payload.update(overrides)
        return TemplatePageOptions(**payload)


class TemplatePageMetadata(BaseModel):
    """Metadata used by page.html and downstream templates."""

    generator: str = "Filare"
    title: str = "Filare Document"
    template: PageTemplateConfig = Field(default_factory=PageTemplateConfig)

    model_config = ConfigDict(extra="forbid")


class FakeTemplatePageMetadataFactory:
    """faker-backed factory for TemplatePageMetadata."""

    @classmethod
    def create(
        cls,
        generator: str = "Filare",
        title: Optional[str] = None,
        template: Optional[PageTemplateConfig] = None,
        **overrides: object,
    ) -> TemplatePageMetadata:
        payload = {
            "generator": generator,
            "title": title or faker.word().title(),
            "template": template or PageTemplateConfig(),
        }
        payload.update(overrides)
        return TemplatePageMetadata(**payload)


class PageTemplateModel(TemplateModel):
    """Context model for rendering page.html directly."""

    template_name: ClassVar[str] = "page"
    metadata: TemplatePageMetadata
    options: TemplatePageOptions
    titleblock: str = "<div id='titleblock'></div>"

    def to_render_dict(self) -> dict:
        return {
            "template_name": self.template_name,
            "metadata": self.metadata,
            "options": self.options,
            "titleblock": self.titleblock,
        }


class FakePageTemplateFactory(TemplateModelFactory):
    """Factory for PageTemplateModel with sensible defaults."""

    class Meta:
        model = PageTemplateModel

    def __init__(self, **kwargs):
        if "metadata" not in kwargs:
            kwargs["metadata"] = FakeTemplatePageMetadataFactory.create()
        if "options" not in kwargs:
            kwargs["options"] = FakeTemplatePageOptionsFactory.create()
        if "titleblock" not in kwargs:
            kwargs["titleblock"] = "<div id='titleblock'>Titleblock</div>"
        super().__init__(**kwargs)
