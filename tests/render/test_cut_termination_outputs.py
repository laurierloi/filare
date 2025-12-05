import shutil
from pathlib import Path

import pytest

from filare.flows.build_harness import build_harness_from_files

pytestmark = pytest.mark.skipif(
    shutil.which("dot") is None, reason="Graphviz dot executable not found"
)


def _write_minimal(tmp_path: Path, with_cut: bool, with_term: bool):
    harness_path = tmp_path / "h.yml"
    metadata_path = tmp_path / "m.yml"
    options = []
    if with_cut:
        options.append("  include_cut_diagram: true")
    if with_term:
        options.append("  include_termination_diagram: true")
    options_block = "\noptions:\n" + "\n".join(options) if options else ""
    harness_path.write_text(
        "connectors:\n"
        "  J1:\n"
        "    pincount: 1\n"
        "connections:\n"
        "  -\n"
        "    - J1: [1]\n"
        f"{options_block}\n"
    )
    metadata_path.write_text(
        "metadata:\n"
        "  pn: T\n"
        "  title: H\n"
        "  company: ACME\n"
        "  address: 1 Road\n"
        "  sheet_total: 1\n"
        "  sheet_current: 1\n"
        "  sheet_name: h\n"
        "  output_dir: .\n"
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
    return harness_path, metadata_path


def _build(tmp_path: Path, with_cut: bool, with_term: bool) -> Path:
    h, m = _write_minimal(tmp_path, with_cut, with_term)
    build_harness_from_files(
        [h],
        [m],
        output_formats=("html",),
        output_dir=tmp_path,
    )
    return tmp_path / "h"


def test_cut_and_termination_pages_generated(tmp_path):
    base = _build(tmp_path, True, True)
    assert base.with_suffix(".cut.html").exists()
    assert base.with_suffix(".termination.html").exists()
    cut_html = base.with_suffix(".cut.html").read_text(encoding="utf-8")
    term_html = base.with_suffix(".termination.html").read_text(encoding="utf-8")
    assert "Cut Diagram" in cut_html
    assert "Termination Diagram" in term_html


def test_cut_and_termination_pages_not_generated_when_disabled(tmp_path):
    base = _build(tmp_path, False, False)
    assert not base.with_suffix(".cut.html").exists()
    assert not base.with_suffix(".termination.html").exists()
