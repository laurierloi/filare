from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Extra, Field, root_validator, validator


class ConfigBaseModel(BaseModel):
    """Common base for YAML-facing configuration models."""

    class Config:
        extra = Extra.allow
        allow_mutation = True
        arbitrary_types_allowed = True


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

    @root_validator(pre=True)
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

    @validator("pins", pre=True)
    def _coerce_pins(cls, value: Any) -> Any:
        if value is None:
            return value
        if isinstance(value, dict):
            return [value]
        return value

    @validator("loops", pre=True)
    def _ensure_loop_list(cls, value: Any) -> Any:
        if value is None:
            return value
        if isinstance(value, dict):
            return [value]
        return list(value)

    @validator("pincount", pre=True, always=True)
    def _derive_pincount(
        cls, value: Optional[int], values: Dict[str, Any]
    ) -> Optional[int]:
        if value is not None:
            return value
        pins = values.get("pins")
        if pins:
            return len(pins)
        pinlabels = values.get("pinlabels")
        if pinlabels:
            return len(pinlabels)
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

    @validator("colors", pre=True)
    def _coerce_colors(cls, value: Any) -> Any:
        if value is None:
            return value
        if isinstance(value, str):
            return [value]
        return list(value)

    @validator("wirecount", always=True)
    def _derive_wirecount(
        cls, value: Optional[int], values: Dict[str, Any]
    ) -> Optional[int]:
        if value is not None:
            return value
        wires = values.get("wires")
        if wires:
            return len(wires)
        colors = values.get("colors")
        if colors:
            return len(colors)
        return value


class ConnectionConfig(ConfigBaseModel):
    endpoints: List[str]
    net: Optional[str] = None
    color: Optional[Union[str, List[str]]] = None
    wire: Optional[str] = None
    bundle: Optional[str] = None
    notes: Optional[List[str]] = None

    @validator("endpoints", pre=True)
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

    @validator("formats", pre=True)
    def _coerce_formats(cls, value: Any) -> Any:
        if value is None:
            return value
        if isinstance(value, str):
            return [value]
        return list(value)
