"""Template model and factory for cut_table.html."""

from __future__ import annotations

from typing import ClassVar, List

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

from filare.models.colors import FakeSingleColorFactory, SingleColor
from filare.models.templates.template_model import TemplateModel, TemplateModelFactory

faker = Faker()


class TemplateCutTableRow(BaseModel):
    """Row entry for cut_table rendering."""

    wire: str
    partno: str
    color: SingleColor
    length: str

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)


class CutTableTemplateModel(TemplateModel):
    """Context model for rendering cut_table.html."""

    template_name: ClassVar[str] = "cut_table"
    rows: List[TemplateCutTableRow] = Field(default_factory=list)


class FakeCutTableTemplateFactory(TemplateModelFactory):
    """Factory for CutTableTemplateModel with faker defaults."""

    class Meta:
        model = CutTableTemplateModel

    def __init__(self, row_count: int = 3, **kwargs):
        if "rows" not in kwargs:
            kwargs["rows"] = [
                TemplateCutTableRow(
                    wire=f"W{idx}",
                    partno=faker.bothify(text="PN-###"),
                    color=FakeSingleColorFactory.create(allow_unknown=False),
                    length=f"{faker.random_int(min=10, max=500)}mm",
                )
                for idx in range(1, row_count + 1)
            ]
        super().__init__(**kwargs)
