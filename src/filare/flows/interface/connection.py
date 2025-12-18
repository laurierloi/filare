from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Optional, Sequence

from pydantic import ValidationError

from filare.flows.interface.errors import InterfaceFlowError
from filare.flows.interface.validate_connection import validate_connection_context
from filare.models.interface.cable import CableInterfaceModel
from filare.models.interface.connection import (
    ConnectionConfigurationInterfaceModel,
    ConnectionInterfaceModel,
)
from filare.models.interface.connector import ConnectorInterfaceModel


def _ensure_mapping(payload: Any, key: str) -> MutableMapping[str, Any]:
    if not isinstance(payload, MutableMapping):
        raise InterfaceFlowError(f"Connection '{key}' must be a mapping.")
    return dict(payload)


def _resolve_entry(
    connections: Mapping[str, Any] | Sequence[Any], key: str
) -> tuple[str, Any]:
    if isinstance(connections, Mapping):
        if key not in connections:
            raise InterfaceFlowError(f"Connection '{key}' not found.")
        return key, connections[key]
    if isinstance(connections, Sequence):
        try:
            index = int(key)
        except ValueError as exc:
            raise InterfaceFlowError(
                f"Connection key '{key}' is not a valid index."
            ) from exc
        if index < 0 or index >= len(connections):
            raise InterfaceFlowError(f"Connection index {index} out of range.")
        return key, connections[index]
    raise InterfaceFlowError("Connections input must be a mapping or list.")


def _normalize_aliases(data: MutableMapping[str, Any]) -> None:
    if "from" in data:
        data["from_"] = data.pop("from")


def _ensure_endpoint_presence(data: Mapping[str, Any], key: str) -> None:
    if not data.get("from_") and not data.get("to"):
        raise InterfaceFlowError(
            f"Connection '{key}' must specify at least one endpoint ('from' or 'to')."
        )


def load_connection(
    connections: Mapping[str, Any] | Sequence[Any],
    key: str,
    config: Optional[ConnectionConfigurationInterfaceModel] = None,
    connectors: Optional[Mapping[str, ConnectorInterfaceModel]] = None,
    cables: Optional[Mapping[str, CableInterfaceModel]] = None,
) -> ConnectionInterfaceModel:
    """Extract, normalize, and validate a connection entry by key/index."""
    resolved_key, raw = _resolve_entry(connections, key)
    data = _ensure_mapping(raw, resolved_key)
    _normalize_aliases(data)
    _ensure_endpoint_presence(data, resolved_key)
    _ = config  # reserved for future parsing toggles
    try:
        model = ConnectionInterfaceModel.model_validate(data)
    except ValidationError as exc:
        raise InterfaceFlowError(
            f"Connection '{resolved_key}' validation failed: {exc}"
        ) from exc
    validate_connection_context(model, resolved_key, connectors, cables)
    return model


def save_connection_yaml(model: ConnectionInterfaceModel) -> str:
    """Serialize a validated connection to YAML."""
    return model.to_yaml()


def generate_connections(count: int = 1) -> Sequence[ConnectionInterfaceModel]:
    """Generate connection models for examples/tests."""
    from filare.models.interface.factories import FakeConnectionInterfaceFactory

    return [FakeConnectionInterfaceFactory.build() for _ in range(count)]
