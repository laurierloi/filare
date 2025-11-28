"""Centralized settings loaded from environment with WV_ prefix."""

import os
from typing import Optional

from pydantic import BaseSettings, Field


class FilareSettings(BaseSettings):
    graphviz_engine: Optional[str] = Field(
        default=None, env="WV_GRAPHVIZ_ENGINE"
    )  # e.g., dot, neato
    debug: bool = Field(default=False, env="WV_DEBUG")

    class Config:
        env_prefix = "WV_"
        case_sensitive = False


settings = FilareSettings()
# Backward compatibility for imports that still refer to the previous brand.
WireVizSettings = FilareSettings
