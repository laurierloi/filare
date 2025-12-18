import json
from pathlib import Path

import pytest

from orchestrator.config import AgentSessionConfig
from orchestrator.runtime import build_run_command, launch_session, resume_plan

pytestmark = pytest.mark.agent


def _setup_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()
    return repo_root


def _session(repo_root: Path) -> AgentSessionConfig:
    return AgentSessionConfig(
        id="alpha",
        role="FEATURE",
        branch="main",
        workspace=repo_root / "work",
        env_file=repo_root / ".env",
        ssh_key=repo_root / "id_rsa",
        image="filare-codex",
        manifest_path=repo_root / "manifest.yml",
        workspace_template=str(repo_root / "work-{n}"),
    )


def test_build_run_command(tmp_path):
    repo_root = _setup_repo(tmp_path)
    session = _session(repo_root)
    cmd = build_run_command(session, repo_root=repo_root)
    assert cmd[:4] == ["uv", "run", "python", "-m"]
    assert "orchestrator.run_container" in cmd
    assert "--workspace" in cmd and str(session.workspace) in cmd
    assert "--ssh-key" in cmd and str(session.ssh_key) in cmd
    assert "--env-file" in cmd and str(session.env_file) in cmd


def test_launch_session_records_state(tmp_path):
    repo_root = _setup_repo(tmp_path)
    session = _session(repo_root)
    state, command = launch_session(session, repo_root=repo_root, execute=False)

    state_path = repo_root / "outputs" / "agents" / session.role / session.id / "state.json"
    assert state_path.exists()
    raw = json.loads(state_path.read_text())
    assert raw["id"] == session.id
    assert raw["status"] == "planned"
    assert raw["dry_run"] is True
    assert command[:4] == ["uv", "run", "python", "-m"]
    assert "orchestrator.run_container" in command
    # workspace should resolve via template if original does not exist
    assert session.workspace.name.startswith("work-")


def test_resume_plan_reads_recorded_states(tmp_path):
    repo_root = _setup_repo(tmp_path)
    session = _session(repo_root)
    launch_session(session, repo_root=repo_root, execute=False)

    plans = resume_plan(repo_root=repo_root)
    assert len(plans) == 1
    assert plans[0]["session_id"] == "alpha"
    assert plans[0]["role"] == "FEATURE"
