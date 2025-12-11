"""Template model and factory for cable.html."""

from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

from filare.models.colors import MultiColor, SingleColor
from filare.models.templates.template_model import TemplateModel, TemplateModelFactory

faker = Faker()


class TemplateWireColor(SingleColor):
    """Wire color with padded HTML helper."""

    @property
    def html_padded(self) -> str:
        return self.html or "#000000"


class TemplateCableColor(MultiColor):
    """Cable color bar with len helper."""

    @property
    def len(self) -> int:
        return len(self.colors)


class TemplatePartnumbers(BaseModel):
    """Minimal partnumbers helper for cable template."""

    values: List[List[str]]

    model_config = ConfigDict(extra="forbid")

    @property
    def is_list(self) -> bool:
        return True

    def as_list(self, parent_partnumbers: Optional["TemplatePartnumbers"] = None) -> List[List[str]]:
        return self.values

    def keep_only_shared(self) -> "TemplatePartnumbers":
        return self


class TemplateWire(BaseModel):
    """Wire entry for cable rendering."""

    id: str
    port: str
    color: TemplateWireColor
    is_shield: bool = False
    partnumbers: Optional[TemplatePartnumbers] = None

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
    color: Optional[TemplateCableColor] = None
    partnumbers: Optional[TemplatePartnumbers] = None
    wire_objects: Dict[str, TemplateWire] = Field(default_factory=dict)
    image: Optional[str] = None
    additional_components: List[object] = Field(default_factory=list)
    notes: Optional[str] = None

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
    def create(cls, idx: int, is_shield: bool = False, with_partnumbers: bool = False) -> TemplateWire:
        color = TemplateWireColor(code_en=faker.random_element(elements=["RD", "BK", "GN"]))
        partnumbers = (
            TemplatePartnumbers(values=[[faker.bothify(text="PN-###")]])
            if with_partnumbers
            else None
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

    def __init__(self, wirecount: int = 3, with_shield: bool = True, **kwargs):
        if "component" not in kwargs:
            wires: Dict[str, TemplateWire] = {}
            for idx in range(1, wirecount + 1):
                wires[f"W{idx}"] = FakeTemplateWireFactory.create(
                    idx, is_shield=False, with_partnumbers=True
                )
            if with_shield:
                wires["S1"] = FakeTemplateWireFactory.create(
                    idx=wirecount + 1, is_shield=True, with_partnumbers=False
                )
            partnumbers = TemplatePartnumbers(values=[[faker.bothify(text="PN-###")]])
            kwargs["component"] = TemplateCableComponent(
                designator="C1",
                type="cable",
                show_wirecount=True,
                wirecount=wirecount,
                gauge_str_with_equiv="18AWG",
                shield=with_shield,
                length_str="1m",
                color=TemplateCableColor(colors=[TemplateWireColor(code_en="RD")]),
                partnumbers=partnumbers,
                wire_objects=wires,
            )
        super().__init__(**kwargs)
