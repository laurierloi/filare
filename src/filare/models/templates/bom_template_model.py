"""Template model and factory for bom.html."""

from __future__ import annotations

from typing import ClassVar, List, Optional

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

from filare.models.templates.template_model import TemplateModel, TemplateModelFactory

faker = Faker()


class TemplateBomOptions(BaseModel):
    """Options controlling BOM rendering."""

    titleblock_rows: int = 0
    titleblock_row_height: float = 5.0
    bom_updated_position: Optional[str] = None
    bom_row_height: float = 5.0
    reverse: bool = False

    model_config = ConfigDict(extra="forbid")


class TemplateBomPayload(BaseModel):
    """BOM payload used by bom.html."""

    headers: List[str]
    columns_class: List[str]
    content: List[List[str]]
    options: TemplateBomOptions

    model_config = ConfigDict(extra="forbid")


class BomTemplateModel(TemplateModel):
    """Context model for rendering bom.html."""

    template_name: ClassVar[str] = "bom"
    bom: TemplateBomPayload
    options: TemplateBomOptions


class FakeBomTemplateFactory(TemplateModelFactory):
    """Factory for BomTemplateModel with faker defaults."""

    class Meta:
        model = BomTemplateModel

    def __init__(self, rows: int = 3, **kwargs):
        if "options" not in kwargs:
            kwargs["options"] = TemplateBomOptions(
                titleblock_rows=3,
                titleblock_row_height=5.0,
                bom_row_height=5.0,
                reverse=False,
            )
        if "bom" not in kwargs:
            headers = ["ID", "QTY", "DESC"]
            columns_class = ["bom_col_id", "bom_col_qty", "bom_col_desc"]
            content = [
                [f"{idx}", str(faker.random_int(min=1, max=5)), faker.sentence(nb_words=3)]
                for idx in range(1, rows + 1)
            ]
            kwargs["bom"] = TemplateBomPayload(
                headers=headers,
                columns_class=columns_class,
                content=content,
                options=kwargs["options"],
            )
        super().__init__(**kwargs)
