from filare.models.bom import BomContent, BomEntry, BomRenderOptions
from filare.models.numbers import NumberAndUnit
from filare.models.partnumber import PartNumberInfo


def test_bom_tsv_matches_expected_sample():
    entry = BomEntry(
        qty=NumberAndUnit(number=2, unit=None),
        partnumbers=PartNumberInfo(pn="PN-TEST"),
        id="1",
        description="Test",
        category="ADD",
        designators=["X1"],
    )
    entry.per_harness = {"H1": {"qty": NumberAndUnit(number=2, unit=None)}}
    content = BomContent({hash(entry): entry})
    render = content.get_bom_render(options=BomRenderOptions(filter_entries=True))
    tsv = render.as_tsv().replace(" ", "")
    # Expected TSV header order (allow extra padding from tabulate)
    header_line = tsv.splitlines()[0]
    assert "#\tQty\tUnit\tDescription\tDesignators\tPerHarness" in header_line
    assert "1\t2" in tsv and "Test" in tsv and "X1" in tsv and "H1:2" in tsv
    assert "H1" in tsv
