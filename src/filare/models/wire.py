"""Pydantic shims for wire-related dataclasses."""

from __future__ import annotations

from typing import Any, List, Optional, Union, cast

from pydantic import BaseModel, ConfigDict, Field, field_validator

from filare.models.colors import MultiColor, SingleColor
from filare.models.dataclasses import ShieldClass, WireClass  # noqa: F401
from filare.models.hypertext import MultilineHypertext
from filare.models.image import Image
from filare.models.numbers import NumberAndUnit
from filare.models.types import BomCategory


class WireModel(BaseModel):
    """Pydantic representation mirroring WireClass fields."""

    designator: str = ""
    parent: Optional[str] = None
    index: Optional[int] = None
    id: Optional[Union[str, int]] = None
    label: str = ""
    color: Optional[MultiColor] = None
    type: Optional[MultilineHypertext] = None
    subtype: Optional[MultilineHypertext] = None
    image: Optional[Image] = None
    notes: Optional[MultilineHypertext] = None
    additional_components: List[Any] = Field(default_factory=list)
    bgcolor: Optional[SingleColor] = None
    bgcolor_title: Optional[SingleColor] = None
    show_name: Optional[bool] = None
    gauge: Optional[NumberAndUnit] = None
    length: Optional[NumberAndUnit] = None
    ignore_in_bom: bool = False
    show_equiv: bool = False
    category: Optional[Union[str, BomCategory]] = None

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    @field_validator("type", "subtype", "notes", mode="before")
    def _to_multiline(
        cls, value: Optional[Union[str, MultilineHypertext]]
    ) -> Optional[MultilineHypertext]:
        if value is None:
            return value
        return MultilineHypertext.to(value)

    @field_validator("color", mode="before")
    def _to_multicolor(
        cls, value: Optional[Union[str, MultiColor]]
    ) -> Optional[MultiColor]:
        if value is None:
            return value
        return MultiColor(value)

    @field_validator("bgcolor", "bgcolor_title", mode="before")
    def _to_single_color(
        cls, value: Optional[Union[str, SingleColor]]
    ) -> Optional[SingleColor]:
        if value is None:
            return value
        return SingleColor(value)

    @field_validator("gauge", "length", mode="before")
    def _to_number_and_unit(cls, value: Any) -> Optional[NumberAndUnit]:
        if value is None:
            return None
        return NumberAndUnit.to_number_and_unit(value)

    @field_validator("parent", mode="before")
    def _coerce_parent(cls, value: Any) -> Optional[str]:
        if value is None:
            return None
        return str(value)

    def to_wireclass(self) -> WireClass:
        return WireClass(
            designator=self.designator,
            parent=self.parent,
            index=self.index,
            id=self.id,
            label=self.label,
            color=self.color,
            type=self.type,
            subtype=self.subtype,
            image=self.image,
            notes=self.notes,
            additional_components=cast(List[WireClass], self.additional_components),
            bgcolor=self.bgcolor,
            bgcolor_title=self.bgcolor_title,
            show_name=self.show_name,
            gauge=self.gauge,
            length=self.length,
            ignore_in_bom=self.ignore_in_bom,
            show_equiv=self.show_equiv,
            category=self.category or BomCategory.WIRE,
        )

    @classmethod
    def from_wireclass(cls, wire: WireClass) -> "WireModel":
        return cls(
            designator=wire.designator,
            parent=wire.parent,
            index=wire.index,
            id=getattr(wire, "id", None),
            label=wire.label,
            color=wire.color,
            type=wire.type,
            subtype=wire.subtype,
            image=wire.image,
            notes=wire.notes,
            additional_components=list(getattr(wire, "additional_components", [])),
            bgcolor=wire.bgcolor,
            bgcolor_title=wire.bgcolor_title,
            show_name=wire.show_name,
            gauge=wire.gauge,
            length=wire.length,
            ignore_in_bom=wire.ignore_in_bom,
            show_equiv=wire.show_equiv,
            category=wire.category,
        )


class ShieldModel(WireModel):
    """Pydantic representation for ShieldClass with conversion helpers."""

    def to_wireclass(self) -> ShieldClass:
        return ShieldClass(
            designator=self.designator,
            parent=self.parent,
            index=self.index,
            id=self.id,
            label=self.label or "Shield",
            color=self.color,
            type=self.type,
            subtype=self.subtype,
            image=self.image,
            notes=self.notes,
            additional_components=cast(List[WireClass], self.additional_components),
            bgcolor=self.bgcolor,
            bgcolor_title=self.bgcolor_title,
            show_name=self.show_name,
            gauge=self.gauge,
            length=self.length,
            ignore_in_bom=self.ignore_in_bom,
            show_equiv=self.show_equiv,
            category=self.category or BomCategory.WIRE,
        )

    @classmethod
    def from_wireclass(cls, wire: ShieldClass) -> "ShieldModel":
        return cls(
            designator=wire.designator,
            parent=wire.parent,
            index=wire.index,
            id=getattr(wire, "id", None),
            label=wire.label,
            color=wire.color,
            type=wire.type,
            subtype=wire.subtype,
            image=wire.image,
            notes=wire.notes,
            additional_components=list(getattr(wire, "additional_components", [])),
            bgcolor=wire.bgcolor,
            bgcolor_title=wire.bgcolor_title,
            show_name=wire.show_name,
            gauge=wire.gauge,
            length=wire.length,
            ignore_in_bom=wire.ignore_in_bom,
            show_equiv=wire.show_equiv,
            category=wire.category,
        )


__all__ = ["WireModel", "ShieldModel", "WireClass", "ShieldClass"]
