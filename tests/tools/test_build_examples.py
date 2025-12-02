from pathlib import Path

from filare.tools import build_examples


def test_build_generated_writes_readme_and_uses_output_dir(tmp_path, monkeypatch):
    # Arrange temporary example set
    examples_dir = tmp_path / "examples"
    examples_dir.mkdir()
    (examples_dir / "metadata.yml").write_text("title: demo\n")
    (examples_dir / "ex01.yml").write_text("connectors: {}\n")
    (examples_dir / "ex01.md").write_text("## Example 01\n\nDescription\n")

    captured = []

    def fake_cli(args):
        captured.append(args)
        return 0

    monkeypatch.setattr(build_examples, "cli", fake_cli)
    monkeypatch.setattr(
        build_examples,
        "groups",
        {
            "examples": {
                "path": examples_dir,
                "prefix": "ex",
                build_examples.readme: ["md", "yml"],
                "title": "Example Gallery",
            }
        },
    )

    output_dir = tmp_path / "outputs"

    # Act
    build_examples.build_generated(["examples"], output_base=output_dir)

    # Assert CLI called with output dir and metadata
    assert captured, "cli should be invoked for the examples group"
    args = captured[0]
    assert "--output-dir" in args
    assert str(output_dir / "examples") in {str(a) for a in args}

    # Readme is generated in the output directory with TSV links
    readme_path = output_dir / "examples" / build_examples.readme
    assert readme_path.exists()
    content = readme_path.read_text()
    assert "[Bill of Materials](ex01.tsv)" in content
