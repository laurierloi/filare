import pytest

from filare.models.templates import (
    FakeTerminationTableTemplateFactory,
    TerminationTableTemplateModel,
)
from filare.render.templates import get_template


def test_termination_table_render_rows():
    model = FakeTerminationTableTemplateFactory(row_count=2)()
    assert isinstance(model, TerminationTableTemplateModel)

    rendered = get_template("termination_table.html").render(model.to_render_dict())

    for row in model.rows:
        assert row.source in rendered
        assert row.target in rendered
        assert row.source_termination in rendered
        assert row.target_termination in rendered


@pytest.mark.render
@pytest.mark.parametrize("row_count", [1, 4])
def test_termination_table_row_variants(row_count):
    model = FakeTerminationTableTemplateFactory(row_count=row_count)()
    rendered = get_template("termination_table.html").render(model.to_render_dict())

    assert rendered.count("<tr>") >= row_count
