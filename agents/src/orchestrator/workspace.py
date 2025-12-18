from __future__ import annotations

from pathlib import Path
from typing import List

from .config import AgentSessionConfig
from .runtime import SessionRegistry


def _workspaces_in_use(registry: SessionRegistry, role: str) -> List[Path]:
    paths: List[Path] = []
    for state in registry.load_all():
        if state.role == role:
            paths.append(Path(state.workspace))
    return paths


def _next_workspace(prefix: str, registry: SessionRegistry, role: str) -> Path:
    used = _workspaces_in_use(registry, role)
    i = 1
    while True:
        candidate = Path(prefix.format(n=i))
        if candidate not in used:
            return candidate
        i += 1


def assign_workspace(session: AgentSessionConfig, repo_root: Path) -> AgentSessionConfig:
    """Return a session with workspace resolved from template/prefix if provided."""
    if session.workspace.exists():
        return session

    registry = SessionRegistry(repo_root)
    if session.workspace_template:
        prefix = session.workspace_template
    elif session.workspace_prefix:
        prefix = f"{session.workspace_prefix}{{n}}"
    else:
        return session

    resolved = _next_workspace(prefix, registry, session.role)
    session.workspace = resolved
    return session
