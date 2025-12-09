import json
import textwrap

import pytest
import yaml

from filare.cli import cli, render_callback
from filare.errors import FilareToolsException
from filare.models.bom import BomEntry
from filare.models.harness import Harness
from filare.models.notes import Notes
from filare.models.numbers import NumberAndUnit
from filare.models.options import PageOptions
from filare.models.partnumber import PartNumberInfo
from filare.render.html import generate_shared_bom


def _write_metadata(path, pn="VERIF-HARNESS"):
    path.write_text(
        textwrap.dedent(
            f"""\
            metadata:
              title: Verification Harness
              pn: {pn}
              company: TestCo
              address: Test Street
              authors: {{}}
              revisions:
                A: {{name: init, date: 2024-01-01, changelog: created}}
              template:
                name: din-6771
                sheetsize: A4
            """
        )
    )


def _write_simple_harness(path):
    path.write_text(
        textwrap.dedent(
            """\
            connectors:
              J1:
                pincount: 2
              J2:
                pincount: 2

            cables:
              W1:
                wirecount: 2

            connections:
              -
                - J1: [1, 2]
                - W1: [1, 2]
                - J2: [1, 2]
            """
        )
    )


@pytest.mark.functional
def test_cli_generates_bom_and_document_representation(tmp_path):
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    metadata_path = tmp_path / "metadata.yml"
    harness_path = tmp_path / "verification.yml"
    _write_metadata(metadata_path, pn="VERIF")
    _write_simple_harness(harness_path)

    render_callback(
        files=(harness_path,),
        formats="tb",  # harness BOM + shared BOM
        components=(),
        metadata=(metadata_path,),
        output_dir=output_dir,
        output_name=None,
        version=False,
        use_qty_multipliers=False,
        multiplier_file_name="quantity_multipliers.txt",
    )

    bom_path = output_dir / "verification.tsv"
    shared_bom_path = output_dir / "shared_bom.tsv"
    doc_path = output_dir / "verification.document.yaml"

    assert bom_path.exists(), "Harness BOM was not generated"
    assert shared_bom_path.exists(), "Shared BOM was not generated"
    assert doc_path.exists(), "Document representation was not emitted"

    bom_text = bom_path.read_text()
    header_line = bom_text.splitlines()[0] if bom_text else ""
    assert "Qty" in header_line and "Description" in header_line
    if len(bom_text.splitlines()) > 1:
        # When entries exist, ensure they reference harness elements.
        assert any(token in bom_text for token in ("J1", "J2", "W1", "Wire"))

    doc_data = yaml.safe_load(doc_path.read_text())
    page_types = {page["type"] for page in doc_data.get("pages", [])}
    assert {"title", "harness", "bom"} <= page_types
    assert doc_data["metadata"]["pn"] == "VERIF"
    assert any("verification" in name for name in doc_data["metadata"]["files"])


@pytest.mark.functional
def test_shared_bom_respects_quantity_multipliers(tmp_path):
    multiplier_file = tmp_path / "quantity_multipliers.txt"
    multiplier_file.write_text(json.dumps({"h1": 3}))
    harness_file = tmp_path / "h1.yml"
    harness_file.write_text("connectors: {}")

    entry = BomEntry(
        qty=NumberAndUnit(number=1, unit=None),
        partnumbers=PartNumberInfo(pn="PN-1"),
        description="Test component",
        category="CON",
        designators=["J1"],
    )
    entry.per_harness = {"h1": {"qty": NumberAndUnit(number=1, unit=None)}}
    shared_bom = {hash(entry): entry}

    shared_bom_base = generate_shared_bom(
        output_dir=tmp_path,
        shared_bom=shared_bom,
        use_qty_multipliers=True,
        files=[harness_file],
        multiplier_file_name=multiplier_file.name,
    )

    assert shared_bom_base == tmp_path / "shared_bom"
    tsv = (tmp_path / "shared_bom.tsv").read_text()
    assert "Test component" in tsv
    assert "h1:3" in tsv.lower().replace(" ", ""), "Per-harness quantity should scale"


@pytest.mark.functional
def test_cli_shared_bom_scales_with_multiplier_file(tmp_path):
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    multiplier_file = output_dir / "quantity_multipliers.txt"
    multiplier_file.write_text(json.dumps({"h1": 3}))

    metadata_path = tmp_path / "metadata.yml"
    harness_path = tmp_path / "h1.yml"
    _write_metadata(metadata_path, pn="h1")
    harness_path.write_text(
        textwrap.dedent(
            """\
            connectors:
              J1:
                pincount: 1
                pn: CON-1
              J2:
                pincount: 1
                pn: CON-2
            cables:
              W1:
                wirecount: 1
                pn: CAB-1
                length: 1
            connections:
              -
                - J1: 1
                - W1: 1
                - J2: 1
            additional_bom_items:
              - type: Sleeve
                pn: SLV-1
                qty: 2
            """
        )
    )

    render_callback(
        files=(harness_path,),
        formats="tb",
        components=(),
        metadata=(metadata_path,),
        output_dir=output_dir,
        output_name=None,
        version=False,
        use_qty_multipliers=True,
        multiplier_file_name=multiplier_file.name,
    )

    shared_bom_text = (output_dir / "shared_bom.tsv").read_text()
    normalized = shared_bom_text.lower().replace(" ", "")
    assert "h1:3" in normalized
    assert "sleeve" in normalized


@pytest.mark.functional
def test_multi_harness_html_and_shared_outputs(tmp_path):
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    metadata_path = tmp_path / "metadata.yml"
    harness_a = tmp_path / "h1.yml"
    harness_b = tmp_path / "h2.yml"

    _write_metadata(metadata_path, pn="MULTI")
    _write_simple_harness(harness_a)
    _write_simple_harness(harness_b)

    render_callback(
        files=(harness_a, harness_b),
        formats="hb",
        components=(),
        metadata=(metadata_path,),
        output_dir=output_dir,
        output_name=None,
        version=False,
        use_qty_multipliers=False,
        multiplier_file_name="quantity_multipliers.txt",
    )

    expected_files = [
        output_dir / "titlepage.html",
        output_dir / "h1.html",
        output_dir / "h2.html",
        output_dir / "shared_bom.tsv",
    ]
    for f in expected_files:
        assert f.exists(), f"Missing expected output {f}"

    shared_bom = (output_dir / "shared_bom.tsv").read_text()
    assert "MULTI-h1" in shared_bom and "MULTI-h2" in shared_bom


@pytest.mark.functional
def test_multi_harness_pdf_bundle(tmp_path):
    pytest.importorskip("weasyprint")

    output_dir = tmp_path / "out"
    output_dir.mkdir()

    metadata_path = tmp_path / "metadata.yml"
    harness_a = tmp_path / "h1.yml"
    harness_b = tmp_path / "h2.yml"

    _write_metadata(metadata_path, pn="PDFMULTI")
    _write_simple_harness(harness_a)
    _write_simple_harness(harness_b)

    render_callback(
        files=(harness_a, harness_b),
        formats="hP",
        components=(),
        metadata=(metadata_path,),
        output_dir=output_dir,
        output_name=None,
        version=False,
        use_qty_multipliers=False,
        multiplier_file_name="quantity_multipliers.txt",
    )

    pdf_path = (output_dir / output_dir.name).with_suffix(".pdf")
    assert pdf_path.exists(), f"Expected combined PDF {pdf_path}"


@pytest.mark.functional
def test_cli_skips_bom_when_disabled(tmp_path):
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    metadata_path = tmp_path / "metadata.yml"
    harness_path = tmp_path / "no_bom.yml"
    _write_metadata(metadata_path, pn="NOBOM")
    harness_path.write_text(
        textwrap.dedent(
            """\
            options:
              include_bom: false
            connectors:
              J1: {pincount: 1}
              J2: {pincount: 1}
            cables:
              W1: {wirecount: 1}
            connections:
              -
                - J1: 1
                - W1: 1
                - J2: 1
            """
        )
    )

    render_callback(
        files=(harness_path,),
        formats="th",
        components=(),
        metadata=(metadata_path,),
        output_dir=output_dir,
        output_name=None,
        version=False,
        use_qty_multipliers=False,
        multiplier_file_name="quantity_multipliers.txt",
    )

    assert not (output_dir / "no_bom.tsv").exists()
    assert (output_dir / "no_bom.html").exists()


@pytest.mark.functional
def test_cli_split_sections_emit_split_files(tmp_path):
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    metadata_path = tmp_path / "metadata.yml"
    harness_path = tmp_path / "split.yml"
    _write_metadata(metadata_path, pn="SPLIT")
    harness_path.write_text(
        textwrap.dedent(
            """\
            options:
              split_bom_page: true
              split_notes_page: true
              split_index_page: true
            notes:
              - SplitNote
            connectors:
              J1: {pincount: 1}
              J2: {pincount: 1}
            cables:
              W1: {wirecount: 1}
            connections:
              -
                - J1: 1
                - W1: 1
                - J2: 1
            """
        )
    )

    render_callback(
        files=(harness_path,),
        formats="h",
        components=(),
        metadata=(metadata_path,),
        output_dir=output_dir,
        output_name=None,
        version=False,
        use_qty_multipliers=False,
        multiplier_file_name="quantity_multipliers.txt",
    )

    base = output_dir / "split"
    for suffix in (".html", ".bom.html", ".notes.html"):
        assert base.with_suffix(suffix).exists(), f"Missing split output {suffix}"

    notes_html = base.with_suffix(".notes.html").read_text()
    assert "SplitNote" in notes_html


def test_shared_bom_missing_multiplier_errors(tmp_path):
    multiplier_file = tmp_path / "quantity_multipliers.txt"
    multiplier_file.write_text(json.dumps({}))
    harness_file = tmp_path / "H1.yml"
    harness_file.write_text("connectors: {}")

    entry = BomEntry(
        qty=NumberAndUnit(number=1, unit=None),
        partnumbers=PartNumberInfo(pn="PN-ERR"),
        description="Test component",
        category="CON",
        designators=["J1"],
    )
    entry.per_harness = {"H1": {"qty": NumberAndUnit(number=1, unit=None)}}
    shared_bom = {hash(entry): entry}

    with pytest.raises(FilareToolsException):
        generate_shared_bom(
            output_dir=tmp_path,
            shared_bom=shared_bom,
            use_qty_multipliers=True,
            files=[harness_file],
            multiplier_file_name=multiplier_file.name,
        )

    assert not (tmp_path / "shared_bom.tsv").exists()


def test_orient_connectors_overview_sets_ports(basic_metadata):
    harness = Harness(
        metadata=basic_metadata,
        options=PageOptions(),
        notes=Notes(),
        shared_bom={},
    )
    harness.add_connector("X1", pincount=1)
    harness.add_connector("X2", pincount=1)
    harness.add_cable("W1", wirecount=1)
    harness.connect("X1", 1, "W1", 1, "X2", 1)

    harness.orient_connectors_overview()

    assert harness.connectors["X1"].ports_right is True
    assert harness.connectors["X1"].ports_left is False
    assert harness.connectors["X2"].ports_left is True
    assert harness.connectors["X2"].ports_right is False


@pytest.mark.functional
def test_cli_additional_bom_items_included(tmp_path):
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    metadata_path = tmp_path / "metadata.yml"
    harness_path = tmp_path / "with_additional.yml"
    _write_metadata(metadata_path, pn="ADD")
    harness_path.write_text(
        textwrap.dedent(
            """\
            connectors:
              J1: {pincount: 1}
              J2: {pincount: 1}
            cables:
              W1: {wirecount: 1}
            connections:
              -
                - J1: 1
                - W1: 1
                - J2: 1
            additional_bom_items:
              - type: Sleeve
                qty: 2
                pn: SLV-1
            """
        )
    )

    render_callback(
        files=(harness_path,),
        formats="tb",
        components=(),
        metadata=(metadata_path,),
        output_dir=output_dir,
        output_name=None,
        version=False,
        use_qty_multipliers=False,
        multiplier_file_name="quantity_multipliers.txt",
    )

    bom_text = (output_dir / "with_additional.tsv").read_text()
    shared_bom_text = (output_dir / "shared_bom.tsv").read_text()
    assert "Sleeve" in bom_text
    assert "Sleeve" in shared_bom_text
