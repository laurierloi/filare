import textwrap

from click.testing import CliRunner

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
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Output formats" in result.output


def test_cli_version_prints(tmp_path):
    runner = CliRunner()
    dummy_file = tmp_path / "dummy.yml"
    dummy_file.write_text("connectors: {}")  # satisfies required files arg

    result = runner.invoke(cli, ["-V", str(dummy_file)])
    assert result.exit_code == 0
    assert APP_NAME in result.output
    assert __version__ in result.output


def test_cli_generates_outputs(tmp_path):
    runner = CliRunner()
    harness_path, metadata_path = _write_minimal_files(tmp_path)

    result = runner.invoke(
        cli,
        [str(harness_path), "-d", str(metadata_path), "-f", "t", "-o", str(tmp_path)],
    )

    assert result.exit_code == 0, result.output

    harness_tsv = tmp_path / f"{harness_path.stem}.tsv"
    assert harness_tsv.exists(), f"Missing CLI output {harness_tsv}"
