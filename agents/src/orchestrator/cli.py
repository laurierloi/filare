from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from .config import ManifestError, load_manifest, select_sessions
from .dashboard import collect_dashboard, to_json
from .feedback import Prompt, add_prompt, list_prompts, resolve_prompt
from .io import IoTarget, send_message, snapshot_transcript
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


@app.command()
def send(
    container: str = typer.Option(..., "--container", help="Docker container name or ID"),
    session: str = typer.Option(..., "--session", help="tmux session name inside container"),
    text: str = typer.Argument(..., help="Text to send"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print command without executing"),
) -> None:
    """Send text to a running codex session (tmux) inside the container."""
    target = IoTarget(container=container, tmux_session=session)
    cmd = send_message(target, text, execute=not dry_run)
    if dry_run:
        typer.echo(" ".join(cmd))


@app.command()
def snapshot(
    container: str = typer.Option(..., "--container", help="Docker container name or ID"),
    session: str = typer.Option(..., "--session", help="tmux session name inside container"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print command without executing"),
) -> None:
    """Capture current tmux pane output for a running codex session."""
    target = IoTarget(container=container, tmux_session=session)
    result = snapshot_transcript(target, execute=not dry_run)
    if dry_run:
        typer.echo(" ".join(result))  # type: ignore[arg-type]
        return
    typer.echo(result.stdout)


@app.command("feedback-list")
def feedback_list(queue: Path = typer.Option(Path("outputs/agents/prompts.json"), "--queue", help="Queue file")) -> None:
    """List pending/decided prompts."""
    prompts = list_prompts(queue)
    if not prompts:
        typer.echo("No prompts recorded.")
        return
    for prompt in prompts:
        status = prompt.decision or "pending"
        typer.echo(f"- id={prompt.id} session={prompt.session_id} role={prompt.role} status={status} reason={prompt.reason}")


@app.command("feedback-add")
def feedback_add(
    prompt_id: str = typer.Option(..., "--id", help="Prompt id"),
    session_id: str = typer.Option(..., "--session-id", help="Session id"),
    role: str = typer.Option(..., "--role", help="Agent role"),
    workspace: str = typer.Option(..., "--workspace", help="Workspace path"),
    branch: str = typer.Option(..., "--branch", help="Branch name"),
    reason: str = typer.Option(..., "--reason", help="Reason for prompt"),
    requested_action: str = typer.Option(..., "--requested-action", help="Requested action"),
    suggested_reply: Optional[str] = typer.Option(None, "--suggested-reply", help="Suggested reply text"),
    severity: str = typer.Option("info", "--severity", help="Severity label"),
    queue: Path = typer.Option(Path("outputs/agents/prompts.json"), "--queue", help="Queue file"),
) -> None:
    """Insert a prompt into the queue (useful for tests/demo)."""
    prompt = Prompt(
        id=prompt_id,
        session_id=session_id,
        role=role,
        workspace=workspace,
        branch=branch,
        reason=reason,
        requested_action=requested_action,
        suggested_reply=suggested_reply,
        severity=severity,
    )
    add_prompt(queue, prompt)
    typer.echo(f"Added prompt {prompt_id} -> {queue}")


@app.command("feedback-resolve")
def feedback_resolve(
    prompt_id: str = typer.Option(..., "--id", help="Prompt id"),
    decision: str = typer.Option(..., "--decision", help="approved|rejected"),
    reply: Optional[str] = typer.Option(None, "--reply", help="Reply text"),
    queue: Path = typer.Option(Path("outputs/agents/prompts.json"), "--queue", help="Queue file"),
) -> None:
    """Resolve a prompt with a decision and optional reply."""
    if decision not in {"approved", "rejected"}:
        raise typer.BadParameter("decision must be approved|rejected")
    prompt = resolve_prompt(queue, prompt_id, decision=decision, reply=reply)  # type: ignore[arg-type]
    typer.echo(f"Updated prompt {prompt.id} decision={prompt.decision}")


@app.command("dashboard")
def dashboard(
    queue: Path = typer.Option(Path("outputs/agents/prompts.json"), "--queue", help="Prompt queue path"),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON instead of table"),
) -> None:
    """Show a snapshot of session registry + pending prompts."""
    entries = collect_dashboard(queue=queue)
    if json_output:
        typer.echo(to_json(entries))
        return
    if not entries:
        typer.echo("No sessions recorded.")
        return
    typer.echo("Sessions:")
    for entry in entries:
        typer.echo(
            f"- {entry.session_id} role={entry.role} branch={entry.branch} status={entry.status} prompts_pending={entry.prompts_pending} workspace={entry.workspace}"
        )


if __name__ == "__main__":
    app()
