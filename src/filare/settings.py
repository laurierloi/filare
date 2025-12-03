"""Centralized settings loaded from environment with WV_ prefix."""

from typing import Optional

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
    USING_PYDANTIC_V1 = False
except ImportError:  # fallback to pydantic v1 BaseSettings for older envs
    from pydantic.v1 import BaseSettings

    SettingsConfigDict = None  # type: ignore
    USING_PYDANTIC_V1 = True


class FilareSettings(BaseSettings):
    graphviz_engine: Optional[str] = None  # e.g., dot, neato
    debug: bool = False

    if not USING_PYDANTIC_V1:
        model_config = SettingsConfigDict(env_prefix="WV_", case_sensitive=False)
    else:
        class Config:
            env_prefix = "WV_"
            case_sensitive = False


settings = FilareSettings()
