from pathlib import Path

from filare.parser.harness_parser import parse_harness_files, parse_metadata_files


def test_parse_metadata_files(tmp_path):
    meta = tmp_path / "meta.yml"
    meta.write_text("meta: 1")
    result = parse_metadata_files([meta])
    assert result["meta"] == "1"


def test_parse_harness_files_combines_components_and_harness(tmp_path):
    comp = tmp_path / "components.yml"
    harness = tmp_path / "harness.yml"
    meta = tmp_path / "meta.yml"
    comp.write_text("connectors:\n  X1:\n    pincount: 2\n")
    harness.write_text("connections: []")
    meta.write_text("metadata:\n  title: test")
    result = parse_harness_files((comp,), (harness,), (meta,))
    assert result["metadata"]["title"] == "test"
    assert "connectors" in result


def test_parse_metadata_files_handles_empty(tmp_path):
    result = parse_metadata_files([])
    assert result == {}
