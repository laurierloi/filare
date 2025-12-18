from __future__ import annotations

from typing import Any, Dict

from pydantic import Field

from filare.models.interface.base import FilareInterfaceModel


class InterfaceConfigCollection(FilareInterfaceModel):
    """Container for per-interface-type configuration dictionaries."""

    connector: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    cable: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    connection: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    options: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    metadata: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    harness: Dict[str, Dict[str, Any]] = Field(default_factory=dict)


class InterfaceConfigurationModel(FilareInterfaceModel):
    """Top-level configuration spanning all interface types and levels."""

    global_config: Dict[str, Any] = Field(
        default_factory=dict,
        alias="global",
        description="Global config applied to all interface types.",
    )
    default: InterfaceConfigCollection = Field(
        default_factory=InterfaceConfigCollection,
        description="Default configs per interface type.",
    )
    type: InterfaceConfigCollection = Field(
        default_factory=InterfaceConfigCollection,
        description="Named configs per interface type.",
    )
    item: InterfaceConfigCollection = Field(
        default_factory=InterfaceConfigCollection,
        description="Item-level configs per interface type keyed by interface id.",
    )
