import pytest

from filare.models.templates import FakeCutTemplateFactory
from filare.models.templates.cut_template_model import CutTemplateModel
from filare.render.templates import get_template


def test_cut_template_render_includes_table():
    model = FakeCutTemplateFactory(row_count=2)()

    assert isinstance(model, CutTemplateModel)
    rendered = get_template("cut.html").render(model.to_render_dict())

    assert "Cut Diagram" in rendered
    assert model.cut_table is not None
    assert "<table" in model.cut_table
    assert "<table" in rendered


@pytest.mark.render
@pytest.mark.parametrize("row_count", [1, 5])
def test_cut_template_row_counts(row_count):
    model = FakeCutTemplateFactory(row_count=row_count)()
    rendered = get_template("cut.html").render(model.to_render_dict())

    assert "cut-table" in rendered
    assert "<td>" in rendered
