import pathlib
from pathlib import Path
from types import SimpleNamespace

import pytest

from filare.flows.index_pages import build_pdf_bundle, build_titlepage
from filare.flows.shared_bom import build_shared_bom
from filare.index_table import IndexTable
from filare.models.metadata import PagesMetadata


def test_build_shared_bom_invokes_render(monkeypatch, tmp_path):
    called = {}

    def fake_generate_shared_bom(**kwargs):
        called["args"] = kwargs
        return tmp_path / "shared_bom"

    monkeypatch.setattr(
        "filare.flows.shared_bom.generate_shared_bom", fake_generate_shared_bom
    )
    out = build_shared_bom(
        tmp_path,
        {"bom": "v"},
        use_qty_multipliers=True,
        files=[tmp_path / "a"],
        multiplier_file_name="m.txt",
    )
    assert out == tmp_path / "shared_bom"
    assert called["args"]["use_qty_multipliers"] is True


def test_build_titlepage_uses_metadata(monkeypatch, tmp_path):
    meta = tmp_path / "meta.yml"
    meta.write_text("metadata: {title: t, template: {name: din-6771}}")
    called = {}

    def fake_generate_titlepage(yaml_data, extra_metadata, shared_bom, for_pdf=False):
        called["for_pdf"] = for_pdf
        called["yaml_data"] = yaml_data

    monkeypatch.setattr(
        "filare.flows.index_pages.generate_titlepage", fake_generate_titlepage
    )
    build_titlepage([meta], {"titlepage": tmp_path / "titlepage"}, {"bom": "v"})
    assert called["for_pdf"] is False
    build_titlepage(
        [meta], {"titlepage": tmp_path / "titlepage"}, {"bom": "v"}, for_pdf=True
    )
    assert called["for_pdf"] is True


def test_build_titlepage_with_harness_metadata_only(tmp_path):
    example = Path("examples/demo01.yml")
    extra_metadata = {
        "output_dir": tmp_path,
        "files": [example],
        "output_names": ["titlepage", example.stem],
        "sheet_total": 2,
        "sheet_current": 3,
        "use_qty_multipliers": False,
        "multiplier_file_name": "quantity_multipliers.txt",
        "titlepage": Path("titlepage"),
        "sheet_name": example.stem.upper(),
    }

    build_titlepage([example], extra_metadata, shared_bom={})

    titlepage_html = tmp_path / "titlepage.html"
    assert titlepage_html.exists()
    content = titlepage_html.read_text(encoding="utf-8")
    assert "demo01" in content.lower()


def test_build_pdf_bundle(monkeypatch, tmp_path):
    html_paths = [tmp_path / "a.html"]
    called = {}

    def fake_generate_pdf_output(paths):
        called["paths"] = paths

    monkeypatch.setattr(
        "filare.flows.index_pages.generate_pdf_output", fake_generate_pdf_output
    )
    build_pdf_bundle(html_paths)
    assert called["paths"] == html_paths


def test_index_table_includes_split_links(tmp_path):
    # Seed files to trigger split detection
    (tmp_path / "titlepage.html").write_text("title", encoding="utf-8")
    (tmp_path / "h1.html").write_text("main", encoding="utf-8")
    (tmp_path / "h1.bom.html").write_text("bom", encoding="utf-8")
    (tmp_path / "h1.notes.html").write_text("notes", encoding="utf-8")
    metadata = PagesMetadata(
        titlepage=Path("titlepage"),
        output_names=["h1"],
        files=["h1.yml"],
        use_qty_multipliers=False,
        multiplier_file_name="qty.txt",
        pages_notes={},
        output_dir=tmp_path,
    )
    table = IndexTable.from_pages_metadata(metadata)
    assert table.header == ("Name", "Content", "Page")
    options = SimpleNamespace(
        for_pdf=False,
        index_table_updated_position="",
        index_table_on_right=True,
        index_table_row_height=4.25,
    )
    rendered = table.render(options)
    assert "h1.bom.html" in rendered
    assert "BOM" in rendered and "Notes" in rendered


def test_index_table_includes_cut_and_termination(tmp_path):
    (tmp_path / "titlepage.html").write_text("title", encoding="utf-8")
    (tmp_path / "h1.html").write_text("main", encoding="utf-8")
    (tmp_path / "h1.cut.html").write_text("cut", encoding="utf-8")
    (tmp_path / "h1.termination.html").write_text("term", encoding="utf-8")
    metadata = PagesMetadata(
        titlepage=Path("titlepage"),
        output_names=["h1"],
        files=["h1.yml"],
        use_qty_multipliers=False,
        multiplier_file_name="qty.txt",
        pages_notes={},
        output_dir=tmp_path,
    )
    table = IndexTable.from_pages_metadata(metadata)
    assert table.header == ("Name", "Content", "Page")
    options = SimpleNamespace(
        for_pdf=False,
        index_table_updated_position="",
        index_table_on_right=True,
        index_table_row_height=4.25,
    )
    rendered = table.render(options)
    assert "h1.cut.html" in rendered
    assert "h1.termination.html" in rendered
    assert "Cut diagram" in rendered and "Termination diagram" in rendered
