"""Centralized settings loaded from environment with WV_ prefix."""

from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class FilareSettings(BaseSettings):
    graphviz_engine: Optional[str] = None  # e.g., dot, neato
    debug: bool = False
    enable_cut_termination: bool = False

    model_config = SettingsConfigDict(env_prefix="FIL_", case_sensitive=False)


settings = FilareSettings()
