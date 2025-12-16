"""Template model and factory for index_table.html."""

from __future__ import annotations

from typing import ClassVar, List, Optional

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

from filare.models.templates.template_model import TemplateModel, TemplateModelFactory

faker = Faker()


class TemplateIndexTableRow(BaseModel):
    """Row entry for index_table rendering."""

    items: List[str]
    pdf_items: Optional[List[str]] = None

    model_config = ConfigDict(extra="forbid")

    def get_items(self, for_pdf: bool) -> List[str]:
        """Return items, optionally swapping in PDF-specific values."""
        if for_pdf and self.pdf_items:
            return self.pdf_items
        return self.items


class TemplateIndexTable(BaseModel):
    """Index table payload with header and rows."""

    header: List[str]
    rows: List[TemplateIndexTableRow]

    model_config = ConfigDict(extra="forbid")


class TemplateIndexTableOptions(BaseModel):
    """Layout options referenced by index_table.html."""

    index_table_row_height: float = 10.0
    index_table_on_right: bool = False
    index_table_updated_position: Optional[str] = None
    show_bom: bool = False
    bom_rows: int = 0
    bom_row_height: float = 5.0
    for_pdf: bool = False
    index_table_title: str = "INDEX TABLE"

    model_config = ConfigDict(extra="forbid")


class FakeTemplateIndexTableRowFactory:
    """faker-backed factory for TemplateIndexTableRow."""

    @classmethod
    def create(cls, idx: int) -> TemplateIndexTableRow:
        base_items = [
            f"I{idx}",
            str(faker.random_int(min=1, max=5)),
            faker.word(),
        ]
        pdf_items = [item.upper() for item in base_items]
        return TemplateIndexTableRow(items=base_items, pdf_items=pdf_items)


class FakeTemplateIndexTableOptionsFactory:
    """faker-backed factory for TemplateIndexTableOptions."""

    @classmethod
    def create(
        cls,
        index_table_row_height: float = 10.0,
        index_table_on_right: bool = False,
        index_table_updated_position: Optional[str] = None,
        show_bom: bool = False,
        bom_rows: int = 0,
        bom_row_height: float = 5.0,
        for_pdf: bool = False,
        index_table_title: str = "INDEX TABLE",
        **overrides: object,
    ) -> TemplateIndexTableOptions:
        payload = {
            "index_table_row_height": index_table_row_height,
            "index_table_on_right": index_table_on_right,
            "index_table_updated_position": index_table_updated_position,
            "show_bom": show_bom,
            "bom_rows": bom_rows,
            "bom_row_height": bom_row_height,
            "for_pdf": for_pdf,
            "index_table_title": index_table_title,
        }
        payload.update(overrides)
        return TemplateIndexTableOptions(**payload)


class IndexTableTemplateModel(TemplateModel):
    """Context model for rendering index_table.html."""

    template_name: ClassVar[str] = "index_table"
    index_table: TemplateIndexTable
    options: TemplateIndexTableOptions = Field(
        default_factory=TemplateIndexTableOptions
    )

    def to_render_dict(self) -> dict:
        return {
            "template_name": self.template_name,
            "index_table": self.index_table,
            "options": self.options,
        }


class FakeIndexTableTemplateFactory(TemplateModelFactory):
    """Factory for IndexTableTemplateModel with faker defaults."""

    class Meta:
        model = IndexTableTemplateModel

    def __init__(self, row_count: int = 3, **kwargs):
        if "index_table" not in kwargs:
            header = ["ID", "QTY", "DESC"]
            rows = [
                FakeTemplateIndexTableRowFactory.create(idx)
                for idx in range(1, row_count + 1)
            ]
            kwargs["index_table"] = TemplateIndexTable(header=header, rows=rows)
        if "options" not in kwargs:
            kwargs["options"] = FakeTemplateIndexTableOptionsFactory.create(
                index_table_row_height=10.0, show_bom=True, bom_rows=2
            )
        super().__init__(**kwargs)
