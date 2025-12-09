from pathlib import Path

import yaml

from filare.tools import build_examples


def test_build_examples_build_and_clean(tmp_path, monkeypatch):
    # Set up minimal group with one example and metadata
    examples_dir = tmp_path / "examples"
    examples_dir.mkdir()
    (examples_dir / "metadata.yml").write_text("metadata:\n  pn: T\n")
    ex_file = examples_dir / "ex01.yml"
    ex_file.write_text("connectors: {}")

    # stub cli to avoid heavy rendering
    monkeypatch.setattr(build_examples, "cli", lambda *args, **kwargs: None)
    original_groups = build_examples.groups.copy()
    build_examples.groups = {
        "temp": {
            "path": examples_dir,
            "prefix": "ex",
            build_examples.readme: [],
            "title": "Temp",
        }
    }

    try:
        build_examples.build_generated(["temp"])
        out_dir = examples_dir
        # manifest is always written
        manifest = out_dir / "document_manifest.yaml"
        assert manifest.exists()

        # create dummy generated file then clean
        dummy = out_dir / "ex01.html"
        dummy.write_text("html")
        build_examples.clean_generated(["temp"])
        assert not dummy.exists()
        assert not manifest.exists()
    finally:
        build_examples.groups = original_groups


def test_write_document_manifest_flags(tmp_path):
    out_dir = tmp_path / "out"
    nested = out_dir / "nested"
    nested.mkdir(parents=True)
    doc1 = out_dir / "doc1.document.yaml"
    doc1.write_text(
        "metadata:\n  pn: P1\nextras:\n  options:\n    split_bom_page: true\n"
        "    split_notes_page: true\n"
    )
    doc2 = nested / "doc2.document.yaml"
    doc2.write_text("extras:\n  options:\n    split_index_page: true\n")
    shared = out_dir / "shared_bom.tsv"
    shared.write_text("bom")

    build_examples._write_document_manifest(out_dir)

    manifest = yaml.safe_load((out_dir / "document_manifest.yaml").read_text())
    assert manifest["shared_bom"] == "shared_bom.tsv"
    assert manifest["split_combined_bom"] is True
    assert manifest["split_notes"] is True
    assert manifest["split_index"] is True
    assert manifest["title_metadata"] == {"pn": "P1"}
    manifest_paths = {entry["path"] for entry in manifest["documents"]}
    assert "doc1.document.yaml" in manifest_paths
    assert "nested/doc2.document.yaml" in manifest_paths
