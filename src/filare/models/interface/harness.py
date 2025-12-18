from __future__ import annotations

from typing import Dict, List

from pydantic import Field, model_validator

from filare.models.interface.base import FilareInterfaceModel
from filare.models.interface.cable import CableInterfaceModel
from filare.models.interface.connection import ConnectionInterfaceModel
from filare.models.interface.connector import ConnectorInterfaceModel
from filare.models.interface.metadata import MetadataInterfaceModel
from filare.models.interface.options import OptionsInterfaceModel


class HarnessInterfaceModel(FilareInterfaceModel):
    """Top-level harness description supplied by users."""

    metadata: MetadataInterfaceModel = Field(
        ..., description="Document metadata describing the harness."
    )
    options: OptionsInterfaceModel = Field(
        default_factory=OptionsInterfaceModel,
        description="Rendering and output options for this harness.",
    )
    connectors: Dict[str, ConnectorInterfaceModel] = Field(
        default_factory=dict,
        description="Mapping of connector designators to connector definitions.",
    )
    cables: Dict[str, CableInterfaceModel] = Field(
        default_factory=dict,
        description="Mapping of cable designators to cable definitions.",
    )
    connections: List[ConnectionInterfaceModel] = Field(
        default_factory=list,
        description="List of connections tying connector endpoints through cable wires.",
    )

    @model_validator(mode="after")
    def _apply_keys_as_designators(self) -> "HarnessInterfaceModel":
        """Propagate mapping keys into designator fields for connectors/cables."""
        for designator, connector in self.connectors.items():
            connector.designator = connector.designator or designator
        for designator, cable in self.cables.items():
            cable.designator = cable.designator or designator
        return self


class HarnessConfigurationInterfaceModel(FilareInterfaceModel):
    """Configuration options controlling harness parsing/normalization."""

    # Placeholder for future parsing toggles; keeps a dedicated config object per harness.
    pass
