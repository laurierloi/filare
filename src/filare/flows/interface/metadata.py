from __future__ import annotations

from typing import Any, Mapping, MutableMapping, Optional, Sequence

from pydantic import ValidationError

from filare.flows.interface.errors import InterfaceFlowError
from filare.models.interface.metadata import (
    MetadataConfigurationInterfaceModel,
    MetadataInterfaceModel,
)


def _ensure_mapping(payload: Any, key: str) -> MutableMapping[str, Any]:
    if not isinstance(payload, MutableMapping):
        raise InterfaceFlowError(f"Metadata '{key}' must be a mapping.")
    return dict(payload)


def load_metadata(
    metadata_map: Mapping[str, Any],
    key: str,
    config: Optional[MetadataConfigurationInterfaceModel] = None,
) -> MetadataInterfaceModel:
    """Extract, normalize, and validate a metadata entry by key."""
    if key not in metadata_map:
        raise InterfaceFlowError(f"Metadata '{key}' not found.")
    raw = metadata_map[key] or {}
    data = _ensure_mapping(raw, key)
    _ = config  # reserved for future parsing toggles
    try:
        return MetadataInterfaceModel.model_validate(data)
    except ValidationError as exc:
        raise InterfaceFlowError(f"Metadata '{key}' validation failed: {exc}") from exc


def save_metadata_yaml(model: MetadataInterfaceModel) -> str:
    """Serialize validated metadata to YAML."""
    return model.to_yaml()


def generate_metadata(count: int = 1) -> Sequence[MetadataInterfaceModel]:
    """Generate metadata models for examples/tests."""
    from filare.models.interface.factories import FakeMetadataInterfaceFactory

    return [FakeMetadataInterfaceFactory.build() for _ in range(count)]
