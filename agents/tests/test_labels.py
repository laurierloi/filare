import pytest

from orchestrator.docker_util import docker_ps

pytestmark = pytest.mark.agent


def test_docker_ps_builds_filters(monkeypatch):
    calls = []

    def fake_run(cmd, check, capture_output, text):
        calls.append(cmd)
        class Result:
            stdout = ""
        return Result()

    monkeypatch.setattr("subprocess.run", fake_run)
    docker_ps({"filare.session": "s1", "filare.role": "FEATURE"})
    assert calls
    cmd = calls[0]
    assert "label=filare.session=s1" in cmd
    assert "label=filare.role=FEATURE" in cmd
