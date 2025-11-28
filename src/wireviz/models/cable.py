"""Cable and wire models."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Union

from pydantic import BaseModel, Extra, Field, root_validator, validator

from wireviz.models.colors import MultiColor, SingleColor, get_color_by_colorcode_index
from wireviz.models.connector import GraphicalComponentModel
from wireviz.models.dataclasses import (  # noqa: F401
    Cable,
    Connection,
    ShieldClass,
    WireClass,
)
from wireviz.models.hypertext import MultilineHypertext
from wireviz.models.numbers import NumberAndUnit
from wireviz.models.types import BomCategory, QtyMultiplierCable  # noqa: F401


class CableModel(GraphicalComponentModel):
    wirecount: Optional[int] = None
    shield: Union[bool, str, MultiColor] = False
    colors: List[str] = Field(default_factory=list)
    color_code: Optional[str] = None
    wirelabels: List[Any] = Field(default_factory=list)
    gauge: Optional[Union[str, NumberAndUnit]] = None
    length: Optional[Union[str, NumberAndUnit]] = None
    show_wirecount: bool = True
    show_equiv: bool = False

    @validator("colors", pre=True)
    def _coerce_colors(cls, value: Any) -> List[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        return list(value)

    @validator("wirelabels", pre=True)
    def _coerce_wirelabels(cls, value: Any) -> List[Any]:
        if value is None:
            return []
        return list(value)

    @validator("gauge", "length", pre=True)
    def _coerce_number_unit(cls, value: Any) -> Optional[NumberAndUnit]:
        if value is None:
            return None
        return NumberAndUnit.to_number_and_unit(value)

    @validator("shield", pre=True)
    def _coerce_shield(cls, value: Any):
        if value is None:
            return False
        if isinstance(value, str):
            return value
        return value

    @root_validator
    def _ensure_colors(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        colors = values.get("colors") or []
        wirecount = values.get("wirecount")
        color_code = values.get("color_code")
        color = values.get("color")
        if not colors and wirecount:
            if color_code:
                colors = [
                    get_color_by_colorcode_index(color_code, i)
                    for i in range(wirecount)
                ]
            elif color:
                multicolor = MultiColor(color)
                colors = [multicolor[i] for i in range(wirecount)]
            else:
                colors = ["" for _ in range(wirecount)]
        values["colors"] = colors
        return values

    def to_cable(self) -> Cable:
        kwargs = dict(
            designator=self.designator,
            type=self.type,
            subtype=self.subtype,
            color=self.color,
            image=self.image,
            notes=self.notes,
            additional_components=self.additional_components,
            bgcolor=self.bgcolor,
            bgcolor_title=self.bgcolor_title,
            show_name=self.show_name,
            wirecount=self.wirecount,
            shield=self.shield,
            colors=self.colors,
            color_code=self.color_code,
            wirelabels=self.wirelabels,
            gauge=self.gauge,
            length=self.length,
            show_wirecount=self.show_wirecount,
            show_equiv=self.show_equiv,
        )
        # defaults to cable category
        kwargs["category"] = BomCategory.CABLE
        return Cable(**kwargs)


__all__ = [
    "Cable",
    "Connection",
    "ShieldClass",
    "WireClass",
    "CableModel",
    "QtyMultiplierCable",
]
