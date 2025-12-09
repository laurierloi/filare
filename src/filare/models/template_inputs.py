from __future__ import annotations

from typing import List, Optional, Sequence, Union

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from filare.errors import ComponentValidationError
from filare.models.configs import (
    CableConfig,
    ConnectionConfig,
    ConnectorConfig,
    WireConfig,
)
from filare.models.numbers import NumberAndUnit


class TemplateBaseModel(BaseModel):
    """Base class for template-facing inputs."""

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    @classmethod
    def model_validate(cls, *args, **kwargs):
        try:
            return super().model_validate(*args, **kwargs)
        except ValidationError as exc:
            raise ComponentValidationError(f"{cls.__name__}: {exc}") from exc

    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValidationError as exc:
            errors = exc.errors()
            message = errors[0].get("msg", str(exc)) if errors else str(exc)
            message = f"{self.__class__.__name__}: {message}"
            raise ComponentValidationError(message) from exc


def _to_color_list(value: Optional[Union[str, Sequence[str]]]) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return list(value)


class TemplatePin(TemplateBaseModel):
    label: Optional[str] = None
    color: List[str] = Field(default_factory=list)
    id: Optional[str] = None

    @field_validator("color", mode="before")
    def _coerce_color(cls, value: Optional[Union[str, Sequence[str]]]) -> List[str]:
        return _to_color_list(value)


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
            pins = [
                TemplatePin(label=p.label, color=_to_color_list(p.color), id=p.id)
                for p in cfg.pins
            ]
        elif cfg.pinlabels:
            colors = cfg.pincolors or []
            if isinstance(colors, dict):
                color_values = list(colors.values())
            else:
                color_values = colors
            for idx, label in enumerate(cfg.pinlabels):
                color_entry = color_values[idx] if idx < len(color_values) else []
                pins.append(TemplatePin(label=label, color=_to_color_list(color_entry)))
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

    @field_validator("color", mode="before")
    def _coerce_color(cls, value: Optional[Union[str, Sequence[str]]]) -> List[str]:
        return _to_color_list(value)

    @field_validator("length", mode="before")
    def _coerce_length(
        cls, value: Union[str, NumberAndUnit, None]
    ) -> Optional[NumberAndUnit]:
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
                        color=_to_color_list(wire.color),
                        length=wire.length,
                    )
                )
        elif cfg.colors:
            for color in cfg.colors:
                wires.append(TemplateWire(color=_to_color_list(color)))
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

    @field_validator("endpoints", mode="before")
    def _coerce_endpoints(cls, value: Union[str, Sequence[str]]) -> List[str]:
        if isinstance(value, str):
            return [value]
        return list(value)

    @field_validator("color", mode="before")
    def _coerce_color(cls, value: Optional[Union[str, Sequence[str]]]) -> List[str]:
        return _to_color_list(value)

    @classmethod
    def from_config(cls, cfg: ConnectionConfig) -> "TemplateConnection":
        return cls(
            endpoints=cfg.endpoints,
            net=cfg.net,
            color=_to_color_list(cfg.color),
        )
