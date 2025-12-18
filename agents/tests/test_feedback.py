import json
from pathlib import Path

import pytest

from orchestrator.feedback import Prompt, add_prompt, list_prompts, resolve_prompt

pytestmark = pytest.mark.agent


def test_add_and_list_prompts(tmp_path):
    queue = tmp_path / "queue.json"
    prompt = Prompt(
        id="p1",
        session_id="s1",
        role="TOOLS",
        workspace="/work",
        branch="main",
        reason="network",
        requested_action="allow network",
    )
    add_prompt(queue, prompt)
    prompts = list_prompts(queue)
    assert len(prompts) == 1
    assert prompts[0].id == "p1"
    raw = json.loads(queue.read_text())
    assert raw[0]["id"] == "p1"


def test_resolve_prompt(tmp_path):
    queue = tmp_path / "queue.json"
    prompt = Prompt(
        id="p1",
        session_id="s1",
        role="TOOLS",
        workspace="/work",
        branch="main",
        reason="network",
        requested_action="allow network",
    )
    add_prompt(queue, prompt)
    resolved = resolve_prompt(queue, "p1", decision="approved", reply="ok")
    assert resolved.decision == "approved"
    assert resolved.reply == "ok"
    prompts = list_prompts(queue)
    assert prompts[0].decision == "approved"
