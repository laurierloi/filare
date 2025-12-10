"""Centralized settings with CLI > ENV > CONFIG > DEFAULT precedence."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Iterable, Optional

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

CONFIG_FILENAMES = {"user": "user.yaml", "project": "project.yaml"}


def _get_base_config_dir() -> Path:
    env_override = os.getenv("FIL_CONFIG_PATH")
    if env_override:
        return Path(env_override).expanduser()
    xdg_config_home = os.getenv("XDG_CONFIG_HOME")
    if xdg_config_home:
        return Path(xdg_config_home) / "filare"
    return Path.home() / ".config" / "filare"


def _assert_scope(scope: str) -> None:
    if scope not in CONFIG_FILENAMES:
        raise ValueError(f"Invalid scope '{scope}'. Expected one of: user, project.")


class FilareSettingsModel(BaseModel):
    """Settings model with defaults."""

    config_dir: Path = Field(default_factory=_get_base_config_dir)
    graphviz_engine: Optional[str] = Field(
        default=None, description="Graphviz engine name."
    )
    debug: bool = Field(default=False, description="Enable debug output.")

    model_config = {"extra": "allow"}


class EnvSettings(BaseSettings):
    """Environment-derived settings."""

    graphviz_engine: Optional[str] = Field(
        default=None, validation_alias="WV_GRAPHVIZ_ENGINE"
    )  # e.g., dot, neato
    debug: bool = False

    model_config = SettingsConfigDict(env_prefix="WV_", case_sensitive=False)


class SettingsStore:
    """Persist and load settings from YAML files."""

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or _get_base_config_dir()

    def path_for_scope(self, scope: str) -> Path:
        _assert_scope(scope)
        return self.base_dir / CONFIG_FILENAMES[scope]

    def load_scope(self, scope: str) -> Dict[str, Any]:
        path = self.path_for_scope(scope)
        if not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        if not isinstance(data, dict):
            raise ValueError(f"Settings file {path} must contain a mapping.")
        return data

    def write_scope(self, scope: str, data: Dict[str, Any]) -> Path:
        path = self.path_for_scope(scope)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(data, handle, sort_keys=True)
        return path

    def merged_config(
        self, scopes: Iterable[str] = ("user", "project")
    ) -> Dict[str, Any]:
        merged: Dict[str, Any] = {}
        for scope in scopes:
            merged.update(self.load_scope(scope))
        return merged


def resolve_settings(
    *,
    cli_overrides: Optional[Dict[str, Any]] = None,
    store: Optional[SettingsStore] = None,
) -> FilareSettingsModel:
    """Resolve settings with CLI > ENV > CONFIG > DEFAULT priority."""
    active_store = store or SettingsStore()
    defaults = FilareSettingsModel(config_dir=active_store.base_dir).model_dump()
    config_values = active_store.merged_config()
    # Prevent stale config_dir from files overriding the active base dir.
    config_values.pop("config_dir", None)
    env_overrides = EnvSettings().model_dump(exclude_unset=True)

    merged: Dict[str, Any] = {}
    merged.update(defaults)
    merged.update(config_values)
    merged.update(env_overrides)
    if cli_overrides:
        merged.update(cli_overrides)
    return FilareSettingsModel(**merged)


class FilareSettings(FilareSettingsModel):
    """Backward-compatible settings facade that resolves env/config/defaults."""

    def __init__(self, **kwargs: Any):
        resolved = resolve_settings(cli_overrides=kwargs)
        super().__init__(**resolved.model_dump())


settings = FilareSettings()
