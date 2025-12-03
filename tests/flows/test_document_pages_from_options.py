from pathlib import Path

from filare.flows.build_harness import build_harness_from_files
from filare.models.page import BOMPage, CutPage, HarnessPage, TerminationPage, TitlePage


def _write_minimal(tmp_path: Path):
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
    return harness_path, metadata_path


def _build_doc(tmp_path: Path, opts: str):
    harness_path, metadata_path = _write_minimal(tmp_path)
    if opts:
        harness_path.write_text(
            harness_path.read_text()
            + "\noptions:\n"
            + opts
        )
    ret = build_harness_from_files(
        [harness_path],
        [metadata_path],
        output_formats=(),
        output_dir=tmp_path,
        return_types=("document",),
    )
    return ret["document"]


def test_document_pages_default(tmp_path: Path):
    doc = _build_doc(tmp_path, "")
    types = [type(p) for p in doc.pages]
    assert TitlePage in types
    assert HarnessPage in types
    assert BOMPage in types
    assert CutPage not in types
    assert TerminationPage not in types


def test_document_pages_with_cut_and_term(tmp_path: Path):
    doc = _build_doc(
        tmp_path,
        "  include_cut_diagram: true\n  include_termination_diagram: true\n",
    )
    types = [type(p) for p in doc.pages]
    assert CutPage in types
    assert TerminationPage in types


def test_document_pages_without_bom(tmp_path: Path):
    doc = _build_doc(tmp_path, "  include_bom: false\n")
    types = [type(p) for p in doc.pages]
    assert BOMPage not in types
