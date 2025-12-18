"""Typer configuration defaults controllable via environment."""

from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class TyperSettings(BaseSettings):
    """Settings for Typer apps (overridable via FIL_TYPER_* env vars)."""

    rich_markup_mode: Optional[str] = Field(
        default="rich",
        description="Rich markup mode for Typer help (set to null/empty to disable).",
    )
    pretty_exceptions_enable: bool = Field(
        default=True, description="Enable Typer pretty exceptions."
    )
    pretty_exceptions_show_locals: bool = Field(
        default=False, description="Show locals in pretty exceptions."
    )
    pretty_exceptions_short: bool = Field(
        default=False, description="Use short pretty exception output."
    )
    add_completion: bool = Field(
        default=True, description="Enable shell completion for Typer apps."
    )
    no_args_is_help: bool = Field(
        default=True, description="Show help when no args are provided."
    )

    model_config = SettingsConfigDict(env_prefix="FIL_TYPER_", case_sensitive=False)

    def to_kwargs(self, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Return kwargs for Typer(...), applying optional overrides."""
        data: Dict[str, Any] = self.model_dump()
        if overrides:
            data.update(overrides)
        # Filter out None rich_markup_mode to let Typer fall back to defaults.
        return {key: value for key, value in data.items() if value is not None}


def typer_kwargs(overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Convenience helper to produce Typer constructor kwargs with env overrides."""
    return TyperSettings().to_kwargs(overrides)
