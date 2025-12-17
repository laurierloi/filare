import pytest

from filare.models.templates import (
    FakeIndexTableTemplateFactory,
    IndexTableTemplateModel,
)


def test_index_table_render_minimal():
    model = FakeIndexTableTemplateFactory(row_count=2)()
    assert isinstance(model, IndexTableTemplateModel)

    rendered = model.render()

    assert model.index_table.header[0] in rendered
    assert model.options.index_table_title in rendered
    for row in model.index_table.rows:
        for item in row.items:
            assert item in rendered


@pytest.mark.render
def test_index_table_pdf_items_used_when_flag_enabled():
    model = FakeIndexTableTemplateFactory(row_count=1)()
    model.options.for_pdf = True

    rendered = model.render()

    pdf_items = model.index_table.rows[0].pdf_items
    assert pdf_items is not None
    for item in pdf_items:
        assert item in rendered


@pytest.mark.render
@pytest.mark.parametrize(
    "index_table_on_right,show_bom,index_table_updated_position,for_pdf",
    [
        (False, False, None, False),
        (True, False, None, False),
        (False, True, None, False),
        (True, True, "top: 30mm; right: 15mm;", False),
        (False, False, "top: 10mm; left: 5mm;", True),
    ],
)
def test_index_table_positioning(
    index_table_on_right, show_bom, index_table_updated_position, for_pdf
):
    model = FakeIndexTableTemplateFactory(row_count=1)()
    model.options.index_table_on_right = index_table_on_right
    model.options.show_bom = show_bom
    model.options.index_table_updated_position = index_table_updated_position
    model.options.for_pdf = for_pdf

    rendered = model.render()

    # Ensure table content renders regardless of positioning flags
    for item in model.index_table.rows[0].get_items(model.options.for_pdf):
        assert item in rendered
    # Row height should appear in CSS
    assert str(model.options.index_table_row_height) in rendered
    # Positioning rules reflected in style
    if index_table_updated_position:
        assert index_table_updated_position in rendered
    elif index_table_on_right and not show_bom:
        assert "right: 20mm" in rendered
    elif show_bom and not index_table_on_right:
        assert (
            f"top: {20 + (model.options.bom_rows + 2) * model.options.bom_row_height}"
            in rendered
            or "left: 10mm" in rendered
        )
    # PDF flag influences which items are chosen
    if for_pdf:
        pdf_items = model.index_table.rows[0].pdf_items
        assert pdf_items
        for item in pdf_items:
            assert item in rendered
