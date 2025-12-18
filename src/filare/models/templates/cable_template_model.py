"""Template model and factory for cable.html."""

from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

from filare.models.colors import (
    COLOR_CODES,
    FakeMultiColorFactory,
    FakeSingleColorFactory,
    MultiColor,
    SingleColor,
)
from filare.models.hypertext import FakeMultilineHypertextFactory, MultilineHypertext
from filare.models.partnumber import FakePartNumberInfoListFactory, PartnumberInfoList
from filare.models.templates.template_model import TemplateModel, TemplateModelFactory

faker = Faker()


class TemplateWire(BaseModel):
    """Wire entry for cable rendering."""

    id: str
    port: str
    color: SingleColor
    is_shield: bool = False
    partnumbers: Optional[PartnumberInfoList] = None

    model_config = ConfigDict(extra="forbid")

    def wireinfo(self) -> str:
        return f"Wire {self.id}"


class TemplateCableComponent(BaseModel):
    """Component context used by cable.html."""

    designator: str
    type: Optional[str] = None
    show_wirecount: bool = True
    wirecount: int = 1
    gauge_str_with_equiv: Optional[str] = None
    shield: bool = False
    length_str: Optional[str] = None
    color: Optional[MultiColor] = None
    partnumbers: Optional[PartnumberInfoList] = None
    wire_objects: Dict[str, TemplateWire] = Field(default_factory=dict)
    image: Optional[str] = None
    additional_components: List[object] = Field(default_factory=list)
    notes: Optional[MultilineHypertext] = None

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    def wire_ins_str(self, wire_id: str) -> str:
        return f"{wire_id}-IN"

    def wire_outs_str(self, wire_id: str) -> str:
        return f"{wire_id}-OUT"


class CableTemplateModel(TemplateModel):
    """Context model for rendering cable.html."""

    template_name: ClassVar[str] = "cable"
    component: TemplateCableComponent

    def to_render_dict(self) -> dict:
        return {"template_name": self.template_name, "component": self.component}


class FakeTemplateWireFactory:
    """faker-backed factory for TemplateWire."""

    @classmethod
    def create(
        cls, idx: int, is_shield: bool = False, with_partnumbers: bool = False
    ) -> TemplateWire:
        color = FakeSingleColorFactory.create(allow_unknown=False)
        partnumbers = (
            FakePartNumberInfoListFactory.create(count=1) if with_partnumbers else None
        )
        return TemplateWire(
            id=f"W{idx}",
            port=f"p{idx}",
            color=color,
            is_shield=is_shield,
            partnumbers=partnumbers,
        )


class FakeCableTemplateFactory(TemplateModelFactory):
    """Factory for CableTemplateModel with faker defaults."""

    class Meta:
        model = CableTemplateModel

    def __init__(
        self,
        wirecount: int = 3,
        with_shield: bool = True,
        partnumber_unique_count: int = 2,
        use_color_code_palette: bool = False,
        **kwargs,
    ):
        if "component" not in kwargs:
            wires: Dict[str, TemplateWire] = {}
            for idx in range(1, wirecount + 1):
                wires[f"W{idx}"] = FakeTemplateWireFactory.create(
                    idx,
                    is_shield=False,
                    with_partnumbers=True,
                )
            if with_shield:
                wires["S1"] = FakeTemplateWireFactory.create(
                    idx=wirecount + 1, is_shield=True, with_partnumbers=False
                )
            partnumbers = FakePartNumberInfoListFactory.create(
                count=partnumber_unique_count
            )
            if use_color_code_palette:
                color_code = faker.random_element(elements=list(COLOR_CODES.keys()))
                color_value = FakeMultiColorFactory.create(
                    count=wirecount, allow_unknown=False, color_code=color_code
                )
            else:
                color_value = FakeMultiColorFactory.create(
                    count=wirecount, allow_unknown=False
                )
            kwargs["component"] = TemplateCableComponent(
                designator="C1",
                type="cable",
                show_wirecount=True,
                wirecount=wirecount,
                gauge_str_with_equiv="18AWG",
                shield=with_shield,
                length_str="1m",
                color=color_value,
                partnumbers=partnumbers,
                wire_objects=wires,
                notes=FakeMultilineHypertextFactory.create(),
            )
        super().__init__(**kwargs)
