"""Helpers to build cable template models from cable data."""

from __future__ import annotations

from typing import Any, Dict, Mapping, Sequence, Union

from filare.models.colors import MultiColor, SingleColor
from filare.models.hypertext import MultilineHypertext
from filare.models.partnumber import PartNumberInfo, PartnumberInfoList
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


def _to_partnumber_list(value: Any) -> Union[PartnumberInfoList, None]:
    """Coerce incoming partnumber data to PartnumberInfoList, skipping None entries."""
    if value is None:
        return None
    if isinstance(value, PartnumberInfoList):
        return value
    try:
        if isinstance(value, PartNumberInfo):
            return PartnumberInfoList(pn_list=[value])
        if isinstance(value, (list, tuple)):
            pn_items: list[PartNumberInfo] = []
            for item in value:
                if item is None:
                    continue
                if isinstance(item, PartNumberInfo):
                    pn_items.append(item)
                elif isinstance(item, dict):
                    pn_items.append(PartNumberInfo(**item))
                else:
                    pn_items.append(PartNumberInfo(pn=str(item)))
            return PartnumberInfoList(pn_list=pn_items) if pn_items else None
        if isinstance(value, dict):
            return PartnumberInfoList(pn_list=[PartNumberInfo(**value)])
        return PartnumberInfoList(pn_list=[PartNumberInfo(pn=str(value))])
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
        partnumbers_val = _to_partnumber_list(
            getattr(wire, "partnumbers", None)
            if hasattr(wire, "partnumbers")
            else wire.get("partnumbers")
        )
        built[str(key)] = TemplateWire(
            id=str(getattr(wire, "designator", key)),
            port=str(getattr(wire, "port", f"p{key}")),
            color=color,
            is_shield=is_shield,
            partnumbers=partnumbers_val,
        )
    return built


def build_cable_model(cable: Any) -> CableTemplateModel:
    """Construct a CableTemplateModel from cable data."""
    wire_objects = getattr(cable, "wire_objects", None) or getattr(cable, "wires", {})
    partnumbers_val = _to_partnumber_list(getattr(cable, "partnumbers", None))
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
        partnumbers=partnumbers_val,
        wire_objects=(
            _build_wires(wire_objects) if isinstance(wire_objects, dict) else {}
        ),
        image=getattr(cable, "image", None),
        additional_components=getattr(cable, "additional_components", []),
        notes=MultilineHypertext.to(getattr(cable, "notes", None)),
    )
    return CableTemplateModel(component=component)
