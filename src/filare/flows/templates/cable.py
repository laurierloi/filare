"""Helpers to build cable template models from cable data."""

from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence, Union

from filare.models.colors import MultiColor, SingleColor
from filare.models.hypertext import MultilineHypertext
from filare.models.templates.cable_template_model import (
    CableTemplateModel,
    TemplateCableComponent,
    TemplateWire,
)


def _to_multicolor(value: Any) -> Union[MultiColor, None]:
    if value is None:
        return None
    if isinstance(value, MultiColor):
        return value
    if isinstance(value, str):
        return MultiColor(value)
    try:
        return MultiColor(list(value))  # type: ignore[arg-type]
    except Exception:
        return None


def _build_wires(wires: Mapping[str, Any]) -> Dict[str, TemplateWire]:
    built: Dict[str, TemplateWire] = {}
    for key, wire in wires.items():
        color_val = getattr(wire, "color", None) if hasattr(wire, "color") else wire.get("color")  # type: ignore[assignment]
        color = (
            color_val
            if isinstance(color_val, SingleColor)
            else SingleColor(inp=str(color_val or ""))
        )
        is_shield = getattr(wire, "category", "") == "shield" if hasattr(wire, "category") else wire.get("category") == "shield"  # type: ignore[assignment]
        built[key] = TemplateWire(
            id=str(getattr(wire, "designator", key)),
            port=str(getattr(wire, "port", f"p{key}")),
            color=color,
            is_shield=is_shield,
            partnumbers=(
                getattr(wire, "partnumbers", None)
                if hasattr(wire, "partnumbers")
                else wire.get("partnumbers")
            ),  # type: ignore[assignment]
        )
    return built


def build_cable_model(cable: Any) -> CableTemplateModel:
    """Construct a CableTemplateModel from cable data."""
    wire_objects = getattr(cable, "wire_objects", None) or getattr(cable, "wires", {})
    component = TemplateCableComponent(
        designator=str(getattr(cable, "designator", "")),
        type=str(getattr(cable, "type", "") or "cable"),
        show_wirecount=True,
        wirecount=int(getattr(cable, "wirecount", len(wire_objects) or 1)),
        gauge_str_with_equiv=str(getattr(cable, "gauge_str_with_equiv", "") or ""),
        shield=bool(getattr(cable, "shield", False)),
        length_str=str(
            getattr(cable, "length", "") or getattr(cable, "length_str", "") or ""
        ),
        color=_to_multicolor(getattr(cable, "color", None)),
        partnumbers=getattr(cable, "partnumbers", None),
        wire_objects=(
            _build_wires(wire_objects) if isinstance(wire_objects, dict) else {}
        ),
        image=getattr(cable, "image", None),
        additional_components=getattr(cable, "additional_components", []),
        notes=str(getattr(cable, "notes", None) or ""),
    )
    return CableTemplateModel(component=component)
