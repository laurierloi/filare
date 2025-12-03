from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


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
    pincolors: Optional[Union[List[str], Dict[str, str]]] = None
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
