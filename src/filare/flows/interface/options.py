from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Optional, Sequence

from pydantic import ValidationError

from filare.flows.interface.errors import InterfaceFlowError
from filare.models.interface.options import (
    OptionsConfigurationInterfaceModel,
    OptionsInterfaceModel,
)


def _ensure_mapping(payload: Any, key: str) -> MutableMapping[str, Any]:
    if not isinstance(payload, MutableMapping):
        raise InterfaceFlowError(f"Options '{key}' must be a mapping.")
    return dict(payload)


def load_options(
    options_map: Mapping[str, Any],
    key: str,
    config: Optional[OptionsConfigurationInterfaceModel] = None,
) -> OptionsInterfaceModel:
    """Extract, normalize, and validate an options entry by key."""
    if key not in options_map:
        raise InterfaceFlowError(f"Options '{key}' not found.")
    raw = options_map[key] or {}
    data = _ensure_mapping(raw, key)
    _ = config  # reserved for future parsing toggles
    try:
        return OptionsInterfaceModel.model_validate(data)
    except ValidationError as exc:
        raise InterfaceFlowError(f"Options '{key}' validation failed: {exc}") from exc


def save_options_yaml(model: OptionsInterfaceModel) -> str:
    """Serialize validated options to YAML."""
    return model.to_yaml()


def generate_options(count: int = 1) -> Sequence[OptionsInterfaceModel]:
    """Generate options models for examples/tests."""
    from filare.models.interface.factories import FakeOptionsInterfaceFactory

    return [FakeOptionsInterfaceFactory.build() for _ in range(count)]
