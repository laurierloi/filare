import textwrap

import yaml
from typer.testing import CliRunner

from filare.cli import cli


def _write_metadata(tmp_path, name, content):
    path = tmp_path / name
    path.write_text(textwrap.dedent(content))
    return path


def test_metadata_validate_and_describe(tmp_path):
    runner = CliRunner()
    meta = _write_metadata(
        tmp_path,
        "meta.yml",
        """
        pn: PN-1
        title: Demo
        company: TestCo
        """,
    )

    result_ok = runner.invoke(cli, ["metadata", "validate", str(meta)])
    assert result_ok.exit_code == 0, result_ok.output

    described = runner.invoke(cli, ["metadata", "describe", str(meta), "--format", "yaml"])
    assert described.exit_code == 0, described.output
    data = yaml.safe_load(described.output)
    assert data["pn"] == "PN-1"
    assert data["title"] == "Demo"

    invalid = _write_metadata(tmp_path, "invalid.yml", "- not-a-mapping")
    result_bad = runner.invoke(cli, ["metadata", "validate", str(invalid)])
    assert result_bad.exit_code != 0


def test_metadata_merge_and_source(tmp_path):
    runner = CliRunner()
    base = _write_metadata(
        tmp_path,
        "base.yml",
        """
        metadata:
          pn: BASE
          title: BaseTitle
        """,
    )
    override = _write_metadata(
        tmp_path,
        "override.yml",
        """
        metadata:
          title: OverrideTitle
          authors:
            Lead:
              name: Alice
        """,
    )

    result = runner.invoke(
        cli,
        ["metadata", "merge", str(base), str(override), "--format", "yaml", "--show-source"],
    )
    assert result.exit_code == 0, result.output
    merged = yaml.safe_load(result.output)
    assert merged["metadata"]["title"] == "OverrideTitle"
    assert merged["metadata"]["pn"] == "BASE"
    assert merged["__source__"]["metadata"].endswith("override.yml")

    out_path = tmp_path / "merged.yml"
    to_file = runner.invoke(
        cli,
        [
            "metadata",
            "merge",
            str(base),
            str(override),
            "--output",
            str(out_path),
        ],
    )
    assert to_file.exit_code == 0, to_file.output
    assert out_path.exists()


def test_metadata_edit_invokes_editor_and_validates(tmp_path):
    runner = CliRunner()
    meta = _write_metadata(
        tmp_path,
        "edit.yml",
        """
        pn: EDIT-1
        """,
    )

    editor_script = tmp_path / "edit.sh"
    editor_script.write_text("#!/bin/sh\necho \"title: Added\" >> \"$1\"\n")
    editor_script.chmod(0o755)

    result = runner.invoke(
        cli,
        ["metadata", "edit", str(meta), "--strict", "--editor", str(editor_script)],
    )
    assert result.exit_code == 0, result.output
    updated = yaml.safe_load(meta.read_text())
    assert updated["title"] == "Added"
