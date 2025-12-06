"""Pydantic adapters for pin/loop/connection dataclasses."""

from __future__ import annotations

import logging
from typing import Any, Optional, Union

from pydantic import BaseModel, ConfigDict, field_validator

from filare.models.colors import MultiColor
from filare.models.dataclasses import Connection, Loop, PinClass
from filare.models.types import Side


class PinModel(BaseModel):
    """Pydantic mirror of PinClass to ease migration away from dataclasses."""

    index: Optional[int] = None
    id: Optional[Union[int, str]] = None
    label: str = ""
    color: Optional[MultiColor] = None
    parent: Optional[str] = None
    _anonymous: bool = False
    _simple: bool = False

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    @field_validator("color", mode="before")
    def _coerce_color(cls, value: Any):
        if value is None:
            return None
        return MultiColor(value)

    @classmethod
    def from_pinclass(cls, pin: PinClass) -> "PinModel":
        return cls(
            index=pin.index,
            id=pin.id,
            label=pin.label,
            color=pin.color,
            parent=pin.parent,
            _anonymous=pin._anonymous,
            _simple=pin._simple,
        )

    def to_pinclass(self) -> PinClass:
        return PinClass(
            index=self.index or 0,
            id=self.id or "",
            label=self.label,
            color=self.color,
            parent=self.parent or "",
            _anonymous=self._anonymous,
            _simple=self._simple,
        )


class LoopModel(BaseModel):
    """Pydantic mirror of Loop for safer transport and manipulation."""

    first: Union[PinModel, PinClass, Any]
    second: Union[PinModel, PinClass, Any]
    side: Optional[Union[Side, str]] = None
    show_label: bool = True
    color: Optional[MultiColor] = None

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    @field_validator("side", mode="before")
    def _coerce_side(cls, value: Any):
        if value is None:
            return None
        if isinstance(value, Side):
            return value
        value_str = str(value).upper()
        for name in ("LEFT", "RIGHT"):
            if name in value_str:
                try:
                    return Side[name]
                except Exception as exc:
                    logging.debug("Failed to coerce side %r; ignoring. error=%s", value, exc)
                    continue
        return None

    @field_validator("color", mode="before")
    def _coerce_color(cls, value: Any):
        if value is None:
            return None
        return MultiColor(value)

    @field_validator("first", "second", mode="before")
    def _coerce_pin(cls, value: Any):
        if value is None:
            return value
        if isinstance(value, PinModel):
            return value
        if isinstance(value, PinClass):
            return PinModel.from_pinclass(value)
        if isinstance(value, dict):
            return PinModel(**value)
        return value

    def to_loop(self) -> Loop:
        first_pin = (
            self.first.to_pinclass() if isinstance(self.first, PinModel) else self.first
        )
        second_pin = (
            self.second.to_pinclass()
            if isinstance(self.second, PinModel)
            else self.second
        )
        side_val = self.side.name if isinstance(self.side, Side) else self.side
        return Loop(
            first=first_pin,
            second=second_pin,
            side=side_val,
            show_label=self.show_label,
            color=self.color,
        )

    @classmethod
    def from_loop(cls, loop: Loop) -> "LoopModel":
        return cls(
            first=PinModel.from_pinclass(loop.first),
            second=PinModel.from_pinclass(loop.second),
            side=loop.side,
            show_label=loop.show_label,
            color=loop.color,
        )


class ConnectionModel(BaseModel):
    """Pydantic mirror of Connection for later flow refactors."""

    from_: Optional[Union[PinModel, PinClass, Any]] = None
    via: Optional[Union[PinModel, PinClass, Any]] = None
    to: Optional[Union[PinModel, PinClass, Any]] = None

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    @field_validator("from_", "via", "to", mode="before")
    def _coerce_pin(cls, value: Any):
        if value is None:
            return None
        if isinstance(value, PinModel):
            return value
        if isinstance(value, PinClass):
            return PinModel.from_pinclass(value)
        if isinstance(value, dict):
            return PinModel(**value)
        return value

    def to_connection(self) -> Connection:
        def _cast(val):
            if val is None:
                return None
            if isinstance(val, PinModel):
                return val.to_pinclass()
            return val

        return Connection(
            from_=_cast(self.from_),
            via=_cast(self.via),
            to=_cast(self.to),
        )

    @classmethod
    def from_connection(cls, connection: Connection) -> "ConnectionModel":
        return cls(
            from_=(
                PinModel.from_pinclass(connection.from_) if connection.from_ else None
            ),
            via=(PinModel.from_pinclass(connection.via) if connection.via else None),
            to=PinModel.from_pinclass(connection.to) if connection.to else None,
        )


__all__ = ["PinModel", "LoopModel", "ConnectionModel"]
