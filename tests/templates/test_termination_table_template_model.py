import pytest

from filare.models.templates import (
    FakeTerminationTableTemplateFactory,
    TerminationTableTemplateModel,
)


def test_termination_table_render_rows():
    model = FakeTerminationTableTemplateFactory(row_count=2)()
    assert isinstance(model, TerminationTableTemplateModel)

    rendered = model.render()

    for row in model.rows:
        assert row.source in rendered
        assert row.target in rendered
        assert row.source_termination in rendered
        assert row.target_termination in rendered


@pytest.mark.render
@pytest.mark.parametrize("row_count", [1, 4])
def test_termination_table_row_variants(row_count):
    model = FakeTerminationTableTemplateFactory(row_count=row_count)()
    rendered = model.render()

    assert rendered.count("<tr>") >= row_count
