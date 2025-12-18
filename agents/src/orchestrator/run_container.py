from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

import typer

from .runtime import find_repo_root

app = typer.Typer(help="Launch the codex container with sensible defaults.")


def _copy_tree(src: Path, dst: Path) -> None:
    """Recursively copy contents of src into dst (dst may already exist)."""
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


@app.command()
def run_container(
    workspace: Path = typer.Option(..., "--workspace", help="Host workspace to bind to /home/agent/workspace"),
    ssh_key: Path = typer.Option(..., "--ssh-key", help="SSH private key to mount read-only"),
    env_file: Path = typer.Option(..., "--env-file", help=".env file with agent environment variables"),
    image: str = typer.Option("filare-codex", "--image", help="Docker image name"),
    seed_from: Optional[Path] = typer.Option(None, "--seed-from", help="If workspace is empty, seed from this path"),
    codex_dir: Optional[Path] = typer.Option(None, "--codex-dir", help="Host .codex cache directory"),
    ssh_temp_dir: Optional[Path] = typer.Option(
        None,
        "--ssh-temp-dir",
        help="Directory for temporary SSH mount; defaults to <workspace>/.orchestrator/tmp to avoid /tmp pressure",
    ),
    session_id: Optional[str] = typer.Option(None, "--session-id", help="Session id label"),
    role: Optional[str] = typer.Option(None, "--role", help="Role label"),
    branch: Optional[str] = typer.Option(None, "--branch", help="Branch label"),
) -> None:
    """
    Run the codex container with the given workspace, SSH key, and env file.

    Mirrors scripts/run_codex_container.sh but implemented in Python for easier reuse.
    """
    workspace = workspace.expanduser().resolve()
    ssh_key = ssh_key.expanduser().resolve()
    env_file = env_file.expanduser().resolve()
    seed_from = seed_from.expanduser().resolve() if seed_from else None
    codex_dir = (codex_dir.expanduser().resolve() if codex_dir else Path.home() / ".codex")

    if not ssh_key.is_file():
        raise typer.BadParameter(f"SSH key not found: {ssh_key}")
    if not env_file.is_file():
        raise typer.BadParameter(f"Env file not found: {env_file}")

    workspace.mkdir(parents=True, exist_ok=True)
    if not any(workspace.iterdir()):
        source = seed_from
        if source is None:
            try:
                source = find_repo_root()
            except Exception:
                source = Path.cwd()
        typer.echo(f"Seeding empty workspace from {source} -> {workspace}")
        _copy_tree(source, workspace)

    codex_dir.mkdir(parents=True, exist_ok=True)

    # Prefer a workspace-local temp area to avoid /tmp exhaustion
    tmp_base = ssh_temp_dir.expanduser().resolve() if ssh_temp_dir else (workspace / ".orchestrator" / "tmp")
    tmp_base.mkdir(parents=True, exist_ok=True)
    ssh_tmp = Path(tempfile.mkdtemp(prefix="codex-ssh-", dir=tmp_base))
    try:
        os.chmod(ssh_tmp, 0o700)
        ssh_target = ssh_tmp / "id_rsa"
        shutil.copy2(ssh_key, ssh_target)
        os.chmod(ssh_target, 0o600)

        cmd = [
            "docker",
            "run",
            "--rm",
            "-it",
            "-v",
            f"{workspace}:/home/agent/workspace",
            "-v",
            f"{codex_dir}:/home/agent/.codex",
            "-v",
            f"{ssh_tmp}:/home/agent/.ssh",
            "--env-file",
            str(env_file),
            "-e",
            "HOME=/home/agent",
            "-w",
            "/home/agent/workspace",
            "--user",
            f"{os.getuid()}:{os.getgid()}",
        ]

        labels = {
            "filare.session": session_id,
            "filare.role": role,
            "filare.branch": branch,
        }
        for key, value in labels.items():
            if value:
                cmd.extend(["--label", f"{key}={value}"])

        cmd.extend([image, "bash"])

        typer.echo("Running container:")
        typer.echo("  " + " ".join(cmd))
        subprocess.run(cmd, check=True)
    finally:
        shutil.rmtree(ssh_tmp, ignore_errors=True)


if __name__ == "__main__":
    app()
