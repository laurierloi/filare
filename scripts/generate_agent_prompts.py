#!/usr/bin/env python
"""Generate Codex prompt Markdown files from Filare agent command YAML.

This converts entries in agents/filare_commands.yml and agents/extra_commands.yml
into Codex-compatible prompt files (one per command). Each file contains YAML
frontmatter (description, argument-hint) followed by a short instruction block
that tells Codex how to run the associated command inside the repo.

Example:
    source scripts/agent-setup.sh >/dev/null && uv run python scripts/generate_agent_prompts.py
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List, Mapping

import yaml

PLACEHOLDER_RE = re.compile(r"\{([A-Za-z0-9_\-]+)\}")


def load_commands(path: Path) -> Dict[str, Mapping]:
    """Load a YAML command catalog file.

    The accepted structure matches agents/filare_commands.yml and
    agents/extra_commands.yml, both of which expose a top-level ``commands``
    mapping. Unknown top-level keys are ignored.
    """

    if not path.is_file():
        raise FileNotFoundError(f"Commands file not found: {path}")

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    commands = data.get("commands") or data.get("extra_commands") or {}
    if not isinstance(commands, dict):
        raise ValueError(f"Commands file has no 'commands' mapping: {path}")
    return commands


def merge_commands(
    primary: Mapping[str, Mapping], secondary: Mapping[str, Mapping]
) -> Dict[str, Mapping]:
    """Merge command mappings, letting secondary override primary on key clashes."""

    merged: Dict[str, Mapping] = {**primary}
    merged.update(secondary)
    return merged


def extract_placeholders(run_template: str) -> List[str]:
    """Return placeholder names (without braces) in order of appearance."""

    seen = []
    for match in PLACEHOLDER_RE.finditer(run_template):
        key = match.group(1)
        if key not in seen:
            seen.append(key)
    return seen


def substitute_placeholders(run_template: str, placeholders: List[str]) -> str:
    """Replace `{placeholder}` tokens with Codex-style `$PLACEHOLDER` variables."""

    substituted = run_template
    for key in placeholders:
        substituted = substituted.replace(f"{{{key}}}", f"${key.upper()}")
    return substituted


def normalize_run_command(command: str) -> str:
    """Collapse whitespace for nicer display while keeping semantics."""

    return " ".join(command.split())


def build_argument_hint(placeholders: List[str]) -> str | None:
    if not placeholders:
        return None
    return " ".join(f'{name.upper()}="<value>"' for name in placeholders)


def build_prompt_body(
    name: str,
    description: str | None,
    run_command: str,
    category: str | None,
    placeholders: List[str],
    safe_for_agents: bool,
) -> str:
    lines: List[str] = []

    if description:
        lines.append(description)
    lines.append(f"Category: {category or 'unspecified'}.")
    if not safe_for_agents:
        lines.append("Marked unsafe for automatic agents — confirm before running.")

    lines.append("")
    lines.append("Command to run inside the repo:")
    lines.append("```bash")
    lines.append(f"source scripts/agent-setup.sh >/dev/null && {run_command}")
    lines.append("```")

    if placeholders:
        hint = " ".join(f'{p.upper()}="..."' for p in placeholders)
        lines.append("")
        lines.append(
            "Provide the required arguments when invoking the slash command, e.g.:"
        )
        lines.append(f"/prompts:{name} {hint}")

    lines.append(
        "After execution, summarize the outcome succinctly and mention any errors or next steps."
    )

    return "\n".join(lines).rstrip() + "\n"


def write_prompt_file(
    output_dir: Path,
    name: str,
    description: str | None,
    argument_hint: str | None,
    body: str,
) -> None:
    metadata = {"description": description or name}
    if argument_hint:
        metadata["argument-hint"] = argument_hint

    frontmatter = yaml.safe_dump(metadata, sort_keys=False).strip()
    content = f"---\n{frontmatter}\n---\n\n{body}"

    outfile = output_dir / f"{name}.md"
    outfile.write_text(content, encoding="utf-8")


def generate_prompts(
    filare_commands_path: Path,
    extra_commands_path: Path | None,
    output_dir: Path,
) -> int:
    base_commands = load_commands(filare_commands_path)
    all_commands = dict(base_commands)

    if extra_commands_path:
        extra_commands = load_commands(extra_commands_path)
        all_commands = merge_commands(all_commands, extra_commands)

    output_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    for name in sorted(all_commands.keys()):
        cmd = all_commands[name] or {}
        raw_description = cmd.get("description")
        description = (
            raw_description.strip() if isinstance(raw_description, str) else None
        )
        category = cmd.get("category")
        safe_for_agents = bool(cmd.get("safe_for_agents", True))
        run_template = cmd.get("run")
        if not run_template:
            # Skip entries without a runnable command
            continue

        placeholders = extract_placeholders(run_template)
        run_command = substitute_placeholders(run_template, placeholders)
        run_command = normalize_run_command(run_command)
        argument_hint = build_argument_hint(placeholders)

        body = build_prompt_body(
            name=name,
            description=description,
            run_command=run_command,
            category=category,
            placeholders=placeholders,
            safe_for_agents=safe_for_agents,
        )

        write_prompt_file(
            output_dir=output_dir,
            name=name,
            description=description,
            argument_hint=argument_hint,
            body=body,
        )
        count += 1

    return count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Codex slash-command prompts from agent command YAML files.",
    )
    parser.add_argument(
        "--filare-commands",
        type=Path,
        default=Path("agents/filare_commands.yml"),
        help="Path to filare_commands.yml (default: agents/filare_commands.yml)",
    )
    parser.add_argument(
        "--extra-commands",
        type=Path,
        default=Path("agents/extra_commands.yml"),
        help="Path to extra_commands.yml (default: agents/extra_commands.yml)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("agents/prompts"),
        help="Directory to write generated prompt Markdown files (default: agents/prompts)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    count = generate_prompts(
        filare_commands_path=args.filare_commands,
        extra_commands_path=args.extra_commands,
        output_dir=args.output_dir,
    )
    print(f"Generated {count} prompt files in {args.output_dir}")


if __name__ == "__main__":
    main()
