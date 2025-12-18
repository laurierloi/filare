from __future__ import annotations

from typing import Any, Dict, Mapping, MutableMapping, Optional, Sequence

from pydantic import ValidationError

from filare.flows.interface.cable import load_cable
from filare.flows.interface.connection import load_connection
from filare.flows.interface.connector import load_connector
from filare.flows.interface.errors import InterfaceFlowError
from filare.flows.interface.metadata import load_metadata
from filare.flows.interface.options import load_options
from filare.models.interface.cable import CableInterfaceModel
from filare.models.interface.connection import ConnectionInterfaceModel
from filare.models.interface.connector import ConnectorInterfaceModel
from filare.models.interface.harness import (
    HarnessConfigurationInterfaceModel,
    HarnessInterfaceModel,
)
from filare.models.interface.metadata import MetadataInterfaceModel
from filare.models.interface.options import OptionsInterfaceModel


def _ensure_mapping(payload: Any, key: str) -> MutableMapping[str, Any]:
    if not isinstance(payload, MutableMapping):
        raise InterfaceFlowError(f"Harness '{key}' must be a mapping.")
    return dict(payload)


def _load_metadata_section(
    payload: Mapping[str, Any], config: Optional[HarnessConfigurationInterfaceModel]
) -> MetadataInterfaceModel:
    meta_map = {"metadata": payload.get("metadata", {})}
    return load_metadata(meta_map, "metadata")


def _load_options_section(
    payload: Mapping[str, Any], config: Optional[HarnessConfigurationInterfaceModel]
) -> OptionsInterfaceModel:
    options_map = {"options": payload.get("options", {})}
    return load_options(options_map, "options")


def _load_connectors_section(
    payload: Mapping[str, Any], config: Optional[HarnessConfigurationInterfaceModel]
) -> Dict[str, ConnectorInterfaceModel]:
    connectors_raw = payload.get("connectors", {}) or {}
    if not isinstance(connectors_raw, Mapping):
        raise InterfaceFlowError("Harness connectors must be a mapping.")
    connectors_map = dict(connectors_raw)
    return {key: load_connector(connectors_map, key) for key in connectors_map}


def _load_cables_section(
    payload: Mapping[str, Any], config: Optional[HarnessConfigurationInterfaceModel]
) -> Dict[str, CableInterfaceModel]:
    cables_raw = payload.get("cables", {}) or {}
    if not isinstance(cables_raw, Mapping):
        raise InterfaceFlowError("Harness cables must be a mapping.")
    cables_map = dict(cables_raw)
    return {key: load_cable(cables_map, key) for key in cables_map}


def _load_connections_section(
    payload: Mapping[str, Any],
    connectors: Mapping[str, ConnectorInterfaceModel],
    cables: Mapping[str, CableInterfaceModel],
    config: Optional[HarnessConfigurationInterfaceModel],
) -> Sequence[ConnectionInterfaceModel]:
    connections_raw = payload.get("connections", []) or []
    if not isinstance(connections_raw, Sequence):
        raise InterfaceFlowError("Harness connections must be a list or mapping.")
    models: list[ConnectionInterfaceModel] = []
    if isinstance(connections_raw, Mapping):
        for key in connections_raw:
            models.append(
                load_connection(
                    connections_raw, key, connectors=connectors, cables=cables
                )
            )
    else:
        for idx, entry in enumerate(connections_raw):
            models.append(
                load_connection(
                    connections_raw, str(idx), connectors=connectors, cables=cables
                )
            )
    return models


def load_harness(
    harnesses: Mapping[str, Any],
    key: str,
    config: Optional[HarnessConfigurationInterfaceModel] = None,
) -> HarnessInterfaceModel:
    """Extract, normalize, and validate a harness entry by key."""
    if key not in harnesses:
        raise InterfaceFlowError(f"Harness '{key}' not found.")
    raw = harnesses[key] or {}
    data = _ensure_mapping(raw, key)
    _ = config  # reserved for future parsing toggles
    metadata_model = _load_metadata_section(data, config)
    options_model = _load_options_section(data, config)
    connectors_model = _load_connectors_section(data, config)
    cables_model = _load_cables_section(data, config)
    connections_model = _load_connections_section(
        data, connectors_model, cables_model, config
    )
    try:
        return HarnessInterfaceModel.model_validate(
            {
                "metadata": metadata_model,
                "options": options_model,
                "connectors": connectors_model,
                "cables": cables_model,
                "connections": connections_model,
            }
        )
    except ValidationError as exc:
        raise InterfaceFlowError(f"Harness '{key}' validation failed: {exc}") from exc


def save_harness_yaml(model: HarnessInterfaceModel) -> str:
    """Serialize validated harness to YAML."""
    return model.to_yaml()


def generate_harnesses(count: int = 1) -> Sequence[HarnessInterfaceModel]:
    """Generate harness models for examples/tests."""
    from filare.models.interface.factories import FakeHarnessInterfaceFactory

    return [FakeHarnessInterfaceFactory.build() for _ in range(count)]
