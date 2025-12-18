import pytest
from typer.testing import CliRunner

from filare.cli import cli
from filare.tools import build_examples


@pytest.mark.functional
def test_examples_cli_build_calls_tool(monkeypatch, tmp_path):
    runner = CliRunner()
    calls = {}

    def fake_build(groups, output_base=None):
        calls["groups"] = list(groups)
        calls["output_base"] = output_base

    monkeypatch.setattr(build_examples, "build_generated", fake_build)

    result = runner.invoke(
        cli,
        [
            "ex",
            "--action",
            "build",
            "--groups",
            "basic",
            "minimal-document",
            "--output-dir",
            str(tmp_path),
        ],
    )

    assert result.exit_code == 0, result.output
    assert calls["groups"] == ["basic", "minimal-document"]
    assert calls["output_base"] == tmp_path


@pytest.mark.functional
def test_examples_cli_clean_calls_tool(monkeypatch):
    runner = CliRunner()
    calls = {}

    def fake_clean(groups):
        calls["groups"] = list(groups)

    monkeypatch.setattr(build_examples, "clean_generated", fake_clean)

    result = runner.invoke(
        cli,
        [
            "ex",
            "--action",
            "clean",
            "--groups",
            "demos",
        ],
    )

    assert result.exit_code == 0, result.output
    assert calls["groups"] == ["demos"]
