import pytest

from filare.models.templates import (
    FakeSimpleConnectorTemplateFactory,
    SimpleConnectorTemplateModel,
)


def test_simple_connector_template_render_minimal():
    model = FakeSimpleConnectorTemplateFactory()()
    assert isinstance(model, SimpleConnectorTemplateModel)

    rendered = model.render()

    assert model.component.type.clean in rendered
    assert str(model.component.pincount) in rendered
    assert model.component.pins_to_show()[0].id in rendered


@pytest.mark.render
def test_simple_connector_without_color():
    model = FakeSimpleConnectorTemplateFactory(show_color=False)()
    rendered = model.render()

    assert "colorbar" not in rendered or model.component.color is None
