"""Template model and factory for colors_macro.html."""

from __future__ import annotations

from typing import ClassVar, List

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

from filare.models.colors import (
    FakeMultiColorFactory,
    FakeSingleColorFactory,
    MultiColor,
    SingleColor,
)
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


class FakeTemplateColorLegendFactory:
    """faker-backed factory for TemplateColorLegend."""

    @classmethod
    def create(
        cls,
        count: int = 1,
        allow_unknown: bool = False,
        unknown_chance: int = 20,
        color_code: str | None = None,
    ) -> TemplateColorLegend:
        multicolor = FakeMultiColorFactory.create(
            count=count,
            allow_unknown=allow_unknown,
            unknown_chance=unknown_chance,
            color_code=color_code,
        )
        colors = list(multicolor.colors)
        if not colors:
            colors = [
                FakeSingleColorFactory.create(
                    allow_unknown=allow_unknown, unknown_chance=unknown_chance
                )
            ]
        hex_color = colors[0].html or faker.hex_color()
        return TemplateColorLegend(
            name=faker.lexify(text="??").upper(),
            hex=hex_color,
            colors=colors,
        )


class FakeColorsMacroTemplateFactory(TemplateModelFactory):
    """Factory for ColorsMacroTemplateModel with faker defaults."""

    class Meta:
        model = ColorsMacroTemplateModel

    def __init__(
        self,
        count: int = 3,
        allow_unknown: bool = False,
        unknown_chance: int = 20,
        color_code: str | None = None,
        legend_color_count: int = 1,
        **kwargs,
    ):
        if "colors" not in kwargs:
            kwargs["colors"] = [
                FakeTemplateColorLegendFactory.create(
                    count=legend_color_count,
                    allow_unknown=allow_unknown,
                    unknown_chance=unknown_chance,
                    color_code=color_code,
                )
                for _ in range(count)
            ]
        super().__init__(**kwargs)
