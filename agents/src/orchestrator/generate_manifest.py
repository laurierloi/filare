from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

import typer
import yaml

from .config import render_manifest

app = typer.Typer(help="Generate an orchestrator manifest from defaults and context.")


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text()) or {}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def _load_context(path: Path) -> str:
    return Path(path).read_text()


@app.command()
def generate(
    base: Path = typer.Option(..., "--base", help="Base manifest defaults (YAML with defaults block)"),
    output: Path = typer.Option(..., "--output", help="Output manifest path"),
    role: str = typer.Option(..., "--role", help="Agent role (e.g., FEATURE/FIXER/DOCUMENTATION)"),
    branch: str = typer.Option(..., "--branch", help="Branch name for this session"),
    session_id: str = typer.Option(..., "--id", help="Session id"),
    goal_file: Optional[Path] = typer.Option(None, "--goal-file", help="File containing goal/description"),
    context_file: Optional[Path] = typer.Option(None, "--context-file", help="Additional context file to pass as metadata"),
    issues: List[Path] = typer.Option([], "--issue", help="Issue/feature files to attach as metadata"),
) -> None:
    """Generate a manifest from a base defaults file and task-specific inputs."""
    base_data = _load_yaml(base)
    defaults = base_data.get("defaults") or {}

    goal = _load_context(goal_file) if goal_file else None
    extra = {}
    if context_file:
        extra["context"] = _load_context(context_file)
    if issues:
        extra["issues"] = [path.read_text() for path in issues]

    session_entry = {
        "id": session_id,
        "role": role,
        "branch": branch,
    }
    if goal:
        session_entry["goal"] = goal.strip()
    if extra:
        session_entry["metadata"] = extra

    manifest_yaml = render_manifest(defaults, [session_entry])
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(manifest_yaml)
    typer.echo(f"Wrote manifest to {output}")


if __name__ == "__main__":
    app()
