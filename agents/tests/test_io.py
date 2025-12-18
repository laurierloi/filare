import pytest

from orchestrator.io import IoTarget, build_send_command, build_snapshot_command

pytestmark = pytest.mark.agent


def test_build_send_command():
    target = IoTarget(container="cid123", tmux_session="s1")
    cmd = build_send_command(target, "hello world")
    assert cmd[:5] == ["docker", "exec", "-i", "cid123", "tmux"]
    assert cmd[-3:] == ["s1", "hello world", "Enter"]


def test_build_snapshot_command():
    target = IoTarget(container="cid123", tmux_session="s1")
    cmd = build_snapshot_command(target)
    assert cmd == ["docker", "exec", "-i", "cid123", "tmux", "capture-pane", "-p", "-t", "s1"]
