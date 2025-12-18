from __future__ import annotations

from typing import Any, Mapping, Optional

from pydantic import ValidationError

from filare.flows.interface.errors import InterfaceFlowError
from filare.models.interface.config import InterfaceConfigurationModel


def load_interface_config(
    config_data: Mapping[str, Any],
) -> InterfaceConfigurationModel:
    """Validate interface configuration data."""
    try:
        return InterfaceConfigurationModel.model_validate(config_data)
    except ValidationError as exc:
        raise InterfaceFlowError(f"Interface config validation failed: {exc}") from exc


def save_interface_config_yaml(model: InterfaceConfigurationModel) -> str:
    """Serialize interface configuration to YAML."""
    return model.to_yaml()


def generate_interface_config() -> InterfaceConfigurationModel:
    """Generate an empty interface configuration."""
    return InterfaceConfigurationModel()
