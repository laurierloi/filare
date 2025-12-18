from typer.testing import CliRunner

from filare.cli import cli
from filare.tools import text_overlap


def test_overlap_cli_passes_arguments(monkeypatch, tmp_path):
    runner = CliRunner()
    called = {}

    def fake_main(argv):
        called["argv"] = argv
        return 0

    monkeypatch.setattr(text_overlap, "main", fake_main)

    html_file = tmp_path / "page.html"
    html_file.write_text("<html></html>")
    json_path = tmp_path / "report.json"

    result = runner.invoke(
        cli,
        [
            "overlap",
            str(html_file),
            "--viewport",
            "1024x768",
            "--warn-threshold",
            "1.5",
            "--error-threshold",
            "3.0",
            "--json",
            str(json_path),
            "--ignore-selector",
            ".legend",
            "--ignore-text",
            "Draft",
            "--config",
            str(tmp_path / "config.yml"),
        ],
    )

    assert result.exit_code == 0, result.output
    argv = called["argv"]
    assert str(html_file) in argv
    assert "--viewport" in argv and "1024x768" in argv
    assert "--warn-threshold" in argv and "1.5" in argv
    assert "--error-threshold" in argv and "3.0" in argv
    assert "--json" in argv and str(json_path) in argv
    assert "--ignore-selector" in argv and ".legend" in argv
    assert "--ignore-text" in argv and "Draft" in argv
    assert "--config" in argv and str(tmp_path / "config.yml") in argv
