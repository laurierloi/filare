import json
from pathlib import Path

from filare.index_table import IndexTable, IndexTableRow
from filare.models.metadata import PagesMetadata


def test_index_table_row_items_and_formatting():
    content_row = IndexTableRow(
        sheet=1,
        page="index",
        content="Index page",
        link="index.html",
        use_quantity=False,
    )
    assert content_row.get_items(for_pdf=True) == ("index", "Index page", "index.html")

    qty_row = IndexTableRow(sheet=2, page="h1", quantity=3, notes="note")
    assert qty_row.get_items() == (
        2,
        "<a href=h1.html>h1</a>",
        3,
        "note",
    )

    no_qty_row = IndexTableRow(
        sheet=3,
        page="custom.html",
        notes="n/a",
        use_quantity=False,
        link="custom.html",
    )
    assert no_qty_row.get_items() == (
        3,
        "<a href=custom.html>custom.html</a>",
        "n/a",
    )


def test_get_index_table_header_respects_quantity_flag(tmp_path):
    assert tuple(IndexTable.get_index_table_header()) == ("Sheet", "Page", "Notes")

    metadata = PagesMetadata(
        titlepage=Path("titlepage"),
        output_names=[],
        files=[],
        use_qty_multipliers=True,
        multiplier_file_name="quantity_multipliers.txt",
        output_dir=tmp_path,
    )
    assert tuple(IndexTable.get_index_table_header(metadata)) == (
        "Sheet",
        "Page",
        "Quantity",
        "Notes",
    )


def test_from_pages_metadata_without_splits_uses_multipliers(tmp_path):
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    harness_file = output_dir / "h1.yml"
    harness_file.write_text("dummy")
    (output_dir / "quantity_multipliers.txt").write_text(json.dumps({"h1": 4}))

    metadata = PagesMetadata(
        titlepage=Path("titlepage"),
        output_names=["titlepage", "h1"],
        files=[harness_file],
        use_qty_multipliers=True,
        multiplier_file_name="quantity_multipliers.txt",
        pages_notes={"h1": "Note"},
        output_dir=output_dir,
    )

    table = IndexTable.from_pages_metadata(metadata)

    assert tuple(table.header) == ("Sheet", "Page", "Quantity", "Notes")
    assert [row.sheet for row in table.rows] == [1, 2]
    assert table.rows[0].quantity == ""
    assert table.rows[1].quantity == 4
    assert table.rows[1].notes == "Note"


def test_from_pages_metadata_with_split_pages(tmp_path):
    output_dir = tmp_path / "out"
    output_dir.mkdir()
    (output_dir / "h1.bom.html").write_text("bom")
    harness_file = output_dir / "h1.yml"
    harness_file.write_text("dummy")

    metadata = PagesMetadata(
        titlepage=Path("titlepage"),
        output_names=["h1"],
        files=[harness_file],
        use_qty_multipliers=False,
        multiplier_file_name="quantity_multipliers.txt",
        pages_notes={"h1": "Note"},
        output_dir=output_dir,
    )

    table = IndexTable.from_pages_metadata(metadata)

    assert table.header == ("Name", "Content", "Page")
    assert [row.content for row in table.rows] == ["Index page", "Harness", "BOM"]
    assert table.rows[0].get_formatted_page(for_pdf=False) == "<a href=titlepage.html>titlepage.html</a>"
    assert table.rows[2].link == "h1.bom.html"
