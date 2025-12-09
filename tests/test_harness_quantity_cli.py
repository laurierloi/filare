from pathlib import Path

from typer.testing import CliRunner

from filare.cli.qty import app as qty_multipliers


def test_qty_multipliers_cli_reads_existing(tmp_path: Path):
    harness = tmp_path / "H1.yml"
    harness.write_text("connectors: {}")
    qty_file = tmp_path / "quantity_multipliers.txt"
    qty_file.write_text('{"H1": 2}')

    runner = CliRunner()
    result = runner.invoke(
        qty_multipliers,
        ["--multiplier-file-name", "quantity_multipliers.txt", str(harness)],
    )
    assert result.exit_code == 0


def test_qty_multipliers_cli_force_new(tmp_path: Path):
    harness = tmp_path / "H1.yml"
    harness.write_text("connectors: {}")
    qty_file = tmp_path / "quantity_multipliers.txt"
    qty_file.write_text('{"H1": 2}')

    runner = CliRunner()
    result = runner.invoke(
        qty_multipliers,
        [
            "--multiplier-file-name",
            "quantity_multipliers.txt",
            "--force-new",
            str(harness),
        ],
        input="1\n",
    )
    assert result.exit_code == 0
    # file should be recreated with prompted multiplier
    assert '"H1": 1' in qty_file.read_text()
