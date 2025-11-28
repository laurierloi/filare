from filare.models.bom import BomContent, BomEntry, BomRenderOptions
from filare.models.partnumber import PartNumberInfo
from filare.models.numbers import NumberAndUnit
from filare.models.dataclasses import BomCategory


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
        category=BomCategory.ADDITIONAL,
        designators=["X1"],
    )
    content = BomContent({hash(entry): entry})
    render = content.get_bom_render(options=BomRenderOptions(filter_entries=True))
    headers = render.headers
    assert "#" in headers and "Description" in headers
    assert len(render.rows) == 1
