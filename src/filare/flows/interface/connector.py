from __future__ import annotations

from typing import Any, Iterable, Mapping, MutableMapping, Optional, Sequence

from pydantic import ValidationError

from filare.flows.interface.errors import InterfaceFlowError
from filare.models.interface.connector import (
    ConnectorConfigurationInterfaceModel,
    ConnectorInterfaceModel,
    LoopInterfaceModel,
)


def _ensure_mapping(payload: Any, key: str) -> MutableMapping[str, Any]:
    if not isinstance(payload, MutableMapping):
        raise InterfaceFlowError(f"Connector '{key}' must be a mapping.")
    return dict(payload)


def _propagate_designator(data: MutableMapping[str, Any], key: str) -> None:
    designator = data.get("designator") or key
    explicit_designator = data.get("designator")
    if explicit_designator and explicit_designator != key:
        raise InterfaceFlowError(
            f"Connector '{key}' designator mismatch: got '{explicit_designator}'."
        )
    data["designator"] = designator


def _validate_pin_lists(model: ConnectorInterfaceModel, key: str) -> None:
    lengths = [
        len(lst) for lst in (model.pins, model.pinlabels, model.pincolors) if lst
    ]
    if len(set(lengths)) > 1:
        raise InterfaceFlowError(
            f"Connector '{key}' pin-related lists must share the same length "
            f"(pins={len(model.pins)}, pinlabels={len(model.pinlabels)}, pincolors={len(model.pincolors)})."
        )


def _known_pin_values(model: ConnectorInterfaceModel) -> set[str]:
    known: set[str] = set()
    for value in model.pins:
        known.add(str(value))
    for value in model.pinlabels:
        known.add(str(value))
    return known


def _validate_loops(model: ConnectorInterfaceModel, key: str) -> None:
    known = _known_pin_values(model)
    if not known:
        return
    for idx, loop in enumerate(model.loops):
        for endpoint in _loop_endpoints(loop):
            if endpoint not in known:
                raise InterfaceFlowError(
                    f"Connector '{key}' loop[{idx}] references unknown pin '{endpoint}'."
                )


def _loop_endpoints(loop: LoopInterfaceModel) -> Iterable[str]:
    return (str(loop.first), str(loop.second))


def load_connector(
    connectors: Mapping[str, Any],
    key: str,
    config: Optional[ConnectorConfigurationInterfaceModel] = None,
) -> ConnectorInterfaceModel:
    """Extract, normalize, and validate a connector entry by key."""
    if key not in connectors:
        raise InterfaceFlowError(f"Connector '{key}' not found.")
    raw = connectors[key] or {}
    data = _ensure_mapping(raw, key)
    _ = config  # reserved for future parsing toggles
    _propagate_designator(data, key)
    try:
        model = ConnectorInterfaceModel.model_validate(data)
    except ValidationError as exc:
        raise InterfaceFlowError(f"Connector '{key}' validation failed: {exc}") from exc
    _validate_pin_lists(model, key)
    _validate_loops(model, key)
    return model


def save_connector_yaml(model: ConnectorInterfaceModel) -> str:
    """Serialize a validated connector to YAML."""
    return model.to_yaml()


def generate_connectors(count: int = 1) -> Sequence[ConnectorInterfaceModel]:
    """Generate connector models for examples/tests."""
    from filare.models.interface.factories import FakeConnectorInterfaceFactory

    return [FakeConnectorInterfaceFactory.build() for _ in range(count)]
