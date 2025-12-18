"""Template model and factory for cut.html."""

from __future__ import annotations

from typing import ClassVar, Optional

from filare.models.templates.cut_table_template_model import (
    CutTableTemplateModel,
    FakeCutTableTemplateFactory,
)
from filare.models.templates.page_template_model import (
    FakePageTemplateFactory,
    PageTemplateModel,
    TemplatePageMetadata,
    TemplatePageOptions,
)
from filare.render.templates import get_template


class CutTemplateModel(PageTemplateModel):
    """Context model for rendering cut.html (extends page.html)."""

    template_name: ClassVar[str] = "cut"
    metadata: TemplatePageMetadata
    options: TemplatePageOptions
    titleblock: str = "<div id='titleblock'></div>"
    cut_table: Optional[str] = None

    def to_render_dict(self) -> dict:
        return {
            "template_name": self.template_name,
            "metadata": self.metadata,
            "options": self.options,
            "titleblock": self.titleblock,
            "cut_table": self.cut_table,
        }


class FakeCutTemplateFactory(FakePageTemplateFactory):
    """Factory for CutTemplateModel with rendered cut_table content."""

    class Meta:
        model = CutTemplateModel

    def __init__(self, row_count: int = 3, **kwargs):
        if "cut_table" not in kwargs:
            from filare.flows.templates.cut_table import build_cut_table_model

            table_model = FakeCutTableTemplateFactory(row_count=row_count)()
            built_table = build_cut_table_model(table_model.rows)
            kwargs["cut_table"] = built_table.render()
        super().__init__(**kwargs)
