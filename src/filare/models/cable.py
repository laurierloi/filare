"""Cable and wire models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union, cast

import factory  # type: ignore[reportPrivateImportUsage]
from factory import Factory  # type: ignore[reportPrivateImportUsage]
from factory.declarations import LazyAttribute
from factory.declarations import (
    Sequence as FactorySequence,  # type: ignore[reportPrivateImportUsage]
)
from faker import Faker  # type: ignore[reportPrivateImportUsage]
from pydantic import Field, field_validator, model_validator

from filare.models.colors import (
    FakeMultiColorFactory,
    FakeSingleColorFactory,
    MultiColor,
    SingleColor,
    get_color_by_colorcode_index,
)
from filare.models.component import FakeComponentModelFactory
from filare.models.connector import GraphicalComponentModel
from filare.models.hypertext import FakeMultilineHypertextFactory, MultilineHypertext
from filare.models.image import Image
from filare.models.numbers import NumberAndUnit
from filare.models.types import BomCategory, QtyMultiplierCable  # noqa: F401
from filare.models.wire import FakeShieldModelFactory, FakeWireModelFactory, WireModel

if TYPE_CHECKING:  # pragma: no cover
    from filare.models.dataclasses import Cable as CableDC
    from filare.models.dataclasses import Connection as ConnectionDC
    from filare.models.dataclasses import ShieldClass as ShieldClassDC
    from filare.models.dataclasses import WireClass as WireClassDC
else:  # pragma: no cover
    try:
        from filare.models.dataclasses import Cable as CableDC
        from filare.models.dataclasses import Connection as ConnectionDC
        from filare.models.dataclasses import ShieldClass as ShieldClassDC
        from filare.models.dataclasses import WireClass as WireClassDC
    except Exception:
        CableDC = ConnectionDC = ShieldClassDC = WireClassDC = None  # type: ignore

Cable = CableDC  # type: ignore
Connection = ConnectionDC  # type: ignore
ShieldClass = ShieldClassDC  # type: ignore
WireClass = WireClassDC  # type: ignore
# Faker instance for factories
faker = Faker()


class CableModel(GraphicalComponentModel):
    wirecount: Optional[int] = None
    shield: Union[bool, str, MultiColor] = False
    colors: List[str] = Field(default_factory=list)
    color_code: Optional[str] = None
    wirelabels: List[Any] = Field(default_factory=list)
    wires: List[Any] = Field(default_factory=list)
    gauge: Optional[Union[str, NumberAndUnit]] = None
    length: Optional[Union[str, NumberAndUnit]] = None
    show_wirecount: bool = True
    show_equiv: bool = False

    @field_validator("colors", mode="before")
    def _coerce_colors(cls, value: Any) -> List[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        return [str(v) for v in value]

    @field_validator("wirelabels", mode="before")
    def _coerce_wirelabels(cls, value: Any) -> List[Any]:
        if value is None:
            return []
        return list(value)

    @field_validator("gauge", "length", mode="before")
    def _coerce_number_unit(cls, value: Any) -> Optional[NumberAndUnit]:
        if value is None:
            return None
        return NumberAndUnit.to_number_and_unit(value)

    @field_validator("shield", mode="before")
    def _coerce_shield(cls, value: Any):
        if value is None:
            return False
        if isinstance(value, str):
            return value
        return value

    @model_validator(mode="after")
    def _ensure_colors(self):
        colors: List[str] = list(self.colors or [])
        wirecount = self.wirecount or (len(colors) if colors else None)
        color_code = self.color_code
        color = self.color
        if not colors and wirecount:
            if color_code:
                colors = [
                    get_color_by_colorcode_index(color_code, i)
                    for i in range(wirecount)
                ]
            elif color:
                multicolor = MultiColor(color)
                colors = [str(multicolor[i]) for i in range(wirecount)]
            else:
                colors = ["" for _ in range(wirecount)]
        self.colors = colors
        return self

    def to_cable(self) -> Cable:
        if CableDC is None:  # pragma: no cover
            raise TypeError("Cable dataclass not available")
        type_value = cast(Optional[MultilineHypertext], self.type)
        subtype_value = cast(Optional[MultilineHypertext], self.subtype)
        color_value = cast(Optional[MultiColor], self.color)
        image_value = cast(Optional[Image], self.image)
        notes_value = cast(Optional[MultilineHypertext], self.notes)
        additional_components = cast(List[Any], self.additional_components)
        bgcolor_value = cast(Optional[SingleColor], self.bgcolor)
        bgcolor_title_value = cast(Optional[SingleColor], self.bgcolor_title)
        show_name_value = cast(Optional[bool], self.show_name)
        shield_value: Union[bool, MultiColor] = (
            self.shield
            if isinstance(self.shield, (bool, MultiColor))
            else MultiColor(self.shield)
        )
        return CableDC(
            designator=self.designator,
            type=type_value,
            subtype=subtype_value,
            color=color_value,
            image=image_value,
            notes=notes_value,
            additional_components=additional_components,
            bgcolor=bgcolor_value,
            bgcolor_title=bgcolor_title_value,
            show_name=show_name_value,
            wirecount=self.wirecount,
            shield=shield_value,
            colors=self.colors,
            color_code=self.color_code,
            wirelabels=self.wirelabels,
            gauge=cast(Optional[NumberAndUnit], self.gauge),
            length=cast(Optional[NumberAndUnit], self.length),
            show_wirecount=self.show_wirecount,
            show_equiv=self.show_equiv,
            category=BomCategory.CABLE,
        )


class FakeCableModelFactory(Factory):
    """factory_boy factory for CableModel."""

    class Meta:
        model = CableModel

    class Params:
        wire_count = 2
        with_wires = False
        with_shield = False
        with_bg = False
        with_color = True
        with_additional = False
        color_code_override: Optional[str] = "TEL"

    designator = FactorySequence(lambda n: f"W{n+1}")
    category = LazyAttribute(lambda _: BomCategory.CABLE)
    wirecount = LazyAttribute(lambda obj: obj.wire_count)
    color = LazyAttribute(
        lambda obj: FakeMultiColorFactory.create() if obj.with_color else None
    )
    colors = LazyAttribute(
        lambda obj: (
            (
                [
                    str(color.code_en or color.html or "RD")
                    for color in (
                        FakeMultiColorFactory.create(
                            count=obj.wire_count, color_code=obj.color_code_override
                        ).colors
                        or []
                    )
                ]
                or ["RD" for _ in range(obj.wire_count)]
            )
            if obj.with_color
            else ["" for _ in range(obj.wire_count)]
        )
    )
    color_code = LazyAttribute(lambda obj: obj.color_code_override)
    wirelabels = LazyAttribute(lambda obj: [f"L{i+1}" for i in range(obj.wire_count)])
    gauge = LazyAttribute(
        lambda _: NumberAndUnit(faker.random_int(min=18, max=26), "AWG")
    )
    length = LazyAttribute(lambda _: NumberAndUnit(faker.random_int(min=1, max=5), "m"))
    notes = LazyAttribute(lambda _: FakeMultilineHypertextFactory.create(lines=1))
    show_wirecount = LazyAttribute(lambda _: faker.boolean())
    show_equiv = LazyAttribute(lambda _: faker.boolean())
    shield = LazyAttribute(
        lambda obj: FakeMultiColorFactory.create() if obj.with_shield else False
    )
    wires = LazyAttribute(
        lambda obj: (
            [
                FakeWireModelFactory.create(
                    parent=obj.designator,
                    index=i,
                    color=FakeMultiColorFactory.create(),
                    gauge=NumberAndUnit(faker.random_int(min=18, max=26), "AWG"),
                    length=NumberAndUnit(faker.random_int(min=1, max=3), "m"),
                    label=f"L{i+1}",
                )
                for i in range(obj.wire_count)
            ]
            if obj.with_wires
            else []
        )
    )
    additional_components = LazyAttribute(
        lambda obj: (
            [FakeComponentModelFactory.create(category=BomCategory.ADDITIONAL)]
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

    @staticmethod
    def create(**kwargs: Any) -> CableModel:
        return FakeCableModelFactory.build(**kwargs)


__all__ = [
    "Cable",
    "Connection",
    "ShieldClass",
    "WireClass",
    "CableModel",
    "FakeCableModelFactory",
    "QtyMultiplierCable",
]
