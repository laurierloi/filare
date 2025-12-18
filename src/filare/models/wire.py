"""Pydantic shims for wire-related dataclasses."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Type, Union, cast

import factory  # type: ignore[reportPrivateImportUsage]
from factory import Factory  # type: ignore[reportPrivateImportUsage]
from factory.declarations import (  # type: ignore[reportPrivateImportUsage]
    LazyAttribute,
    Sequence,
)
from faker import Faker  # type: ignore[reportPrivateImportUsage]
from pydantic import BaseModel, ConfigDict, Field, field_validator

from filare.models.colors import (
    FakeMultiColorFactory,
    FakeSingleColorFactory,
    MultiColor,
    SingleColor,
)
from filare.models.component import FakeComponentModelFactory
from filare.models.hypertext import MultilineHypertext
from filare.models.image import Image
from filare.models.numbers import NumberAndUnit
from filare.models.types import BomCategory

if TYPE_CHECKING:
    from filare.models.dataclasses import ShieldClass as ShieldClassType
    from filare.models.dataclasses import WireClass as WireClassType
else:  # pragma: no cover
    ShieldClassType = WireClassType = Any  # type: ignore

# Compatibility dataclass aliases
try:  # pragma: no cover
    from filare.models.dataclasses import ShieldClass as ShieldClassDC  # noqa: F401
    from filare.models.dataclasses import WireClass as WireClassDC
except Exception:  # pragma: no cover
    ShieldClassDC = WireClassDC = None  # type: ignore

WireClass = cast(Type[WireClassType], WireClassDC)
ShieldClass = cast(Type[ShieldClassType], ShieldClassDC)
faker = Faker()


class WireModel(BaseModel):
    """Pydantic representation mirroring WireClass fields."""

    designator: str = ""
    parent: Optional[str] = None
    index: Optional[int] = None
    id: Optional[str] = None
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

    @field_validator("id", mode="before")
    def _coerce_id(cls, value: Any) -> Optional[str]:
        if value is None:
            return None
        return str(value)

    def to_wireclass(self) -> WireClassType:
        if WireClassDC is None:  # pragma: no cover
            raise TypeError("WireClass dataclass not available")
        wire_class = cast(Type[WireClassType], WireClassDC)
        return wire_class(
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
            additional_components=cast(List[Any], self.additional_components),
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
    def from_wireclass(cls, wire: WireClassType) -> "WireModel":
        if WireClassDC is None:  # pragma: no cover
            raise TypeError("WireClass dataclass not available")
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

    def to_wireclass(self) -> ShieldClassType:
        if ShieldClassDC is None:  # pragma: no cover
            raise TypeError("ShieldClass dataclass not available")
        shield_class = cast(Type[ShieldClassType], ShieldClassDC)
        return shield_class(
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
            additional_components=cast(List[Any], self.additional_components),
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
    def from_wireclass(cls, wire: ShieldClassType) -> "ShieldModel":
        if ShieldClassDC is None:  # pragma: no cover
            raise TypeError("ShieldClass dataclass not available")
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


class FakeWireModelFactory(Factory):
    """factory_boy factory for WireModel."""

    class Meta:
        model = WireModel

    class Params:
        with_additional = False
        with_bg = False
        with_colors = True
        with_gauge = True
        with_length = True

    designator = Sequence(lambda n: f"W{n+1}")
    parent = LazyAttribute(lambda obj: obj.designator.replace("W", "C", 1))
    index = Sequence(lambda n: n)
    id = LazyAttribute(lambda obj: f"{obj.designator.lower()}-{obj.index}")
    label = LazyAttribute(lambda _: faker.word())
    color = LazyAttribute(
        lambda obj: FakeMultiColorFactory.create() if obj.with_colors else None
    )
    type = LazyAttribute(lambda _: MultilineHypertext.to(faker.word()))
    subtype = LazyAttribute(lambda _: MultilineHypertext.to(faker.word()))
    image = None
    notes = LazyAttribute(lambda _: MultilineHypertext.to(" ".join(faker.words(3))))
    additional_components = LazyAttribute(
        lambda obj: (
            [
                FakeComponentModelFactory.create(
                    category=BomCategory.ADDITIONAL, parent=obj.designator
                ).to_component()
            ]
            if obj.with_additional
            else []
        )
    )
    bgcolor = LazyAttribute(
        lambda obj: FakeSingleColorFactory.create() if obj.with_bg else None
    )
    bgcolor_title = LazyAttribute(
        lambda obj: FakeSingleColorFactory.create() if obj.with_bg else None
    )
    show_name = LazyAttribute(lambda _: bool(faker.boolean()))
    gauge = LazyAttribute(
        lambda obj: (
            NumberAndUnit.to_number_and_unit(f"{faker.random_int(min=18, max=26)} AWG")
            if obj.with_gauge
            else None
        )
    )
    length = LazyAttribute(
        lambda obj: (
            NumberAndUnit.to_number_and_unit(f"{faker.random_int(min=1, max=5)} m")
            if obj.with_length
            else None
        )
    )
    ignore_in_bom = LazyAttribute(lambda _: bool(faker.boolean()))
    show_equiv = LazyAttribute(lambda _: bool(faker.boolean()))
    category = BomCategory.WIRE

    @staticmethod
    def create(**kwargs: Any) -> WireModel:
        return FakeWireModelFactory.build(**kwargs)


class FakeShieldModelFactory(FakeWireModelFactory):
    """factory_boy factory for ShieldModel."""

    class Meta:
        model = ShieldModel

    label = LazyAttribute(lambda _: "Shield")
    category = BomCategory.WIRE

    @staticmethod
    def create(**kwargs: Any) -> ShieldModel:
        return FakeShieldModelFactory.build(**kwargs)


__all__ = [
    "WireModel",
    "ShieldModel",
    "WireClass",
    "ShieldClass",
    "FakeWireModelFactory",
    "FakeShieldModelFactory",
]
