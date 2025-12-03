import logging
from pathlib import Path

import yaml

from filare.flows.build_harness import build_harness_from_files


def test_document_representation_written(tmp_path: Path, caplog):
    caplog.set_level(logging.WARNING)
    harness_path = tmp_path / "h.yml"
    metadata_path = tmp_path / "m.yml"
    harness_path.write_text(
        "connectors:\n  J1:\n    pincount: 1\nconnections:\n  -\n    - J1: [1]\n"
    )
    metadata_path.write_text(
        "metadata:\n"
        "  pn: T\n"
        "  company: ACME\n"
        "  address: 1 Road\n"
        "  sheet_total: 1\n"
        "  sheet_current: 1\n"
        "  sheet_name: S\n"
        "  output_dir: .\n"
        "  titlepage: t\n"
        "  output_names: [h]\n"
        "  files: [h.yml]\n"
        "  use_qty_multipliers: false\n"
        "  multiplier_file_name: qty.txt\n"
    )

    build_harness_from_files(
        [harness_path],
        [metadata_path],
        output_formats=(),
        output_dir=tmp_path,
        return_types=("document",),
    )

    doc_path = tmp_path / "h.document.yaml"
    registry = tmp_path / "document_hashes.yaml"
    assert doc_path.exists()
    assert registry.exists()


def test_document_representation_not_overwritten_on_user_edit(tmp_path: Path, caplog):
    caplog.set_level(logging.WARNING)
    harness_path = tmp_path / "h.yml"
    metadata_path = tmp_path / "m.yml"
    harness_path.write_text(
        "connectors:\n  J1:\n    pincount: 1\nconnections:\n  -\n    - J1: [1]\n"
    )
    metadata_path.write_text(
        "metadata:\n"
        "  pn: T\n"
        "  company: ACME\n"
        "  address: 1 Road\n"
        "  sheet_total: 1\n"
        "  sheet_current: 1\n"
        "  sheet_name: S\n"
        "  output_dir: .\n"
        "  titlepage: t\n"
        "  output_names: [h]\n"
        "  files: [h.yml]\n"
        "  use_qty_multipliers: false\n"
        "  multiplier_file_name: qty.txt\n"
    )

    # First run writes doc + hash
    build_harness_from_files(
        [harness_path],
        [metadata_path],
        output_formats=(),
        output_dir=tmp_path,
        return_types=("document",),
    )

    doc_path = tmp_path / "h.document.yaml"
    registry = tmp_path / "document_hashes.yaml"
    # User edits document
    content = yaml.safe_load(doc_path.read_text())
    content["metadata"]["pn"] = "USER_EDIT"
    doc_path.write_text(yaml.safe_dump(content))

    # Second run should warn and not overwrite
    caplog.clear()
    build_harness_from_files(
        [harness_path],
        [metadata_path],
        output_formats=(),
        output_dir=tmp_path,
        return_types=("document",),
    )
    assert any("skipping overwrite" in rec.message for rec in caplog.records)
    reloaded = yaml.safe_load(doc_path.read_text())
    assert reloaded["metadata"]["pn"] == "USER_EDIT"
