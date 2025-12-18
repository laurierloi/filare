from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Literal, Optional


Decision = Literal["approved", "rejected"]


@dataclass
class Prompt:
    """Represents a prompt awaiting operator decision."""

    id: str
    session_id: str
    role: str
    workspace: str
    branch: str
    reason: str
    requested_action: str
    suggested_reply: Optional[str] = None
    severity: str = "info"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    decision: Optional[Decision] = None
    decided_at: Optional[str] = None
    reply: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Prompt":
        return cls(**data)


def load_queue(queue_path: Path) -> List[Prompt]:
    if not queue_path.exists():
        return []
    raw = json.loads(queue_path.read_text())
    return [Prompt.from_dict(item) for item in raw]


def save_queue(queue_path: Path, prompts: List[Prompt]) -> None:
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    queue_path.write_text(json.dumps([p.to_dict() for p in prompts], indent=2))


def add_prompt(queue_path: Path, prompt: Prompt) -> Prompt:
    prompts = load_queue(queue_path)
    prompts.append(prompt)
    save_queue(queue_path, prompts)
    return prompt


def list_prompts(queue_path: Path) -> List[Prompt]:
    return load_queue(queue_path)


def resolve_prompt(queue_path: Path, prompt_id: str, decision: Decision, reply: Optional[str] = None) -> Prompt:
    prompts = load_queue(queue_path)
    for prompt in prompts:
        if prompt.id == prompt_id:
            prompt.decision = decision
            prompt.reply = reply
            prompt.decided_at = datetime.now(timezone.utc).isoformat()
            save_queue(queue_path, prompts)
            return prompt
    raise ValueError(f"Prompt id '{prompt_id}' not found")
