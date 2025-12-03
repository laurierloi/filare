from filare.models.bom import BomEntry, BomRender, BomRenderOptions
from filare.models.numbers import NumberAndUnit
from filare.models.partnumber import PartNumberInfo


def make_entry(desc="Widget", qty=1, designators=None, per_harness=None):
    return BomEntry(
        id="1",
        qty=NumberAndUnit(qty),
        partnumbers=PartNumberInfo(),
        description=desc,
        designators=designators or [],
        per_harness=per_harness or {},
    )


def test_bom_entry_as_list_and_strings():
    entry = make_entry(desc="LongDescription" * 5, qty=2, designators=["A", "B", "C"])
    entry.restrict_printed_lengths = True
    lst = entry.as_list()
    assert lst[1] == 2  # qty number
    assert "..." in lst[3]  # description truncated
    assert "A, B" in lst[4] and "..." in lst[4]

    entry.restrict_printed_lengths = False
    assert entry.description_clean.startswith("LongDescription")
    assert entry.designators_str.endswith("C")


def test_bom_entry_per_harness_scaling():
    entry = make_entry(per_harness={"H1": {"qty": 1}})
    entry.scale_per_harness({"H1": 2})
    assert entry.per_harness["H1"]["qty"] == 2


def test_bom_render_strip_empty_columns():
    entries = [
        make_entry(desc="Item1", qty=1, designators=["X1"]),
        make_entry(desc="Item2", qty=2, designators=["X2"]),
    ]
    render = BomRender(
        header=["#", "Qty", "Unit", "Description", "Designators", ""],
        rows=[e.as_list() + [""] for e in entries],
        strip_empty_columns=True,
    )
    rendered = render.render(page_options={}, bom_options=BomRenderOptions())
    assert "Item1" in rendered
    assert "Item2" in rendered


def test_bom_render_as_tsv():
    entries = [
        make_entry(desc="Item1", qty=1, designators=["X1"]),
        make_entry(desc="Item2", qty=2, designators=["X2"]),
    ]
    render = BomRender(
        header=["#", "Qty", "Unit", "Description", "Designators"],
        rows=[e.as_list() for e in entries],
    )
    tsv = render.as_tsv()
    assert "Item1" in tsv
    assert "Item2" in tsv
