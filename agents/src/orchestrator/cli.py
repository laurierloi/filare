from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from .config import ManifestError, load_manifest, select_sessions
from .runtime import find_repo_root, launch_session, resume_plan

app = typer.Typer(help="Orchestrate codex agent containers (manifest-driven).")


def _print_session_summary(manifest_path: Path, sessions) -> None:
    typer.echo(f"Loaded manifest: {manifest_path}")
    for session in sessions:
        typer.echo(
            f"- {session.id} role={session.role} branch={session.branch} workspace={session.workspace} image={session.image}"
        )


@app.command()
def validate(manifest: Path, session: Optional[str] = typer.Option(None, help="Limit to one session id")) -> None:
    """Validate a manifest and print the resolved sessions."""
    try:
        sessions = load_manifest(manifest)
        sessions = select_sessions(sessions, session)
    except ManifestError as exc:
        typer.secho(f"Manifest error: {exc}", fg=typer.colors.RED)
        raise typer.Exit(code=1) from exc

    _print_session_summary(manifest, sessions)
    typer.secho("Manifest validated.", fg=typer.colors.GREEN)


@app.command()
def start(
    manifest: Path,
    session: Optional[str] = typer.Option(None, help="Limit to one session id"),
    execute: bool = typer.Option(False, "--execute", help="Actually launch docker; defaults to dry-run"),
) -> None:
    """Plan or start agent containers based on a manifest."""
    try:
        sessions = select_sessions(load_manifest(manifest), session)
    except ManifestError as exc:
        typer.secho(f"Manifest error: {exc}", fg=typer.colors.RED)
        raise typer.Exit(code=1) from exc

    repo_root = find_repo_root(manifest.parent)
    _print_session_summary(manifest, sessions)

    for session_cfg in sessions:
        state, command = launch_session(session_cfg, repo_root=repo_root, execute=execute)
        mode = "EXECUTE" if execute else "DRY-RUN"
        typer.echo(f"[{mode}] session={session_cfg.id} state={state.status}")
        typer.echo("Command:")
        typer.echo("  " + " ".join(command))
        typer.echo(f"State recorded at outputs/agents/{session_cfg.role}/{session_cfg.id}/state.json")


@app.command("resume-all")
def resume_all() -> None:
    """Show how to reconnect to previously recorded sessions."""
    plans = resume_plan()
    if not plans:
        typer.echo("No recorded sessions found under outputs/agents.")
        raise typer.Exit(code=0)

    typer.echo("Reconnect plan (run from repo root):")
    for plan in plans:
        typer.echo(
            f"- session={plan['session_id']} role={plan['role']} branch={plan['branch']} workspace={plan['workspace']}"
        )
        typer.echo("  hint: docker ps | grep <id> && docker exec -it <cid> tmux attach -t <id>")


if __name__ == "__main__":
    app()
