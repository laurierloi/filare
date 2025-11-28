from __future__ import annotations

from typing import List, Optional, Sequence, Union

from pydantic import BaseModel, Extra, Field, validator

from wireviz.models.configs import CableConfig, ConnectorConfig, ConnectionConfig, WireConfig
from wireviz.models.numbers import NumberAndUnit


class TemplateBaseModel(BaseModel):
    """Base class for template-facing inputs."""

    class Config:
        extra = Extra.forbid
        arbitrary_types_allowed = True


class TemplatePin(TemplateBaseModel):
    label: Optional[str] = None
    color: List[str] = Field(default_factory=list)
    id: Optional[str] = None

    @validator("color", pre=True)
    def _coerce_color(cls, value: Union[str, Sequence[str]]) -> List[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        return list(value)


class TemplateConnector(TemplateBaseModel):
    designator: str
    pins: List[TemplatePin] = Field(default_factory=list)
    style: Optional[str] = None
    images: List[str] = Field(default_factory=list)
    loops: List[dict] = Field(default_factory=list)

    @classmethod
    def from_config(cls, cfg: ConnectorConfig) -> "TemplateConnector":
        pins: List[TemplatePin] = []
        if cfg.pins:
            pins = [TemplatePin(label=p.label, color=p.color or [], id=p.id) for p in cfg.pins]
        elif cfg.pinlabels:
            colors = cfg.pincolors or []
            for idx, label in enumerate(cfg.pinlabels):
                color = colors[idx] if idx < len(colors) else []
                pins.append(TemplatePin(label=label, color=color))
        return cls(
            designator=cfg.designator,
            pins=pins,
            style=cfg.style,
            images=cfg.images or [],
            loops=cfg.loops or [],
        )


class TemplateWire(TemplateBaseModel):
    label: Optional[str] = None
    color: List[str] = Field(default_factory=list)
    length: Optional[NumberAndUnit] = None

    @validator("color", pre=True)
    def _coerce_color(cls, value: Union[str, Sequence[str]]) -> List[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        return list(value)

    @validator("length", pre=True)
    def _coerce_length(cls, value: Union[str, NumberAndUnit, None]) -> Optional[NumberAndUnit]:
        if value is None:
            return None
        return NumberAndUnit.to_number_and_unit(value)


class TemplateCable(TemplateBaseModel):
    designator: str
    wires: List[TemplateWire] = Field(default_factory=list)
    length: Optional[NumberAndUnit] = None
    shields: List[dict] = Field(default_factory=list)

    @classmethod
    def from_config(cls, cfg: CableConfig) -> "TemplateCable":
        wires: List[TemplateWire] = []
        if cfg.wires:
            for wire in cfg.wires:
                wires.append(
                    TemplateWire(
                        label=wire.label,
                        color=wire.color or [],
                        length=wire.length,
                    )
                )
        elif cfg.colors:
            for color in cfg.colors:
                wires.append(TemplateWire(color=color))
        return cls(
            designator=cfg.designator,
            wires=wires,
            length=NumberAndUnit.to_number_and_unit(cfg.length) if cfg.length else None,
            shields=cfg.shields or [],
        )


class TemplateConnection(TemplateBaseModel):
    endpoints: List[str]
    net: Optional[str] = None
    color: List[str] = Field(default_factory=list)

    @validator("endpoints", pre=True)
    def _coerce_endpoints(cls, value: Union[str, Sequence[str]]) -> List[str]:
        if isinstance(value, str):
            return [value]
        return list(value)

    @validator("color", pre=True)
    def _coerce_color(cls, value: Union[str, Sequence[str]]) -> List[str]:
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        return list(value)

    @classmethod
    def from_config(cls, cfg: ConnectionConfig) -> "TemplateConnection":
        return cls(endpoints=cfg.endpoints, net=cfg.net, color=cfg.color or [])
