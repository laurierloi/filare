import logging
from pathlib import Path

import pytest
import yaml

from filare.flows.build_harness import build_harness_from_files
from filare.index_table import IndexTable
from filare.models.document import DocumentRepresentation
from filare.models.harness import Harness
from filare.models.metadata import Metadata, PageTemplateConfig, PageTemplateTypes
from filare.models.notes import Notes
from filare.models.options import PageOptions
from filare.models.page import CutPage, HarnessPage, PageType, TitlePage
from filare.render.html import generate_html_output
from filare.settings import settings


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


@pytest.mark.functional
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
    # lock overrides
    reg_data = yaml.safe_load(registry.read_text()) or {}
    reg_data[doc_path.name]["allow_override"] = False
    registry.write_text(yaml.safe_dump(reg_data))

    # Second run should warn and not overwrite
    caplog.clear()
    build_harness_from_files(
        [harness_path],
        [metadata_path],
        output_formats=(),
        output_dir=tmp_path,
        return_types=("document",),
    )
    assert any(
        ("skipping overwrite" in rec.message)
        or ("Document representation locked" in rec.message)
        for rec in caplog.records
    )
    reloaded = yaml.safe_load(doc_path.read_text())
    assert reloaded["metadata"]["pn"] == "USER_EDIT"


def test_document_representation_respected_when_locked(tmp_path: Path):
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

    # Seed a user-authored document and lock it via registry
    doc_path = tmp_path / "h.document.yaml"
    doc_path.write_text(
        yaml.safe_dump({"metadata": {"pn": "USER_DOC"}, "pages": [], "extras": {}})
    )
    registry = tmp_path / "document_hashes.yaml"
    registry.write_text(
        yaml.safe_dump({doc_path.name: {"hash": "ignored", "allow_override": False}})
    )

    ret = build_harness_from_files(
        [harness_path],
        [metadata_path],
        output_formats=(),
        output_dir=tmp_path,
        return_types=("document",),
    )
    assert ret["document"].metadata.get("pn") == "USER_DOC"
    reloaded = yaml.safe_load(doc_path.read_text())
    assert reloaded["metadata"]["pn"] == "USER_DOC"


def test_document_input_controls_generation_when_locked(tmp_path: Path, monkeypatch):
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

    document = DocumentRepresentation(
        metadata={"pn": "DOC"},
        pages=[
            TitlePage(type=PageType.title, name="titlepage"),
            HarnessPage(type=PageType.harness, name="h", formats=["html"]),
            CutPage(type=PageType.cut, name="cut"),
        ],
        extras={"options": {"include_bom": False, "include_cut_diagram": True}},
    )
    doc_path = tmp_path / "h.document.yaml"
    document.to_yaml(doc_path)
    original_doc = doc_path.read_text()
    (tmp_path / "document_hashes.yaml").write_text(
        yaml.safe_dump(
            {doc_path.name: {"hash": document.compute_hash(), "allow_override": False}}
        )
    )

    captured = {}

    def fake_output(self, filename, view=False, cleanup=True, fmt=("html",)):
        captured["fmt"] = fmt
        captured["filename"] = filename

    monkeypatch.setattr(Harness, "output", fake_output)
    ret = build_harness_from_files(
        [harness_path],
        [metadata_path],
        output_formats=("html", "tsv"),
        output_dir=tmp_path,
        return_types=("harness",),
    )

    harness = ret["harness"]
    assert harness.options.include_bom is False
    assert harness.options.show_bom is False
    assert harness.options.include_cut_diagram is True
    assert captured["filename"] == tmp_path / "h"
    assert "html" in captured["fmt"]
    assert "tsv" not in captured["fmt"]
    assert doc_path.read_text() == original_doc


def test_index_generated_only_for_titlepage(tmp_path: Path):
    metadata = Metadata(
        title="T",
        pn="PN",
        company="ACME",
        address="1 Road",
        sheet_total=1,
        sheet_current=1,
        sheet_name="H",
        output_dir=tmp_path,
        output_name="h",
        output_names=["h"],
        files=[tmp_path / "h.yml"],
        use_qty_multipliers=False,
        multiplier_file_name="qty.txt",
        titlepage=Path("titlepage"),
    )
    options = PageOptions(split_index_page=True, show_index_table=True)
    notes = Notes()
    svg_path = tmp_path / "h.svg"
    svg_path.write_text("<svg></svg>")
    generate_html_output(
        tmp_path / "h", bom=[], metadata=metadata, options=options, notes=notes
    )
    assert not (tmp_path / "h.index.html").exists()

    title_metadata = metadata.model_copy(
        update={
            "template": PageTemplateConfig(name=PageTemplateTypes.titlepage),
            "sheet_name": "titlepage",
            "output_name": "titlepage",
            "output_names": ["titlepage", "h"],
        }
    )
    title_options = PageOptions(split_index_page=True, show_index_table=True)
    generate_html_output(
        tmp_path / "titlepage",
        bom=[],
        metadata=title_metadata,
        options=title_options,
        notes=Notes(),
    )
    title_html = (tmp_path / "titlepage.html").read_text()
    assert '<div id="index_table">' not in title_html  # split removes from combined
    assert (tmp_path / "titlepage.index.html").exists()
    assert '<div id="index_table">' in (tmp_path / "titlepage.index.html").read_text()


def test_index_table_lists_split_outputs(tmp_path: Path):
    output_dir = tmp_path
    titlepage = Path("titlepage")
    metadata = Metadata(
        title="T",
        pn="PN",
        company="ACME",
        address="1 Road",
        sheet_total=2,
        sheet_current=1,
        sheet_name="H1",
        output_dir=output_dir,
        output_name="h1",
        output_names=["titlepage", "h1"],
        files=[tmp_path / "h1.yml"],
        use_qty_multipliers=False,
        multiplier_file_name="qty.txt",
        titlepage=titlepage,
    )
    # create split/aux pages
    (output_dir / "h1.html").write_text("harness")
    (output_dir / "h1.bom.html").write_text("bom")
    (output_dir / "h1.cut.html").write_text("cut")
    (output_dir / "h1.termination.html").write_text("term")
    table = IndexTable.from_pages_metadata(metadata)
    header = list(table.header)
    assert header == ["Name", "Content", "Page"]
    contents = {(row.page, row.content) for row in table.rows}
    assert ("h1", "Harness") in contents
    assert ("h1.bom", "BOM") in contents
    assert ("h1.cut", "Cut diagram") in contents
    assert ("h1.termination", "Termination diagram") in contents


def test_cut_and_termination_pages_rendered(tmp_path: Path):
    metadata = Metadata(
        title="T",
        pn="PN",
        company="ACME",
        address="1 Road",
        sheet_total=1,
        sheet_current=1,
        sheet_name="H",
        output_dir=tmp_path,
        output_name="h",
        output_names=["h"],
        files=[tmp_path / "h.yml"],
        use_qty_multipliers=False,
        multiplier_file_name="qty.txt",
        titlepage=Path("titlepage"),
    )
    options = PageOptions(include_cut_diagram=True, include_termination_diagram=True)
    notes = Notes()
    svg_path = tmp_path / "h.svg"
    svg_path.write_text("<svg></svg>")
    generate_html_output(
        tmp_path / "h", bom=[], metadata=metadata, options=options, notes=notes
    )
    assert (tmp_path / "h.cut.html").exists()
    assert (tmp_path / "h.termination.html").exists()
