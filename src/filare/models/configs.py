from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

import factory  # type: ignore[reportPrivateImportUsage]
from factory import Factory  # type: ignore[reportPrivateImportUsage]
from factory.declarations import (  # type: ignore[reportPrivateImportUsage]
    LazyAttribute,
    Sequence,
    SubFactory,
)
from faker import Faker  # type: ignore[reportPrivateImportUsage]
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

faker = Faker()


class ConfigBaseModel(BaseModel):
    """Common base for YAML-facing configuration models."""

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)


class PinConfig(ConfigBaseModel):
    id: Optional[str] = None
    label: Optional[str] = None
    color: Optional[Union[str, List[str]]] = None
    note: Optional[str] = None


class ConnectorConfig(ConfigBaseModel):
    designator: str
    pincount: Optional[int] = None
    pins: Optional[List[PinConfig]] = None
    pinlabels: Optional[List[str]] = None
    pincolors: Optional[
        Union[List[Union[str, List[str]]], Dict[str, Union[str, List[str]]]]
    ] = None
    loops: Optional[List[Dict[str, Any]]] = None
    style: Optional[str] = None
    images: Optional[List[str]] = None
    notes: Optional[List[str]] = None

    @field_validator("pins", mode="before")
    def _coerce_pins(cls, value: Any) -> Any:
        if value is None:
            return value
        if isinstance(value, dict):
            return [value]
        return value

    @field_validator("loops", mode="before")
    def _ensure_loop_list(cls, value: Any) -> Any:
        if value is None:
            return value
        if isinstance(value, dict):
            return [value]
        return list(value)

    @model_validator(mode="before")
    def _set_pincount_from_inputs(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        if values.get("pincount") is None:
            pins = values.get("pins") or []
            pinlabels = values.get("pinlabels") or []
            if isinstance(pins, dict):
                pins = [pins]
            if isinstance(pinlabels, dict):
                pinlabels = list(pinlabels.values())
            if pins:
                values["pincount"] = len(pins)
            elif pinlabels:
                values["pincount"] = len(pinlabels)
        return values

    @field_validator("pincolors", mode="before")
    def _normalize_pincolors(cls, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, list):
            # flatten list-of-lists to per-pin colors
            return [v if isinstance(v, str) else list(v) for v in value]
        if isinstance(value, dict):
            return {k: (v if isinstance(v, str) else list(v)) for k, v in value.items()}
        return value


class WireConfig(ConfigBaseModel):
    label: Optional[str] = None
    color: Optional[Union[str, List[str]]] = None
    gauge: Optional[Any] = None
    length: Optional[Any] = None
    shield: Optional[Any] = None
    notes: Optional[List[str]] = None


class CableConfig(ConfigBaseModel):
    designator: str
    wirecount: Optional[int] = None
    colors: Optional[List[str]] = None
    shields: Optional[List[Any]] = None
    length: Optional[Any] = None
    wires: Optional[List[WireConfig]] = None
    notes: Optional[List[str]] = None
    style: Optional[str] = None

    @field_validator("colors", mode="before")
    def _coerce_colors(cls, value: Any) -> Any:
        if value is None:
            return value
        if isinstance(value, str):
            return [value]
        return list(value)

    @model_validator(mode="after")
    def _derive_wirecount(self):
        if self.wirecount is not None:
            return self
        if self.wires:
            self.wirecount = len(self.wires)
        elif self.colors:
            self.wirecount = len(self.colors)
        return self


class ConnectionConfig(ConfigBaseModel):
    endpoints: List[str]
    net: Optional[str] = None
    color: Optional[Union[str, List[str]]] = None
    wire: Optional[str] = None
    bundle: Optional[str] = None
    notes: Optional[List[str]] = None

    @field_validator("endpoints", mode="before")
    def _coerce_endpoints(cls, value: Any) -> List[str]:
        if isinstance(value, str):
            return [value]
        if isinstance(value, (tuple, set)):
            return list(value)
        return list(value)


class MetadataConfig(ConfigBaseModel):
    title: Optional[str] = None
    pn: Optional[str] = None
    company: Optional[str] = None
    address: Optional[str] = None
    output_dir: Optional[Any] = None
    output_name: Optional[str] = None
    files: List[str] = Field(default_factory=list)
    sheet_total: Optional[int] = None
    sheet_current: Optional[int] = None
    sheet_name: Optional[str] = None
    titlepage: Optional[Any] = None
    output_names: List[str] = Field(default_factory=list)
    authors: Dict[str, Any] = Field(default_factory=dict)
    revisions: Dict[str, Any] = Field(default_factory=dict)
    template: Optional[Dict[str, Any]] = None
    use_qty_multipliers: Optional[bool] = None
    multiplier_file_name: Optional[str] = None


class PageOptionsConfig(ConfigBaseModel):
    bgcolor: Optional[Any] = None
    bgcolor_connector: Optional[Any] = None
    bgcolor_overview: Optional[Any] = None
    connector_overview_style: Optional[str] = None
    overview_inherit_styles: Optional[bool] = None
    font: Optional[str] = None
    dpi: Optional[int] = None
    width_mm: Optional[float] = None
    margin_mm: Optional[float] = None
    formats: Optional[List[str]] = None

    @field_validator("formats", mode="before")
    def _coerce_formats(cls, value: Any) -> Any:
        if value is None:
            return value
        if isinstance(value, str):
            return [value]
        return list(value)


class FakePinConfigFactory(Factory):
    class Meta:
        model = PinConfig

    id = LazyAttribute(lambda _: faker.random_element(["1", "2", "A", "B"]))
    label = LazyAttribute(lambda _: faker.word())
    color = LazyAttribute(lambda _: ["RD", "BK"])
    note = LazyAttribute(lambda _: faker.sentence(nb_words=3))


class FakeConnectorConfigFactory(Factory):
    class Meta:
        model = ConnectorConfig

    designator = Sequence(lambda n: f"J{n+1}")
    pincount = 2
    pins = LazyAttribute(lambda _: [FakePinConfigFactory.create(), FakePinConfigFactory.create()])
    pinlabels = LazyAttribute(lambda obj: [pin.label for pin in obj.pins])
    pincolors = LazyAttribute(lambda _: [["RD"], ["BK"]])
    loops = LazyAttribute(lambda _: [{"first": "1", "second": "2"}])
    style = "default"
    images = LazyAttribute(lambda _: ["front.png"])
    notes = LazyAttribute(lambda _: ["note1"])


class FakeWireConfigFactory(Factory):
    class Meta:
        model = WireConfig

    label = LazyAttribute(lambda _: faker.word())
    color = LazyAttribute(lambda _: ["RD"])
    gauge = LazyAttribute(lambda _: "20 AWG")
    length = LazyAttribute(lambda _: "2 m")
    shield = False
    notes = LazyAttribute(lambda _: ["wire note"])


class FakeCableConfigFactory(Factory):
    class Meta:
        model = CableConfig

    designator = Sequence(lambda n: f"W{n+1}")
    wirecount = 2
    colors = LazyAttribute(lambda _: ["RD", "BK"])
    shields = LazyAttribute(lambda _: [])
    length = LazyAttribute(lambda _: "1 m")
    wires = LazyAttribute(lambda _: [FakeWireConfigFactory.create(), FakeWireConfigFactory.create()])
    notes = LazyAttribute(lambda _: ["cable note"])
    style = "default"


class FakeConnectionConfigFactory(Factory):
    class Meta:
        model = ConnectionConfig

    endpoints = LazyAttribute(lambda _: ["J1.1", "J2.1"])
    net = LazyAttribute(lambda _: faker.word())
    color = LazyAttribute(lambda _: ["RD"])
    wire = LazyAttribute(lambda _: "W1.1")
    bundle = None
    notes = LazyAttribute(lambda _: ["net note"])


class FakeMetadataConfigFactory(Factory):
    class Meta:
        model = MetadataConfig

    title = LazyAttribute(lambda _: faker.sentence(nb_words=3))
    pn = LazyAttribute(lambda _: faker.bothify("PN-####"))
    company = LazyAttribute(lambda _: faker.company())
    address = LazyAttribute(lambda _: faker.address())
    output_dir = LazyAttribute(lambda _: "outputs")
    output_name = LazyAttribute(lambda _: faker.slug())
    files = LazyAttribute(lambda _: ["file1", "file2"])
    sheet_total = 1
    sheet_current = 1
    sheet_name = LazyAttribute(lambda _: faker.word())
    titlepage = LazyAttribute(lambda _: "titlepage.svg")
    output_names = LazyAttribute(lambda _: ["out.svg"])
    authors = LazyAttribute(lambda _: {"created": {"name": faker.name()}})
    revisions = LazyAttribute(lambda _: {"A": {"name": faker.name()}})
    template = LazyAttribute(lambda _: {"name": "din-6771"})
    use_qty_multipliers = False
    multiplier_file_name = "mult.txt"


class FakePageOptionsConfigFactory(Factory):
    class Meta:
        model = PageOptionsConfig

    bgcolor = "WH"
    bgcolor_connector = "WH"
    bgcolor_overview = "WH"
    connector_overview_style = "simple"
    overview_inherit_styles = True
    font = "arial"
    dpi = 96
    width_mm = 200.0
    margin_mm = 10.0
    formats = LazyAttribute(lambda _: ["svg", "pdf"])


__all__ = [
    "ConfigBaseModel",
    "PinConfig",
    "ConnectorConfig",
    "WireConfig",
    "CableConfig",
    "ConnectionConfig",
    "MetadataConfig",
    "PageOptionsConfig",
    "FakePinConfigFactory",
    "FakeConnectorConfigFactory",
    "FakeWireConfigFactory",
    "FakeCableConfigFactory",
    "FakeConnectionConfigFactory",
    "FakeMetadataConfigFactory",
    "FakePageOptionsConfigFactory",
]
