from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import yaml


class ManifestError(Exception):
    """Raised when a manifest is missing required fields or is malformed."""


@dataclass
class AgentSessionConfig:
    id: str
    role: str
    branch: str
    workspace: Path
    env_file: Path
    ssh_key: Path
    goal: Optional[str] = None
    image: str = "filare-codex"
    tags: List[str] = field(default_factory=list)
    startup_script: Optional[str] = None
    operator_contact: Dict[str, Any] = field(default_factory=dict)
    workspace_prefix: Optional[str] = None
    workspace_template: Optional[str] = None
    reuse_existing: bool = False
    manifest_path: Optional[Path] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        for key, value in list(data.items()):
            if isinstance(value, Path):
                data[key] = str(value)
        return data


def _resolve_path(base_dir: Path, value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = base_dir / path
    return path


def _coerce_tags(raw: Any) -> List[str]:
    if raw is None:
        return []
    if isinstance(raw, str):
        return [raw]
    if isinstance(raw, Iterable) and not isinstance(raw, (dict, bytes)):
        return [str(item) for item in raw]
    raise ManifestError(f"Invalid tags value: {raw!r}")


def _apply_defaults(session: Dict[str, Any], defaults: Dict[str, Any]) -> Dict[str, Any]:
    merged = defaults.copy()
    merged.update(session)
    return merged


def _normalize_sessions(raw: Any, manifest_path: Path) -> List[Dict[str, Any]]:
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        # if dict with sessions key, accept it; otherwise treat as single session
        if "sessions" in raw:
            return raw["sessions"]
        return [raw]
    raise ManifestError("Manifest must be a list of sessions or a mapping with 'sessions'.")


def _extract_defaults(raw: Any) -> Dict[str, Any]:
    if isinstance(raw, dict) and "defaults" in raw:
        defaults = raw["defaults"]
        if defaults is None:
            return {}
        if not isinstance(defaults, dict):
            raise ManifestError("defaults must be a mapping of field: value.")
        return defaults
    return {}


def load_manifest(path: Path) -> List[AgentSessionConfig]:
    manifest_path = Path(path).resolve()
    if not manifest_path.exists():
        raise ManifestError(f"Manifest not found: {manifest_path}")

    base_dir = manifest_path.parent
    raw = yaml.safe_load(manifest_path.read_text()) or {}

    defaults = _extract_defaults(raw)
    raw_sessions = _normalize_sessions(raw, manifest_path)

    sessions: List[AgentSessionConfig] = []
    for session_data in raw_sessions:
        if not isinstance(session_data, dict):
            raise ManifestError(f"Session entry must be a mapping, got: {session_data!r}")
        merged = _apply_defaults(session_data, defaults)

        missing = [field for field in ("id", "role", "branch", "workspace", "env_file", "ssh_key") if field not in merged]
        if missing:
            raise ManifestError(f"Session {session_data!r} missing required fields: {', '.join(missing)}")

        session = AgentSessionConfig(
            id=str(merged["id"]),
            role=str(merged["role"]),
            branch=str(merged["branch"]),
            workspace=_resolve_path(base_dir, str(merged["workspace"])),
            env_file=_resolve_path(base_dir, str(merged["env_file"])),
            ssh_key=_resolve_path(base_dir, str(merged["ssh_key"])),
            goal=merged.get("goal"),
            image=str(merged.get("image", "filare-codex")),
            tags=_coerce_tags(merged.get("tags")),
            startup_script=merged.get("startup_script"),
            operator_contact=merged.get("operator_contact") or {},
            workspace_prefix=str(merged.get("workspace_prefix")) if merged.get("workspace_prefix") else None,
            workspace_template=str(merged.get("workspace_template")) if merged.get("workspace_template") else None,
            reuse_existing=bool(merged.get("reuse_existing", False)),
            manifest_path=manifest_path,
        )
        sessions.append(session)

    ids = [session.id for session in sessions]
    if len(ids) != len(set(ids)):
        raise ManifestError(f"Duplicate session ids detected: {ids}")

    return sessions


def select_sessions(sessions: List[AgentSessionConfig], session_id: Optional[str]) -> List[AgentSessionConfig]:
    if session_id is None:
        return sessions
    for session in sessions:
        if session.id == session_id:
            return [session]
    raise ManifestError(f"Session id '{session_id}' not found in manifest.")
