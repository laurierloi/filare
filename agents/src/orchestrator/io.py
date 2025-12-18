from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class IoTarget:
    """Container + tmux session metadata for routing messages."""

    container: str
    tmux_session: str


def build_send_command(target: IoTarget, message: str) -> List[str]:
    """Construct the docker exec command to send a line into a tmux session."""
    return [
        "docker",
        "exec",
        "-i",
        target.container,
        "tmux",
        "send-keys",
        "-t",
        target.tmux_session,
        message,
        "Enter",
    ]


def build_snapshot_command(target: IoTarget) -> List[str]:
    """Construct the docker exec command to capture tmux pane output once."""
    return [
        "docker",
        "exec",
        "-i",
        target.container,
        "tmux",
        "capture-pane",
        "-p",
        "-t",
        target.tmux_session,
    ]


def send_message(target: IoTarget, message: str, execute: bool = True) -> List[str]:
    """Send a message; returns the command used (executes when requested)."""
    cmd = build_send_command(target, message)
    if execute:
        subprocess.run(cmd, check=True)
    return cmd


def snapshot_transcript(target: IoTarget, execute: bool = True) -> subprocess.CompletedProcess[str] | List[str]:
    """Capture current tmux pane output; returns process (or command when dry)."""
    cmd = build_snapshot_command(target)
    if not execute:
        return cmd
    return subprocess.run(cmd, check=True, capture_output=True, text=True)
