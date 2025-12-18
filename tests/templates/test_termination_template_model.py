import pytest

from filare.models.templates import FakeTerminationTemplateFactory
from filare.models.templates.termination_template_model import TerminationTemplateModel


def test_termination_template_render_includes_table():
    model = FakeTerminationTemplateFactory(row_count=2)()

    assert isinstance(model, TerminationTemplateModel)
    rendered = model.render()

    assert "Termination Diagram" in rendered
    assert model.termination_table is not None
    assert "<table" in rendered


@pytest.mark.render
@pytest.mark.parametrize("row_count", [1, 4])
def test_termination_template_row_counts(row_count):
    model = FakeTerminationTemplateFactory(row_count=row_count)()
    rendered = model.render()

    assert "termination-table" in rendered
    assert "<td>" in rendered
