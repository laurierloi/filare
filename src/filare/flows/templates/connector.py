"""Helpers to build connector template models from connector data."""

from __future__ import annotations

from typing import Any, Iterable, List, Optional, Sequence, Union

from filare.models.colors import MultiColor, SingleColor
from filare.models.connector import ConnectorModel
from filare.models.hypertext import MultilineHypertext
from filare.models.templates.connector_template_model import (
    ConnectorTemplateModel,
    TemplateConnectorComponent,
    TemplateConnectorPin,
    TemplateMultiColor,
)
from filare.models.templates.simple_connector_template_model import (
    SimpleConnectorTemplateModel,
)


def _to_multicolor(value: Any) -> Optional[TemplateMultiColor]:
    if value is None:
        return None
    if isinstance(value, TemplateMultiColor):
        return value
    if isinstance(value, MultiColor):
        return TemplateMultiColor(colors=value.colors)
    if isinstance(value, str):
        return TemplateMultiColor(colors=[SingleColor(value)])
    try:
        return TemplateMultiColor(colors=[SingleColor(v) for v in value])  # type: ignore[arg-type]
    except Exception:
        return None


def _build_pins(
    pins: Sequence[Any],
    pinlabels: Sequence[Any],
    pincolors: Sequence[Any],
) -> List[TemplateConnectorPin]:
    built: List[TemplateConnectorPin] = []
    for idx, pin in enumerate(pins):
        pin_id = str(getattr(pin, "id", pin))
        label = pinlabels[idx] if idx < len(pinlabels) else None
        color_val = pincolors[idx] if idx < len(pincolors) else None
        color = _to_multicolor(color_val)
        built.append(
            TemplateConnectorPin(id=pin_id, index=idx, label=label, color=color)
        )
    return built


def build_connector_model(
    connector: Union[ConnectorModel, Any],
) -> Union[ConnectorTemplateModel, SimpleConnectorTemplateModel]:
    """Construct a connector template model (simple or full) from connector data."""
    # Normalize to ConnectorModel for consistent field access when possible.
    if not isinstance(connector, ConnectorModel):
        try:
            connector = ConnectorModel(**getattr(connector, "__dict__", {}))  # type: ignore[assignment]
        except Exception:
            # Fallback: minimal mapping from attributes.
            connector = ConnectorModel(
                designator=str(getattr(connector, "designator", "")),
                type=getattr(connector, "type", None),
                subtype=getattr(connector, "subtype", None),
                color=getattr(connector, "color", None),
                pins=getattr(connector, "pins", []),
                pinlabels=getattr(connector, "pinlabels", []),
                pincolors=getattr(connector, "pincolors", []),
                pincount=getattr(connector, "pincount", None),
                loops=getattr(connector, "loops", []),
                style=getattr(connector, "style", None),
                additional_components=getattr(connector, "additional_components", []),
                notes=getattr(connector, "notes", None),
            )

    pins = connector.pins or []
    pinlabels = connector.pinlabels or []
    pincolors = connector.pincolors or []
    component = TemplateConnectorComponent(
        designator=str(connector.designator),
        type=(
            MultilineHypertext.to(connector.type)
            if connector.type
            else MultilineHypertext.to("")
        ),
        subtype=MultilineHypertext.to(connector.subtype) if connector.subtype else None,
        color=_to_multicolor(connector.color),
        show_pincount=True,
        pincount=connector.pincount or len(pins),
        ports_left=getattr(connector, "ports_left", True),
        ports_right=getattr(connector, "ports_right", True),
        has_pincolors=bool(pincolors),
        pins=_build_pins(pins, pinlabels, pincolors),
        partnumbers=getattr(connector, "partnumbers", None),
        image=getattr(connector, "image", None),
        additional_components=getattr(connector, "additional_components", []),
        notes=MultilineHypertext.to(connector.notes) if connector.notes else None,
    )

    if getattr(connector, "style", None) == "simple":
        return SimpleConnectorTemplateModel(component=component)
    return ConnectorTemplateModel(component=component)
