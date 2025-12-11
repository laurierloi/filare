import textwrap
from pathlib import Path

import yaml
from typer.testing import CliRunner

from filare.cli import cli


def _make_file(tmp_path: Path, name: str, content: str = "") -> Path:
    path = tmp_path / name
    path.write_text(content)
    return path


def test_drawio_validate_and_import(tmp_path):
    runner = CliRunner()
    diagram = _make_file(tmp_path, "diagram.drawio", "<xml/>")
    rules = _make_file(tmp_path, "rules.yml", "rules: {}")

    res_validate = runner.invoke(cli, ["drawio", "validate", str(diagram), "--rules", str(rules), "--format", "json"])
    assert res_validate.exit_code == 0, res_validate.output

    mapping = _make_file(tmp_path, "mapping.yml", "mapping: {}")
    res_import = runner.invoke(
        cli,
        ["drawio", "import", str(diagram), "--mapping", str(mapping), "--output", str(tmp_path / "out.yml")],
    )
    assert res_import.exit_code == 0, res_import.output
    assert (tmp_path / "out.yml").exists()


def test_drawio_export_and_sync(tmp_path):
    runner = CliRunner()
    harness = _make_file(tmp_path, "harness.yml", "harness: {}")
    template = _make_file(tmp_path, "template.drawio", "<xml/>")
    style = _make_file(tmp_path, "style.yml", "style: {}")
    export_out = tmp_path / "export.drawio"

    res_export = runner.invoke(
        cli,
        [
            "drawio",
            "export",
            str(harness),
            "--template",
            str(template),
            "--style",
            str(style),
            "--output",
            str(export_out),
        ],
    )
    assert res_export.exit_code == 0, res_export.output
    assert export_out.exists()

    diagram = _make_file(tmp_path, "diagram.drawio", "<xml/>")
    backup = tmp_path / "diagram.bak"
    report = tmp_path / "sync.json"
    res_sync = runner.invoke(
        cli,
        [
            "drawio",
            "sync",
            str(harness),
            str(diagram),
            "--direction",
            "to-drawio",
            "--backup",
            str(backup),
            "--report",
            str(report),
        ],
    )
    assert res_sync.exit_code == 0, res_sync.output
    assert backup.exists()
    assert report.exists()
    data = yaml.safe_load(report.read_text()) if report.exists() else {}
    assert data.get("direction") == "to-drawio"


def test_drawio_edit_and_review(tmp_path):
    runner = CliRunner()
    diagram = _make_file(tmp_path, "diagram.drawio", "<xml/>")

    editor_script = tmp_path / "editor.sh"
    editor_script.write_text("#!/bin/sh\nexit 0\n")
    editor_script.chmod(0o755)

    res_edit = runner.invoke(
        cli,
        [
            "drawio",
            "edit",
            str(diagram),
            "--editor",
            str(editor_script),
            "--no-validate",
        ],
    )
    assert res_edit.exit_code == 0, res_edit.output

    comments_path = tmp_path / "comments.txt"
    review_editor = tmp_path / "review.sh"
    review_editor.write_text("#!/bin/sh\nexit 0\n")
    review_editor.chmod(0o755)
    res_review = runner.invoke(
        cli,
        [
            "drawio",
            "review",
            str(diagram),
            "--comments-path",
            str(comments_path),
            "--editor",
            str(review_editor),
            "--format",
            "json",
        ],
        input="Looks good\n",
    )
    assert res_review.exit_code == 0, res_review.output
    assert comments_path.exists()
    assert "ok" in res_review.output
