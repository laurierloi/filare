"""Pydantic adapters for pin/loop/connection dataclasses."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Optional, Union, cast

from pydantic import BaseModel, ConfigDict, field_validator

from filare.models.colors import MultiColor
from filare.models.types import Side
from filare.models.wire import ShieldModel, WireModel

if TYPE_CHECKING:
    from filare.models.dataclasses import Connection as ConnectionType
    from filare.models.dataclasses import Loop as LoopType
    from filare.models.dataclasses import PinClass as PinClassType
else:  # pragma: no cover
    ConnectionType = LoopType = PinClassType = Any  # type: ignore

try:  # pragma: no cover
    from filare.models.dataclasses import Connection as ConnectionDC
    from filare.models.dataclasses import Loop as LoopDC
    from filare.models.dataclasses import PinClass as PinClassDC
except Exception:  # pragma: no cover
    ConnectionDC = LoopDC = PinClassDC = None  # type: ignore

PinClass = cast(PinClassType, PinClassDC)
Loop = cast(LoopType, LoopDC)
Connection = cast(ConnectionType, ConnectionDC)


class PinModel(BaseModel):
    """Pydantic mirror of PinClass to ease migration away from dataclasses."""

    index: Optional[int] = None
    id: Optional[Union[int, str]] = None
    label: Optional[str] = None
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
    def from_pinclass(cls, pin: PinClassType) -> "PinModel":
        if PinClassDC is None:  # pragma: no cover
            raise TypeError("PinClass dataclass not available")
        return cls(
            index=pin.index,
            id=pin.id,
            label=pin.label,
            color=pin.color,
            parent=pin.parent,
            _anonymous=pin._anonymous,
            _simple=pin._simple,
        )

    def to_pinclass(self) -> PinClassType:
        if PinClassDC is None:  # pragma: no cover
            raise TypeError("PinClass dataclass not available")
        pin_class = cast(Any, PinClassDC)
        return pin_class(
            index=self.index or 0,
            id=self.id,
            label=self.label,
            color=self.color,
            parent=self.parent,
            _anonymous=self._anonymous,
            _simple=self._simple,
        )


class LoopModel(BaseModel):
    """Pydantic mirror of Loop for safer transport and manipulation."""

    first: Union[PinModel, PinClassType, Any]
    second: Union[PinModel, PinClassType, Any]
    side: Optional[Side] = None
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
                    logging.debug(
                        "Failed to coerce side %r; ignoring. error=%s", value, exc
                    )
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
        if PinClassDC and isinstance(value, PinClassDC):
            return PinModel.from_pinclass(value)
        if isinstance(value, dict):
            return PinModel(**value)
        return value

    def to_loop(self) -> LoopType:
        if LoopDC is None:  # pragma: no cover
            raise TypeError("Loop dataclass not available")
        first_pin = (
            self.first.to_pinclass() if isinstance(self.first, PinModel) else self.first
        )
        second_pin = (
            self.second.to_pinclass()
            if isinstance(self.second, PinModel)
            else self.second
        )
        loop_dc = cast(Any, LoopDC)
        return loop_dc(
            first=first_pin,
            second=second_pin,
            side=self.side,
            show_label=self.show_label,
            color=self.color,
        )

    @classmethod
    def from_loop(cls, loop: LoopType) -> "LoopModel":
        return cls(
            first=PinModel.from_pinclass(loop.first) if loop.first else None,
            second=PinModel.from_pinclass(loop.second) if loop.second else None,
            side=loop.side,
            show_label=loop.show_label,
            color=loop.color,
        )


class ConnectionModel(BaseModel):
    """Pydantic mirror of Connection for later flow refactors."""

    from_: Optional[Union[PinModel, PinClassType, WireModel, ShieldModel, Any]] = None
    via: Optional[Union[PinModel, PinClassType, WireModel, ShieldModel, Any]] = None
    to: Optional[Union[PinModel, PinClassType, WireModel, ShieldModel, Any]] = None

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    @field_validator("from_", "via", "to", mode="before")
    def _coerce_pin(cls, value: Any):
        if value is None:
            return None
        if isinstance(value, PinModel):
            return value
        if PinClassDC and isinstance(value, PinClassDC):
            return PinModel.from_pinclass(value)
        if isinstance(value, (WireModel, ShieldModel)):
            return value
        if isinstance(value, dict):
            return PinModel(**value)
        return value

    def to_connection(self) -> ConnectionType:
        if ConnectionDC is None:  # pragma: no cover
            raise TypeError("Connection dataclass not available")

        def _cast(val):
            if val is None:
                return None
            if isinstance(val, PinModel):
                return val.to_pinclass()
            if isinstance(val, (WireModel, ShieldModel)):
                return val.to_wireclass()
            return val

        connection_dc = cast(Any, ConnectionDC)
        return connection_dc(
            from_=_cast(self.from_),
            via=_cast(self.via),
            to=_cast(self.to),
        )

    @classmethod
    def from_connection(cls, connection: ConnectionType) -> "ConnectionModel":
        def _to_model(value: Any):
            if value is None:
                return None
            if PinClassDC and isinstance(value, PinClassDC):
                return PinModel.from_pinclass(value)
            return value

        return cls(
            from_=_to_model(connection.from_),
            via=_to_model(connection.via),
            to=_to_model(connection.to),
        )


__all__ = ["PinModel", "LoopModel", "ConnectionModel"]
