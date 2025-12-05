import json
import textwrap

import yaml

from filare.cli import cli
from filare.models.bom import BomEntry
from filare.models.numbers import NumberAndUnit
from filare.models.partnumber import PartNumberInfo
from filare.render.html import generate_shared_bom


def _write_metadata(path, pn="VERIF-HARNESS"):
    path.write_text(
        textwrap.dedent(
            f"""\
            metadata:
              pn: {pn}
              company: TestCo
              address: Test Street
              authors: {{}}
              revisions: {{}}
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


def test_cli_generates_bom_and_document_representation(tmp_path):
    output_dir = tmp_path / "out"
    output_dir.mkdir()

    metadata_path = tmp_path / "metadata.yml"
    harness_path = tmp_path / "verification.yml"
    _write_metadata(metadata_path, pn="VERIF")
    _write_simple_harness(harness_path)

    cli.callback(  # type: ignore[attr-defined]
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


def test_shared_bom_respects_quantity_multipliers(tmp_path):
    multiplier_file = tmp_path / "quantity_multipliers.txt"
    multiplier_file.write_text(json.dumps({"H1": 3}))
    harness_file = tmp_path / "H1.yml"
    harness_file.write_text("connectors: {}")

    entry = BomEntry(
        qty=NumberAndUnit(number=1, unit=None),
        partnumbers=PartNumberInfo(pn="PN-1"),
        description="Test component",
        category="CON",
        designators=["J1"],
    )
    entry.per_harness = {"H1": {"qty": NumberAndUnit(number=1, unit=None)}}
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
    assert "H1:3" in tsv.replace(" ", ""), "Per-harness quantity should scale"
