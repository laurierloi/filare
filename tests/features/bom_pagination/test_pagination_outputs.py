from pathlib import Path

from filare.flows.build_harness import build_harness_from_files


def _write_metadata(tmp_path: Path) -> Path:
    metadata_path = tmp_path / "m.yml"
    metadata_path.write_text(
        "metadata:\n"
        "  pn: PAGETEST\n"
        "  title: Harness Paginated BOM\n"
        "  company: ACME\n"
        "  address: 1 Road\n"
        "  sheet_total: 1\n"
        "  sheet_current: 1\n"
        "  sheet_name: h\n"
        f"  output_dir: {tmp_path}\n"
        "  titlepage: t\n"
        "  output_names: [h]\n"
        "  files: [h.yml]\n"
        "  use_qty_multipliers: false\n"
        "  multiplier_file_name: qty.txt\n"
        "  revisions:\n"
        "    a:\n"
        "      name: tester\n"
        "      date: 2024-01-01\n"
        "      changelog: init\n"
    )
    return metadata_path


def _run_build(tmp_path: Path, harness_body: str) -> Path:
    harness_path = tmp_path / "h.yml"
    harness_path.write_text(harness_body)
    metadata_path = _write_metadata(tmp_path)
    build_harness_from_files(
        [harness_path],
        [metadata_path],
        output_formats=("html",),
        output_dir=tmp_path,
        extra_metadata={"output_dir": tmp_path},
    )
    return tmp_path / "h"


def test_bom_pagination_outputs_lettered_pages(tmp_path):
    base = _run_build(
        tmp_path,
        "connectors:\n"
        "  J1:\n"
        "    pincount: 1\n"
        "    pn: J1PN\n"
        "  J2:\n"
        "    pincount: 1\n"
        "    pn: J2PN\n"
        "cables:\n"
        "  C1:\n"
        "    wirecount: 1\n"
        "    length: 1\n"
        "    pn: C1PN\n"
        "connections:\n"
        "  -\n"
        "    - J1: [1]\n"
        "    - C1: [1]\n"
        "    - J2: [1]\n"
        "options:\n"
        "  split_bom_page: true\n"
        "  split_index_page: true\n"
        "  bom_rows_per_page: 1\n"
        "  table_page_suffix_letters: true\n",
    )

    assert base.with_suffix(".bom.html").exists()
    assert base.with_suffix(".bom.b.html").exists()
    assert base.with_suffix(".bom.c.html").exists()
    assert not base.with_suffix(".bom.a.html").exists()

    index_html = base.with_suffix(".index.html").read_text(encoding="utf-8")
    assert "h.bom.a" in index_html
    assert "h.bom.b" in index_html
    assert "h.bom.c" in index_html


def test_cut_pagination_adds_lettered_pages_and_sheet_suffix(tmp_path):
    base = _run_build(
        tmp_path,
        "connectors:\n"
        "  J1:\n"
        "    pincount: 3\n"
        "  J2:\n"
        "    pincount: 3\n"
        "cables:\n"
        "  C1:\n"
        "    wirecount: 3\n"
        "    colors: [RD, BK, GN]\n"
        "    length: 5\n"
        "connections:\n"
        "  -\n"
        "    - J1: [1, 2, 3]\n"
        "    - C1: [1, 2, 3]\n"
        "    - J2: [1, 2, 3]\n"
        "options:\n"
        "  include_cut_diagram: true\n"
        "  split_index_page: true\n"
        "  cut_rows_per_page: 1\n"
        "  table_page_suffix_letters: true\n",
    )

    assert base.with_suffix(".cut.a.html").exists()
    assert base.with_suffix(".cut.b.html").exists()
    assert base.with_suffix(".cut.c.html").exists()

    cut_html = base.with_suffix(".cut.a.html").read_text(encoding="utf-8")
    assert "Sheet 1a" in cut_html

    index_html = base.with_suffix(".index.html").read_text(encoding="utf-8")
    assert "h.cut.a" in index_html
    assert "h.cut.b" in index_html
    assert "h.cut.c" in index_html
