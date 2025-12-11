"""Template model and factory for colors_macro.html."""

from __future__ import annotations

from typing import ClassVar, List

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

from filare.models.colors import MultiColor, SingleColor
from filare.models.templates.template_model import TemplateModel, TemplateModelFactory

faker = Faker()


class TemplateColorLegend(BaseModel):
    """Color legend entry."""

    name: str
    hex: str
    colors: List[SingleColor] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")

    @property
    def html(self) -> str:
        return self.hex

    @property
    def len(self) -> int:
        return len(self.colors) if self.colors else 1


class ColorsMacroTemplateModel(TemplateModel):
    """Context model for rendering colors_macro.html."""

    template_name: ClassVar[str] = "colors_macro"
    colors: List[TemplateColorLegend] = Field(default_factory=list)


class FakeColorsMacroTemplateFactory(TemplateModelFactory):
    """Factory for ColorsMacroTemplateModel with faker defaults."""

    class Meta:
        model = ColorsMacroTemplateModel

    def __init__(self, count: int = 3, **kwargs):
        if "colors" not in kwargs:
            legends = []
            for _ in range(count):
                hex_color = faker.hex_color()
                legends.append(
                    TemplateColorLegend(
                        name=faker.lexify(text="??").upper(),
                        hex=hex_color,
                        colors=[SingleColor(hex_color)],
                    )
                )
            kwargs["colors"] = legends
        super().__init__(**kwargs)
