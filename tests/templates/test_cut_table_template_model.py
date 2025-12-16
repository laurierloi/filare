import pytest

from filare.models.templates import CutTableTemplateModel, FakeCutTableTemplateFactory
from filare.render.templates import get_template


def test_cut_table_render_rows():
    model = FakeCutTableTemplateFactory(row_count=3)()

    assert isinstance(model, CutTableTemplateModel)
    rendered = get_template("cut_table.html").render(model.to_render_dict())

    for row in model.rows:
        assert row.wire in rendered
        assert row.partno in rendered
        assert str(row.color) in rendered
        assert row.length in rendered


@pytest.mark.render
@pytest.mark.parametrize("row_count", [1, 5])
def test_cut_table_row_variants(row_count):
    model = FakeCutTableTemplateFactory(row_count=row_count)()
    rendered = get_template("cut_table.html").render(model.to_render_dict())

    assert rendered.count("<tr>") >= row_count
