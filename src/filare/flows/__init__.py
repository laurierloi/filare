"""Flow-level orchestration helpers with lazy imports to avoid circulars."""

from typing import Any

__all__ = ["build_harness_from_files", "render_harness_outputs"]


def build_harness_from_files(*args: Any, **kwargs: Any):
    from filare.flows.build_harness import build_harness_from_files as _impl

    return _impl(*args, **kwargs)


def render_harness_outputs(*args: Any, **kwargs: Any):
    from filare.flows.render_outputs import render_harness_outputs as _impl

    return _impl(*args, **kwargs)
