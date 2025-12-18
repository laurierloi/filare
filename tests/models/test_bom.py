import logging
from typing import Any, List, cast

import pytest
from pydantic import ValidationError

from filare.errors import UnsupportedModelOperation
from filare.models.bom import (
    BomContent,
    BomEntry,
    BomRender,
    BomRenderOptions,
    FakeBomEntryFactory,
)
from filare.models.numbers import NumberAndUnit
from filare.models.partnumber import PartNumberInfo
from filare.models.types import BomCategory


def test_bom_entry_scale_per_harness(bom_entry_sample):
    multipliers = {"H1": 2}
    bom_entry_sample.scale_per_harness(multipliers)
    assert bom_entry_sample.qty.number == 2
    assert bom_entry_sample.per_harness["H1"]["qty"].number == 2


def test_bom_content_render_filters_columns():
    entry = BomEntry(
        qty=NumberAndUnit(1, None),
        partnumbers=PartNumberInfo(pn="PN-TEST"),
        id="1",
        description="Test",
        category=str(BomCategory.ADDITIONAL),
        designators=["X1"],
    )
    content = BomContent({hash(entry): entry})
    render = content.get_bom_render(options=BomRenderOptions(filter_entries=True))
    headers = render.headers
    assert "#" in headers and "Description" in headers
    assert len(render.rows) == 1


def test_bom_entry_scale_qty_invalid_multiplier_and_amount():
    with pytest.raises(ValidationError):
        entry = BomEntry(
            qty=NumberAndUnit(2, None),
            amount=NumberAndUnit(3, "m"),
            partnumbers=PartNumberInfo(pn="PN"),
            qty_multiplier=cast(Any, "bad"),
        )


def test_bom_entry_add_and_designators_str():
    base = BomEntry(
        qty=NumberAndUnit(1, None),
        partnumbers=PartNumberInfo(pn="A"),
        designators=["D1", "D2", "D3"],
    )
    b = BomEntry(
        qty=NumberAndUnit(2, None),
        partnumbers=PartNumberInfo(pn="A"),
        designators=["D4"],
    )
    a = cast(BomEntry, base + b)
    assert a.qty.number == 3
    assert a.designators_str.endswith("(...)")
    with pytest.raises(UnsupportedModelOperation):
        cast(Any, a).__add__(object())
    assert (a == []) is False
    assert (a == 123) is None
    plus_list = cast(List[BomEntry], cast(Any, a + [b]))
    assert plus_list and plus_list[0].qty.number == 5
    filtered = a.as_list(filter_empty=True, include_per_harness=False)
    assert "" not in filtered


def test_bom_entry_scale_per_harness_warns_once(caplog):
    import filare.models.bom as bom_module

    bom_module.logging = logging
    entry = BomEntry(
        qty=NumberAndUnit(1, None),
        partnumbers=PartNumberInfo(pn="PN"),
        per_harness={"H": {"qty": NumberAndUnit(1, None)}},
    )
    entry.scale_per_harness({"H": 2})
    entry.scaled_per_harness = True
    with caplog.at_level("WARNING"):
        entry.scale_per_harness({"H": 2})
    assert "scale_per_harness()" in caplog.text


def test_bom_content_filters_empty_and_reverse_rows():
    empty = BomEntry(
        qty=NumberAndUnit(0, None),
        partnumbers=PartNumberInfo(pn="PN"),
        id="E",
    )
    good = BomEntry(
        qty=NumberAndUnit(1, None),
        partnumbers=PartNumberInfo(pn="GOOD"),
        id="G",
    )
    content = BomContent({1: empty, 2: good})
    render = content.get_bom_render(options=BomRenderOptions(reverse=True))
    assert len(render.rows) == 1
    assert render.rows[0][0] == "G"
    # ensure filter removes zero-qty entries
    assert all(row[0] != "E" for row in render.rows)


def test_bom_render_strip_empty_columns(tmp_path):
    from filare.models.options import PageOptions

    render = BomRender(
        header=["#", "", "Qty"], rows=[[1, "x", 2]], strip_empty_columns=True
    )
    html = render.render(page_options=PageOptions(), bom_options=BomRenderOptions())
    assert "table" in html.lower()


def test_print_bom_table_outputs(capsys):
    from filare.models.bom import print_bom_table

    entry = BomEntry(
        qty=NumberAndUnit(1, None),
        partnumbers=PartNumberInfo(pn="PN"),
        id="1",
        description="Desc",
        designators=["X1"],
    )
    print_bom_table({1: entry})
    captured = capsys.readouterr().out
    assert "Description" in captured and "Designators" in captured


def test_fake_bom_entry_factory_variants():
    entry = FakeBomEntryFactory.create(qty_multiplier=2, per_harness={"H1": {"qty": 1}})
    assert entry.qty.number >= 2
    assert entry.designators
    assert entry.partnumbers is not None
    content = BomContent({1: entry})
    render = content.get_bom_render(options=BomRenderOptions(filter_entries=True))
    assert render.rows and render.headers
