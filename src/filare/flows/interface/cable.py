from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Optional, Sequence

from pydantic import ValidationError

from filare.flows.interface.errors import InterfaceFlowError
from filare.models.interface.cable import (
    CableConfigurationInterfaceModel,
    CableInterfaceModel,
)


def _ensure_mapping(payload: Any, key: str) -> MutableMapping[str, Any]:
    if not isinstance(payload, MutableMapping):
        raise InterfaceFlowError(f"Cable '{key}' must be a mapping.")
    return dict(payload)


def _propagate_designator(data: MutableMapping[str, Any], key: str) -> None:
    designator = data.get("designator") or key
    explicit_designator = data.get("designator")
    if explicit_designator and explicit_designator != key:
        raise InterfaceFlowError(
            f"Cable '{key}' designator mismatch: got '{explicit_designator}'."
        )
    data["designator"] = designator


def _validate_wirecount(model: CableInterfaceModel, key: str) -> None:
    if model.wirecount <= 0:
        raise InterfaceFlowError(f"Cable '{key}' must have wirecount > 0.")


def _validate_colors(model: CableInterfaceModel, key: str) -> None:
    if model.colors and len(model.colors) != model.wirecount:
        raise InterfaceFlowError(
            f"Cable '{key}' colors length ({len(model.colors)}) "
            f"must match wirecount ({model.wirecount}) when provided."
        )


def load_cable(
    cables: Mapping[str, Any],
    key: str,
    config: Optional[CableConfigurationInterfaceModel] = None,
) -> CableInterfaceModel:
    """Extract, normalize, and validate a cable entry by key."""
    if key not in cables:
        raise InterfaceFlowError(f"Cable '{key}' not found.")
    raw = cables[key] or {}
    data = _ensure_mapping(raw, key)
    _ = config  # reserved for future parsing toggles
    _propagate_designator(data, key)
    try:
        model = CableInterfaceModel.model_validate(data)
    except ValidationError as exc:
        raise InterfaceFlowError(f"Cable '{key}' validation failed: {exc}") from exc
    _validate_wirecount(model, key)
    _validate_colors(model, key)
    return model


def save_cable_yaml(model: CableInterfaceModel) -> str:
    """Serialize a validated cable to YAML."""
    return model.to_yaml()


def generate_cables(count: int = 1) -> Sequence[CableInterfaceModel]:
    """Generate cable models for examples/tests."""
    from filare.models.interface.factories import FakeCableInterfaceFactory

    return [FakeCableInterfaceFactory.build() for _ in range(count)]
