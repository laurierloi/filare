"""Template model and factory for termination_table.html."""

from __future__ import annotations

from typing import ClassVar, List

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

from filare.models.templates.template_model import TemplateModel, TemplateModelFactory

faker = Faker()


class TemplateTerminationRow(BaseModel):
    """Row entry for termination_table rendering."""

    source: str
    target: str
    source_termination: str
    target_termination: str

    model_config = ConfigDict(extra="forbid")


class FakeTemplateTerminationRowFactory:
    """faker-backed factory for TemplateTerminationRow."""

    @classmethod
    def create(cls, idx: int) -> TemplateTerminationRow:
        return TemplateTerminationRow(
            source=f"S{idx}",
            target=f"T{idx}",
            source_termination=faker.word(),
            target_termination=faker.word(),
        )


class TerminationTableTemplateModel(TemplateModel):
    """Context model for rendering termination_table.html."""

    template_name: ClassVar[str] = "termination_table"
    rows: List[TemplateTerminationRow] = Field(default_factory=list)


class FakeTerminationTableTemplateFactory(TemplateModelFactory):
    """Factory for TerminationTableTemplateModel with faker defaults."""

    class Meta:
        model = TerminationTableTemplateModel

    def __init__(self, row_count: int = 3, **kwargs):
        if "rows" not in kwargs:
            kwargs["rows"] = [
                FakeTemplateTerminationRowFactory.create(idx)
                for idx in range(1, row_count + 1)
            ]
        super().__init__(**kwargs)
