from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .config import AgentSessionConfig


class RegistryError(Exception):
    """Raised when session registry operations fail."""


def find_repo_root(start: Optional[Path] = None) -> Path:
    """Walk up from `start` (or cwd) until a directory containing .git is found."""
    cursor = (start or Path.cwd()).resolve()
    for parent in [cursor, *cursor.parents]:
        if (parent / ".git").exists():
            return parent
    raise RegistryError("Could not locate repository root (missing .git?)")


@dataclass
class SessionState:
    id: str
    role: str
    branch: str
    workspace: str
    env_file: str
    ssh_key: str
    image: str
    manifest_path: str
    status: str
    command: List[str]
    recorded_at: str
    dry_run: bool = True

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, object]) -> "SessionState":
        return cls(**data)  # type: ignore[arg-type]


class SessionRegistry:
    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = find_repo_root(repo_root)

    def _session_dir(self, session: AgentSessionConfig) -> Path:
        return self.repo_root / "outputs" / "agents" / session.role / session.id

    def _state_path(self, session: AgentSessionConfig) -> Path:
        return self._session_dir(session) / "state.json"

    def record(self, session: AgentSessionConfig, command: List[str], status: str, dry_run: bool) -> SessionState:
        state = SessionState(
            id=session.id,
            role=session.role,
            branch=session.branch,
            workspace=str(session.workspace),
            env_file=str(session.env_file),
            ssh_key=str(session.ssh_key),
            image=session.image,
            manifest_path=str(session.manifest_path) if session.manifest_path else "",
            status=status,
            command=command,
            recorded_at=datetime.now(timezone.utc).isoformat(),
            dry_run=dry_run,
        )
        session_dir = self._session_dir(session)
        session_dir.mkdir(parents=True, exist_ok=True)
        self._state_path(session).write_text(json.dumps(state.to_dict(), indent=2))
        return state

    def load_all(self) -> List[SessionState]:
        states: List[SessionState] = []
        root = self.repo_root / "outputs" / "agents"
        if not root.exists():
            return []
        for path in root.rglob("state.json"):
            try:
                raw = json.loads(path.read_text())
                states.append(SessionState.from_dict(raw))
            except Exception as exc:  # pragma: no cover - defensive logging
                raise RegistryError(f"Failed to load state from {path}: {exc}") from exc
        return states


def build_run_command(session: AgentSessionConfig, repo_root: Optional[Path] = None) -> List[str]:
    root = find_repo_root(repo_root)
    script = root / "scripts" / "run_codex_container.sh"
    cmd = [
        str(script),
        "--workspace",
        str(session.workspace),
        "--ssh-key",
        str(session.ssh_key),
        "--env-file",
        str(session.env_file),
    ]
    if session.image and session.image != "filare-codex":
        cmd.extend(["--image", session.image])
    return cmd


def launch_session(
    session: AgentSessionConfig,
    repo_root: Optional[Path] = None,
    execute: bool = False,
) -> Tuple[SessionState, List[str]]:
    root = find_repo_root(repo_root)
    command = build_run_command(session, repo_root=root)
    registry = SessionRegistry(root)
    state = registry.record(session, command=command, status="planned", dry_run=not execute)

    if execute:
        subprocess.run(command, cwd=root, check=True)
        state = registry.record(session, command=command, status="running", dry_run=False)

    return state, command


def resume_plan(repo_root: Optional[Path] = None) -> List[Dict[str, str]]:
    """Return suggestions on how to reconnect to existing sessions."""
    root = find_repo_root(repo_root)
    registry = SessionRegistry(root)
    plans: List[Dict[str, str]] = []
    for state in registry.load_all():
        plans.append(
            {
                "session_id": state.id,
                "role": state.role,
                "branch": state.branch,
                "workspace": state.workspace,
                "note": "Identify the container (by label/name) then docker exec to tmux session named after session_id.",
            }
        )
    return plans
