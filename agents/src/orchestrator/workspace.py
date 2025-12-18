from __future__ import annotations

from pathlib import Path
from typing import Callable, List

from .config import AgentSessionConfig


def _workspaces_in_use(load_states: Callable[[], List], role: str) -> List[Path]:
    """Avoid circular import by passing a callable to fetch states."""
    return [Path(state.workspace) for state in load_states() if state.role == role]


def _next_workspace(prefix: str, load_states: Callable[[], List], role: str) -> Path:
    used = _workspaces_in_use(load_states, role)
    i = 1
    while True:
        candidate = Path(prefix.format(n=i))
        if candidate not in used:
            return candidate
        i += 1


def assign_workspace(session: AgentSessionConfig, load_states: Callable[[], List]) -> AgentSessionConfig:
    """Return a session with workspace resolved from template/prefix if provided."""
    if session.workspace.exists():
        return session

    if session.workspace_template:
        prefix = session.workspace_template
    elif session.workspace_prefix:
        prefix = f"{session.workspace_prefix}{{n}}"
    else:
        return session

    resolved = _next_workspace(prefix, load_states, session.role)
    session.workspace = resolved
    return session
