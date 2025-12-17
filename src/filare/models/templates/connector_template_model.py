"""Template model and factory for connector.html."""

from __future__ import annotations

from typing import ClassVar, List, Optional

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

from filare.models.colors import MultiColor, SingleColor
from filare.models.hypertext import MultilineHypertext
from filare.models.templates.template_model import TemplateModel, TemplateModelFactory

faker = Faker()


class TemplateMultiColor(MultiColor):
    """MultiColor with a len property for template convenience."""

    @property
    def len(self) -> int:
        return len(self.colors)


class TemplateConnectorPin(BaseModel):
    """Pin entry for connector template rendering."""

    id: str
    index: int = 0
    label: Optional[str] = None
    color: Optional[TemplateMultiColor] = None

    model_config = ConfigDict(extra="forbid")


class TemplateConnectorComponent(BaseModel):
    """Component context used by connector.html."""

    designator: str
    type: MultilineHypertext
    subtype: Optional[MultilineHypertext] = None
    color: Optional[TemplateMultiColor] = None
    show_pincount: bool = True
    pincount: int = 0
    ports_left: bool = True
    ports_right: bool = True
    has_pincolors: bool = True
    pins: List[TemplateConnectorPin] = Field(default_factory=list)
    partnumbers: Optional[object] = None
    image: Optional[str] = None
    additional_components: List[object] = Field(default_factory=list)
    notes: Optional[MultilineHypertext] = None

    model_config = ConfigDict(extra="forbid")

    def pins_to_show(self) -> List[TemplateConnectorPin]:
        """Return pins with index populated for template port naming."""
        result: List[TemplateConnectorPin] = []
        for idx, pin in enumerate(self.pins):
            pin.index = idx
            result.append(pin)
        return result


class ConnectorTemplateModel(TemplateModel):
    """Context model for rendering connector.html."""

    template_name: ClassVar[str] = "connector"
    component: TemplateConnectorComponent

    def to_render_dict(self) -> dict:
        return {"template_name": self.template_name, "component": self.component}


class FakeTemplateMultiColorFactory:
    """faker-backed factory for TemplateMultiColor."""

    @classmethod
    def create(cls, colors: Optional[List[str]] = None) -> TemplateMultiColor:
        base_colors = colors or [faker.random_element(elements=["RD", "BK", "GN"])]
        single_colors = [SingleColor(color) for color in base_colors]
        return TemplateMultiColor(colors=single_colors)


class FakeTemplateConnectorPinFactory:
    """faker-backed factory for TemplateConnectorPin."""

    @classmethod
    def create(cls, idx: int) -> TemplateConnectorPin:
        color = FakeTemplateMultiColorFactory.create()
        return TemplateConnectorPin(
            id=f"{idx + 1}",
            index=idx,
            label=faker.random_element(elements=[f"L{idx+1}", None]),
            color=color,
        )


class FakeConnectorTemplateFactory(TemplateModelFactory):
    """Factory for ConnectorTemplateModel with faker defaults."""

    class Meta:
        model = ConnectorTemplateModel

    def __init__(self, pincount: int = 2, **kwargs):
        if "component" not in kwargs:
            pins = [FakeTemplateConnectorPinFactory.create(i) for i in range(pincount)]
            kwargs["component"] = TemplateConnectorComponent(
                designator="J1",
                type=MultilineHypertext.to(faker.word().title()),
                subtype=MultilineHypertext.to(faker.word().title()),
                color=FakeTemplateMultiColorFactory.create(["RD", "BK"]),
                show_pincount=True,
                pincount=pincount,
                ports_left=True,
                ports_right=True,
                has_pincolors=True,
                pins=pins,
                partnumbers=None,
            )
        super().__init__(**kwargs)
