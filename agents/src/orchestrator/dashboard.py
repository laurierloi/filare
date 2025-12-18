from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List

from .feedback import load_queue
from .runtime import SessionRegistry, find_repo_root


@dataclass
class DashboardEntry:
    session_id: str
    role: str
    branch: str
    status: str
    workspace: str
    prompts_pending: int

    def to_dict(self) -> dict:
        return asdict(self)


def collect_dashboard(repo_root: Path | None = None, queue: Path | None = None) -> List[DashboardEntry]:
    root = find_repo_root(repo_root)
    registry = SessionRegistry(root)
    prompts = load_queue(queue or (root / "outputs" / "agents" / "prompts.json"))
    pending_by_session = {}
    for prompt in prompts:
        if prompt.decision:
            continue
        pending_by_session[prompt.session_id] = pending_by_session.get(prompt.session_id, 0) + 1

    entries: List[DashboardEntry] = []
    for state in registry.load_all():
        entries.append(
            DashboardEntry(
                session_id=state.id,
                role=state.role,
                branch=state.branch,
                status=state.status,
                workspace=state.workspace,
                prompts_pending=pending_by_session.get(state.id, 0),
            )
        )
    return entries


def to_json(entries: List[DashboardEntry]) -> str:
    return json.dumps([entry.to_dict() for entry in entries], indent=2)
