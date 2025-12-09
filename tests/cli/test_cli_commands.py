import textwrap

import pytest
from typer.testing import CliRunner

from filare import APP_NAME, __version__
from filare.cli import cli


def _write_minimal_files(tmp_path):
    metadata_path = tmp_path / "metadata.yml"
    metadata_path.write_text(
        textwrap.dedent(
            """\
            metadata:
              pn: TEST
              company: TestCo
              address: Test Street
              authors: {}
              revisions: {}
              template:
                name: din-6771
                sheetsize: A4
            """
        )
    )

    harness_path = tmp_path / "h.yml"
    harness_path.write_text(
        textwrap.dedent(
            """\
            connectors:
              J1:
                pincount: 2
              J2:
                pincount: 2

            cables:
              W1:
                wirecount: 2

            connections:
              -
                - J1: [1, 2]
                - W1: [1, 2]
                - J2: [1, 2]
            """
        )
    )

    return harness_path, metadata_path


def test_cli_help_succeeds():
    runner = CliRunner()
    result = runner.invoke(cli, ["run", "--help"])
    assert result.exit_code == 0
    assert "Output formats" in result.output


def test_cli_version_prints(tmp_path):
    runner = CliRunner()
    dummy_file = tmp_path / "dummy.yml"
    dummy_file.write_text("connectors: {}")  # satisfies required files arg

    result = runner.invoke(cli, ["run", "-V", str(dummy_file)])
    assert result.exit_code == 0
    assert APP_NAME in result.output
    assert __version__ in result.output


@pytest.mark.functional
def test_cli_generates_outputs(tmp_path):
    runner = CliRunner()
    harness_path, metadata_path = _write_minimal_files(tmp_path)

    result = runner.invoke(
        cli,
        [
            "run",
            str(harness_path),
            "-d",
            str(metadata_path),
            "-f",
            "t",
            "-o",
            str(tmp_path),
        ],
    )

    assert result.exit_code == 0, result.output

    harness_tsv = tmp_path / f"{harness_path.stem}.tsv"
    assert harness_tsv.exists(), f"Missing CLI output {harness_tsv}"


def test_cli_pdf_and_shared_bom_flow(monkeypatch, tmp_path):
    runner = CliRunner()
    harness_path, _ = _write_minimal_files(tmp_path)

    calls = {}

    def fake_parse(components, metadata_files, return_types, output_formats, **kwargs):
        calls["parse_formats"] = set(output_formats)
        shared_bom = kwargs["shared_bom"]
        shared_bom["h"] = {"qty": 1}
        return {"shared_bom": shared_bom}

    def fake_shared_bom(**_kwargs):
        calls["shared_bom"] = True
        return tmp_path / "shared.tsv"

    def fake_titlepage(metadata, extra_metadata, shared_bom, for_pdf=False):
        calls.setdefault("titlepages", []).append(for_pdf)

    def fake_pdf_bundle(paths):
        calls["pdf_bundle"] = list(paths)

    monkeypatch.setattr("filare.cli.render.wv.parse", fake_parse)
    monkeypatch.setattr("filare.cli.render.build_shared_bom", fake_shared_bom)
    monkeypatch.setattr("filare.cli.render.build_titlepage", fake_titlepage)
    monkeypatch.setattr("filare.cli.render.build_pdf_bundle", fake_pdf_bundle)

    result = runner.invoke(
        cli,
        [
            "run",
            str(harness_path),
            "-f",
            "Phb",
            "-o",
            str(tmp_path),
        ],
    )

    assert result.exit_code == 0, result.output
    assert "pdf" not in calls["parse_formats"]  # pdf is stripped before parse
    assert calls["shared_bom"] is True
    assert calls["titlepages"] == [False, True]  # html + pdf titlepages
    assert calls["pdf_bundle"] and calls["pdf_bundle"][0].name.startswith("titlepage")
