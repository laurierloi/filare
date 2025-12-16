"""Template model and factory for termination.html."""

from __future__ import annotations

from typing import ClassVar, Optional

from filare.models.templates.page_template_model import (
    FakePageTemplateFactory,
    FakeTemplatePageMetadataFactory,
    FakeTemplatePageOptionsFactory,
    PageTemplateModel,
    TemplatePageMetadata,
    TemplatePageOptions,
)
from filare.models.templates.termination_table_template_model import (
    FakeTerminationTableTemplateFactory,
)
from filare.render.templates import get_template


class TerminationTemplateModel(PageTemplateModel):
    """Context model for rendering termination.html (extends page.html)."""

    template_name: ClassVar[str] = "termination"
    metadata: TemplatePageMetadata
    options: TemplatePageOptions
    titleblock: str = "<div id='titleblock'></div>"
    termination_table: Optional[str] = None

    def to_render_dict(self) -> dict:
        return {
            "template_name": self.template_name,
            "metadata": self.metadata,
            "options": self.options,
            "titleblock": self.titleblock,
            "termination_table": self.termination_table,
        }


class FakeTerminationTemplateFactory(FakePageTemplateFactory):
    """Factory for TerminationTemplateModel with rendered termination_table content."""

    class Meta:
        model = TerminationTemplateModel

    def __init__(self, row_count: int = 3, **kwargs):
        if "termination_table" not in kwargs:
            table_model = FakeTerminationTableTemplateFactory(row_count=row_count)()
            kwargs["termination_table"] = get_template("termination_table.html").render(
                table_model.to_render_dict()
            )
        if "metadata" not in kwargs:
            kwargs["metadata"] = FakeTemplatePageMetadataFactory.create()
        if "options" not in kwargs:
            kwargs["options"] = FakeTemplatePageOptionsFactory.create()
        super().__init__(**kwargs)
