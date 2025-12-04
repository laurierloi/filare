from pathlib import Path

from click.testing import CliRunner

from filare.models.harness_quantity import qty_multipliers


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
